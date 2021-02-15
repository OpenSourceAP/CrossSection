# For holding period variations on baseline portfolio tests
# takes about 2 hours, but outputs data every 30 min
# Andrew Chen 2020 01

rm(list = ls())

### ENVIRONMENT AND DATA ###

tryCatch(
  source("00_SettingsAndTools.R"),
  error = function(cond) {
    message("Error: 00_SettingsAndTools.R not found.  please setwd to pathProject/Portfolios/Code/")
  }
)
source('01_PortfolioFunction.R')

source(paste0(pathProject, "Portfolios/Code/setup_crspm.r"), echo = T)

######################################################################
### SELECT SIGNALS
######################################################################
strategylist0 <- alldocumentation %>% filter(Cat.Signal == "Predictor")
strategylist0 <- ifquickrun()


######################################################################
### BASE LS PERFORMANCE BY HOLDING PERIOD
######################################################################


holdperlist <- c(1, 3, 6, 12)
## holdperlist = c(3)

for (i in seq(1, length(holdperlist))) {
  print(paste0(
    "Running portperiod = ",
    holdperlist[i],
    " ======================================="
  ))

  ls_curr <- loop_over_strategies(
    strategylist0 %>% mutate(portperiod = holdperlist[i])
  ) %>%
    filter(port == "LS")

  checkport(ls_curr, c("signalname"))

  writestandard(
    ls_curr %>%
      select(signalname, date, ret, Nlong, Nshort),
    pathDataPortfolios,
    paste0("CheckPredictorLS_HoldPer_", holdperlist[i], ".csv")
  )
} # for i
