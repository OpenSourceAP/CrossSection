# tbc: zipping full sets
# Andrew 2021 03

print('Script: repackaging signals and portfolios')
Sys.time()

dir.create(paste0(pathStorage,'Firm Level Characteristics/'))
dir.create(paste0(pathStorage,'Firm Level Characteristics/Full Sets/'))
dir.create(paste0(pathStorage,'Firm Level Characteristics/Individual/'))


# ==== SIGNALS IN WIDE FORMAT ====

print(paste0('Repackaging signals ',Sys.time()))

# set up for loop
doc = readdocumentation() %>%
  filter(Cat.Signal=='Predictor') %>%
  filter(!signalname %in% c('Price','Size','STreversal')) # remove crsp predictors

prds = doc%>% pull(signalname)
signs = doc %>% pull(Sign) %>% as.numeric


# initialize
signals = read_csv(paste0(pathPredictors, prds[1], '.csv')) %>%
    select(permno, yyyymm) %>%
    as.data.table

# loop over predictors and append
for (i in 1:length(prds)){

    print(paste('Appending ', prds[i], ' #', i, ' of ', length(prds)))

    if (file.exists(paste0(pathPredictors, prds[i], '.csv'))) {
        tempin = fread(paste0(pathPredictors, prds[i], '.csv'))
        tempin[,3] = signs[i]*tempin[,3] # sign according top OP

        gc()

        signals = merge(signals,tempin, by=c('permno','yyyymm'), all=T)

        gc()

    } else {
        message(paste(i, ' does not exist in Data/Predictors folder'))
    }
}

## save to disk
# first write csv
fwrite(
    signals
  , file = paste0(pathShipping, 'Data/signed_predictors_dl_wide.csv')
)
print(paste0('Done repackaging signals ',Sys.time()))

# zip to storage


print(paste0('Zipping Predictor Wide csvs, takes about 20 min ',Sys.time()))
tempdir = getwd()
setwd(paste0(pathShipping,'Data/')) # avoids copying paths into zip
zip(
  zipfile = paste0(pathStorage, 'Firm Level Characteristics/Full Sets/signed_predictors_dl_wide.zip')
  , files = 'signed_predictors_dl_wide.csv'
)
setwd(tempdir)
print(paste0('Done zipping Predictor Wide csvs ',Sys.time()))


# ==== INDIVIDUAL SIGNALS ====

print(paste0('Copying individual signal csvs ',Sys.time()))
file.copy(
  from = paste0(pathPredictors)
  , to = paste0(pathStorage,'Firm Level Characteristics/Individual/')
  , recursive=TRUE
)


file.copy(
  from = paste0(pathPlacebos)
  , to = paste0(pathStorage,'Firm Level Characteristics/Individual/')
  , recursive=TRUE
)

print(paste0('Done copying individual signal csvs ',Sys.time()))


# remove crsp predictors
file.remove(
  paste0(pathStorage,'Firm Level Characteristics/Individual/Predictors/Price.csv')
)
file.remove(
  paste0(pathStorage,'Firm Level Characteristics/Individual/Predictors/Size.csv')
)
file.remove(
  paste0(pathStorage,'Firm Level Characteristics/Individual/Predictors/STreversal.csv')
)

# remove TAQ spreads
file.remove(
  paste0(pathStorage,'Firm Level Characteristics/Individual/Placebos/BidAskTAQ.csv')
)

