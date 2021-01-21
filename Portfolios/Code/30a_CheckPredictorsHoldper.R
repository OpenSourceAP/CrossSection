# For holding period variations on baseline portfolio tests
# takes about 2 hours, but outputs data every 30 min
# Andrew Chen 2020 01

rm(list=ls())

### ENVIRONMENT AND DATA ###

tryCatch(        
    source('00_SettingsAndFunctions.R')
  , error = function(cond){
      message('Error: 00_SettingsAndFunctions.R not found.  please setwd to pathProject/Portfolios/Code/')          
  }
)

source('setup_crspm.r')

######################################################################
### SELECT SIGNALS
######################################################################
# 2021 01 I took out the holdper == 1 requirement and added likely predictors
strategylist0 = alldocumentation %>% filter(Cat.Signal == 'Predictor')
strategylist0 = ifquickrun()

######################################################################
### BASE LS PERFORMANCE BY HOLDING PERIOD
######################################################################


## # debug
source('00_SettingsAndFunctions.R')

holdperlist = c(1,3,6,12)
## holdperlist = c(3)

for (i in seq(1,length(holdperlist))){
    print(paste0(
        'Running holdper = '
      , holdperlist[i]
      , ' ======================================='))

    ls_curr = loop_over_strategies(
        strategylist0 %>% mutate(holdper = holdperlist[i])
    ) %>%
        filter(port == 'LS') %>%
        select(signalname, date, ret, Nstocks)

    checkport(ls_curr,c('signalname'))

    writestandard(
        ls_curr
      , pathDataPortfolios
      , paste0('CheckPredictorLS_HoldPer_', holdperlist[i], '.csv')
    )
    
} # for i

