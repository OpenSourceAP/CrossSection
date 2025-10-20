# """
# Inputs: Parses `00_settings.yaml` to expose shipping paths; requires optional packages `yaml` and `googledrive` when advanced features are used.
# Outputs: Provides helper functions (`load_shipping_settings`, `shipping_bootstrap`, `readdocumentation`, `ensure_dir`) for other shipping scripts.
# How to run: Source this file with `source('00_functions.r')` inside `Shipping/Code/` to make helpers available.
# Example: `helpers <- shipping_bootstrap(auth_drive = FALSE); pathStorage <- helpers$pathStorage`
# """

load_shipping_settings <- function(settings_path = '00_settings.yaml') {
  if (!file.exists(settings_path)) {
    alt_path <- file.path('Shipping', 'Code', settings_path)
    if (file.exists(alt_path)) {
      settings_path <- alt_path
    } else {
      stop(sprintf('Unable to locate %s or %s.', settings_path, alt_path))
    }
  }

  if (requireNamespace('yaml', quietly = TRUE)) {
    settings <- yaml::read_yaml(settings_path)
    if (is.null(settings)) {
      return(list())
    }
    return(settings)
  }

  message("Package 'yaml' not found; using a simple key:value parser for 00_settings.yaml.")
  settings_lines <- readLines(settings_path)
  settings <- list()
  for (line in settings_lines) {
    line <- trimws(line)
    if (line == '' || startsWith(line, '#')) {
      next
    }
    parts <- strsplit(line, ':', fixed = TRUE)[[1]]
    if (length(parts) < 2) {
      next
    }
    key <- trimws(parts[1])
    value <- trimws(paste(parts[-1], collapse = ':'))
    settings[[key]] <- value
  }
  settings
}

ensure_dir <- function(path) {
  dir.create(path, recursive = TRUE, showWarnings = FALSE)
}

shipping_bootstrap <- function(settings_path = '00_settings.yaml',
                               auth_drive = FALSE,
                               ensure_subdirs = TRUE,
                               change_wd = TRUE) {
  settings <- load_shipping_settings(settings_path)

  if (is.null(settings$pathProject) || is.null(settings$pathStorage)) {
    stop('00_settings.yaml must define pathProject and pathStorage.')
  }

  pathProject <- path.expand(settings$pathProject)
  pathStorage <- path.expand(settings$pathStorage)
  pathShipping <- file.path(pathProject, 'Shipping')
  code_dir <- file.path(pathShipping, 'Code')
  data_dir <- file.path(pathShipping, 'Data')
  data_portfolios_dir <- file.path(data_dir, 'Portfolios')
  data_portfolios_indiv_dir <- file.path(data_portfolios_dir, 'Individual')
  temp_dir <- file.path(data_dir, 'temp')

  if (ensure_subdirs) {
    ensure_dir(pathStorage)
    ensure_dir(data_dir)
    ensure_dir(data_portfolios_dir)
    ensure_dir(data_portfolios_indiv_dir)
    ensure_dir(temp_dir)
  }

  if (change_wd) {
    setwd(code_dir)
  }

  if (auth_drive) {
    if (!requireNamespace('googledrive', quietly = TRUE)) {
      stop("Package 'googledrive' is required for Drive actions. Install it with install.packages('googledrive').")
    }
    googledrive::drive_auth()
  }

  list(
    pathProject = pathProject,
    pathStorage = pathStorage,
    pathShipping = pathShipping,
    code_dir = code_dir,
    data_dir = data_dir,
    data_temp_dir = temp_dir,
    pathPredictors = file.path(pathProject, 'Signals/pyData/Predictors'),
    pathPlacebos = file.path(pathProject, 'Signals/pyData/Placebos'),
    pathPortfolios = file.path(pathProject, 'Portfolios/Data/Portfolios'),
    pathResults = file.path(pathProject, 'Results'),
    OLD_PATH_RELEASES = settings$OLD_PATH_RELEASES,
    NEW_PATH_RELEASES = settings$NEW_PATH_RELEASES
  )
}

readdocumentation <- function(path_project = get0('pathProject', ifnotfound = NULL, inherits = TRUE)) {
  if (is.null(path_project)) {
    stop('readdocumentation requires a path_project argument or a global pathProject variable.')
  }

  if (!requireNamespace('readr', quietly = TRUE) ||
      !requireNamespace('dplyr', quietly = TRUE) ||
      !requireNamespace('forcats', quietly = TRUE) ||
      !requireNamespace('stringr', quietly = TRUE) ||
      !requireNamespace('tidyselect', quietly = TRUE)) {
    stop("Packages readr, dplyr, forcats, stringr, and tidyselect are required for readdocumentation().")
  }

  doc_path <- file.path(path_project, 'SignalDoc.csv')
  alldocumentation <- readr::read_csv(doc_path, show_col_types = FALSE)
  alldocumentation <- dplyr::rename(alldocumentation, signalname = Acronym)
  alldocumentation <- dplyr::mutate(
    alldocumentation,
    Cat.Data = forcats::fct_relevel(forcats::as_factor(Cat.Data),
                                    'Accounting', 'Analyst', 'Event', 'Options', 'Price', 'Trading', '13F', 'Other'),
    Cat.Economic = stringr::str_to_title(Cat.Economic)
  )
  alldocumentation <- dplyr::rename(
    alldocumentation,
    sweight = 'Stock Weight',
    q_cut = 'LS Quantile',
    q_filt = 'Quantile Filter',
    portperiod = 'Portfolio Period',
    startmonth = 'Start Month',
    filterstr = 'Filter'
  )
  alldocumentation <- dplyr::mutate(
    alldocumentation,
    filterstr = dplyr::if_else(filterstr %in% c('NA', 'None', 'none'), NA_character_, filterstr)
  )
  alldocumentation <- dplyr::select(alldocumentation, -tidyselect::starts_with('Note'))
  alldocumentation <- dplyr::arrange(alldocumentation, signalname)

  names(alldocumentation) <- make.names(names(alldocumentation))
  alldocumentation
}
