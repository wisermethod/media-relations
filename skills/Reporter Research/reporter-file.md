# Reporter file

The contract for the one file Reporter Research writes on one journalist. The Pitch skill and any later checker read this contract. It is the only list of fields.

Dates follow Dates in `standards/conventions.md` in `wiser`: absolute, `YYYY-MM-DD`. A register is one of the four named in Sourcing Registers in that standard, and a figure's label is one of the four named in Evidence Labels there. This contract adds no register and no label.

## File name

The file name is the family name, a hyphen, and the given name, in lower case, then `.md`. A space becomes a hyphen. A character Names in `standards/conventions.md` in `wiser` forbids is dropped. An accented letter becomes the plain ASCII letter. A name given as one word is the whole stem.

The name is the file's name only. The home the skill resolved supplies the directory.

Where that home already holds this file name for a different journalist, the name gains a hyphen and the primary outlet, normalized the same way, and the other file is left in place. Where the family name is not the last word, or the order is unclear, or a collision has no outlet to add, the name is unresolved. No name is guessed.

The file records the name on the `File` line.

## Opening lines

The title is `# Reporter: <name as given>`. These lines follow it, in this order:

```
File: <file name>
Status: <draft or filed>
Staleness: <number> days, <default or requester>
Created: YYYY-MM-DD
Last enriched: YYYY-MM-DD
```

When `Status` is `draft`, these two lines sit between `Status` and `Staleness`, in this order:

```
A pitch should not rely on this file until dated work, the role statement, and the beat are filled.
Missing: <dated work, role statement, beat>
```

`Missing` lists only the absent ones of those three tokens.

`Status` is `draft` when any of dated work, a role statement, or a beat is absent. It is `filed` when all three are present. On `filed`, the warning and `Missing` are absent.

`Created` is the date the file was first written and does not change. `Last enriched` is the as-of date of the run that last changed a fact. A run that changes no fact leaves both dates as they stand.

`Staleness` records the threshold that applied. `default` means 30 days. `requester` means the requester set the number.

Status, last enriched, and work at another outlet are not currency.

## Lines

A fact uses this shape. Optional parts are omitted when they do not apply. The parts that remain stay in this order:

```
- <value>. Source: <source>. Register: <register>. As of: YYYY-MM-DD. Kind: <statement or sighting>. Label: <label>. Read: <fetch, archive, or browser>. Superseded YYYY-MM-DD: <the later evidence>.
```

A reading that did not arrive uses this shape and is not a fact:

```
- Not available: <reason>. As of: YYYY-MM-DD. Read: <fetch, archive, browser, or not read>.
```

`Kind: statement` means the journalist or the outlet said it, and the as-of date is the date it was made. `Kind: sighting` means a page listed it, and the as-of date is the date the page was read or captured.

`Read` is the way that page was read. `fetch` is a plain fetch. `archive` is an archived copy. `browser` is a rendered page. A `Not available` line names every way that was tried, or `not read` when none was. A fact that did not come from a page omits `Read`.

`Label` is present on every figure, in place. A fact that is not a figure omits it.

A hedge in the source stays inside the value. A superseded fact keeps its source, its register, and its as-of date, and gains `Superseded`. It is not deleted, and it is not marked twice for the same later evidence.

## Fields

Each heading below is required, in this order. A heading holds at least one fact line or one `Not available` line. The value starts with the token named here. Every fact names its outlet where it is about one outlet.

