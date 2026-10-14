# Bio sketch extension: journalist (version 1)

Name: journalist
Version: 1
Prefix: journalist_
Staleness: 30 days
Declared for: a person whose ask is earned media coverage by a journalist, editor, producer or host.

This extends `skills/Bio Sketch/sketch-format.md` in `wiser`. Its Lines and Figures apply throughout. Its Supplied records governs database values: they do not fill `Outlet:`, `Type:` or `Reach:` here. Identity, Role, Standing and fit, Record, Routes, Assessment and Supplied records remain the base's.

## Headings

### Outlets

- Tokens: `Outlet:` an outlet the journalist works at now, current as the base's Currency judges an organization; `Type:` as the source states it; `Still publishes:` `yes` or `no`; `Outlet closed:` a dated closure the evidence shows.
- Register: `Public statement`, `Firsthand` or `Secondhand`. `Still publishes:` and `Outlet closed:` carry `Kind`.
- Required: yes. `Outlet closed:` is an event, not a required field.

`Still publishes: yes` needs a piece the outlet published, with its publication date, or a dated statement from the outlet. `Still publishes: no` needs a dated statement from the outlet. A listing, directory or database row is a sighting of that listing, never the in-force `yes`. Where neither publication evidence nor a dated statement arrives, `Still publishes` is `Not available` with the reason. An outlet that is not current takes no line here; its history stays in the base Role.

### Beat

- Tokens: `Beat:` what the journalist covers at that outlet; `Beat change:` a dated change the evidence shows, naming the outlet.
- Register: `Public statement`, or `Research inference` naming the dated record items it rests on. A stated `Beat change:` carries `Kind`.
- Required: yes. `Beat change:` is an event, not a required field.

### Audience

- Tokens: `Audience:` the audience the outlet serves.
- Register: `Public statement`, or `Research inference` from the outlet's own account, naming it.
- Required: no.

### Formats

- Tokens: `Format:` the outlet, then one of `staff reporting`, `contributed pieces`, `outside quotes`, `segments or episodes`, then `takes` or `does not take`. Four lines per current outlet. Nothing stated: one `Not available` line naming that format at that outlet.
- Register: `Public statement`.
- Required: no.

### Sources quoted

- Tokens: `Quoted:` who the journalist quotes. For a host, a guest the episode or segment states took part, the value saying guest, on that episode's excerpt. A name only in a list of headlines is never quoted.
- Register: one piece's quotation `Public statement`; a pattern across pieces `Research inference` naming the pieces.
- Required: no.

### Angles

- Tokens: `Angle not taken:` what a recent piece left aside, where a source states it or the evidence shows it, naming the pieces. No angle is proposed. A first-person piece takes no angle line.
- Register: `Research inference` naming the pieces, or `Not available: the pieces do not state an angle left aside`.
- Required: no.

### Style

- Tokens: `Style:` how the journalist writes or presents. Quoted sample phrases are marked as quotations.
- Register: `Research inference` naming the dated record items it rests on.
- Required: no.

### Preferences

- Tokens: `Preference:` a pitch preference the journalist or the outlet stated, in their words or marked as a paraphrase.
- Register: `Public statement` or `Firsthand`.
- Required: no.

### Reach

- Tokens: `Reach:` one measured figure for the journalist's own audience or their column, show, newsletter or section, with metric and value. At most one outlet-wide figure where nothing narrower is stated. Never another product of the outlet. No combined score and no tier.
- Register: the source's register under Sourcing Registers in `standards/conventions.md` in `wiser`.
- Label: the base's Figures, in place.
- Required: no.

## Markers

None.

## Fit reason codes added

None.

## Queries for the gather

1. Whether each current outlet still publishes, and the audience it serves.
2. Who the recent pieces quote; for a host, guests the episode states took part, never names from a headline list.
3. Whether each current outlet's desk takes staff reporting, contributed pieces, outside quotes, or segments or episodes.
4. Pitch preferences the journalist or the outlet stated, with the words and the date.
5. Audience figures the Reach heading allows, copied as stated.
6. The angle each recent piece left aside.
