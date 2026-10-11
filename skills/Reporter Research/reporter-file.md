# Reporter file

The contract for the one file Reporter Research writes on one journalist. The Pitch skill and any later checker read it. It is the only field list.

Dates are absolute `YYYY-MM-DD`, per Dates in `standards/conventions.md` in `wiser`. A register is one of the four in Sourcing Registers there, and a figure's label is one of the four in Evidence Labels there. This contract adds neither.

## File name

The file name is the family name, a hyphen, and the given name, in lower case, then `.md`. A space becomes a hyphen. A character Names in `standards/conventions.md` in `wiser` forbids is dropped. An accented letter becomes the plain ASCII letter. A name given as one word is the whole stem.

The name is the file's name only. The resolved home supplies the directory. An update keeps the `File` line the file already has.

Where that name is already another journalist's file, it gains a hyphen and the primary outlet, normalized the same way, and the other file stays. The primary outlet is the outlet of the one in-force role line, and only a collision uses it. No in-force role line, or two or more: no primary outlet. The name is unresolved where the family name is not the last word, the order is unclear, a collision has no outlet to add, or the suffixed name is also another journalist's file. No name is guessed.

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

`Missing` lists only the absent tokens.

`Status` is `draft` when dated work, a role statement, or a beat is absent, and `filed` when all three are present. On `filed`, the warning and `Missing` are absent.

`Created` is the date the file was first written and does not change. `Last enriched` is the as-of date of the run that last changed a fact. A run that changes no fact leaves both as they stand.

`Staleness` records the threshold that applied. `default` means 30 days. `requester` means the requester set the number.

## Lines

A fact uses this shape. Omit optional parts. Keep this order:

```
- <value>. Source: <source>. Register: <register>. As of: YYYY-MM-DD. Kind: <statement or sighting>. Label: <label>. Read: <fetch, archive, or browser>. Superseded YYYY-MM-DD: <the later evidence>.
```

A reading that did not arrive is not a fact, and uses this shape:

```
- Not available: <reason>. As of: YYYY-MM-DD. Read: <fetch, archive, browser, or not read>.
```

`Kind: statement` means the journalist or the outlet said it. `Kind: sighting` means a page listed it.

A stated date includes one that resolves to one absolute date. Which as-of date does this line take? Take the first match.

- A relative date that does not resolve. Ask. Do not write it.
- A work item, and the source states its publication date. Use that date.
- A work item, and the source states none. `Not available`, and not dated work, whatever else dates the read.
- A statement, and the source states the date it was made. Use that date. `Kind: statement`.
- A sighting, and the source states a date. Use that date. `Kind: sighting`.
- A sighting, no source date, and the file it came in states a capture date. Use that capture date. `Kind: sighting`.
- A sighting with neither. Use this run's as-of date. `Kind: sighting`.
- A `Research inference`. Use the latest publication date among the dated work it names, each piece named with its own date in the value.
- None of these. `Not available: the source states no date`. A role line with no date does not count as the role statement.

A capture date or this run's as-of date dates a sighting and never makes an item dated work.

`Read` names how that page was read: `fetch` a plain fetch, `archive` an archived copy, `browser` a rendered page. A `Not available` line names every way tried, or `not read` when none was. A fact that did not come from a page omits `Read`.

`Label` is on every figure, in place, and omitted on any other fact. A hedge in the source stays inside the value. A superseded fact keeps its source, register, and as-of date, and gains `Superseded`. It is not deleted, and not marked twice for the same later evidence.

## Fields

Each heading below is required, in this order. A heading holds at least one line. Any line under it meets that. A listed token is not itself a line. The value starts with the token named here. Every fact names its outlet where it is about one outlet. `Departure`, `Return`, `Retirement`, `Move`, `Beat change`, `Outlet closed`, and `Flag` are written only where the evidence shows the event. No `Not available` line is written because an event was not found.

