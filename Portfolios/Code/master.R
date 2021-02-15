# master.R created 2020 12 AC
# scripts below do the following
#   sets up paths (see 00_SettingsAndFunctions.R)
#   downloads crsp data that can't be easily shared and creates related predictors
#   creates all portfolios and saves csvs to disk
#   creates all exhibits for the paper

# the scripts require
#   user entry of pathProject in 00_SettingsAndFunctions.R
#   signal-firm-month csvs created by the signals code

# Most people only need to run up to 20_PredictorPorts.R and can skip any exhibits
# Exhibits are run immediately after the data required is created so
# you don't need to run every damn thing to update exhibits.

# exhibits can break if quickrun == T, and also you probably don't want
# incomplete exhibits anyway.

# I think it takes about 12 hours to run everything, and about 45 min to run up
# to 20_PredictorPorts.R

source('00_SettingsAndTools.R', echo=T)
source('01_PortfolioFunction.R', echo=T)


print('master: 10_DownloadCRSP.R')
tryCatch({
    source('10_DownloadCRSP.R', echo=T) 
})


print('master: 11_CreateCRSPPredictors.R')
tryCatch({
    source('11_CreateCRSPPredictors.R', echo=T) 
})


## # this is incomplete 2021 01 17 AC
## print('master: 12_SignalExhibits.R')
## tryCatch({
##     source('12_SignalExhibits.R', echo=T) 
## })


print('master: 20_PredictorPorts')
tryCatch({
    source('20_PredictorPorts.R', echo=T) # 30 min
})


## # update me
## print('master: 21_PredictorExhibits.R')
## if (quickrun==F){
##     tryCatch({
##         source('21_PredictorExhibits.R', echo=T)
##     })
## }

print('master: 30a_CheckPredictorsHoldper.R')
tryCatch({
    source('30a_CheckPredictorsHoldper.R', echo=T) # 2 hours
})

print('master: 30b_CheckPredictorsLiqScreens.R')
tryCatch({
    source('30b_CheckPredictorsLiqScreens.R', echo=T) # 2 hours
})

print('master: 30c_CheckPredictorsDeciles.R')
tryCatch({
    source('30c_CheckPredictorsDeciles.R', echo=T) # 30 min
})

## if (quickrun==F){
##     print('31_CheckPredictorsExhibits.R')
##     tryCatch({
##         source('31_CheckPredictorsExhibits.R', echo=T, verbose=T)
##     })
## }

print('master: 40 40_PlaceboPorts.R')
tryCatch({
    source('40_PlaceboPorts.R', echo=T) # 30 min
})

## # incomplete
## if (quickrun==F){
##     print('41_PlaceboExhibits.R')
##     tryCatch({
##         source('41_PlaceboExhibits.R', echo=T, verbose=T)
##     })
## }


print('master: 50_DailyPredictorPorts.R')
tryCatch({
    source('50_DailyPredictorPorts.R', echo=T) # about 6 hours
})
