# For baseline portfolio tests
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
### SELECT SIGNALS AND CHECK FOR CSVS
######################################################################

strategylist0 <- alldocumentation %>% filter(Cat.Signal == "Predictor")
strategylist0 <- ifquickrun()

csvlist = list.files(pathPredictors) %>% as_tibble() %>% rename(signalname=value) %>%
  mutate(
    signalname = substr(signalname,1,str_length(signalname)-4)
    , in_csv = 1
  )

missing = strategylist0 %>% select(signalname) %>% left_join(csvlist) %>%
  filter(is.na(in_csv)) # note: CRSP predictors are put into pathPredictors by 11_CreateCRSPPredictors.R

if (dim(missing)[1]>0){
  print('Warning: the following predictor signal csvs are missing:')
  print(missing$signalname)
  
  temp = readline('press enter to continue, type quit to quit: ')
  if (temp=='quit'){print('erroring out'); stop()}
}


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
  pivot_wider(names_from = signalname, values_from = ret) %>%
  arrange(date)

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

if (dim(sumbase %>% filter(is.na(port)))[1] == 0){
  print('20_PredictorPorts.R: all portfolios successfully computed')
}