| Heading | Token and what it holds | Register or label |
| --- | --- | --- |
| Identity | `Name:` the professional name, and a byline where it differs from the name as given. | `Public statement`, `Firsthand`, or `Secondhand`. |
| Role | `Role statement:`, `Role sighting:`, `Former role:`, `Departure:`, `Return:`, `Retirement:`, `Move:`, or `Beat change:`. One event per line, naming the outlet. | `Public statement`, `Firsthand`, or `Secondhand`. `Kind` on every line. |
| Flags | `Flag:` one reason code, `left_field`, `retired`, `deceased`, `vendor`, or `non_practitioner`, then what shows it. One code per line, as Flags below states. Where none is shown, one line: `No flag was found in the sources read.`, with its as-of date, or the `Not available` line Flags below gives. | As the statement it rests on, under Flags below. `Kind: statement` on every `Flag:` line. |
| Outlets | `Outlet:`, `Type:` as the source states it, `Still publishes: yes` or `Still publishes: no`, and `Outlet closed:` when one has closed. | `Public statement`, `Firsthand`, or `Secondhand`. `Still publishes` and `Outlet closed` carry `Kind`. |
| Beat | `Beat:` what the journalist covers at that outlet. | `Public statement`, or `Research inference` from dated work, naming it. |
| Audience | `Audience:` the audience that outlet serves. | `Public statement`, or `Research inference` from the outlet's own account, naming it. |
| Formats | `Format:` the outlet, then one of `staff reporting`, `contributed pieces`, `outside quotes`, `segments or episodes`, then `takes` or `does not take`. | `Public statement`. If nothing was stated, one `Not available` line for that format at that current outlet. |
| Recent work | `Work:` the title as the source stated it, the outlet, and what it covered. Five to ten pieces, the latest that count. Fewer than five: each that counts. Then `Angle not taken:`. | A work line is `Public statement`. `Angle not taken` is `Research inference` naming the pieces, or `Not available`. |
| Sources quoted | `Quoted:` who the journalist quotes. For a host of a show, podcast, or broadcast segment, a guest that episode or segment states took part, the value says guest, on that episode's excerpt. A person named only in a list of headlines is not quoted. | A quotation one piece states is `Public statement`. A pattern across pieces is `Research inference` naming the pieces. |
| Preferences | `Preference:` a pitch preference the journalist or the outlet stated, in their words or marked as a paraphrase. | `Public statement` or `Firsthand`. |
| Contact routes | `Route:` a route to the journalist, or a pitch or tip route a current outlet publishes, and where it was seen. Not reader letters or a general inbox. `Route works:` only where a statement says it works. | `Public statement`, `Firsthand`, or `Secondhand`. A listing is `Kind: sighting`. `Route works` is `Kind: statement` or `Not available: seen listed, not shown to work`. |
| Reach | `Reach:` one measured figure for the journalist's own audience, or for the column, show, newsletter, or section they publish in, the metric and the value. At most one outlet-wide audience figure, where nothing narrower is stated. Not another product of the outlet. No combined score and no tier. | The figure's label, in place. |
| Assessments | Four subheadings, in order: What they care about; Style; What motivates a yes; What never to do. | `Research inference`. |
| Open gaps | What is missing, what conflicts, and a currency field past the threshold this run did not refresh. Where no dated role change was found, `No dated role change was found in the sources read.` `None as of YYYY-MM-DD.` when nothing is to name. | A gap is not a claim and carries no register. |
| Database notes | `Database:` an identifier, a search identifier, a filter dump, or any other value only in that database or account. | `Secondhand`, naming the database as the relay. A figure keeps its label. |

No field beyond this table is added. A `Not available` line names the heading, the token, and the outlet where the field is about one outlet.

A work line is dated work only when the title, the publication date, and the outlet are all present. Missing any of the three, it is `Not available` and does not count. Record `Angle not taken` when a source states what the work left aside, or the evidence says it and names the pieces. Otherwise `Not available: the pieces do not state an angle left aside`. No angle is proposed. A piece recorded as a first-person column takes no angle line.

For `Status`, a role statement is one `Role statement:` line. A `Role sighting:` does not fill it. A beat is one `Beat:` line that is a `Public statement`, or a `Research inference` drawn from dated work. Dated work is one work line that counts.

An assessment subheading holds a claim only when it names the dated work it was derived from. Otherwise it holds one line naming what was missing, and no claim.

`Role statement`, `Beat`, and `Preference` come from the professional public record only, including where it and the database disagree. The database value stays on a `Database` line. Silence is `Not available`. Open gaps names a disagreement.

On any other field, where a database value and the public record disagree, both stay, in their own fields, and Open gaps names the disagreement.

A database value may fill `Outlet` and `Type` on a current outlet, and `Route`, `Reach`, and `Database`, as a sighting or a labeled figure, the database named as the source. It does not fill `Still publishes`.

The currency fields are `Still publishes`, the in-force role line, the in-force `Beat`, and `Route works`. The in-force role line is the latest `Role statement`, `Former role`, `Return`, `Departure`, `Retirement`, or `Move` not yet superseded. A `Role sighting` is never that line, and an in-force `Former role` shows the role has ended.

## Currency

Each currency field has its own source and as-of date. `Still publishes`, the role, and the beat are per current outlet. `Route works` is per route.

