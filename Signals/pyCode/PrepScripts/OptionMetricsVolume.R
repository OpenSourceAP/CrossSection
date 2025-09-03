# Option Volume Data from OptionMetrics
# Created 2020 Andrew
# Updated 2022-02
# Separated from OptionMetricsProcessing.R
# Downloads option volume data and aggregates by month

# Environment -------------------------------------------------------------

rm(list = ls())

querylimit = 'all' # use 'all' for full data, '20' for debugging

path_dl_me = './data_for_dl/'

dir.create(path_dl_me)

library(RPostgres)
library(tidyverse)
library(lubridate)

# heads up: this assumes (1) running on wrds server and (2) pgpass is set up following this:
# https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-r/r-from-the-web/
wrds <- dbConnect(Postgres(),
                  host='wrds-pgdata.wharton.upenn.edu',
                  port=9737,
                  dbname='wrds',
                  sslmode='require')

# Set up loop -------------------------------------------------------------
temp_dat = dbGetQuery(wrds, "SELECT table_name FROM information_schema.tables 
                      WHERE table_schema = 'optionm' AND table_name like 'opprcd%'")                  
yearlist = substr(temp_dat$table_name, 7,12)

yearlist

volume_many = list()

# Loop over years -------------------------------------------------------------

# From Page 268 of the paper "Specifically, OPVOLi,w equals the total volume in 
# option contracts across all strikes for options expiring in the 30 trading days 
# beginning five days after the trade date."

querylimit = 'all'
i = 1
for (year in yearlist) {
  print(Sys.time())
  tic = Sys.time()
  print("Processing Volume for Year:")
  print(year)
  
  # download data with lots of filters
  # 30 trading days after 5 days after trade date
  query = paste0(
    "select secid, date, exdate, volume
    from optionm.opprcd", year, "
    where cp_flag != 'NaN' and
      exdate - date >= 5 and
      exdate - date <= 5+30*(365/252) 
    limit ", querylimit
  )
  
  res = dbSendQuery(wrds, query)
  temp = res %>% dbFetch()
  
  volume_many[[i]] = temp
  
  toc = Sys.time()
  
  print((toc - tic))
}


# Bind and save -----------------------------------------------------------

# finally, merge years together
volume_all = do.call(rbind,volume_many)

# write to csv
data.table::fwrite(volume_all,
                   file = paste0(
                     path_dl_me
                     , 'OptionMetricsVolume.csv'
                   )
)

# Disconnect from WRDS
dbDisconnect(wrds)