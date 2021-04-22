# Note: daily portfolios currently (2021 04) do not aggregate up to monthly
# because the daily portfolios recalculate stock weights (equal or value-weighting) 
# every day while the monthly portfolios recalculate stock weights every month.

# Note: monthly portfolios are not screened at all for minimum number of stocks
# and instead, we store Nstocks, and then screen for Nstocks when we do summary stats
# However, to keep the daily portfolios data of a manageable size
# we do not store Nlong and Nshort, and instead impose the screen at the portfolio 
# level.  

# takes about 1.5 hours per implementation, or about 10 hours total

### ENVIRONMENT AND DATA ####
start_time = Sys.time()

# minimum number of stocks in a portfolio
# for now set to 1 (2021 04), matching baseline
# setting to 20 removes IO_ShortInterest portfolios
Nstocksmin = 1

### load crsp returns
crspinfo = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspminfo.fst')
) %>% # me, screens, 
  setDT()
crspret = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspdret.fst')
) %>% # returns
  setDT()

### SET UP PATHS

# since no other files use these paths, they don't go in 00_Settings*.R
pathDataDaily  = paste0(pathProject, 'Portfolios/Data/DailyPortfolios/')
pathDataDailyBase   = paste0(pathDataDaily, 'Predictor/')
pathDataDailyBaseVW   = paste0(pathDataDaily, 'PredictorVW/')
pathDataDailyDecile = paste0(pathDataDaily, 'CtsPredictorDecile/')
pathDataDailyDecileVW  = paste0(pathDataDaily, 'CtsPredictorDecileVW/')
pathDataDailyQuintile = paste0(pathDataDaily, 'CtsPredictorQuintile/')
pathDataDailyQuintileVW  = paste0(pathDataDaily, 'CtsPredictorQuintileVW/')

dir.create(pathDataDaily)
dir.create(pathDataDailyBase)
dir.create(pathDataDailyBaseVW)
dir.create(pathDataDailyDecile)
dir.create(pathDataDailyDecileVW)
dir.create(pathDataDailyQuintile)
dir.create(pathDataDailyQuintileVW)

# since no other script uses lme4, it should go here.
install.packages(setdiff(c('lme4'), rownames(installed.packages())))
library(lme4)


### SELECT SIGNALS
strategylist0 = alldocumentation %>% filter(Cat.Signal == 'Predictor')
strategylist0 = ifquickrun()

strategylistcts = strategylist0 %>% filter(Cat.Form == 'continuous')




### BASELINE ####

## BASELINE
print('50_DailyPredictorPorts.R: predictor baseline strats')

port = loop_over_strategies(
    strategylist0
  , saveportcsv = T
  , saveportpath = pathDataDailyBase
  , saveportNmin = Nstocksmin
  , passive_gain = T
)

## BASELINE
print('50_DailyPredictorPorts.R: predictor baseline VW')

port = loop_over_strategies(
  strategylist0 %>% mutate(sweight = 'VW' )
  , saveportcsv = T
  , saveportpath = pathDataDailyBaseVW
  , saveportNmin = Nstocksmin
  , passive_gain = T  
)

Sys.time()
    


### DECILES ####


## FORCE DECILES
print ('50_DailyPredictorPorts.R: predictor force decile strats')
port = loop_over_strategies(
    strategylistcts %>% mutate(q_cut = 0.1)
  , saveportcsv = T
  , saveportpath = pathDataDailyDecile
  , saveportNmin = Nstocksmin    
  , passive_gain = T  
)


## FORCE DECILES AND VW
print ('50_DailyPredictorPorts.R: predictor force decile and VW strats')
port = loop_over_strategies(
    strategylistcts %>% mutate(q_cut = 0.1, sweight = 'VW')
  , saveportcsv = T
  , saveportpath = pathDataDailyDecileVW
  , saveportNmin = Nstocksmin        
  , passive_gain = T  
)

Sys.time()

### QUINTILES ####

## FORCE QUINTILES
print ('50_DailyPredictorPorts.R: predictor force quint strats')
port = loop_over_strategies(
  strategylistcts %>% mutate(q_cut = 0.2)
  , saveportcsv = T
  , saveportpath = pathDataDailyQuintile
  , saveportNmin = Nstocksmin    
  , passive_gain = T  
)


## FORCE QUINTILES AND VW
print ('50_DailyPredictorPorts.R: predictor force quint and VW strats')
port = loop_over_strategies(
  strategylistcts %>% mutate(q_cut = 0.2, sweight = 'VW')
  , saveportcsv = T
  , saveportpath = pathDataDailyQuintileVW
  , saveportNmin = Nstocksmin        
  , passive_gain = T  
)

print('50_DailyPredictorPorts.R done!')
end_time = Sys.time()

print('start time, end time = ')
print(start_time)
print(end_time)


# CHECK CSVS ####
# this creates DailyPortSummary.xlsx

