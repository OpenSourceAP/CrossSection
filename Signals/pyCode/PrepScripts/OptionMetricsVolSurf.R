# Volatility Surface Data from OptionMetrics
# Created 2020 Andrew
# Updated 2022-02
# Separated from OptionMetricsProcessing.R
# Downloads volatility surface data for Smile Slope and other predictors

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


# Vol Surface -----------------------------------------------------
# Used in Smile Slope a.k.a. Slope (Yan) 
# also used in An Ang Bali Cakici 2014
# right now we DL delta = 50 (NTM) and days in (30,91) but we can adjust later

# takes about 60 min

# set up loop
rm(list = ls(pattern = 'temp'))

vsurf_tables = dbGetQuery(
  wrds, "
  SELECT table_name 
      FROM information_schema.tables
      WHERE table_schema = 'optionm' 
        AND table_name like 'vsurfd%'
  "
  )
yearlist = substr(vsurf_tables$table_name, 7,12)

# prepare list of data frames
vsurfmany = list()

# Setup query
# adding the filter for deltas and duration speeds query up a lot I think
  queryprestring = paste0("select a.secid, a.date, a.days, a.cp_flag, a.delta "
                          ,",a.impl_volatility "
                         ,"from optionm.vsurfd")
  querypoststring = paste0(
    " as a "
    ,"where (a.impl_volatility != 'NaN')"
    ," and abs(a.delta) = 50"
    ," and a.days in (30,91) "
    ," and extract(day from a.date) >= 0 "
    ," limit "
    , querylimit
  )   
  

i = 1
for (year in yearlist) {
  
  print(Sys.time())
  start_time = Sys.time()
  print("Processing Vol Surface for Year: ")
  print(year)
  
  # download data
  res = dbSendQuery(
    conn=wrds,
    statement=paste0(queryprestring,year,querypoststring)
  )
  tempd <- dbFetch(res)
  dbClearResult(res)
  
  # take last obs each month
  tempd = tempd %>% mutate(time_avail_m = ceiling_date(date, unit = "month")-1)  
  tempm = tempd %>%
    group_by(secid, cp_flag, delta, days, time_avail_m) %>%      
    arrange(secid, cp_flag, delta, days, date) %>%
    filter(row_number()==n()) %>%
    rename(impl_vol = impl_volatility)
  
  # # compute spread
  # tempmwide = tempm %>% select(secid,time_avail_m,cp_flag,impl_vol) %>%
  #     spread(cp_flag, impl_vol)
  # tempmwide = tempmwide %>% mutate(slope = P-C) %>%
  #   select(secid, time_avail_m, slope)
  
  # save and advance  
  vsurfmany[[i]] = tempm
  i = i + 1
  
  end_time <- Sys.time()
  print(end_time - start_time)    
  
}  # end Slope loop over years

# finally, merge years together
vsurfall = do.call(rbind,vsurfmany)

# write to csv
data.table::fwrite(vsurfall,
                   file = paste0(
                     path_dl_me
                     , 'OptionMetricsVolSurf.csv'
                   )
)

# Disconnect from WRDS
dbDisconnect(wrds)

print("Vol Surface data complete: OptionMetricsVolSurf.csv")