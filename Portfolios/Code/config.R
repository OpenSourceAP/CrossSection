# Run: edit these settings, then run master.R. To check the worker count, run
#   Rscript -e 'source("Portfolios/Code/config.R"); portfolio_n_workers("daily")'
# Inputs: operational choices below; scientific settings stay in SignalDoc.csv.
# Outputs: portfolio_config and portfolio_n_workers(), used by later scripts;
#   no file writes.

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
    max_workers = 3L, # never run more workers than this
    # Ballpark peak RAM of one worker, with headroom. Measured 2026-10-23:
    # daily peaks at 12.4 GiB (3 signals x EW/VW) plus about 2.2 GiB of results
    # kept across 212 signals; monthly peaks at about 2.3 GiB.
    gib_per_worker = c(monthly = 4, daily = 16)
  ),

  daily = list(
    # Minimum stock count applied before saving daily returns. Daily CSVs omit
    # Nlong/Nshort; monthly portfolios retain counts and screen in summaries.
    # 1 matches the baseline; setting this to 20 removes IO_ShortInterest portfolios.
    min_stocks = 1L
  )
)

# Workers = available RAM / RAM per worker, capped by max_workers (at least 1).
portfolio_n_workers <- function(stage, config = portfolio_config,
                                available_gib = ps::ps_system_memory()$avail / 1024^3) {
  gib_per_worker <- config$resources$gib_per_worker[[stage]]
  workers <- as.integer(max(1, min(config$resources$max_workers,
                                   floor(available_gib / gib_per_worker))))
  message(sprintf("[%s] %d workers: %.1f GiB available / %g GiB per worker, max %d",
                  stage, workers, available_gib, gib_per_worker,
                  config$resources$max_workers))
  if (available_gib < gib_per_worker) warning("[", stage, "] even one worker may not fit in RAM")
  workers
}
