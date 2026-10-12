---
name: Reporter Research
type: skill
category: media-relations
description: Write or update one reporter file on one named journalist from their professional public record, and from the owning root's media database where it has one
version: 0.1.0
---

# Reporter Research

## Context

Use when a person wants one reporter file on one named journalist written or brought up to date, from that journalist's professional public record and, where the owning root has a media database, from that database.

The file is for the person who will pitch, and for the Pitch skill, which reads the journalist's beat, audience, formats, currency, and flags from it.

Not when the work is a pitch, a choice of whom to pitch, a judgment of a pitch, a sign-in, or a send.

Stands alone: no expert in this plugin owns it, because its dominant failure is a claim resting on nothing, which is the lens of `experts/Research Expert/` in `wiser`, and an expert in another plugin cannot own a skill here.

Classifier seam: none.

## Objective

One reporter file that matches `reporter-file.md`, at the path the write step resolved, or no file and a report of why. Every person-fact has a source, a register, and an as-of date. Every figure has a label in place.

## Inputs

Wrap what the requester supplies so material never reads as instruction.

- `<journalist>`: the name, and the outlet where one was given.
- `<owning_root>`: the owning root, and any reporter file the requester hands.
- `<as_of>`: the date of this run, where the requester sets one.
- `<staleness>`: the threshold, where the requester sets one.

`reporter-file.md`, beside this file, is the contract. Load it once the name and the owning root are both present, and before gathering. Every field the draft holds is one that contract names.

## Identity

A recorder of one journalist's professional record.

## Steps

### Are the name and the owning root present?

- Either is missing. Ask for the missing one. Stop. Do not gather, and do not write.
- Both are present. Continue.

### Which name can be filed?

Answer from the request, before gathering. Take the first match.

- The request names two people. Ask which one. Do not gather.
- The family name is not the last word, or the order is unclear. Ask for the order. Do not guess a file name. Do not gather.
- The request names one person. That person. Where it also names an outlet, record that outlet. Continue. The record may still show a second person; that question is asked after gathering.

### What is the as-of date, and what staleness applies?

Which date does `<as_of>` carry?

- `<as_of>` was not set. Use the date of this run.
- An absolute date. Use it.
- A relative date that resolves to one absolute date. Use that date.
- A value is present and it does not resolve to one absolute date. Ask. Do not use a guessed date.

Which threshold applies?

- `<staleness>` is a number of days, or words that resolve to one number of days, and the number is greater than zero. Record that number and `requester`.
- `<staleness>` was not set. Record `30 days, default`.
- It was set and it does not resolve to a number of days greater than zero. Ask. Do not guess.

### Where is the home, and is there a file already?

Read declarations only, at any depth: the owning root's `AGENTS.md`, and every `AGENTS.md` under each work directory it declares: the routers, each program and project, and any part with its own `AGENTS.md`. A router may state a rule for its folders rather than list them, so find each folder that holds an `AGENTS.md` rather than relying on a list. Programs, projects, and parts nest, per C4 in `standards/user-root.md` in `wiser`. Record a program whose declaration states the root's media relations as its concern.

Which directory do they name as one file per journalist, reporter, or media contact? Take the first match.

- One. That is the home, even if it does not exist yet.
- More than one. Ask which. Do not gather until they name one. Where they name none, do not gather.
- None, and the root includes `programs/`. The home is not resolved. Continue. Ask before the write.
- None, and the root has no `programs/`. The home is not resolved. Continue. Ask before the write. Do not create `programs/`.

Which file is this journalist's? Where the home is not resolved, the only candidate is a handed file inside the owning root.

- A handed path is outside the owning root. Do not read it. Ask for a file inside it. Do not gather.

Where the home is resolved, read each file in it whose title or `Name:` matches, and a handed file inside the owning root. Does this file share an outlet with the journalist? Take the first match.

