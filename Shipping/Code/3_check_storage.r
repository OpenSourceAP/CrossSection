# andrew 2021 03
# used for checking what's in what csv
# source without echo pls

# ENVIRONMENT ####

print('pathStorage is ')
print(pathStorage)


sink(paste0(pathStorage,'storage_checks.txt'),append=F)
print('Checking storage for completeness and basic statistics')
print(Sys.time())
cat('\n\n')


alldoc = readdocumentation()
doc_predictor = alldoc %>% filter(Cat.Signal=='Predictor') %>% select(signalname) %>% mutate(indoc=1)
doc_predictor_dl = doc_predictor %>% filter(!signalname %in% c('Price','STreversal','Size'))
doc_placebo = alldoc %>% filter(Cat.Signal=='Placebo') %>% select(signalname) %>% mutate(indoc=1)


# goes in order of the data release documentation

# ==== SIGNAL FULL SETS ==== 

print(' === SIGNAL FULL SETS === ')
cat('\n\n')
print(Sys.time())


## Check Full Sets Predictors Indiv
tempdir = 'Firm Level Characteristics/Full Sets/PredictorsIndiv.zip'
tempdoc = doc_predictor_dl

store_list = unzip(paste0(pathStorage,tempdir), files = 'noextractionpls', list = T) %>%
  mutate(
    signalname = basename(Name), signalname = str_remove(signalname,'.csv') 
  ) %>%
  mutate(intarget = 1) %>%
  select(signalname,intarget,everything())

listcomp = full_join(tempdoc,store_list)
mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget)) %>% arrange(indoc,signalname)


print('The following files are mismatched in ')
print(tempdir)
print(as.data.frame(mismatch))
cat('\n\n')


## Check Full Sets Placebos Indiv
tempdir = 'Firm Level Characteristics/Full Sets/PlacebosIndiv.zip'
tempdoc = doc_placebo

store_list = unzip(paste0(pathStorage,tempdir), files = 'noextractionpls', list = T) %>%
  mutate(
    signalname = basename(Name), signalname = str_remove(signalname,'.csv') 
  ) %>%
  mutate(intarget = 1) %>%
  select(signalname,intarget,everything())

listcomp = full_join(tempdoc,store_list)
mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget)) %>% arrange(indoc,signalname)

print('The following files are mismatched in ')
print(tempdir)
print(as.data.frame(mismatch))
cat('\n\n')

# ==== CHECK WIDE SIGNALS ====

# unzip and read in
unzip(
  paste0(pathStorage, 'Firm Level Characteristics/Full Sets/signed_predictors_dl_wide.zip')
  , exdir = '../Data/temp'
)
signals = fread(paste0('../Data/temp/signed_predictors_dl_wide.csv'))
file.remove(paste0('../Data/temp/signed_predictors_dl_wide.csv'))

# ####

# check 

# ####

tempdoc = doc_predictor_dl

# number of years with data 
obs = signals %>% group_by(yyyymm) %>% summarize_all(funs(sum(!is.na(.))))
mat = as.matrix(obs %>% select(-c(permno)))

store_list = tibble(
  signalname = colnames(mat)
  , years_w_data = colSums(mat > 0) /12
) %>%
  filter(signalname != 'yyyymm') %>%
  mutate(intarget = 1)

listcomp = full_join(tempdoc,store_list)
mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget)) %>% arrange(indoc,signalname)

print('The following files are mismatched in signed_predictors_dl_wide.zip')
print(as.data.frame(mismatch))
cat('\n\n')


  # ####




# n firms per month
firmobs_per_month =  colSums(mat) / colSums(mat>0) 

firmobs_per_month %>% as.data.frame %>%
  setnames(.,'nfirms_per_month') %>%
  arrange(nfirms_per_month) %>%
  head(40)



sink()
stop()


# ==== SIGNAL INDIVIDUAL ====


print(' === SIGNAL INDIVIDUAL CSVS BY FOLDER === ')
cat('\n\n')
print(Sys.time())

tempdir = 'Firm Level Characteristics/Individual/Predictors'
tempdoc = doc_predictor_dl

store_list = list.files(paste0(pathStorage,tempdir)) %>%
  as_tibble() %>%
  mutate(
    signalname = basename(value), signalname = str_remove(signalname,'.csv') 
  ) %>%
  mutate(intarget = 1) %>%
  select(signalname,intarget,everything())

listcomp = full_join(tempdoc,store_list)
mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget)) %>% arrange(indoc,signalname)


print('The following files are mismatched in ')
print(tempdir)
print(as.data.frame(mismatch))
cat('\n\n')


tempdir = 'Firm Level Characteristics/Individual/Placebos'
tempdoc = doc_placebo

store_list = list.files(paste0(pathStorage,tempdir)) %>%
  as_tibble() %>%
  mutate(
    signalname = basename(value), signalname = str_remove(signalname,'.csv') 
  ) %>%
  mutate(intarget = 1) %>%
  select(signalname,intarget,everything())

listcomp = full_join(tempdoc,store_list)
mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget)) %>% arrange(indoc,signalname)


print('The following files are mismatched in ')
print(tempdir)
print(as.data.frame(mismatch))
cat('\n\n')

# ==== SCRATCH ====
### SIGNAL FILES


### PORTFOLIOS FILES
list.files(paste0(pathProject, '/Portfolios/Data/Portfolios/'))
temp = fread(paste0(pathProject, 'Portfolios/Data/Portfolios/PredictorPortsFull.csv'))


temp %>% filter(date == '2020-12-31') %>% filter(!is.na(ret)) %>% distinct(signalname, .keep_all=T)

lastobs = temp %>%
    filter(port == 'LS', !is.na(ret)) %>%
    arrange(signalname, desc(date)) %>%
    group_by(signalname) %>%
    filter(row_number() == 1) %>%
    transmute(signalname, last_ret_obs = date) %>%
    arrange(last_ret_obs) %>%
    as.data.frame
   
lastobs %>% group_by(last_ret_obs) %>% summarize(n())

temp %>% filter(signalname == 'fgr5yrLag', date >= '1982-01-01') %>%
    group_by(port) %>% summarize(mean(ret))
    xxx


### WIDE SIGNALS
raw = fread(paste0(pathStorage,'temp/signed_predictors_all_wide.csv'))
raw = raw %>% select(-c(V1))

## check signals are all there
library(readxl)
signaldoc = read_xlsx(paste0(pathProject,'SignalDocumentation.xlsx'), sheet = 'BasicInfo')
inwide = names(raw %>% select(-c(permno,yyyymm))) %>% as_tibble() %>%
    transmute(Acronym = value, inwide = T)
indoc = signaldoc %>% filter(Cat.Signal == 'Predictor') %>% select(Acronym) %>%
    mutate(indoc = T)
namecheck = full_join(   
    indoc, inwide
) %>%
    mutate_all(list(~ifelse(is.na(.), F, .)))

# list matches and missing
namecheck %>% as.data.frame
namecheck %>% filter(!inwide)

