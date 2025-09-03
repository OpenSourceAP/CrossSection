# Environment -------------------------------------------------------------

rm(list = ls())


library(RPostgres)
library(tidyverse)
library(lubridate)
library(data.table)

# secid : The Security ID is the unique identifier for this security.
# Unlike CUSIP numbers and ticker symbols, Security IDs
# are unique over the security?s lifetime and are not recycled.
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


# Loop over years --------------------------------------------------------------------


bh_many = list()
i = 1
print("Calculating BH's CP vol spread  year by year")
for (year in yearlist) {
  
  print(Sys.time())
  start_time = Sys.time()
  print(year)
  
  
  ## query daily data with lots of filters
  # about 3 million optionid-dailydate obs per year total
  # filters follow page 1799 Section 2 paragraph 2
  res <- dbSendQuery(
    wrds
    , paste0("
  select a.secid, a.date, a.close
            , b.optionid, b.cp_flag, b.exdate, b.strike_price, b.impl_volatility, b.best_bid, b.best_offer "
            ,"from optionm.secprd"
            ,year
            ," as a inner join optionm.opprcd"
            ,year
            ," as b   
  on a.secid = b.secid and a.date = b.date
  where (b.exdate - a.date >= 30) and (b.exdate - a.date <= 90)                   
    and b.open_interest > 0 and b.best_bid > 0 and b.impl_volatility != 'NaN'
    and (b.best_offer - b.best_bid) < 0.5 * (b.best_offer+best_bid)/2
    and abs(ln(abs(close)/(strike_price/1000))) < 0.1
    "
    ," limit "
    ,querylimit
    )
  )      
  tempd <- dbFetch(res)
  setDT(tempd)
  
  # keep last option obs each month (also following same paragraph)
  tempm1 = tempd %>% 
    # keep last monthly obs of each optionid
    mutate(month = as.numeric(format(date, "%m")),
           day   = as.numeric(format(date, "%d"))) %>%
    group_by(optionid, month) %>%
    filter(day == max(day))
  
  # average across options (by different groups)
  tempm2 = tempm1 %>%
    # by call / put
    group_by(secid, cp_flag, month) %>% 
    summarize(
      mean_imp_vol = mean(impl_volatility), mean_day = mean(day), nobs = n()
    ) %>%
    ungroup() %>% 
    rbind(
      # overall
      tempm1 %>%
        group_by(secid, month) %>% 
        summarize(
          mean_imp_vol = mean(impl_volatility), mean_day = mean(day), nobs = n()
        ) %>% 
        ungroup() %>% 
        mutate(cp_flag = 'BOTH')
    ) %>% 
  # clean up
  mutate(date = lubridate::ceiling_date(as.Date(paste0(year, "-", month, "-01")), unit = "month") - 1) %>% 
  arrange(secid, month, cp_flag) %>% 
  select(-month) 
  

  ## append
  bh_many[[i]] = tempm2
  i = i + 1
}


# Bind and Save ---------------------------------------

bh_imp_vol = do.call(rbind,bh_many) %>%
  # join with tickers
  left_join(securd, by = c("secid")) 



# finally write to csv!
data.table::fwrite(bh_imp_vol,
                   "./data_for_dl/bali_hovak_imp_vol.csv"
)

