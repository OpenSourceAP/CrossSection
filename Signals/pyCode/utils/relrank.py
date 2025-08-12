# ### Usage mapped to your Stata snippets

# **Snippet 1 (industry × month ranks of `mve_c`):**

# ```python
# # Assuming df has columns: permno, time_avail_m, ret, mve_c, sicCRSP, tempFF48
# # and you already created tempFF48 and dropped missing industries:
# df = relrank(df, "mve_c", by=["tempFF48", "time_avail_m"], out="tempRK")
# ```

# **Snippet 2 (monthly ranks for several columns):**

# ```python
# for v in ["SG", "BM", "AOP", "LTG"]:
#     df = relrank(df, v, by="time_avail_m", out=f"rank{v}")
# ```

import pandas as pd

def relrank(df: pd.DataFrame, value_col: str, by, out: str | None = None) -> pd.Series | pd.DataFrame:
    """
    Pandas equivalent of Stata:
        by <byvars>: relrank <value_col>, gen(<out>) ref(<value_col>)

    Behavior:
    - Computes the empirical CDF / relative rank of `value_col` within each group `by`.
    - Ties get the same value (average rank), matching Stata `cumul, equal`.
    - Output is in (0, 1]; singleton groups yield 1.0.
    - Missing values in `value_col` => NaN in the result (Stata sets missing when ref is missing).

    Parameters
    ----------
    df : pd.DataFrame
        Input data.
    value_col : str
        Column to rank; this is both the "value" and the "reference" (ref(value_col)).
    by : str | list[str]
        Grouping columns (Stata's `by:`). Can be a column name or list of names.
    out : str | None, default None
        If provided, writes the result to `df[out]` and returns the DataFrame.
        If None, returns a Series aligned to `df.index`.

    Returns
    -------
    pd.Series | pd.DataFrame
        Series of relative ranks (if out is None) or the mutated DataFrame (if out is a string).

    Notes
    -----
    - This mirrors Stata's `relrank` used as:
        by <byvars>: relrank v, gen(newv) ref(v)
      which internally calls `cumul` with `equal` tie handling.
    - Implementation detail:
        We use pandas' `rank(method="average", pct=True)` within each group.
        See docs:
        * pandas.Series.rank: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.rank.html
        * pandas.GroupBy: https://pandas.pydata.org/pandas-docs/stable/user_guide/groupby.html

    Examples
    --------
    # Stata:
    # by tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
    # Python (pandas):
    # df = relrank(df, "mve_c", by=["tempFF48", "time_avail_m"], out="tempRK")

    # Stata loop:
    # foreach v of varlist SG BM AOP LTG {
    #     by time_avail_m: relrank `v', gen(rank`v') ref(`v')
    # }
    # Python (pandas):
    # for v in ["SG","BM","AOP","LTG"]:
    #     df = relrank(df, v, by="time_avail_m", out=f"rank{v}")
    """
    # Group and compute percentile ranks with average tie handling (Stata: cumul, equal)
    # pct=True returns rank / group_size -> values in (0, 1]
    ranks = (
        df.groupby(by, dropna=False, sort=False)[value_col]
          .rank(method="average", pct=True)
    )

    # pandas already yields NaN for rows where value_col is NaN,
    # which matches Stata relrank setting generated value to missing if ref is missing.
    if out is not None:
        df[out] = ranks
        return df
    return ranks





