# andrew 2021 03
# used for checking what's in what csv
# source without echo pls

# goes in order of the data release documentation, except port full sets go first

# ENVIRONMENT, sink to txt ####
options(width=1e3)

print('pathStorage is ')
print(pathStorage)


sink(paste0(pathStorage,'storage_checks.txt'))
print('Checking storage for completeness and basic statistics')
print(Sys.time())
cat('\n\n')


alldoc = readdocumentation()
doc_predictor = alldoc %>% filter(Cat.Signal=='Predictor') %>% select(signalname) %>% mutate(indoc=1)
doc_predictor_dl = doc_predictor %>% filter(!signalname %in% c('Price','STreversal','Size'))
doc_predictor_cts = alldoc %>% filter(Cat.Signal=='Predictor', Cat.Form == 'continuous') %>% 
    select(signalname) %>% mutate(indoc=1)
doc_placebo_dl = alldoc %>% filter(Cat.Signal=='Placebo') %>% 
  select(signalname) %>% mutate(indoc=1) %>% 
  filter(signalname != 'BidAskTAQ')


## function for checking match with SignalDocumentation.xlsx
# used repeatedly here
check_doc = function(tempdir,tempdoc,iszip){

  if (!file.exists(paste0(pathStorage,tempdir))){
    print('error: path is missing for')
    print(paste0(pathStorage,tempdir))
    stop()
  }
  if (iszip){
    store_list0 = unzip(
      paste0(pathStorage,tempdir)
      , files = 'noextractionpls'
      , list = T
      )
  } else {
    store_list0 = list.files(paste0(pathStorage,tempdir)) 
    store_list0 = store_list0[grepl('.csv',store_list0)] %>%
      as.data.frame() %>% rename('Name' = '.')
  }

  store_list = store_list0 %>%
    as_tibble() %>%
    mutate(
      signalname = basename(Name)
      , signalname = str_remove(signalname,'.csv') 
      , signalname = str_remove(signalname,'_ret')
    ) %>%
    mutate(intarget = 1) %>% 
    filter(!grepl('\\/$',Name)) %>% # remove folders
    select(signalname,intarget,everything())  
  
  listcomp = full_join(tempdoc,store_list)
  mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget)) %>% arrange(indoc,signalname)
  
  
  if (dim(mismatch)[1] == 0){
    print('The files in the following folder match SignalDocumentation.xlsx!')
    print(tempdir)
    cat('\n\n')
  } else{
    print('The following files are mismatched in ')
    print(tempdir)
    print(as.data.frame(mismatch))
    
    print('listcomp is ')    
    print(as.data.frame(listcomp))
    
    print('store_list is ')    
    print(as.data.frame(store_list))    
    cat('\n\n')
  }
}


# ==== PORTFOLIO FULL SETS ====

print(' === PORTFOLIO FULL SETS === ')
cat('\n')

## Check timing of baseline 
port = fread(
  paste0(pathStorage,'Portfolios/Full Sets OP/PredictorPortsFull.csv')
)

print('Count of predictors with long-short returns by month')

port %>% 
filter(
  port == 'LS', !is.na(ret), month(date) == 12, year(date) >= 2000
) %>%
  group_by(date) %>%
  summarize(n_distinct(signalname)) %>%
  arrange(desc(date)) %>%
  as.data.frame() %>% 
  print()

cat('\n\n')


