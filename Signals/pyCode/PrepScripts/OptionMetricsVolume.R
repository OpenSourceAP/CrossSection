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


# Option Volume -------------------------------------------------------
# from opvold dataset
# about 2 min for all data, since it's at the (dailydate,secid,cpflag) level

rm(list = ls(pattern = 'temp'))

# download volume data
start_time = Sys.time()
res = dbSendQuery(conn = wrds, statement = 
                    "select a.*
                      from optionm.opvold as a
                      where a.cp_flag != 'NaN'"
) 
tempd = res %>% dbFetch()
tempd = tempd %>% mutate(time_avail_m = ceiling_date(date, unit = "month")-1)  
dbClearResult(res)
end_time = Sys.time()
print(end_time-start_time)

# sum volume over month by secid, month, calls and puts together
tempm = tempd %>% group_by(secid, time_avail_m) %>%
  summarize(
    optVolume = sum(volume), optInterest = sum(open_interest)
  )

# save
optVolall = tempm

# write to csv
data.table::fwrite(optVolall,
                   file = paste0(
                     path_dl_me
                     , 'OptionMetricsVolume.csv'
                   )
)

# Disconnect from WRDS
dbDisconnect(wrds)

print("Option Volume data complete: OptionMetricsVolume.csv")