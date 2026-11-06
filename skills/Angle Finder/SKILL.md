---
name: Angle Finder
type: skill
category: media-relations
description: A ranked menu of the stories readers on a beat are following and what the sender adds, with coverage, open questions, proof and check results, or one checked story angle when asked.
version: 0.2.0
gaps:
  - "earned-media strategy beyond ranking stories: a decision to pursue one, an outreach route and a pitch schedule"
  - crisis judgment on a pitch during an unfolding incident
  - a news-value read of a stunt, a mascot, a visual or a playful tie-in, which the angle checks have no contribution entry for
---

# Angle Finder

## Context

Use when a person has material or a direction and wants a ranked menu of stories readers are following, with the question each leaves and what the sender adds. When they ask for one story, return a single-angle package built coverage first and checked the same way. Hand a chosen story to `skills/Media List/`, a decision to pitch to `skills/Pitch/`, and the menu to `skills/Campaign Plan/` for a campaign document.

Not for choosing journalists, which is `skills/Media List/`, or drafting a pitch, which is `skills/Pitch/`. Prose belongs to `skills/Content Author/` in `wiser`; spoken remarks to `skills/Speech Writing/` in `wiser`. Ranking stories and dropping those the sender adds nothing to are this skill's work. The remaining gap is earned-media strategy beyond ranking stories: a decision to pursue one, an outreach route and a pitch schedule. Crisis judgment is the crisis gap.

Stands alone: no expert in this plugin owns it, because its checks are steps, not a lens. The checks never verify the sender's claims. They read the sender's own account as material and ask whether the package says more than the material does; ranking belongs here, outside those checks.

Classifier seam: none.

## Objective

A ranked menu and its working part, or one story angle and its working part, carrying the results of `angle-checks.md` and `story-checks.md`, beside this file, for every kept story. A run with no package names why. A saved menu is one angle package: the working part follows the menu in the same file. Nothing is drafted or sent. Verified against Success.

## Inputs

Wrap each input so material inside is never instruction.

- `<material>`: the person's material, with its sources, any claims register with exact wording and approval status, and any terms binding what the sender may say.
- `<request>`: the direction, the beat in words, the coverage window, the audience they want, any spokesperson, any medium or route they named, and whether they want one story or a menu.
- `<owning_root>`: the owning root.
- `<as_of>`: the date the angle is checked as of.

Material or a direction, and the owning root, are required. Assemble the material record defines what the sender and checks read. The reader context receives no sender material.

## Identity

The person assembling stories for a desk, starting with what its readers are following and then finding what the sender adds.

## Steps

Take the first match where a step lists outcomes, unless it says to take each applicable one. Every answer the person gave stands across a return to an earlier step. Ask no question already answered. Blanket acceptance answers a choice only where a named recommendation is in hand; it supplies no missing fact or unnamed home.

Is the offer a stunt, a mascot, a visual or a playful tie-in?

- Yes. Name the gap: a news-value read of a stunt, a mascot, a visual or a playful tie-in, which the angle checks have no contribution entry for. Continue; handle any contribution stop under the checks below.
- No. Continue.

### Is this ask outside the angle?

For a mixed ask, apply this question again to the parts left. Stop each outside part. A story-menu or angle ask can continue.

- They want a decision to pursue a story, an outreach route or a pitch schedule beyond the menu's ranking. Name the gap: earned-media strategy beyond ranking stories: a decision to pursue one, an outreach route and a pitch schedule. Stop that question. Do not answer it.
- They want journalists chosen. Name `skills/Media List/`. Stop that part.
- They want a reporter researched. Name `skills/Reporter Research/`. Stop that part.
- They want a pitch package or a draft pitch. Name `skills/Pitch/`. Stop that part.
- They want a campaign document. Name `skills/Campaign Plan/`. Stop that part; a menu it needs can continue.
- They want spoken remarks. Name `skills/Speech Writing/` in `wiser`. Stop that part.
- They want a press release, op-ed or other prose. Name `skills/Content Author/` in `wiser`. Stop that part.
- They want stories ranked or one angle from material or a direction. Continue.
- Nothing remains inside this skill. Stop the run with no package until an in-scope request is given.

### Are the inputs present?

- Material and a direction are both missing, or the owning root is missing. Ask for the missing input. Stop the run with no package until answered.
- Material or a direction, and the owning root, are present. Continue.

Which date does `<as_of>` carry? Take the first match.

- None set. Use the date of this run as `YYYY-MM-DD`.
- One absolute date, or a relative date that resolves to one. Use the absolute date as `YYYY-MM-DD`.
- A value that cannot resolve to one absolute date. Ask for the as-of date. Stop the run with no package until answered.

Are the beat and window settled?

- The request names a beat in words and a window resolving to inclusive `YYYY-MM-DD` start and end dates, ending no later than the as-of date. Carry them. Strip the sender's name and its own product names; keep the category and subject in words. No subject remains: ask for the neutral subject and stop the run with no package until answered.
- Either is missing, ambiguous or cannot take that form. Ask for that field. Stop the run with no package until answered. Do not replace an ambiguous beat with the sender's product category.

Which output is requested?

- One story or one angle. Carry that scope through both contexts; do not force it into a menu.
- Otherwise. Build the ranked menu.

### Does this stop for crisis?

- The request or material shows an unfolding incident involving the sender. Name the gap: crisis judgment on a pitch during an unfolding incident. Stop the whole run, per Behavioral Core in `wiser`. No package.
- No such incident is shown. Continue to assembly.

For the rest of the run, the parent reads every pull, every research return and every opened page in full for an unfolding incident involving the sender, before any date or sender filter removes anything and before using the return. One found takes the same full-run stop in place, with no package and the gap named. Keep excluded originals in the parent's material record. Never return to this step or re-enter assembly from later in the run. Story-specific tragedy withholding happens in the sender context below.

### Assemble the material record

Keep the supplied material, the direction and every factual statement from `<request>`, labelled as the person's account, with their sources, as one material record. Give entries stable references such as M1. Keep the claims register's exact wording and approval status with row references such as C1, and the terms in full. No register or approval rule supplied: record that absence, never invent an approval requirement or an approved status. The sender's recorded words in any setting count as material for any story they answer.

The parent sender context adds the reader context's output unchanged and any concept package or research returned, with its sources, dates, hedges and evidence labels. Keep sender material distinct from coverage and reader findings so the check inputs below can select them separately. Carry a recorded sourcing register beside every quote or fact about a person, with its source, per Sourcing Registers in `wiser/standards/conventions.md`. If one would enter the presented package without its source or register, ask once for what is missing. Not supplied: leave that quote or fact out of the package.

### 1. Prepare the reader context, in the parent sender context

#### What coverage is handed over?