### FUNCTION FOR CHECKING A WHOLE FOLDER OF DAILY RETURNS
checkdir = function(dircurr){
  
  sumsignal = tibble()
  for (signalcurr in csvlist$signalname){
    retd = fread(paste0(pathDataDaily,dircurr,'/',signalcurr,'_ret.csv')) %>%
      gather(port,'ret',-date) %>%
      filter(!is.na(ret))
    tempstat = retd %>% group_by(port) %>% 
      summarize(
        nobs_years = n()/250
        , rbar_monthly = mean(ret,na.rm=T)*20
      ) %>%
      mutate(signalname = signalcurr)
    sumsignal = rbind(sumsignal,tempstat)
  }
  
  sumdir = sumsignal %>% group_by(port) %>% 
    summarize(
      n_distinct(signalname)
      ,mean(nobs_years)
      ,mean(rbar_monthly)
    ) %>%
    mutate(implementation = dircurr)
  
} # end function checkdir


print(paste0('Checking on Daily Port stats ', Sys.time()))
dirlist = list.dirs(pathDataDaily, full.names=F)
dirlist = dirlist[dirlist != ''] 

### check for completeness of daily portfolio csvs and summary stats
sumdaily = tibble()
for (dircurr in dirlist){
  
  print(paste0('checking on ', dircurr))
  
  csvlist = list.files(paste0(pathDataDaily,dircurr,'/' )) %>%
    as_tibble() %>%
    transmute(
      signalname = str_remove(value, '_ret.csv')
      , incsv = 1
    )
  
  ## check for mismatches in signal lists
  if (substr(dircurr,1,3) == 'Cts'){
    doclist = strategylistcts %>% select(signalname) %>% mutate(indoc = 1)
  } else {
    doclist = strategylist0 %>% select(signalname) %>% mutate(indoc = 1)
  } # substr(dircurr,1,3)
  
  mismatch = full_join(doclist, csvlist) %>%
    filter(is.na(indoc) | is.na(incsv))
  
  if (dim(mismatch)[1]>0){
    print(paste0('Warning: mismatch between signal docs and csvs for '))
    print(paste0(pathDataDaily,dircurr,'/' ))
    print(mismatch)
    
  } # if there's a mismatch
  

  ## check summary stats 
  sumdir = checkdir(dircurr)
  print(paste0('Summary of ', dircurr))
  print(sumdir)
  sumdaily = rbind(sumdaily,sumdir)

} # for dircurr

### check timing of daily predictor ports (base) with monthly returns 
portmonthly = fread(paste0(pathDataPortfolios, 'PredictorPortsFull.csv')) %>%
  transmute(signalname, port, datem = as.Date(date), retm = ret)

dircurr = 'Predictor'

csvlist = list.files(paste0(pathDataDaily,dircurr,'/' )) %>%
  as_tibble() %>%
  transmute(
    signalname = str_remove(value, '_ret.csv')
    , incsv = 1
  )
signallist = csvlist$signalname

print('checking daily vs monthly return timing')
reg_retm_retmagg = tibble()
for (signalcurr in signallist){
  
  print(signalcurr)
  
  # read daily 
  temp = fread(paste0(pathDataDaily,dircurr,'/',signalcurr,'_ret.csv'))
  if (dim(temp)[1]>0){
    # aggregate to monthly  
    datd = temp %>%
      gather(port,'ret',-date) %>%
      mutate(port = substr(port, 5,6)) %>%
      filter(!is.na(ret)) %>%
      mutate(datem = ceiling_date(date, 'month') - days(1)) %>%
      group_by(datem, port) %>%
      summarize(retm_agg = 100*(prod(1+ret/100)-1)) 

    datboth = portmonthly %>%
      filter(signalname == signalcurr) %>%
      left_join(datd, by=c('port','datem')) %>% 
      filter(!is.na(retm_agg))
    
    # remove port if too few observations
    temp = datboth %>% group_by(port) %>% summarize(nobs = sum(!is.na(retm))) %>%
      filter(nobs>10)
    datboth = datboth %>% filter(port %in% temp$port)
    
    # regress monthly on daily aggregated to monthly
    temp = lmList(retm~retm_agg|port,data=datboth)
    reg_curr = tibble(
      signalname = signalcurr
      , port = rownames(coef(temp))
      , intercept = coef(temp)[,1]
      , slope = coef(temp)[,2]
      , rsq = summary(temp)$r.squared
    )
  } else {
    # here the return file is empty, probably because not enough stocks in the portfolio
    reg_curr[] = NA
    reg_curr = reg_curr[1,] %>% mutate(signalname = signalcurr)
  }
  
  # append
  reg_retm_retmagg = rbind(reg_retm_retmagg, reg_curr)
}

# summarize regressions
reg_sum = reg_retm_retmagg %>% 
  group_by(port) %>%
  filter(!is.na(slope)) %>%
  summarize(
    quantile(slope, 0.1)
    , quantile(slope, 0.5)
    , quantile(rsq, 0.1)
    , quantile(rsq, 0.5)    
  )
  
### output

write_xlsx(
  list(
    sumstats = sumdaily %>% 
      select(implementation,everything()) %>%
      arrange(implementation,port)
    , timingcheck = reg_sum
  )
  , paste0(pathDataDaily, 'DailyPortSummary.xlsx')
)

print(paste0('Done: Checking on Daily Port stats ', Sys.time()))
