# Creates portfolios with various liquidity screens

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
# merge and select predictors and remove filters
signallist = temp1 %>% left_join(temp2, by="signalname") %>%
    filter(
        Cat.Predictor == '1_clear'
      , Cat.Variant == '1_original'
      , is.na(FilterPrice)
      , (FilterExchange != '1') | is.na(FilterExchange)
    ) 
        

# create ME screen
mescreen0 = fread(paste0(pathSignalFile, 'SignalFirmMonthMetaData.csv')) %>% 
  mutate(date = paste(substr(time_avail_m, 1,4), 
                      substr(time_avail_m, 6,7), 
                      "28", 
                      sep = "-") %>% 
           as.Date()
  )

tempcut = mescreen0 %>%
    filter(exchcd == 1) %>%
    group_by(date) %>%
    summarize(cutoff = quantile(mve_c, probs=0.2, na.rm = T))

mescreen1 = mescreen0 %>%
    left_join(tempcut, by='date') %>%
    mutate(keep = mve_c > cutoff) %>%
    select(permno, date, keep, mve_c)


### CONSTRUCT PORTS ###

## 1. baseline
long_short_base = many_ports_longlist(
    longlist = signallist
  , keys = keys, wide = wide, signalPath = pathSignalFile
  , customscreen = NULL
) %>%  filter(rettype == 'gross') 
    


## 2. Price > 5
long_short_price = many_ports_longlist(
    longlist = signallist %>% mutate(FilterPrice = 5)
  , keys = keys, wide = wide, signalPath = pathSignalFile
  , customscreen = NULL
)  %>% filter(rettype == 'gross')


## 3. NYSE only 
long_short_nyse = many_ports_longlist(
    longlist = signallist %>% mutate(FilterExchange = '1')
  , keys = keys, wide = wide, signalPath = pathSignalFile
  , customscreen = NULL
)  %>% filter(rettype == 'gross')


## 4. ME > NYSE 20th pct
long_short_me = many_ports_longlist(
    longlist = signallist 
  , keys = keys, wide = wide, signalPath = pathSignalFile
  , customscreen = mescreen1
)  %>% filter(rettype == 'gross')

long_short = rbind(
    long_short_base %>% mutate(screen = 'none')
  , long_short_price %>% mutate(screen = 'price')
  , long_short_nyse  %>% mutate(screen = 'nyse')
  , long_short_me %>% mutate(screen = 'me')
)
    

## EXPORT
fwrite(long_short,paste0(pathStratMonth, 'ret_StratMonth_LiqScreens.csv'))


### CHECK OUTPUT ###

temp_out = long_short %>%
    group_by(screen) %>%
    summarize(ret = mean(return), tstat = ret/sd(return)*sqrt(n()))  %>%
    as.data.frame()

print(temp_out)
