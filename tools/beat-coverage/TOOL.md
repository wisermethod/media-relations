---
name: beat-coverage
type: tool
category: media-relations
description: Pull dated beat-matching coverage from reporter files into Markdown with every item marked unverified, or return counts only
version: 0.1.0
---

# beat-coverage

## Context

The reader step of Angle Finder's story-first menu: collect the coverage already recorded in a directory of reporter files for a date window and optional beat expression. It does not decide stories or open pages. A file's existing source labels do not make this reading a verification: every returned item carries **unverified**.

Classifier seam: none.

## Quick Start

Run from this tool's directory. Node built-ins cover every command; nothing installs.

```bash
node scripts/beat-coverage.js help
node scripts/beat-coverage.js count --dir /path/to/work/reporters --from 2026-01-01 --to 2026-11-05 --beat '\bagent'
node scripts/beat-coverage.js pull --dir /path/to/work/reporters --from 2026-01-01 --to 2026-11-05 --beat '\bagent' --output /path/to/work/coverage.md
```

Omit `--output` to return the Markdown in the `markdown` field of the one JSON object on stdout. `pull` with `--output` returns `{ "counts": { ... }, "output": "<resolved path>" }`. `count` returns the counts object alone. `help`, `--help`, `-h`, and `<command> help` return `{ "usage": "<usage text>" }`, before any file is read. Help also uses JSON so every successful run has the same stdout discipline.

## Commands and options

| Command | Reads | Writes | Stdout |
|---------|-------|--------|--------|
| `pull` | The selected reporter files | One new Markdown file when `--output` is given | `counts` and either `output` or `markdown` |
| `count` | The selected reporter files | Nothing | Counts only |
| `help` | Nothing | Nothing | `usage` |

| Option | Applies to | Meaning |
|--------|------------|---------|
| `--dir <path>` | `pull`, `count` | Required absolute directory of reporter Markdown files; no recursion |
| `--from <YYYY-MM-DD>` | `pull`, `count` | Required first date, inclusive |
| `--to <YYYY-MM-DD>` | `pull`, `count` | Required last date, inclusive; must be on or after `--from` |
| `--beat <regex>` | `pull`, `count` | Case-insensitive JavaScript regular expression over each recorded item, including its continuation text; omitted means no beat filter |
| `--exclude <name>` | `pull`, `count` | Exact file name to skip before reading; repeatable; no directory components |
| `--output <path>` | `pull` | New absolute `.md` file outside this tool; its parent must already exist; an existing destination is refused |
| `--help`, `-h` | Every command | Return usage without reading input |

Options other than `--exclude` may be given only once. No command accepts `--install` or `--env`. The behavior shared with other tools is governed by `wiser/standards/script-contract.md` and described in `wiser/tools/RUNNING.md`; this tool's help is JSON as specified above.

## What it reads

Visible `.md` files immediately inside `--dir`, in file-name order. Excluded files and subdirectories are not read. A link is resolved before reading; it must remain within the input directory and resolve to a visible Markdown file. Exclusion checks both the listed name and the resolved name.

- Older reporter files: numbered or bulleted items under headings starting `Compelling work` or `Most recent`, with their continuation lines.
- Bio Sketch files identified by `schema: bio-sketch` or the `Bio sketch:` title: bullets under `Record`, and `Item:` bullets under any other heading. Role, beat, outlet, and assessment statements are not coverage items. The base format is `skills/Bio Sketch/sketch-format.md` in `wiser`; the journalist extension is `skills/Reporter Research/journalist.md` in this plugin.

Headings end the preceding item. Empty `Not available:` records and fenced code blocks are ignored. Duplicate recorded items stay separate; no source is opened or deduplicated.

For an older item, the first ISO date on its first line is its date. `YYYY-MM` is compared as that month's first day and marked month only. A standalone year is included only when it equals the window's last year, even if the window starts partway through that year; the output explicitly marks this inclusion. For a Bio Sketch record, an explicit `Published:`, `Date:`, or `As of:` date is used; per the base format, a record's `As of:` is its publication date. Otherwise its value is checked before source metadata, so a URL or read date cannot date an undated record. Invalid dates count as undated.

The beat expression is applied first, matching the recorded item and its continuation lines. Rejection counts are disjoint: an off-beat item increments only `off_beat`; a matching item then increments `undated`, `outside_window`, or `kept`. `year_only` is the subset of `kept` included on a year alone. Thus `items = kept + undated + off_beat + outside_window`.

## What it writes

Markdown grouped by file, with one bullet line per kept item in recorded order. Each line names its file and original section, carries **unverified** and the recorded date, and retains the recorded item text, including its headline and outlet as supplied. No headline or outlet is inferred from a role or another item. Continuation lines are joined onto that line; `Traction:` continuation lines are dropped, including bold or bulleted forms. The beat test uses the original recorded text before that output-only removal.

| Count field | Meaning |
|-------------|---------|
| `files` | Files actually read after exclusions |
| `items` | Coverage items found before filtering |
| `kept` | Items selected, including year-only items |
| `year_only` | Kept items dated only by year |
| `undated` | Beat-matching items without a usable date |
| `off_beat` | Items failing the beat expression |
| `outside_window` | Beat-matching dated items outside the window, including other years |
| `bytes` | Total source bytes read, before filtering |

Only `pull --output` writes a deliverable. It creates no parent directories and replaces nothing. The caller creates its declared destination directory before passing `--output`; to keep Markdown in the session instead, omit that option. The output screen compares every existing ancestor's device and inode with this tool directory, so a different case or symbolic link cannot hide a destination inside it. A failed or interrupted write can leave an incomplete new output; inspect it and choose a fresh path. Tests create temporary `beat-coverage-test-<random>` siblings beside this tool and remove their own directories after ordinary success or failure; interruption can leave them. No run contacts an external service.

## Troubleshooting

| Stop | Fix |
|------|-----|
| Required option missing, invalid calendar date, or reversed window | Supply `--dir`, `--from`, and `--to` with a valid inclusive window |
| Invalid `--beat` | Correct the JavaScript regular expression; quote it so the shell preserves backslashes |
| Unknown or repeated option | Read `help`; repeat only `--exclude` |
| Relative path or unreadable input | Pass an absolute, readable directory |
| Reporter link leaves the directory or points to a non-Markdown file | Remove it from the input directory or skip its name with `--exclude` |
| Output exists, resolves inside this tool, has no existing parent, or lacks `.md` | Choose a new absolute Markdown path in an existing work directory outside this tool |
| Fewer items than expected | Check the coverage headings or `Item:` tokens, the recorded dates, exclusions, and disjoint rejection counts; this tool supplies no missing coverage |

## Success

- `pull` returns every selected recorded item once per occurrence, grouped by file, with file, section, recorded headline, outlet and date, and **unverified** on each item line.
- Both reporter shapes work; year-only inclusions are marked, undated and off-beat items are omitted and counted, and output carries no `Traction:` lines.
- Every successful command prints one JSON object. Usage errors and read or write failures print only to stderr and exit 1. Help needs no input directory or configuration.
- `node --test` in this directory passes on synthetic fixtures without installing anything or opening a network connection.
