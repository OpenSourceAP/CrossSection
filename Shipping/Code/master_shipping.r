# ==== SETTINGS ====
# this code moves and zips files from the local repo Data subfolders
# to some storage area for shipping
# Not sure anyone besides us will need to us it.
# But it's good for replication, and to make data updates easier down the road.

library(tidyverse)
library(readxl)
library(data.table) # for speed
library(googledrive)

# Read settings from 00_settings.txt
settings_lines = readLines('00_settings.txt')
settings_lines = settings_lines[!grepl('^#', settings_lines) & nchar(trimws(settings_lines)) > 0]
for (line in settings_lines) {
  parts = strsplit(line, ' = ')[[1]]
  assign(trimws(parts[1]), trimws(parts[2]))
}
pathProject = path.expand(pathProject)
pathStorage = path.expand(pathStorage)


pathShipping = paste0(pathProject,'Shipping/') # where Code/master_shipping.r is
pathPredictors = paste0(pathProject, 'Signals/Data/Predictors/')
pathPlacebos = paste0(pathProject, 'Signals/Data/Placebos/')
pathPortfolios = paste0(pathProject, 'Portfolios/Data/Portfolios/')
pathResults = paste0(pathProject, 'Results')

# create folders
dir.create(pathStorage)
setwd(paste0(pathShipping,'Code/'))
dir.create('../Data/')
dir.create('../Data/Portfolios/')
dir.create('../Data/Portfolios/Individual')
dir.create('../Data/temp')

# trigger googledrive auth
drive_auth()

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
  alldocumentation = read_csv(
    paste0(pathProject, 'SignalDoc.csv')
  ) %>%
    rename(signalname = Acronym)  %>%
    # Format order of category labels
    mutate(Cat.Data = as_factor(Cat.Data) %>% 
             factor(levels = c('Accounting', 'Analyst', 'Event', 'Options', 'Price', 'Trading', '13F', 'Other'))) %>% 
    # Make economic category proper
    mutate(Cat.Economic = str_to_title(Cat.Economic)) %>% 
    # Clean column names
    rename(
      sweight = 'Stock Weight'
      , q_cut = 'LS Quantile'
      , q_filt = 'Quantile Filter'  
      , portperiod = 'Portfolio Period'
      , startmonth = 'Start Month'
      , filterstr = 'Filter'
    ) %>%
    mutate(
      filterstr = if_else(filterstr %in% c('NA','None','none')
                          , NA_character_
                          , filterstr)
    ) %>%
    select(-c(starts_with('Note'))) %>% 
    arrange(signalname)   
  
  
  
  names(alldocumentation) = make.names(names(alldocumentation))
  
  return(alldocumentation)
  
  
} # end function


# ==== DO STUFF ====

# update SignalDo
file.copy(
  from = paste0(pathProject,'SignalDoc.csv')
  , to = paste0(pathStorage)
)

# source('1_pack_signals.r')
# source('2_pack_portfolios_and_results.r')
# source('3_check_storage.r')

