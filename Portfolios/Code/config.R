# Run: edit these settings, then run master.R.
# Inputs: operational choices below; scientific settings stay in SignalDoc.csv.
# Outputs: portfolio_config, used by 00_SettingsAndTools.R; no file writes.

portfolio_config <- list(
  signal_source = "Python", # "Python" or legacy "Stata" signals

  paths = list(
    output_root = NULL # NULL uses the project root; set a folder for isolated runs
  ),

  run = list(
    daily = TRUE,
    exhibits = TRUE,
    quick = FALSE, # Quick runs use only quick_signals and skip exhibits
    quick_signals = c("Accruals", "AM"),
    verbose = FALSE
  ),

  resources = list(
    max_workers = 3L,
    memory_budget_gib = NULL, # NULL uses detected available memory
    reserve_gib = 8,
    threads_per_worker = 1L
  ),

  daily = list(
    workers = "auto", # "auto" or an integer, subject to resource limits
    # Minimum stock count applied before saving daily returns. Daily CSVs omit
    # Nlong/Nshort; monthly portfolios retain counts and screen in summaries.
    # 1 matches the baseline; setting this to 20 removes IO_ShortInterest portfolios.
    min_stocks = 1L
  )
)
