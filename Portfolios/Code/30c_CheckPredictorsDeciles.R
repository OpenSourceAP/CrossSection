### ENVIRONMENT AND DATA ###
source(paste0(pathProject, "/Portfolios/Code/setup_crspm.r"), echo = T)


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


writestandard(port, pathDataPortfolios, "CheckPredictorPorts_Deciles.csv")



## QUINTILE SORTS
port <- loop_over_strategies(
  strategylist0 %>% mutate(q_cut = 0.2)
)

checkport(port, c("signalname", "port"))


writestandard(port, pathDataPortfolios, "CheckPredictorPorts_Quintiles.csv")
