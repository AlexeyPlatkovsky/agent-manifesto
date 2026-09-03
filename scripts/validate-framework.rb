#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "pathname"
require "set"
require "yaml"

ROOT = Pathname.new(__dir__).join("..").expand_path

def read_yaml(path)
  YAML.safe_load(path.read, permitted_classes: [], permitted_symbols: [], aliases: false)
rescue Psych::SyntaxError => e
  raise "#{path.relative_path_from(ROOT)}: invalid YAML: #{e.message}"
end

def frontmatter(path)
  match = path.read.match(/\A---\s*\n(.*?)\n---\s*\n/m)
  raise "#{path.relative_path_from(ROOT)}: missing YAML frontmatter" unless match

  YAML.safe_load(match[1], permitted_classes: [], permitted_symbols: [], aliases: false)
rescue Psych::SyntaxError => e
  raise "#{path.relative_path_from(ROOT)}: invalid frontmatter: #{e.message}"
end

def schema_ref(root_schema, ref)
  raise "unsupported schema reference #{ref}" unless ref.start_with?("#/")

  ref.delete_prefix("#/").split("/").reduce(root_schema) do |value, segment|
    value.fetch(segment.gsub("~1", "/").gsub("~0", "~"))
  end
end

def type_matches?(value, type)
  case type
  when "object" then value.is_a?(Hash)
  when "array" then value.is_a?(Array)
  when "string" then value.is_a?(String)
  when "boolean" then value == true || value == false
  when "integer" then value.is_a?(Integer)
  else false
  end
end

def validate_schema(value, schema, root_schema, location = "$")
  return validate_schema(value, schema_ref(root_schema, schema.fetch("$ref")), root_schema, location) if schema["$ref"]

  errors = []
  if schema["type"] && !type_matches?(value, schema["type"])
    return ["#{location}: expected #{schema['type']}, got #{value.class}"]
  end

  errors << "#{location}: expected #{schema['const'].inspect}" if schema.key?("const") && value != schema["const"]
  errors << "#{location}: value is not in #{schema['enum'].inspect}" if schema["enum"] && !schema["enum"].include?(value)

  if value.is_a?(String)
    errors << "#{location}: shorter than #{schema['minLength']} characters" if schema["minLength"] && value.length < schema["minLength"]
    errors << "#{location}: does not match #{schema['pattern']}" if schema["pattern"] && !Regexp.new(schema["pattern"]).match?(value)
  end

  if value.is_a?(Integer)
    errors << "#{location}: below minimum #{schema['minimum']}" if schema["minimum"] && value < schema["minimum"]
    errors << "#{location}: above maximum #{schema['maximum']}" if schema["maximum"] && value > schema["maximum"]
  end

  if value.is_a?(Array)
    errors << "#{location}: requires at least #{schema['minItems']} items" if schema["minItems"] && value.length < schema["minItems"]
    errors << "#{location}: items must be unique" if schema["uniqueItems"] && value.uniq.length != value.length
    if schema["items"]
      value.each_with_index do |item, index|
        errors.concat(validate_schema(item, schema["items"], root_schema, "#{location}[#{index}]"))
      end
    end
  end

  if value.is_a?(Hash)
    Array(schema["required"]).each do |key|
      errors << "#{location}: missing required property #{key}" unless value.key?(key)
    end

    properties = schema.fetch("properties", {})
    if schema["additionalProperties"] == false
      (value.keys - properties.keys).each { |key| errors << "#{location}: unknown property #{key}" }
    end

    properties.each do |key, property_schema|
      next unless value.key?(key)

      errors.concat(validate_schema(value[key], property_schema, root_schema, "#{location}.#{key}"))
    end
  end

  errors
end

def dependency_errors(workflow, file)
  steps = workflow.fetch("steps")
  ids = steps.map { |step| step.fetch("id") }
  prefix = file.relative_path_from(ROOT)
  errors = []

  duplicates = ids.group_by(&:itself).select { |_id, occurrences| occurrences.length > 1 }.keys
  duplicates.each { |id| errors << "#{prefix}: duplicate step id #{id}" }

  known = ids.to_set
  graph = {}
  steps.each do |step|
    dependencies = Array(step["needs"])
    dependencies.each do |dependency|
      errors << "#{prefix}: step #{step['id']} needs unknown step #{dependency}" unless known.include?(dependency)
      errors << "#{prefix}: step #{step['id']} depends on itself" if dependency == step["id"]
    end
    graph[step["id"]] = dependencies
  end

  visiting = Set.new
  visited = Set.new
  visit = lambda do |id|
    return if visited.include?(id) || !graph.key?(id)
    if visiting.include?(id)
      errors << "#{prefix}: workflow dependency cycle includes #{id}"
      return
    end

    visiting.add(id)
    graph.fetch(id).each { |dependency| visit.call(dependency) }
    visiting.delete(id)
    visited.add(id)
  end
  ids.each { |id| visit.call(id) }

  errors
