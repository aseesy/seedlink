# Minimum Autopoietic Proof

This document is protected. The organism reads it and never modifies it.

## Goal

Starting from a known healthy Python module, autonomously produce and test a modification that adds one requested capability without damaging existing behavior.

For the first proof:

- Healthy module: `template/arithmetic.py`, which defines `add(a, b)`.
- Requested capability: `genome/goal.txt`, "Add a multiply(a, b) function without breaking add()."
- Acceptance: `immutable_tests/test_arithmetic.py` passes in full.

## Success Criteria

The future system must be able to:

- preserve protected files
- generate a valid mutation
- verify the mutation independently
- promote a successful mutation
- reject a regression
- restore the healthy state after failure
- record both successful and failed outcomes
- terminate cleanly

## Protected State

The future organism must never autonomously modify:

```text
genome/
immutable_tests/
kernel/
template/
MINIMUM_AUTOPOIETIC_PROOF.md
```

## Writable State

The only writable code target during the first proof will be:

```text
workspace/arithmetic.py
```

The organism may also create new result files in `history/`.

Every other file, including `seed.py` and `README.md`, is read-only to the organism.

## Non-Goals

This proof does not include:

- continuous operation
- infinite loops
- self-directed goals
- self-modifying kernel
- generalized shell execution
- agent creation
- multiple agents
- generalized memory
- semantic memory
- capability generation
- self-written tests
- external browsing
- application development
- architecture mutation
