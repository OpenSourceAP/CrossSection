# Computes placebo portfolios
# Andrew Chen 2020 01

# ==== ENVIRONMENT AND DATA ====
crspinfo = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspminfo.fst')
) %>% # me, screens, 
  setDT()
crspret = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspmret.fst')
) %>% # returns
  setDT()


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
