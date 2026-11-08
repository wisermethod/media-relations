# Media Relations

A WISER plugin for earned media at a company of any kind: pitching reporters, newsjacking, and bylined writing. It loads alongside the `wiser` plugin and uses its writing and research skills.

## What ships

Start with Angle Finder for a story menu, choose one story for Media List, then run Pitch for each journalist or host you decide to approach; Campaign Plan turns the menu into a client proposal. Each of the five skills also runs on its own.

- **Angle Finder** takes your material or a direction to build a ranked menu of stories readers on a beat are following and what you add, one checked story angle, a newsjacking package with a draft comment or a no-response decision on one breaking item, or a saved menu re-ranked from reported replies in your pitch log.
- **Media List** takes one chosen story from the menu, or your own angle, and returns a short list of reporters and podcast hosts from your workspace's reporter files, starting with those whose coverage the story cites and carrying dated work, show fit, episode limits and list-check results.
- **Pitch** uses one named journalist or host's reporter sketch to prepare a pitch for a story you have decided to pursue, including a podcast guest offer tied to that story, with the email, subject lines, follow-up plan and checks, and logs your confirmed sends and reported replies against the story they concern.
- **Reporter Research** writes or updates one sourced, dated reporter file on a named journalist through `wiser`'s Bio Sketch with this plugin's journalist extension, using their professional public record and your workspace's media database where available.
- **Campaign Plan** turns a story menu and engagement terms into a client campaign proposal as a PDF in your workspace's bound design, with starting stories, reporters and podcast hosts, a worked pitch, claims and positions for sign-off, and a short cover-note draft.
- **Assignment Editor** gives one menu entry, angle package or pitch a second news-desk read, returning an assignment verdict and the one change that would most improve it; this expert owns no skill and leaves the decision with you.
- **beat-coverage** supplies Angle Finder's reader step with dated coverage already held in reporter files for a beat and date window, marking every returned item unverified, or returns counts alone.

## What it does not do

Nothing in this plugin sends messages or runs outreach. Campaign Plan proposes a campaign for your approval; you still decide whether to pursue a story, which suggested contacts to approach, by which route and when.

The plugin does not provide crisis judgment during an unfolding incident or for a story hooked to a tragedy. Angle Finder's checks cannot judge the news value of a stunt, mascot, visual or playful tie-in, and do not verify your own claims.

Media List does not build lists from a subscription media database. The plugin gives no news-desk read to a press release or op-ed drafted through Content Author directly, and writes no recorded script for a podcast, video or voice-over.

Campaign Plan sets out what monthly reporting should show, and Angle Finder's re-rank summary can feed that report; writing the monthly report is another skill's work, and that skill is not yet built. Campaign Plan does not set a month-by-month story schedule. `system/GAPS.md` collects the primitives' declared gaps.

## Install

Install Wiser first, by its [Install steps](https://github.com/wisermethod/wiser#install): this plugin loads beside it. Then add this plugin in the same app:

- **Claude Cowork.** Open Customize, then Plugins, then Add marketplace. Give it `https://github.com/wisermethod/media-relations`, and install `media-relations`. Then turn on Sync automatically for this marketplace, as Wiser's steps do for theirs.
- **Claude Code.** Run `claude plugin marketplace add wisermethod/media-relations`, then `claude plugin install media-relations@wiser-method-media-relations`, and start Claude Code in your working folder.
- **Codex.** Add `wisermethod/media-relations` as a marketplace and install `media-relations`.
- **ChatGPT for desktop.** Add `wisermethod/media-relations` as a marketplace and install `media-relations`.
- **Grok.** Run `grok plugin marketplace add wisermethod/media-relations`, then `grok plugin install media-relations --trust`.
- **Cursor.** Add your clone of this repository as a workspace root beside your clone of Wiser and your working folder.

Work lands in the working folder you attach, never in this repository.

## Support

Email support@wisermemory.com.
