Edit `Code/config.R`, then run `Rscript Portfolios/Code/master.R` from the project root, or Source the saved `Code/master.R` in RStudio. `here::i_am()` locates the project root from the current working directory. Start R from the project root or one of its subfolders.

`run$daily` and `run$exhibits` default to `TRUE`. Quick runs use `run$quick_signals` and skip exhibits. `paths$output_root` redirects generated data, summaries, exhibits and incidental plot files while keeping upstream inputs in the project; a relative root is resolved against the project root. Leave it `NULL` for normal outputs. Scientific portfolio settings remain in `SignalDoc.csv`. Missing dependencies stop the build without installing packages.

Signal-coverage and stock-correlation exhibits have been retired. Portfolio-return exhibits remain in `21_PredictorExhibits.R`. Shipping excludes retired files and removes stale copies from the target Results folder when the shipping script is run.

`config.R` contains only the editable configuration list. `master.R` sources it followed by `00_SettingsAndTools.R`, which validates settings, initializes paths, and checks dependencies before loading packages.

### Checks

Run `Rscript Portfolios/tests/test_resources.R`. The fixture checks cover configuration validation, dependency checks, output isolation, master startup and shipping exclusions without loading research data.