Read declarations only: the owning root's `AGENTS.md` and every `AGENTS.md` under its declared work directories. Find the directories declared to hold reporter files. Exclude `sources/`, `memory/`, archives and programs for another concern, and everything under them.

- One or more reporter-file directories. Load `tools/beat-coverage/TOOL.md`. Run its `pull` on each directory for the settled window, using the coverage-destination match below. Use a beat expression only where it expresses the beat's topic terms without the sender's identity; otherwise omit the optional filter. Combine returned items without dropping their file references or precision labels. Carry the tool's counts and any failures. On a tool failure, retry once without `--output`. A successful retry supplies its `markdown` in the session; say it was not written. A second failure supplies no coverage: record `Not available` with both failures' reasons and continue to the dated search with what is in hand.
- None declared. Record `Not available: no declared reporter-file directory` as the coverage input. The dated search below can still run; do not invent reporter files or a tool result.

Where is a tool return kept? Resolve this before each pull. Before counting destinations, exclude reporter-file directories, pitch-package directories, `sources/`, `memory/`, archives, programs declared for another concern and everything under them, as for the package home below.

- One eligible declared active work directory is unambiguous for this task. Create that declared directory first if absent, per Working Files in `wiser/standards/conventions.md`, then pass `--output` for a new coverage input file there. If creation fails, say why and run without `--output`.
- No such destination, or several with none selected. Omit `--output`; carry the returned `markdown` in the session as the coverage input and say it was not written. Do not invent a home. The final package's home is resolved separately below.

Does the coverage input itself name the sender or carry the sender's own published work? Apply this filter in the parent to recorded coverage, every research return and every page opened before handing anything to the reader.

- Yes. Keep the original in the material record; remove sender-identifying wrapper text and exclude the sender's own work and any item naming or otherwise identifying the sender, its people or its own products. In a research or opened-page return, omit each whole finding or source entry if any of its text, title or URL names or otherwise identifies the sender, its people or its products. Omit any separately returned sender-identifying title or URL in full too. Hand what remains, or nothing from that return. Do not alter a recorded headline to hide the name. Record exclusions for the sender context only.
- No. Keep its text unchanged, subject to the reference handling below.

Keep file references and their root-relative paths in the parent's material record. In the reader copy, replace disk references with neutral item ids and keep their mapping only in the parent. When assigning coverage ids, choose a letter prefix used by no material-record or claims-register reference in this run, comparing without regard to case; use that prefix for recorded and added research items throughout the run. Record the chosen prefix and its separation from those references in the working part. Hand the redacted text itself, never the owning-root or coverage-file path. The parent restores the mapped references alongside the unchanged reader output in the working part.

#### What dated research is handed over?

For one-story mode, use the requested story's neutral subject; for a menu, use the neutral beat. Does the recorded coverage contain no item inside the settled window whose recorded headline or subject carries the handed topic terms?

- Yes. Name that shortage in the dated research request and ask it to fill in on the handed subject.
- No. Ask for beat-wide dated research.

Intersect the seven inclusive days ending on the as-of date with the settled coverage window: start is the later of the window start and as-of minus six days; end is the earlier of the window end and as-of. An empty intersection: run no breaking-news search, hand an empty breaking-thread list and name that date limit. Otherwise run the dated search only over those intersecting dates; this is the breaking-search window below, and "this week" means that window.

Only for a nonempty intersection, the parent runs `skills/External Research/` in `wiser` by name. Hand `<research_request>` a natural-language question asking what broke on the neutral beat or subject in that breaking-search window, naming this story menu or single-angle package as the consumer; `<scope>` the beat or subject, those inclusive dates and the settled coverage window; `<source_material>` the redacted recorded coverage and its supplied sources, never sender material. Take the returned brief with its sources, dates, hedges and evidence labels; do not reproduce its research method.

What did the search return? Only where the intersection is nonempty.

- Readable items. After the parent's unfiltered incident read, keep only items in the breaking-search window, apply the sender filter above, and add the eligible text with its marks and any returned shortage or coverage limit. Open added items used to support a requested story as below.
- No items, a shortage or a search that could not run. Carry the returned limitation with `Not available` and its reason. Use only the recorded coverage that is in hand; claim no knowledge of this week's news that never returned.

To open added items or known recorded coverage URLs, run `skills/External Research/` in `wiser` by name. Hand `<research_request>` a question asking it to fetch each handed URL and return each page's headline and publication date for this story menu or single-angle package; `<scope>` the URL or list of URLs and settled coverage window; `<source_material>` the corresponding recorded items with their sources and marks. The parent reads the whole return, including every opened page, for a sender incident before applying the sender filter to it. Apply the page-match rule below separately to each item.

Did the return show that the item's own page was opened, with that page's returned headline and publication date matching the recorded item?

- Yes. Mark **opened YYYY-MM-DD**, using the date opened.
- Any other return, including a snippet, summary, missing or mismatched headline or date, or an opening that failed or could not run. Keep **unverified**; no fact is established by an unopened page.

A roundup, newsletter or search summary stays unverified until its own page is opened; opening it does not open the articles it mentions. Carry those marks, the breaking-search dates or empty-window limit, and the filtered research text inside the redacted coverage input.

#### Hand off to the reader

Open a second context that has not seen the sender's identity or material. Hand only four wrapped inputs: the neutral beat or subject in words, settled window, as-of date and redacted coverage text. Select one scope instruction: one-story mode, return only the handed subject's story and threads; menu mode, return broad stories on the handed beat. Hand that sentence and only the instructions from What are readers following? through its return below. Never hand the preparation instructions, sender's name, material, requested position, claims register, terms or disk paths. A requested angle is represented only by its neutral subject. On a host with one context, a new chat given only this allowed handoff is the second context, per Behavioral Core in `wiser`. Only when no such context or chat can be opened for the reader handoff, stop the whole run with no package and name the missing reader context; do not simulate blindness in the sender context.

#### What are readers following?

Read every handed coverage item and keep its neutral reference, precision and unverified or opened mark. Use only this text; do not open the owning root, any coverage file on disk or any other source. The coverage input includes the filtered dated research and its breaking-search window; "this week" below means that window. An empty window leaves the breaking-thread list empty.

Group the coverage into broad stories: one thing readers would tell a friend is happening, broad enough to hold related threads. Name each in plain reader words about what is happening, never a category label. For a menu, return every supported story up to ten; fewer than six, including none: name the shortage and never pad. For one-story mode, return only the requested story and its threads, or name the shortage if none is supported.

For each thread, take the first match.

- It belongs to a story. Put it there, one line per thread.
- It fits none, and at least one of its own recorded items supports a distinct statement of what is happening. Make it a story, within the requested scope and story limit.
- It broke in the handed breaking-search window. Keep it on the breaking-thread list even if small; carry its date and any dated window or deadline to ranking, with its source. An unstated window stays `not stated`.
- Otherwise. Leave it among the ungrouped items.

