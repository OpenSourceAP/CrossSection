# Run: Rscript Portfolios/tests/test_resources.R (from any working directory).
# Inputs: installed R dependencies and portfolio source files; no research data.
# Outputs: assertions and temporary fixtures/logs, deleted on completion.

test_file <- sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE))[1L]
code_dir <- normalizePath(file.path(dirname(test_file), "..", "Code"))
setwd(code_dir)
here::i_am("Portfolios/tests/test_resources.R")
source(file.path(code_dir, "config.R"))

test_resources <- function() {
  temporary <- tempfile("portfolio-tests-")
  dir.create(temporary)
  on.exit(unlink(temporary, recursive = TRUE), add = TRUE)
  original_config <- portfolio_config
  setup_config <- original_config
  setup_config$paths$output_root <- file.path(temporary, "setup")
  setup_config$run$exhibits <- FALSE
  assign("portfolio_config", setup_config, envir = .GlobalEnv)
  on.exit(assign("portfolio_config", original_config, envir = .GlobalEnv), add = TRUE)
  suppressMessages(suppressPackageStartupMessages(
    base::source(file.path(code_dir, "00_SettingsAndTools.R"), local = .GlobalEnv)))
  assign("portfolio_config", original_config, envir = .GlobalEnv)
  config_only <- new.env(parent = baseenv())
  sys.source(file.path(code_dir, "config.R"), envir = config_only)
  stopifnot(identical(ls(config_only), "portfolio_config"))
  expect_error <- function(expression, pattern) {
    message <- tryCatch({ force(expression); NULL }, error = conditionMessage)
    stopifnot(!is.null(message), grepl(pattern, message))
  }
  config <- portfolio_config
  stopifnot(identical(portfolio_validate_config(config), config))
  for (name in c("max_workers", "threads_per_worker")) {
    bad <- config
    bad$resources[[name]] <- 1.5
    expect_error(portfolio_validate_config(bad), name)
  }
  bad <- config
  bad$run$quick <- NA
  expect_error(portfolio_validate_config(bad), "quick")
  bad <- config
  bad$daily$workers <- "four"
  expect_error(portfolio_validate_config(bad), "workers")
  bad <- config
  bad$resources$typo <- 1
  expect_error(portfolio_validate_config(bad), "resources")
  checker <- portfolio_check_dependencies
  checker_env <- new.env(parent = environment(checker))
  checker_env$requireNamespace <- function(package, ...) !package %in% c("ggrepel", "lme4")
  environment(checker) <- checker_env
  expect_error(checker(config), "ggrepel, lme4")
  no_optional <- config
  no_optional$run$daily <- FALSE
  no_optional$run$exhibits <- FALSE
  checker(no_optional)
  paths <- portfolio_paths(config, portfolio_root)
  config$paths$output_root <- file.path(temporary, "isolated")
  isolated <- portfolio_paths(config, portfolio_root)
  stopifnot(identical(paths$pathPredictors, isolated$pathPredictors),
            identical(paths$pathSignalsIntermediate, isolated$pathSignalsIntermediate))
  for (name in c("pathDataIntermediate", "pathDataPortfolios", "pathDataSummary", "pathDataDaily", "pathResults")) {
    stopifnot(startsWith(isolated[[name]], config$paths$output_root))
  }
  config$paths$output_root <- "temp/portfolio-relative-test"
  stopifnot(startsWith(portfolio_paths(config, portfolio_root)$pathResults,
                      file.path(portfolio_root, config$paths$output_root)))

  # Exercise master startup from project folders, stubbing only heavy stages.
  # This checks configuration, legacy paths and exhibit ordering without CRSP.
  original_wd <- getwd()
  on.exit(setwd(original_wd), add = TRUE)
  setwd(temporary)
  expect_error(base::source(file.path(code_dir, "master.R"), local = new.env()),
               "Could not find associated project")
  for (scenario in c("default", "quick", "disabled")) {
    setwd(switch(scenario, default = portfolio_root, quick = code_dir,
                 disabled = dirname(code_dir)))
    quick <- scenario == "quick"
    env <- new.env(parent = globalenv())
    env$seen <- character()
    env$source <- function(file, local = TRUE, ...) {
      name <- basename(file)
      if (name %in% c("config.R", "00_SettingsAndTools.R")) {
        suppressMessages(suppressPackageStartupMessages(base::source(file, local = env)))
        if (name == "config.R") {
          env$portfolio_config$run$quick <- quick
          if (scenario == "disabled") {
            env$portfolio_config$run$daily <- FALSE
            env$portfolio_config$run$exhibits <- FALSE
          }
          env$portfolio_config$paths$output_root <- file.path(temporary, "master-output")
        }
        if (name == "00_SettingsAndTools.R") {
          env$check_crsp_inputs <- function(...) TRUE
          env$check_signal_csvs <- function(...) TRUE
        }
      } else {
        env$seen <- c(env$seen, name)
        stopifnot(startsWith(env$pathDataIntermediate, file.path(temporary, "master-output")))
      }
      invisible(NULL)
    }
    env$check_crsp_inputs <- function(...) TRUE
    env$check_signal_csvs <- function(...) TRUE
    base::source(file.path(code_dir, "master.R"), local = env)
    exhibits <- c("21_PredictorExhibits.R", "31_CheckPredictorsExhibits.R", "41_PlaceboExhibits.R")
    stopifnot(!"12_SignalExhibits.R" %in% env$seen,
              all((exhibits %in% env$seen) == (scenario == "default")),
              ("50_DailyPredictorPorts.R" %in% env$seen) == (scenario != "disabled"))
    if (scenario == "default") stopifnot(match(exhibits[1L], env$seen) < match(exhibits[3L], env$seen))
  }
  setwd(temporary)
  # Load the real settings with isolated outputs, and check incidental plots.
  env$portfolio_config <- portfolio_config
  env$portfolio_config$run$exhibits <- FALSE
  env$portfolio_config$paths$output_root <- file.path(temporary, "settings-output")
  list2env(portfolio_paths(env$portfolio_config, portfolio_root), envir = env)
  env$runexhibits <- FALSE
  old_device <- getOption("device")
  on.exit(options(device = old_device), add = TRUE)
  suppressPackageStartupMessages(base::source(file.path(code_dir, "00_SettingsAndTools.R"), local = env))
  plot(1)
  grDevices::dev.off()
  stopifnot(file.exists(file.path(env$pathResults, "Rplots.pdf")), !file.exists(file.path(temporary, "Rplots.pdf")))

  # Exercise just the shipping results block with fixture files and a stale copy.
  results_source <- file.path(temporary, "shipping-source")
  results_dest <- file.path(temporary, "shipping-dest")
  dir.create(results_source)
  dir.create(results_dest)
  writeLines("retained", file.path(results_source, "fig1Port_jointly.pdf"))
  writeLines("retired", file.path(results_source, "coverage.xlsx"))
  writeLines("stale", file.path(results_dest, "coverage.xlsx"))
  shipping <- readLines(file.path(portfolio_root, "Shipping", "Code", "2_pack_portfolios_and_results.r"))
  block <- shipping[seq.int(match("# ==== RESULTS ====", shipping) + 1L, length(shipping))]
  shipping_env <- list2env(list(pathResults = results_source, dir_results = results_dest))
  eval(parse(text = block), envir = shipping_env)
  stopifnot(identical(list.files(results_dest), "fig1Port_jointly.pdf"))
  message("Portfolio configuration tests passed.")
}

test_resources()
