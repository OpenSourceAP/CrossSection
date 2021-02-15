# For baseline portfolio tests
# Andrew Chen 2020 01

rm(list = ls())

### ENVIRONMENT AND DATA ###

source("00_SettingsAndFunctions.R", echo = T)

source(paste0(pathProject, "Portfolios/Code/setup_crspm.r"), echo = T)

######################################################################
### SELECT SIGNALS
######################################################################

strategylist0 <- alldocumentation %>% filter(Cat.Signal == "Predictor")
strategylist0 <- ifquickrun()


#####################################################################
### BASE PORTS
#####################################################################
port <- loop_over_strategies(
  strategylist0
)

# feedback
checkport(port)


## EXPORT
writestandard(port, pathDataPortfolios, "PredictorPortsFull.csv")

### OUTPUT WIDE ###
portlswide <- port %>%
  filter(port == "LS") %>%
  select(date, signalname, ret) %>%
  pivot_wider(names_from = signalname, values_from = ret)

writestandard(
  portlswide,
  pathDataPortfolios,
  "PredictorLSretWide.csv"
)

# SUMMARY STATS BY SIGNAL -------------------------------------------------

sumbase <- sumportmonth(
  port,
  groupme = c("signalname", "port", "samptype"), Nstocksmin = 1
) %>%
  left_join(
    strategylist0 %>%
      select(
        sweight, q_cut, q_filt, portperiod, startmonth, filterstr,
        everything()
      ),
    by = "signalname"
  )


## export
write_xlsx(
  list(
    ls_insamp_only = sumbase %>%
      filter(
        samptype == "insamp",
        port == "LS"
      ) %>%
      arrange(tstat),
    full = sumbase
  ),
  paste0(pathDataPortfolios, "PredictorSummary.xlsx")
)


# FEEDBACK ON ERRORS -------------------------------------------------

print("The following ports are computed succesfully")
print(
  sumbase %>% filter(port == "LS", samptype == "insamp") %>% arrange(tstat) %>% as.data.frame()
)

print("The following ports failed to compute")
print(
  sumbase %>% filter(is.na(port)) %>% arrange(tstat) %>% as.data.frame()
)
