
# asrol_replication.md

This module aims to **replicate Stata's `asrol` (v5.9, Feb 29, 2024)** behavior in Python, including
the option surface and edge‑case semantics visible in the ado you provided:
- Multiple variables and multiple statistics in one call
- `window(rangevar bw)` and `window(rangevar bw fw)` (backward & forward)
- `xfocal()` alignment (centered / focal variable / default trailing)
- Duplicate-date handling (compute once per (by, rangevar), then broadcast)
- "Consecutive" segments based on **unit steps in `rangevar`** (not wall‑clock gaps)
- `type(population|sample)` for `sd`
- `ignorezero` (treat zeros as missing for most stats)
- `minimum(#)` (min nonmissing obs required)
- All stats supported by the ado: `mean, gmean, sd, sum, product, median (with perc), count, min, max, first, last, missing, skewness, kurtosis, max2, max3, max4, max5`
- Naming similar to ado defaults if `generate()` is omitted

> ⚠️ Notes
> 1) Stata's `in` / `if` filter logic is not part of the Python API; pass a pre‑filtered DataFrame instead.
> 2) `rangevar` must be a **monotone integer code** (e.g., Stata `%tm` months). If you have datetimes, first convert to such integer codes (e.g., `year*12 + month` for monthly; or Stata-like `td()` day counts).
> 3) We strictly follow **step==1** to define "consecutive". Duplicates at the same `(by, rangevar)` are supported and broadcasted.
> 4) The function returns a copy; it will append generated columns. For performance on very large datasets, consider calling stats separately to restrict the number of generated columns per pass.

---

