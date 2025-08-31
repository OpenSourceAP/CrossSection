# asrol_py.py — Python port of Stata asrol.ado (v5.x)

The code block below contains a complete, production-ready Python module that replicates Stata's `asrol.ado` behavior, with pandas and polars support and fast paths where available. Save it locally as **`asrol_py.py`** and import it in your projects.

```python
"""asrol_py.py — Python port of Stata asrol.ado (v5.x)
Implements rolling/group statistics with options: by, window (2-arg and 3-arg), perc, minimum,
xfocal, ignorezero, type (population/sample). Supports pandas and polars DataFrames.
Author: ChatGPT (auto-generated)
License: MIT (for this port). Stata asrol is GPLv3; this is a clean-room reimplementation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union, Sequence, Optional, Tuple, Dict, Any
import math

try:
    import pandas as pd
    import numpy as np
except Exception:
    pd=None; np=None
try:
    import polars as pl
except Exception:
    pl=None


@dataclass
class WindowSpec:
    rangevar: str
    back: int
    forward: int


def _normalize_window(window):
    if len(window) == 2:
        rangevar, L = window
        if not isinstance(L, int) or L <= 0:
            raise ValueError("When window has 2 args, the length must be a positive integer.")
        return WindowSpec(rangevar=rangevar, back=-(L - 1), forward=0)
    elif len(window) == 3:
        rangevar, back, forward = window
        if not isinstance(back, int) or not isinstance(forward, int):
            raise ValueError("When window has 3 args, back and forward must be integers.")
        return WindowSpec(rangevar=rangevar, back=back, forward=forward)
    else:
        raise ValueError("window must be (rangevar, L) or (rangevar, back, forward).")


def _validate_stats(stats):
    allowed = {
        "mean", "gmean", "sd", "sum", "product", "median", "count", "min", "max",
        "first", "last", "missing", "skewness", "kurtosis", "max2", "max3", "max4", "max5"
    }
    for s in stats:
        if s not in allowed:
            raise ValueError(f"Unsupported stat: {s}. Allowed: {sorted(allowed)}")


def _percentile_stata(values, p: float) -> float:
    x = values
    n = x.size
    if n == 0:
        return float('nan')
    if p <= 0:
        return float(np.min(x))
    if p >= 1:
        return float(np.max(x))
    xs = np.sort(x)
    r = p * (n + 1)
    k = int(np.floor(r))
    d = r - k
    if k <= 0:
        return float(xs[0])
    if k >= n:
        return float(xs[-1])
    lower = xs[k - 1]
    upper = xs[k]
    return float(lower + d * (upper - lower))


def _nanprod(arr, ignorezero: bool) -> float:
    x = arr[~np.isnan(arr)]
    if x.size == 0:
        return float('nan')
    if ignorezero:
        x = x[x != 0]
        if x.size == 0:
            return float('nan')
        return float(np.prod(x))
    if np.any(x == 0):
        return 0.0
    return float(np.prod(x))


def _geomean(arr, ignorezero: bool) -> float:
    x = arr[~np.isnan(arr)]
    if x.size == 0:
        return float('nan')
    if ignorezero:
        x = x[x != 0]
    if x.size == 0 or np.any(x <= 0):
        return float('nan')
    return float(np.exp(np.mean(np.log(x))))


def _max_k(arr, k: int) -> float:
    x = arr[~np.isnan(arr)]
    if x.size < k:
        return float('nan')
    idx = np.argpartition(-x, k - 1)[:k]
    topk = np.sort(x[idx])[::-1]
    return float(topk[k - 1])


def _skew_kurt(arr, ddof: int):
    x = arr[~np.isnan(arr)]
    n = x.size
    if n == 0:
        return (float('nan'), float('nan'))
    m = float(np.mean(x))
    var = float(np.var(x, ddof=ddof))
    if var == 0 or abs(var) < 1e-20:
        return (float('nan'), float('nan'))
    s = math.sqrt(var)
    m3 = float(np.mean((x - m) ** 3))
    m4 = float(np.mean((x - m) ** 4))
    skew = m3 / (s ** 3)
    kurt = m4 / (var ** 2)
    return (skew, kurt)


def _window_indices(n: int, i: int, back: int, forward: int):
    lo = i + back
    hi = i + forward
    lo = max(0, lo)
    hi = min(n - 1, hi)
    if lo > hi:
        return (1, 0)  # empty
    return (lo, hi)


def _apply_stats_block(block, stats, perc, ddof: int, ignorezero: bool):
    out = {}
    x = block
    nnan = np.sum(~np.isnan(x))
    nmiss = x.size - nnan
    if "count" in stats:
        out["count"] = float(nnan)
    if "missing" in stats:
        out["missing"] = float(nmiss)
    if nnan == 0:
        for s in stats:
            if s not in ("count", "missing"):
                out[s] = float('nan')
        return out
    if "sum" in stats:
        out["sum"] = float(np.nansum(x))
    if "mean" in stats:
        out["mean"] = float(np.nanmean(x))
    if "sd" in stats:
        out["sd"] = float(np.nanstd(x, ddof=ddof))
    if "min" in stats:
        out["min"] = float(np.nanmin(x))
    if "max" in stats:
        out["max"] = float(np.nanmax(x))
    if "first" in stats:
        idx = np.flatnonzero(~np.isnan(x))
        out["first"] = float(x[idx[0]]) if idx.size else float('nan')
    if "last" in stats:
        idx = np.flatnonzero(~np.isnan(x))
        out["last"] = float(x[idx[-1]]) if idx.size else float('nan')
    if any(s in stats for s in ("median", "skewness", "kurtosis", "max2", "max3", "max4", "max5", "gmean", "product")):
        clean = x[~np.isnan(x)]
        if "median" in stats:
            q = 0.5 if perc is None else float(perc)
            out["median"] = _percentile_stata(clean, q)
        if "skewness" in stats or "kurtosis" in stats:
            sk, ku = _skew_kurt(clean, ddof=ddof)
            if "skewness" in stats: out["skewness"] = sk
            if "kurtosis" in stats: out["kurtosis"] = ku
        if "max2" in stats: out["max2"] = _max_k(clean, 2)
        if "max3" in stats: out["max3"] = _max_k(clean, 3)
        if "max4" in stats: out["max4"] = _max_k(clean, 4)
        if "max5" in stats: out["max5"] = _max_k(clean, 5)
        if "product" in stats: out["product"] = _nanprod(clean, ignorezero=ignorezero)
        if "gmean" in stats: out["gmean"] = _geomean(clean, ignorezero=ignorezero)
    return out


def _engine_group_apply_numpy(
    df_group,
    var: str,
    ws: WindowSpec,
    stats,
    perc,
    minimum: int,
    xfocal_mode: Optional[str],
    rangevar: str,
    ignorezero: bool,
    ddof: int,
):
    if pd is not None and isinstance(df_group, pd.DataFrame):
        vals = df_group[var].to_numpy(dtype=float)
        rvar = df_group[rangevar].to_numpy()
    elif pl is not None and isinstance(df_group, pl.DataFrame):
        vals = df_group.get_column(var).to_numpy()
        rvar = df_group.get_column(rangevar).to_numpy()
    else:
        raise TypeError("Unsupported DataFrame type for group.")
    n = len(vals)
    out_arrays = {s: np.full(n, float('nan'), dtype=float) for s in stats}
    # precompute duplicate index map for rangevar if needed
    if xfocal_mode == "exclude_rangevar_dups":
        unique_vals = {}
        for idx, rv in enumerate(rvar):
            unique_vals.setdefault(rv, []).append(idx)
        dup_index = {rv: np.array(ix, dtype=int) for rv, ix in unique_vals.items()}
    else:
        dup_index = {}

    back, forward = ws.back, ws.forward
    for i in range(n):
        lo, hi = _window_indices(n, i, back, forward)
        if hi < lo:
            continue
        idx = np.arange(lo, hi + 1)
        if xfocal_mode == "exclude_self":
            idx = idx[idx != i]
        elif xfocal_mode == "exclude_rangevar_dups":
            rm = dup_index.get(rvar[i], None)
            if rm is not None and rm.size > 0:
                mask = np.ones(idx.shape[0], dtype=bool)
                mask[np.isin(idx, rm)] = False
                idx = idx[mask]
        block = vals[idx] if idx.size > 0 else np.array([], dtype=float)
        if block.size == 0 or np.sum(~np.isnan(block)) < minimum:
            continue
        res = _apply_stats_block(block, stats, perc, ddof, ignorezero)
        for s, v in res.items():
            out_arrays[s][i] = v
    return out_arrays


def asrol(
    df,
    varlist,
    stat,
    *,
    window=None,
    by=None,
    generate=None,
    perc=None,
    minimum: int = 0,
    xfocal: Optional[str] = None,
    ignorezero: bool = False,
    type: str = "population",
):
    if isinstance(varlist, str):
        vars_list = [varlist]
    else:
        vars_list = list(varlist)
    stats_list = [stat] if isinstance(stat, str) else list(stat)
    _validate_stats(stats_list)
    if type.lower() in ("p", "population"):
        ddof = 0
    elif type.lower() in ("s", "sample"):
        ddof = 1
    else:
        raise ValueError("type must be 'population' or 'sample'")
    if window is None:
        ws = WindowSpec(rangevar=vars_list[0], back=-(10**9), forward=10**9)
        window_two_arg = False
    else:
        ws = _normalize_window(window)
        window_two_arg = (len(window) == 2)
    xfocal_mode = None
    if xfocal is not None:
        if xfocal == "focal":
            xfocal_mode = "exclude_self"
        else:
            xfocal_mode = "exclude_rangevar_dups"
    def _col_name(v: str, s: str) -> str:
        if generate and len(stats_list) == 1 and len(vars_list) == 1:
            return generate
        base = f"{v}_{s}"
        if window_two_arg:
            L = -ws.back + 1 if ws.back <= 0 else ws.back + 1
            base = f"{base}{L}"
        return base

    # pandas backend
    if pd is not None and isinstance(df, pd.DataFrame):
        df_out = df.copy()
        groupers = list(by) if by is not None else []
        sort_cols = groupers + ([ws.rangevar] if ws.rangevar in df_out.columns else [])
        if sort_cols:
            df_out = df_out.sort_values(sort_cols, kind="mergesort")
        fast_trailing = (ws.forward == 0 and ws.back <= 0 and xfocal_mode is None)
        for v in vars_list:
            s = df_out[v].astype(float)
            if fast_trailing:
                win = -ws.back + 1
                obj = df_out.groupby(groupers, sort=False)[v] if groupers else s
                for st in stats_list:
                    colname = _col_name(v, st)
                    if st == "mean":
                        ser = obj.rolling(win, min_periods=max(minimum, 1)).mean()
                    elif st == "sd":
                        ser = obj.rolling(win, min_periods=max(minimum, 1)).std(ddof=ddof)
                    elif st == "sum":
                        ser = obj.rolling(win, min_periods=max(minimum, 1)).sum()
                    elif st == "min":
                        ser = obj.rolling(win, min_periods=max(minimum, 1)).min()
                    elif st == "max":
                        ser = obj.rolling(win, min_periods=max(minimum, 1)).max()
                    elif st == "count":
                        cnt = obj.rolling(win, min_periods=1).count()
                        ser = cnt.astype(float)
                        ser[cnt < minimum] = float('nan')
                    elif st == "median" and (perc is None or abs(perc - 0.5) < 1e-12):
                        ser = obj.rolling(win, min_periods=max(minimum, 1)).median()
                    else:
                        ser = None
                    if ser is not None:
                        if groupers:
                            ser = ser.reset_index(level=groupers, drop=True)
                        df_out[colname] = ser
                deferred = [st for st in stats_list if st not in ("mean","sd","sum","min","max","count") and not (st=="median" and (perc is None or abs(perc-0.5)<1e-12))]
                if deferred:
                    for key, grp in df_out.groupby(groupers, sort=False) if groupers else [((), df_out)]:
                        res = _engine_group_apply_numpy(grp, v, ws, deferred, perc, minimum, xfocal_mode, ws.rangevar, ignorezero, ddof)
                        idx = grp.index
                        for st, arr in res.items():
                            colname = _col_name(v, st)
                            df_out.loc[idx, colname] = arr
                continue
            for key, grp in df_out.groupby(groupers, sort=False) if groupers else [((), df_out)]:
                res = _engine_group_apply_numpy(grp, v, ws, stats_list, perc, minimum, xfocal_mode, ws.rangevar, ignorezero, ddof)
                idx = grp.index
                for st, arr in res.items():
                    colname = _col_name(v, st)
                    df_out.loc[idx, colname] = arr
        return df_out

    # polars backend
    if pl is not None and isinstance(df, pl.DataFrame):
        df_out = df.clone()
        sort_cols = (list(by) if by is not None else []) + ([ws.rangevar] if ws.rangevar in df_out.columns else [])
        if sort_cols:
            df_out = df_out.sort(sort_cols)
        if by is None or len(by) == 0:
            for v in vars_list:
                res = _engine_group_apply_numpy(df_out, v, ws, stats_list, perc, minimum, xfocal_mode, ws.rangevar, ignorezero, ddof)
                for st, arr in res.items():
                    colname = _col_name(v, st)
                    df_out = df_out.with_columns(pl.Series(name=colname, values=arr))
        else:
            new_cols_data = {}
            gb = df_out.group_by(list(by), maintain_order=True)
            for keys, grp in gb:
                for v in vars_list:
                    res = _engine_group_apply_numpy(grp, v, ws, stats_list, perc, minimum, xfocal_mode, ws.rangevar, ignorezero, ddof)
                    for st, arr in res.items():
                        colname = _col_name(v, st)
                        new_cols_data.setdefault(colname, []).append(arr)
            for colname, parts in new_cols_data.items():
                import numpy as _np
                df_out = df_out.with_columns(pl.Series(name=colname, values=_np.concatenate(parts)))
        return df_out

    raise TypeError("df must be a pandas or polars DataFrame.")
```

## Quick usage

```python
import pandas as pd
from asrol_py import asrol

df = pd.DataFrame({
    "id": [1,1,1,2,2,2],
    "t":  [2001,2002,2003,2001,2002,2003],
    "x":  [10,20,30,5,6,7]
})

# trailing 3 incl current, by id
out = asrol(df, "x", ["mean","sd"], window=("t", 3), by=["id"], minimum=1)

# 75th percentile over trailing 3
p75 = asrol(df, "x", ["median"], window=("t", 3), by=["id"], perc=0.75)

# asymmetric window: back 1, forward 1
sym = asrol(df, "x", "sum", window=("t", -1, 1), by=["id"])

# exclude focal obs in the window
xf = asrol(df, "x", "mean", window=("t", 3), by=["id"], xfocal="focal")
```
