# mini-organism

This repository is intentionally tiny. It exists to prove one closed autonomous loop: modify a single file, verify the change against tests the organism cannot touch, then keep or discard the change. No further autonomy is added until that loop works.

The proof's goal, success criteria, protected files and non-goals are in [MINIMUM_AUTOPOIETIC_PROOF.md](MINIMUM_AUTOPOIETIC_PROOF.md).

## Layout

| Path | Role |
| --- | --- |
| `genome/goal.txt` | The one requested capability |
| `template/arithmetic.py` | Known healthy module, used to restore the workspace |
| `workspace/arithmetic.py` | The only file the organism may modify |
| `immutable_tests/` | Acceptance tests the organism must pass and never edit |
| `kernel/organism.py` | The cycle: observe, propose, validate, mutate, verify, record |
| `history/` | One record per attempt, success or failure |
| `seed.py` | Entry point |

## Status

Step 1: skeleton and test fixture. The kernel functions are placeholders, and `seed.py` prints the goal and exits. No LLM is called.

## Run the tests

Python 3 standard library only. From `mini-organism/`:

```sh
python3 -m unittest -v immutable_tests.test_arithmetic
```

At step 1 the two `add` tests pass and the three `multiply` tests fail, because `multiply()` does not exist yet.