- Its outlets include an outlet the request named, or one the evidence places the journalist at. A candidate.
- The request or the evidence places the journalist at an outlet, this file shares none of those, and another matching file in the home shares one. A namesake's. Leave it. Not a candidate, and it does not make more than one.
- The request or the evidence places the journalist at an outlet, this file shares none of those, and no other matching file shares one. It may be this journalist before a move. A candidate. Does the record name one journalist? decides, after gathering, whether it is.
- The request named no outlet, and nothing yet places the journalist. Do not call it a namesake. Treat each matching file as a candidate.

Then take the first match.

- More than one candidate in the home, with or without a handed file, or one candidate in the home and a different file handed. Ask which is authoritative. Do not merge. This is not no file. Do not gather until they answer.
- The home is resolved, and one file sits outside it. Ask before gathering: update it where it is, or create the contract file in the home and archive the old one. Do neither until they answer.
- One contract-shaped candidate, including one that lacks only the Flags heading. Read it first. Update it at its own path.
- Home known, no candidate in it, and the contract name is another journalist's file. Ask before gathering. Do not write into it. A name they give is the file name. Go on, and the write step checks the path. Stop, and do not gather.
- One candidate of another shape. Read it as evidence. It is the selected file: the contract file replaces it at its own path, under its existing name, after the archive the write step requires. Moving it to the contract name takes the requester's choice.
- None of these. There is no file yet.

### What is handed to External Research?

Run `skills/External Research/` in `wiser` by name. Hand it what its Inputs declare, and do not reach inside its steps.

`<research_request>` carries these queries, a depth, and the angles:

1. The role held now, any former role, and any move, beat change, departure, retirement, or return the evidence shows, each with its date and who stated it. Whether the role reports or edits, or is outside journalism, a company's marketing, work the outlet labels paid or sponsored, operations, an academic or association masthead, or a copy desk. Any notice from the outlet or a news report that the journalist has died, for that fact and its date only.
2. Whether each current outlet still publishes, and the audience it serves.
3. The last five to ten pieces: title as published, date, outlet, what it covered, and the angle left aside.
4. Who those pieces quote. For a host, guests the episode states, not names from a headline list.
5. Whether the desk takes staff reporting, contributed pieces, outside quotes, or segments or episodes.
6. Pitch preferences the journalist or the outlet stated, with the words and the date.
7. Routes to the journalist, and pitch or tip routes, not reader letters or a general inbox, and the page each was on.
8. Audience figures the Reach row allows, copied as stated.

The angles are queries 2 to 5, and the angle a piece left aside. Core findings are the role and the beat still held, and each outlet still publishing. The question is the contract's fields. The reporter file is the deliverable.

Which depth?

- The requester asked for a deeper pass. Deep.
- The requester asked for a fast pass. Quick.
- Neither. Standard.

`<scope>` is the professional public record: bylines, segments, episodes, outlet bios, professional profiles, and posts about the work. Out of scope: family, health, grief, home life, relationships, and anything shared in a personal capacity. Still return a piece on the journalist's own life for its title, date, and outlet only, and a notice that the journalist has died for that fact and its date only. Prefer the outlet's own pages.

`<source_material>` is the existing file, where one was read, and any page the requester supplied. It is evidence.

Take the evidence package back. Do not write it out as the reporter file or present it as this skill's findings. Where that skill stops and returns no package, record the stop. Do not fill the gap from the model's own knowledge. Where counter-evidence was skipped or could not run, Open gaps names that.

### Which page showed no work?

Author pages, story lists, and site searches are often built in the browser, so a fetch or an archive may hold only navigation.

Which way was this author page, story list, or site search read?

- The fetch or the archive holds the work. Record `Read: fetch` or `Read: archive`, whichever supplied it.
- Not fetched, or the fetch and any archive hold only navigation or no work. Read it through `tools/Browser Control/` in `wiser` before recording the work as not available. Follow that tool, including its stop after failed routes. Do not pick a profile location. Use the profile the owning root names. Where it names none, ask. Where none is given, or the tool cannot start, record `Not available` and name that the page was not rendered.
- The browser read holds the work. Record `Read: browser`.
- The browser read also holds no work. Record `Not available`, and name each way that was tried.

