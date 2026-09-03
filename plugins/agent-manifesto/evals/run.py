#!/usr/bin/env python3
"""Prepare and check the framework's own behavioral evaluation cases.

Principle 8 asks whether the harness still earns its place against a fresh
minimal baseline. That question is behavioral, so these cases are judged, not
asserted: the runner automates what a machine can decide and prints the rest as
a checklist for the reviewer.

    python3 evals/run.py --list
    python3 evals/run.py plain-notes-setup            # stage a working copy
    python3 evals/run.py plain-notes-setup --check DIR  # check a finished run

Staging copies the fixture to a scratch directory so a run never dirties the
committed fixture.
"""

from __future__ import annotations

import argparse
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


def check(case: dict, result: Path) -> int:
    """Apply the mechanical assertions; print the judged ones as a checklist."""
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

    judged = len(case.get("must") or []) + len(case.get("must_not") or [])
    print(f"the {judged} assertions below are NOT checked here. Judge them against the run's")
    print("transcript and diff, then decide the case yourself:\n")
    for assertion in case.get("must") or []:
        print(f"  [ ] must      {assertion}")
    for assertion in case.get("must_not") or []:
        print(f"  [ ] must not  {assertion}")

    rationale = (case.get("rationale") or "").strip()
    if rationale:
        print(f"\nwhy this case exists:\n  {rationale}")

    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage or check a framework evaluation case.")
    parser.add_argument("case", nargs="?", help="case name (see --list)")
    parser.add_argument("--list", action="store_true", help="list available cases")
    parser.add_argument("--check", metavar="DIR", help="check a completed run in DIR")
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
        return check(case, result)

    staged = stage(case)
    print(f"staged {case['fixture']} at:\n  {staged}\n")
    print(f"run `{case.get('workflow', 'the workflow')}` there with this prompt:\n  {case['prompt']}\n")
    print(f"then check it:\n  python3 evals/run.py {case['name']} --check {staged}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
