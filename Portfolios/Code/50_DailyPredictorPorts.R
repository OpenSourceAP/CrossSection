# Run: source from master.R after configuration and CRSP processing.
# Inputs: processed daily CRSP, monthly stock information, signals and baseline monthly portfolios.
# Outputs: six daily CSV families and DailyPortSummary.xlsx, under the configured output root.
# Worker count: portfolio_config$resources in config.R.

# Note: daily portfolios currently (2021 04) do not aggregate up to monthly
# because the daily portfolios recalculate stock weights (equal or value-weighting) 
# every day while the monthly portfolios recalculate stock weights every month.

# The six configurations run as independent jobs on parallel workers; the number
# of workers comes from portfolio_n_workers('daily') in config.R. Each
# configuration takes about 1.5 hours.

### ENVIRONMENT AND DATA ####
start_time = Sys.time()

Nstocksmin = portfolio_config$daily$min_stocks

# the timing check below compares against the baseline monthly portfolios;
# check before spending hours on daily portfolios
if (!file.exists(paste0(pathDataPortfolios, 'PredictorPortsFull.csv'))) {
  stop('50_DailyPredictorPorts.R needs baseline monthly portfolios: run 20_PredictorPorts.R first')
}

# returns are reread per signal by signalname_to_ports
crspretpath = paste0(pathDataIntermediate, 'crspdret.fst')

### SET UP PATHS

# Configuration-specific subfolders below share the configured daily output root.
# pathDataDaily is resolved from the configured output root by master.R.
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

# Dependencies are checked by master.R; never install during a build.
library(lme4)

### SELECT SIGNALS
strategylist0 = alldocumentation %>% filter(Cat.Signal == 'Predictor')
strategylist0 = ifquickrun()

strategylistcts = strategylist0 %>% filter(Cat.Form == 'continuous')


### DAILY CONFIGURATIONS ####
# Workers take configurations in this order, so the baselines start first.
daily_jobs = list(
  baseline = list(
    strategylist = strategylist0
    , saveportpath = pathDataDailyBase
  )
  , baseline_vw = list(
    strategylist = strategylist0 %>% mutate(sweight = 'VW')
    , saveportpath = pathDataDailyBaseVW
  )
  , decile = list(
    strategylist = strategylistcts %>% mutate(q_cut = 0.1)
    , saveportpath = pathDataDailyDecile
  )
  , decile_vw = list(
    strategylist = strategylistcts %>% mutate(q_cut = 0.1, sweight = 'VW')
    , saveportpath = pathDataDailyDecileVW
  )
  , quintile = list(
    strategylist = strategylistcts %>% mutate(q_cut = 0.2)
    , saveportpath = pathDataDailyQuintile
  )
  , quintile_vw = list(
    strategylist = strategylistcts %>% mutate(q_cut = 0.2, sweight = 'VW')
    , saveportpath = pathDataDailyQuintileVW
  )
)

# One configuration's signal loop, run serially in a worker. Portfolios are
# saved as CSVs; only the output path returns to this session.
run_daily_configuration = function(job){
  port = loop_over_strategies(
    job$strategylist
    , saveportcsv = T
    , saveportpath = job$saveportpath
    , saveportNmin = Nstocksmin
    , passive_gain = T
  )
  job$saveportpath
}

# Each worker loads packages, portfolio functions and monthly stock info once.
# Daily returns are not loaded here: signalname_to_ports rereads them per signal.
setup_daily_worker = function(){
  options(stringsAsFactors = FALSE, dplyr.summarise.inform = FALSE
          , scipen = 999) # scipen sets number formatting in the saved CSVs
  suppressPackageStartupMessages({
    library(tidyverse)
    library(data.table)
    library(fst)
  })
  source(paste0(pathCode, '01_PortfolioFunction.R'))
  crspinfo <<- read.fst(paste0(pathDataIntermediate, 'crspminfo.fst')) %>% # me, screens, 
    setDT()
}

print('50_DailyPredictorPorts.R: running daily configurations in parallel')
daily_paths = portfolio_run_jobs(
  'daily'
  , daily_jobs
  , run_daily_configuration
  , setup = setup_daily_worker
  , globals = list(
    pathCode = pathCode, pathDataIntermediate = pathDataIntermediate
    , pathPredictors = pathPredictors, pathCRSPPredictors = pathCRSPPredictors
    , pathPlacebos = pathPlacebos, pathtemp = pathtemp
    , crspretpath = crspretpath, feed.verbose = feed.verbose, Nstocksmin = Nstocksmin
    , loop_over_strategies = loop_over_strategies, writestandard = writestandard
  )
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
