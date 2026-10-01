---
description: Turn recent work in this repo into brag-doc entries (accomplishments with impact)
argument-hint: "[since, e.g. '2 weeks ago' or a commit/tag] (default: all history)"
allowed-tools: Bash(git log:*), Bash(git diff:*), Bash(git show:*), Bash(git shortlog:*), Read, Grep, Glob
---

Write brag-document entries for the work done in this repository.

## Scope

- Range: `$ARGUMENTS` — if it looks like a date ("2 weeks ago", "2026-09-01"), use `git log --since="$ARGUMENTS"`; if it looks like a commit or tag, use `git log $ARGUMENTS..HEAD`; if empty, use the full history.
- Only count commits authored by the current git user (`git config user.email`), unless there are none — then include all commits and say so.

## Gather evidence

1. List the commits in range with `git log --stat --format='%h %ad %s' --date=short`.
2. For the substantial commits, read the diffs and the files they touch (`src/`, `src/intelligence/`, `frontend/src/`, `notebooks/`, `README.md`) to understand *what* was built and *why* it matters.
3. Pull concrete facts from the code and README: model choices and metrics, API endpoints, test coverage, privacy safeguards, UI features. Never invent numbers — if a metric isn't in the repo, leave it out or mark it `[add metric]`.

## Output

Group accomplishments by theme (e.g. Machine Learning, Backend/API, LLM & Privacy, Frontend, Testing & Quality, Documentation). For each entry write one bullet in the form:

> **Action verb + what you built** — how (key tech/decision) — impact or why it matters. *(commits: abc1234, def5678)*

Then add:

- **Highlights** — the 3 strongest bullets, rewritten as resume-ready one-liners (≤ 25 words each).
- **Skills demonstrated** — a comma-separated list of technologies and competencies evidenced by the commits.
- **Gaps to fill** — any spots marked `[add metric]` and what measurement would back them up.

Keep it factual and specific; prefer outcomes over activity.
