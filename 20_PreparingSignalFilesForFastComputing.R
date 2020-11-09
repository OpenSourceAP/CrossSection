## Created 2020 Jan 27 Andrew.
## Should help manage memory and save time
## Ideally this file is run separately, and R is shut down afterwards
## to avoid memory fragmentation

rm(list=ls())

### ENVIRONMENT ###
options(stringsAsFactors = FALSE)
library(data.table)
library(tidyverse)
library(lubridate)
library(xts)
library(readxl)
library(statar)
library(pryr)
library(fst)

pathSignalFile = '../DataCleanStata/'
pathCostFile   = '../DataClean/'

if (Sys.getenv("USERNAME") != 'Tom') {
  pathSummary    = '../DataSummary/'
} else {
  pathSummary    = 'C:/Users/Tom/Google Drive/anomalies.com/DataSummary/'
}

source('00_functions.R', echo=TRUE)


### IMPORT ###
## Benchmark Portfolio settings
temp1 = read_excel(
  paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet = 'Construction'
) %>%
  rename(
    signalname = Acronym
    , weight_me = VW
    , q_cut = Quantile
  )

temp2 = read_excel(
  paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet = 'BasicInfo'
) %>%
  rename(signalname = Acronym)  %>%
  select(-Authors)

# check for missing
missing_from_construction  = setdiff(temp2$signalname,temp1$signalname)
missing_from_basicinfo  = setdiff(temp1$signalname,temp2$signalname)

if (length(missing_from_construction) > 0){
  print("Error: the following signals are missing from construction sheet:")
  print(missing_from_construction)
  stop()
}

if (length(missing_from_basicinfo) > 0){
  print("Error: the following signals are missing from basic info sheet:")
  print(missing_from_basicinfo)
  stop()
}


portset = temp1 %>% left_join(temp2, by="signalname") 


## HXZ settings
headerhxz = read_excel(
  paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet = 'HXZ'
)  %>%
  rename(
    'signalname' = 'Closest Acronym (Stata)'
  ) 



## signals
#signalCols = fread(paste0(pathSignalFile, 'SignalFirmMonth.csv'), nrows = 0)
#signalRows = fread(paste0(pathSignalFile, 'SignalFirmMonth.csv'), select = 'permno')
#signal = fread(paste0(pathSignalFile, 'SignalFirmMonth.csv'), header = TRUE, nrows = round(nrow(signal)/2))

signal = haven::read_dta(paste0(pathSignalFile, 'FinalSignalFile.dta')) %>% 
  mutate(date = ymd(paste0(time_avail_mString, '-28'))) %>% 
  select(-time_avail_m, -time_avail_mString)

## signal metadata
signalMeta = signal %>% 
  select(gvkey, permno, date, ret, mve_c, prc, NYSE, exchcd)

## Write signals only to disk
signal = signal %>% 
  select(-gvkey, -ret, -mve_c, -NYSE, -bh1m, -tickerIBES, -sicCS, -sicCRSP, -shrcd
         #-prc, -exchcd
         )

signalsInSignalFile = names(signal %>% select(-permno, -date, -prc, -exchcd))

write_fst(signal, paste0(pathSignalFile, 'temp.fst'))

rm(signal)
gc()



## trading costs
cost0 = fread(paste0(pathCostFile, 'tcosts_CV_20191203.csv')) %>% 
  transmute(permno,
            date = paste(substr(month, 1, 4), substr(month, 5, 6), '28', sep = '-') %>% 
              as.Date(),
            half_spread = tcost*100
  ) 


### ERROR CHECKING ###


## Compare portset to signal file
missing_from_signal  = setdiff(portset$signalname, signalsInSignalFile)
missing_from_portset = setdiff(signalsInSignalFile, portset$signalname)

if (length(missing_from_signal) > 0){
  print("Error: the following signals are missing from signal file:")
  print(missing_from_signal)
  stop()
  # portset = portset %>% filter(!(signalname %in% missing_from_signal))
}