# function of summary statistics for full sets
# used only for full sets
check_portfull = function(pathcsv){
  # read in LS, add sample types
  lscurr = fread(pathcsv)[
    port == 'LS'
  ][
    alldoc %>% select(signalname,SampleStartYear,SampleEndYear,Year) %>% data.table()
    , on = c('signalname')
    , ':=' (
      SampleStartYear = SampleStartYear
      , SampleEndYear = SampleEndYear
      , PubYear = Year
    )
  ][
    , samptype := case_when(
      year(date) < SampleStartYear ~ 'before'
      , year(date) >= SampleStartYear & year(date) <= SampleEndYear ~ 'insamp'
      , year(date) > SampleEndYear & year(date) <= PubYear ~ 'between'
      , year(date) > PubYear ~ 'postpub'
    )
  ]
  
  # find mean return for various sample types
  rbar1 = lscurr[
    , .(rbar = mean(ret))
    , by = c('signalname','samptype')
  ] 
  
  rbar2 = lscurr[
    year(date) >= year(Sys.time()) - 5 
    , .(rbar = mean(ret))
    , by = c('signalname')
  ][
    , samptype := 'last5years'
  ]
  
  rbar3 = lscurr[
    year(date) == year(Sys.time()) - 1 
    , .(rbar = mean(ret))
    , by = c('signalname')
  ][
    , samptype := as.character(year(Sys.time()) - 1 ) 
  ]
  
  # merge and format
  rbarall = rbind(rbar1,rbar2,rbar3) %>%
    spread(samptype, rbar, drop = F) %>%
    select(signalname, before, insamp, between, postpub, last5years
           , as.character(year(Sys.time()) - 1))
  
  return(rbarall)
} # end check_portfull

## first check baseline
rbarbase = check_portfull(
  paste0(pathStorage,'Portfolios/Full Sets OP/PredictorPortsFull.csv')
)

## then check alt ports
implist = list.files(
  paste0(pathStorage, 'Portfolios/Full Sets Alt/')
  , pattern = '.zip'
) 

rbarimp = data.frame()
for (impcurr in implist){
  unzip(
    zipfile = paste0(pathStorage, 'Portfolios/Full Sets Alt/', impcurr)
    , exdir = paste0(pathShipping,'Data')
  )
  
  rbarall = check_portfull(
    paste0(pathShipping,'Data/',str_remove(impcurr,'.zip'), '.csv')
  )
  
  # average across signals and save
  rbarimp = rbind(
    rbarimp, 
    rbarall %>% 
      summarise(across(-signalname, mean, na.rm=T)) %>%
      mutate(impname = impcurr) %>%
      select(impname,(everything()))
  )
  
} # for impcurr

# add baseline
rbarimp = rbind(
  rbarimp
  , rbarbase %>% 
    summarise(across(-signalname, mean, na.rm=T)) %>%
    mutate(impname = 'PredictorPortsFull') %>%
    select(impname,(everything()))
)


## output port full set stats

options(max.print = 1e5)   
cat('\n')
print('Summary of portfolio full set mean monthly long-short returns')
rbarimp %>%
  mutate_if(is.numeric, round, digits=2) %>%
  mutate(
    impid = case_when(
      grepl('PredictorPortsFull', impname,) ~ 1
      , grepl('HoldPer', impname,) ~ 2
      , grepl('LiqScreen', impname,) ~ 3
      , grepl('Quintiles', impname,) ~ 4
      , grepl('Deciles', impname,) ~ 5
    )
  ) %>%  
  mutate(
    impname = str_remove(impname,'.zip')
    , impname = str_remove(impname,'PredictorAltPorts_')
    , impname = str_remove(impname,'LiqScreen_')    
  ) %>%  
  arrange(impid, impname) %>% 
  print(right=F)
cat('\n\n')



print('Predictor signal-level mean monthly long-short returns (OP implementations)')
rbarbase %>%
  mutate_if(is.numeric, round, digits=2) %>%
  arrange(signalname) %>% 
  as.data.frame() %>% 
  print(right=F)
cat('\n\n')
options(max.print = 1e3)   

# ==== SIGNAL FULL SETS LONG ==== 

print(' === SIGNAL FULL SETS LONG === ')
cat('\n\n')

check_doc(
  'Firm Level Characteristics/Full Sets/PredictorsIndiv.zip'
  , doc_predictor_dl
  , iszip = T
)

