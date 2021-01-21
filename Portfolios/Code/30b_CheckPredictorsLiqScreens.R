# For liquidity screen variations on baseline portfolio tests
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

source('setup_crspm.r', echo = T)

######################################################################
### SELECT SIGNALS
######################################################################
# 2021 01 I took out the holdper == 1 requirement and added likely predictors
strategylist0 = alldocumentation %>% filter(Cat.Signal == 'Predictor')
strategylist0 = ifquickrun()

#####################################################################
### BASE LS PERFORMANCE BY LIQUIDITY SCREEN
#####################################################################

print('CheckLiq: ME > NYSE 20 pct =========================================')

## ME > NYSE 20th pct
# create ME screen
# customscreen is used on the signal df, which is then lagged, so no look ahead here
ls = loop_over_strategies(
    strategylist0 %>% mutate(filtcust = 'me > me_nyse20')
)  %>%
    filter(port == 'LS') %>%
    select(signalname, date, ret, Nstocks)

checkport(ls,c('signalname'))

writestandard(ls, pathDataPortfolios, 'CheckPredictorLS_LiqScreen_ME_gt_NYSE20pct.csv')


## Price > 5
print('CheckLiq: Price > 5  =========================================')
ls = loop_over_strategies(
    strategylist0 %>% mutate(FilterPrice = 5)
)  %>%
    filter(port == 'LS') %>%
    select(signalname, date, ret, Nstocks)
writestandard(ls, pathDataPortfolios, 'CheckPredictorLS_LiqScreen_Price_gt_5.csv')



## NYSE only

print('CheckLiq: NYSE only =========================================')
ls = loop_over_strategies(
    strategylist0 %>% mutate(FilterExchange = '1')
)  %>%
    filter(port == 'LS') %>%
    select(signalname, date, ret, Nstocks)

checkport(ls,c('signalname'))

writestandard(ls, pathDataPortfolios, 'CheckPredictorLS_LiqScreen_NYSEonly.csv')



## VW
print('CheckLiq: VW force =========================================')
ls = loop_over_strategies(
    strategylist0 %>% mutate(weight_me = 1)
)  %>%
    filter(port == 'LS') %>%
    select(signalname, date, ret, Nstocks)

checkport(ls,c('signalname'))

writestandard(ls, pathDataPortfolios, 'CheckPredictorLS_LiqScreen_VWforce.csv')


