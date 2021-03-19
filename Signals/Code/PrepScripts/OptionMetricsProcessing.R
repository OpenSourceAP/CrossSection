
### ENVIRONMENT ###
rm(list = ls())
library(RPostgres)
library(tidyverse)
library(lubridate)


numRowsToPull = -1

pathProject = '/cm/chen/anomalies.com/cfr1/'


# check system for wrds login
sysinfo = Sys.info()
if (sysinfo[1] == "Linux") {

    cat("wrds username: ");
    user  <- readLines("stdin",n=1);
    cat( "\n" )

    cat("wrds password: ");
    pass  <- readLines("stdin",n=1);
    cat( "\n" )

    wrds <- dbConnect(Postgres(), 
                  host='wrds-pgdata.wharton.upenn.edu',
                  port=9737,
                  sslmode='require',
                  user=user,
                  password=pass,
                  dbname='wrds')
}



# Download and process options data
# this code is so involved I decided to make it separate - Andrew 2019 10
# Whole thing takes about 3 hours to run

## === Options Prep 1/3: Smile Slope a.k.a. Slope (Yan) code
# takes about 60 min

# set up loop
rm(list = ls(pattern = 'temp'))

# retrieve list datasets (which years are available)
allsets = dbListTables(wrds)
setlist = allsets[startsWith(allsets,"opprcd")]
setlist = sort(unique(setlist))
yearlist = str_sub(setlist,-4,-1)


slopemany = list()

# Setup query
# adding the filter for deltas and duration speeds query up a lot I think
  queryprestring = paste0("select a.secid, a.date, a.days, a.cp_flag, a.delta "
                          ,",a.impl_volatility "
                         ,"from optionm.vsurfd")
  querypoststring = paste0(
      " as a "
     ,"where (a.impl_volatility != 'NaN')"
     ," and ((a.cp_flag = \'C\' and a.delta = 50)  "
     ,"  or (a.cp_flag = \'P\' and a.delta = -50)) "
     ," and a.days = 30 "
     ," and extract(day from a.date) >= 23 "
  )   

print("Calculating Smile Slope a.k.a. Slope (Yan) year by year")
i = 1
for (year in yearlist) {
  print(Sys.time())
  start_time = Sys.time()
  print(year)
  
  # download data
  res = dbSendQuery(
    conn=wrds,
    statement=paste0(queryprestring,year,querypoststring)
  )
  tempd <- dbFetch(res, numRowsToPull)
  tempd = tempd %>% mutate(time_avail_m = ceiling_date(date, unit = "month")-1)  
  dbClearResult(res)
  
  # take last obs each month
  tempm = tempd %>%
      group_by(secid, cp_flag, time_avail_m) %>%      
      arrange(secid, cp_flag, date) %>%
      filter(row_number()==n()) %>%
      rename(impl_vol = impl_volatility)
  
  # compute spread
  tempmwide = tempm %>% select(secid,time_avail_m,cp_flag,impl_vol) %>%
      spread(cp_flag, impl_vol)
  tempmwide = tempmwide %>% mutate(slope = P-C) %>%
    select(secid, time_avail_m, slope)
  
  # save and advance  
  slopemany[[i]] = tempmwide
  i = i + 1
  
  end_time <- Sys.time()
  print(end_time - start_time)    
  
}  # end Slope loop over years

# finally, merge years together
slopeall = do.call(rbind,slopemany)

## === Options Prep 2/3: Smirk a.k.a. Skew1 (Xing Zhang, Zhao 2010)
# may take 2 hours

# set up loop
rm(list = ls(pattern = 'temp'))

# retrieve list datasets (which years are available)
allsets = dbListTables(wrds)
setlist = allsets[startsWith(allsets,"opprcd")]
setlist = sort(unique(setlist))
yearlist = str_sub(setlist,-4,-1)

skewmany = list()

print("Calculating Smirk aka Skew1 year by year")
i = 1
for (year in yearlist) {
  print(Sys.time())
  start_time = Sys.time()
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
    ")
  )    
  tempd <- dbFetch(res, numRowsToPull)
  
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



## === Options Prep 3/3: Volume
rm(list = ls(pattern = 'temp'))

# option volume will later be merged with stock volume
# about 2 min

# download volume data
start_time = Sys.time()
res = dbSendQuery(conn = wrds, statement = 
                    "select a.*
                      from optionm.opvold as a
                      where a.cp_flag != 'NaN'"
) 
tempd = res %>% dbFetch(n = numRowsToPull)
tempd = tempd %>% mutate(time_avail_m = ceiling_date(date, unit = "month")-1)  
dbClearResult(res)
end_time = Sys.time()
print(end_time-start_time)

# sum volume over month by secid, month, calls and puts together
tempm = tempd %>% group_by(secid, time_avail_m) %>%
  summarize(optVolume = sum(volume))

# save
optVolall = tempm

## === Options Finish: merge datasets from Prep 1-3 and add linking info

rm(list = ls(pattern = 'temp'))
rm(list = c("skewmany","slopemany"))

# download linking file
start_time = Sys.time()
optID = dbSendQuery(conn = wrds, statement = 
                      "select distinct a.secid, a.ticker, a.cusip, a.effect_date
                      from optionm.optionmnames as a
                      "
) %>% dbFetch(n = numRowsToPull)
end_time = Sys.time()
print(end_time-start_time)

# additional prep:
# convert effective dates to monthly, find beginning and end dates
# use year 3000 if no end date
optID = optID %>% 
  mutate(match_begin_m = ceiling_date(effect_date, unit = "month")-1)  %>%
  arrange(secid,match_begin_m) %>%
  group_by(secid) %>%
  mutate(match_end_m = lead(match_begin_m, order_by=secid)) %>%
  mutate(match_end_m = replace_na(match_end_m,as.Date("3000-01-01"))) %>%
  select(-c("effect_date"))


# merge skewall, slopeall, and optID into OptionMetrics
OptionMetrics = full_join(skewall,slopeall,by= c("secid","time_avail_m"))
OptionMetrics = full_join(OptionMetrics,optVolall,by= c("secid","time_avail_m"))
temp1 = left_join(OptionMetrics,optID,by = "secid") 
temp2 = temp1 %>% 
  filter(time_avail_m >= match_begin_m & time_avail_m <= match_end_m )
OptionMetrics = temp2 %>% select(-c("match_begin_m","match_end_m"))

# finally write to csv!
data.table::fwrite(OptionMetrics,
                   file = paste0(
                       pathProject
                       , 'Signals/Data/Prep/OptionMetrics.csv'
                       )
                   )
