#!/usr/bin/env python3
"""Prepare and check the framework's own behavioral evaluation cases.

Principle 8 asks whether the harness still earns its place against a fresh
minimal baseline. That question is behavioral, so these cases are judged, not
asserted: the runner automates what a machine can decide and prints the rest as
a checklist for the reviewer.

    python3 evals/run.py --list
    python3 evals/run.py plain-notes-setup            # stage a working copy
    python3 evals/run.py plain-notes-setup --check DIR --judgments judgments.json

Staging copies the fixture to a scratch directory so a run never dirties the
committed fixture.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

# Plugin hosts copy the directory verbatim and do not honour .gitignore, so a
# stray __pycache__ would ship to every user. Import without writing bytecode.
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from validate import parse_yaml  # noqa: E402  (path set above)

EVALS_DIR = Path(__file__).resolve().parent
CASES_DIR = EVALS_DIR / "cases"
FIXTURES_DIR = EVALS_DIR / "fixtures"


def load_cases() -> dict[str, dict]:
    cases = {}
    for path in sorted(CASES_DIR.glob("*.yml")):
        data = parse_yaml(path.read_text())
        if not isinstance(data, dict) or "name" not in data:
            raise SystemExit(f"{path}: case needs a name")
        if data["name"] in cases:
            raise SystemExit(f"{path}: duplicate case name {data['name']!r}")
        if not (data.get("fixture") and (FIXTURES_DIR / data["fixture"]).is_dir()):
            raise SystemExit(f"{path}: fixture {data.get('fixture')!r} does not exist")
        cases[data["name"]] = data
    return cases


def stage(case: dict) -> Path:
    fixture = FIXTURES_DIR / case["fixture"]
    if not fixture.is_dir():
        raise SystemExit(f"missing fixture: {fixture}")
    destination = Path(tempfile.mkdtemp(prefix=f"eval-{case['name']}-"))
    shutil.copytree(fixture, destination, dirs_exist_ok=True)
    return destination


def load_judgments(path: Path, assertions: list[tuple[str, str]]) -> tuple[list[str], list[str]]:
    """Return (format errors, failed assertions) from explicit human/LLM judgments."""
    try:
        document = json.loads(path.read_text())
    except (OSError, ValueError) as exc:
        return [f"cannot read judgments: {exc}"], []
    entries = document.get("judgments") if isinstance(document, dict) else None
    if not isinstance(entries, list):
        return ["judgments file needs a judgments array"], []

    errors, failed, seen = [], [], set()
    expected = set(assertions)
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"judgments[{index}] must be an object")
            continue
        key = (entry.get("kind"), entry.get("assertion"))
        if key not in expected:
            errors.append(f"judgments[{index}] names an unknown assertion")
            continue
        if key in seen:
            errors.append(f"duplicate judgment for {key[0]} {key[1]!r}")
        seen.add(key)
        if not isinstance(entry.get("passed"), bool):
            errors.append(f"judgment for {key[0]} {key[1]!r} needs boolean passed")
        elif not entry["passed"]:
            failed.append(f"{key[0]} {key[1]}")
        if not isinstance(entry.get("evidence"), str) or not entry["evidence"].strip():
            errors.append(f"judgment for {key[0]} {key[1]!r} needs evidence")
    for kind, assertion in sorted(expected - seen):
        errors.append(f"missing judgment for {kind} {assertion!r}")
    return errors, failed


def check(case: dict, result: Path, judgments: Path | None) -> int:
    """Apply mechanical assertions and require evidence-backed behavioral judgments."""
    failures = []

    for relative in case.get("paths_absent") or []:
        if (result / relative).exists():
            failures.append(f"must not exist, but does: {relative}")
    for relative in case.get("paths_present") or []:
        if not (result / relative).exists():
            failures.append(f"must exist, but does not: {relative}")

    print(f"case: {case['name']}   fixture: {case['fixture']}   workflow: {case.get('workflow', '-')}")
    print(f"result: {result}\n")

    mechanical = len(case.get("paths_absent") or []) + len(case.get("paths_present") or [])
    if not mechanical:
        print("no automated checks for this case: the exit code verifies nothing.")
    elif failures:
        print("automated checks FAILED:")
        for failure in failures:
            print(f"  x {failure}")
    else:
        print(f"automated checks passed ({mechanical}).")
    print()

    assertions = (
        [("must", assertion) for assertion in case.get("must") or []]
        + [("must_not", assertion) for assertion in case.get("must_not") or []]
    )
    judgment_errors, judgment_failures = [], []
    if assertions and judgments is None:
        judgment_errors.append("behavioral assertions require --judgments FILE")
    elif assertions:
        judgment_errors, judgment_failures = load_judgments(judgments, assertions)

    if judgment_errors:
        print("behavioral judgments INCOMPLETE:")
        for error in judgment_errors:
            print(f"  x {error}")
    elif judgment_failures:
        print("behavioral judgments FAILED:")
        for assertion in judgment_failures:
            print(f"  x {assertion}")
    else:
        print(f"behavioral judgments passed ({len(assertions)}), each with recorded evidence.")

    rationale = (case.get("rationale") or "").strip()
    if rationale:
        print(f"\nwhy this case exists:\n  {rationale}")

    if judgment_errors:
        return 2
    return 1 if failures or judgment_failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage or check a framework evaluation case.")
    parser.add_argument("case", nargs="?", help="case name (see --list)")
    parser.add_argument("--list", action="store_true", help="list available cases")
    parser.add_argument("--check", metavar="DIR", help="check a completed run in DIR")
    parser.add_argument("--judgments", metavar="FILE", help="JSON judgments with evidence for every behavioral assertion")
    args = parser.parse_args()

    cases = load_cases()

    if args.list or not args.case:
        for name, case in cases.items():
            print(f"{name:28} {case['fixture']:18} {case.get('workflow', '-')}")
        return 0

    if args.case not in cases:
        raise SystemExit(f"unknown case {args.case!r}; try --list")
    case = cases[args.case]

    if args.check:
        result = Path(args.check)
        if not result.is_dir():
            raise SystemExit(f"not a directory: {result}")
        return check(case, result, Path(args.judgments) if args.judgments else None)

    staged = stage(case)
    print(f"staged {case['fixture']} at:\n  {staged}\n")
    print(f"run `{case.get('workflow', 'the workflow')}` there with this prompt:\n  {case['prompt']}\n")
    print(
        "then record one evidence-backed judgment per assertion and check it:\n"
        f"  python3 evals/run.py {case['name']} --check {staged} --judgments judgments.json"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
