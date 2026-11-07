#!/usr/bin/env python3
"""Locate all maximal shared runs of five or more normalized words, offline."""

import bisect
import json
import re
import sys

sys.dont_write_bytecode = True

import os as _os
sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))  # this script's own folder, also under python -I
from paths import screen_path, self_test as path_self_test


HELP = """Campaign Plan unpublished-source overlap check (no dependencies or writes).
Usage: python3 overlap.py --plan <absolute.txt> --source <absolute.txt>
       python3 overlap.py --self-test
       python3 overlap.py help
Options:
  --plan <path>     Complete client-facing plan as UTF-8 plain text.
  --source <path>   Complete unpublished source as UTF-8 plain text.
  --self-test      Run offline planted-overlap, clean and occurrence tests.
  --help, -h       Print this help without opening inputs.
Case is folded; punctuation (including underscores) and whitespace separate
words. Every maximal run of at least five words is reported at every occurrence
pair, including repeats. Contained windows at the same alignment are subsumed.
Locations: one-based lines, columns and word numbers; zero-based character
offsets; end_column and end offsets are exclusive. Input line endings are
retained for offsets.
Clean: one JSON object on stdout, exit 0. Matches: full JSON report on stderr,
empty stdout, exit 1. Other failures: JSON error on stderr, exit 1.
Paths must be absolute regular files. Protected .env and memory paths are
refused before reading. No configuration, installation, network or stdin.
Unknown and duplicate flags are refused; see --help.
"""


def options(argv):
    values = {}
    allowed = {"--plan", "--source", "--self-test", "--help", "-h"}
    if not argv or argv == ["help"]:
        return {"--help": True}
    index = 0
    while index < len(argv):
        flag = argv[index]
        if flag not in allowed:
            raise ValueError(f"Unknown option {flag}; see overlap.py --help")
        if flag in values:
            raise ValueError(f"Duplicate option {flag}; use it once; see --help")
        index += 1
        if flag in {"--plan", "--source"}:
            if index == len(argv) or argv[index].startswith("--"):
                raise ValueError(f"{flag} needs a path; see --help")
            values[flag] = argv[index]
            index += 1
        else:
            values[flag] = True
    if values.get("--self-test") and set(values) != {"--self-test"}:
        raise ValueError("--self-test must be used alone; see --help")
    return values


def source_path(value):
    return screen_path(value, file=True)


def tokens(text):
    return [(match.group().casefold(), match.start(), match.end())
            for match in re.finditer(r"[^\W_]+", text, re.UNICODE)]


def location(text, words, start, count):
    lines = [0] + [match.end() for match in re.finditer("\n", text)]
    begin = words[start][1]
    end = words[start + count - 1][2]
    first_line = bisect.bisect_right(lines, begin)
    last_line = bisect.bisect_right(lines, end - 1)
    return {
        "line": first_line, "column": begin - lines[first_line - 1] + 1,
        "end_line": last_line, "end_column": end - lines[last_line - 1] + 1,
        "start_word": start + 1, "end_word": start + count,
        "start_offset": begin, "end_offset": end,
    }


def shared_runs(plan, source):
    left, right = tokens(plan), tokens(source)
    left_words = [word[0] for word in left]
    right_words = [word[0] for word in right]
    index = {}
    for start in range(len(right) - 4):
        key = tuple(right_words[start:start + 5])
        index.setdefault(key, []).append(start)
    matches = []
    for plan_start in range(len(left) - 4):
        key = tuple(left_words[plan_start:plan_start + 5])
        for source_start in index.get(key, []):
            # Only the leftmost seed at this alignment extends a maximal run.
            if (plan_start and source_start and
                    left_words[plan_start - 1] == right_words[source_start - 1]):
                continue
            count = 5
            while (plan_start + count < len(left) and
                   source_start + count < len(right) and
                   left_words[plan_start + count] == right_words[source_start + count]):
                count += 1
            matches.append({
                "word_count": count,
                "normalized_run": " ".join(left_words[plan_start:plan_start + count]),
                "plan": location(plan, left, plan_start, count),
                "source": location(source, right, source_start, count),
            })
    return matches


def self_test():
    # Punctuation and a line break hide the planted near-quote from a literal find.
    plan = "Opening.\nBuyers NEED the test-log before signing."
    source = "Notes: buyers need the test log before signing; then ask why."
    planted = shared_runs(plan, source)
    assert len(planted) == 1 and planted[0]["word_count"] == 7
    assert planted[0]["plan"]["line"] == 2
    assert planted[0]["plan"]["column"] == 1
    assert planted[0]["source"]["column"] == 8
    assert plan[planted[0]["plan"]["start_offset"]:
                planted[0]["plan"]["end_offset"]] == "Buyers NEED the test-log before signing"
    assert not shared_runs("A fresh view of repair records.",
                           "Shipping invoices mention a delayed parcel.")
    assert not shared_runs("one two three four", "one two three four")
    assert len(shared_runs("one two three four five", "ONE, TWO three four FIVE")) == 1
    repeated = shared_runs("one two three four five gap one two three four five",
                           "one two three four five break one two three four five")
    assert len(repeated) == 4
    assert all(match["word_count"] == 5 for match in repeated)
    assert len(shared_runs("red blue red blue red blue", "red blue red blue red blue")) == 1
    unicode_match = shared_runs("STRASSE café has five useful words",
                                "Straße CAFÉ has five useful words")
    assert unicode_match[0]["word_count"] == 6
    assert not shared_runs("", "")
    # Punctuation is a word separator, not deletion: don't and dont differ.
    assert [word[0] for word in tokens("don't")] == ["don", "t"]
    assert not shared_runs("don't stop before the fifth word",
                           "dont stop before a fifth word")
    assert planted[0]["plan"]["end_column"] == 40
    path_result = path_self_test()
    return {"status": "passed", "tests": [
        "planted near-quote found (7 words, exact locations)", "clean pair passes",
        "four words ignored; five found", "all four repeated occurrence pairs found",
        "contained windows subsumed", "Unicode casefold", "empty pair passes",
        "apostrophes separate words; exclusive end_column", path_result,
    ]}


def main(argv=None):
    try:
        args = options(sys.argv[1:] if argv is None else argv)
        if args.get("--help") or args.get("-h"):
            print(HELP, end="")
            return 0
        if args.get("--self-test"):
            print(json.dumps(self_test()))
            return 0
        if "--plan" not in args or "--source" not in args:
            raise ValueError("--plan and --source are required; see --help")
        # Screen both before reading either. No universal-newline conversion:
        # offsets address characters in the original UTF-8-decoded file.
        plan_path = source_path(args["--plan"])
        unpublished_path = source_path(args["--source"])
        with plan_path.open(encoding="utf-8", newline="") as handle:
            plan = handle.read()
        with unpublished_path.open(encoding="utf-8", newline="") as handle:
            unpublished = handle.read()
        matches = shared_runs(plan, unpublished)
        report = {"status": "overlap" if matches else "clean", "minimum_words": 5,
                  "plan": str(plan_path), "source": str(unpublished_path),
                  "matches": matches}
        if matches:
            report["fix"] = "Rewrite or remove every located run, then rerun on current text"
        print(json.dumps(report), file=sys.stderr if matches else sys.stdout)
        return 1 if matches else 0
    except (OSError, ValueError, AssertionError) as error:
        message = str(error) or "Self-test assertion failed"
        print(json.dumps({"error": message,
                          "fix": "Supply readable UTF-8 plain-text paths; see overlap.py --help"}),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
