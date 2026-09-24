---
name: ship
description: "Run a feature end to end through the other skills: grill the idea, spec and ticket it, agree the tests, implement red-green, verify, document, report. Resumes from `.todo/<feature>/` when re-run."
---

# Ship

Drive one piece of work from a loose idea to a verified, documented, reported change, by running the other skills in order. Ship itself decides nothing about the code; it decides **which skill runs next**, records where you are, and holds the gates.

```
vision  →  plan  →  tests  →  implement  →  verify  →  document  →  report  →  finish
 (gate)     (gate)   (gate)
```

Three gates stop for the user: after **vision** (shared understanding), after **plan** (tickets approved), and after **tests** (seams and test plan agreed). From there ship runs to the end without check-ins. Only four things stop it: an irreversible or destructive operation; a security-sensitive action; a side effect outside the repo (a merge, a push, a publish); or a plan so broken that every path forward is a guess. Everything else is a **ruling**: decide, record it in the ship log as `Ruling: <what> - <why> - <cost if wrong>`, keep going.

## State and resume

Everything lives in `.todo/<feature-slug>/`, next to the `spec.md` and tickets the other skills write. Ship keeps its own section at the bottom of `spec.md`:

```markdown
## Ship

Branch: feature/<slug>

- [x] vision (shared understanding reached)
- [x] plan (4 tickets approved)
- [ ] tests
- [ ] implement
- [ ] verify
- [ ] document
- [ ] report
- [ ] finish

Ruling: ...
```

On invocation, resolve the feature slug from the argument (or ask for one line describing the work and derive it). If `.todo/<slug>/spec.md` exists, read its `## Ship` section and resume at the first unchecked stage; do not redo checked stages. If it does not exist, start at vision. Announce where you are: "Resuming `invoice-payments` at implement, 2 of 4 tickets done."

Before touching code, make sure you are on `feature/<slug>` (create it from the current branch if needed). Never implement on `main`/`master`.

## Stages

### 1. Vision

Size the request first and say the size out loud so the user can correct it:

- **Spike**: a feasibility question. Answer it cheaply, keep nothing, report the finding. Ship ends here.
- **Small**: a well-scoped change to a flow that already exists (a flag, a small endpoint, a one-file fix). Grill briefly, then write a single ticket in step 2 instead of a spec and breakdown.
- **Feature**: everything else. Full pipeline.
- **Too big for one map**: several independent subsystems, or more than one session's worth of decisions. Stop and suggest `wayfinder`; ship one of its resolved slices later.

Load two skills with `skill_view` (`grilling` and `domain-modeling`) and grill until the frontier is empty. Explore the codebase yourself for facts; the decisions are the user's. When you believe you have shared understanding, write it back in a few lines (what, for whom, done-when, out of scope) and **stop for the gate**: the user confirms or corrects.

Tick `vision`.

### 2. Plan

Load the `to-spec` skill (`skill_view`): synthesise the conversation into `.todo/<slug>/spec.md`. Then load `to-tickets`: break it into tracer-bullet tickets with `Blocked by:` edges. `to-tickets` already quizzes the user on the breakdown; their approval of it is the **second gate**. For a small change, write one ticket by hand from the `to-tickets` template and skip the quiz.

Append the `## Ship` section to `spec.md`, tick `plan` with the ticket count, commit `.todo/` on the branch.

### 3. Tests

Load the `tdd` skill (`skill_view`). Its rule is that tests are written only at **pre-agreed seams**, so agree them now, before any code:

1. From the spec's Testing Decisions, list every seam under test: the public interface, what behaviour it must show, which tickets it covers. Prefer existing seams; one is ideal.
2. For each seam, name the kind of test (through the interface, integration-style; mocks only at system boundaries), the prior art in the codebase it should resemble, and the exact command that runs it.
3. Turn each ticket's acceptance criteria into the test names that will prove them, one line each, written into the ticket under `## Tests`. No test bodies yet: bulk tests written before the code verify imagined behaviour, which `tdd` names as an anti-pattern. The bodies are written one at a time in step 4, each before its implementation.
4. Present seams, test kinds, and the per-ticket test names and **stop for the gate**: the user confirms or moves the seams.