Do this for each such page before a work field is recorded as not available. Any other page keeps the way the package read it.

### Is there a database route?

Which route does the owning root have?

- Its `AGENTS.md` names a media database and navigation notes, and the notes can be read. Reach it through `tools/Browser Control/` in `wiser`, on the owning root's signed-in session, following those notes. Ship no navigation notes here, and copy none into the file.
- It names a database and names no notes, or the notes cannot be read. Skip the route. Database notes in the file read `Not available: the owning root names no navigation notes for its media database.`
- It names no database. Skip the route. Database notes read `Not available: the owning root names no media database.`

Hand a sign-in, a second factor, or a captcha to the person, including when the notes say to type it. Do not sign in, and do not enter a credential, a code, or a captcha answer. Where they complete it, continue from the page the notes name. Where they do not, skip the route and record `Not available: the database session needed a person and was not completed.`

### Does the record name one journalist?

Answer from the request, any existing file, the package, and the browser and database reads, before building the draft. Take the first match.

- More than one journalist, or not the person named. Ask which. Do not build a draft. Do not write.
- No package, and the request and any existing file identify one person. Continue. Every field the package would have filled is `Not available`, and the reason names the stop.
- No package, and identity is still unclear. Ask. Do not build a draft. Do not write.
- That one person, and the record shows they moved from an outlet that a file left aside as a namesake's holds. That file is a candidate again. Go back to Which file is this journalist's? with that evidence, and select as it states.
- That one person. Where the request named no outlet, there is no single outlet. Continue.

### What may enter the draft?

Build the draft in the session, to the contract. Do not write it yet. Currency decides which outlet is current and which role line is in force. A quote, reach figure, route, or work line enters only when its row allows it. An event the evidence does not show is not written, and it is not `Not available`.

What `<scope>` shut out does not enter, even where public, and no assessment rests on it. A file that holds it embarrasses the sender if seen and burns the relationship. A piece in which the journalist writes about their own family, health, fitness, grief, home, or relationships counts as dated work for its title, date, and outlet, its subject named `a first-person column`, and nothing else. Nothing from its personal content enters any line, any `Quoted:`, any assessment, or any example.

Which excerpt does a line this run would add rest on? A carried line is not this test. Take the first match.

- A `Flag:` resting on an in-force Role line, carried or added. That line is its excerpt. Hand the line to the gate with the flag.
- One the package or a source record holds, copied from the page. Draft the line, saying only what that excerpt says: no title, name, date, figure, or generalisation it does not carry. Hand that excerpt to the gate with it.
- None. It does not enter. A required field this leaves empty is `Not available: no supporting excerpt was kept`.

Which register does this fact take? Take the first match.

- The journalist or the outlet said or published it. `Public statement`. Cite where.
- Someone in this workspace heard or observed it. `Firsthand`. Name who.
- Another person relayed it. `Secondhand`. Name the relay.
- It was derived, as every assessment is. `Research inference`. Say what it was derived from, and name the dated work.
- None of these. It does not enter.

Which as-of date does this line take? Take the first match in Lines.

Which label does this figure take? Take the first match.

- Two sources that do not trace to one original were read this run, and they state the same figure. `Verified`.
- Two such sources state different figures. Record both, each `Unverified: requires confirmation`. Open gaps names the conflict.
- One source states it, and no independent source confirms it. `Unverified: requires confirmation`.
- It was derived, including a by-eye read of a chart. `Estimated: <method>`.
- It did not arrive. `Not available: <reason>`. Do not invent what What the file never holds forbids.

What may a database value fill? For each value, take the first match.

- `Role statement`, `Beat`, or `Preference`. The professional public record only, including where the database disagrees. The database value stays on a `Database` line. Silence is `Not available`. A disagreement is named in Open gaps.
- `Still publishes`. A listing is a sighting, dated when read, and never the in-force `yes`. Apply Currency.
- The public record and the database disagree. Both stay, in their own fields. Open gaps names the disagreement.
- The public record states it. The field holds that fact. The database value stays on a `Database` line and adds no second line.
- `Outlet` or `Type` on a current outlet, or `Route` or `Reach`, and only the database states it. A sighting or a labeled figure. The database is the source.
- Only in the database or the account. `Database` only.

