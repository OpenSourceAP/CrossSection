Edit `Code/config.R`, then run `Rscript Portfolios/Code/master.R` from the project root, or Source the saved `Code/master.R` in RStudio. `here::i_am()` locates the project root from the current working directory. Start R from the project root or one of its subfolders.

`run$daily` and `run$exhibits` default to `TRUE`. Quick runs use `run$quick_signals` and skip exhibits. `paths$output_root` redirects generated data, summaries, exhibits and incidental plot files while keeping upstream inputs in the project; a relative root is resolved against the project root. Leave it `NULL` for normal outputs. Scientific portfolio settings remain in `SignalDoc.csv`. Missing dependencies stop the build without installing packages.

Signal-coverage and stock-correlation exhibits have been retired. Portfolio-return exhibits remain in `21_PredictorExhibits.R`. Shipping excludes retired files and removes stale copies from the target Results folder when the shipping script is run.

`config.R` contains the editable configuration list and the worker-count formula. `master.R` sources it followed by `00_SettingsAndTools.R`, which validates settings, initializes paths, and checks dependencies before loading packages.

### Parallel workers

`50_DailyPredictorPorts.R` runs its six configurations (baseline, deciles and quintiles, each EW and VW) as independent jobs on parallel workers. Each worker runs one configuration's signals in order, then takes the next configuration. Monthly stages still run serially. The worker count comes from `portfolio_n_workers(stage)` in `config.R`:

$$\text{workers} = \max\left(1, \min\left(\texttt{max\_workers}, \left\lfloor \frac{\text{available RAM}}{\texttt{gib\_per\_worker[stage]}} \right\rfloor\right)\right)$$

Available RAM comes from `ps::ps_system_memory()`. To check the count on this machine, run this from the project root:

```sh
Rscript -e 'source("Portfolios/Code/config.R"); portfolio_n_workers("daily"); portfolio_n_workers("monthly")'
```

Stages run jobs with `portfolio_run_jobs(stage, jobs, run_job, setup, globals)` from `00_SettingsAndTools.R`. Workers are fresh R sessions. `globals` are copied into each worker, `setup()` runs once per worker to load packages and shared data, and `run_job(job)` writes its outputs and returns a small result. Worker output prints to the terminal, interleaved and tagged by job name at start and finish; under RStudio it goes to RStudio's own output, not the console. If a job fails, the remaining jobs still finish and then the stage stops and names the failed jobs. On an error or interrupt, the workers are killed.

`gib_per_worker` holds ballpark estimates, not run-time measurements. On 2026-10-23, a daily worker peaked at 12.4 GiB over 3 signals × EW/VW, and results kept in memory add about 2.2 GiB across 212 signals. The setting is 16 GiB. A monthly worker peaked at about 2.3 GiB, and the setting is 4 GiB. Re-measure these after substantial changes to CRSP or the portfolio code.

### Checks

Run `Rscript Portfolios/tests/test_resources.R`. The fixture checks cover configuration validation, worker-count arithmetic, parallel job scheduling and failure cleanup, dependency checks, output isolation, master startup and shipping exclusions without loading research data.
