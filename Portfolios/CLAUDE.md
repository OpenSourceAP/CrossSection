# CrossSection Portfolios

This project is the second stage of the Open Asset Pricing `CrossSection` repo. The first stage is `Signals`, which creates permno-month level signals for stock returns. This second stage converts those signals into portfolio.

## Folder Structure

Check the user's `~/.claude/CLAUDE.md` for full path of `Portfolios/`
- search for "PORTFOLIOSPATH"
- if "PORTFOLIOSPATH" is not found, ask the user to add it to `~/.claude/CLAUDE.md`

```
Portfolios
├── Code        # R code for portfolio creation
├── pyData      # Portfolios created by `Portfolios/Code/`
                # Be careful not to confuse this with `Signals/pyData/`: that is the signals created by `Signals/Code/`
```