Also list every thread that broke this week, including ones already grouped, with its date, source, parent story if any and any window. This list goes to ranking; small timely threads are never lost to the story-count target.

Under each story retain its threads and all its items: reporter, outlet, publication date at its recorded precision, headline as recorded, URL and reporter-file reference where supplied, and unverified or opened mark. Missing metadata stays `not stated`. Put an item in at most one story. Count only those items: item count, distinct outlet count, newest dated item and whether this week's news reopens it. Say the counts are of recorded items, flag duplicate recordings, and do not treat them as independent corroboration. A partial date supplies no precise breaking date.

What does a reader want to know next? For each story and ungrouped breaking thread, write up to three distinct questions the coverage raises but does not answer, the strongest first, in a reader's own voice. Where a story has more than one thread, spread the questions across its threads rather than taking all from one. Spread them across kinds too: what is actually happening and whether anyone could tell; who answers for it; and what a reader in this beat's audience would do next. At least one widens beyond the named actors to what a reader's own organization would want to know or do. Use only the handed coverage and keep every question one it raises and does not answer. Write each question directly. Where a sentence claims an absence, say what the coverage in hand does not say. Never claim nobody has answered, nobody is asking, no one knows, or that a question is still open across the whole field.

Return the stories with names, threads, items, counts and open questions; the breaking-thread list; then the ungrouped items and coverage limitations. The return must arrive whole: where the host lets the reader context write a file, it writes the whole return to one new file in the session's scratch area, outside the owning root, and hands back only its path, which the parent reads whole; otherwise it returns the text. A return that arrives marked truncated or cut short is incomplete: the parent opens a new reader context once with the same handoff; still incomplete, it uses the return with the gap named in the working part and never fills it. If no story or breaking thread is supported, return that shortage to the parent sender context; it still considers an evergreen offer. The parent adds this output unchanged to the material record.

### 2. The sender context

Run here, on the reader context's output unchanged, the material record, the claims register or its recorded absence, and the terms. Do not send the sender's material back to reshape the reader context's findings.

Does a returned story's own name or any of its coverage make it a tragedy or hook it to one? The parent reads each story's name and all its coverage, and each ungrouped breaking-thread candidate, before continuing here.

- Yes. Withhold that story or candidate only, naming the crisis-judgment gap and the reason with its drop. Keep the reader output unchanged in the record. Continue here with the other candidates, without returning to the crisis step, assembly or the reader. Apply this same withholding in place if later material or a check result names that gap for a story.
- No. Carry it to the sender's contribution steps below.

The reader returned no story or breaking thread: carry its shortage here. Consider a story-less evergreen candidate from the material's offer and the question it answers, marked `No coverage found in the window`. In one-story mode it must answer the requested subject's question; do not substitute another story. It goes through contribution, ranking, honesty and both check files in the same way, with no invented story or coverage.

#### Who is the audience, and who speaks?

For each of audience, spokesperson and what they can speak to, and medium or route, take the first match.

- The material record states this field. Carry it with its source. A route named by the person is recorded, not selected here.
- It does not state this field. Write `not stated`. Do not infer an audience, a role or authority.

#### Is the concept settled?

Does the material record hold an eligible contribution in `angle-checks.md`'s Contribution terms, applying Build the angle record's eligibility rule and the clean-pairing test in What does the sender add? In one-story mode test all the requested story's questions, across its threads. For a menu test whether at least one whole story or ungrouped breaking thread carried to ranking has such a contribution. With no coverage, test the story-less evergreen candidate's question and offer.

- Yes. Continue without Build Concepts. Developing an already usable take further is not this call's work.
- No. Run `skills/Build Concepts/` in `wiser` by name. Hand `<source_material>` the material record and `<user_request>` its direction and constraints, naming the owning root and the audience above as the reader. For `not stated`, name the intended reader as "unstated". The audience field stays `not stated`; a reader Build Concepts names never fills it. Take its package as returned. Do not reproduce its extraction method.

What did that call return? Only where it ran.

- A concept package in one-story mode with no eligible offer answering any of the requested story's questions cleanly, or its material-held service question where no coverage exists. Name that mismatch and take Rank and drop's none-kept path, returning the reader findings, drops and reasons as a named stop with no angle package.
- A concept package otherwise. Add it with its core insight, sources and sourced or constructed markings. With no coverage, form a story-less evergreen candidate from its eligible offer and question; in one-story mode keep only an offer answering one of the requested story's questions cleanly, or its material-held service question where no coverage exists. Continue.
- Nothing to teach, no package, or a call stopped for a missing reader. Say so plainly and report its reason. Take Rank and drop's none-kept path, returning the reader findings, drops and reasons with no angle package.

#### What does the sender add?

Before ranking, test every question of every story carried to ranking, across all its threads, and every ungrouped breaking thread's questions, against every argument and fact the material holds. Also test any person, data, example or access offered, and any story-less evergreen candidate's material-held question. Pair each argument or fact with the question it answers cleanly: it resolves the question as asked, and the sender is not the party whose claim or product the question doubts. Use only the reader context's questions where coverage exists; do not invent or reshape one to fit the sender. Choose the strongest clean pairing for each candidate. Record the tested pairings and their reasons in the working part, citing material-record ids or claims-register rows there, including each rejected pairing that casts the sender as the doubted party. Do not use that pairing; where the same argument answers another story's question cleanly, put it there. Apply this clean-pairing test to new contributions and reworks too.

Where does an argument come from?

- The material shows the spokesperson holding it, and it answers the question cleanly. Apply it: write it in one sentence as their argument, then the question it answers. Applying that argument to this story is the pitch angle, never a fact about the story or a quotation they did not say.
- The person's account holds it and it answers the question cleanly, but the spokesperson is not shown holding it. Say it is a position to put to the spokesperson, not yet theirs.
- Neither. Do not attribute it to them. Write `nothing in the material` or `touches the topic only` where nothing answers the story's questions, even as an argument.

Each entry is a whole story the reader returned, with that story's following and name, even when the chosen question comes from just one of its threads. A grouped thread, including one on the breaking-thread list, never becomes a separate entry. Only an ungrouped breaking thread or a story-less evergreen may stand without a parent story. The same material may serve several stories; reuse is never a reason to drop one. The sender's own published material is proof for this step, never coverage. If a missed sender item is discovered here, leave the reader output unchanged and record the exclusion in a separate sender-side note in the same material record; exclude the item from the kept story's coverage and adjust its following count before ranking. Otherwise carry the coverage as returned.

For every spokesperson line, what tension makes it worth quoting?

