from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
sys.dont_write_bytecode = True
sys.path.insert(0, str(PLUGIN_ROOT / "scripts"))

import validate  # noqa: E402

sys.path.insert(0, str(PLUGIN_ROOT / "evals"))
import run as eval_runner  # noqa: E402


class ValidatorTests(unittest.TestCase):
    def test_duplicate_yaml_key_is_rejected(self):
        with self.assertRaisesRegex(validate.YamlError, "duplicate mapping key"):
            validate.parse_yaml("name: first\nname: second\n")

    def test_generated_validator_defaults_to_project_root(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            self.assertEqual(validate.default_root(project / ".claude" / "scripts"), project)
            self.assertEqual(validate.default_root(project / "plugin" / "scripts"), project / "plugin")

    def test_symlinked_skill_target_is_collected_once(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / ".codex" / "skills" / "shared"
            source.mkdir(parents=True)
            (source / "SKILL.md").write_text("---\nname: shared\ndescription: Shared policy.\n---\n")
            link = root / ".claude" / "skills" / "shared"
            link.parent.mkdir(parents=True)
            link.symlink_to(source, target_is_directory=True)
            self.assertEqual(len(validate.collect(root, validate.SKILL_GLOBS)), 1)

    def test_qualitative_agent_does_not_require_schema_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            agent = root / ".claude" / "agents" / "reviewer.md"
            agent.parent.mkdir(parents=True)
            agent.write_text(
                "---\nname: reviewer\ndescription: Reviews changes for people.\n"
                "isolation_reason: Independent evidence matters.\n---\n"
            )
            errors, _ = validate.validate(root)
            self.assertEqual(errors, [])

    def test_contracts_reject_contradictory_results(self):
        proposal_schema = json.loads((PLUGIN_ROOT / "contracts/change-proposal.schema.json").read_text())
        unsafe_delete = {
            "summary": "Delete an obsolete landscape artifact.",
            "operations": [{
                "action": "delete", "path": "old.md", "concern": "documentation",
                "reason": "The file is obsolete.", "destructive": False, "authority_expanding": False,
            }],
        }
        self.assertTrue(validate.validate_schema(unsafe_delete, proposal_schema, proposal_schema))
        unsafe_move = {
            "summary": "Move one approved landscape artifact.",
            "operations": [{
                "action": "move", "path": "new.md", "concern": "documentation",
                "reason": "The destination is canonical.", "destructive": True,
                "authority_expanding": False,
            }],
        }
        self.assertTrue(validate.validate_schema(unsafe_move, proposal_schema, proposal_schema))

        evaluation_schema = json.loads((PLUGIN_ROOT / "contracts/instruction-evaluation.schema.json").read_text())
        contradictory_evaluation = {
            "verdict": "accept",
            "scope": ["CLAUDE.md"],
            "findings": [{
                "severity": "major", "artifact": "CLAUDE.md",
                "issue": "A real problem exists.", "recommendation": "Fix the problem.",
            }],
            "unverified": [],
        }
        self.assertTrue(
            validate.validate_schema(contradictory_evaluation, evaluation_schema, evaluation_schema)
        )
        for verdict, findings in (
            ("revise", []),
            ("accept-with-notes", []),
            ("accept-with-notes", [{
                "severity": "major", "artifact": "CLAUDE.md",
                "issue": "A real problem exists.", "recommendation": "Fix the problem.",
            }]),
        ):
            contradictory_evaluation["verdict"] = verdict
            contradictory_evaluation["findings"] = findings
            self.assertTrue(
                validate.validate_schema(contradictory_evaluation, evaluation_schema, evaluation_schema),
                verdict,
            )

    def test_preexisting_change_is_ignored_only_while_unchanged(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._init_git(root)
            user_file = root / "user.txt"
            user_file.write_text("user change\n")
            worktree_hash = self._hash(user_file.read_bytes())
            index_hash = validate.index_fingerprint(root, "user.txt")
            proposal = self._proposal(
                root,
                preexisting_changes=[{
                    "path": "user.txt",
                    "worktree_sha256": worktree_hash,
                    "index_sha256": index_hash,
                }],
            )
            self.assertEqual(validate.check_proposal(root, proposal), [])
            user_file.write_text("agent also changed it\n")
            self.assertTrue(validate.check_proposal(root, proposal))

    def test_authority_hash_and_private_directory_are_enforced(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._init_git(root)
            settings = root / "settings.json"
            settings.write_text('{"allow": ["test"]}\n')
            secret = root / "private" / "secret.txt"
            secret.parent.mkdir()
            secret.write_text("secret\n")
            subprocess.run(["git", "add", "private/secret.txt"], cwd=root, check=True)
            proposal = self._proposal(
                root,
                operation={
                    "action": "create",
                    "path": "settings.json",
                    "concern": "enforcement",
                    "reason": "Approve one explicit command.",
                    "destructive": False,
                    "authority_expanding": True,
                    "effects": ["Allows the test command"],
                    "approved_sha256": self._hash(settings.read_bytes()),
                },
                private_to_local=["private"],
            )
            errors = validate.check_proposal(root, proposal)
            self.assertTrue(any("private_to_local" in error for error in errors))
            settings.write_text('{"allow": ["test", "deploy"]}\n')
            errors = validate.check_proposal(root, proposal)
            self.assertTrue(any("approved hash" in error for error in errors))

    def test_proposal_paths_are_relative_to_git_root_for_nested_validator(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self._init_git(root)
            plugin = root / "plugins" / "example"
            plugin.mkdir(parents=True)
            workflow = root / ".github" / "workflows" / "release.yml"
            workflow.parent.mkdir(parents=True)
            workflow.write_text("name: release\n")
            proposal = self._proposal(
                root,
                operation={
                    "action": "create",
                    "path": ".github/workflows/release.yml",
                    "concern": "enforcement",
                    "reason": "Approve the release workflow.",
                    "destructive": False,
                    "authority_expanding": True,
                    "effects": ["Runs the approved release workflow"],
                    "approved_sha256": self._hash(workflow.read_bytes()),
                },
            )
            self.assertEqual(validate.check_proposal(plugin, proposal), [])

    def test_behavioral_judgments_require_complete_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            judgments = Path(directory) / "judgments.json"
            judgments.write_text(json.dumps({
                "judgments": [{
                    "kind": "must", "assertion": "keeps the rule",
                    "passed": True, "evidence": "diff line 4",
                }]
            }))
            errors, failures = eval_runner.load_judgments(
                judgments, [("must", "keeps the rule"), ("must_not", "adds ceremony")]
            )
            self.assertTrue(any("missing judgment" in error for error in errors))
            self.assertEqual(failures, [])

    def test_no_change_review_and_documentation_order_are_structural(self):
        review = validate.parse_yaml((PLUGIN_ROOT / "workflows/review.yml").read_text())
        review_steps = {step["id"]: step for step in review["steps"]}
        self.assertNotIn("output_contract", review_steps["report"])
        self.assertIn("when", review_steps["propose"])
        self.assertEqual(review_steps["approve"]["needs"], ["propose"])

        for name in ("extend", "adopt-tool", "retire"):
            workflow = validate.parse_yaml((PLUGIN_ROOT / f"workflows/{name}.yml").read_text())
            steps = {step["id"]: step for step in workflow["steps"]}
            verification = "verify" if name == "retire" else "validate"
            self.assertEqual(steps[verification]["needs"], ["document"])
            self.assertEqual(steps["evaluate"]["needs"], [verification])
            self.assertEqual(steps["finish"]["needs"], ["evaluate"])

    @staticmethod
    def _hash(content: bytes) -> str:
        return hashlib.sha256(content).hexdigest()

    @staticmethod
    def _init_git(root: Path):
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        (root / "user.txt").write_text("original\n")
        subprocess.run(["git", "add", "user.txt"], cwd=root, check=True)
        subprocess.run(
            ["git", "-c", "user.name=Test", "-c", "user.email=test@example.com", "commit", "-qm", "base"],
            cwd=root,
            check=True,
        )

    @staticmethod
    def _proposal(root: Path, operation=None, **extra) -> Path:
        operation = operation or {
            "action": "modify",
            "path": "approved.txt",
            "concern": "documentation",
            "reason": "Approved documentation update.",
            "destructive": False,
            "authority_expanding": False,
        }
        data = {"summary": "Apply one approved and bounded change.", "operations": [operation], **extra}
        path = root / "approved-change.json"
        path.write_text(json.dumps(data))
        return path


if __name__ == "__main__":
    unittest.main()
