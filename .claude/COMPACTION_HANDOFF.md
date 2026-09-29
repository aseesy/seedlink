# Seedlink handoff — written 2026-09-29, end of session 1

Ground truth for the next session. Read this, then `.claude/step2_plan_original.md`.

## Where we stopped

- **Step 1 is done, committed and pushed.** Step 1 code ends at `e09bb93` on https://github.com/aseesy/seedlink (public). This handoff and the Step 2 plan were committed after it and pushed to `main` as well, so any machine that clones the repo has them.
- **Step 2 has not started.** The user pasted a Step 2 plan and asked "Is this a good plan?". I reviewed it and proposed 8 amendments, ending with "Say go and I'll build Step 2 with these changes." The user closed the session **without saying go**.
- **First action next session:** ask the user to approve the amended Step 2 plan (or edit it). Build nothing until they approve.

## Step 1 state (verified 2026-09-29, Python 3.14.2 at /opt/homebrew/bin/python3)

- Layout: `Seedlink/` is the git root, and it contains `.gitignore` (`__pycache__/`) and `mini-organism/`.
- Test command, run from `mini-organism/`: `python3 -m unittest -v immutable_tests.test_arithmetic` → 5 tests: 2 `add` tests pass, 3 `multiply` tests error with AttributeError, exit code 1. `unittest discover` and running the file directly do not work (namespace packages, no `__init__.py`).
- The test imports `from workspace import arithmetic` and calls each function inside its own test. This deliberately differs from the spec's `from workspace.arithmetic import add, multiply`, which would fail the whole file at import, so `add` would never be tested. The user was told about this and did not object.
- `template/arithmetic.py` and `workspace/arithmetic.py` are byte-identical (sha256 `ba1a531f…`).
- The kernel's 6 functions raise NotImplementedError. `seed.py` prints the goal and exits 0.
- The proof doc has a "Writable State" section: the organism may write only `workspace/arithmetic.py` and new files in `history/`. Everything else is read-only to it.

## Step 2 amendments I proposed (awaiting approval)

1. **Verify in a temporary copy, not in place.** Evidence: in a scratch copy, a same-size `a - b` regression with a matching mtime passed a *fresh* process (`OK`) because of a stale `__pycache__` .pyc; after deleting `__pycache__` the same run reported `FAILED (failures=2)`. Copy `immutable_tests/` + the candidate into a new temp dir and run there. Write the real workspace only on a pass. On failure the healthy file was never replaced; prove that with its sha256 before == after.
2. **Timeout on `subprocess.run`.** A candidate with an endless loop at import would hang verify(). A timeout counts as rejected, with the return code recorded as null. (Standard behavior; not run.)
3. **Kernel functions take a root directory**, defaulting to `mini-organism/`. Tests run on a temp copy, so the demos never leave `multiply()` in the real workspace (which would make Step 3 trivial) and never commit demo history. Hash the real tree before and after the suite.
4. **`run_mutation` records validation rejections too**, as outcome `invalid`. "Before any write" means before any workspace write.
5. **Prove restoration by hash only.** Drop the plan's re-run of the restored baseline, because it fails 3 tests by design.
6. **`validate_response` returns the input unchanged or raises `ValueError`** naming the rule it broke. No normalization.
7. **History files** get a nanosecond timestamp in their names and are opened with exclusive create `open(path, "x")`, so no record can be overwritten.
8. **Protected check = sha256 of every file under `mini-organism/`** except `workspace/arithmetic.py` and `history/`. The plan's 5-file list misses `seed.py`, `README.md` and the new `test_organism.py`.

For Step 3 (not a change now): the safeguards control which file the organism can write, not what the candidate code does when the tests import it. That code runs with the user's permissions and could write to any file using a full path. Decide on isolation before connecting an LLM.

## How the user works (from this session)

- On "X or Y" implementation questions, imagine both outcomes and decide yourself; report the choice and the reason. Ask only product questions.
- Tight scope. Stop at each step boundary. Standard library only.
- Committing and pushing to `aseesy/seedlink` `main` was authorized for Step 1 by the user supplying the repo URL.
