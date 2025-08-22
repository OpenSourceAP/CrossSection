# part 1

Here’s the short, precise version—and where Stata documents it.

### What Stata does with a singular $X$

* **Detects perfect collinearity** (including constants, factor levels, interactions, or linear combinations).
* **Omits (does not estimate) the offending RHS terms** and proceeds with the remaining full‑rank set. The output prints notes like `note: x3 omitted because of collinearity.` ([Stata][1])

### Which variable gets omitted?

* Stata’s behavior is **deterministic but not user‑tunable**: it flags enough variables to restore full rank using the same internal logic most official commands use (the `_rmcoll/rmcoll` routine). You don’t choose “drop A instead of B”; Stata decides based on the specific expanded design (after factor‑variable expansion, interactions, empty cells, etc.).&#x20;
* With **factor variables**, Stata omits the **base level** (or a redundant level if you included all levels with a constant). If you request “include all levels” along with a constant, one level will still be omitted to break collinearity. ([Stata][2])
* Since **Stata 11**, variables are **“omitted” (marked with `o.`)** rather than physically dropped from the parameter vector—relevant for programmers parsing results. ([Stata][3])

### How you can see/replicate the decision

* Use **`rmcoll`** (or its programmer prefix `_rmcoll`) on your varlist to see exactly which variables Stata would flag/omit for the *current sample*, with factor‑variable expansion and empty‑cell checks. This mirrors what estimation commands do internally.&#x20;
* Stata’s official **FAQ** shows a quick diagnostic trick: regress the *omitted* variable on the rest to reveal the dependency. ([Stata][4])

### Pointers to documentation

* **`regress` manual:** shows the “omitted because of collinearity” behavior and examples (including interactions and constants). ([Stata][1])
* **FAQ – “Estimation commands and omitted variables”:** how/why Stata omits variables and how to diagnose. ([Stata][4])
* **`rmcoll` manual:** the routine most commands use to identify collinearity, with examples (factor levels, interactions, empty cells).&#x20;
* **FAQ – “Keep all levels of a variable in the model”:** why one level must be omitted with a constant even if you ask for all levels. ([Stata][2])
* **FAQ – “Factor variable support for ado-files” (programmer note):** explains the `o.` omission marker introduced in Stata 11. ([Stata][3])

If you want, I can show a concrete example using your regressors—expand the factor vars, run `_rmcoll`, and list exactly what Stata would omit and why.

[1]: https://www.stata.com/manuals/rregress.pdf?utm_source=chatgpt.com "regress, vce(robust)"
[2]: https://www.stata.com/support/faqs/statistics/keep-all-levels-of-variable/?utm_source=chatgpt.com "FAQ: Keeping all levels of a variable in the model"
[3]: https://www.stata.com/support/faqs/programming/factor-variable-support/?utm_source=chatgpt.com "How do I modify an ado-file created for previous versions of ..."
[4]: https://www.stata.com/support/faqs/statistics/estimation-commands-and-omitted-variables/?utm_source=chatgpt.com "FAQ: Estimation commands and omitted variables"


# part 2

Awesome—here’s a compact, reliable helper that mirrors Stata’s “drop enough RHS columns to restore full rank for the current estimation sample” behavior.

It favors clarity and speed:

* **Fast path:** QR with column pivoting (SciPy/LAPACK).
* **Safe fallback:** a greedy least‑squares method if SciPy isn’t installed.
* **Stata‑like sample handling:** it uses only rows that are finite across `X` (and `y` if provided).
* **Actionable output:** what to keep/drop and why (constant vs. collinear).

