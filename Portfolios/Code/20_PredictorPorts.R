# For baseline portfolio tests
# Andrew Chen 2020 01

### ENVIRONMENT AND DATA ###
source(paste0(pathProject, "/Portfolios/Code/setup_crspm.r"), echo = T)

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

# reread in case you want to edit the summary later
port = read.csv(paste0(pathDataPortfolios, "PredictorPortsFull.csv"))

sumbase <- sumportmonth(
    port,
    groupme = c("signalname", "port", "samptype"), Nstocksmin = 1
) %>%
    left_join(
        alldocumentation
      , by = "signalname"
    )

sumshort = sumbase %>%
    filter(
        samptype == "insamp",
        port == "LS"
    ) %>%
    arrange(
        signalname
    ) %>%
    select(-signallag)

## export
write_xlsx(
  list(
    short = sumshort
    , full = sumbase
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
  sumbase %>% filter(is.na(port)) %>% arrange(tstat) %>% as.data.frame() %>%
  select(signalname,port)
)
