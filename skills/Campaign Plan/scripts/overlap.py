#!/usr/bin/env python3
"""Locate all maximal shared runs of five or more normalized words, offline."""

import bisect
import json
import re
import sys
import unicodedata

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
  --self-test      Run offline planted-overlap, clean, occurrence, wrap-hyphen,
                   soft-hyphen, normalization and unspaced-script tests.
  --help, -h       Print this help without opening inputs.
Each word is NFC-normalized and case-folded before comparison; punctuation
(including underscores) and whitespace separate words. Combining marks
(U+0300-036F, U+1AB0-1AFF, U+1DC0-1DFF, U+20D0-20FF, U+FE20-FE2F) and soft
hyphens (U+00AD) belong to the word; a soft hyphen is dropped from its value.
A hyphen followed by optional spaces, a line break and optional spaces between
two word fragments is read both as one joined word and as two words, and runs
found either way are reported. Every maximal run of at least five words is
reported at every occurrence pair, including repeats. Contained windows at the
same alignment are subsumed.
Locations: one-based lines, columns and word numbers; zero-based character
offsets into the original text; end_column and end offsets are exclusive. Word
numbers count each wrapped fragment as a word. Input line endings are retained
for offsets.
Clean: one JSON object on stdout, exit 0. Matches: full JSON report on stderr,
empty stdout, exit 1. Text in either file holding a script written without
spaces between words (Han, Hiragana, Katakana, Thai, Lao, Khmer, Myanmar, the
CJK extension planes) is refused: this check cannot see word boundaries there,
so a JSON error names that text, the script and its first location, exit 1.
Other failures: JSON error on stderr, exit 1.
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


MARKS = "\u0300-\u036f\u1ab0-\u1aff\u1dc0-\u1dff\u20d0-\u20ff\ufe20-\ufe2f"
WORD = re.compile("(?:[^\\W_]|[\u00ad" + MARKS + "])+")
# A hyphen, optional spaces, a line break and optional spaces between two
# fragments may be a wrapped word or a compound: both readings are compared.
WRAP = re.compile("[-\u2010][ \t]*(?:\r\n|\r|\n)[ \t]*")
SOFT_WRAP = re.compile("[ \t]*(?:\r\n|\r|\n)[ \t]*")
UNSPACED = (
    ("Han", 0x2E80, 0x2FDF), ("Han", 0x3005, 0x3007), ("Han", 0x3021, 0x3029),
    ("Han", 0x3038, 0x303B), ("Hiragana", 0x3040, 0x309F),
    ("Katakana", 0x30A0, 0x30FF), ("Katakana", 0x31F0, 0x31FF),
    ("Han", 0x3400, 0x4DBF), ("Han", 0x4E00, 0x9FFF), ("Han", 0xF900, 0xFAFF),
    ("Katakana", 0xFF66, 0xFF9D), ("Thai", 0x0E00, 0x0E7F), ("Lao", 0x0E80, 0x0EFF),
    ("Myanmar", 0x1000, 0x109F), ("Khmer", 0x1780, 0x17FF), ("Khmer", 0x19E0, 0x19FF),
    ("Myanmar", 0xA9E0, 0xA9FF), ("Myanmar", 0xAA60, 0xAA7F),
    ("Hiragana", 0x1B000, 0x1B16F), ("Han", 0x20000, 0x3FFFF),
)


class UnspacedScript(ValueError):
    """The text holds a script this word-run check cannot segment."""


def value(raw):
    folded = unicodedata.normalize("NFC", raw.replace("\u00ad", "")).casefold()
    return unicodedata.normalize("NFC", folded)


def tokens(text):
    """Word fragments as (value, start, end, joins_next) in the original text."""
    words = []
    for match in WORD.finditer(text):
        word = value(match.group())
        if word:
            words.append([word, match.start(), match.end(), False])
    for here, after in zip(words, words[1:]):
        gap = text[here[2]:after[1]]
        here[3] = bool(WRAP.fullmatch(gap) or (
            text[here[1]:here[2]].endswith("\u00ad") and SOFT_WRAP.fullmatch(gap)))
    return [tuple(word) for word in words]


UNSPACED_CHAR = re.compile("[" + "".join(
    f"\\U{low:08x}-\\U{high:08x}" for _, low, high in UNSPACED) + "]")


def unspaced(text, name):
    found = UNSPACED_CHAR.search(text)
    if found:
        point = ord(found.group())
        script = next(script for script, low, high in UNSPACED if low <= point <= high)
        offset = found.start()
        line = text.count("\n", 0, offset) + 1
        column = offset - (text.rfind("\n", 0, offset) + 1) + 1
        raise UnspacedScript(
            f"The {name} text holds {script} script at line {line}, column {column}, "
            "written without spaces between words; this check cannot see word "
            "boundaries in that text")


def location(lines, words, start, count):
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


def windows(words, start, size=5):
    """Every reading of `size` words from fragment `start`, joined or not."""
    found = []

    def walk(at, taken):
        if len(taken) == size:
            found.append(tuple(taken))
            return
        joined = ""
        for stop in range(at, len(words)):
            joined += words[stop][0]
            walk(stop + 1, taken + [joined])
            if not words[stop][3]:
                break
    walk(start, [])
    return found


