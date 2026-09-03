# Evaluation Cases

Principle 8 of [MANIFEST.md](../MANIFEST.md) says the framework must be retested against a fresh minimal baseline
after a significant model or tool change, and at least every six months. These cases make that question answerable
instead of rhetorical.

They are behavioral, not unit tests. A landscape is good or bad because of what a model does with it, so most
assertions are judged by a reviewer against a real run. The runner automates only what a machine can decide.

## The cases

| Case | What it protects |
| --- | --- |
| `plain-notes-setup` | Restraint. Fails when the framework installs its own shape rather than answering the project. |
| `bloated-2x-review` | Discrimination. Fails when a review drops durable facts or keeps outgrown scaffolding. |
| `healthy-minimal-review` | Silence. Fails when a review manufactures work on a landscape that is already correct. |

`healthy-minimal-review` is the case most likely to catch drift toward ceremony, and the one most likely to fail
quietly. Take a "no findings" result there as a pass, not as a wasted run.

## Running one

```text
python3 evals/run.py --list
python3 evals/run.py plain-notes-setup
```

Staging copies the fixture to a scratch directory, so a run never dirties the committed fixture. Run the named
workflow there against the case's prompt, in a fresh session with no memory of this repository. Then:

```text
python3 evals/run.py plain-notes-setup --check /path/to/staged/copy --judgments judgments.json
```

The runner checks paths and requires one evidence-backed judgment for every behavioral assertion. A missing or malformed
judgment exits `2`; a failed mechanical or behavioral assertion exits `1`. Judge the run against its transcript and
diff, not its summary—a run that claims restraint while creating six files fails.

```json
{
  "judgments": [
    {
      "kind": "must",
      "assertion": "exact assertion text from the case file",
      "passed": true,
      "evidence": "transcript or diff evidence supporting the judgment"
    }
  ]
}
```

## Release gate

Before a versioned release creates its tag, CI runs every case in a separate, non-persistent Claude session and uses a
second fresh session to judge every assertion from the full transcript and filesystem diff:

```text
PYTHONDONTWRITEBYTECODE=1 python3 evals/run-live.py --artifacts /path/to/evidence
```

The release job requires `ANTHROPIC_API_KEY`, fails closed when the key or any judgment is missing, and uploads the
transcripts, diffs, and judgments as a GitHub Actions artifact. Ordinary validation does not spend API credits; it
validates the case definitions and runner with regression tests. A release cannot tag or publish until the live gate
passes.

## Comparing against a baseline

To answer whether the harness still earns its place, run a case twice: once with the landscape installed, once against
a fresh session with no framework at all. If the results are equivalent, the scaffolding under test is no longer
carrying weight and should be removed. That is the intended outcome of a maintenance review, not a failure of it.

## The native harness

Claude Code ships `claude plugin eval`, which runs `evals/**/case.yaml` cases with LLM graders and an `--ablation
with-without` mode that scores a run against a no-plugin baseline. That ablation is a direct mechanical answer to
Principle 8, and it is where these cases should eventually live — Principle 5 prefers a tool's native mechanism over a
local imitation.

It remains early access and is not enabled on the account maintaining this suite, so its authoring schema and execution
cannot yet be verified end to end. The interim runner uses `cases/*.yml`, not `case.yaml`, so the layouts do not collide
and cases can migrate one at a time. Recheck `claude plugin eval init --help` before extending this harness.

## Adding a case

Add a fixture directory under `fixtures/` and a case file under `cases/`. A case names its fixture, workflow, and
prompt, states in `rationale` what regression it protects against, and lists assertions as `must` and `must_not`.
Use `paths_absent` and `paths_present` for the assertions a machine can settle.

Write cases that can fail. An assertion every plausible run satisfies protects nothing.