```python
import numpy as np
import pandas as pd

def drop_collinear(
    X: pd.DataFrame,
    y: pd.Series | np.ndarray | None = None,
    sample_mask: pd.Series | np.ndarray | None = None,
    *,
    rtol: float | None = None,
    method: str = "qr",          # "qr" (fast, needs SciPy) or "greedy" (no deps)
    scale: bool = True,          # column-normalize for numerics (improves stability)
    return_reduced_X: bool = True
):
    """
    Identify and drop RHS columns that cause rank deficiency (Stata rmcoll-like).

    Parameters
    ----------
    X : DataFrame of numeric regressors (no constant automatically added).
    y : optional response; if given, the estimation sample uses rows finite in both X and y.
    sample_mask : optional boolean array to define the estimation sample explicitly.
                  If provided, it overrides y-based masking and is intersected with X finiteness.
    rtol : optional relative tolerance for rank determination.
           Default: eps * max(n, p) * largest_diag(R) for QR, or eps * max(n, p) * max(singular_value) for greedy.
    method : "qr" uses SciPy's QR with column pivoting (fast & robust). Falls back to "greedy" if SciPy not available.
    scale : if True, columns are L2-normalized before rank tests (recommended).
    return_reduced_X : if True, return X with only kept columns (same row subset).

    Returns
    -------
    keep_cols : list[str] in original order
    drop_cols : list[str] in original order
    reasons   : dict[col -> "constant" | "collinear"]
    X_reduced : DataFrame with kept columns on the estimation sample (only if return_reduced_X=True)

    Notes
    -----
    - This operates on the *current estimation sample* (Stata-like). Rows with any non-finite
      value in the used columns (and optionally y) are excluded.
    - Factor variables / dummies: including a full set of category dummies *plus* a constant will cause
      one dummy to be flagged as collinear (which is expected).
    - If you must preserve certain columns, pass them first in X's column order and use method="greedy",
      which tends to keep earlier independent columns.
    """
    # --- 0) Basic validations ---
    if not isinstance(X, pd.DataFrame):
        raise TypeError("X must be a pandas DataFrame.")
    non_num = [c for c in X.columns if not pd.api.types.is_numeric_dtype(X[c])]
    if non_num:
        raise TypeError(f"All columns must be numeric. Non-numeric columns: {non_num}")

    cols = list(X.columns)

    # --- 1) Build estimation sample mask (Stata does listwise deletion on current sample) ---
    finite_X = np.isfinite(X.to_numpy(dtype=float, copy=False)).all(axis=1)
    if sample_mask is not None:
        mask = np.asarray(sample_mask, dtype=bool) & finite_X
    elif y is not None:
        y_arr = np.asarray(y)
        if y_arr.ndim > 1:
            y_arr = y_arr.squeeze()
        mask = finite_X & np.isfinite(y_arr)
    else:
        mask = finite_X

    Xs = X.loc[mask]
    if Xs.shape[0] == 0:
        raise ValueError("No rows left after applying estimation-sample mask.")

    A = Xs.to_numpy(dtype=float, copy=False)  # n x p

    n, p = A.shape
    if p == 0:
        return [], [], {}, (Xs if return_reduced_X else None)

    # --- 2) Quick constant-column screening (gives clear reasons, also speeds the rank step) ---
    ptp = np.ptp(A, axis=0)  # max-min per column
    is_const = (ptp == 0)
    reasons = {}
    const_idx = np.where(is_const)[0].tolist()
    for j in const_idx:
        reasons[cols[j]] = "constant"

    keep_mask_pre = ~is_const
    cols_pre = [c for k, c in enumerate(cols) if keep_mask_pre[k]]
    A_pre = A[:, keep_mask_pre]
    if A_pre.shape[1] == 0:
        keep_cols = []
        drop_cols = cols[:]  # all constants
        if return_reduced_X:
            return keep_cols, drop_cols, reasons, Xs[keep_cols]
        else:
            return keep_cols, drop_cols, reasons, None

    # Optionally scale columns to unit norm (improves numerical stability of rank tests)
    if scale:
        norms = np.linalg.norm(A_pre, axis=0)
        # Norms should be >0 here (we removed constants), but guard anyway:
        norms[norms == 0] = 1.0
        A_test = A_pre / norms
    else:
        A_test = A_pre

    # --- 3) Rank-revealing step: QR w/ pivoting (fast) or greedy fallback ---
    # Determine tolerance (relative to the largest scale in the factorization)
    eps = np.finfo(A_test.dtype).eps
    if method == "qr":
        try:
            from scipy.linalg import qr as scipy_qr  # noqa
            Q, R, piv = scipy_qr(A_test, mode="economic", pivoting=True)
            diagR = np.abs(np.diag(R))
            # Set default tolerance if not provided
            tol = (rtol if rtol is not None else (eps * max(n, A_test.shape[1]) * diagR.max()))
            rank = int((diagR > tol).sum())
            piv = np.asarray(piv)
            indep_local = piv[:rank].tolist()
            dep_local = piv[rank:].tolist()
        except Exception:
            # SciPy not available or failed: fall back to greedy
            method = "greedy"

    if method == "greedy":
        # Greedy: keep earliest independent columns (in A_pre's order).
        # At each step, test if new col is in span(kept); if yes → dependent.
        tol = (rtol if rtol is not None else (eps * max(n, A_test.shape[1])))
        indep_local = []
        dep_local = []
        for j in range(A_test.shape[1]):
            if not indep_local:
                # If this column has nonzero norm, keep it
                if np.linalg.norm(A_test[:, j]) > tol:
                    indep_local.append(j)
                else:
                    dep_local.append(j)
                continue
            # Project A_test[:, j] onto columns in indep_local, then check residual norm
            Aj = A_test[:, j]
            Akeep = A_test[:, indep_local]
            # Solve least squares Akeep * b ≈ Aj
            b, *_ = np.linalg.lstsq(Akeep, Aj, rcond=None)
            resid = Aj - Akeep @ b
            if np.linalg.norm(resid) > tol:
                indep_local.append(j)
            else:
                dep_local.append(j)

    # indep_local/dep_local are indices in A_pre/cols_pre space; map back to original columns
    keep_cols_preorder = [cols_pre[k] for k in indep_local]
    drop_cols_preorder = [cols_pre[k] for k in dep_local]
    for c in drop_cols_preorder:
        reasons[c] = "collinear"

    # Reconstitute full keep/drop *in original column order*
    keep_set = set(keep_cols_preorder)
    keep_cols = [c for c in cols if (c in keep_set) and (c not in reasons or reasons[c] != "constant")]
    # Everything else is dropped either as constant or collinear
    drop_cols = [c for c in cols if c not in keep_cols]

    if return_reduced_X:
        return keep_cols, drop_cols, reasons, Xs[keep_cols]
    else:
        return keep_cols, drop_cols, reasons, None
```

