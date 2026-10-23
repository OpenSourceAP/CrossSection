# Run: Rscript Portfolios/Code/master.R, or Source this saved file in RStudio.
# Inputs: config.R, SignalDoc.csv, signal CSVs and Signals/pyData CRSP parquet files.
# Outputs: portfolio CSVs/workbooks, processed CRSP and optional exhibits under
# the configured output root (the project root by default).

# Start R from the project root or a subfolder (including Portfolios/Code).
here::i_am("Portfolios/Code/master.R")
source(here::here('Portfolios/Code/config.R'), local = TRUE)
source(here::here('Portfolios/Code/00_SettingsAndTools.R'), local = TRUE)
setwd(pathCode)
source('01_PortfolioFunction.R', echo = feed.verbose, local = TRUE)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Check that the CRSP inputs from Signals/pyCode exist (stops if not)
check_crsp_inputs(pathProject, skipdaily)

# Check if signals data is complete
signals_complete <- check_signal_csvs(pathProject, SignalSource)
if (!interactive()) {
    if (!signals_complete) {
        stop('Non-interactive run halted: signals not complete')
    }
} else {
    user_response <- tolower(trimws(readline(prompt = 'Proceed with portfolio build? [y/N]: ')))
    if (!(user_response %in% c('y', 'yes'))) {
        stop('Aborting master.R execution at user request.')
    }
    if (!signals_complete) {
        message('Continuing despite missing signals based on user confirmation.')
    }
}

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# PREPARE INTERMEDIATE DATA ####

print('master: 11_ProcessCRSP.R')
tryCatch({
    source('11_ProcessCRSP.R', echo=feed.verbose, local=TRUE)
})

# ==== CREATE BASELINE PORTFOLIOS ====
print('master: 20_PredictorPorts')
tryCatch({
    source('20_PredictorPorts.R', echo=feed.verbose, local=TRUE) # 30 min
})


if (runexhibits){
    print('master: 21_PredictorExhibits.R')
    tryCatch({
        source('21_PredictorExhibits.R', echo=feed.verbose, local=TRUE)
    })
}

# CREATE ALTERNATIVE PORTFOLIOS AND PLACEBOS ####


print('master: 30_PredictorAltPorts.R')
tryCatch({
    source('30_PredictorAltPorts.R', echo=feed.verbose, local=TRUE) # about 6 hours
})


if (runexhibits){
    print('31_CheckPredictorsExhibits.R')
    tryCatch({
        source('31_CheckPredictorsExhibits.R', echo=feed.verbose, verbose=feed.verbose, local=TRUE)
    })
}

print('master: 32_Predictor2x3Ports.R')
tryCatch({
    source('32_Predictor2x3Ports.R', echo=feed.verbose, local=TRUE)
})

print('master: 40 40_PlaceboPorts.R')
tryCatch({
    source('40_PlaceboPorts.R', echo=feed.verbose, local=TRUE) # 30 min
})


if (runexhibits){
    print('41_PlaceboExhibits.R')
    tryCatch({
        source('41_PlaceboExhibits.R', echo=feed.verbose, verbose=feed.verbose, local=TRUE)
    })
}

# EXTRA STUFF ####

# this can be run at the end since it takes a long time and isn't necessary for other results
if (!skipdaily){
    print('master: 50_DailyPredictorPorts.R')
    tryCatch({
        source('50_DailyPredictorPorts.R', echo=feed.verbose, local=TRUE) # about 6 hours
    })
}