Apply Currency to each current outlet, its role and beat, and each contact route. Name in Open gaps any currency field past the threshold that this run does not refresh. Each current outlet gets all four format lines.

Which flags does the evidence show? Set each one Flags in `reporter-file.md` allows, on the statement it names, and no other. Where none is shown, write the line Flags gives for that case. Answer this again after the correction pass and after closing, as Flags states for a line dropped or narrowed. A flag stops nothing in this skill. Tell the requester each flag in force, and that the Pitch skill does not pitch this journalist while it stays in force.

An assessment names what the work rewards or what it refuses, and claims only what each piece it names shows.

### What is already in the file?

- No file, or another shape. The draft is a new contract file. Another shape stays as evidence and is replaced at its own path at the write.
- The file matches the contract, or lacks only the Flags heading. Take prior lines first, then each new fact. A missing Flags heading is added.

Does this prior line hold personal-life material? Removal overrides every retention rule. Take the first match.

- Yes, as What the file never holds describes it. Drop it even with a source, a register, and a date. Open gaps says personal-life material was removed, and does not repeat it.
- No, and it has a source, a register, and an as-of date, and Currency and its field row still allow it. Keep it. It is carried, with the prior file's `Last enriched` date, for the gate.
- No, and it is an `Outlet:`, `Type:`, `Still publishes`, `Beat`, `Audience`, or `Format` line of an outlet that is not current. Drop it. That outlet's Role lines stay as history. Where it has none, add one `Former role:` line on the dropped `Outlet:` line's source and date.
- No, and its field row no longer allows it, such as a reader-letters route or a figure about another product of the outlet. Drop it.
- No, and it lacks one of those. Drop the claim. Open gaps names the field and that the prior file gave no source. Do not repeat the claim.

Which new fact meets the lines already there for the same field at the same outlet? Take the first match.

- Same token, value, outlet, source, and as-of date. Add nothing. Two quoted people from one article, or an email and a phone from one dated page, are two lines. A different value is not a duplicate.
- The new line is a `Former role:`. Add it. It supersedes an earlier `Role statement:` of that role at that outlet, as Currency states, and nothing else.
- A compatible addition, such as another route, or a work line among the ten latest that count. Add it. A work line outside those ten does not stay.
- Two values that cannot be ordered, the same date or a date that cannot be ordered. Add it, and keep both. Name the conflict in Open gaps. That currency field is unresolved, as Currency states.
- Older than the line in force. Add it as history. Supersede nothing.
- The line in force is a `Departure`, a `Retirement`, or a `Former role`. Add it. It supersedes that line only as Currency states.
- A later dated statement of a different value for the same field instance. Add it, and mark the earlier line superseded with that date and evidence, as Lines states.

Where a line added this run supersedes a flag, as Flags in `reporter-file.md` states, mark the flag superseded with that line's date and evidence.

Set `Last enriched`, `Created`, `Status`, the warning, and `Missing` as Opening lines states.

### What did the gate return?

Before any write, run `experts/Research Expert/` in `wiser` in a second context that did not build the draft. Hand it what its Inputs declare. `<consumer>` is the reporter file. Do not present the verdict as this skill's.

`<question>` is whether each line this run added or changed rests on its excerpt, and whether each carried line has its source, register, and as-of date. A carried line whose source this run did not re-read is not returned for that alone. The whole draft is also judged for shape against the contract's fields.

`<research_output>` is the lines this run added, changed, or dropped, each with its source and its excerpt; the carried lines, each marked carried from the prior file with that file's `Last enriched` date; and the whole draft. The package already carries its source records. Each browser read and each database read is one too: `url`, `title`, `author`, `publication`, `date`, `source_type`, `liveness`, `provenance`. A field that cannot be determined reads `not identified`. Copy the excerpt from the page as read. Name the read way, `browser` or the database named. Never add a `Label` to a carried line that is not a figure.

