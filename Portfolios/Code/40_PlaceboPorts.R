# Computes placebo portfolios
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
strategylist0 <- alldocumentation %>% filter(Cat.Signal == "Placebo")
strategylist0 <- ifquickrun()

#####################################################################
### COMPUTE PORTFOLIOS
#####################################################################

portmonth <- loop_over_strategies(strategylist0[79:111, ])

## EXPORT
writestandard(
  portmonth,
  pathDataPortfolios,
  "PlaceboPortsFull.csv"
)


# FEEDBACK ON ERRORS -------------------------------------------------

tempsum <- sumportmonth(
  portmonth,
  groupme = c("signalname", "port", "samptype"), Nstocksmin = 20
)

print("The following ports are computed succesfully")
print(
  tempsum %>% filter(port == "LS", samptype == "insamp") %>% arrange(tstat) %>% as.data.frame()
)

print("The following ports failed to compute")
print(
  tempsum %>% filter(is.na(port)) %>% arrange(tstat) %>% as.data.frame()
)
