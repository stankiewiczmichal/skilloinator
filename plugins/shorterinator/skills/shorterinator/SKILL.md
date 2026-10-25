---
name: shorterinator
description: Use when the user wants the AI to stop repeating the same multi-step routine by hand and use a script instead - "make a script for this", "automate this step", "find what can be scripted in this project", "zrób skrypt do tego", "zautomatyzuj to", "przyspiesz pracę w tym projekcie". Asks whether the script belongs to this project folder or to all AI work, analyses the project and proposes routines worth scripting (or takes the one the user names), agrees success criteria with the user, writes a script that never touches source files, tests it, and registers it so the AI uses it in later sessions. The human approves every script; when the AI is unsure a result is right, it stops and asks.
---

# Shorterinator

You turn routines that the AI repeats step by step into scripts that the AI
runs in one call. The script is for the AI, not for the person: you write it,
you save it where the AI will find it, and you leave an instruction so the AI
uses it next time instead of redoing the steps by hand.

Example: a designer finishes every vector project by exporting the same set of
variants (outlined, not outlined, PDF, ...). Instead of the AI running each
conversion again in every session, one script produces the whole set.

The person decides; you propose and do the work. A script that runs on its own
can do quiet damage, so two things are never acceptable: changing or
overwriting a source file, and passing on a wrong result as if it were right.

## 1. Scope

Ask once, before anything else (use a question tool if you have one):

- **This project**: the script works only in the current folder or project.
- **All AI work**: the script is available in every project.

Locations:

| Scope | Script and registry | Instruction file the AI loads |
| --- | --- | --- |
| This project | `<project>/.agents/scripts/` | `CLAUDE.md`, or `AGENTS.md` if the project uses that |
| All AI work | `~/.agents/scripts/` | `~/.claude/CLAUDE.md` (Claude Code), `~/.codex/AGENTS.md` (Codex) |

If the project already keeps AI helpers somewhere else, use that place and say
so. A global script must not assume any project's paths: everything it works
on comes in as arguments.

## 2. Which routine

There are two ways in:

- **The person names a routine** ("script the export"): go to step 4.
- **Nothing named**: analyse (step 3) and propose.

## 3. Analyse and propose

Read what you can reach in the chosen scope:

- file types and how outputs are named next to their sources
  (`logo.svg`, `logo-outlined.pdf`, `logo-web.png` suggests an export set),
- build and task files (`Makefile`, `package.json` scripts, `justfile`, CI
  configs): routines that already have a command do not need a new script,
- `CLAUDE.md`, `AGENTS.md`, `README`, notes and memory that describe how the
  work is done,
- git history: commits that keep touching the same group of files the same way,
- the existing registry, so you do not propose a script that already exists.

Propose only routines that are repeated, have a fixed sequence of steps and
need no judgment along the way. If a step needs a human eye (picking a crop,
fixing something by hand before export), leave it out or say that the routine
cannot be scripted as it stands.

Show the candidates as a table and let the person choose:

| Routine | Evidence | Steps today | What the script would do | Risk |
| --- | --- | --- | --- | --- |

Evidence means files or history you actually saw. Do not guess how often
something happens; if you cannot tell, say so.

## 4. Specification and success criteria

Before writing code, agree on a short specification:

- **Input**: which files or arguments, and how they are found.
- **Output**: which files, named how, written where.
- **Tools needed**: check that each one is installed (`command -v`) and note
  the version. If one is missing, stop and tell the person.
- **Side effects**: everything the script writes or deletes. Sources are
  read-only.
- **Success criteria**: how to tell a good result from a bad one, for example
  "the PDF opens and has the same page count as the source", "no live text
  left in the outlined version", "fonts embedded". Take them from three places
  and say which is which:
  1. what the analysis shows,
  2. earlier outputs in the project that were clearly accepted (delivered,
     committed, used as references),
  3. what the person tells you.

Ask which mistakes would be unacceptable and make sure each one has a
criterion. Watch for tools that degrade quietly instead of failing: a missing
font replaced by a fallback, a colour profile dropped, a layer skipped. "Fonts
embedded" does not catch a substituted font; "fonts in the output are the ones
named in the source" does.

Show the specification and wait for approval. The criteria are approved
together with the script; they are the reference point for every later run.

## 5. Write the script

Use POSIX shell for short tool chains and Python 3 (standard library) for
anything with logic. Every script must:

- open with a header: purpose, usage, scope, success criteria, date created,
- never modify or overwrite its inputs,
- in project scope, resolve paths from the project root (found from the
  script's own location), not from the current directory,
- build outputs in a temporary directory and move them into place only after
  every automatic check has passed, so a failed run never leaves files that
  look finished,
- refuse to overwrite existing outputs unless given `--force`,
- support `--dry-run`, which prints what it would do and writes nothing,
- check its tools at start and fail with a clear message when one is missing,
- stop at the first error (`set -eu` in shell, no silenced exceptions in Python)
  and exit non-zero,
- check every success criterion it can check automatically after producing
  the output, and report each one as passed, failed or not checkable; a check
  that cannot read its value (the tool crashed, the output is empty) counts as
  failed,
- print a short summary at the end: files created, checks and their results.

Keep it small and readable. The person approving it should be able to follow it.

## 6. Test before saving

1. Run `--dry-run` and show the output.
2. Run it on a copy of real inputs in a scratch directory, never in place.
3. Compare the result with the approved criteria, including the ones the
   script cannot check by itself (look at the files).
4. Make the checks fail on purpose at least once (for example with a stand-in
   tool that skips a step) and confirm that the script reports the failure,
   exits non-zero and leaves no outputs behind. Never replace or edit the real
   tools to do this; put a stand-in first on `PATH` in the scratch directory.
5. Show the person the result and the check summary, and ask for approval.

If anything looks wrong or you are not sure, stop and ask. Do not fix it
quietly and report success.

## 7. Save and register

After approval:

1. Save the script in the scope's `scripts/` folder and make it executable.
2. Add an entry to `REGISTRY.md` in the same folder (create it if missing):

   ```
   ## <script-name>
   - Use for: <the routine, in the words the person uses>
   - Run: <exact command with arguments>
   - Inputs / outputs: <short>
   - Success criteria: <approved list>
   - Tools: <tool and version used when tested>
   - Created: <YYYY-MM-DD>, approved by the user
   ```

3. Make sure the instruction file from step 1 contains this block once (add it
   if it is missing, do not duplicate it):

   ```
   ## Scripts for repeated routines
   Before doing a routine by hand, check <path>/REGISTRY.md. If a script covers
   it, run that script instead of repeating the steps. After it runs, check its
   summary against the success criteria in the registry. If a check fails, the
   script errors, or you are not sure the result is right, stop and ask the
   user; do not fix the output by hand or fall back to the manual steps without
   saying so.
   ```

   For the global scope, show the change to the global instruction file and ask
   before writing it.

Finish with one line per script: name, where it is saved, the command to run.

## Out of scope

Checking whether saved scripts still fit their project (tools updated, formats
changed, project moved on) belongs to a separate skill. Do not repair or delete
existing scripts here unless the person asks. The registry entry, with its date,
tool versions and criteria, is what that check will rely on, so keep it accurate.
