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

# pathSummary    = '../DataSummary/'
# pathSignalFile = '../DataClean/'
# pathStratMonth = '../DataStratMonth/'

if (Sys.getenv("USERNAME") != 'Tom') {
  setwd("/cm/chen/anomalies.com/code.fed")
  pathSignalFile = '../DataOutput/'
  pathCostFile   = '../DataOutput/'
  pathSummary    = '../DataSummary/'
  pathResults    = '../Results/'
  pathStratMonth = '../DataStratMonth/'
} else {
  pathSignalFile = '../DataClean/'
  pathCostFile   = '../DataClean/'
  pathSummary    = 'C:/Users/Tom/Google Drive/anomalies.com/DataSummary/'
  pathResults    = 'C:/Users/Tom/Google Drive/anomalies.com/Results/'
  pathStratMonth = '../DataOutput/'  
}

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


### CALCULATE RETURNS FOR MANY STRATS ###

## calculate portfolio returns
## most of the time is spent here!
long_short = many_ports_longlist(
  longlist = signallist
  , keys = keys
  , wide = wide  
  , signalPath = pathSignalFile
)  %>% filter(rettype == 'gross')


## EXPORT
fwrite(long_short,paste0(pathStratMonth, 'ret_StratMonth_base.csv'))


### OUTPUT WIDE ###
long_short_wide = long_short %>% 
  select(date,signalname,return) %>%
  spread(signalname, return)

fwrite(long_short_wide,paste0(pathStratMonth, 'retWide_SignalMonth_base.csv'))