- A reader could dispute its answer, mechanism or consequence. Carry the line and the question it answers.
- Nobody would disagree with it. Flag that in one short sentence beside the line. Reframe around the buyer's question the news raises, in one short sentence there too. Propose an answer the material supports that someone could argue with; where none is held, record the answer needed as a question for the sender, never as their position.
- No spokesperson line is offered. Record that; judge the fact, person, data, example or access offered on its own.

Which name-check outcome applies to each candidate?

- A story-less evergreen. Carry it to Rank and drop with `No coverage found in the window` and no name-check failure; continue the sender-claim check below.
- The story's name holds against its actual coverage. Keep it.
- The name does not hold, but the coverage supports a narrower or different name and frame for the whole story. Record the overreach, the original name and the proposed name and frame in the working part, keeping the original reader output unchanged. Use the proposed name in field 7 for checking and as the entry's heading; the menu shows the name-check result only through that heading, never the name-check working. Do not turn one thread into the entry. Where vendors each define a category as what they sell, test the frame of what the thing is and how a buyer would judge a good one, rather than claiming everyone is in it.
- No supported story can be named. Carry that failure to Rank and drop; invent no coverage to rescue it.

Does a sender claim undercut this story's own argument?

- Yes. Beside the argument, flag the claim and explain the clash in one short sentence in plain words, keeping its approval status in the text. Put its source or row in that field's sources list. Do not silently use it as proof.
- No. Carry the proof as held.

For a competitor's deal, speak to the buyer's question in a frame that outlasts the deal. Do not turn the sender into a commentator on the other companies' products or customers.

#### Rank and drop

Rank all supported whole stories, ungrouped breaking-thread candidates and story-less evergreen candidates by three things together: following, using the reader context's counts; the fit and distinctiveness of the sender's clean answer to a question from any of the story's threads, by fact, data, example or argument; and timing, using newest items, this week's threads and any dated event ahead. Record the evidence and a short judgment for each factor, and explain the order where factors pull differently. An ungrouped breaking thread is weighed even when its item count is small; a grouped one strengthens its whole story's timing. An evergreen without coverage records no following or news timing; that shortage alone does not drop a usable offer.

What stays?

- No supported story or material-held evergreen offer, or nothing distinctive the sender holds, argument included, answers any of its questions cleanly. Drop it with the reason, however big it is. A story whose only pairing casts the sender as the doubted party has no fit. Sharing the sender's product category is not distinctive.
- An answer fits cleanly, with a claim not yet approved. Keep it; put the claim on the approvals list, not among the drops.
- Otherwise an answer fits cleanly. Keep it.

None kept: return the reader findings, drops and reasons as a named stop, with no angle package. One-story mode returns that story's package or its named stop, never a substitute story chosen silently.

#### Why is the spokesperson worth quoting here?

For each kept story, build the credibility bridge: their record, analyst recognition, customers or data, each with its recorded source and sourcing register where applicable.

- No spokesperson is offered. Record `not offered`; no bridge is invented.
- The material record sources the credential, or a claims-register row does. Carry that source and add the row and its status where one exists. A row is not required for a sourced role, field or work.
- Neither the material nor a row sources it. Write a question for the sender, `Can we say ...? Source needed`, never a credential stated as fact.

#### What does the why-now hold?

For each kept story, take each form the material holds, as `angle-checks.md`'s The why-now names it.

- Hard news. State the news, with its source.
- A borrowed hook. Name it with its source and date. A source or date missing from the material goes to `skills/External Research/` in `wiser` by name. Hand `<research_request>` a natural-language question checking that hook's source or date, naming this angle package as the consumer; `<scope>` the hook and as-of date; `<source_material>` the relevant material and supplied sources. Take the returned brief with its sources, dates, hedges and evidence labels. Match the return below; never replace the named hook.
- An evergreen offer. Name the form the material holds. Name the kind of desk only where the material, request or form names one, as a product review names a review desk. Otherwise the desk is `not stated`.
- None of those forms is held. Say `None found`, including where research returned no hook or could not run. An unsuccessful lookup never removes an evergreen or hard-news form.

What did the hook lookup return? Only where it ran.

- A source or date for the named hook that fills an unstated field without conflicting with the material. Add it to the material record and that field's sources list, keeping its hedge and labels in the text too.
- A conflicting source or date, or a different hook. Keep the material's hook and values; record the conflict beside them. An unresolved field remains `not stated`.
- Nothing returned, or research could not run. Keep the field `not stated` and carry `Not available` with the reason.

#### Open what the menu will show

After Rank and drop and before the honesty checks, select the three to seven items each kept entry will show from its whole story's coverage, or its ungrouped breaking thread's coverage; fewer held, keep fewer and say so. For each entry with recorded URLs, the parent makes one External Research URL handoff as defined above, handing that entry's full list of recorded URLs for the selected items in one call. Open those items, except any this run already opened with a page match, which keep their marks, and apply the existing page-match rule to each return: `opened YYYY-MM-DD` only on a matching headline and publication date from the item's own page; otherwise `unverified`. An item with no recorded URL stays `unverified` and goes on the task list by outlet and headline. A story-less evergreen has no coverage to open.

Read the whole return and every opened page for a sender incident before filtering or using any of it. Then apply the existing sender filter. Keep originals, exclusions and mark changes beside the unchanged reader output in the working part; update the selected items and following evidence without filling a vacancy with an unopened replacement. Reapply the name and clean-pairing tests in place to the remaining coverage. If the exclusions leave no supported story or clean pairing, apply Rank and drop's drop outcome in place. Failed openings remain unverified and go on the task list; they alone do not drop a story. Carry these final marks into each item's field text and sources before the honesty checks and both check files.

#### Run the honesty checks last

Assemble a provisional menu and working part in the output shape below, or the single-angle equivalent. On the whole, take each applicable outcome, fix the failure, and record what was fixed.

- Coverage differs from the reader record after its explicit sender-side exclusions and recorded opening updates, an unverified item is stated as fact, or a working count does not say what it counts. Restore that eligible coverage without reinstating excluded sender material, attribute the unread item as unread in the text, or specify the adjusted count and its method in the working part only.
- A spokesperson's material does not support the offered line's application to this question. The material shows them holding an argument that answers this question cleanly: rewrite the line as that argument with its true attribution. It does not: return that story to Rank and drop.
- This week's news carries many voices on the same point. Say so.
- A sender claim is not approved under the material's approval rule. Write it as proposed, `after approval`, naming who approves in plain words; never drop the story for that absence.
- A coverage claim says nobody, no one or still open. Say what the coverage in hand does not say, in `story-checks.md`'s own change words; do not keep a claim that nobody has answered, even bounded to this coverage. An every claim without a basis: narrow it to the outlets actually held.
- The same question-and-answer wording appears in several stories. Keep each story's chosen reader question and write its own application of the answer; never invent a question or drop a story for reuse of material.
- None of these. Keep the provisional output.

### 3. The checks, per kept story

