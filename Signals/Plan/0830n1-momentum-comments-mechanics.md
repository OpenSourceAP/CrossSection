# Plan: Update Momentum Predictor Comments - Computational Mechanics

**Goal:** Update momentum predictor files to have comments that explain the computational mechanics of what each line of code does.

## Momentum Predictors to Update

Based on file analysis, these are the momentum-related predictors:
- Mom12m.py
- Mom6m.py  
- MomRev.py
- IndMom.py
- MomSeason.py
- MomOffSeason.py
- MomVol.py
- LRreversal.py
- IntMom.py
- MomOffSeason06YrPlus.py
- MomOffSeason11YrPlus.py
- MomOffSeason16YrPlus.py

## Comment Update Strategy

### ABOUTME Lines:
Replace translation references with computational descriptions

**Current Pattern:**
```python
# ABOUTME: Translates MomRev predictor from Stata to Python
# ABOUTME: Creates momentum and long-term reversal signal based on 6m and 36m momentum
```

**New Pattern:**
```python
# ABOUTME: Creates binary signal by ranking stocks on 6-month and 36-month momentum, going long high short-term/low long-term momentum stocks
# ABOUTME: Run from pyCode/ directory: python3 Predictors/MomRev.py
```

### Inline Comments:
Add explanations for key computational steps

## MomRev.py Specific Updates

**Line 66-71 Comment:**
```python
# Goes long (MomRev = 1) stocks in top quintile for 6m momentum AND bottom quintile for 36m momentum
# Goes short (MomRev = 0) stocks in bottom quintile for 6m momentum AND top quintile for 36m momentum
df['MomRev'] = np.nan
df.loc[(df['tempMom6'] == 5) & (df['tempMom36'] == 1), 'MomRev'] = 1
df.loc[(df['tempMom6'] == 1) & (df['tempMom36'] == 5), 'MomRev'] = 0
```

**Line 41-42 Comment:**
```python
# Compounds monthly returns over months t-5 to t-1 to create 6-month momentum
df['Mom6m'] = ((1 + df['ret_lag1']) * (1 + df['ret_lag2']) * (1 + df['ret_lag3']) * 
               (1 + df['ret_lag4']) * (1 + df['ret_lag5'])) - 1
```

**Line 48-51 Comment:**
```python
# Compounds monthly returns over months t-36 to t-13 to create long-term momentum
mom36m_product = 1
for i in range(13, 37):
    mom36m_product *= (1 + df[f'ret_lag{i}'])
df['Mom36m'] = mom36m_product - 1
```

**Line 59, 63 Comments:**
```python
# Ranks stocks into quintiles (1-5) within each month based on 6-month momentum
df['tempMom6'] = fastxtile(df, 'Mom6m_clean', by='time_avail_m', n=5)

# Ranks stocks into quintiles (1-5) within each month based on 36-month momentum  
df['tempMom36'] = fastxtile(df, 'Mom36m_clean', by='time_avail_m', n=5)
```

## Implementation Order

Start with these momentum predictors in order:
1. **MomRev.py** - ✅ COMPLETED - has clear long/short logic to explain
2. **Mom12m.py** - ✅ COMPLETED - classic momentum with skip-month
3. **Mom6m.py** - ✅ COMPLETED - simpler 6-month version
4. **LRreversal.py** - ✅ COMPLETED - long-term reversal logic
5. **IndMom.py** - ✅ COMPLETED - industry aggregation mechanics

## Progress Summary

**Completed (5/5):**
- MomRev.py: Updated ABOUTME to describe binary signal logic, added comments explaining long/short assignment rules
- Mom12m.py: Updated ABOUTME to describe 12-month compounding, clarified skip-month logic
- Mom6m.py: Updated ABOUTME to describe 6-month compounding, clarified skip-month logic
- LRreversal.py: Updated ABOUTME to describe long-term reversal calculation over t-36 to t-13
- IndMom.py: Updated ABOUTME to describe industry momentum aggregation, clarified market-cap weighting

## Key Changes Made

**Common Pattern Replacements:**
- ❌ "Translates X.do to create Y predictor" → ✅ "Calculates/Creates [specific computation description]"
- ❌ "Direct line-by-line translation" → ✅ Removed these references entirely
- Added specific explanations of computational mechanics throughout

**Momentum Strategy Mechanics Explained:**
- Return compounding formulas clearly documented
- Lag structures and time windows specified  
- Long/short assignment rules clarified
- Industry grouping and weighting methods detailed

**Next Steps:**
Ready to expand to other predictor categories (value, profitability, investment, etc.) if requested.

Focus on explaining:
- **Return compounding calculations**
- **Lag structures and time windows** 
- **Quintile ranking logic**
- **Long/short assignment rules**
- **Industry grouping methods** (for IndMom)
- **Seasonal filtering** (for seasonal momentum predictors)