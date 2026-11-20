#!/usr/bin/env python3
"""The World in One Day - Friday 20 November 2026 (entrypoint).

The front page itself is drawn by render.py, a pure standard-library
program kept in this repository as the reproducible source of the
artwork: run it and it regenerates entry.png byte for byte.

The grader's pinned Python image ships only the standard library,
so this entrypoint - the file the grader runs - also uses only the
standard library: it copies the repository's entry.png to the
output path, exactly the deliverable form the competition rules
describe ("the simplest program copies an image the repository
holds"). Two runs therefore always write the same bytes, with no
network, well inside the time and memory budgets.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    src = os.path.join(HERE, "entry.png")
    # The grader sets MAKEFUN_OUTPUT_DIR locally; on the grading
    # sandbox the output path is /output. Fall back to the repo
    # folder itself when neither exists (a local smoke run).
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    if not os.path.isdir(out_dir):
        out_dir = HERE
    dst = os.path.join(out_dir, "entry.png")
    if os.path.abspath(src) != os.path.abspath(dst):
        shutil.copyfile(src, dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
