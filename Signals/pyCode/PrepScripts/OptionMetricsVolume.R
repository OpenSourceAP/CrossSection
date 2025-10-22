# Option Volume Data from OptionMetrics
# Created 2020 Andrew
# Updated 2025-09 to more closely match Johnson and So 2012 JFE
# Separated from OptionMetricsProcessing.R
# Downloads option volume data and aggregates by month

# Environment -------------------------------------------------------------

rm(list = ls())

querylimit = 'all' # use 'all' for full data, '1000' for debugging

path_dl_me = './data_for_dl/'

dir.create(path_dl_me)

library(RPostgres)
library(tidyverse)
library(lubridate)
library(data.table)

# heads up: this assumes running on wrds server 
wrds <- dbConnect(Postgres(),
                  host='wrds-pgdata.wharton.upenn.edu',
                  port=9737,
                  dbname='wrds',
                  sslmode='require')

# Set up loop -------------------------------------------------------------

# get list of years 
# each year has a different table (e.g. opprcd2023)
temp_dat = dbGetQuery(wrds, "SELECT table_name FROM information_schema.tables 
                      WHERE table_schema = 'optionm' AND table_name like 'opprcd%'")                  
yearlist = substr(temp_dat$table_name, 7,12)
volume_many = list()

# Loop over years -------------------------------------------------------------

# From Page 268 of the paper "Specifically, OPVOLi,w equals the total volume in 
# option contracts across all strikes for options expiring in the 30 trading days 
# beginning five days after the trade date."

i = 1
dat_by_year = list()
for (year in yearlist) {
  print(Sys.time())
  tic = Sys.time()
  print("Processing Volume for Year:")
  print(year)
  
  # download data with exdate filter
  # 30 trading days after 5 days after trade date
  query = paste0(
    "select secid, optionid, date, exdate, volume
    from optionm.opprcd", year, "
    where cp_flag != 'NaN' and
      volume > 0 and
      exdate - date >= 5 and
      exdate - date <= 5+30*(365/252) 
    limit ", querylimit
  )
  option_day = dbSendQuery(wrds, query) %>% dbFetch() %>% setDT() 
  
  # aggregate to stock-day
  stock_day = option_day[
    !is.na(volume)
    , .(
      optvolume_js12 = sum(volume), # option volume as defined in Johnson and So 2012
      expir_mean = mean(exdate - date),
      expir_min = min(exdate - date),
      expir_max = max(exdate - date)
    ),
    by = c('secid','date')
  ]

  # save and advance
  dat_by_year[[i]] = stock_day
  i = i + 1
    
  toc = Sys.time()
  
  
  print((toc - tic))
} # end for year


# Bind and save -----------------------------------------------------------

optvolall = do.call(rbind, dat_by_year)
fwrite(optvolall,
       file = paste0(
         path_dl_me
         , 'OptionMetricsVolume.csv'
       )
 )



# Disconnect from WRDS
dbDisconnect(wrds)