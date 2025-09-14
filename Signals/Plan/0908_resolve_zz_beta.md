1. Calendar-Based Lag Misalignment (CRITICAL)



- Stata: l.MarketCapitalization = 1 calendar month ago (gaps → NaN)

- Python: shift(1) = previous row (gaps → wrong month's data)

- Impact: Corrupts all market and stock-level lag operations throughout pipeline

- Fix: Use fill_date_gaps() before lag operations



2. Model Coefficient Merge Conflict (HIGH)



# Line 137-141: Illiquidity coefficients stored as _b_cons, _b_templ1, _b_templ2

# Line 181-185: Return coefficients merge creates _b_cons_ret but overwrites _b_cons

# Line 228: Keeps wrong _b_cons (from return model, not illiquidity model)

- Impact: Stock illiquidity innovations use wrong coefficients

- Fix: Proper coefficient column management with unique names



3. Missing Value Handling Differences (HIGH)



# Filtering without explicit NaN handling

market_subset = df[(df['prc'].abs() > 5) & (df['prc'].abs() < 1000)]

- Stata: Missing values auto-excluded from boolean operations

- Python: NaN propagation in boolean logic may behave differently

- Impact: Different market subset → different market aggregations → different coefficients

- Fix: Explicit dropna() before filtering operations



4. Market Return Reweighting (MEDIUM)



'rM': (x['vwretd'] * x['mktcap']).sum() / x['mktcap'].sum()

- Issue: Reweighting already market-cap-weighted vwretd by filtered subset's market caps

- Impact: Market return innovations differ from expected values

- Assessment: Uncertain if this differs from Stata's weighted collapse



5. Time Period Conversion (LOW-MEDIUM)



daily_crsp['time_avail_m'] = daily_crsp['time_d'].dt.to_period('M').dt.start_time

- Stata: mofd(time_d) may handle month boundaries differently

- Impact: Potential misalignment in monthly aggregations

- Assessment: Less likely but possible edge case differences



6. Rolling Window Implementation (LOW)



- Python asrol() function vs Stata asreg/asrol with window(time 60) min(24)

- Assessment: Implementation appears correct but timing alignment depends on #1



Priority Order for Investigation:



1. FIRST: Implement fill_date_gaps() - likely fixes 80%+ of differences

2. SECOND: Fix coefficient merge conflict - ensures correct model coefficients

3. THIRD: Add explicit missing value handling in filtering operations

4. FOURTH: Investigate market return aggregation logic

5. FIFTH: Verify time period conversion alignment