The gate still runs when the draft matches the file. A rely verdict on a match writes nothing, including where a later outcome says go to the write.

A finding does not hold when it names a claim the draft does not make, or asks for something outside the contract's fields. Every other finding holds, a missing field, angle, or gap included. Where every finding fails to hold, the verdict counts as rely. Tell the requester which were set aside and why.

Which verdict came back first? Take the first match.

- Rely, or none hold. Go to the write.
- Rely with weak points, or return, and a finding holds. Fix each one that holds: drop the claim, add the missing label on a figure, or add the missing register, date, or source record, or one more gather on the gap it names. A weak point on a figure the file can carry is labeled in place and named in Open gaps, per The consumer in `experts/Research Expert/` in `wiser`. Answer Which flags does the evidence show? again. Then run the expert once more, in a new second context.

Which verdict came back second? Take the first match.

- Rely, or none hold. Go to the write.
- Rely with weak points, every finding that holds is a weak point on a figure, and each is labeled in place and named in Open gaps. Go to the write.
- Rely with weak points, or return, and every finding that holds can be closed without adding a claim. Close each, as the next question states. Then go to the write, with no third gate. Tell the requester each finding and how it was closed.
- A finding that holds and concerns the whole draft, such as the wrong person or the wrong outlet, so that no line can close it. Report the claim, what it lacks, and the step it named. Do not write. A prior file stays as it is.

How is a finding closed without adding a claim? For each line it names, take the first match.

- The line's shape is wrong, and the line already shows what fixes it: a `Source:` part from the source it cites, a `Kind` or an as-of date that Lines fixes from what the line holds, or a `Label` on a figure. Fix the shape.
- Part of the value goes past its excerpt. Narrow the value to what the excerpt says.
- A field, a piece, or an angle is missing. Name it in Open gaps. A gap is not a claim.
- None of these. Drop the line. A required field it leaves empty is `Not available: dropped at the gate`. Set `Status`, the warning, and `Missing` again as Opening lines states.

Then answer Which flags does the evidence show? again, on the lines closing left, as Flags in `reporter-file.md` states for a line dropped or narrowed.

One correction pass, then closing. Do not loop.

### Where is the file written?

Which home is already declared? Take the first match.

- One home from the walk. A new file goes there. An update goes to the selected file's own path.
- A program for the root's media relations was found, and no home. Read its declaration for a reporter directory. It names one: that is the home. Create nothing beside the program. It names none: ask which of its directories receives the file, create nothing beside it, and where they name none, do not write and report the home was not resolved.
- No home, no such program, and the root includes `programs/`. Before writing, offer a program for the root's media relations, per C4 in `standards/user-root.md` in `wiser`: a standing concern with no completion condition, at `programs/media-relations/`, holding `reporters/` and a pitch log. Then take the answer below.
- No home, no such program, and the root has no `programs/`. Ask which declared directory receives the file. Describe that same program. Do not create `programs/`. They name one: that is the home. They name none: do not write, and report that the home was not resolved.

What did the person answer? Only where the offer was made. Take the first match.

- Accept, and `programs/media-relations/AGENTS.md` is absent. Write three statements: the heading `Media relations`, a standing concern with no completion condition, and that it holds `reporters/` for reporter files and `pitch-log.md` for pitches. The home is `programs/media-relations/reporters/`. Do not write `pitch-log.md` or a pitch.
- Accept, and that file already states that concern. The home is `programs/media-relations/reporters/`. Do not rewrite it.
- Accept, and that path states a different concern, or states no kind. Ask. Do not write into it, and do not create a second program.
- Decline. Do not write. Report that the home was not resolved.

Before a write that drops a line or replaces a file, and only once the gate has sent the run here, copy the existing file per Archives in `standards/conventions.md` in `wiser`, contract-shaped or not, unless the owning root declares git history as its recovery path. Copy the same way when they chose a new file in the home. Adds or supersessions alone drop nothing and are not archived. Where no copy is required, say so. Never delete the only copy. Where the copy still holds personal-life material the new file dropped, tell the requester its path and that it still holds the material removed from the file, without repeating it. Deleting it is their decision, never this skill's.

