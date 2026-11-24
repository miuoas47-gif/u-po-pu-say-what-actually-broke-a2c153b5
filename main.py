#!/usr/bin/env python3
"""Say What Actually Broke — make.fun entry.

Writes one line of software error copy to $MAKEFUN_OUTPUT_DIR/entry.txt
(falling back to /output). The line names a specific real failure in plain
words, tells the user what to do next, and carries one joke.

No arguments, no network, stdlib only, deterministic: every run writes the
exact same bytes.
"""

import os
import sys

# The entry: one line, 141 characters, no trailing newline in the file.
LINE = (
    "Your upload failed: the file is 2.1 GB and our limit is 25 MB. "
    "That's not an attachment, that's a hostage situation. "
    "Shrink it and try again."
)

MAX_CHARS = 200


def main() -> int:
    # Gate the line exactly the way the bounty gate does.
    if not 1 <= len(LINE) <= MAX_CHARS:
        print(f"error: line is {len(LINE)} characters, must be 1-{MAX_CHARS}",
              file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("error: line must be a single line", file=sys.stderr)
        return 1
    if not LINE.strip():
        print("error: line must not be only whitespace", file=sys.stderr)
        return 1

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = LINE.encode("utf-8")
    # newline="" keeps the bytes exactly as encoded: one line, no trailing
    # newline, so the file content is the line and nothing else.
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)

    # Read back and verify byte-for-byte before declaring success.
    with open(path, "rb") as f:
        written = f.read()
    if written != data:
        print("error: read-back mismatch in entry.txt", file=sys.stderr)
        return 1
    # Re-check the file itself against the gate, not just the constant:
    # exactly one line, 1-200 characters, not only whitespace.
    text = written.decode("utf-8")
    if not 1 <= len(text) <= MAX_CHARS or "\n" in text or not text.strip():
        print("error: entry.txt fails the gate on read-back", file=sys.stderr)
        return 1

    print(f"wrote {path}: {len(LINE)} characters, 1 line")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
