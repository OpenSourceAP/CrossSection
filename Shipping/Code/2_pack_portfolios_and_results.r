# """
# Inputs: Uses `pathStorage`, `pathPortfolios`, and `pathResults` from `00_settings.yaml`; consumes portfolio CSVs and result artifacts.
# Outputs: Copies and zips portfolio deliverables plus results into the release tree under `pathStorage`.
# How to run: Called from `master_shipping.r`; can be sourced directly after loading helpers from `00_functions.r`.
# Example: `Rscript 2_pack_portfolios_and_results.r`
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

starttime <- Sys.time()
script_wd <- getwd()
on.exit(setwd(script_wd), add = TRUE)

dir_portfolios <- file.path(pathStorage, 'Portfolios')
dir_full_sets_op <- file.path(dir_portfolios, 'Full Sets OP')
dir_full_sets_alt <- file.path(dir_portfolios, 'Full Sets Alt')
dir_individual <- file.path(dir_portfolios, 'Individual')
dir_daily_storage <- file.path(pathStorage, 'DailyPortfolios')
dir_results <- file.path(pathStorage, 'Results')

ensure_dir(dir_portfolios)
ensure_dir(dir_full_sets_op)
ensure_dir(dir_full_sets_alt)
ensure_dir(dir_individual)
ensure_dir(dir_daily_storage)
ensure_dir(dir_results)

# ==== FULL SETS OP ====
flist <- list.files(pathPortfolios)
flist <- flist[!grepl('PredictorAlt', flist)]

for (fcurr in flist) {
  file.copy(
    from = file.path(pathPortfolios, fcurr),
    to = dir_full_sets_op
  )
}

# ==== FULL SETS ALT ====
implist <- list.files(pathPortfolios, pattern = 'PredictorAlt') %>%
  str_remove('.csv')

tempdir <- getwd()
setwd(pathPortfolios)

print(paste0('Zipping Predictor Alt csvs ', Sys.time()))
for (impcurr in implist) {
  zip(
    zipfile = file.path(dir_full_sets_alt, paste0(impcurr, '.zip')),
    files = paste0(impcurr, '.csv')
  )
}

impcurr <- 'PlaceboPortsFull'
zip(
  zipfile = file.path(dir_full_sets_alt, paste0(impcurr, '.zip')),
  files = paste0(impcurr, '.csv')
)

setwd(tempdir)
print(paste0('Done zipping Predictor Alt csvs ', Sys.time()))

# ==== INDIVIDUAL PREDICTOR PORTFOLIO SORTS REPACKING ====
write_indiv <- function(setname, outfolder) {
  pathout <- file.path(dir_individual, outfolder)

  ensure_dir(pathout)

  allport <- fread(file.path(pathPortfolios, setname))
  signallist <- allport %>% distinct(signalname) %>% as.matrix()

  for (i in seq_along(signallist)) {
    tempret <- allport %>%
      filter(signalname == signallist[i]) %>%
      select(date, port, ret) %>%
      filter(!is.na(ret)) %>%
      spread(port, ret, sep = '')

    write.csv(
      tempret,
      file = file.path(pathout, paste0(signallist[i], '.csv'))
    )
  }
}

print('writing portfolios individual original cuts')
write_indiv('PredictorPortsFull.csv', 'Original_Cuts')

print('writing portfolios individual original cuts VW')
write_indiv('PredictorAltPorts_LiqScreen_VWforce.csv', 'Original_CutsVW')

print('writing portfolios individual cts deciles')
write_indiv('PredictorAltPorts_Deciles.csv', 'Cts_Deciles')

print('writing portfolios individual cts quintiles')
write_indiv('PredictorAltPorts_Quintiles.csv', 'Cts_Quintiles')

print('writing portfolios individual cts deciles vw')
write_indiv('PredictorAltPorts_DecilesVW.csv', 'Cts_DecilesVW')

print('writing portfolios individual cts quintiles vw')
write_indiv('PredictorAltPorts_QuintilesVW.csv', 'Cts_QuintilesVW')

# ==== DAILY PORTFOLIOS ====

daily_portfolios_dir <- file.path(pathPortfolios, '..', 'DailyPortfolios')
tempdir <- getwd()
setwd(daily_portfolios_dir)

implist <- list.dirs('.', recursive = FALSE, full.names = FALSE)
implist <- implist[grepl('Predictor', implist)]

print(paste0('Daily Predictor csvs ', Sys.time()))
for (impcurr in implist) {
  zip(
    zipfile = file.path(dir_daily_storage, paste0(impcurr, '.zip')),
    files = impcurr
  )
}

file.copy(
  from = 'DailyPortSummary.xlsx',
  to = dir_daily_storage
)

setwd(tempdir)
print(paste0('Done zipping daily portfolio csvs ', Sys.time()))

print(Sys.time() - starttime)

# ==== RESULTS ====
result_wd <- getwd()
setwd(pathResults)

flist <- list.files()
for (fcurr in flist) {
  success <- file.copy(
    from = fcurr,
    to = file.path(dir_results, fcurr)
  )
  if (!success) {
    print(paste0('Failed to copy ', fcurr))
  }
}
setwd(result_wd)