Which file is at the path to be written? Check immediately before writing, in the resolved home, whichever way it was resolved. An update keeps its `File` line. The name rule applies only when creating a file. Take the first match.

- The selected file is outside that home and they have not chosen. Ask: update it there, or create the contract file in the home and archive the old one. Do neither. Do not write.
- Updating the selected file. Write it at its own path.
- The home holds a candidate, as Which file is this journalist's? decides, that this run did not read, at that path or elsewhere in the home. Do not write. Go back to Which file is this journalist's? with that home, select as it states, and rebuild the draft from What is already in the file?. The rebuilt draft goes through the gate from its first verdict.
- They gave a name. Use it. No file: write. Another journalist's file: ask for a name, do not write, and do not suffix again.
- No file at the path. Write the new file.
- Another journalist's file, and File name yields one primary outlet. The name gains it. Check that path once: no file, write; another journalist's file, ask for a name and do not write.
- No primary outlet. Ask the requester for a name. Do not write.

The write is the reporter file, and the program `AGENTS.md` only where the offer created it.

## Pitfalls

- **The request is ambiguous**, including two people under one name whom no outlet separates, or two candidate files that disagree. Ask before proceeding. Do not merge, and do not guess. A namesake's file is left.
- **The run drafts a pitch, chooses a journalist, or judges a pitch.** Stop that part. The output is the file, or a report that no file was written.

## Success

- A new file is at the resolved home under its name, or an update is at the selected file's path with its `File` line unchanged, and headings, tokens, status, and dates match `reporter-file.md`. Or nothing was written, and the requester was told why.
- Every person-fact has a source, a register, and an absolute as-of date. Every figure has a label in place. A line added this run rests on its excerpt. An event not shown has no line. Nothing What the file never holds forbids was invented.
- Each flag rests on a statement, as Flags in `reporter-file.md` states, one fact setting one flag; or the Flags line says none was found, or, where this run read no source beyond the existing file, that none was read. A flag stopped nothing in this skill, and the requester was told each one in force. No flag outlived the line it rested on.
- No personal-life fact remains, and no assessment rests on one. A prior line of that kind was dropped even with a source, a register, and a date. Open gaps names the removal and does not repeat it.
- A role statement, a former role, and a sighting stay apart. `Still publishes: yes` is dated publication evidence, never a listing. A departure or a former role is superseded only as Currency states. Each currency field has its own source and as-of date. An unresolved field is not current. A current outlet has its lines. Any other outlet appears only in Role. `Staleness` records `30 days, default` or the requester's number.
- Prior facts remain, except a dropped personal-life line, an unsourced claim, or a work line outside the ten latest. A superseded fact is marked, not deleted. The same line was not added twice. A different value was not dropped as a duplicate. The same evidence twice left the file unchanged.
- A drop or a replace was copied first where Archives in `standards/conventions.md` in `wiser` requires a copy. Adds and supersessions alone were not. Where the copy still holds removed personal-life material, the requester was told its path and that it holds that material. A file of this journalist's found only at the write was read and the draft rebuilt before anything was written.
- The home was the one named directory, the person's choice, the accepted offer, or the found program's reporter directory, with nothing created beside that program. Or the skill asked and did not write.
- `experts/Research Expert/` in `wiser` ran in a second context before any write, handed what What did the gate return? states, with browser and database reads in the eight fields. A carried non-figure gained no `Label`. One correction pass. Rely writes. Weak points on figures, labeled in Open gaps, write. After the second verdict, findings closed without adding a claim (shape fixed from what the line shows, value narrowed to its excerpt, a gap named, or the line dropped) write, each told to the requester. A held finding about the whole draft, such as the wrong person, is reported, and the file stays unwritten. Set-aside findings were told, with why. A matching draft was left unchanged.
- No pitch was written, no journalist was chosen, no pitch was judged, no sign-in was entered, and nothing was sent.
