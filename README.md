# Skills

My agent skills for [Hermes Agent](https://github.com/NousResearch/hermes-agent). Most are near-verbatim copies of [Matt Pocock's skills](https://github.com/mattpocock/skills) ([aihero.dev/skills](https://www.aihero.dev/skills)), adjusted to track issues as plain markdown files in `.todo/`.

Upstream snapshot: `mattpocock/skills@c55ee46`. The first commit in this repo is the untouched import, so `git diff <first-commit> -- skills/` shows every local change.

## Install

Clone the repo, then point Hermes at its `skills/` directory in `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - ~/code/skills/skills
```

Every skill then shows up in `skills_list` and as a `/skill-name` command. `git pull` keeps them current.

## The `locoder` profile

The repo also ships a ready-made agent: [`config.yaml`](./config.yaml) (Hermes
configuration) and [`SOUL.md`](./SOUL.md) (its identity). Together they turn
these skills into a coding agent rather than a pile of markdown.

Wire it up as a dedicated Hermes profile, symlinked so the checkout stays the
single source of truth:

```sh
REPO=$(pwd)
hermes profile create locoder --no-skills     # --no-skills: `hermes update` never writes into the repo
P=~/.hermes/profiles/locoder
mv $P/skills $P/bundled-skills                # keeps the seeded hermes-agent skill
ln -s $REPO/skills      $P/skills
ln -s $REPO/config.yaml $P/config.yaml
ln -s $REPO/SOUL.md     $P/SOUL.md

# the delegation target, for work too big for a local context
cp -r ~/.hermes/skills/autonomous-ai-agents/claude-code \
      $P/bundled-skills/autonomous-ai-agents/

hermes -p locoder skills list                 # or just: locoder
```

`bundled-skills/` is a second read-only scan root, listed under
`skills.external_dirs` in `config.yaml` as a profile-relative path.

### Web extraction with Defuddle

[`plugins/web/defuddle/`](./plugins/web/defuddle/) is a Hermes web-provider
plugin that routes every `web_extract` call through
[kepano/defuddle](https://github.com/kepano/defuddle) — the main-content
extractor behind Obsidian Web Clipper. It returns the article body as markdown
instead of a page dump, which is what makes `/research` quote sources rather
than sidebars. On Wikipedia's write-ahead logging page, the previous backend
opened with the *"Find sources: …"* maintenance banner; Defuddle opens with the
first sentence of the article.

It needs the Node CLI, which is **not** bundled:

```sh
mkdir -p ~/.hermes/tools/defuddle && cd ~/.hermes/tools/defuddle && npm install defuddle
ln -s $REPO/plugins ~/.hermes/profiles/locoder/plugins
```

The binary is found via `$HERMES_DEFUDDLE_BIN`, then `web.defuddle_bin`, then
`$PATH`, then that vendored path. `config.yaml` pins `web.extract_backend:
defuddle`; the provider is extract-only, so search keeps using its own backend.
If the binary goes missing the whole batch fails, which trips Hermes' one-shot
keyless rescue — extraction degrades to the keyless ring instead of breaking.

Note the asymmetry with skills: **plugin** discovery uses `iterdir()`, which
*does* follow symlinks, so linking `plugins/` (or a single plugin inside it)
both work. Skill discovery uses `rglob`, which does not.

Two things worth knowing before you change that layout:

- **The `skills/` symlink must be the scan root.** Skill discovery is
  `Path.rglob("**/SKILL.md")`, which refuses to descend into symlinked
  *subdirectories* — a link dropped *inside* a skills dir finds nothing. Link
  whole roots, or use `skills.external_dirs` (each entry is its own root).
- **Hermes writes runtime state into the skills dir** (`.hub/`, `.usage.json`).
  [`.gitignore`](./.gitignore) covers it.

What `config.yaml` tunes, beyond the model/provider block:

- `agent.coding_context: focus` — coding brief plus a live git snapshot, lean
  coding toolset, non-coding skill categories demoted to names-only.
- `agent.coding_instructions` — the standing rules that make these skills the
  default method (`/ship`, `/tdd`, `/verify`, `.todo/`, delegation, research).
- `agent.tool_use_enforcement` / `execution_guidance` forced **`true`**, not
  `auto`: `auto` matches on the *model name* (`gpt`, `codex`, `qwen`, …), so a
  locally-served model called `coder` silently gets neither.
- `agent.verify_on_stop: auto` — the runtime half of the `verify` skill.
- `skills.auto_load: [verify]` — the one rule that must never be a recall miss.
- **Delegation to Claude Code** for work too big for a local context (see the
  `claude-code` skill), and a keyless web-research ring for `research`.

## Skills

### Pipeline

- **[ship](./skills/ship/SKILL.md)**: Run a feature end to end through the skills below: vision → plan → acceptance → implement → verify → document → report → finish. Three gates (after vision, plan, and the red acceptance tests), then it runs unattended. Re-run `/ship <feature>` to resume from `.todo/<feature>/`.

### Planning

- **[grill-me](./skills/grill-me/SKILL.md)**: Get relentlessly interviewed about a plan or design.
- **[grill-with-docs](./skills/grill-with-docs/SKILL.md)**: Same, but also updates `CONTEXT.md` and ADRs as terms and decisions land.
- **[grilling](./skills/grilling/SKILL.md)**: The interview loop behind both of the above.
- **[domain-modeling](./skills/domain-modeling/SKILL.md)**: Build and sharpen the project glossary (`CONTEXT.md`) and ADRs.
- **[to-spec](./skills/to-spec/SKILL.md)**: Turn the conversation into a spec at `.todo/<feature>/spec.md`.
- **[to-tickets](./skills/to-tickets/SKILL.md)**: Break a spec or plan into tracer-bullet tickets, one file each.
- **[wayfinder](./skills/wayfinder/SKILL.md)**: Plan work too big for one session as a map of decision tickets.
- **[triage](./skills/triage/SKILL.md)**: Move `.todo/` issues through the triage states and write agent briefs.

### Coding

- **[implement](./skills/implement/SKILL.md)**: Build the tickets, test-first, then review and commit.
- **[tdd](./skills/tdd/SKILL.md)**: Red-green loop at pre-agreed seams.
- **[refactor](./skills/refactor/SKILL.md)**: Behaviour-preserving cleanup in small test-gated steps; green before, green after, revert on red.
- **[code-review](./skills/code-review/SKILL.md)**: Two-axis review (standards and spec) of a diff, run as parallel sub-agents.
- **[verify](./skills/verify/SKILL.md)**: Evidence before claims: run the proof, read the output, then say it's done.
- **[diagnosing-bugs](./skills/diagnosing-bugs/SKILL.md)**: Feedback-loop-first diagnosis for hard bugs and performance regressions.
- **[codebase-design](./skills/codebase-design/SKILL.md)**: Deep-module vocabulary: module, interface, depth, seam, adapter.
- **[improve-codebase-architecture](./skills/improve-codebase-architecture/SKILL.md)**: Find deepening opportunities and show them as an HTML report.
- **[prototype](./skills/prototype/SKILL.md)**: Throwaway prototype (logic demo or UI variants) to answer a design question.
- **[resolving-merge-conflicts](./skills/resolving-merge-conflicts/SKILL.md)**: Resolve a merge or rebase hunk by hunk, by intent.
- **[research](./skills/research/SKILL.md)**: Background research against primary sources, saved as a cited markdown file.

### Productivity

- **[to-agent](./skills/to-agent/SKILL.md)**: Compact the conversation into a handoff doc for a fresh agent.
- **[to-report](./skills/to-report/SKILL.md)**: Like `to-agent`, but for a person: a plain-language progress report, change summary, how-to, or explainer from this session.
- **[wait-what](./skills/wait-what/SKILL.md)**: Make the agent re-pitch a message that didn't land.
- **[to-questionnaire](./skills/to-questionnaire/SKILL.md)**: Turn a decision you can't make alone into a questionnaire for someone who can.
- **[writing-for-agents](./skills/writing-for-agents/SKILL.md)**: How to write skills, `AGENTS.md`, and other docs agents read.

### Typical flow

`/ship <feature>` runs the whole chain: `grill-with-docs` → `to-spec` → `to-tickets` → `tdd` outer loop (failing acceptance tests) → `implement` (inner red-green loop per ticket) → `verify` + `code-review` → docs and `domain-modeling` → `to-report` → merge / PR menu. Each step is also a skill you can run on its own. For work too big for one session, start with `/wayfinder`.

## Issues: the `.todo/` directory

Issues are markdown files in a `.todo/` directory at the root of the project you're working on, committed with the code.

```
.todo/
├── login-timeout.md          # a standalone issue (bug report, idea)
└── checkout-v2/              # one directory per feature or wayfinder effort
    ├── spec.md               # from to-spec
    ├── map.md                # from wayfinder (instead of spec.md)
    ├── 01-cart-summary.md    # tickets, numbered in dependency order
    └── 02-apply-coupon.md
```

Each file starts with its title and a few plain `Key: value` lines:

```markdown
# 02: Apply coupon

Status: ready-for-agent
Type: enhancement
Blocked by: 01

## What to build
...

## Comments
```

- **Status** (one of):
  - `needs-triage`, `needs-info`: triage is not finished
  - `ready-for-agent`, `ready-for-human`: ready to be worked on
  - `open`: an unclaimed wayfinder ticket
  - `in-progress`: someone is working on it
  - `done`
  - `wontfix`
- **Type**: `bug` or `enhancement` (triage), or `research`, `prototype`, `grilling` or `task` (wayfinder).
- **Blocked by**: ticket numbers in the same directory, or `none`.
- Discussion goes at the bottom under `## Comments`. Files are never deleted or moved: finishing an issue only changes its `Status:` line.

Finding work is a grep away: `grep -rl '^Status: ready-for-agent' .todo`.

Rejected enhancements are recorded in `.out-of-scope/` (see the triage skill).

## Changes from upstream

- Dropped: `ask-matt`, `setup-matt-pocock-skills`, `teach`, `wizard`, and everything in upstream's `misc/`, `in-progress/`, and `deprecated/`.
- Added: `refactor`, `to-report`, `verify` and `ship` (not from upstream; distilled from other public skills, credited inside each). `ship` is the superpowers-style pipeline over the rest.
- The GitHub, GitLab, and "configure your tracker" branches are gone. `to-spec`, `to-tickets`, `triage`, `wayfinder`, `code-review`, and `implement` use `.todo/` directly.
- `implement` updates ticket `Status:` lines as it works.
- "Call the Skill tool with X" became "Load the `X` skill (`skill_view`)", which is how Hermes loads a skill.
- Removed `disable-model-invocation` and `argument-hint` (Hermes ignores them) and the Codex `agents/openai.yaml` files.
- Renamed `handoff` to `to-agent`: Hermes has a built-in `/handoff` command, so the skill's slash command was unreachable. It also pairs with `to-report` (to an agent / to a person).

## Adding a skill

Create `skills/<name>/SKILL.md` with `name` (matching the folder) and `description` frontmatter; put any reference files next to it. Add a line to this README. Load `writing-for-agents` when writing it.

## License

MIT. Original skills © Matt Pocock; see [LICENSE](./LICENSE).