end

errors = []

markdown_sources = [
  ROOT.join("MANIFEST.md"),
  ROOT.join("IMPLEMENTATION.md"),
  ROOT.join("README.md"),
  *ROOT.glob("skills/*/SKILL.md"),
  *ROOT.glob("agents/*.md")
]
workflow_files = ROOT.glob("workflows/*.yml")
contract_files = ROOT.glob("contracts/*.schema.json")

expected_version = frontmatter(ROOT.join("MANIFEST.md")).fetch("version")

metadata = {}
markdown_sources.each { |path| metadata[path] = frontmatter(path).fetch("version") }
workflow_files.each { |path| metadata[path] = read_yaml(path).fetch("version") }
contract_files.each do |path|
  metadata[path] = JSON.parse(path.read).fetch("x-framework-version")
rescue JSON::ParserError => e
  errors << "#{path.relative_path_from(ROOT)}: invalid JSON: #{e.message}"
end

metadata.each do |path, version|
  errors << "#{path.relative_path_from(ROOT)}: version #{version.inspect}, expected #{expected_version}" unless version == expected_version
end

workflow_schema_path = ROOT.join("contracts/workflow.schema.json")
workflow_schema = JSON.parse(workflow_schema_path.read)

version_rule = workflow_schema.fetch("properties").fetch("version")
unless validate_schema(expected_version, version_rule, workflow_schema).empty?
  errors << "contracts/workflow.schema.json: version rule rejects the framework version #{expected_version}"
end

skill_records = ROOT.glob("skills/*/SKILL.md").map { |path| [path, frontmatter(path)] }
agent_records = ROOT.glob("agents/*.md").map { |path| [path, frontmatter(path)] }.select { |_path, data| data["name"] }
skill_names = skill_records.map { |_path, data| data.fetch("name") }.to_set
agent_names = agent_records.map { |_path, data| data.fetch("name") }.to_set
contract_names = contract_files.map { |path| path.basename.to_s.delete_suffix(".schema.json") }.to_set

if skill_names.length != skill_records.length
  errors << "skills: frontmatter names must be unique"
end
if agent_names.length != agent_records.length
  errors << "agents: frontmatter names must be unique"
end

agent_records.each do |path, data|
  prefix = path.relative_path_from(ROOT)
  errors << "#{prefix}: missing isolation_reason" unless data["isolation_reason"].is_a?(String) && !data["isolation_reason"].empty?

  contract = data["output_contract"]
  if !contract.is_a?(String) || contract.empty?
    errors << "#{prefix}: missing output_contract"
  elsif !/\A[a-z][a-z0-9-]*\z/.match?(contract)
    errors << "#{prefix}: output_contract must be a schema basename, got #{contract.inspect}"
  elsif !contract_names.include?(contract)
    errors << "#{prefix}: references unknown contract #{contract}"
  end
end

workflow_files.each do |path|
  workflow = read_yaml(path)
  validate_schema(workflow, workflow_schema, workflow_schema).each do |error|
    errors << "#{path.relative_path_from(ROOT)}: #{error}"
  end
  errors.concat(dependency_errors(workflow, path))

  Array(workflow["inputs"]).each do |input|
    errors << "#{path.relative_path_from(ROOT)}: missing input #{input}" unless ROOT.join(input).file?
  end

  workflow.fetch("steps").each do |step|
    Array(step["skills"]).each do |name|
      errors << "#{path.relative_path_from(ROOT)}: step #{step['id']} references unknown skill #{name}" unless skill_names.include?(name)
    end
    if step["agent"] && !agent_names.include?(step["agent"])
      errors << "#{path.relative_path_from(ROOT)}: step #{step['id']} references unknown agent #{step['agent']}"
    end
    %w[input_contract output_contract].each do |key|
      name = step[key]
      next unless name && !contract_names.include?(name)

      errors << "#{path.relative_path_from(ROOT)}: step #{step['id']} references unknown contract #{name}"
    end
  end
end

if errors.empty?
  puts "Framework validation passed at #{expected_version}: #{metadata.length} versioned sources, #{workflow_files.length} workflows."
else
  warn errors.join("\n")
  exit 1
end
