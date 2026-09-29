"""Entry point for the mini organism.

Step 1: prints the goal and exits. The mutation loop and LLM call
are added in a later step.
"""

from pathlib import Path

ROOT = Path(__file__).parent


def main():
    goal = (ROOT / "genome" / "goal.txt").read_text().strip()
    print(f"Goal: {goal}")
    print("The mutation loop is not implemented yet. Exiting.")


if __name__ == "__main__":
    main()