check_doc(
  'Firm Level Characteristics/Full Sets/PlacebosIndiv.zip'
  , doc_placebo_dl
  , iszip = T
)

# ==== SIGNAL FULL SET WIDE ====
# this is a bit slow

# unzip and read in
unzip(
  paste0(pathStorage, 'Firm Level Characteristics/Full Sets/signed_predictors_dl_wide.zip')
  , exdir = '../Data/temp'
)
signals = fread(paste0('../Data/temp/signed_predictors_dl_wide.csv'))
file.remove(paste0('../Data/temp/signed_predictors_dl_wide.csv'))

## check signals are all there
store_list = names(signals) %>% as_tibble() %>% transmute(signalname=value, intarget=1) %>%
  filter(!signalname %in% c('permno','yyyymm'))

listcomp = full_join(doc_predictor_dl,store_list)
mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget)) %>% arrange(indoc,signalname)

if (dim(mismatch)[1] == 0){
  print('signed_predictors_dl_wide.zip matches SignalDocumentation.xlsx!')
  cat('\n\n')
} else{
  print('signed_predictors_dl_wide.zip does not matche SignalDocumentation.xlsx')
  print(as.data.frame(mismatch))
  cat('\n\n')
}


# find data availability in wide signals
# this is an indirect check on the long and other signals
obs = signals %>%
  select(-permno) %>%
  group_by(yyyymm) %>%
  summarize_all(funs(sum(!is.na(.))))

widesum = obs %>% pivot_longer(
  -yyyymm
  , names_to = 'signalname'
  , values_to = 'obs'
) %>%
  filter(obs >= 1) %>%
  group_by(signalname) %>%
  summarize(
    date_begin = min(yyyymm)
    , date_end = max(yyyymm)
    , mean_firmobs_per_month = floor(mean(obs))
  ) %>% as.data.frame()


print('Downloadable signal data availability summary: ')
print(widesum)
cat('\n\n')

# ==== SIGNAL INDIVIDUAL ====


print(' === SIGNAL INDIVIDUAL CSVS BY FOLDER === ')
cat('\n')
print(Sys.time())

check_doc(
  'Firm Level Characteristics/Individual/Predictors'
  , doc_predictor_dl
  , iszip = F
)

check_doc(
  'Firm Level Characteristics/Individual/Placebos'
  , doc_placebo_dl
  , iszip = F
)

# ==== PORTFOLIO INDIVIDUAL ====

print(' === PORTFOLIO INDIVIDUAL CSVS BY FOLDER === ')
cat('\n')

check_doc(
  'Portfolios/Individual/Original_Cuts'
  , doc_predictor
  , iszip = F
)

check_doc(
  'Portfolios/Individual/Original_CutsVW'
  , doc_predictor
  , iszip = F
)

implist = c(
  'Cts_Deciles'
  , 'Cts_DecilesVW'
  , 'Cts_Quintiles'
  , 'Cts_QuintilesVW'  
)

for (impcurr in implist){
  check_doc(
    paste0('Portfolios/Individual/', impcurr)
    , doc_predictor_cts
    , iszip = F
  )
}

cat('\n\n')



# ==== DAILY PORTFOLIOS ====
print(' === PORTFOLIO INDIVIDUAL CSVS BY FOLDER === ')
cat('\n')

check_doc(
  'DailyPortfolios/Predictor.zip'
  , doc_predictor
  , iszip = T
)
check_doc(
  'DailyPortfolios/PredictorVW.zip'
  , doc_predictor
  , iszip = T
)


implist = c(
  'CtsPredictorDecile'
  , 'CtsPredictorDecileVW'
  , 'CtsPredictorQuintile'
  , 'CtsPredictorQuintileVW'  
)

for (impcurr in implist){
  check_doc(
    paste0('DailyPortfolios/', impcurr, '.zip')
    , doc_predictor_cts
    , iszip = T
  )
}

# restore output to console ====
sink()
