# For baseline portfolio tests
# includes likely, maybe, and not predictors, as well as variants
# Andrew Chen 2020 04

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
library(feather)

pathSummary    = '../DataSummary/'
pathSignalFile = '../DataClean/'
pathStratMonth = '../DataStratMonth/'

source('00_functions.R', echo=TRUE)

### LOAD DATA ###

## this loads objects: wide, keys, portset (not used)
load(paste0(pathSignalFile, 'temp.RDS'))
rm(portset)

## load signal header
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
# merge
signallist = temp1 %>% left_join(temp2, by="signalname")


## load CRSP data
# in principle, this data is in wide$ret, but we can keep things tidy if we don't worry about bh spreads.
crsp = fread(paste0(pathSignalFile, 'SignalFirmMonthMetaData.csv'))
crsp = crsp %>% 
  mutate(date = paste(substr(crsp$time_avail_m, 1,4), 
                      substr(crsp$time_avail_m, 6,7), 
                      "28", 
                      sep = "-") %>% 
           as.Date()
  ) %>%
  as_tibble() %>%
  arrange(permno,date) %>% 
  group_by(permno) %>%
  mutate(melag = lag(mve_c)) %>%
  ungroup %>%
  transmute(permno, date, ret = 100*ret, melag) 


### LOOP OVER SIGNALS
# based off of 99f_functions.R's many_ports_longlist
default = list(
  ls_sign = 0
  ,q_cut   = 0.2
  ,q_spread  = 0
  ,nyse_q = F
  ,weight_me = F
  ,holdper  = 1
  ,startingmonth = 6
  ,FilterPrice = NA
  ,FilterExchange = NA
  ,Sign = 1
)


## fill out signallist with defaults
signallistfull = signallist
for (tempname in names(default)){
  if ( !tempname %in% colnames(signallistfull)){
    signallistfull[[tempname]] = default[[tempname]]
  }
}
signallistfull$weight_me = replace_na(signallistfull$weight_me, 0)       
signallistfull$FilterPrice = replace_na(signallistfull$FilterPrice, 0)
signallistfull$FilterExchange = replace_na(signallistfull$FilterExchange, '1;2;3')    
signallistfull$Sign = replace_na(signallistfull$Sign, 1)




### FUNCTION FOR LOOPING OVER SIGNALS

loopallquant = function(signallistfull){
  
  allport = tibble()
  
  for (sigi in seq(1,dim(signallistfull)[1])) {
    start_time <- Sys.time()
    
    ### LOAD UP DATA
    
    ## focus on one signal from big dataset
    print("reading big signal-firm-month data")
    onesignal = read_feather(paste0(pathSignalFile, 'temp.feather'),
                             columns = c("permno","date",signallistfull$signalname[sigi],"prc","exchcd")) %>% 
      rename(signalcurr = signallistfull$signalname[sigi]) %>%
      filter(!(is.na(signalcurr)))
    
    
    ## apply filters and sign
    tempexchlist = strsplit(signallistfull$FilterExchange[sigi],";") %>%
      unlist() %>% as.character() %>% as.numeric()     
    
    onesignal = onesignal %>%
      mutate(
        signalcurr = ifelse(abs(prc) > signallistfull$FilterPrice[sigi], signalcurr, NA)
        ,signalcurr = ifelse(exchcd %in% tempexchlist, signalcurr, NA)
        ,signalcurr = signallistfull$Sign[sigi]*signalcurr                
      )
    
    ## enforce signal updating frequency
    # find months that signals are updated
    rebmonths =  (
      signallistfull$startingmonth[sigi]
      + seq(0,12)*signallistfull$holdper[sigi]
    ) %% 12
    rebmonths[rebmonths == 0] = 12
    
    onesignal = onesignal %>%        
      mutate(
        month = month(date)
        , signalcurr = if_else(month %in% rebmonths, signalcurr, as.numeric(NA))
      ) %>%
      fill(signalcurr) %>%
      select(-month)
    
    ## clean up
    onesignal = onesignal %>%
      arrange(permno,date) %>%
      group_by(permno) %>%
      mutate(
        signallag = lag(signalcurr)
      )  %>%
      filter(!is.na(signallag))
    
    
    ### CREATE PORTFOLIO RETURNS
    print('creating portfolio returns')
    ## assign to portfolios
    if (!is.na(signallistfull$q_cut[sigi])){
      
      nport = 1/signallistfull$q_cut[sigi]
      
      portnum = onesignal %>%
        arrange(date,signallag) %>%
        group_by(date) %>% 
        mutate(portlag =
                 findInterval(
                   signallag
                   , quantile(signallag, probs=0:nport/nport)
                   , rightmost.closed = T)
        )
      
    } else {
      
      sigmap = data.frame(
        signalval = onesignal$signallag %>% unique %>% sort()
        , port = c(1,2)
      )
      portnum = onesignal %>%
        mutate(
          portlag = case_when(
            signallag == sigmap$signalval[1] ~ sigmap$port[1]
            ,signallag == sigmap$signalval[2] ~ sigmap$port[2]
          )
        )       
      
    } # if !is.na(signallistfull$q_cut[sigi])
    
    portnum = portnum %>% select(permno, date, signalcurr, portlag)
    
    ## find portfolio returns
    # add returns and weights    
    portnum2  =  portnum %>%
      inner_join(
        crsp, by = c('permno','date')
      ) %>%
      rename(weight = melag) %>%
      filter(!is.na(weight))
    if (signallistfull$weight_me[sigi] == 0){
      portnum2$weight = 1
    }
    
    portsum = portnum2 %>%
      group_by(date, portlag) %>%
      summarize(
        signalmean = mean(signalcurr, na.rm=T)
        , ret = weighted.mean(ret, weight, na.rm = T)
      ) %>%
      ungroup
    
    ## label and store
    allport = rbind(
      allport
      , portsum %>%
        mutate(
          signalname = signallistfull$signalname[sigi]
        ) %>%
        rename(port = portlag) %>%
        as_tibble()
    )
    
    # feedback
    print("99allquantile loop  ==============  ")
    print(paste0("sigi = ",sigi))
    print(signallistfull$signalname[sigi])    
    end_time <- Sys.time()
    print(end_time - start_time)       
    
    
  } # for sigi
  
  return(allport)
  
} # ====== END FUNCTION LOOPALLQUANT



## FIND ALL QUANTS FOR BASE (CLEAR AND LIKELY)

# calculate
templist = signallistfull %>%
  filter(
    Cat.Variant == '1_original'
    , Cat.Predictor %in% c('1_clear','2_likely')
  )

allportretbase = loopallquant(templist)

# write to disk
write.csv(allportretbase, '../SharedData/allportretbase.csv')


## FIND ALL QUANTS FOR BASE (CLEAR AND LIKELY), FORCE DECILES, CONT ONLY

# calculate
templist = signallistfull %>%
  filter(
    Cat.Variant == '1_original'
    , Cat.Predictor %in% c('1_clear','2_likely')
  ) %>%
  filter(!is.na(q_cut)) %>%        
  mutate(q_cut = 0.1)                                     
allportretdec = loopallquant(templist)


# write to disk
write.csv(allportretdec, '../SharedData/allportretdec.csv')

