# For liquidity screen variations on baseline portfolio tests
# takes about 2 hours, but outputs data every 30 min
# Andrew Chen 2020 01

rm(list = ls())

### ENVIRONMENT AND DATA ###
pathProject = getwd()

tryCatch(
  source(paste0(pathProject, '/Portfolios/Code/00_SettingsAndTools.R')),
  error = function(cond) {
    message("Error: 00_SettingsAndTools.R not found.  please setwd to pathProject/Portfolios/Code/")
  }
)

source(paste0(pathProject, '/Portfolios/Code/01_PortfolioFunction.R'))

source(paste0(pathProject, "/Portfolios/Code/setup_crspm.r"), echo = T)

######################################################################
### SELECT SIGNALS
######################################################################
# 2021 01 I took out the portperiod == 1 requirement and added likely predictors
strategylist0 <- alldocumentation %>% filter(Cat.Signal == "Predictor")
strategylist0 <- ifquickrun()

#####################################################################
### BASE LS PERFORMANCE BY LIQUIDITY SCREEN
#####################################################################

print("CheckLiq: ME > NYSE 20 pct =========================================")

## ME > NYSE 20th pct
# create ME screen
# customscreen is used on the signal df, which is then lagged, so no look ahead here
ls <- loop_over_strategies(
  strategylist0 %>% mutate(filterstr = "me > me_nyse20")
) %>%
  filter(port == "LS")

checkport(ls, c("signalname"))

writestandard(
  ls %>%
    select(signalname, date, ret, Nlong, Nshort),
  pathDataPortfolios, "CheckPredictorLS_LiqScreen_ME_gt_NYSE20pct.csv"
)


## Price > 5
print("CheckLiq: Price > 5  =========================================")
ls <- loop_over_strategies(
  strategylist0 %>% mutate(filterstr = "abs(prc) > 5")
) %>%
  filter(port == "LS")

writestandard(
  ls %>%
    select(signalname, date, ret, Nlong, Nshort),
  pathDataPortfolios, "CheckPredictorLS_LiqScreen_Price_gt_5.csv"
)


## NYSE only

print("CheckLiq: NYSE only =========================================")
ls <- loop_over_strategies(
  strategylist0 %>% mutate(filterstr = "exchcd==1")
) %>%
  filter(port == "LS")

checkport(ls, c("signalname"))

writestandard(
  ls %>%
    select(signalname, date, ret, Nlong, Nshort),
  pathDataPortfolios, "CheckPredictorLS_LiqScreen_NYSEonly.csv"
)



## VW
print("CheckLiq: VW force =========================================")
ls <- loop_over_strategies(
  strategylist0 %>% mutate(sweight = "VW")
) %>%
  filter(port == "LS")

checkport(ls, c("signalname"))

writestandard(
  ls %>%
    select(signalname, date, ret, Nlong, Nshort),
  pathDataPortfolios, "CheckPredictorLS_LiqScreen_VWforce.csv"
)