#### Build the angle record

Build one record per kept whole story, ungrouped breaking thread or story-less evergreen from the provisional menu text after the honesty fixes. Each of its eight fields has **Text**, in plain words a pitcher could use, and its own **Sources** list. Copy the text that will be shown, without source references embedded in it. In that field's sources list keep the material-record ids, claims-register rows, coverage ids, record keys, sourcing registers and provenance notes that resolve each statement; retain the supplied sources, URLs, hedges and evidence labels there too. Coverage and reader provenance belong in fields 7 and 8's sources lists, except the individual why-now items cited in field 3; fields 1 to 6's sources otherwise come from sender material and contribution sources, never reader findings. An empty text is `not stated`; a field with no recorded sources says so in its sources list, never inventing one. The working part carries text and sources together for every field.

The text itself keeps every shown item's opened or unverified mark, all applicable hedges and evidence labels, `after approval` with who approves in words, and a position not yet the spokesperson's explicitly said to be so. Each tension flag, proposed line reframe and claim that undercuts an argument stays in one short sentence beside the line it concerns. The text never contains material-record ids, claims-register rows, coverage ids, record keys, thread or story numbers from the reader output, "per the reader context", count-method notes or the name check's working. The name check's result appears only as the entry's name; where a proposed narrower name replaces a failed one, field 7 uses that proposed name and its sources list records both names; the name-check reason stays in the working part outside the check handoff.

The menu's heading is the entry's rank number and the checked name in field 7, never field 1; a story-less evergreen uses the plain offer description from checked field 1, marked `Story-less evergreen`. Map the eight fields as follows, keeping text within these bounds before checking:

1. **Headline angle:** one sentence saying what the sender adds, first in **What we add**.
2. **Contribution:** the argument or fact in at most two sentences, then its proof in at most two sentences, in `angle-checks.md`'s Contribution terms. Each flag or reframe is one short sentence beside its line, in addition to those limits. This follows field 1 in **What we add**.
3. **Why-now:** **Why here**, at most two sentences naming the hook with its date and opened or unverified mark, or the evergreen form or `None found` as held. A hook with no recorded matching page opening stays unverified; a missing date stays `not stated`. Keep its source in this field's sources list.
4. **Audience:** the stated audience, labelled **Audience**.
5. **Spokesperson and scope:** any spokesperson offered and what they can speak to, with that label.
6. **Medium or route:** any medium or route the person named, with that label.
7. **Story readers are following:** the story's name, which heads the entry and is not repeated beneath it, then **What readers are following**, one line saying what is happening, then the exact three to seven selected item records, each with reporter, outlet, date, recorded headline and opened or unverified mark. Fewer held: show fewer and say so, never pad. An unread item's claim is attributed as unread. The whole story's name heads the entry even if field 8 comes from only one thread. An ungrouped breaking thread is marked `Breaking thread`, with its date and window; an unstated window stays `not stated`. A story-less evergreen says `No coverage found in the window`. All remaining coverage stays in the working part.
8. **Open question:** **The open question**, one question in the reader's voice that the sender answers cleanly.

Run the checks on each field's text and sources together. Present exactly the checked fields' text, without their sources lists, subject only to the rerun outcome's final local removals or narrowings. Where field 4, 5 or 6 has identical checked text in every presented entry, show that field's exact checked text once in the menu header with its label, omitting it from the entries. Test each of those fields separately; keep its text and sources in every entry's working record even when the menu shows the text once.

The headline angle states what the sender adds to the story's question: the spokesperson's recorded line applied as their argument, or the sender's fact. It never restates the news as the offer; the news belongs in field 7, which angle checks do not receive. For a story-less evergreen, field 1 is a plain description of its offer and field 7 is `No coverage found in the window`; state its material-held service question in field 8.

Keep the as-of date with the record. A stunt-shaped offer stays named as such, with its material and source and any contribution the material also holds. Eligibility rule: a specific Build Concepts marked constructed stays only in the session material record with its marking. It never counts as a contribution or enters an angle field, headline, presented package or claim handed on. Apply this rule to every concept return and rework.

#### What did the checks return?

For each story, run `angle-checks.md` unchanged in a second context that did not build it, then `story-checks.md` in another second context, per Behavioral Core in `wiser`. On a host with one context, a new chat given only the allowed handoff is each check's second context. If no such context or chat can be opened for a check, leave that check uncompleted, name the missing context and omit that story from the presented menu; never run it in the context that built the record. Each available context receives only its own check file and three wrapped inputs, never the other file, its verdict or the reasoning that built the package:

- `<angle>`: the first six fields for angle checks; all eight for story checks, each handed as its text together with its own sources list. The sources are part of that field's input, not a fourth wrapped input. For angle checks, include only sources belonging to fields 1 to 6; do not attach field 7 or 8's sources or reader findings.
- `<material>` for angle checks: the sender's material record with its sources, concept returns and research supporting the sender's contribution. Remove all coverage and reader findings, including coverage from the parent's research, then add back only the individual coverage items the why-now cites, with their marks and sources. Do not hand the reader's story field, other coverage or the whole reader output to angle checks. Retain the sender's claims register and terms or their stated absence with the sender material.
- `<material>` for story checks: the whole material record with its sources, all coverage and the reader output, claims register and terms or their stated absence.
- `<as_of>`: the check date's `YYYY-MM-DD` string.

Take each result as stated. Do not restate or change either check file. Finish both attempts in a check round and classify both returns below before working findings or making final cuts. A withhold or omission from either return governs that story regardless of the other verdict. Never detour back to assembly or the reader step.

What came back? First read each return's opening word only to distinguish exactly lowercase `pass`, `stop` and no completed result; match `pass` and `stop` as whole words, ignoring Markdown emphasis or code marks around the word, such as `**pass**`. A word appearing later does not count as the status; a missing or different opening word is no completed result. Preserve the body, including its why-now line where present, findings and notes. Then read that body for the crisis-judgment gap before using the status. Take the first match for each return.

- The return reveals an unfolding incident involving the sender. Take the full-run stop in place, with no package and the crisis-judgment gap named.
- The body names the crisis-judgment gap, a pass included. State the result, findings and notes as returned and withhold that story in the same way as in the sender context, before any take-on choice. Other stories continue; return to no earlier step.
- No completed result. Say which check did not complete and why, naming a missing context where applicable; omit that story from the presented menu and substitute no verdict.
- `pass`. Carry the result and notes into the package.
- An initial `stop`. Queue its findings for the finding match below, together with the other file's initial stops. Work them only after both returns are classified and the story is neither withheld nor omitted.
- A `stop` from the rerun. Keep the findings as returned. Is every held finding across both files small and local, cured solely by removing or narrowing its named text without widening a claim, adding an unsupported one or losing an obligation? Yes: make only those removals or narrowings in the menu and its angle record, record them beside the unchanged results and deliver without another check. No: put the remaining findings to the person as written and record their choices with the findings, without changing the angle or running the checks again. A retained stop stays a stop.

