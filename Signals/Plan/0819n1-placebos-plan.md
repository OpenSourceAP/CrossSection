# Plan: Translating `Placebos/` from Stata to Python

## Context

**Read first:**

* `DocsForClaude/leg4-Placebos.md` (overview & definitions)
* `DocsForClaude/traps.md` (gotchas when translating)
* `CLAUDE.md` (project-wide rules; run everything from `Signals/pyCode/`, use `pyCode/.venv`, keep 1:1 filenames, no placeholder data, no speculation; prefer targeted debugging and bisection)

**Working dirs** (from `CLAUDE.md`):

* Stata sources: `Signals/Code/Placebos/`
* Stata outputs: `Signals/Data/Placebos/`
* Python code: `Signals/pyCode/Placebos/` (this is the working directory for scripts)
* Python data: `Signals/pyData/Placebos/`
* Logs: `Signals/Logs/`
* Planning docs: `Signals/Plan/`

## Mission

Translate every Stata `.do` in `Code/Placebos/` into an equivalent Python script in `pyCode/Placebos/`, validate outputs against the Stata results, and wire them into the project’s test + run pipelines.

---

## Step 0 — Environment Checklist

* [ ] `Signals/pyCode/.venv` exists and is active
* [ ] `requirements.txt` installed
* [ ] Paths in `~/.claude/openap-instructions.md` resolve to `Signals/` root
* [ ] Stata outputs for placebos exist (or a path to produce them exists)

---

## Step 1 — First‑Pass Translation (per file)

For each placebo, perform **this exact checklist**:

* [ ] Read the `.do` in `Code/Placebos/`
* [ ] Identify inputs (tables, required columns, join keys, filters) and outputs (schema, file name)
* [ ] Understand Stata‑specific constructs (lags `l.`, leads `f.`, `tsfill`, by‑sort behavior, `egen`, `xtset` panel semantics)
* [ ] If there is a Stata-equivalent function within @pyCode/utils for a stata function, use that
* [ ] Decide Python primitives (groupby+merge\_asof, resampling, categorical handling, missing value policy, sort keys)
* [ ] Port the code line‑for‑line, keeping operations stable & explicit
* [ ] Save outputs to `../pyData/Placebos/` with the exact expected filename(s)

---

## Step 2 — Validation Harness

**Goal:** Compare Python outputs to Stata outputs at both schema and value levels.

**Artifacts:**

* `pyCode/utils/test_placebos.py` (mirrors predictors test tool)

  * CLI: `python3 utils/test_placebos.py --placebos <name1 name2 ...>`

**Claude tasks:**

* [ ] If Stata outputs exist, locate them in `Data/Placebos/` (or the definitive location) for side‑by‑side testing
* [ ] Implement tester + diff reporter

---

## Step 3 — Bisection & Debugging Loop

When diffs are detected:

* [ ] Pick a single `(permno, yyyymm)` that differs
* [ ] Trace every upstream operation changing that row in both implementations
* [ ] Confirm Stata semantics for time operations (calendar vs positional)
* [ ] Inspect merges (`merge 1:1`, `m:1`, `1:m`) → choose the exact pandas equivalent
* [ ] Never “patch” by adding rows; keep investigating until root cause is known
* [ ] Document the root cause + fix in `Journal/<date>_placebo_<name>_debug.md`

---

## Work Tracker (live‑updated by Claude)

> Claude maintains this; rows are auto‑generated in **Step 1**.

| Placebo | Py Script | Status | Parity | Last Run | Open Issues |
| ------- | --------- | ------ | ------ | -------- | ----------- |
| (auto)  | (auto)    | todo   | —      | —        | —           |

---

## Daily Cadence (Claude’s loop)

* Run first passes on all placebos
* When on validation stage, run **Step 2 → Step 3**
* If diffs: go to **Step 3**; otherwise, mark `green`
* Write `Journal/<date>_standup.md` with current session's progress, blockers

---

## Definition of Done

* All `.do` files have 1:1 Python equivalents with green validation
* Tests can run any subset via CLI
* Schemas, filenames, and CLI flags are documented and stable
* `DocsForClaude/leg4-Placebos.md` updated with any discovered traps & exact semantics
