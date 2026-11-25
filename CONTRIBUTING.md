# Contributing (a.k.a. how I work in this repo)

This is a personal learning repository, but I treat it like a professional
codebase — the same habits I would use on a team.

## Workflow

1. Branch from `main` for anything non-trivial
   (`feature/subnet-json-output`, `notes/linux-filesystem`).
2. Commit in the imperative mood, one logical change per commit
   ("Add DHCP lab write-up", not "stuff").
3. Open a pull request even when working alone — it keeps CI honest and
   builds the review habit.
4. Merge only when CI is green.

## Local checks

```bash
# spelling
pip install codespell
python3 -m codespell_lib --check-filenames --check-hidden .

# markdown style
npx markdownlint-cli2 "**/*.md"

# project tests
python3 -m pytest projects/subnet-calculator
```

## What CI runs

`.github/workflows/checks.yml` runs on every push and pull request:

| Job | Tool | What it catches |
| --- | ---- | --------------- |
| spelling | codespell | typos in prose and filenames |
| markdown | markdownlint-cli2 | broken structure: missing bullets, bad headings |
| tests | pytest | regressions in project code |

## Conventions

- Notes live in topic folders with a README; labs in `labs/`, projects in `projects/`.
- Every project README ends with a "What I learned" section.
- Prose typos are bugs: CI exists because the first 400 lines of notes
  shipped with roughly forty of them.