Budget: each story has one combined rework covering all initial stops from both files and their research returns, then one rerun of each file. Apart from the final local removals or narrowings in the rerun outcome above, a remaining stop or a new finding permits no further rework or check run.

For each initial finding, take the first match. Keep its evidence and every choice it carries. A chosen change joins the combined package; taking a finding on without an edit is available only where its own outcomes offer it, and retains its stop. Sourced, attribution and claims approval take their specific changes, never take-on as a substitute.

- **Missing input.** Get the missing record from what is in hand, never an invented value. Not in hand: leave that check uncompleted, name the missing input and omit that story from the presented menu.
- **Contribution, and the offer is a stunt, a mascot, a visual or a playful tie-in.** Put the finding to the person as written. Offer the choice to take the angle on as it is or supply a new contribution. They take it on: record that with the finding. They supply a new contribution: include it as one change in the combined package. They decline: withhold that angle and say why; other stories continue.
- **Other contribution.** Go to the material for what is new to a desk first. A contribution there: use it. None, and the finding says the main offer was already done or reported: ask the person, never Build Concepts. None for any other contribution stop: run `skills/Build Concepts/` in `wiser` once for this rework, with the inputs from Is the concept settled?, but match the return here, never its initial-call stop. A usable eligible contribution answering this candidate's question cleanly, one of the requested story's questions or its no-coverage service question in one-story mode, returned: use it. Nothing to teach, an empty, unrelated or unusable return: put the finding to the person as written and leave that angle. A contribution the person supplies joins the combined changes; otherwise the finding and angle stay.
- **Authority.** The material shows another person whose role, field or work is on the topic: offer that person. It shows none: ask the person. They supply one: offer that person. They have none: drop the spokesperson and keep the angle, saying so.
- **Crowded moment.** Put the finding to the person as written.
- **Sourced.** The material holds the source: supply it. Otherwise the finding is a hook's source or date: run `skills/External Research/` in `wiser`, handed as What does the why-now hold? says. Any other fact: ask the person; they supply it, use it; they cannot, drop it.
- **Attribution.** Take the finding's own change: supply a held coverage item or drop it; mark an unopened item as unread or open it through the External Research URL handoff above and record the page match; say what the coverage in hand does not say; or write an unheld argument as a position to put to the spokesperson or drop it. Narrow an every claim without a basis to the outlets actually held. Only the person can supply a missing statement of their position; do not invent it.
- **Claims approval.** Write the claim as proposed, `after approval`, naming who approves in plain words, or drop it as the finding says. This corrects wording; it adds no approval hold.

For a story still eligible after an initial stop and its finding match, make the combined changes in the provisional menu and rebuild the record from that exact text, with each field's sources list kept beside it. Add every supplied fact, source or contribution to the material record before rerunning, labelled as the person's account. Rerun the files in the same order and separate contexts with their own inputs, then match their returns above. If a missing input prevents a rerun, leave that check uncompleted, name the input and omit the story.

This skill adds no hold, wait or condition outside the checks; notes and contested choices stand as the checks word them. Results retained after the final run keep their original verdict, with any final local removals or narrowings recorded beside them. Every other substantive presentation edit belongs in the combined rework.

### 4. The output

#### What does the package hold?

Default: a ranked menu short enough to read in five minutes, about three pages, then its working part. The bound is the menu; the working part stays whole. Header: as-of date, beat, window and what was read in one sentence, followed by the exact checked text of any common Audience, Spokesperson and scope, or Medium or route field as defined above. Each kept whole story, ungrouped breaking thread or story-less evergreen is its own entry in rank order, never one thread of a returned story. Head it by its rank number and the checked field 7 name, using the proposed name where the reader's original name failed; never by the headline angle. A story-less evergreen is headed by its plain offer description from checked field 1, marked `Story-less evergreen`.

Use the four parts below. Present only each field's checked text, with its honesty marks and beside-the-line flags, without its sources list or working notes. Keep the lengths and exact field mapping from Build the angle record; do not rewrite after checking except for the rerun outcome's permitted final local removals or narrowings.

- **What readers are following:** field 7, one line saying what is happening, then three to seven items, each with reporter, outlet, date, recorded headline and opened or unverified mark. Fewer held: show fewer and say so, never pad. Carry the breaking-thread or story-less evergreen marking where applicable.
- **The open question:** field 8, one question the sender answers cleanly, in the reader's voice.
- **What we add:** field 1's headline angle in one sentence, then field 2's argument or fact in at most two sentences and proof in at most two sentences. Keep `after approval` with who approves in words and any position not yet the spokesperson's said to be so. Keep each tension flag, proposed line reframe and undercutting claim in one short sentence beside its line. Follow with checked fields 4, 5 and 6, labelled **Audience**, **Spokesperson and scope**, and **Medium or route**, except those already shown once in the header.
- **Why here:** field 3, at most two sentences with the hook's date and opened or unverified mark, or the held evergreen form or `None found`. The rank is the entry's position; its supporting judgment and evidence stay in the working part.

Then **Dropped**, one line per dropped story by its reader name, with the reason in plain words, including stories big enough a reader would ask why they are missing. For a dropped ungrouped thread use its reader name; for a story-less evergreen use its plain offer description. No ids or working notes enter these lines. Then **Before any of this is pitched:** items still to open, claims to approve where required, and questions for the sender. Name each item to open by outlet and headline, including each shown item with no recorded URL. This task list may name a claim in plain words with its claims-register row beside it, so the person can approve the right claim; name who approves. This heading is a task list, never a new hold on pitching.

The **Working part**, after the menu in the same package, carries the full reader output; every story's ranking factors and evidence, counts and their method notes; every tested clean or rejected pairing and its reason, including those that cast the sender as the doubted party; every drop and reason, including withheld tragedy hooks; each credibility bridge in full; each name check, with both original and proposed names where it failed; the selected coverage and opening results, exclusions and mark changes; honesty-check results and fixes; and each kept entry's eight-field angle record with each field's text and its own sources list together, why-now forms, both check files' results, findings and notes as returned, rework and choices with evidence. Keep the eligible material record and source references with it so a later reader can resolve every material, claims-register and neutral coverage reference and record key, following the eligibility rule above. Record the coverage prefix and why it cannot collide with the material or claims references in this run. The written working part omits constructed specifics, including any embedded in concept returns or material-record excerpts; those stay only in the session record, never in the angle file. Carry Build Concepts' core insight where returned. Name each unknown with what would settle it and each applicable gap. An angle taken on with an open finding keeps its stop, never a pass. An uncompleted check or crisis gap leaves that story out of the presented menu and names why in the working part; no checked stories remain: return a named stop, not a package.

