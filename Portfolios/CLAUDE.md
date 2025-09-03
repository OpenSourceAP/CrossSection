# CrossSection Portfolios

This project is the second stage of the Open Asset Pricing `CrossSection` repo. The first stage is `Signals`, which creates permno-month level signals for stock returns. This second stage converts those signals into portfolio.

## Folder Structure

All paths here are relative to `PORTFOLIOSPATH`:
- This is the full path to the `Portfolios/` folder
- Check for `PORTFOLIOSPATH` in the user's `~/.claude/CLAUDE.md`
- If `PORTFOLIOSPATH` is not found, ask the user to add it to `~/.claude/CLAUDE.md`

### Main Portfolios Structure

**`PORTFOLIOSPATH/Code/`**
- R code for portfolio creation
- Uses as inputs: either
    - `../Signals/Data/Predictors/*.csv`: old legacy Stata-generated signals
    - `../Signals/pyData/Predictors/*.csv`: new Python-generated signals

**`PORTFOLIOSPATH/Data/`** 
- Intermediate data and portfolios created by `PORTFOLIOSPATH/Code/`
- Note: Don't confuse with `../Signals/Data/` (signals created by `../Signals/Code/`)

### Related External Structure

**`PORTFOLIOSPATH/../Signals/Data/Predictors/`**
- permno-month level signals created by the legacy Stata code in `Signals/Code/`

**`PORTFOLIOSPATH/../Signals/pyData/Predictors/`**
- permno-month level signals created by the new Python code in `Signals/pyCode/`