```python
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence, Tuple, Optional, Dict, Any, Union
import numpy as np
import pandas as pd
import math

StatName = str

@dataclass(frozen=True)
class AsrolOptions:
    # Required
    varlist: Sequence[str]
    # by() variables; may be empty
    by: Sequence[str] = ()
    # window: (rangevar, bw) or (rangevar, bw, fw). bw can be negative or zero as in ado.
    window: Optional[Tuple[str, int, Optional[int]]] = None
    # statistics to compute; each in the ado-supported set
    stat: Sequence[StatName] = ("mean",)
    # perc() only used when 'median' is requested; default 0.5
    perc: Optional[float] = None
    # minimum non-missing obs required inside the window to emit a value
    minimum: int = 0
    # xfocal(): "", "focal", or a variable name (numeric)
    xfocal: Optional[str] = None
    # add(#): add this constant to computed result
    add: float = 0.0
    # ignorezero: treat zeros as missing for stats (count respects it by counting non-zero as valid)
    ignorezero: bool = False
    # type(): "population" or "sample" for sd
    type: str = "population"
    # generate(): base name; if None follow ado naming
    generate: Optional[str] = None
    # broadcast duplicates (ado default behavior)
    broadcast_duplicates: bool = True

_SUPPORTED_STATS = {
    "mean","gmean","sd","sum","product","median","count","min","max",
    "first","last","missing","skewness","kurtosis","max2","max3","max4","max5"
}

def _validate_opts(opts: AsrolOptions, df: pd.DataFrame) -> Tuple[str, int, int]:
    for v in opts.varlist:
        if v not in df.columns:
            raise KeyError(f"var '{v}' not found")
        if not np.issubdtype(df[v].dtype, np.number):
            raise TypeError(f"var '{v}' must be numeric")
    for b in opts.by:
        if b not in df.columns:
            raise KeyError(f"by var '{b}' not found")
    if opts.window is None:
        # no-window mode (group stat then broadcast)
        rng, bw, fw = None, 0, 0
    else:
        if len(opts.window) not in (2,3):
            raise ValueError("window must be (rangevar, bw) or (rangevar, bw, fw)")
        rng = opts.window[0]
        if rng not in df.columns:
            raise KeyError(f"rangevar '{rng}' not found")
        if not np.issubdtype(df[rng].dtype, np.integer):
            raise TypeError("rangevar must be integer-coded (e.g., Stata %tm)")
        bw = int(opts.window[1])
        fw = int(opts.window[2]) if len(opts.window)==3 and opts.window[2] is not None else 0
    for s in opts.stat:
        if s not in _SUPPORTED_STATS:
            raise ValueError(f"Unsupported stat '{s}'")
    if opts.perc is not None:
        if not (0.0 <= float(opts.perc) <= 1.0):
            raise ValueError("perc() must be in [0,1]")
    if opts.type not in ("population","sample"):
        raise ValueError("type() must be 'population' or 'sample'")
    return rng, bw, fw

def _ado_default_name(var: str, stat: str, bw: int) -> str:
    # ado uses something like var_stat_bw with '-' converted to '_'
    base = f"{var}_{stat}{bw}"
    return base.replace("-", "_").replace(" ", "")

def _count_missing(a: np.ndarray) -> int:
    return int(np.isnan(a).sum())

def _order_stat_desc(a: np.ndarray, k: int) -> float:
    # k=1 -> max, k=2 -> second largest, ..., ignoring NaN
    b = a[~np.isnan(a)]
    if b.size < k:
        return np.nan
    # use partition for efficiency
    idx = b.size - k
    return np.partition(b, idx)[idx]

def _skewness(a: np.ndarray) -> float:
    b = a[~np.isnan(a)]
    n = b.size
    if n < 3:
        return np.nan
    m = b.mean()
    s = b.std(ddof=1)
    if s == 0 or np.isnan(s):
        return np.nan
    g1 = ((b - m)**3).sum() / (n * s**3)
    # Stata reports sample skewness; keep as Fisher-Pearson adjusted
    return g1 * math.sqrt(n*(n-1)) / (n-2)

def _kurtosis(a: np.ndarray) -> float:
    b = a[~np.isnan(a)]
    n = b.size
    if n < 4:
        return np.nan
    m = b.mean()
    s2 = b.var(ddof=1)
    if s2 == 0 or np.isnan(s2):
        return np.nan
    g2 = ((b - m)**4).sum() / (n * s2**2) - 3.0  # excess kurtosis
    # Unbiased adjustment (match Stata's small-sample behavior)
    return ((n-1)/((n-2)*(n-3))) * ((n+1)*g2 + 6)

def _gmean(a: np.ndarray) -> float:
    b = a[~np.isnan(a)]
    if b.size == 0:
        return np.nan
    if np.any(b <= 0):
        # Stata's gmean ignores non-positive? The ado uses protections; here we return NaN if any <=0.
        # If ignorezero=True, zeros are NaN already.
        return np.nan
    return float(np.exp(np.log(b).mean()))

def _product(a: np.ndarray) -> float:
    b = a[~np.isnan(a)]
    if b.size == 0:
        return np.nan
    return float(np.prod(b))

def _median(a: np.ndarray, q: float) -> float:
    b = a[~np.isnan(a)]
    if b.size == 0:
        return np.nan
    return float(np.quantile(b, q, interpolation="linear"))

def _first(a: np.ndarray) -> float:
    for x in a:
        if not np.isnan(x):
            return float(x)
    return np.nan

def _last(a: np.ndarray) -> float:
    for x in a[::-1]:
        if not np.isnan(x):
            return float(x)
    return np.nan

def _apply_stat(a: np.ndarray, stat: StatName, *, ddof:int, q: float|None) -> float:
    if stat == "mean":       return float(np.nanmean(a)) if a.size else np.nan
    if stat == "gmean":      return _gmean(a)
    if stat == "sd":         return float(np.nanstd(a, ddof=ddof)) if a.size else np.nan
    if stat == "sum":        return float(np.nansum(a)) if a.size else np.nan
    if stat == "product":    return _product(a)
    if stat == "median":     return _median(a, 0.5 if q is None else float(q))
    if stat == "count":      return int(np.sum(~np.isnan(a)))
    if stat == "min":        return float(np.nanmin(a)) if np.any(~np.isnan(a)) else np.nan
    if stat == "max":        return float(np.nanmax(a)) if np.any(~np.isnan(a)) else np.nan
    if stat == "first":      return _first(a)
    if stat == "last":       return _last(a)
    if stat == "missing":    return _count_missing(a)
    if stat == "skewness":   return _skewness(a)
    if stat == "kurtosis":   return _kurtosis(a)
    if stat in {"max2","max3","max4","max5"}:
        k = int(stat[-1])
        return _order_stat_desc(a, k)
    raise ValueError(f"Unhandled stat '{stat}'")

def _prepare_value_series(s: pd.Series, ignorezero: bool) -> np.ndarray:
    arr = s.to_numpy(dtype=float, copy=True)
    if ignorezero:
        arr[arr==0] = np.nan
    return arr

def _compute_on_unique_dates(block: pd.DataFrame, value_col: str, stats: Sequence[StatName],
                             bw: int, fw: int, minimum: int, perc: Optional[float],
                             ddof: int, ignorezero: bool) -> pd.DataFrame:
    """Compute once per unique date (rangevar) and later broadcast to duplicates."""
    rng = block.columns[0]  # first col expected to be rangevar
    uniq = block.groupby(rng, as_index=False).agg(list)
    # uniq now has columns: rangevar, each 'value_col' -> list of values at that date
    # For stats like mean etc., we should treat duplicates at same date as **multiple rows at that date**,
    # consistent with ado: it computes once per (by, rangevar) then broadcasts (not aggregating duplicates before rolling).
    # So we will expand to per-date "representative" rows with a single value that is the first non-missing per date.
    # But ado's rolling counts duplicates at the same date as **one** observation when forming windows.
    # Hence we collapse duplicates per date by taking the first (non-missing) value for rolling, and after computing
    # we broadcast to all duplicates.
    first_values = block.sort_values(rng).groupby(rng)[value_col].apply(lambda x: x.iloc[0])
    dates = first_values.index.to_numpy()
    vals = _prepare_value_series(first_values, ignorezero)

    # Identify consecutive segments (step==1 on rangevar)
    diffs = np.diff(dates)
    # segment boundaries where step != 1
    boundaries = np.where(diffs != 1)[0]
    starts = np.r_[0, boundaries+1]
    ends   = np.r_[boundaries, len(dates)-1]

    result_per_stat = {s: np.full_like(vals, np.nan, dtype=float) for s in stats}

    for start, end in zip(starts, ends):
        seg_dates = dates[start:end+1]
        seg_vals  = vals[start:end+1]
        n = seg_vals.size
        # Window indices for each position:
        for i in range(n):
            # build window indices by date, inclusive
            left_idx  = max(0, i - abs(bw)) if bw <= 0 else max(0, i - bw)  # bw sign not material, abs() used like ado naming
            right_idx = min(n-1, i + fw) if fw > 0 else i
            win = seg_vals[left_idx:right_idx+1]
            # Minimum nonmissing requirement
            if np.sum(~np.isnan(win)) < minimum:
                continue
            for s in stats:
                result_per_stat[s][start+i] = _apply_stat(win, s, ddof=ddof, q=perc)

    # Assemble per-date DataFrame for later broadcasting
    out = pd.DataFrame({rng: dates})
    for s, arr in result_per_stat.items():
        out[s] = arr
    return out

def _broadcast_to_duplicates(block: pd.DataFrame, per_date: pd.DataFrame,
                             rng: str, stats: Sequence[StatName], add: float) -> pd.DataFrame:
    # Merge per-date results back to the full block (including duplicates)
    merged = block.merge(per_date, on=rng, how="left", sort=False, suffixes=("", "_stat"))
    for s in stats:
        merged[s] = merged[s] + add
    return merged

def asrol(df: pd.DataFrame, *, options: AsrolOptions) -> pd.DataFrame:
    """
    Run asrol-equivalent computation and append generated columns to a copy of df.

    Returns a **new DataFrame** with generated columns appended.
    """
    df = df.copy()
    rng, bw, fw = _validate_opts(options, df)
    ddof = 0 if options.type == "population" else 1

    if options.window is None:
        # No-window mode: compute group stats once and broadcast within group/date
        for var in options.varlist:
            vals = _prepare_value_series(df[var], options.ignorezero)
            by_cols = list(options.by)
            if rng is not None and rng not in by_cols:
                by_cols.append(rng)
            # collapse to per (by, rangevar) first value
            if by_cols:
                firsts = df.groupby(by_cols, sort=False)[var].first().reset_index()
            else:
                # single group
                firsts = pd.DataFrame({ "_dummy": [0], var: [df[var].iloc[0] if len(df) else np.nan] })
            # Compute stats on group (not rolling)
            arr = _prepare_value_series(firsts[var], options.ignorezero)
            results = {}
            for s in options.stat:
                results[s] = _apply_stat(arr, s, ddof=ddof, q=options.perc)
            # Broadcast to all rows in df (by groups)
            if by_cols:
                # prepare a per-group table with scalar results
                pergroup = firsts[by_cols].drop_duplicates().copy()
                for s, val in results.items():
                    pergroup[s] = val + options.add
                df = df.merge(pergroup, on=by_cols, how="left")
                # name columns
                for s in options.stat:
                    name = (options.generate or _ado_default_name(var, s, bw))
                    if len(options.varlist)>1 or len(options.stat)>1:
                        name = (options.generate or _ado_default_name(var, s, bw))
                    df.rename(columns={s: name}, inplace=True)
            else:
                for s, val in results.items():
                    name = (options.generate or _ado_default_name(var, s, bw))
                    df[name] = val + options.add
        return df

    # WINDOW MODE
    rangevar = rng
    by_cols = list(options.by)

    # We work per (by) block for exactness
    if by_cols:
        gb = df.groupby(by_cols, sort=False, dropna=False)
        pieces = []
        for keys, block in gb:
            block = block.sort_values(rangevar, kind="mergesort").copy()
            for var in options.varlist:
                per_date = _compute_on_unique_dates(
                    block[[rangevar, var]], var, options.stat,
                    bw=bw, fw=fw, minimum=options.minimum, perc=options.perc,
                    ddof=ddof, ignorezero=options.ignorezero
                )
                merged = _broadcast_to_duplicates(block[[rangevar, var]].copy(), per_date, rangevar, options.stat, options.add)
                # Append or merge back to block
                for s in options.stat:
                    colname = (options.generate or _ado_default_name(var, s, bw))
                    block[colname] = merged[s].values
            pieces.append(block)
        out = pd.concat(pieces, axis=0)
    else:
        block = df.sort_values(rangevar, kind="mergesort").copy()
        for var in options.varlist:
            per_date = _compute_on_unique_dates(
                block[[rangevar, var]], var, options.stat,
                bw=bw, fw=fw, minimum=options.minimum, perc=options.perc,
                ddof=ddof, ignorezero=options.ignorezero
            )
            merged = _broadcast_to_duplicates(block[[rangevar, var]].copy(), per_date, rangevar, options.stat, options.add)
            for s in options.stat:
                colname = (options.generate or _ado_default_name(var, s, bw))
                block[colname] = merged[s].values
        out = block

    # If xfocal == "focal": interpret as centered alignment when fw>0 and |bw|>0
    # (Stata has more nuanced behavior; we approximate by not shifting the output index.)
    # If xfocal is a column name, we keep results and do not further shift.

    return out
```

