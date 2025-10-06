# Inputs: Predictor portfolio returns in `Portfolios/Data/Portfolios/PredictorPortsFull.csv`,
#         signal metadata from `SignalDoc.csv`, and the October 2024 public
#         release folder on Google Drive (`https://drive.google.com/drive/folders/1SSoHGbwgyhRwUCzLE0YWvUlS0DjLCd4k`).
#         References `Signals/DocsForClaude/PredictorSummary.xlsx` (downloaded each run).
# Outputs: Console summary plus `Signals/Logs/TestOutPortSelect.md` and
#          `Signals/Logs/TestOutPortSelect.csv` comparing fresh t-stats with the
#          release workbook.
# How to run:
# - `Rscript utils/TestPortSelect.R --predictors ShortInterest`
# - `Rscript utils/TestPortSelect.R --predictors ShortInterest,OptionVolume1`

suppressPackageStartupMessages({
  library(dplyr)
  library(readr)
  library(tidyr)
  library(stringr)
  library(lubridate)
})

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

# Argument parsing -----------------------------------------------------------
target_signals <- character(0)

parse_predictor_arg <- function(value) {
  str_split(value, pattern = ",", simplify = FALSE) %>%
    unlist() %>%
    str_trim() %>%
    {
      .[. != ""]
    }
}

i <- 1
while (i <= length(args_trailing)) {
  arg <- args_trailing[[i]]
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

target_signals <- unique(target_signals)

if (length(target_signals) == 0) {
  stop("No predictors supplied. Use --predictors to provide one or more signal names.")
}

# Load signal documentation --------------------------------------------------
doc_path <- file.path(project_root, "SignalDoc.csv")
signal_doc <- read_csv(doc_path, show_col_types = FALSE) %>%
  rename(signalname = Acronym)

available_predictors <- signal_doc %>%
  filter(Cat.Signal == "Predictor") %>%
  pull(signalname)

missing_in_doc <- setdiff(target_signals, available_predictors)
if (length(missing_in_doc) > 0) {
  stop("Predictors not found in SignalDoc.csv: ", paste(missing_in_doc, collapse = ", "))
}

# Check predictor CSVs exist -------------------------------------------------
path_predictors <- file.path(project_root, "Signals", "pyData", "Predictors")

missing_csv <- target_signals[!file.exists(file.path(path_predictors, paste0(target_signals, ".csv")))]
if (length(missing_csv) > 0) {
  warning("Predictor CSVs missing under ", path_predictors, ": ", paste(missing_csv, collapse = ", "))
}

# Load long-short portfolio returns -----------------------------------------
ports_path <- file.path(project_root, "Portfolios", "Data", "Portfolios", "PredictorPortsFull.csv")
if (!file.exists(ports_path)) {
  stop("Portfolio return file not found: ", ports_path)
}

message("Reading portfolio returns from ", ports_path)
ports_df <- read_csv(
  ports_path,
  show_col_types = FALSE,
  col_select = c(signalname, port, date, ret, signallag, Nlong, Nshort)
)

ls_df <- ports_df %>%
  filter(signalname %in% target_signals, port == "LS")

if (nrow(ls_df) == 0) {
  stop("No LS portfolio rows found for the requested predictors. Ensure upstream portfolios have been generated.")
}

sample_info <- signal_doc %>%
  select(signalname, SampleStartYear, SampleEndYear, Year)

ls_df <- ls_df %>%
  mutate(date = as.Date(date)) %>%
  left_join(sample_info, by = "signalname") %>%
  mutate(
    sample_year = year(date),
    samptype = case_when(
      !is.na(SampleStartYear) & !is.na(SampleEndYear) &
        sample_year >= SampleStartYear & sample_year <= SampleEndYear ~ "insamp",
      !is.na(Year) & sample_year > Year ~ "postpub",
      TRUE ~ NA_character_
    )
  ) %>%
  filter(samptype == "insamp")

if (nrow(ls_df) == 0) {
  stop("No in-sample LS portfolio rows matched the documentation-defined sample period for the requested predictors.")
}

summary_df <- ls_df %>%
  mutate(
    Ncheck = pmin(Nlong, Nshort, na.rm = TRUE)
  ) %>%
  filter(!is.na(ret), Ncheck >= 1) %>%
  group_by(signalname) %>%
  summarize(
    tstat = round(mean(ret) / sd(ret) * sqrt(n()), 2),
    rbar = round(mean(ret), 2),
    vol = round(sd(ret), 2),
    T = n(),
    Nlong = round(mean(Nlong, na.rm = TRUE), 1),
    Nshort = round(mean(Nshort, na.rm = TRUE), 1),
    signallag = round(mean(signallag, na.rm = TRUE), 3),
    .groups = "drop"
  )

# Prepare comparison with reference workbook --------------------------------
reference_dir <- file.path(project_root, "Signals", "DocsForClaude")
if (!dir.exists(reference_dir)) {
  dir.create(reference_dir, recursive = TRUE, showWarnings = FALSE)
}

reference_path <- file.path(reference_dir, "PredictorSummary.xlsx")

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

# Always attempt to refresh the workbook from the October 2024 release
download_success <- download_reference_from_drive(reference_path)
have_reference <- file.exists(reference_path)

if (have_reference) {
  suppressPackageStartupMessages(library(readxl))
  reference_df <- readxl::read_xlsx(reference_path) %>%
    select(signalname, tstat, rbar, vol, T, Nlong, Nshort)
} else {
  warning("Reference workbook not available. Diff column will be NA. Confirm Google Drive access and rerun.")
  reference_df <- tibble(signalname = character(), tstat = double(), rbar = double(), vol = double(), T = double(), Nlong = double(), Nshort = double())
}

new_long <- summary_df %>%
  select(signalname, tstat, rbar, vol, T, Nlong, Nshort) %>%
  pivot_longer(cols = -signalname, names_to = "metric", values_to = "new")

old_long <- reference_df %>%
  filter(signalname %in% target_signals) %>%
  pivot_longer(cols = -signalname, names_to = "metric", values_to = "old")

comparison <- new_long %>%
  left_join(old_long, by = c("signalname", "metric")) %>%
  mutate(diff = ifelse(is.na(old), NA_real_, new - old)) %>%
  arrange(signalname, match(metric, c("tstat", "rbar", "vol", "T", "Nlong", "Nshort")))

message(strrep("=", 47))
message("TestPortSelect comparison")
print(comparison)

# Persist results -----------------------------------------------------------
logs_dir <- file.path(project_root, "Signals", "Logs")
if (!dir.exists(logs_dir)) {
  dir.create(logs_dir, recursive = TRUE, showWarnings = FALSE)
}

md_path <- file.path(logs_dir, "TestOutPortSelect.md")
csv_path <- file.path(logs_dir, "TestOutPortSelect.csv")

tstat_table <- comparison %>% filter(metric == "tstat")
md_lines <- capture.output(print(format(tstat_table, justify = "right"), row.names = FALSE))
writeLines(md_lines, md_path)

write_csv(tstat_table, csv_path)

cat('\n\n All metrics:\n', file = md_path, append = TRUE)
all_lines <- capture.output(print(format(comparison, justify = "right"), row.names = FALSE))
cat(paste0(all_lines, '\n'), file = md_path, append = TRUE)

message('\nOutputs written to:')
message('  ', md_path)
message('  ', csv_path)
