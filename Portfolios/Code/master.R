# master.R 

# You need to set the project path below before executing other scripts

# scripts below do the following
#   sets up paths (see 00_SettingsAndTools.R)
#   downloads crsp data that can't be easily shared and creates related predictors
#   creates all portfolios and saves csvs to disk
#   creates all exhibits for the paper

# the scripts require
#   user entry of pathProject in 00_SettingsAndTools.R
#   signal-firm-month csvs created by the signals code

# Most people only need to run up to 20_PredictorPorts.R and can skip any exhibits
# Exhibits are run immediately after the data required is created so
# you don't need to run every damn thing to update exhibits.

# exhibits can break if quickrun == T, and also you probably don't want
# incomplete exhibits anyway.

# I think it takes about 12 hours to run everything, and about 45 min to run up
# to 20_PredictorPorts.R

# ENVIRONMENT ####
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
rm(list = ls())
# ENTER PROJECT PATH HERE (i.e. this should be the path to your local repo folder)
pathProject = 'd:/pc_work/DebugCross/'

quickrun =  F # use T if you want to run quickly for testing
quickrunlist = c('Size','STreversal') # list of signals to use for quickrun
skipdaily = T # use T to skip daily CRSP which is very slow
feed.verbose = F # use T if you want lots of feedback

# Check whether project path is set correctly
if (!dir.exists(paste0(pathProject, 'Portfolios'))) {
    stop('Project path not set correctly')
}

# setwd to folder with all R scripts for convenience
setwd(paste0(pathProject,'Portfolios/Code/'))

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
source('00_SettingsAndTools.R', echo=T)
source('01_PortfolioFunction.R', echo=T)

# PREPARE INTERMEDIATE DATA ####

print('master: 10_DownloadCRSP.R')
tryCatch({
    source('10_DownloadCRSP.R', echo=T)
})

print('master: 11_ProcessCrsp.R')
tryCatch({
    source('11_ProcessCRSP.R', echo=T)
})

print('master: 12_CreateCRSPPredictors.R')
tryCatch({
    source('12_CreateCRSPPredictors.R', echo=T)
})

# ==== CREATE BASELINE PORTFOLIOS ====
print('master: 20_PredictorPorts')
tryCatch({
    source('20_PredictorPorts.R', echo=T) # 30 min
})


print('master: 21_PredictorExhibits.R')
if (quickrun==F){
    tryCatch({
        source('21_PredictorExhibits.R', echo=T)
    })
}

# CREATE ALTERNATIVE PORTFOLIOS AND PLACEBOS ####


print('master: 30_PredictorAltPorts.R')
tryCatch({
    source('30_PredictorAltPorts.R', echo=T) # about 6 hours
})


if (quickrun==F){
    print('31_CheckPredictorsExhibits.R')
    tryCatch({
        source('31_CheckPredictorsExhibits.R', echo=T, verbose=T)
    })
}

print('master: 40 40_PlaceboPorts.R')
tryCatch({
    source('40_PlaceboPorts.R', echo=T) # 30 min
})


if (quickrun==F){
    print('41_PlaceboExhibits.R')
    tryCatch({
        source('41_PlaceboExhibits.R', echo=T, verbose=T)
    })
}

# EXTRA STUFF ####

# this can be run at the end since it takes a long time and isn't necessary for other results
print('master: 12_SignalExhibits.R')
tryCatch({
    source('12_SignalExhibits.R', echo=T)
})

if (!skipdaily){
    print('master: 50_DailyPredictorPorts.R')
    tryCatch({
        source('50_DailyPredictorPorts.R', echo=T) # about 6 hours
    })
}