One story requested: title the package with the same checked field 7 name, using the proposed name where the reader's original name failed, or the marked checked field 1 offer description for a story-less evergreen. Present the same four parts using only checked field text, with its as-of date, then the same working part with the eight fields' text and sources, results, why-now forms, notes, unknowns, gaps and choices. No ranking against stories not considered is claimed.

Name `skills/Media List/` for a story chosen from the menu, handed `<angle>` with headline, audience, contribution and any medium, and `<owning_root>`. Name `skills/Pitch/` for when the person decides to pitch, with the checked story and its sources ready for `<story>`; Pitch needs a journalist chosen separately. Name `skills/Campaign Plan/` for a campaign document from this menu. Nothing is drafted or sent. A run stopped before a package names the stop instead.

#### What one menu entry looks like (made-up, format only)

The common fields below appear in this made-up menu's header; each entry's working record still carries them.

> As of 2026-04-10; home batteries; window 2026-03-12 to 2026-04-10; recorded coverage and dated research read.
>
> **Audience:** Prospective home-battery buyers.
>
> **Spokesperson and scope:** The research director, on tariff assumptions in savings claims.
>
> **Medium or route:** not stated
>
> ### 2. Buyers are questioning promised home-battery savings
>
> **What readers are following:** Owners report savings far below their quotes, and a regulator is examining how savings are claimed.
>
> - A. Reporter, *Energy Weekly*, 2026-04-03, "My battery saved me $11 a year", unverified
> - B. Reporter, *The Ledger*, 2026-04-07, "Regulator opens inquiry into solar-battery savings claims", opened 2026-04-10
> - C. Reporter, *Grid Notes*, 2026-04-08, "Installers say savings depend on tariffs buyers never see", opened 2026-04-10
>
> **The open question:** What tariff assumptions should I ask an installer to write into a savings quote?
>
> **What we add:** Ask for the assumed tariff in writing before trusting a battery-savings quote. The research director argues that a savings claim is only as good as the tariff it assumes. Proposed after approval by the research lead: our 2025 study of 1,200 installs found savings within 10% of the quote where the tariff was stated, and 40% below it where it was not.
>
> **Why here:** The regulator's inquiry into savings claims, reported 2026-04-07, opened 2026-04-10.

**Working part's copy: the same entry's angle record (made-up).** As of 2026-04-10.

1. **Headline angle**
   - **Text:** Ask for the assumed tariff in writing before trusting a battery-savings quote.
   - **Sources:**
     - M3, recorded interview with the research director, 2026-03-25; Public statement.
     - Provenance: application of their tariff argument to the buyer question, not a quotation.

2. **Contribution**
   - **Text:** The research director argues that a savings claim is only as good as the tariff it assumes. Proposed after approval by the research lead: our 2025 study of 1,200 installs found savings within 10% of the quote where the tariff was stated, and 40% below it where it was not.
   - **Sources:**
     - M3, the recorded interview and Public statement register above, for the argument.
     - M5, the cooperative's 2025 tariff study, and claims-register row C2, pending research-lead approval, for the proposed figures.
     - M1 identifies the sender as an independent energy-research cooperative, not an installer whose quote is being questioned.

3. **Why-now**
   - **Text:** The regulator's inquiry into savings claims, reported 2026-04-07, opened 2026-04-10.
   - **Sources:**
     - K2, B. Reporter, The Ledger, 2026-04-07, "Regulator opens inquiry into solar-battery savings claims"; https://ledger.example/inquiry. Its own page returned the matching headline and publication date, opened 2026-04-10. Borrowed hook.

4. **Audience**
   - **Text:** Prospective home-battery buyers.
   - **Sources:**
     - M1, the supplied request, audience field.

5. **Spokesperson and scope**
   - **Text:** The research director, on tariff assumptions in savings claims.
   - **Sources:**
     - M3, recorded interview, 2026-03-25; Public statement. The interview records the director's role and work on tariff assumptions.

6. **Medium or route**
   - **Text:** not stated
   - **Sources:**
     - None recorded; M1 names no medium or route.

7. **Story readers are following**
   - **Text:** Buyers are questioning promised home-battery savings. Owners report savings far below their quotes, and a regulator is examining how savings are claimed.
     - A. Reporter, *Energy Weekly*, 2026-04-03, "My battery saved me $11 a year", unverified
     - B. Reporter, *The Ledger*, 2026-04-07, "Regulator opens inquiry into solar-battery savings claims", opened 2026-04-10
     - C. Reporter, *Grid Notes*, 2026-04-08, "Installers say savings depend on tariffs buyers never see", opened 2026-04-10
   - **Sources:**
     - K1, A. Reporter, Energy Weekly, 2026-04-03, "My battery saved me $11 a year"; recorded headline and publication_date, no URL recorded, unverified.
     - K2, B. Reporter, The Ledger, 2026-04-07, "Regulator opens inquiry into solar-battery savings claims"; https://ledger.example/inquiry, headline and publication_date matched on the opened page, opened_date 2026-04-10.
     - K3, C. Reporter, Grid Notes, 2026-04-08, "Installers say savings depend on tariffs buyers never see"; https://grid.example/tariffs, headline and publication_date matched on the opened page, opened_date 2026-04-10.
     - Provenance: the blind reader returned this whole story name; the name check held it.
     - ID assignment: coverage prefix K is unused by material references M and claims-register references C in this made-up run.

8. **Open question**
   - **Text:** What tariff assumptions should I ask an installer to write into a savings quote?
   - **Sources:**
     - The blind reader's question on K1, K2 and K3, across the savings and tariff-disclosure threads; its text is unchanged.

### Where is the package written?

Write only a package What does the package hold? presents. A run stopped before a package writes nothing. Before any write, form the package's as-of date as `YYYY-MM-DD` and the topic slug as lowercase words joined by hyphens; where either cannot be made so, ask and write nothing until both are in form, then return to the home match below.

Read declarations only: the owning root's `AGENTS.md`, and every `AGENTS.md` under each work directory it declares. A package home is a directory a declaration says holds angle packages. Exclude reporter-file directories, pitch-package directories, `sources/`, `memory/`, archives, programs declared for another concern and anything under them before counting homes or eligible programs, whatever a declaration says. Never offer a program under an excluded directory. Refuse any write whose path is under one. A program's own folder is not a package home. Treat a program as eligible for the media-relations concern only when its own `AGENTS.md` states that standing concern. If its text does not settle whether that is its concern, ask and wait before counting it. Count homes by directory. Take the first match.

