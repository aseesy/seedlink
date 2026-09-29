"""Kernel of the mini organism: one closed modify-and-verify cycle.

Step 1 contains placeholders only. Each function raises
NotImplementedError until a later step implements it.
"""


def observe():
    """Read the goal, the current workspace code, and the protected tests."""
    raise NotImplementedError("observe() is implemented in a later step")


def propose():
    """Ask the model for a replacement workspace/arithmetic.py."""
    raise NotImplementedError("propose() is implemented in a later step")


def validate_response():
    """Accept only a well-formed proposal that targets workspace/arithmetic.py."""
    raise NotImplementedError("validate_response() is implemented in a later step")


def mutate_sandbox():
    """Write the proposal to workspace/arithmetic.py, the only writable code target."""
    raise NotImplementedError("mutate_sandbox() is implemented in a later step")


def verify():
    """Run immutable_tests/ against the mutated workspace and report pass or fail."""
    raise NotImplementedError("verify() is implemented in a later step")


def record_result():
    """Write the outcome, success or failure, as a new file in history/."""
    raise NotImplementedError("record_result() is implemented in a later step")