An outlet is current when its in-force role line is a `Role statement` or a `Return`, a work line there is dated within 365 days of the as-of date, or the request named it. An in-force `Departure`, `Retirement`, `Move` away, or `Former role` does not make it current. Only a current outlet takes `Outlet:`, `Type:`, `Still publishes`, `Beat`, `Audience`, and the four `Format` lines. Any other outlet appears only in Role: its history lines, or one `Former role:` line where it has none.

A statement that the role was held before, including served as, formerly, was, or previously, is `Former role:`, never `Role statement:`, dated when made, `Kind: statement`, evidence the role had ended by that date. It supersedes an earlier `Role statement:` of that role at that outlet, and is then the in-force role line there. A `Departure:` stays for a dated end the evidence states.

A `Role statement` is evidence the role was held. A `Role sighting`, including a database row and a page that still lists the journalist, is evidence the page said so, not that the role was held. Pages go stale.

On a current outlet, a database row, a directory, or any page that lists an outlet is a sighting of that listing, dated when read, and never the in-force `Still publishes: yes`. That line needs a piece the outlet published, with its publication date, or a dated statement from the outlet. Where neither arrives, `Still publishes` is `Not available` with the reason, and the listing stays as a sighting or on a `Database` line.

A `Departure`, `Retirement`, `Move`, `Beat change`, `Outlet closed`, and `Return` each carry their date and source, checked against the run's as-of date. A later date does not enter as a fact already true. A date that cannot be ordered against it does not supersede another line, and Open gaps names both.

Once a `Departure`, a `Retirement`, or a `Former role` is recorded, only a later `Return`, or a later `Role statement` that states they hold that role at that outlet, supersedes it. A later byline does not. A later sighting does not.

A work line counts only for the outlet it names, not as the role or the beat elsewhere, and not against a departure.

Two statements of different values that cannot be ordered, the same date or a date that cannot be ordered, leave that currency field unresolved. A pitch reads it as not current.

The staleness threshold is 30 days unless the requester sets another number. Past that age, from the field's own as-of date to the pitch date, refresh the field before a pitch relies on it. `Staleness` records the number and whether it was the default or the requester's. Status, last enriched, and work at another outlet are not currency: they do not refresh a currency field and do not show that it is current.

## Flags

A flag marks a journalist the Pitch skill does not pitch while the flag is in force. It stops nothing else: the file is still built, gated, and written, and `Status` is set as Opening lines states.

| Code | Set when |
| --- | --- |
| `left_field` | The in-force role line places the journalist in work outside journalism, such as communications for a company or an agency. |
| `retired` | The in-force role line is a `Retirement`. |
| `deceased` | The outlet or a news report states that the journalist has died. |
| `vendor` | The journalist works for a company that sells a product or service, and their work at the outlet is that company's marketing. |
| `non_practitioner` | The in-force role is one in which the journalist does not report or edit pieces a pitch could reach: operations, writing or producing what the outlet labels paid or sponsored content, an academic or association masthead, or a copy desk. |

One fact sets one flag. Where it fits more than one of `vendor`, `left_field`, and `non_practitioner`, set the first of them in that order.

A flag rests on a statement: an in-force Role line with `Kind: statement`, or, for `deceased`, its own excerpt copied from the page. A flag on a Role line names that line's token and outlet in its value, and takes that line's source, register, and as-of date. A sighting, a database value, a `Research inference`, or a work line alone never sets a flag, and neither does one piece the outlet labels paid or sponsored. Geography and any other fit to one program are not flags and take no line.

Where this run read no source beyond the existing file, Flags holds any flag a carried Role line shows, and otherwise `Not available: no source was read this run that could show a flag`, never the line saying none was found.

A `deceased` flag holds the code, its source, and its date. Nothing else from the notice enters any line.

A flag stays in force until it is superseded. A flag resting on a Role line is superseded when that line is. `retired` and `left_field` are also superseded by a later `Return:`, or a later `Role statement:` of reporting or editing at a news outlet. `vendor` and `non_practitioner` are superseded by a later `Role statement:` of reporting or editing. A dated correction or retraction, by the source of the statement a flag rests on, supersedes that flag, `deceased` included. Nothing else supersedes `deceased`. A superseded flag gains `Superseded` as Lines states.

## What the file never holds

No field holds the journalist's family, health, grief, home life, relationships, or anything shared in a personal capacity, and no assessment rests on that. A `deceased` flag records that a death was reported, and nothing more, as Flags states.

A follower count, circulation, traffic figure, headline, episode title, or preference that no source stated is `Not available: <reason>`.
