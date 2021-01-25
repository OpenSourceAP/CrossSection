# Andrew Chen 2020 01

rm(list = ls())

### ENVIRONMENT AND DATA ###

tryCatch(
  source("00_SettingsAndFunctions.R"),
  error = function(cond) {
    message("Error: 00_SettingsAndFunctions.R not found.  please setwd to pathProject/Portfolios/Code/")
  }
)

source(paste0(pathProject, "Portfolios/Code/setup_crspm.r"), echo = T)

######################################################################
### SELECT SIGNALS
######################################################################
strategylist0 <- alldocumentation %>%
  filter(
    Cat.Signal == "Predictor",
    Cat.Form == "continuous"
  )

strategylist0 <- ifquickrun()

######################################################################
### DO STUFF
######################################################################


## DECILE SORTS
port <- loop_over_strategies(
  strategylist0 %>% mutate(q_cut = 0.1)
)

checkport(port, c("signalname", "port"))
