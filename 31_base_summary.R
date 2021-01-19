## Create summary stats for baseline replications
## Andrew 2020 04

### ENVIRONMENT ###
rm(list=ls())
options(stringsAsFactors = FALSE)
options(scipen=999)
optFontsize = 18  # Fix fontsize for graphs here

library(data.table)
library(ggplot2)
library(tidyverse)
library(readxl)  # readxl is much faster and cleaner than read.xlsx
library(writexl)
library(lubridate)
library(xtable)
library(fst)
options(xtable.floating = FALSE)


if (Sys.getenv("USERNAME") != 'Tom') {
  setwd("/cm/chen/anomalies.com/code.fed")
  pathSignalFile = '../DataOutput/'
  pathCostFile   = '../DataOutput/'
  pathSummary    = '../DataSummary/'
  pathResults    = '../Results/'
  pathStratMonth = '../DataStratMonth/'
} else {
  pathSignalFile = '../DataCleanStata/'
  pathCostFile   = '../DataClean/'
  pathSummary    = 'C:/Users/Tom/Google Drive/anomalies.com/DataSummary/'
  pathResults    = 'C:/Users/Tom/Google Drive/anomalies.com/Results/'
  pathStratMonth = '../DataOutput/'  
}



# LOAD DATA ---------------------------------------------------------------

## import baseline returns
portbase = read_fst(paste0(pathStratMonth, 'ret_StratMonth_base.fst')) %>% 
  as_tibble() %>% 
  mutate(date = ymd(date))


## import header data
temp1 = read_excel(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  ,sheet='BasicInfo'
) 

temp2 = read_excel(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  ,sheet='Construction'
)

temp3 = read_excel(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  ,sheet='HXZ'
) 
# this header has one row for each unique signal using our counting method
headerbase = left_join(
    temp1
  , temp2 %>% select(-c(Authors))
  , by = "Acronym") %>% 
    rename(signalname = Acronym) %>% 
    # Format order of category labels
    mutate(Cat.Data = as_factor(Cat.Data) %>% 
               factor(levels = c('Accounting', 'Analyst', 'Event', 'Options', 'Price', 'Trading', '13F', 'Other'))) %>% 
    # Make economic category proper
    mutate(Cat.Economic = str_to_title(Cat.Economic))


# SUMMARY STATS BY SIGNAL -------------------------------------------------

### baseline first

## define samples
portbase1 = portbase %>% 
  left_join(
    headerbase %>%
      select(signalname, SampleStartYear, SampleEndYear, Year, Cat.Predictor)
    , by=c("signalname")
  ) %>%
  rename(PubYear = Year) %>% 
  mutate(
    samptype = case_when(
      year(date) >= SampleStartYear & year(date) <= SampleEndYear ~ "insamp"
      ,year(date) > SampleEndYear & year(date) <= PubYear ~ "between"            
      ,year(date) > PubYear ~ "postpub",
      TRUE ~ NA_character_
    )
  ) %>%
  select(-c(SampleStartYear, SampleEndYear, PubYear))

## find stats for all groups, with Nstocks filter (only few stocks for IO_ShortInterest, so no filter there)
sumbase = portbase1 %>%
    filter( (Nstocks >= 20 | signalname == 'IO_ShortInterest'), ls_sign==0, rettype=="gross", samptype=="insamp") %>%
    group_by(signalname, ls_sign, q_cut, q_spread, nyse_q, weight_me, holdper,
             rettype,samptype) %>%
    summarize(
        ret = mean(return), vol = sd(return), T = n(), tstat = ret/vol*sqrt(T)
    ) %>%
    ungroup()

## add some header info and rearrange
sumbase = sumbase %>%
    left_join(
        headerbase, by=c('signalname')
    ) %>%
    select(
        signalname, tstat, ret, vol, T
      , q_cut, weight_me,  samptype, Cat.Predictor, Cat.Variant, Cat.Economic, Cat.Data
    ) 


# WRITE TO EXCEL -------------------------------------------------

### WRITE TO DISK
write_xlsx(
    list(sumstats=sumbase)
    , paste0(pathSummary, 'SignalSummaryBase20201113.xlsx')
)
