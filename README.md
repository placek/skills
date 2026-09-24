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

## Skills

### Pipeline

- **[ship](./skills/ship/SKILL.md)**: Run a feature end to end through the skills below: vision → plan → implement → verify → document → report → finish. Two gates (after vision, after plan), then it runs unattended. Re-run `/ship <feature>` to resume from `.todo/<feature>/`.

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

- **[handoff](./skills/handoff/SKILL.md)**: Compact the conversation into a handoff doc for a fresh agent.
- **[to-report](./skills/to-report/SKILL.md)**: Like handoff, but for a person: a plain-language progress report, change summary, how-to, or explainer from this session.
- **[wait-what](./skills/wait-what/SKILL.md)**: Make the agent re-pitch a message that didn't land.
- **[to-questionnaire](./skills/to-questionnaire/SKILL.md)**: Turn a decision you can't make alone into a questionnaire for someone who can.
- **[writing-for-agents](./skills/writing-for-agents/SKILL.md)**: How to write skills, `AGENTS.md`, and other docs agents read.

### Typical flow

`/ship <feature>` runs the whole chain: `grill-with-docs` → `to-spec` → `to-tickets` → `implement` (with `tdd`) → `verify` + `code-review` → docs and `domain-modeling` → `to-report` → merge / PR menu. Each step is also a skill you can run on its own. For work too big for one session, start with `/wayfinder`.

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

## Adding a skill

Create `skills/<name>/SKILL.md` with `name` (matching the folder) and `description` frontmatter; put any reference files next to it. Add a line to this README. Load `writing-for-agents` when writing it.

## License

MIT. Original skills © Matt Pocock; see [LICENSE](./LICENSE).