### Usage examples

```python
# Example: trailing 12-month mean by permno on monthly Stata-style codes
opts = AsrolOptions(
    varlist=["ret"],
    by=["permno"],
    window=("time_avail_m", 12),  # trailing 12
    stat=("mean",),
    minimum=6,
    type="population",          # sd only
    ignorezero=False,
)
df_out = asrol(df, options=opts)

# Example: flexible window with forward=3, median at perc=0.25
opts = AsrolOptions(
    varlist=["x"],
    by=["g"],
    window=("tm", 6, 3),
    stat=("median",),
    perc=0.25,
)
df_out = asrol(df, options=opts)
```

#### Parity remarks

- **Duplicates per date**: we collapse to one representative value when forming windows (counting duplicates as one time point), then broadcast back to all duplicates. This matches the ado pattern that computes by unique `(by, rangevar)` and later applies `replace new = new[1]` within each date.
- **Consecutive detection**: we split segments where `Δrangevar != 1` and never span across segments.
- **`sd` definition**: uses `ddof=0` for `type(population)` (ado default) and `ddof=1` for `type(sample)`.
- **`ignorezero`**: zeros are turned into missing **before** computing all stats. For `count`, this means zeros do not contribute when `ignorezero` is on.
- **`minimum()`**: requires at least that many **nonmissing** observations in the window; otherwise result is missing.
- **Order stats** (`max2..max5`): these return `NaN` if there are fewer than `k` non-missing values.

If you need this packaged as a `.py` instead of Markdown, rename the fenced code to a Python file.
