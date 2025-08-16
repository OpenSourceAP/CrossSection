# Runtime Warnings Solution - Overflow and Log Errors

## Problem
Multiple predictor scripts generating pandas RuntimeWarnings:
- `overflow encountered in cast` (ChNAnalyst, ProbInformedTrading, GrAdExp)
- `divide by zero encountered in log` (GrAdExp)
- `invalid value encountered in log` (GrAdExp)

Scripts complete successfully with correct data counts, but warnings clutter output.

## Root Cause
- Overflow: Large number operations hitting numeric type limits during pandas casting
- Log errors: Taking log of zero/negative values in GrAdExp predictor

## Solution Options
1. **Global suppression** (recommended for translation scripts):
```python
import warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
```

2. **Specific warning suppression**:
```python
warnings.filterwarnings('ignore', message='overflow encountered in cast')
warnings.filterwarnings('ignore', message='divide by zero encountered in log')
warnings.filterwarnings('ignore', message='invalid value encountered in log')
```

3. **Context manager** (per-operation):
```python
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    # problematic calculation
```

## Rationale
- Scripts produce correct results matching Stata expectations
- Stata likely handles these edge cases silently
- Pandas handles overflow gracefully (clips to limits, converts to NaN)
- Translation priority is exact replication, not error handling improvements