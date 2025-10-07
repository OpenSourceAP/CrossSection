# Inputs: Signal metadata in `SignalDoc.csv`, predictor CSVs under
#         `Signals/pyData/Predictors/`, CRSP intermediates in
#         `Portfolios/Data/Intermediate/`, and the October 2024 public release
#         folder on Google Drive (`https://drive.google.com/drive/folders/1SSoHGbwgyhRwUCzLE0YWvUlS0DjLCd4k`).
# Outputs: Console comparison plus `Signals/Logs/TestOutPortSelect.md` and
#          `Signals/Logs/TestOutPortSelect.csv` logging t-stats versus the
#          release workbook fetched from Google Drive.
# How to run:
# - `Rscript utils/TestPortSelect.R --predictors ShortInterest`
# - `Rscript utils/TestPortSelect.R ShortInterest OptionVolume1`
# - `Rscript utils/TestPortSelect.R` (defaults to OptionVolume1/OptionVolume2)

args_trailing <- commandArgs(trailingOnly = TRUE)
args_full <- commandArgs(trailingOnly = FALSE)

release_oct2024 <- "https://drive.google.com/drive/folders/1SSoHGbwgyhRwUCzLE0YWvUlS0DjLCd4k"

# Resolve script path to infer project root ----------------------------------
script_path <- ""
file_arg_idx <- grep("^--file=", args_full)
if (length(file_arg_idx) > 0) {
  script_path <- normalizePath(sub("^--file=", "", args_full[file_arg_idx[1]]), mustWork = TRUE)
} else {
  script_path <- normalizePath(getwd(), mustWork = TRUE)
}

project_root <- normalizePath(file.path(dirname(script_path), "..", "..", ".."), mustWork = TRUE)
if (!grepl(paste0(.Platform$file.sep, "$"), project_root)) {
  project_root <- paste0(project_root, .Platform$file.sep)
}

parse_predictor_arg <- function(value) {
  splits <- strsplit(value, ",", fixed = TRUE)[[1]]
  if (length(splits) == 0) {
    return(character(0))
  }
  trimmed <- trimws(splits)
  trimmed[trimmed != ""]
}

target_signals <- character(0)

i <- 1
while (i <= length(args_trailing)) {
  arg <- args_trailing[[i]]
  if (grepl("^--(predictor|predictors|p)=", arg)) {
    pieces <- sub("^--(predictor|predictors|p)=", "", arg)
    target_signals <- c(target_signals, parse_predictor_arg(pieces))
    i <- i + 1
    next
  }
  if (arg %in% c("--predictor", "--predictors", "-p")) {
    if (i == length(args_trailing)) {
      stop("Argument provided to ", arg, " but no predictor names supplied.")
    }
    target_signals <- c(target_signals, parse_predictor_arg(args_trailing[[i + 1]]))
    i <- i + 2
    next
  }
  if (arg %in% c("--project-root", "--path-project")) {
    if (i == length(args_trailing)) {
      stop("Argument provided to ", arg, " but no path supplied.")
    }
    project_root <- normalizePath(args_trailing[[i + 1]], mustWork = TRUE)
    if (!grepl(paste0(.Platform$file.sep, "$"), project_root)) {
      project_root <- paste0(project_root, .Platform$file.sep)
    }
    i <- i + 2
    next
  }
  target_signals <- c(target_signals, parse_predictor_arg(arg))
  i <- i + 1
}

target_signals <- unique(target_signals[target_signals != ""])

# Align with TestPortFocused logic ------------------------------------------
pathProject <- project_root
SignalSource <- "Python"

setwd(file.path(pathProject, "Portfolios", "Code"))

source("00_SettingsAndTools.R", echo = TRUE)
source("01_PortfolioFunction.R", echo = TRUE)

default_quickrun <- c("OptionVolume1", "OptionVolume2")
quickrun <- TRUE
quickrunlist <- if (length(target_signals) == 0) default_quickrun else target_signals
skipdaily <- TRUE
feed.verbose <- FALSE

quickrunlist <- unique(quickrunlist)

missing_in_doc <- setdiff(quickrunlist, alldocumentation$signalname)
if (length(missing_in_doc) > 0) {
  stop("Predictors not found in SignalDoc.csv: ", paste(missing_in_doc, collapse = ", "))
}

suppressPackageStartupMessages(library(fst))
suppressPackageStartupMessages(library(data.table))

crspinfo <- read.fst(paste0(pathProject, "Portfolios/Data/Intermediate/crspminfo.fst")) %>%
  setDT()
