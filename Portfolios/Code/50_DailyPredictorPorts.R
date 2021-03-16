
### ENVIRONMENT AND DATA ###
source(paste0(pathProject, "/Portfolios/Code/setup_crspd.r"), echo = T)


######################################################################
### SET UP PATHS
######################################################################

# since no other files use these paths, they don't go in 00_Settings*.R
pathDataDaily  = paste0(pathProject, 'Portfolios/Data/DailyPortfolios/')
pathDataDailyBase   = paste0(pathDataDaily, 'Predictor/')
pathDataDailyDecile = paste0(pathDataDaily, 'CtsPredictorDecile/')
pathDataDailyDecileVW  = paste0(pathDataDaily, 'CtsPredictorDecileVW/')

dir.create(pathDataDaily)
dir.create(pathDataDailyBase)
dir.create(pathDataDailyDecile)
dir.create(pathDataDailyDecileVW)


######################################################################
### SELECT SIGNALS
######################################################################
strategylist0 = alldocumentation %>% filter(Cat.Signal == 'Predictor')
strategylist0 = ifquickrun()

strategylist1 = strategylist0 %>% filter(!is.na(q_cut))

######################################################################
### DO STUFF
######################################################################

## BASELINE
print('50_DailyPredictorPorts.R: predictor baseline strats')

port = loop_over_strategies(
    strategylist0
  , saveportcsv = T
  , saveportpath = pathDataDailyBase
  , saveportNmin = 20
)

checkport(port)

## writestandard(
##     port
##     , pathDataPortfolios
##     , 'DailyPredictorPorts.csv'
## )
    
######################################################################
### NON BINARY ONLY
######################################################################
# 40 sec per port, 2 hours for all predictors

## FORCE DECILES
print ('50_DailyPredictorPorts.R: predictor force decile strats')
port = loop_over_strategies(
    strategylist1 %>% mutate(q_cut = 0.1)
  , saveportcsv = T
  , saveportpath = pathDataDailyDecile
  , saveportNmin = 20    
)

checkport(port)
    

## FORCE DECILES AND VW
print ('50_DailyPredictorPorts.R: predictor force decile and VW strats')
port = loop_over_strategies(
    strategylist1 %>% mutate(q_cut = 0.1, sweight = 'VW')
  , saveportcsv = T
  , saveportpath = pathDataDailyDecileVW
  , saveportNmin = 20        
)

checkport(port)
    
