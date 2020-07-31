## 2019 12 Andrew
## Does a more precise replication of Gompers, Ishii, Metrix
## By accounting for the month of the IIRC data

options(stringsAsFactors=F)
library(tidyverse)
library(readxl)
library(stringr)
library(lubridate)

tmp <- tempfile()
download.file('https://spinup-000d1a-wp-offload-media.s3.amazonaws.com/faculty/wp-content/uploads/sites/7/2019/06/Governance.xlsx', 
              destfile = tmp, 
              method = 'curl')
 
gov0 = read_excel(path = tmp)
cnames = gov0[23,]
gov0 <- tail(gov0, -23) %>%
    setNames(cnames)

## import data and add months based on xls header.  The 2000 thing is super not clear but shouldn't make much difference

gov1 = gov0 %>%
  group_by(ticker, year) %>% 
  filter(row_number() == 1) %>% 
  ungroup() %>% 
  mutate(
    year = ifelse(year==2000,1999,year)
  ) %>%
  mutate(
    month = case_when(
      year == 1990 ~ 9
      ,year == 1993 ~ 7
      ,year == 1995 ~ 7
      ,year == 1998 ~ 2
      ,year == 1999 ~ 11
      ,year >= 2002 ~ 1
    )
  ) %>%
  mutate(time_avail_m = ymd(paste(as.character(year), as.character(month), '28', sep = '-'))) %>% 
  mutate(time_avail_m = ceiling_date(time_avail_m, unit = 'month') - 1) %>% 
  mutate(ticker = str_trim(ticker)) %>% 
  select(ticker, G, time_avail_m)

GovIndex = gov1 %>% 
  # Interpolate missing dates
  # extend one year beyond end of data
  rbind(tibble(ticker       = unique(gov1$ticker),
               time_avail_m = ymd('2007-01-31'),
               G            = NA_real_)) %>%
  # Fill gaps
  mutate(datem = statar::as.monthly(time_avail_m)) %>% 
  group_by(ticker) %>% 
  statar::fill_gap(datem, roll = TRUE) %>% 
  ungroup() %>% 
  filter(!is.na(G)) %>% 
  # Convert to binary following paper
  mutate(G_Binary = case_when(
    G <= 5 ~ 1,
    G >= 14 ~0, 
    TRUE ~ NA_real_ 
  )) %>%
  mutate(time_avail_m = as.Date(datem)) %>% 
  select(ticker, time_avail_m, G, G_Binary)

## write to disk
data.table::fwrite(GovIndex, file = '../DataRaw/GovIndex.csv') 



  



# ## create grid for interpolation
# alldates = seq(
#   min(gov1$time_avail_m, na.rm=T)
#   ,max(gov1$time_avail_m, na.rm=T)+365 # extend to 1 year past end of data
#   ,by="months"
# )
# 
# allticker = unique(gov1$ticker)
# 
# grid = expand.grid(ticker = allticker,
#                    time_avail_m = alldates, 
#                    stringsAsFactors = FALSE) %>%
#   mutate(time_avail_m = ceiling_date(time_avail_m, unit = "month")-1)
# 
# 
# ## merge onto grid and fill
# gov2 = left_join(
#   grid
#   , gov1
#   , by=c("ticker","time_avail_m")) %>%
#   arrange(ticker,time_avail_m) %>%
#   group_by(ticker) %>%
#   fill(G) %>%
#   ungroup() %>% 
#   filter(!is.na(G)) 
# 



