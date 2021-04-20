# ==== SETTINGS ====
# this code moves and zips files from the local repo Data subfolders
# to some storage area for shipping
# Not sure anyone besides us will need to us it.
# But it's good for replication, and to make data updates easier down the road.

library(tidyverse)
library(readxl)
library(data.table) # for speed

pathProject = 'd:/pc_work/crossSection/' # local code base directory
pathStorage = 'D:/Google Drive/Work/Public/openap/Data Release 2021.04/' # a place to store copies for uploading

pathShipping = paste0(pathProject,'Shipping/') # where Code/master_shipping.r is
pathPredictors = paste0(pathProject, 'Signals/Data/Predictors/')
pathPlacebos = paste0(pathProject, 'Signals/Data/Placebos/')
pathPortfolios = paste0(pathProject, 'Portfolios/Data/Portfolios/')


setwd(paste0(pathShipping,'Code/'))
dir.create('../Data/')
dir.create('../Data/Portfolios/')
dir.create('../Data/Portfolios/Individual')
dir.create('../Data/temp')


# function for reading in documentation, copied for Portfolios/Code/
readdocumentation = function(){
  
  # little function for converting string NA into numeric NA
  as.num = function(x, na.strings = c("NA",'None','none')) {
    stopifnot(is.character(x))
    na = x %in% na.strings
    x[na] = 0
    x = as.numeric(x)
    x[na] = NA_real_
    x
  }
  
  ## load signal header
  temp1 = read_excel(
    paste0(pathProject, 'SignalDocumentation.xlsx')
    , sheet = 'BasicInfo'
  ) %>%
    rename(signalname = Acronym)  %>%
    # Format order of category labels
    mutate(Cat.Data = as_factor(Cat.Data) %>% 
             factor(levels = c('Accounting', 'Analyst', 'Event', 'Options', 'Price', 'Trading', '13F', 'Other'))) %>% 
    # Make economic category proper
    mutate(Cat.Economic = str_to_title(Cat.Economic))
  
  temp2 = read_excel(
    paste0(pathProject, 'SignalDocumentation.xlsx')
    , sheet = 'AddInfo'
  ) %>%
    select(-Authors) %>%         
    rename(
      signalname = Acronym
      , sweight = 'Stock Weight'
      , q_cut = 'LS Quantile'
      , q_filt = 'Quantile Filter'  
      , portperiod = 'Portfolio Period'
      , startmonth = 'Start Month'
      , filterstr = 'Filter'
    ) %>%
    mutate_at(
      c('q_cut','portperiod','startmonth')
      , .funs = as.num
      , 
    ) %>%
    mutate(
      filterstr = if_else(filterstr %in% c('NA','None','none')
                          , NA_character_
                          , filterstr)
    ) %>%
    select(-c(starts_with('Note')))
  
  
  # merge
  alldocumentation = temp1 %>% left_join(temp2, by="signalname") %>%
    arrange(signalname)   
  
  # clean up
  alldocumentation = alldocumentation %>%
    mutate(Sign = as.numeric(Sign))
  
  names(alldocumentation) = make.names(names(alldocumentation))
  
  return(alldocumentation)
  
  
} # end function

# ==== DO STUFF ====

# update SignalDocumentation
file.copy(
  from = paste0(pathProject,'SignalDocumentation.xlsx')
  , to = paste0(pathStorage)
)

source('1_pack_signals.r')
source('2_pack_portfolios.r')
source('3_check_storage.r')