| Heading | Token and what it holds | Register or label |
| --- | --- | --- |
| Identity | `Name:` the professional name, and a byline where it differs from the name as given. | `Public statement`, `Firsthand`, or `Secondhand`. |
| Role | `Role statement:`, `Role sighting:`, `Departure:`, `Return:`, `Retirement:`, `Move:`, or `Beat change:`. Each event is one line, using one of these tokens, and naming the outlet. | `Public statement`, `Firsthand`, or `Secondhand`. `Kind` on every line. |
| Outlets | `Outlet:`, `Type:` as the source states it, `Still publishes: yes` or `Still publishes: no`, and `Outlet closed:` when one has closed. | `Public statement`, `Firsthand`, or `Secondhand`. `Still publishes` and `Outlet closed` carry `Kind`. |
| Beat | `Beat:` what the journalist covers at that outlet. | `Public statement`, or `Research inference` derived from dated work and naming it. |
| Audience | `Audience:` the audience that outlet serves. | `Public statement`, or `Research inference` derived from the outlet's own account of its audience and naming it. |
| Formats | `Format:` the outlet, then one of `staff reporting`, `contributed pieces`, `outside quotes`, `segments or episodes`, then `takes` or `does not take`. | `Public statement`. Where nothing was stated, one `Not available` line for that format at that outlet. |
| Recent work | `Work:` the title as the source stated it, the outlet, and what it covered. The as-of date is the publication date. Then `Angle not taken:`. | A work line is `Public statement`. `Angle not taken` is `Research inference` naming the pieces, or `Not available`. |
| Sources quoted | `Quoted:` who the journalist quotes. | A quotation one piece states is `Public statement`. A pattern across pieces is `Research inference` naming the pieces. |
| Preferences | `Preference:` a preference about pitches the journalist or the outlet stated, in their words, or marked as a paraphrase. | `Public statement` or `Firsthand`. |
| Contact routes | `Route:` the professional route and where it was seen. `Route works:` only where a statement says it works. | `Public statement`, `Firsthand`, or `Secondhand`. A listing is `Kind: sighting`. `Route works` is `Kind: statement` or `Not available: seen listed, not shown to work`. |
| Reach | `Reach:` one measured figure, the metric and the value. No combined score and no tier. | The figure's label, in place, plus the source and the as-of date. |
| Assessments | Four subheadings, in order: What they care about; Style; What motivates a yes; What never to do. | `Research inference`. The value says what it was derived from and names the dated work. |
| Open gaps | What is missing, what conflicts, and a currency field older than the threshold whose refresh did not land. `None as of YYYY-MM-DD.` when there is nothing to name. | A gap is not a claim and carries no register. |
| Database notes | `Database:` an identifier, a search identifier, a filter dump, or any other value that exists only in the root's media database or in one account. | `Secondhand`, naming the database as the relay. A figure keeps its label. |

No field beyond this table is added. A `Not available` line names the heading, the token, and the outlet where the field is about one outlet.

A work line counts as dated work only when the title, the publication date, and the outlet are all present. An item missing any of the three is a `Not available` line and does not count. `Angle not taken` is recorded when a source states what the work left aside, or when the evidence says it and names the pieces. Where the pieces do not state one, the line is `Not available: the pieces do not state an angle left aside`. No angle is proposed.

A role statement, for `Status`, is one `Role statement:` line. A `Role sighting:` does not fill it. A beat, for `Status`, is one `Beat:` line that is a `Public statement`, or a `Research inference` drawn from dated work. Dated work, for `Status`, is one work line that counts.

An assessment subheading holds a claim only when the claim names the dated work it was derived from. Where it cannot, the subheading holds one line naming what was missing, and no claim.

A database value may fill `Outlet`, `Type`, `Still publishes`, `Route`, `Reach`, and `Database`. It is a sighting or a labeled figure, with the database named as the source. It does not fill `Role statement`, `Beat`, or `Preference`. Those three are filled from the professional public record, or they are `Not available`. Where a database value and the public record disagree, both stay, in their own fields, and Open gaps names the disagreement.

`Still publishes`, the in-force role line, the in-force `Beat` line, and `Route works` are the currency fields. The in-force role line is the latest `Role statement`, `Return`, `Departure`, `Retirement`, or `Move` that has not been superseded. A `Role sighting` is never that line.

## Currency

Each currency field has its own source and its own as-of date. `Still publishes` is per outlet. The role and the beat are per outlet. `Route works` is per route.

A `Role statement` is evidence the role was held on the date it was made. A `Role sighting`, including a database row and a page that still lists the journalist, is evidence that the page said so on the date it was read or captured. Pages go stale.

A `Departure`, a `Retirement`, a `Move`, a `Beat change`, an `Outlet closed`, and a `Return` each carry the date and the source. Each is checked against the run's as-of date. A date later than that as-of date does not enter as a fact already true. A date that cannot be ordered against it does not supersede another line, and Open gaps names both lines.

Once a `Departure` or a `Retirement` is recorded, only a later `Return`, or a later `Role statement` that states they hold that role at that outlet, supersedes it. A later byline does not. A later sighting does not. The superseded line stays.

A work line is evidence only for the outlet it names. It does not show the role or the beat at another outlet, and it does not supersede a departure.

A `Route` line is a sighting that the route was listed, dated when seen. `Route works` is `Not available: seen listed, not shown to work` unless a statement says it works.

The staleness threshold is 30 days unless the requester sets another number of days. It is the age past which a currency field is refreshed before a pitch relies on it. Age is counted from that field's own as-of date to the date of the pitch. The file records the number, and whether it was the default or the requester's, on the `Staleness` line. Status, last enriched, and work at another outlet do not refresh a currency field and do not show that it is current.

## What the file never holds

No field holds the journalist's family, health, grief, home life, relationships, or anything they share in a personal capacity. No assessment rests on any of that.

A follower count, a circulation, a traffic figure, a headline, an episode title, or a preference that no source stated is not in the file. The line is `Not available: <reason>`.
