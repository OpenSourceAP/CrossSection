# Creates alternative holding period portfolios
# Andrew Chen 

# made from 99_ConstructPorts.R 

# 2020 04

# 


### ENVIRONMENT ###
rm(list=ls())

options(stringsAsFactors = FALSE)
library(data.table)
library(tidyverse)
library(lubridate)
library(xts)
library(readxl)
library(statar)
library(pryr)
library(feather)

pathSignalFile = '../DataClean/'
pathSummary    = '../DataSummary/'
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
# and subset signals to those with one-month benchmark rebalancing and clear predictors
signallist = temp1 %>% left_join(temp2, by="signalname") %>%
    filter(
                Cat.Predictor == '1_clear'
              , holdper == 1
              , Cat.Variant == '1_original'
            )

### CALCULATE SINGLE LEG RETURNS ###
holdperlist = c(1,3,6,12)

long_short = data.frame()
for (holdpercurr in holdperlist){
    
  ## load settings for current holding period
  portsetcurr = signallist
  portsetcurr$holdper = holdpercurr
    
  ## calculate portfolio returns
  ## most of the time is spent here!
  long_short_curr = many_ports_longlist(
    longlist = portsetcurr
    , keys = keys
    , wide = wide  
    , signalPath = pathSignalFile
  )
  long_short_curr = long_short_curr %>%
      filter(rettype == 'gross')
    
  ## append
  if (length(long_short_curr) > 0){
    long_short = rbind(long_short,long_short_curr)
  }
}




## EXPORT
fwrite(long_short,paste0(pathStratMonth, 'ret_StratMonth_HoldPer.csv'))


### CHECK OUTPUT ###

temp_out = long_short %>%
  filter(rettype == "gross") %>%
  group_by(signalname,holdper) %>%
  summarize(ret = mean(return)) %>% spread(holdper,ret) %>% as.data.frame()

temp_out
