#!/usr/bin/env python3
"""Run every behavioral case in fresh Claude sessions and judge the evidence."""

from __future__ import annotations

import argparse
import difflib
import json
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import run as eval_runner  # noqa: E402

EVALS_DIR = Path(__file__).resolve().parent
PLUGIN_ROOT = EVALS_DIR.parent


def invoke(command: list[str], prompt: str, cwd: Path) -> str:
    completed = subprocess.run(
        command + [prompt], cwd=cwd, text=True, capture_output=True, check=False
    )
    if completed.returncode:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"Claude exited {completed.returncode}: {detail}")
    return completed.stdout.strip()


def tree_diff(before: Path, after: Path) -> str:
    """Return a reviewable unified diff without requiring a Git repository."""
    ignored = {".git"}

    def files(root: Path) -> dict[str, Path]:
        return {
            path.relative_to(root).as_posix(): path
            for path in root.rglob("*")
            if path.is_file() and not any(part in ignored for part in path.relative_to(root).parts)
        }

    old, new = files(before), files(after)
    chunks = []
    for relative in sorted(set(old) | set(new)):
        old_text = old[relative].read_text(errors="replace").splitlines(keepends=True) if relative in old else []
        new_text = new[relative].read_text(errors="replace").splitlines(keepends=True) if relative in new else []
        if old_text == new_text:
            continue
        chunks.extend(difflib.unified_diff(
            old_text, new_text, fromfile=f"a/{relative}", tofile=f"b/{relative}"
        ))
    return "".join(chunks) or "(no filesystem changes)\n"


def judgment_schema(assertions: list[tuple[str, str]]) -> dict:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["judgments"],
        "properties": {
            "judgments": {
                "type": "array",
                "minItems": len(assertions),
                "maxItems": len(assertions),
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["kind", "assertion", "passed", "evidence"],
                    "properties": {
                        "kind": {"enum": ["must", "must_not"]},
                        "assertion": {"enum": [assertion for _, assertion in assertions]},
                        "passed": {"type": "boolean"},
                        "evidence": {"type": "string", "minLength": 1},
                    },
                },
            }
        },
    }


def parse_structured_output(raw: str) -> dict:
    envelope = json.loads(raw)
    value = envelope.get("structured_output") if isinstance(envelope, dict) else None
    if value is None and isinstance(envelope, dict):
        value = envelope.get("result")
    if isinstance(value, str):
        value = json.loads(value)
    if not isinstance(value, dict):
        raise ValueError("Claude response did not contain structured_output")
    return value


def run_case(case: dict, claude: str, model: str | None, artifacts: Path) -> int:
    staged = eval_runner.stage(case)
    fixture = eval_runner.FIXTURES_DIR / case["fixture"]
    common = [claude, "--bare", "--no-session-persistence"]
    if model:
        common.extend(["--model", model])

    run_prompt = (
        f"Use the /agent-manifesto:ai-landscape skill from the supplied plugin. "
        f"Follow {case['workflow']} for this request: {case['prompt']} "
        "This is the first user turn: do not invent approval or silently skip a required question. "
        "Work only in the current fixture and respond exactly as you would to its user."
    )
    transcript = invoke(
        common + [
            "--plugin-dir", str(PLUGIN_ROOT), "--permission-mode", "acceptEdits",
            "--output-format", "text", "-p",
        ],
        run_prompt,
        staged,
    )
    diff = tree_diff(fixture, staged)
    assertions = (
        [("must", value) for value in case.get("must") or []]
        + [("must_not", value) for value in case.get("must_not") or []]
    )
    judge_prompt = (
        "Independently judge every assertion against the complete candidate transcript and filesystem diff. "
        "For a must assertion, passed means the behavior is present. For must_not, passed means the forbidden "
        "behavior is absent. Preserve each assertion verbatim and cite concrete transcript or diff evidence.\n\n"
        f"CASE:\n{json.dumps(case, indent=2)}\n\nTRANSCRIPT:\n{transcript}\n\nDIFF:\n{diff}"
    )
    raw_judgment = invoke(
        common + [
            "--restricted", "--output-format", "json",
            "--json-schema", json.dumps(judgment_schema(assertions)), "-p",
        ],
        judge_prompt,
        fixture,
    )
    judgments = parse_structured_output(raw_judgment)

    case_dir = artifacts / case["name"]
    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "transcript.txt").write_text(transcript + "\n")
    (case_dir / "diff.patch").write_text(diff)
    judgment_path = case_dir / "judgments.json"
    judgment_path.write_text(json.dumps(judgments, indent=2) + "\n")
    return eval_runner.check(case, staged, judgment_path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the release behavioral gate with fresh Claude sessions.")
    parser.add_argument("--claude", default="claude", help="Claude Code executable")
    parser.add_argument("--model", help="model alias or full model name")
    parser.add_argument("--artifacts", type=Path, default=EVALS_DIR / "artifacts")
    args = parser.parse_args()

    args.artifacts.mkdir(parents=True, exist_ok=True)
    failures = 0
    for case in eval_runner.load_cases().values():
        print(f"\n=== live behavioral case: {case['name']} ===")
        try:
            failures += bool(run_case(case, args.claude, args.model, args.artifacts))
        except (OSError, RuntimeError, ValueError, json.JSONDecodeError) as exc:
            failures += 1
            print(f"FAILED: {exc}", file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
