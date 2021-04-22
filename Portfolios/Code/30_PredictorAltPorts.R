# ==== ENVIRONMENT AND DATA ====
crspinfo = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspminfo.fst')
) %>% # me, screens, 
  setDT()
crspret = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspmret.fst')
) %>% # returns
  setDT()


# SELECT SIGNALS 

strategylist0 <- alldocumentation %>% filter(Cat.Signal == "Predictor")
strategylist0 <- ifquickrun()


#### ALT HOLDING PERIODS ####

holdperlist <- c(1, 3, 6, 12)

for (i in seq(1, length(holdperlist))) {
  print(paste0(
    "Running portperiod = ",
    holdperlist[i],
    " ======================================="
  ))
  
  port <- loop_over_strategies(
    strategylist0 %>% mutate(portperiod = holdperlist[i])
  ) 
  
  checkport(port, c("signalname"))
  
  writestandard(
    port,
    pathDataPortfolios,
    paste0("PredictorAltPorts_HoldPer_", holdperlist[i], ".csv")
  )
} # for i


#### ALT LIQUIDITY ADJUSTMENTS ####

print("CheckLiq: ME > NYSE 20 pct =========================================")

## ME > NYSE 20th pct
# create ME screen
# customscreen is used on the signal df, which is then lagged, so no look ahead here
port <- loop_over_strategies(
  strategylist0 %>% mutate(filterstr = "me > me_nyse20")
)
checkport(port, c("signalname"))
writestandard(
  port,
  pathDataPortfolios, "PredictorAltPorts_LiqScreen_ME_gt_NYSE20pct.csv"
)


## Price > 5
print("CheckLiq: Price > 5  =========================================")
port <- loop_over_strategies(
  strategylist0 %>% mutate(filterstr = "abs(prc) > 5")
)
writestandard(
  port,
  pathDataPortfolios, "PredictorAltPorts_LiqScreen_Price_gt_5.csv"
)


## NYSE only

print("CheckLiq: NYSE only =========================================")
port <- loop_over_strategies(
  strategylist0 %>% mutate(filterstr = "exchcd==1")
)
checkport(port, c("signalname"))
writestandard(
  port,
  pathDataPortfolios, "PredictorAltPorts_LiqScreen_NYSEonly.csv"
)



## VW
print("CheckLiq: VW force =========================================")
port <- loop_over_strategies(
  strategylist0 %>% mutate(sweight = "VW")
)
checkport(port, c("signalname"))
writestandard(
  port,
  pathDataPortfolios, "PredictorAltPorts_LiqScreen_VWforce.csv"
)


#### ALT QUANTILES ####

## DECILE SORTS

strategylistcts = strategylist0 %>% filter(Cat.Form == 'continuous')

# OP stock weighting
port <- loop_over_strategies(
  strategylistcts %>% mutate(q_cut = 0.1)
)

checkport(port, c("signalname", "port"))

writestandard(port, pathDataPortfolios, "PredictorAltPorts_Deciles.csv")

# force value weighting
port <- loop_over_strategies(
  strategylistcts %>% mutate(q_cut = 0.1, sweight = 'VW')
)

checkport(port, c("signalname", "port"))

writestandard(port, pathDataPortfolios, "PredictorAltPorts_DecilesVW.csv")



## QUINTILE SORTS

# OP stock weighting
port <- loop_over_strategies(
  strategylistcts %>% mutate(q_cut = 0.2)
)
checkport(port, c("signalname", "port"))
writestandard(port, pathDataPortfolios, "PredictorAltPorts_Quintiles.csv")

# force value weighting
port <- loop_over_strategies(
  strategylistcts %>% mutate(q_cut = 0.2, sweight = 'VW')
)
checkport(port, c("signalname", "port"))
writestandard(port, pathDataPortfolios, "PredictorAltPorts_QuintilesVW.csv")
