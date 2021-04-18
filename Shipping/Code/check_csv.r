# andrew 2021 03
# used for checking what's in what csv

print('pathStorage is ')
print(pathStorage)

alldoc = readdocumentation()

# CHECK FOR COMPLETENESS ####

# ####

# to do: apply to other datasets, output to xlsx

## check for mismatches between doc and predictor csvs
dirstr = pathPredictors
catstr = 'Predictor'

csvlist = list.files(dirstr) %>% as_tibble() %>%
  transmute(signalname = str_remove(value, '.csv'), intarget = 1)
doclist = alldoc %>% filter(Cat.Signal==catstr) %>% select(signalname) %>% mutate(indoc = 1)
listcomp = full_join(doclist, csvlist) 
mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget))
print('The following signals are mismatched in ')
print(dirstr)
mismatch

# ####

## check for mismatches between doc and placebo csvs
csvlist =   list.files(pathPlacebos) %>% as_tibble() %>%
  transmute(signalname = str_remove(value, '.csv'), intarget = 1)


doclist = alldoc %>% filter(Cat.Signal=='Placebo') %>% select(signalname) %>% mutate(indoc = 1)
listcomp = full_join(doclist, csvlist) 
mismatch =  listcomp %>% filter(is.na(indoc) | is.na(intarget))

mismatch




### SIGNAL FILES
list.files(paste0(pathProject, '/Signals/Data/Predictors/'))

temp = fread(paste0(pathProject, '/Signals/Data/Predictors/ZScore.csv'))

temp



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

## run some sample 
small = raw %>% filter(yyyymm <= Inf & yyyymm >= 196301)

ret = small %>%
    select(permno,yyyymm,STreversal) %>%
    mutate(
        dateold = yyyymm
      ,  yyyymm = yyyymm - 1
      , yyyymm = if_else(yyyymm %% 100 == 0, yyyymm-100+1,yyyymm)
    ) %>%
    transmute(dateold, permno,yyyymm, retnextmonth = -1*STreversal) %>%
    filter(!is.na(retnextmonth))

signallist = signaldoc %>% filter(Cat.Signal == 'Predictor') %>%
    transmute(signalname = Acronym) %>%
    mutate(beta = NA_real_)

for (i in 1:dim(signallist)[1]){
    print(paste0(i, ' of ', dim(signallist)[1], ' :', signallist$signalname[i]))

    signalselect = signallist$signalname[i]



    onesignal = small %>%
        select(c('permno','yyyymm',signalselect)) %>%
        rename(signal = signalselect) %>%
        filter(is.finite(signal))

    tempsd = sd(onesignal$signal)
    tempmean = mean(onesignal$signal)

    onesignal = onesignal %>%
        mutate(signal = (signal - tempmean)/tempsd)

    checkset = onesignal %>%
        inner_join(ret, by=c('permno','yyyymm')) %>%
        mutate(const = 1)

    X = as.matrix(checkset %>% select(const, signal))
    y = checkset$retnextmonth

    temp = lm.fit(X, y)    
    signallist$beta[i] = temp$coefficients[2]

    print(temp$coefficients)
    
} # for i            


signallist$beta

options(scipen=999)
print('Mean of beta are ')    
mean(signallist$beta)
print('Quantiles of beta are ')    
quantile(signallist$beta, 0:4/4)
print('Share of beta > 0 is')
print(sum(signallist$beta>0)/length(signallist$beta))
