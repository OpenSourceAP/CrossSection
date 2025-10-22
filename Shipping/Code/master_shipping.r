# """
# Inputs: Reads `00_settings.yaml` for `pathProject` and `pathStorage`, consumes outputs from Signals and Portfolios subpipelines.
# Outputs: Populates the release folder under `pathStorage` with signals, portfolios, results, and validation checks.
# How to run: Execute `Rscript master_shipping.r` from `Shipping/Code/` after upstream pipelines succeed.
# Example: `Rscript master_shipping.r`
# """
# ==== SETTINGS ====
# this code moves and zips files from the local repo Data subfolders
# to some storage area for shipping
# Not sure anyone besides us will need to us it.
# But it's good for replication, and to make data updates easier down the road.

library(tidyverse)
library(readxl)
library(data.table) # for speed
library(googledrive)

tryCatch(
  source('00_functions.r'),
  error = function(err) {
    alt_path = file.path('Shipping', 'Code', '00_functions.r')
    if (file.exists(alt_path)) {
      source(alt_path)
    } else {
      stop(err)
    }
  }
)

paths = shipping_bootstrap(auth_drive = TRUE)
list2env(paths, envir = environment())

message('Shipping configuration:')
config_summary <- tibble::tibble(
  item = c(
    'pathProject',
    'pathStorage',
    'pathPredictors',
    'pathPlacebos',
    'pathPortfolios',
    'pathResults',
    'OLD_PATH_RELEASES',
    'NEW_PATH_RELEASES'
  ),
  value = c(
    pathProject,
    pathStorage,
    pathPredictors,
    pathPlacebos,
    pathPortfolios,
    pathResults,
    ifelse(is.null(OLD_PATH_RELEASES), NA_character_, OLD_PATH_RELEASES),
    ifelse(is.null(NEW_PATH_RELEASES), NA_character_, NEW_PATH_RELEASES)
  )
)
print(config_summary, n = nrow(config_summary), width = Inf)

message('Please check the configuration above')
response <- tolower(trimws(readline(prompt = 'Proceed with shipping? [y/N]: ')))
if (!response %in% c('y', 'yes')) {
  stop('Shipping aborted by user.', call. = FALSE)
}

message('Continuing with shipping...')


# ==== DO STUFF ====

# update SignalDo
file.copy(
  from = paste0(pathProject,'SignalDoc.csv')
  , to = paste0(pathStorage)
)

source('1_pack_signals.r')
source('2_pack_portfolios_and_results.r')
source('3_check_storage.r')
source('4_old_vs_new_check.r')
