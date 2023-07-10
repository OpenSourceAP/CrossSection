# Environment -------------------------------------------------------------

rm(list = ls())


library(RPostgres)
library(tidyverse)
library(lubridate)
library(haven)
library(data.table)
library(remotes)
library(stataXml)

# secid : The Security ID is the unique identifier for this security.
# Unlike CUSIP numbers and ticker symbols, Security IDs
# are unique over the security’s lifetime and are not recycled.
# The Security ID is the primary key for all data contained in
# IvyDB.

# optionid : Option ID is a unique integer identifier for the option
# contract. This identifier can be used to track specific
# option contracts over time.

# heads up: this assumes (1) running on wrds server and (2) pgpass is set up following this:
# https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-r/r-from-the-web/
wrds <- dbConnect(Postgres(),
                  host='wrds-pgdata.wharton.upenn.edu',
                  port=9737,
                  dbname='wrds',
                  sslmode='require')




#  Query -------------------------------------------------------------

querylimit = 'all' # use 'all' for full data, '20' for debugging

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

securd <- dbFetch(res)
setDT(securd)

yearlist = substr(vsurf_tables$table_name, 7,12)
yearlist = yearlist[1:9]
# yearlist = c("1996")
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
  -- and(abs(b.strike_price/1000/a.close-1) < .1)
  and a.volume > 0
  and b.impl_volatility != 'NaN'
  and b.best_bid > 0                                                          
  and b.open_interest > 0
  and b.volume != 'NaN'
  -- and extract(day from a.date) >= 23
  -- and extract(day from a.date) >= 5

    "
            ," limit "
            ,querylimit
    )
  )      
  tempd <- dbFetch(res)
  setDT(tempd)
  

  
  
  BH_filtered_clean = tempd %>%                                                 # option month
    
    # delete options with absolute values of the natural log of the ratio of the stock price to the exercise press < .1
    filter(abs(log((strike_price/1000) / close)) < .1) %>%
    
    # keep obs where bid-ask prices are within 50% of the average bid-ask (should we do this within secid groups?)
    group_by(secid) %>%
    filter((best_offer - best_bid) < .5*((best_offer + best_bid)/2)) %>%
    ungroup() %>%
    
    # keep last monthly obs of each optionid
    mutate(month = as.numeric(format(date, "%m")),
           day   = as.numeric(format(date, "%d"))) %>%
    group_by(optionid, month) %>%
    filter(day == max(day)) %>%
    arrange(secid, optionid, month) %>% 
    ungroup()
  
  
  BH_filtered_temp = BH_filtered_clean %>%                                      # stock c/p month (average implied volatilties for calls/puts)
    # average monthly implied vol within (stock, call or put)
    group_by(secid, cp_flag, month) %>%
    # mutate(mean_imp_vol = mean(impl_volatility)) %>%
    dplyr::summarize(mean_imp_vol = mean(impl_volatility)) %>%
    ungroup() %>%
    distinct(secid, month, cp_flag, .keep_all = TRUE) %>%
  
    # tidy up
    arrange(secid, month, cp_flag) %>%
    select(secid, month, mean_imp_vol, cp_flag) %>%
    
    # make date variable
    mutate(date = lubridate::ceiling_date(as.Date(paste0(year, "-", month, "-01")), unit = "month") - 1)
    

  
  ## append
  bh_many[[i]] = BH_filtered_temp
  i = i + 1
}

BH_filtered_temp %>% pivot_wider(id_cols = c(month, secid), names_from = cp_flag, values_from = mean_imp_vol)


start_date = as.Date("1996-02-01")
end_date   = as.Date("2005-01-31")

bh_all <- do.call(rbind,bh_many) %>%
  pivot_wider(id_cols = c(date, secid), names_from = cp_flag, values_from = mean_imp_vol) %>%
  
  # join bh_all with tickers
  left_join(securd, by = c("secid")) %>%
  rename(bh_call = C, bh_put = P) %>%
  
  # filter to match sample size
  filter(date > start_date & date <= end_date)


# finally write to csv!
data.table::fwrite(bh_all,
                   "~/data_prep/bali_hovak.csv"
)