Tick `tests`.

### 4. Implement

Load the `implement` skill (`skill_view`); it keeps ticket `Status:` lines current. Work the frontier in number order, and every ticket is red-green:

- Take the first test name from the ticket's `## Tests`. Write it, run it, **see it fail**. A test that passes before the implementation exists is a finding about the test.
- Write the minimum code that makes it pass. Run it, see it pass. Commit.
- Next test name. Refactoring waits for step 5.
- A ticket is `done` only when every test named for it exists, has been seen red then green, and its acceptance criteria are ticked.

**Subagents.** If there are four or more tickets and the frontier holds independent ones, offer to dispatch a fresh subagent per frontier ticket. Each subagent gets exactly: the ticket file, `spec.md`, `CONTEXT.md` if present, and an instruction to load `tdd`. Nothing from this conversation. When one returns, do not trust its report: read `git diff` for its commits and run its tests yourself before marking the ticket done. Default is inline when the user does not ask.

Do not stop between tickets. Plan defects are rulings. If a test will not go green and the cause is not obvious, load `diagnosing-bugs` rather than guessing.

Tick `implement` when every ticket is `Status: done`.

### 5. Verify

Load the `verify` skill (`skill_view`) and hold to it for the rest of the run.

1. Run the project's full checks: typecheck, lint, test suite, build. All green, evidence in this session.
2. Walk the spec's acceptance criteria and user stories one by one against the running code. Tick each in the ticket files; a criterion you cannot demonstrate is not met.
3. Load `code-review` (`skill_view`) against the branch's merge base. Fix every Standards or Spec finding that would affect a person using the software: reproduce with a failing test, make it pass, rerun the full checks. This is also where refactoring belongs (`refactor` if it is more than a local cleanup). Findings you decline become rulings. Minor polish is listed for the report, not fixed.
4. Repeat 1-3 until a pass produces no fixes.

Tick `verify` with the commands and results (`tests 84/84, tsc clean, build ok`).

### 6. Document

Documentation is part of the change, not an afterthought.

- Update every doc the change made stale or incomplete: README, `docs/`, CHANGELOG, API reference, CLI help, config examples, comments that described the old behaviour. Add docs for anything a user needs to know to use the feature.
- Load `domain-modeling` (`skill_view`) once more: any term the work introduced goes into `CONTEXT.md`; any decision that met the three ADR tests gets its ADR.
- Commit.

Tick `document`.

### 7. Report

Load the `to-report` skill (`skill_view`) and write a **change summary** for the person who asked for the feature, saved to `.todo/<slug>/report.md`. If the run stopped short (a spike, a blocker), write a progress report instead.

Set `spec.md`'s `Status:` to `done`, tick `report`, commit.

### 8. Finish

Run the full checks once more on the final tree (evidence, again). Then present exactly this and wait:

```
Shipped <feature> on feature/<slug>: N commits, all checks green, report at .todo/<slug>/report.md.

1. Merge into <base> locally
2. Push and open a pull request
3. Leave the branch as it is
```

Carry out the choice. For 1, run the checks again on the merged result before deleting the branch. For 2, follow the repo's PR conventions and report the URL. Tick `finish`.

End with two lists in your final message, both exhaustive: **Rulings I made** (from the ship log, each with its cost if wrong) and **Left for later** (deferred review findings, follow-up ideas, remaining smells). They are the only place the decisions you took on the user's behalf reach them.

## What ship does not do

- It does not re-grill on resume: a checked stage is done.
- It does not skip a gate because the answer seems obvious. Present, then wait.
- It does not merge, push, or publish without the user choosing it in step 8.
- It does not fix bugs or refactor beyond the tickets. Those are new tickets, or a `refactor` session.

## Credits

The stage shape, gates, rulings, the four stops, resume-from-ledger, and the finish menu are adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT): `brainstorming`, `writing-plans`, `executing-plans`, `subagent-driven-development`, `finishing-a-development-branch`. The stages themselves are this repo's skills.
