# Step 2 plan — user's original text (verbatim, pasted 2026-09-29)

Amendments agreed in review live in `.claude/COMPACTION_HANDOFF.md`; where they differ, the amendments win.

---

Continue working in the existing `aseesy/seedlink` repository.

Step 1 is complete and correct.

Do not redesign the repository. Do not add LLM integration yet.

## Objective of Step 2

Build and prove the **deterministic mutation, verification, rejection, restoration, and history mechanism** without involving an LLM.

At the end of this step, the system must prove that:

1. it can observe the current goal and workspace state,
2. it can accept a supplied structured mutation proposal,
3. it can reject malformed proposals,
4. it can apply a valid proposal only to the allowed workspace file,
5. it can verify the result in a **fresh Python interpreter process**,
6. it can accept a correct mutation,
7. it can reject a regression,
8. it can restore the last healthy state after a failed mutation,
9. it can record both success and failure,
10. protected files remain untouched.

Do not implement autonomous proposal generation yet.

---

# Important architectural constraint

The verifier must run tests in a fresh Python process.

Use Python's standard library:

```python
subprocess.run(...)
```

but:

- invoke `sys.executable` directly,
- pass arguments as a list,
- use `shell=False`,
- do not execute arbitrary commands,
- do not accept command strings from proposals,
- do not expose generalized shell access.

For example, conceptually:

```python
subprocess.run(
    [
        sys.executable,
        "-m",
        "unittest",
        "-v",
        "immutable_tests.test_arithmetic",
    ],
    ...
)
```

The verifier's authoritative pass/fail signal must be the subprocess **exit code**, not parsing human-readable unittest output.

Capture stdout and stderr only for diagnostics/history.

---

# Keep the existing repository structure

Do not add architecture layers.

You may add only the minimum files necessary for deterministic Step 2 testing.

Prefer keeping the implementation inside:

```text
mini-organism/
├── seed.py
├── kernel/
│   └── organism.py
└── history/
```

If you need a dedicated Step 2 test file for the kernel itself, you may add:

```text
mini-organism/immutable_tests/test_organism.py
```

That file becomes protected state just like the existing immutable tests.

Do not add packages or dependencies.

---

# Structured Mutation Proposal

For Step 2, mutation proposals are supplied by the test harness or caller.

There is no LLM.

Use the smallest possible proposal format:

```python
{
    "target": "workspace/arithmetic.py",
    "replacement_file": "...complete Python source..."
}
```

Do not support:

- patches
- bash
- shell commands
- multiple files
- arbitrary paths
- deletes
- renames
- directory creation
- test modification
- genome modification
- kernel modification

There is exactly one valid mutation target:

```text
workspace/arithmetic.py
```

---

# Implement `observe()`

Update:

```text
kernel/organism.py
```

Implement `observe()`.

It should return a simple structured object containing only what is needed for this proof:

```python
{
    "goal": "...",
    "workspace": "...current arithmetic.py contents..."
}
```

Do not include unnecessary repository scanning.

Do not implement a generalized world model.

---

# Leave `propose()` unimplemented

`propose()` must remain clearly unimplemented in Step 2 because proposal generation will be added later.

It should continue to raise `NotImplementedError`.

Do not fake an LLM.

Do not make it generate code itself.

---

# Implement `validate_response()`

`validate_response(proposal)` must accept a Python dictionary and validate it deterministically.

A proposal is valid only if:

1. it is a dictionary,
2. it has exactly the required fields:
   - `target`
   - `replacement_file`
3. `target` equals exactly:

```text
workspace/arithmetic.py
```

4. `replacement_file` is a non-empty string.

Reject anything else.

Examples that must be rejected:

```python
{"target": "kernel/organism.py", ...}
```

```python
{"target": "../something.py", ...}
```

```python
{"target": "immutable_tests/test_arithmetic.py", ...}
```

```python
{"target": "workspace/arithmetic.py", "replacement_file": "", ...}
```

```python
{"command": "rm -rf ..."}
```

Do not silently normalize dangerous paths into acceptable paths.

Validation should either return a normalized validated proposal or raise a clear validation exception.

---

# Implement sandboxed mutation

Implement `mutate_sandbox()` with extremely narrow behavior.

Before replacing `workspace/arithmetic.py`:

1. read and preserve its current contents,
2. write the proposed replacement to a temporary/sandbox candidate,
3. do not overwrite protected files,
4. retain enough information to restore the original state if verification fails.

The active healthy version must never be lost.

You may use Python standard-library tools such as:

```text
tempfile
pathlib
shutil
```

Keep this as simple as possible.

## Important

The mutation should be verified before it is permanently accepted.

You may choose one of these simple approaches:

### Preferred approach

Temporarily replace `workspace/arithmetic.py`, run verification in a fresh process, and restore the original immediately if verification fails.

or

### Alternative

Construct a temporary mini copy of only what is required for verification.

Choose the smaller, clearer implementation.

Do not introduce git branches/worktrees yet.

---

# Implement `verify()`

`verify()` must invoke:

```text
python -m unittest -v immutable_tests.test_arithmetic
```

using the current Python interpreter:

```python
sys.executable
```

Run it from the `mini-organism/` directory.

Requirements:

- fresh process
- `shell=False`
- fixed test command
- no proposal-controlled command arguments
- capture stdout
- capture stderr
- capture return code

Return a structured result similar to:

```python
{
    "passed": True,
    "returncode": 0,
    "stdout": "...",
    "stderr": "..."
}
```

`passed` must be:

```python
returncode == 0
```

Do not infer success from text output.

A syntax error must count as failure automatically because the subprocess exits nonzero.

---

# Implement promotion/rejection behavior

For Step 2:

