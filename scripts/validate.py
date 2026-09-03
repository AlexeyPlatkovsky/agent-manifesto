#!/usr/bin/env python3
"""Validate an AI landscape, or this framework repository itself.

Uses only the Python standard library so it can run inside any generated
landscape without installing project dependencies.

    python3 scripts/validate.py            # validate the landscape at the repo root
    python3 scripts/validate.py path/to/repo
    python3 scripts/validate.py --quiet    # report failures only

Framework mode adds a version-synchronisation check and is selected
automatically when the target carries this framework's own MANIFEST.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
BUNDLED_WORKFLOW_SCHEMA = SCRIPT_DIR.parent / "contracts" / "workflow.schema.json"

# Where each layer may live. Generated landscapes use native tool locations.
WORKFLOW_GLOBS = ("workflows/*.yml", "workflows/*.yaml", ".claude/workflows/*.yml", ".agent/workflows/*.yml")
SKILL_GLOBS = ("skills/*/SKILL.md", ".claude/skills/*/SKILL.md", ".codex/skills/*/SKILL.md")
AGENT_GLOBS = ("agents/*.md", ".claude/agents/*.md")
CONTRACT_GLOBS = ("contracts/*.schema.json", ".claude/contracts/*.schema.json")

NAME_PATTERN = re.compile(r"\A[a-z][a-z0-9-]*\Z")
FRONTMATTER_PATTERN = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)


# --------------------------------------------------------------------------
# Minimal YAML subset parser
#
# Covers exactly what workflow files and frontmatter use: nested mappings,
# block and inline sequences, comments, quoted scalars, and the >- / | / >
# block scalar styles. Anything outside that subset is reported as an error
# rather than silently misparsed.
# --------------------------------------------------------------------------


class YamlError(Exception):
    pass


def _scalar(raw: str):
    raw = raw.strip()
    if not raw:
        return None
    if raw[0] in "\"'" and len(raw) >= 2 and raw[-1] == raw[0]:
        return raw[1:-1]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [_scalar(item) for item in inner.split(",")] if inner else []
    if raw in ("true", "false"):
        return raw == "true"
    if raw == "null" or raw == "~":
        return None
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if re.fullmatch(r"-?\d+\.\d+", raw):
        return float(raw)
    return raw


def _strip_comment(line: str) -> str:
    out, quote = [], None
    for char in line:
        if quote:
            out.append(char)
            if char == quote:
                quote = None
        elif char in "\"'":
            quote = char
            out.append(char)
        elif char == "#" and (not out or out[-1] in " \t"):
            break
        else:
            out.append(char)
    return "".join(out).rstrip()


def _read_block_scalar(lines, index, indent, style):
    """Consume an indented block scalar, returning (text, next_index)."""
    collected, i = [], index
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            collected.append("")
            i += 1
            continue
        line_indent = len(raw) - len(raw.lstrip(" "))
        if line_indent <= indent:
            break
        collected.append(raw[indent + 1 :] if len(raw) > indent else "")
        i += 1
    while collected and not collected[-1]:
        collected.pop()
    if style.startswith("|"):
        text = "\n".join(line.strip() if False else line for line in collected)
    else:
        # Folded: blank lines become paragraph breaks, others join with a space.
        parts, buffer = [], []
        for line in collected:
            if line.strip():
                buffer.append(line.strip())
            else:
                parts.append(" ".join(buffer))
                buffer = []
        parts.append(" ".join(buffer))
        text = "\n".join(part for part in parts)
    if style.endswith("-"):
        text = text.rstrip("\n")
    elif not text.endswith("\n"):
        text += "\n" if style.endswith("+") else ""
    return text, i


def _parse_block(lines, index, indent):
    """Parse a mapping or sequence at the given indent. Returns (value, index)."""
    container = None
    while index < len(lines):
        raw = lines[index]
        if not raw.strip():
            index += 1
            continue
        stripped = _strip_comment(raw)
        if not stripped.strip():
            index += 1
            continue
        line_indent = len(stripped) - len(stripped.lstrip(" "))
        if line_indent < indent:
            break
        if line_indent > indent:
            raise YamlError(f"line {index + 1}: unexpected indentation")

        body = stripped.strip()

        if body.startswith("- "):
            if container is None:
                container = []
            if not isinstance(container, list):
                raise YamlError(f"line {index + 1}: sequence item inside a mapping")
            item_text = body[2:].strip()
            item_indent = line_indent + 2
            if re.match(r"\A[A-Za-z_][\w.-]*\s*:", item_text):
                # A mapping whose first key shares the dash's line.
                synthetic = " " * item_indent + item_text
                value, index = _parse_block([synthetic] + lines[index + 1 :], 0, item_indent)
                # _parse_block consumed from a spliced list; recompute the offset.
                consumed = value_consumed(lines, index, item_indent)
                container.append(value)
                index = consumed
            else:
                container.append(_scalar(item_text))
                index += 1
            continue

        match = re.match(r"\A([A-Za-z_][\w.-]*)\s*:(.*)\Z", body)
        if not match:
            raise YamlError(f"line {index + 1}: cannot parse {body!r}")
        if container is None:
            container = {}
        if not isinstance(container, dict):
            raise YamlError(f"line {index + 1}: mapping key inside a sequence")
        key, rest = match.group(1), match.group(2).strip()

        if rest in (">-", ">", ">+", "|-", "|", "|+"):
            container[key], index = _read_block_scalar(lines, index + 1, line_indent, rest)
        elif rest:
            container[key] = _scalar(rest)
            index += 1
        else:
            nested, index = _parse_block(lines, index + 1, _next_indent(lines, index + 1, line_indent))
            container[key] = nested
    return container, index


def value_consumed(lines, index, indent):
    """Advance past a nested block that began on a dash line."""
    i = index
    while i < len(lines):
        raw = lines[i]
        if not raw.strip():
            i += 1
            continue
        line_indent = len(raw) - len(raw.lstrip(" "))
        if line_indent < indent:
            break
        i += 1
    return i


def _next_indent(lines, index, parent_indent):
    for i in range(index, len(lines)):
        if not lines[i].strip():
            continue
        stripped = _strip_comment(lines[i])
        if not stripped.strip():
            continue
        return len(stripped) - len(stripped.lstrip(" "))
    return parent_indent + 2


def parse_yaml(text: str):
    lines = text.replace("\t", "    ").split("\n")
    lines = [line for line in lines if line.strip() != "---"]
    value, _ = _parse_block(lines, 0, _next_indent(lines, 0, 0))
    return value if value is not None else {}


# --------------------------------------------------------------------------
# Minimal JSON Schema subset validator
# --------------------------------------------------------------------------

TYPE_CHECKS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "boolean": lambda v: isinstance(v, bool),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
}


def resolve_ref(root: dict, ref: str):
    if not ref.startswith("#/"):
        raise ValueError(f"unsupported schema reference {ref}")
    node = root
    for segment in ref[2:].split("/"):
        node = node[segment.replace("~1", "/").replace("~0", "~")]
    return node


def validate_schema(value, schema, root, location="$"):
    if "$ref" in schema:
        return validate_schema(value, resolve_ref(root, schema["$ref"]), root, location)

    errors = []
    expected = schema.get("type")
    if expected and not TYPE_CHECKS.get(expected, lambda _: True)(value):
        return [f"{location}: expected {expected}, got {type(value).__name__}"]

    if "const" in schema and value != schema["const"]:
        errors.append(f"{location}: expected {schema['const']!r}")
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{location}: value is not in {schema['enum']!r}")

    if isinstance(value, str):
        if "minLength" in schema and len(value) < schema["minLength"]:
            errors.append(f"{location}: shorter than {schema['minLength']} characters")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{location}: does not match {schema['pattern']}")

    if isinstance(value, int) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            errors.append(f"{location}: below minimum {schema['minimum']}")
        if "maximum" in schema and value > schema["maximum"]:
            errors.append(f"{location}: above maximum {schema['maximum']}")

    if isinstance(value, list):
        if "minItems" in schema and len(value) < schema["minItems"]:
            errors.append(f"{location}: requires at least {schema['minItems']} items")
        if schema.get("uniqueItems"):
            marks = [json.dumps(item, sort_keys=True) for item in value]
            if len(set(marks)) != len(marks):
                errors.append(f"{location}: items must be unique")
        if "items" in schema:
            for index, item in enumerate(value):
                errors.extend(validate_schema(item, schema["items"], root, f"{location}[{index}]"))

    if isinstance(value, dict):
        for key in schema.get("required", []):
            if key not in value:
                errors.append(f"{location}: missing required property {key}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False:
            for key in value:
                if key not in properties:
                    errors.append(f"{location}: unknown property {key}")
        for key, subschema in properties.items():
            if key in value:
                errors.extend(validate_schema(value[key], subschema, root, f"{location}.{key}"))

    return errors


# --------------------------------------------------------------------------
# Landscape model
# --------------------------------------------------------------------------


def frontmatter(path: Path) -> dict:
    match = FRONTMATTER_PATTERN.match(path.read_text())
    if not match:
        raise YamlError("missing YAML frontmatter")
    data = parse_yaml(match.group(1))
    if not isinstance(data, dict):
        raise YamlError("frontmatter is not a mapping")
    return data


def collect(root: Path, globs) -> list[Path]:
    found: list[Path] = []
    for pattern in globs:
        found.extend(sorted(root.glob(pattern)))
    return found


def dependency_errors(workflow: dict, label: str) -> list[str]:
    steps = workflow.get("steps") or []
    ids = [step.get("id") for step in steps if isinstance(step, dict)]
    errors = []

    seen = set()
    for step_id in ids:
        if step_id in seen:
            errors.append(f"{label}: duplicate step id {step_id}")
        seen.add(step_id)

    graph = {}
    for step in steps:
        if not isinstance(step, dict):
            continue
        needs = step.get("needs") or []
        for dependency in needs:
            if dependency not in seen:
                errors.append(f"{label}: step {step.get('id')} needs unknown step {dependency}")
            if dependency == step.get("id"):
                errors.append(f"{label}: step {step.get('id')} depends on itself")
        graph[step.get("id")] = list(needs)

    visiting, visited = set(), set()

    def visit(node):
        if node in visited or node not in graph:
            return
        if node in visiting:
            errors.append(f"{label}: workflow dependency cycle includes {node}")
            return
        visiting.add(node)
        for dependency in graph[node]:
            visit(dependency)
        visiting.discard(node)
        visited.add(node)

    for step_id in ids:
        visit(step_id)
    return errors


def validate(root: Path) -> tuple[list[str], dict]:
    errors: list[str] = []
    root = root.resolve()

    def rel(path: Path) -> str:
        try:
            return str(path.relative_to(root))
        except ValueError:
            return str(path)

    workflow_files = collect(root, WORKFLOW_GLOBS)
    skill_files = collect(root, SKILL_GLOBS)
    agent_files = collect(root, AGENT_GLOBS)
    contract_files = collect(root, CONTRACT_GLOBS)

    manifest = root / "MANIFEST.md"
    framework_mode = False
    expected_version = None
    if manifest.is_file():
        try:
            data = frontmatter(manifest)
            framework_mode = data.get("project") == "agent-manifest" and "version" in data
            expected_version = data.get("version")
        except YamlError as exc:
            errors.append(f"MANIFEST.md: {exc}")

    # --- frontmatter of every skill and agent -----------------------------
    skills: dict[str, Path] = {}
    for path in skill_files:
        try:
            data = frontmatter(path)
        except YamlError as exc:
            errors.append(f"{rel(path)}: {exc}")
            continue
        name = data.get("name")
        if not isinstance(name, str) or not NAME_PATTERN.match(name):
            errors.append(f"{rel(path)}: skill needs a kebab-case name, got {name!r}")
            continue
        if not isinstance(data.get("description"), str) or not data["description"].strip():
            errors.append(f"{rel(path)}: skill needs a description")
        if name in skills:
            errors.append(f"{rel(path)}: duplicate skill name {name} (also {rel(skills[name])})")
        skills[name] = path

    contracts = {path.name[: -len(".schema.json")]: path for path in contract_files}
    for path in contract_files:
        try:
            json.loads(path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{rel(path)}: invalid JSON: {exc}")

    agents: dict[str, Path] = {}
    for path in agent_files:
        try:
            data = frontmatter(path)
        except YamlError as exc:
            errors.append(f"{rel(path)}: {exc}")
            continue
        name = data.get("name")
        if not isinstance(name, str):
            continue  # _README.md and similar prose files carry no agent name
        if not NAME_PATTERN.match(name):
            errors.append(f"{rel(path)}: agent name must be kebab-case, got {name!r}")
            continue
        if name in agents:
            errors.append(f"{rel(path)}: duplicate agent name {name} (also {rel(agents[name])})")
        agents[name] = path

        if not isinstance(data.get("description"), str) or not data["description"].strip():
            errors.append(f"{rel(path)}: agent needs a description")
        reason = data.get("isolation_reason")
        if not isinstance(reason, str) or not reason.strip():
            errors.append(f"{rel(path)}: missing isolation_reason")
        contract = data.get("output_contract")
        if not isinstance(contract, str) or not contract.strip():
            errors.append(f"{rel(path)}: missing output_contract")
        elif not NAME_PATTERN.match(contract):
            errors.append(f"{rel(path)}: output_contract must be a schema basename, got {contract!r}")
        elif contract not in contracts:
            errors.append(f"{rel(path)}: references unknown contract {contract}")

    # --- workflow schema ---------------------------------------------------
    schema_path = contracts.get("workflow")
    if schema_path is None and BUNDLED_WORKFLOW_SCHEMA.is_file():
        schema_path = BUNDLED_WORKFLOW_SCHEMA
    workflow_schema = None
    if workflow_files and schema_path is not None:
        try:
            workflow_schema = json.loads(schema_path.read_text())
        except json.JSONDecodeError as exc:
            errors.append(f"{rel(schema_path)}: invalid JSON: {exc}")
    elif workflow_files:
        errors.append("workflows present but no workflow.schema.json to validate them against")

    if workflow_schema and expected_version:
        rule = workflow_schema.get("properties", {}).get("version")
        if rule and validate_schema(expected_version, rule, workflow_schema):
            errors.append(
                f"{rel(schema_path)}: version rule rejects the framework version {expected_version}"
            )

    for path in workflow_files:
        label = rel(path)
        try:
            workflow = parse_yaml(path.read_text())
        except YamlError as exc:
            errors.append(f"{label}: invalid YAML: {exc}")
            continue
        if not isinstance(workflow, dict):
            errors.append(f"{label}: workflow is not a mapping")
            continue

        if workflow_schema:
            for error in validate_schema(workflow, workflow_schema, workflow_schema):
                errors.append(f"{label}: {error}")
        errors.extend(dependency_errors(workflow, label))

        for entry in workflow.get("inputs") or []:
            if not (root / entry).is_file():
                errors.append(f"{label}: missing input {entry}")

        for step in workflow.get("steps") or []:
            if not isinstance(step, dict):
                continue
            step_id = step.get("id")
            for name in step.get("skills") or []:
                if name not in skills:
                    errors.append(f"{label}: step {step_id} references unknown skill {name}")
            agent = step.get("agent")
            if agent and agent not in agents:
                errors.append(f"{label}: step {step_id} references unknown agent {agent}")
            for key in ("input_contract", "output_contract"):
                name = step.get(key)
                if name and name not in contracts:
                    errors.append(f"{label}: step {step_id} references unknown contract {name}")

    # --- framework-only: one version across every source -------------------
    versioned = 0
    if framework_mode:
        sources: list[tuple[Path, object]] = []
        for path in [root / "IMPLEMENTATION.md", root / "README.md", *skill_files, *agent_files]:
            if not path.is_file():
                continue
            try:
                sources.append((path, frontmatter(path).get("version")))
            except YamlError as exc:
                errors.append(f"{rel(path)}: {exc}")
        for path in workflow_files:
            try:
                sources.append((path, parse_yaml(path.read_text()).get("version")))
            except YamlError:
                continue
        for path in contract_files:
            try:
                sources.append((path, json.loads(path.read_text()).get("x-framework-version")))
            except json.JSONDecodeError:
                continue

        versioned = len(sources) + 1
        for path, version in sources:
            if version != expected_version:
                errors.append(f"{rel(path)}: version {version!r}, expected {expected_version}")

    summary = {
        "framework_mode": framework_mode,
        "version": expected_version,
        "versioned": versioned,
        "workflows": len(workflow_files),
        "skills": len(skills),
        "agents": len(agents),
        "contracts": len(contracts),
    }
    return errors, summary


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an AI landscape or this framework repository.")
    parser.add_argument("path", nargs="?", default=None, help="landscape root (default: the repository root)")
    parser.add_argument("--quiet", action="store_true", help="print nothing unless validation fails")
    args = parser.parse_args()

    root = Path(args.path) if args.path else SCRIPT_DIR.parent
    if not root.is_dir():
        print(f"not a directory: {root}", file=sys.stderr)
        return 2

    errors, summary = validate(root)
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    if not args.quiet:
        if summary["framework_mode"]:
            print(
                f"Framework validation passed at {summary['version']}: "
                f"{summary['versioned']} versioned sources, {summary['workflows']} workflows."
            )
        else:
            print(
                "Landscape validation passed: "
                f"{summary['workflows']} workflows, {summary['skills']} skills, "
                f"{summary['agents']} agents, {summary['contracts']} contracts."
            )
    return 0


if __name__ == "__main__":
    sys.exit(main())
