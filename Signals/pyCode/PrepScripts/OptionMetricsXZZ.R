# Smirk/Skew1 Data from OptionMetrics  
# Created 2020 Andrew
# Updated 2022-02
# Separated from OptionMetricsProcessing.R
# Calculates Smirk a.k.a. Skew1 (Xing Zhang, Zhao 2010)

# Environment -------------------------------------------------------------

rm(list = ls())

querylimit = 'all' # use 'all' for full data, '20' for debugging

path_dl_me = './data_for_dl/'

dir.create(path_dl_me)

library(RPostgres)
library(tidyverse)
library(lubridate)

# heads up: this assumes running on wrds server 
wrds <- dbConnect(Postgres(),
                  host='wrds-pgdata.wharton.upenn.edu',
                  port=9737,
                  dbname='wrds',
                  sslmode='require')


# Smirk a.k.a. Skew1 (Xing Zhang, Zhao 2010) --------------------
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

# Disconnect from WRDS
dbDisconnect(wrds)

print("Smirk/Skew1 data complete: OptionMetricsXZZ.csv")