## If verification passes

The mutated version becomes the accepted workspace state.

## If verification fails

Restore the exact previous healthy contents of:

```text
workspace/arithmetic.py
```

Then verify the restored version behaves exactly as it did before the attempted mutation.

Do not leave a failed mutation active.

---

# Implement `record_result()`

Every attempted mutation must write one new immutable historical record into:

```text
history/
```

Use JSON.

Each record should contain only useful facts such as:

```json
{
  "outcome": "accepted",
  "target": "workspace/arithmetic.py",
  "verification_returncode": 0,
  "restored": false
}
```

or:

```json
{
  "outcome": "rejected",
  "target": "workspace/arithmetic.py",
  "verification_returncode": 1,
  "restored": true
}
```

You may additionally include:

- timestamp
- diagnostic stdout
- diagnostic stderr
- SHA-256 of state before mutation
- SHA-256 of proposed mutation
- SHA-256 of final state

Those hashes are encouraged because they give us deterministic evidence of restoration.

Do not build generalized memory.

This is only an append-only experiment log.

Each attempt must create a new history file rather than overwriting previous history.

---

# Add one orchestrating function

Add a single small function such as:

```python
run_mutation(proposal)
```

Its sequence must be:

```text
observe
↓
validate proposal
↓
preserve healthy state
↓
apply mutation
↓
verify in fresh process
↓
PASS?
    yes → keep mutation
    no  → restore previous state
↓
record result
↓
return structured result
```

Do not loop.

One function call equals one mutation attempt.

---

# Deterministic proof scenarios

Before finishing Step 2, demonstrate both scenarios from a clean baseline.

The baseline must begin as:

```python
def add(a, b):
    return a + b
```

## Scenario A — Correct mutation

Supply this proposal manually:

```python
{
    "target": "workspace/arithmetic.py",
    "replacement_file": """def add(a, b):
    return a + b


def multiply(a, b):
    return a * b
"""
}
```

Expected result:

```text
all 5 tests pass
mutation accepted
workspace contains multiply()
history records accepted
```

---

# Scenario B — Regression

First reset the workspace to the original healthy baseline:

```python
def add(a, b):
    return a + b
```

Then supply this deliberately bad proposal manually:

```python
{
    "target": "workspace/arithmetic.py",
    "replacement_file": """def add(a, b):
    return a - b


def multiply(a, b):
    return a * b
"""
}
```

Expected result:

```text
verification fails
mutation rejected
original workspace restored exactly
history records rejected
```

After restoration, remember that the original baseline intentionally does **not** contain `multiply()`, so the original acceptance suite will again have the known Step 1 state:

```text
2 add tests pass
3 multiply tests error because multiply() is absent
```

That is expected.

Therefore, restoration correctness must be verified primarily by comparing the restored file with its preserved pre-mutation contents/hash, not by requiring all five acceptance tests to pass after restoring the original Step 1 baseline.

This distinction is important.

---

# Also test validation boundaries

Demonstrate that these proposals are rejected before any write occurs:

1.

```python
{
    "target": "kernel/organism.py",
    "replacement_file": "..."
}
```

2.

```python
{
    "target": "../arithmetic.py",
    "replacement_file": "..."
}
```

3.

```python
{
    "target": "workspace/arithmetic.py",
    "replacement_file": ""
}
```

4.

```python
{
    "command": "echo hello"
}
```

For each validation rejection:

- workspace must remain byte-for-byte unchanged,
- protected files must remain unchanged,
- no executable action occurs.

---

# Protect the experiment itself

Before running the demonstrations, compute SHA-256 hashes for the protected files/directories relevant to the proof.

After all demonstrations, verify they are unchanged.

At minimum verify:

```text
genome/goal.txt
immutable_tests/test_arithmetic.py
kernel/organism.py
template/arithmetic.py
MINIMUM_AUTOPOIETIC_PROOF.md
```

There is one exception:

`kernel/organism.py` will necessarily change as part of implementing Step 2.

Therefore:

1. finish the Step 2 implementation,
2. establish the protected-file baseline hashes,
3. run the mutation demonstrations,
4. prove that the mutation system itself did not alter those protected files during execution.

Do not confuse developer-authored Step 2 changes with organism-authored mutations.

---

# `seed.py`

Do not connect the LLM yet.

You may update `seed.py` minimally to demonstrate or expose Step 2 behavior, but it must not automatically mutate anything merely because it is executed unless the behavior is an explicit deterministic demo mode.

Prefer keeping experimentation in tests rather than adding unnecessary CLI behavior.

---

# Update documentation minimally

Update `README.md` and/or `MINIMUM_AUTOPOIETIC_PROOF.md` only as needed to document that Step 2 now proves deterministic mutation containment and verification.

Do not expand the architecture document.

Do not introduce future components.

---

# Hard restrictions

Do not:

- integrate an LLM
- call Anthropic
- call OpenAI
- add API keys
- use pip
- add third-party packages
- add an infinite loop
- add autonomous retries
- add self-directed goals
- allow arbitrary commands
- allow arbitrary file paths
- add git automation
- add agents
- add memory architecture
- add world-model architecture
- add capability generation
- add self-modification of kernel or tests
- move on to Step 3

Use only Python standard library.

---

# Completion report

When finished, stop.

Report:

1. files changed or added,
2. exact behavior implemented in each function,
3. result of Scenario A,
4. result of Scenario B,
5. validation-boundary test results,
6. proof that failed mutation restored the exact previous bytes/hash,
7. proof that protected state remained unchanged during organism execution,
8. history files created,
9. all commands/tests used,
10. any deviations from this prompt and why.

Do not implement LLM proposal generation.

Do not proceed beyond Step 2.