def extend(left, right, plan_at, source_at):
    """Finest common reading from aligned starts: (units, plan_end, source_end)."""
    units = []
    while plan_at < len(left) and source_at < len(right):
        plan_end, source_end = plan_at, source_at
        a, b = left[plan_at][0], right[source_at][0]
        while a != b:
            if len(a) < len(b) and b.startswith(a) and left[plan_end][3] \
                    and plan_end + 1 < len(left):
                plan_end += 1
                a += left[plan_end][0]
            elif len(b) < len(a) and a.startswith(b) and right[source_end][3] \
                    and source_end + 1 < len(right):
                source_end += 1
                b += right[source_end][0]
            else:
                return units
        units.append((a, plan_at, plan_end, source_at, source_end))
        plan_at, source_at = plan_end + 1, source_end + 1
    return units


def shared_runs(plan, source):
    unspaced(plan, "plan")
    unspaced(source, "source")
    left, right = tokens(plan), tokens(source)
    plan_lines = [0] + [match.end() for match in re.finditer("\n", plan)]
    source_lines = [0] + [match.end() for match in re.finditer("\n", source)]
    index = {}
    for start in range(len(right)):
        for key in windows(right, start):
            starts = index.setdefault(key, [])
            if not starts or starts[-1] != start:
                starts.append(start)
    visited = set()
    matches = []
    for plan_start in range(len(left)):
        source_starts = set()
        for key in windows(left, plan_start):
            source_starts.update(index.get(key, []))
        for source_start in sorted(source_starts):
            # A seed inside a run already found at this alignment is skipped.
            if (plan_start, source_start) in visited:
                continue
            units = extend(left, right, plan_start, source_start)
            visited.update((unit[1], unit[3]) for unit in units)
            if len(units) < 5:
                continue
            plan_end, source_end = units[-1][2], units[-1][4]
            matches.append({
                "word_count": len(units),
                "normalized_run": " ".join(unit[0] for unit in units),
                "plan": location(plan_lines, left, plan_start, plan_end - plan_start + 1),
                "source": location(source_lines, right, source_start,
                                   source_end - source_start + 1),
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
    unicode_match = shared_runs("STRASSE caf\u00e9 has five useful words",
                                "Stra\u00dfe CAF\u00c9 has five useful words")
    assert unicode_match[0]["word_count"] == 6
    assert not shared_runs("", "")
    # Punctuation is a word separator, not deletion: don't and dont differ.
    assert [word[0] for word in tokens("don't")] == ["don", "t"]
    assert not shared_runs("don't stop before the fifth word",
                           "dont stop before a fifth word")
    assert planted[0]["plan"]["end_column"] == 40
    # A wrap hyphen or a soft hyphen inside a quoted word still matches the
    # reflowed plan, located in the original source text.
    reflowed = "We need the test log before signing extra copies."
    wrapped = "Notes: we need the test log be-\nfore signing extra copies."
    wrap_match = shared_runs(reflowed, wrapped)
    assert len(wrap_match) == 1 and wrap_match[0]["word_count"] == 9
    assert wrapped[wrap_match[0]["source"]["start_offset"]:
                   wrap_match[0]["source"]["end_offset"]] == \
        "we need the test log be-\nfore signing extra copies"
    assert wrap_match[0]["source"]["end_line"] == 2
    soft = "Notes: we need the test log be­fore signing extra copies."
    soft_match = shared_runs(reflowed, soft)
    assert len(soft_match) == 1 and soft_match[0]["word_count"] == 9
    # A compound wrapped at its own hyphen still matches the plan's compound,
    # and both readings combine inside one quotation.
    compound = shared_runs("A well-known rule of the trade.",
                           "Here a well-\n  known rule of the trade.")
    assert len(compound) == 1 and compound[0]["word_count"] == 7
    mixed = shared_runs("act before well-known rules apply",
                        "act be-\nfore well-\nknown rules apply")
    assert len(mixed) == 1 and mixed[0]["word_count"] == 6
    # NFC and NFD spellings of the same French sentence match.
    nfc = unicodedata.normalize("NFC", "Les acheteurs ont déjà besoin du journal.")
    nfd = unicodedata.normalize("NFD", nfc)
    assert nfc != nfd
    french = shared_runs(nfc, nfd)
    assert len(french) == 1 and french[0]["word_count"] == 7
    assert french[0]["source"]["end_offset"] == len(nfd) - 1
    # A script written without spaces fails closed, never clean.
    chinese = "记者已经在报道这个故事"
    for pair in ((chinese, chinese), ("Plain English text here.", chinese)):
        try:
            shared_runs(*pair)
        except UnspacedScript as error:
            assert "cannot see word boundaries" in str(error) and "Han" in str(error)
        else:
            raise AssertionError("unspaced script returned a result")
    path_result = path_self_test()
    return {"status": "passed", "tests": [
        "planted near-quote found (7 words, exact locations)", "clean pair passes",
        "four words ignored; five found", "all four repeated occurrence pairs found",
        "contained windows subsumed", "Unicode casefold", "empty pair passes",
        "apostrophes separate words; exclusive end_column",
        "wrap hyphen and soft hyphen match the reflowed plan",
        "wrapped compound and mixed readings match", "NFC matches NFD",
        "unspaced script refused, never clean", path_result,
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
    except UnspacedScript as error:
        print(json.dumps({"error": str(error),
                          "fix": "No clean result is possible for this text here; "
                                 "the overlap check stays uncompleted"}),
              file=sys.stderr)
        return 1
    except (OSError, ValueError, AssertionError) as error:
        message = str(error) or "Self-test assertion failed"
        print(json.dumps({"error": message,
                          "fix": "Supply readable UTF-8 plain-text paths; see overlap.py --help"}),
              file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
