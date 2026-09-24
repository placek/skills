# AGENTS.md

Agent skills for Hermes, plus the `locoder` agent that runs them. See
[README.md](./README.md) for the skill index and profile setup.

## This checkout is live

The `locoder` profile symlinks straight here:

| path | effect of editing it |
|---|---|
| `skills/` | the running agent's skills — a saved `SKILL.md` is live next time it loads |
| `plugins/` | Hermes loads these; a Python change needs a new session |
| `config.yaml`, `SOUL.md` | take effect **next session**, not this one |

So a broken `SKILL.md` or `plugin.yaml` breaks the agent editing it. After
touching either, confirm the whole set still resolves:

```sh
hermes -p locoder skills list     # expect: N local — N enabled, 0 disabled
hermes -p locoder plugins list    # expect: web-defuddle ... enabled
```

Hermes also writes runtime state into `skills/` (`.hub/`, `.usage.json`) and
`__pycache__/` into `plugins/`. Both are gitignored — never commit them.

## Writing a skill

`skills/<name>/SKILL.md`, YAML frontmatter with `name` (matching the directory)
and `description`; reference files sit beside it. Add a line to the README's
skill index. Load `writing-for-agents` before writing one — it covers the
description wording that decides whether the skill ever fires, and
`SKILL-MECHANICS.md` beside it covers frontmatter.

Two names to avoid: anything Hermes already owns as a built-in command (that is
why `handoff` became `to-agent`), and a name already in `skills/`.

## Discovery traps

Skill and plugin discovery do **not** behave the same way:

- **Skills** are found with `Path.rglob("**/SKILL.md")`, which refuses to
  descend into symlinked directories. A symlink *inside* a skills root finds
  nothing; only the root itself may be a link.
- **Plugins** are found with `iterdir()`, which follows symlinks fine.

A skill that does not appear in `skills list` is usually this, a `name` that
disagrees with its directory, or invalid frontmatter YAML.

## Conventions

Issues are markdown in `.todo/`, committed with the code; finishing one changes
its `Status:` line rather than deleting the file. Commits use an imperative
subject and a body explaining why, not what.
