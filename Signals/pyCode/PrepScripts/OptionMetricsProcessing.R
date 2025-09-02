# created 2020? Andrew
# updated 2022 02
# Creates two options-related predictors, and downloads option vol data for a third predictor.


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


# Download and process options data
# this code is so involved I decided to make it separate - Andrew 2019 10
# Whole thing takes about 3 hours to run

# 2/3: Vol Surface -----------------------------------------------------
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



# 3/3: Smirk a.k.a. Skew1 (Xing Zhang, Zhao 2010) --------------------
# from opprcd dataset (option prices)
# this dataset is too big to download more generally, so we 
# calculate for specific uses 
# may take 2 hours

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
skewmany = list()


i = 1
for (year in yearlist) {
  print(Sys.time())
  start_time = Sys.time()
  print("Calculating Smirk aka Skew1 for Year:")
  print(year)     
  
  ## download daily data with lots of filters
  res <- dbSendQuery(
    wrds
    ,paste0("
  select a.secid, a.date, a.close 
  ,b.optionid, b.cp_flag, b.strike_price, b.impl_volatility "
  ,"from optionm.secprd"
  ,year
  ," as a left join optionm.opprcd"
  ,year
  ," as b   
  on a.secid = b.secid and a.date = b.date
  where (b.strike_price != 'NaN') and (b.impl_volatility != 'NaN')
  and (b.exdate - a.date >= 10) and (b.exdate - a.date <= 60)
  and (
    (b.cp_flag = 'C' and b.strike_price/1000/a.close > 0.95 and b.strike_price/1000/a.close < 1.05)
    or
    (b.cp_flag = 'P' and b.strike_price/1000/a.close < 0.95 and b.strike_price/1000/a.close > 0.80)
    )
  and a.volume > 0
  and b.impl_volatility > 0.03 and b.impl_volatility < 2.0
  and (b.best_bid+b.best_offer)/2 > 0.125
  and b.open_interest > 0 and b.volume != 'NaN'    
  and extract(day from a.date) >= 23
    "
   ," limit "
   ,querylimit
	)
  )    
  tempd <- dbFetch(res)
  
  ## find "money-ness-based skew" daily
  tempcall = tempd  %>%
    filter(cp_flag == 'C') %>%
    group_by(secid,date) %>%
    arrange(abs(strike_price/1000/close-1)) %>%
    filter(row_number()==1)    
  tempput = tempd  %>%
    filter(cp_flag == 'P') %>%        
    group_by(secid,date) %>%
    arrange(desc(strike_price/1000/close)) %>%
    filter(row_number()==1)
  tempd2 = inner_join(tempcall,tempput,by=c("secid","date"),suffix=c(".call",".put")) %>%
    mutate(Skew1 = impl_volatility.put - impl_volatility.call)
  
  
  ## average within month (actually last week of the month, see sql query)
  tempm = tempd2 %>%
    mutate(time_avail_m = ceiling_date(date, unit = "month")-1) %>%
    group_by(secid,time_avail_m) %>%
    summarize(Skew1 = mean(Skew1))
  
  ## append
  skewmany[[i]] = tempm
  i = i + 1
  
  end_time <- Sys.time()
  print(end_time - start_time)  
  
  
}  # end Skew loop over years

## finally, merge years together
skewall = do.call(rbind,skewmany)

# write 
data.table::fwrite(skewall,
                   file = paste0(
                       path_dl_me
                       , 'OptionMetricsXZZ.csv'
                       )
                   )
