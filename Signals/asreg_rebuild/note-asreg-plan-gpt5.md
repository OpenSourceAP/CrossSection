# === First draft of plan ===

Great—let’s blueprint this before touching code. Below is a concrete plan that (1) adds an `asreg` function that mirrors Stata’s `asreg` behavior and (2) makes the whole module faster, especially for rolling/overlapping windows.

# What we’ll add and why

## 1) New public API: `asreg(...)`

**Goal:** rolling/expanding OLS like Stata’s `asreg`, optionally by panel groups, aligned to a time index, returning per‑period coefficients (and optionally standard errors and fit stats).

**Proposed signature (Pythonic, but Stata‑familiar):**

```python
def asreg(
    df: pd.DataFrame,
    y: str,
    X: list[str] | str,              # list of RHS columns or a wildcard/prefix helper we’ll resolve to columns
    *,
    by: list[str] | str | None = None,  # panel keys, e.g. ['permno']
    time: str | None = None,            # time column (required for rolling)
    window: int | str = 60,             # e.g. 60 rows or '12m' if we later support true time spans
    min_obs: int = 10,                   # minimum rows needed to produce output
    expanding: bool = False,            # if True, window grows from first obs; else fixed-size rolling
    align: str = "right",               # 'right' (Stata-like), 'center', or 'left'
    add_constant: bool = True,
    drop_collinear: bool = True,        # Stata-like handling within each window
    collinear_policy: str = "nan",      # 'nan' (mark window output missing), 'drop' (per-window drop), or 'zero'
    stats: tuple[str, ...] = ("coef",), # choose any of: 'coef', 'se', 't', 'r2', 'nobs', 'sigma'
    robust_se: str | None = None,       # e.g. 'HC1' (optional; slower)
    engine: str = "numba",              # 'numba' (fast rolling updates) or 'numpy_cumsum' (simple, small p)
    parallel: bool = True,              # parallelize across groups
    method: str = "auto",               # 'auto' tries cholesky->qr->lstsq per window
    rtol: float | None = None,          # rank tolerance (Stata-like)
) -> pd.DataFrame
```

**Outputs (wide, Stata-esque column names):**

* `_Nobs`, `_R2`, `_adjR2`, `_sigma` (optional)
* For each regressor `a_3`, `a_5`, …: `_b_a_3`, `_se_a_3`, `_t_a_3` (depending on `stats`)
* `_b_cons`, `_se_cons`, `_t_cons` if `add_constant=True`

**Behavioral notes (to mimic Stata):**

* Sort by `by + time`. Missing in `y`/`X` rows are excluded from the estimation window (listwise within window).
* Rolling window is **right-aligned** by default (last `window` observations up to the current row) — matches `asreg, window(timevar 60)`.
* If `nobs < min_obs` or the design is rank-deficient and `collinear_policy == 'nan'`, emit `NaN` for that row’s stats (what users typically see in Stata when the window can’t be estimated).
* If `collinear_policy == 'drop'`, we’ll drop collinear RHS *for that window only* (closest to Stata’s internal `rmcoll` behavior) and still return a full set of columns: omitted variables get `NaN` (or `0` if user insists on `'zero'`).
* Optionally compute robust SEs (HC1). This is slower; default off to keep speed.

## 2) Fast rolling-OLS core

`asreg` must avoid per-window `statsmodels` overhead. We’ll implement a **lightweight linear algebra kernel**:

* Maintain **rolling normal equations** per group:

  * $S_{xx} = \sum x_t x_t^\top$, $S_{xy} = \sum x_t y_t$, $S_{yy} = \sum y_t^2$
  * As the window advances, **add** the new row’s outer products, **subtract** the oldest row’s.
  * Solve $\beta = S_{xx}^{-1} S_{xy}$ efficiently.
* Solver strategy per window (`method='auto'`):

  1. Try **Cholesky** on $S_{xx}$ (fast; SPD case).
  2. If Cholesky fails or cond. no. is large, fall back to **QR with column pivoting** (scipy) to detect rank and (optionally) drop collinear RHS deterministically.
  3. Final fallback: `np.linalg.lstsq` (SVD-based), returning rank and residuals.
* Compute SEs and t-stats only if requested (`'se'`/`'t'` in `stats`) to save time.
* Avoid pandas in inner loops: convert group slices to contiguous `float64` arrays once, preallocate outputs, and write in-place.

**Why this is fast:**
We do $O(p^2)$ work per step to update $S_{xx}$ and $S_{xy}$, not $O(pn)$ to refit from scratch. For small–moderate $p$ (typical in finance cross-sections), this is a big win. We also avoid per-window Python/Statsmodels overhead.

## 3) Column selection + dtypes upfront

* Resolve `X` early (support a helper to expand wildcards like `A_*` once).
* Validate all columns are numeric; coerce to `float64`; warn/fail otherwise (mirrors your existing `drop_collinear` checks).
* If `add_constant`, append a constant column **just once** in the numpy matrix we feed the kernel.

## 4) Missing data + window definition

