# """
# Inputs: Uses `pathPredictors` and `pathPlacebos` under `pathProject` plus metadata from `SignalDoc.csv` (resolved via `00_settings.yaml`).
# Outputs: Writes the wide signed predictor CSV/ZIP and copies individual predictor and placebo files into `pathStorage`.
# How to run: Called from `master_shipping.r`; can be executed stand-alone after sourcing `00_functions.r`.
# Example: `Rscript 1_pack_signals.r`
# """

library(tidyverse)
library(data.table)

tryCatch(
  source('00_functions.r'),
  error = function(err) {
    alt_path <- file.path('Shipping', 'Code', '00_functions.r')
    if (file.exists(alt_path)) {
      source(alt_path)
    } else {
      stop(err)
    }
  }
)

paths <- shipping_bootstrap(auth_drive = FALSE)
list2env(paths, envir = environment())

print('Script: repackaging signals and portfolios')
Sys.time()

dir_firm_char <- file.path(pathStorage, 'Firm Level Characteristics')
dir_full_sets <- file.path(dir_firm_char, 'Full Sets')
dir_individual <- file.path(dir_firm_char, 'Individual')
dir_individual_predictors <- file.path(dir_individual, 'Predictors')
dir_individual_placebos <- file.path(dir_individual, 'Placebos')

ensure_dir(dir_firm_char)
ensure_dir(dir_full_sets)
ensure_dir(dir_individual)

# ==== SIGNALS IN WIDE FORMAT ====

print(paste0('Repackaging signals ', Sys.time()))

doc <- readdocumentation() %>%
  filter(Cat.Signal == 'Predictor') %>%
  filter(!signalname %in% c('Price', 'Size', 'STreversal'))

prds <- doc %>% pull(signalname)
signs <- doc %>% pull(Sign) %>% as.numeric()

# initialize
signals <- read_csv(file.path(pathPredictors, paste0(prds[1], '.csv'))) %>%
  select(permno, yyyymm) %>%
  as.data.table()

# loop over predictors and append
for (i in seq_along(prds)) {
  print(paste('Appending ', prds[i], ' #', i, ' of ', length(prds), ' non-CRSP predictors'))

  csv_path <- file.path(pathPredictors, paste0(prds[i], '.csv'))
  if (file.exists(csv_path)) {
    tempin <- fread(csv_path)
    tempin[, 3] <- signs[i] * tempin[, 3]

    gc()

    signals <- merge(signals, tempin, by = c('permno', 'yyyymm'), all = TRUE)

    gc()
  } else {
    message(paste(i, ' does not exist in Data/Predictors folder'))
  }
}

# save to disk
signed_predictors_path <- file.path(data_dir, 'signed_predictors_dl_wide.csv')
fwrite(signals, file = signed_predictors_path)
print(paste0('Done repackaging signals ', Sys.time()))

# zip to storage
print(paste0('Zipping Predictor Wide csvs, takes about 20 min ', Sys.time()))
tempdir <- getwd()
setwd(data_dir) # avoids copying paths into zip
zip(
  zipfile = file.path(dir_full_sets, 'signed_predictors_dl_wide.zip'),
  files = 'signed_predictors_dl_wide.csv'
)
setwd(tempdir)
print(paste0('Done zipping Predictor Wide csvs ', Sys.time()))

# ==== INDIVIDUAL SIGNALS ====

print(paste0('Copying individual signal csvs ', Sys.time()))
file.copy(
  from = pathPredictors,
  to = dir_individual,
  recursive = TRUE
)

file.copy(
  from = pathPlacebos,
  to = dir_individual,
  recursive = TRUE
)

print(paste0('Done copying individual signal csvs ', Sys.time()))

# remove CRSP predictors
file.remove(file.path(dir_individual_predictors, 'Price.csv'))
file.remove(file.path(dir_individual_predictors, 'Size.csv'))
file.remove(file.path(dir_individual_predictors, 'STreversal.csv'))

# remove TAQ spreads
file.remove(file.path(dir_individual_placebos, 'BidAskTAQ.csv'))

# zip predictors to storage -----------------------------------------------
print(paste0('Zipping PredictorsIndiv.zip ', Sys.time()))
tempdir <- getwd()
setwd(dir_individual_predictors) # avoids copying paths into zip
files2zip <- dir(pattern = '*.csv')
zip(
  zipfile = file.path(dir_full_sets, 'PredictorsIndiv.zip'),
  files = files2zip
)
setwd(tempdir)
print(paste0('Done zipping PredictorsIndiv.zip ', Sys.time()))

# zip placebos to storage -----------------------------------------------
print(paste0('Zipping PlacebosIndiv.zip ', Sys.time()))
tempdir <- getwd()
setwd(dir_individual_placebos) # avoids copying paths into zip
files2zip <- dir(pattern = '*.csv')
zip(
  zipfile = file.path(dir_full_sets, 'PlacebosIndiv.zip'),
  files = files2zip
)
setwd(tempdir)
print(paste0('Done zipping PlacebosIndiv.zip ', Sys.time()))