### Why this design

* **Easy to understand:** clean stages (mask rows → drop constants → rank test → map back to names) with clear reasons.
* **Efficient:** QR with column pivoting (LAPACK) is the standard, numerically stable way to extract an independent set; the greedy path is decent for most sizes when SciPy isn’t present.
* **Stata‑like:** it works on the *current sample* (after listwise deletion), exactly how Stata evaluates collinearity.

### Usage examples

**Basic (X only):**

```python
keep, drop, why, Xr = drop_collinear(df.filter(like="A_"))
print("Kept:", keep)
print("Dropped:", drop)
print("Reasons:", why)        # {"A_17": "collinear", "A_204": "constant", ...}
```

**With y to mirror your regression sample:**

```python
keep, drop, why, Xr = drop_collinear(df.filter(like="A_"), y=df["fRet"])
# Now run your regression on Xr and df.loc[Xr.index, "fRet"]
```

**If you must avoid SciPy:**

```python
keep, drop, why, Xr = drop_collinear(df.filter(like="A_"), y=df["fRet"], method="greedy")
```

**Protect earlier columns (greedy tends to keep earlier independents):**

```python
ordered = ["A_core"] + sorted([c for c in df if c.startswith("A_") and c != "A_core"])
keep, drop, why, Xr = drop_collinear(df[ordered], y=df["fRet"], method="greedy")
```

---

If you want, I can tailor it to your exact pipeline (e.g., add a constant automatically, integrate with `statsmodels`/`linearmodels`, or expose a `force_keep=["A_3", "A_5"]` option).