* Build a boolean **row-valid mask** per group from `isfinite(y) & isfinite(X).all(1)`.
* The **index of the rolling window is always in terms of *valid rows*** (like `asreg`), not calendar periods — meaning if some months are missing, the window still has up to `window` valid observations.
* `min_obs` gate checked per window after masking.

## 5) Collinearity handling per window

* If `drop_collinear=True` and rank < p:

  * `'nan'`: mark all outputs for that window NaN (common/simple).
  * `'drop'`: use pivoted QR indices to keep independent columns; fill results for kept ones; set omitted vars to NaN (or `0` if `'zero'`).
* This mirrors the choices you made for `regress`, but **performed window-by-window**.

## 6) Parallelism

* **Parallelize over groups**: each group’s rolling pass is independent. We can use:

  * `numba` with `parallel=True` loops per group (best when groups are many and medium-sized), or
  * `joblib`/`concurrent.futures` to run groups in processes (avoids GIL; simpler to start).
* Guard the crossover: for a single huge group, parallelism doesn’t help much; we’ll switch off or cap workers automatically.

## 7) Output assembly (Stata-like)

* Return a DataFrame with the original index (or `[by, time]` index), plus:

  * `_Nobs`, `_R2`, `_adjR2`, `_sigma` (optional)
  * `_b_<name>`, `_se_<name>`, `_t_<name>` for each regressor and `_cons` if present.
* Keep column order stable and readable (e.g., stats columns grouped).

---

# What we’ll refactor/optimize in the current module (and why)

1. **Extract a light OLS “solve” helper**
   Create a small, dependency-light function used by both `regress` and the new rolling kernel:

```python
_beta, _se, info = solve_ols_from_crossmoments(Sxx, Sxy, Syy, nobs, want_se, method, rtol)
```

* Returns `beta`, optional `se`, and metadata: `rank`, `cond`, `dropped_idx` (if pivoting), `sigma2`, etc.
* **Why:** De-duplicates logic between batch `regress` and rolling `asreg`, and gives us a single place to handle rank/collinearity consistently.

2. **Make `drop_collinear` optionally consume cross-moments**

* Add an internal variant that takes `Sxx` and tolerance to identify rank/kept columns without materializing the window’s full matrix (optional; used when `collinear_policy='drop'`).
* **Why:** Faster and avoids slicing big pandas frames per window.

3. **Speed up `regress` path for big problems**

* If `omit_collinear` is True, keep your QR path; but let `regress` skip statsmodels when possible:

  * Use the same `solve_ols_from_crossmoments` on full-sample $X'X, X'y$ (still return a `ResultsLike` object or a thin dataclass we define).
* **Why:** Minimizes overhead and harmonizes numerics.

4. **Precomputation & memory layout**

* Convert RHS and y to contiguous `np.float64` arrays once.
* Pre-allocate all outputs (dict of arrays) and only wrap as DataFrame at the end.
* **Why:** Removes Python overhead from tight loops.

5. **Optional: robust SEs as a separate pass**

* If `robust_se` requested, compute residuals and sandwich variance using cached $X$ in the window or an efficient streaming update (costly). We’ll warn that robust SEs materially slow `asreg` and recommend turning them off unless necessary.
* **Why:** Keeps the fast path fast.

6. **Deterministic tolerance defaults**

* Mirror your `drop_collinear` tolerance defaults: `eps * max(n, p) * scale` (with scale derived from Cholesky/QR diag magnitude).
* **Why:** Stable, “Stata-like” rank detection.

7. **User-facing ergonomics**

* Add small helpers:

  * `expand_columns(df, pattern_or_list)` to turn `A_*` into ordered column lists (respect original df order).
  * `ensure_sorted(df, by, time)` with explicit raises/warnings.
* **Why:** Cuts down on user errors and keeps behavior predictable.

---

# Edge cases (and our choices)

* **Gaps in time:** window counts valid rows (like `asreg`) rather than calendar span. (We can later add a “true timespan” mode if needed.)
* **All-constant or near-constant windows:** flagged by rank test; respect `collinear_policy`.
* **Group with fewer than `min_obs` anywhere:** output NaNs for that group until enough data accumulates.
* **Huge `p`** (dozens–hundreds): we’ll recommend `engine='numba'` with `'nan'` policy for collinearity to avoid heavy QR in every step; QR fallback kicks in only when needed.

---

# Validation plan

1. **Numerical parity tests** against Stata on a small, reproducible panel:

   * Same `by`, `time`, `window`, `min_obs`, RHS set, and alignment.
   * Compare `_b_*`, `_Nobs`, and `_R2` across many rows.
2. **Performance checks**:

   * Measure wall time with/without robust SEs, different engines, and varying `p` and `window`.
   * Confirm near-linear scaling in `n` for fixed `p` and window via rolling updates.
3. **Stress tests**:

   * Missing data patterns, collinearity injected (e.g., duplicate columns), constant-only windows.

---

# Summary of concrete code changes

* **New:** `asreg(...)` (public), using:

  * **New internal:** `rolling_ols_kernel_numba(...)` and `rolling_ols_kernel_numpy(...)`
  * **New internal:** `solve_ols_from_crossmoments(...)`
  * **New internal:** `expand_columns(...)`, `ensure_sorted(...)`