- The person wants it kept in this session. Write nothing; say the package stays in the session.
- More than one package home. Ask which. Write nothing until they name one.
- One package home. Write there, creating the directory if absent, per Working Files in `standards/conventions.md` in `wiser`.
- No home, and one program declares the root's media relations as its concern. Offer `angles/` in it. Show the declaration it adds to that program's `AGENTS.md`, in that file's own form: `angles/` holds angle packages, one per file, named `<YYYY-MM-DD>-<topic slug>.md`. Write nothing until they answer.
- No home, and more than one such program. Ask which. Their answer names the program only: then make the offer above for that program, and wait for its answer. Write nothing until they accept it.
- No home and no such program. Ask which declared directory receives the package, or whether it stays in the session. Write nothing until they answer.

What did the person answer? Apply after the choice among package homes or programs, the no-home question which declared directory, or the angles offer. Take the first match.

- They want the session. Write nothing; say the package stays in the session.
- They name one of the package homes just listed. Write there. Add no declaration.
- They name one of the programs just asked about. Make the angles offer above for that program and wait for its answer; naming the program accepts no declaration or write.
- They accept the angles offer. Open that program's `AGENTS.md`. Identify its existing directory list by section heading and an existing directory key; place only the shown declaration beside that keyed entry, in the list's own form. Change no other declaration or text. No unique list or adjacent entry: show the proposed line and ask where it belongs before writing either the declaration or package; once answered, add it only there. Write in `angles/`.
- They were asked which declared directory because no home or eligible program existed, and name one that may receive angle packages. Write there. Add no declaration.
- They decline or name none. Write nothing. Say the package stays in the session.
- They name anything else, including an undeclared directory or one excluded above. Say why it is not one of the eligible homes and ask again. Write nothing.

Name the new file `<YYYY-MM-DD>-<topic slug>.md`, the date the package's as-of date. If taken, add `-2`, then `-3`, before `.md` until free. Never overwrite or change an existing package. Tell the person the path written, or that nothing was written and why.
The menu or single story and its working part are written in that one angle-package file, the working part after the menu or story. Never write a second working file.

## Pitfalls

- **The request is ambiguous.** Which material or direction, beat, window, story or owning root. Ask before proceeding. Do not guess.
- **A requested angle has no matching recorded item.** Use the parent's filtered dated search within the settled window before considering the sender; the sender's own article or appearance is proof, never substitute coverage.
- **A remaining finding tempts another correction.** Take only the rerun outcome's final local removals or narrowings where its test holds; otherwise keep the finding and the person's choice as returned.

## Success

- A ranked menu with its working part, one story angle with its working part, or a named stop was returned. Nothing was drafted or sent.
- The parent collected coverage, ran dated External Research over the intersection with the settled window or named its limit, filtered out sender items and identifying text, and handed redacted text only. Coverage ids used a letter prefix unused by any material-record or claims-register reference in the run, with that choice recorded. The reader context never received sender identity, material or disk paths and opened no source. A new chat given only the allowed handoff counted as the second context; only when no such reader context or chat could be opened did that absence stop the run with no package.
- The reader read all handed coverage with its marks, grouped whole stories and carried dated threads and windows to ranking. Its up-to-three reader-voiced questions per story spread across threads where there was more than one and across what is happening and whether anyone could tell, who answers for it, and what a reader would do next. At least one widened to what a reader's own organization would ask; all stayed questions the coverage raised and did not answer.
- Before ranking, every candidate story's questions across all threads were tested against every material-held argument and fact. Each kept pairing answered the question as asked and did not cast the sender as the party whose claim or product was doubted. Rejected pairings were recorded; an argument that answered another story cleanly went there, with reuse allowed. A story with only doubted-party pairings had no fit and was dropped. Ranking weighed following, the sender's distinct clean answer and timing; no story was dropped for reused material or an unapproved claim. Recorded words in any setting were eligible; an applied argument remained an argument with its true attribution.
- Every entry was a whole returned story, an ungrouped breaking thread or a story-less evergreen, never one thread of a returned story. A question from any thread could supply a whole story's clean fit; the story kept its whole following and checked name. Every spokesperson line was tested for tension, every story name against its coverage. Tension flags, line reframes and undercutting claims stayed in short sentences beside their lines; a failed name check appeared in the menu only as the proposed checked name, with both names and the working kept in the working part.
- After Rank and drop and before honesty checks, the parent opened every shown item with a recorded URL through one URL-list handoff per entry. Every item kept its page-match-based opened or unverified mark in the text. Missing URLs and unsuccessful openings stayed unverified and were named by outlet and headline on the task list. The parent read every pull, research return and opened page before filtering for sender incidents, which produced no package. It withheld a story whose own name or coverage was a tragedy, or whose check result named the crisis gap, and continued in place without re-entering assembly.
- Every presented field was exactly its checked text without its sources list, subject only to the rerun outcome's permitted final local removals or narrowings. Its working record kept that same text with its own sources list, resolving every statement. Text kept honesty marks, hedges, approval wording naming who approves, and positions not yet the spokesperson's said to be so; ids, record keys, reader story or thread numbers, provenance notes, count-method notes and name-check working stayed out of the entry. Identical Audience, Spokesperson and scope, or Medium or route text appeared once in the menu header. Following was one line plus three to seven items, or fewer held with the shortage named; the open question was one question; What we add led with its one-sentence headline, then at most two sentences of argument or fact and two of proof, with each flag one short sentence; Why here was at most two sentences with the dated hook and mark, or the held evergreen form or `None found`. Dropped was one plain line per story by its reader name; the task list could carry a claim's register row beside its plain wording.
- Each entry's heading and the single-angle package's title used the checked field 7 name, with a proposed name replacing one that failed, never the headline angle; a story-less evergreen used its plain offer description from checked field 1, marked `Story-less evergreen`. What we add showed field 1 followed by field 2; the story field held the news. Both check files received field text and its own sources together, the first six fields for angle checks and all eight for story checks. Angle checks received sender material plus only why-now coverage; story checks received the whole record. Both ran unchanged in separate second contexts or new chats, each with only its own file and three inputs; a missing check context left the check uncompleted and the story out. The opening word separated pass, stop and no result; the body was then tested for the crisis gap. Findings, notes and original verdicts survived; changes followed the shared budget and any final cuts were recorded.
- The evergreen form was named wherever held, including a story-less angle marked `No coverage found in the window`; an unstated desk remained `not stated`. No hook, date, authority, approval status or coverage was invented. No absence of a hook or coverage alone stopped an angle; nothing kept after rank and drop returned the reader findings and a named stop.
- Build Concepts and External Research were composed by name, their returns and labels carried, their methods not reproduced. One-story mode kept a concept offer only when it answered the requested question cleanly. No constructed specific became an angle field, a claim handed on or part of the written working part.
- The package carried its as-of date, results, notes, unknowns, applicable gaps and named handoffs. A saved package was one new file in a declared or accepted angle-package home with the working part after the menu or story; otherwise it stayed in the session and the person was told why.