if (length(missing_from_portset) > 0){
  print("Error: the following signals are missing from Basic Info and Construction:")
  print(missing_from_portset)
  stop()
}

## check for distinct in hxz
temp3b = headerhxz %>%
  arrange(HXZname) %>%
  group_by(signalname, holdper) %>%
  mutate( distinct = ifelse( n() > 1, 0, 1) ) %>%
  select(HXZname, signalname, holdper, distinct) %>%
  as.data.frame()

badones = temp3b %>%
  filter(distinct == 0) %>%
  arrange(signalname, holdper) %>%
  distinct(signalname, holdper) %>%
  mutate(bad = 1) 

hxzcheck = temp3b %>% left_join(badones) %>% replace_na(list(bad = 0)) %>%
  arrange(bad, signalname, holdper)

# check for errors and write to csv
if ( sum(hxzcheck$bad) > 0 ){
  print('ERROR WE HAVE DUPLICATES IN THE HXZ HEADER SHEET: HERE ARE A FEW')
  hxzcheck %>% filter(bad == 1) %>% head()
  print('saving to hxzbad.csv')
  write.csv(hxzcheck, 'hxzbad.csv')
  stop()
}

## compare portset to hxz
missing_from_portset  = setdiff(headerhxz$signalname, portset$signalname)
if ( length(missing_from_portset) > 0){
  print('error: there are signals in hxz that are missing from portset')
  print(missing_from_portset)
}   

## check for missing obs in signal file

# debug: for removing signals that shouldn't be there (for now)
# signal = signal %>% select(-c(std_dolvol))

# count nobs for each signal in each month
signalobs = tibble()
print("=== CHECKING FOR MISSING VALUE PROBLEMS ===")
for (tempname in signalsInSignalFile){
  print(tempname)
  
  # Load signal
  signal = read_fst(
    path = paste0(pathSignalFile, 'temp.fst'),
    columns = c('permno', 'date', tempname)
  )
  
  # grab sample beginning and end
  tempyear = portset %>% filter(signalname == tempname) %>%
    select(SampleStartYear, SampleEndYear)
  
  # count observations in each month
  tempobs = signal %>% 
    rename(signalcurr = tempname) %>%
    group_by(date) %>%
    summarize(nobs = sum(!is.na(signalcurr))) %>%
    mutate(
      year = year(date)
    ) %>%
    ungroup() %>% 
    filter(year > tempyear$SampleStartYear, year <= tempyear$SampleEndYear) %>%
    summarize(minobs = min(nobs)) %>% 
    mutate(signalname = tempname)
  
  # append
  signalobs = rbind(signalobs,tempobs)
  
} # for tempname in signallist

# check that the minimum obs > some threshold
toomanymissing = signalobs %>% 
  filter(minobs < 10, !(signalname %>% endsWith("_q")), !(signalname == 'ChNAnalyst'), !(signalname == 'PosNegCons'))

if ( dim(toomanymissing)[1] > 0 ){
  print("error: we have missing value problems in in-sample data")
  print("here are the first 20")    
  print(toomanymissing %>% head(20))
  stop()
  # check
  ## tempname = "ChangeInRecommendation"
  ## signalobs %>% filter(signalname == tempname) %>% arrange(nobs) %>% head(20)
  ## signalobs %>% filter(signalname == tempname) %>% arrange(time_avail_m)
}    



### REFORMAT DATA FOR SPEEDY COMPUTATION ###
## prep helper balanced matricies
print("prepping reused matricies")
ptm <- proc.time()
wide = prep_matricies(signalsInFile = signalsInSignalFile,
                      signalMetadata = signalMeta,
                      cost0  = cost0, 
                      anomalyNames = portset$signalname)
rm(cost0)
proc.time() - ptm


# workaround for R's single output
keys = wide$keys
wide = wide[names(wide)!="keys"]


# save data only in wide format: also should help manage RAM
save(keys, wide, portset
     , file = paste0(pathSignalFile, 'temp.RDS'))



print("20_PreparingSignalFilesForFastComputing.R is done!")