* **Refactor:** `regress(...)` optionally use `solve_ols_from_crossmoments` to avoid full statsmodels cost when `return_full_coefs` is requested but we don’t need the rich results object.
* **Optional enhancement:** Extend `drop_collinear(...)` to accept cross-moments (or share its tolerance logic with the solver).

If this plan looks right to you, I’ll implement it so you can call:

```python
out = asreg(
    df, y="fRet", X="A_*",
    by="permno", time="time_avail_m",
    window=60, min_obs=24, add_constant=True,
    stats=("coef","t","r2","nobs"),
    collinear_policy="nan",
    engine="numba", parallel=True
)
```

and get Stata‑style rolling outputs at speed.

# === Second draft of plan ===

Got it—let’s trim this to the essentials and keep it fast.

# What we’ll build (lean version)

## New public API

```python
def asreg(
    df: pd.DataFrame,
    y: str,
    X: list[str] | str,          # list or a wildcard/prefix we’ll expand once
    *,
    by: list[str] | str | None = None,
    time: str | None = None,     # required if window/expanding used
    window: int = 60,            # count of valid rows (right‑aligned)
    min_obs: int = 10,           # minimum valid rows to emit estimates
    expanding: bool = False,     # if True: from first obs; else fixed-size rolling
    add_constant: bool = True,
    drop_collinear: bool = True, # per-window check; if rank-deficient → NaNs
    compute_se: bool = False,    # standard OLS SEs (no robust option)
    method: str = "auto",        # solver fallback: cholesky→qr→lstsq
    rtol: float | None = None,   # rank tolerance
) -> pd.DataFrame
```

### Output (Stata‑style, minimal but useful)

* `_Nobs`, `_R2`, `_adjR2`, `_sigma`
* `_b_<var>` (and `_b_cons` if added)
* If `compute_se=True`: `_se_<var>`, `_t_<var>`, `_se_cons`, `_t_cons`

### Behavior (simple + Stata‑like)

* Sort by `[by, time]`.
* Right‑aligned rolling window over **valid rows** (listwise within window).
* If `valid_obs < min_obs` → all outputs for that row are `NaN`.
* If `drop_collinear=True` and rank < p in a window → emit `NaN` for that row (simple, predictable).
* No `align`, no `engine`, no `robust_se`, no per‑window drop lists to manage.

---

# How we’ll make it fast (without extra knobs)

1. **Rolling cross‑moments (single pass per group)**

   * Maintain for current window:

     * $S_{xx}=\sum x x^\top$, $S_{xy}=\sum x y$, $S_{yy}=\sum y^2$, $n=\sum 1$
   * Slide window: add newest row, subtract oldest row (or just add for expanding).
   * Solve $\beta = S_{xx}^{-1} S_{xy}$ each step with a tiny solver.

2. **Tiny solver with smart fallback (shared by `regress` and `asreg`)**

   ```python
   beta, se, meta = solve_ols_from_crossmoments(Sxx, Sxy, Syy, n, compute_se, method, rtol)
   ```

   * Try **Cholesky**; if fails or diag too small → **QR with column pivoting**; final fallback **lstsq** (SVD).
   * Returns `rank`; if `rank < p` and `drop_collinear=True` → mark row `NaN`.

3. **Keep Python overhead out of the loop**

   * Convert group blocks to contiguous `float64` arrays once.
   * Preallocate output arrays and fill in place; wrap as DataFrame at the end.
   * No `statsmodels` in the rolling loop.

4. **Parallel where it’s free**

   * Internally, process different `by` groups in parallel with `concurrent.futures` (no user option; we pick a sensible worker count).
   * Single huge group? We’ll just run single‑threaded—no complexity exposed.

---

# Minimal changes to the current module

1. **Add** `solve_ols_from_crossmoments(...)`

   * Shared numeric core for batch and rolling.
   * Computes `beta`, (optional) SE/t, and `_R2`, `_adjR2`, `_sigma`, `rank`.

2. **Add** helpers

   * `expand_columns(df, X)`: turn `"A_*"` into ordered column list.
   * `ensure_sorted(df, by, time)`: sort & validate monotonic time within group.
   * `build_valid_mask(Y, X)`: listwise validity per row.

3. **Implement** `asreg(...)`

   * Group by `by` (or a single implicit group).
   * For each group: slice arrays, compute masks, walk the series computing/updating $S_{xx},S_{xy},S_{yy},n$.
   * On each step: check `min_obs`; call solver; write outputs; else `NaN`.

4. **(Optional light refactor)** `regress(...)`

   * Keep current API, but allow an internal fast path:

     * compute $X'X, X'y, y'y, n$ once; call `solve_ols_from_crossmoments`.
     * Still return your current `full_coefficients` table for compatibility.

---

# Why this is enough

* Matches the common `asreg` workflow (rolling/expanding OLS by panel & time).
* Keeps API compact and predictable.
* Delivers speed by removing heavy per‑window overhead (no statsmodels, no robust SE).
* Deterministic handling of bad windows (either enough data & full rank → numbers, else → NaN).

If this pared‑down plan looks good, I’ll implement exactly this, keeping the code clean and focused.