crspret <- read.fst(paste0(pathProject, "Portfolios/Data/Intermediate/crspmret.fst")) %>%
  setDT()

strategylist0 <- alldocumentation %>%
  dplyr::filter(Cat.Signal == "Predictor")
strategylist0 <- ifquickrun()

pathPredictors <- paste0(pathProject, "Signals/", signalDataFolder, "/Predictors/")
csvlist <- list.files(pathPredictors) %>%
  tibble::as_tibble() %>%
  dplyr::rename(signalname = value) %>%
  dplyr::mutate(
    signalname = substr(signalname, 1, nchar(signalname) - 4),
    in_csv = 1
  )

missing <- strategylist0 %>%
  dplyr::select(signalname) %>%
  dplyr::left_join(csvlist, by = "signalname") %>%
  dplyr::filter(is.na(in_csv))

if (nrow(missing) > 0) {
  print("Warning: the following predictor signal csvs are missing:")
  print(missing$signalname)
  temp <- readline("press enter to continue, type quit to quit: ")
  if (temp == "quit") {
    print("erroring out")
    stop()
  }
}

port <- loop_over_strategies(strategylist0)

sumnew0 <- checkport(port)

# Download release workbook --------------------------------------------------
reference_path <- file.path(pathtemp, "PredictorSummary.xlsx")

download_reference_from_drive <- function(dest_path) {
  tryCatch({
    suppressPackageStartupMessages(library(googledrive))
    message("Attempting to download PredictorSummary.xlsx from Google Drive release...")
    release <- googledrive::as_id(release_oct2024)
    target <- release %>%
      googledrive::drive_ls() %>%
      dplyr::filter(name == "Portfolios") %>%
      googledrive::drive_ls() %>%
      dplyr::filter(name == "Full Sets OP") %>%
      googledrive::drive_ls() %>%
      dplyr::filter(name == "PredictorSummary.xlsx")
    if (nrow(target) == 0) {
      warning("PredictorSummary.xlsx not found under provided release path.")
      return(FALSE)
    }
    googledrive::drive_download(target, path = dest_path, overwrite = TRUE)
    TRUE
  }, error = function(e) {
    warning("Failed to download PredictorSummary.xlsx from Google Drive: ", conditionMessage(e))
    FALSE
  })
}

download_success <- download_reference_from_drive(reference_path)
have_reference <- file.exists(reference_path)

if (have_reference) {
  suppressPackageStartupMessages(library(readxl))
  sumold0 <- readxl::read_xlsx(reference_path) %>%
    dplyr::select(signalname, tstat, rbar, vol, T, Nlong, Nshort)
} else {
  warning("Reference workbook not available. Diff column will be NA.")
  sumold0 <- tibble::tibble(
    signalname = character(),
    tstat = double(),
    rbar = double(),
    vol = double(),
    T = double(),
    Nlong = double(),
    Nshort = double()
  )
}

new_vs <- sumnew0 %>%
  dplyr::filter(port == "LS", signalname %in% quickrunlist) %>%
  dplyr::select(signalname, tstat, rbar, vol, T, Nlong, Nshort) %>%
  tidyr::pivot_longer(cols = !signalname, names_to = "metric", values_to = "new") %>%
  dplyr::left_join(
    sumold0 %>%
      dplyr::filter(signalname %in% quickrunlist) %>%
      tidyr::pivot_longer(cols = !signalname, names_to = "metric", values_to = "old"),
    by = c("signalname", "metric")
  ) %>%
  dplyr::mutate(diff = new - old)

print("===============================================")
print("\n\n New vs old portfolios:")
print(new_vs)

logs_dir <- file.path(pathProject, "Signals", "Logs")
if (!dir.exists(logs_dir)) {
  dir.create(logs_dir, recursive = TRUE, showWarnings = FALSE)
}

md_path <- file.path(logs_dir, "TestOutPortSelect.md")
csv_path <- file.path(logs_dir, "TestOutPortSelect.csv")

tstat <- new_vs %>% dplyr::filter(metric == "tstat")
txt <- capture.output(print(format(tstat, justify = "right"), row.names = FALSE))
writeLines(txt, md_path)

write.csv(tstat, csv_path, row.names = FALSE)

cat("\n\n All metrics:\n", file = md_path, append = TRUE)
txt_all <- capture.output(print(format(new_vs, justify = "right"), row.names = FALSE))
cat(paste0(txt_all, "\n"), file = md_path, append = TRUE)

message("\nOutputs written to:")
message("  ", md_path)
message("  ", csv_path)
