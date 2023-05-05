# Environment -------------------------------------------------------------

rm(list = ls())


library(RPostgres)
library(tidyverse)
library(lubridate)
library(data.table)

# heads up: this assumes (1) running on wrds server and (2) pgpass is set up following this:
# https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-r/r-from-the-web/
wrds <- dbConnect(Postgres(),
                  host='wrds-pgdata.wharton.upenn.edu',
                  port=9737,
                  dbname='wrds',
                  sslmode='require')




# Test Query -------------------------------------------------------------


year = 2001
querylimit = '20' # use 'all' for full data, '20' for debugging

tic = Sys.time()
print(Sys.time() - tic)


# get year list from the Volatility Surface files 
vsurf_tables = dbGetQuery(
  wrds, "
   SELECT table_name 
   FROM information_schema.tables
   WHERE table_schema = 'optionm' 
   AND table_name like 'vsurfd%'
   "
)

# get list of all tickers and security ids in the OptionMetrics universe
res <- dbSendQuery(
  wrds,
  paste0("select ticker, secid from optionm.securd", " limit ",querylimit)
)

tickers <- dbFetch(res)
setDT(tickers)

yearlist = substr(vsurf_tables$table_name, 7,12)

# setup loop ----

bh_many = list()
i = 1
print("Calculating BH's CP vol spread  year by year")
for (year in yearlist) {
  print(Sys.time())
  start_time = Sys.time()
  print(year)
  
  
  ## query daily data with lots of filters
  res <- dbSendQuery(
    wrds
    ,paste0("
  select a.secid, a.date, a.close
  ,b.optionid, b.cp_flag, b.strike_price, b.impl_volatility, b.best_bid, b.best_offer "
            ,"from optionm.secprd"
            ,year
            ," as a inner join optionm.opprcd"
            ,year
            ," as b   
  on a.secid = b.secid and a.date = b.date
  where (b.strike_price != 'NaN') and (b.impl_volatility != 'NaN')              
  and (b.exdate - a.date >= 30) and (b.exdate - a.date <= 90)                 
  and(abs(b.strike_price/1000/a.close-1) < .1)
  and a.volume > 0
  and b.impl_volatility != 'NaN'
  and b.best_bid > 0                                                          
  and b.open_interest > 0
  and b.volume != 'NaN'    
  and extract(day from a.date) >= 23
    "
            ," limit "
            ,querylimit
    )
  )      
  tempd <- dbFetch(res)
  setDT(tempd)
  

  
  
  BH_filtered_temp = tempd %>%
    
    # keep obs where bid-ask prices are within 50% of the average bid-ask (should we do this within secid groups?)
    filter((best_offer - best_bid) < .5*((best_offer + best_bid)/2)) %>% 
    
    # keep last monthly obs of each option [TBC]
    mutate(month = as.numeric(format(date, "%m")),
           day   = as.numeric(format(date, "%d"))) %>%
    group_by(secid, month) %>%
    filter(day == max(day)) %>%
    arrange(secid, date) %>% 
    ungroup() %>%
    
    # average implied vol within (stock, call or put)
    group_by(secid, cp_flag, date) %>%
    summarize(mean_imp_vol = mean(impl_volatility)) %>%
    ungroup()
  
  ## append
  bh_many[[i]] = BH_filtered_temp
  i = i + 1
}


bh_all = do.call(rbind,bh_many)


# finally write to csv!
data.table::fwrite(bh_all,
                   "~/data_prep/bali_hovak.csv"
)
