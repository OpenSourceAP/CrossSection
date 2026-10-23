# Run: source from master.R after configuration and CRSP processing.
# Inputs: processed monthly CRSP, signal CSVs and SignalDoc.csv.
# Outputs: placebo portfolio CSVs and PlaceboSummary.xlsx, under the configured output root.
# Worker count: portfolio_config$resources in config.R.

# Computes placebo portfolios
# Andrew Chen 2020 01

# ==== ENVIRONMENT AND DATA ====
# workers load monthly stock info and reread returns per signal
crspretpath = paste0(pathDataIntermediate, 'crspmret.fst')


######################################################################
### SELECT SIGNALS
######################################################################
strategylist0 <- alldocumentation %>% filter(Cat.Signal == "Placebo")
strategylist0 <- ifquickrun()

#####################################################################
### COMPUTE PORTFOLIOS
#####################################################################

portmonth <- loop_over_strategies(
  strategylist0
  , stage = 'monthly'
)

## EXPORT
writestandard(
  portmonth,
  pathDataPortfolios,
  "PlaceboPortsFull.csv"
)


# SUMMARY STATS BY SIGNAL -------------------------------------------------

sumbase <- sumportmonth(
  portmonth,
  groupme = c("signalname", "port", "samptype"), Nstocksmin = 20
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
  paste0(pathDataPortfolios, "PlaceboSummary.xlsx")
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
