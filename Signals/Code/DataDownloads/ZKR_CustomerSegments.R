# creates customer momentum
# Created Andrew 2019 12


## still currently getting poor matches because of poor company name matching
## > seg_customer %>% filter(gvkey == "001021") %>% select(-c(cid,gareac,gareat)) 
## 19 001021    Schein Henry Inc COMPANY  2.182   2 BUSSEG 2004-06-30
## 20 001021    Schein Henry Inc COMPANY     NA   0 BUSSEG 2005-06-30
## > ccm %>% filter(grepl('SCHEIN',conm))
##    gvkey                      conm  tic     cusip lpermno lpermco     linkdt
## 1 109185 SCHEIN PHARMACEUTICAL INC SHP. 806416103   85952   34727 1998-04-09
## 2 061494          HENRY SCHEIN INC HSIC 806407102   82581   14098 1995-11-03


########## environment
rm(list = ls())

# Check for and potentially install missing packages
install.packages(setdiff(c('tidyverse', 'zoo', 'tm', 'data.table'), rownames(installed.packages())))

library(tidyverse)
library(lubridate)
library(zoo)
library(tm) # for removePunctuation


# Parse arguments
args = commandArgs(trailingOnly = "TRUE")
if (length(args)) {
  arg1 <- args[1]
} else {
  message('Supply path')
}



seg_customer = data.table::fread(file = paste0(arg1, '/Signals/Data/Intermediate/CompustatSegmentDataCustomers.csv')) %>% 
  mutate(datadate = dmy(datadate))

ccm          = data.table::fread(file = paste0(arg1, '/Signals/Data/Intermediate/CCMLinkingTable.csv')) %>% 
  mutate(linkdt    = dmy(linkdt),
         linkenddt = dmy(linkenddt))

m_crsp       = data.table::fread(file = paste0(arg1, '/Signals/Data/Intermediate/mCRSP.csv')) %>% 
  mutate(date = dmy(date))


### CLEAN DATA ###
seg_customer = seg_customer %>% 
  mutate(cnms = toupper(cnms)) %>% 
  filter(ctype == "COMPANY") %>% 
  mutate(cnms = removePunctuation(cnms)) %>%
  filter(
    (cnms != "NOT REPORTED") & !endsWith(cnms,"CUSTOMERS") & !endsWith(cnms,"CUSTOMER")) %>%
  mutate(
    cnms = str_remove(cnms," INC$")
    ,cnms = str_remove(cnms," INC THE$")
    ,cnms = str_remove(cnms," CORP$")
    ,cnms = str_remove(cnms," LLC$")
    ,cnms = str_remove(cnms," PLC$")
    ,cnms = str_remove(cnms," LLP$")
    ,cnms = str_remove(cnms," LTD$")
    ,cnms = str_remove(cnms," CO$")
    ,cnms = str_remove(cnms," SA$")
    ,cnms = str_remove(cnms," AG$")
    ,cnms = str_remove(cnms," AB$")
    ,cnms = str_remove(cnms," CO LTD$")
    ,cnms = str_remove(cnms," GROUP$")
    ,cnms = str_remove_all(cnms,"[ ]")
    ,cnms = str_replace(cnms,"MTR","MOTORS")
    ,cnms = str_replace(cnms,"MOTOR$","MOTORS")        
  ) %>%
  select(gvkey,datadate,cnms) 


ccm0 = ccm %>% mutate(conm = toupper(conm)) %>% mutate(conm = removePunctuation(conm)) %>%
  mutate(
    conm = str_remove(conm," INC$")
    ,conm = str_remove(conm," INC THE$")
    ,conm = str_remove(conm," CORP$")
    ,conm = str_remove(conm," LLC$")
    ,conm = str_remove(conm," PLC$")
    ,conm = str_remove(conm," LLP$")
    ,conm = str_remove(conm," LTD$")
    ,conm = str_remove(conm," CO$")
    ,conm = str_remove(conm," SA$")
    ,conm = str_remove(conm," AG$")
    ,conm = str_remove(conm," AB$")
    ,conm = str_remove(conm," CO LTD$")
    ,conm = str_remove(conm," GROUP$")
    ,conm = str_remove(conm," ")
    ,conm = str_remove_all(conm,"[ ]")
    ,conm = str_replace(conm,"MTR","MOTORS")
    ,conm = str_replace(conm,"MOTOR$","MOTORS")                
  ) 


## add permno data (both firm and customer) 
## need to make sure names are in all uppercase in both seg_customer and ccm!
seg_customer2 = seg_customer %>% 
  inner_join(ccm0, by="gvkey") %>% # add firm permno
  filter((datadate >= linkdt) & (datadate <= linkenddt | is.na(linkenddt))) %>%
  select(gvkey,cnms,datadate,lpermno) %>%
  rename(permno = lpermno) %>% 
  # add customer permno: make sure all names are in same case!
  left_join(ccm0 %>% rename(cust_permno=lpermno) %>% select(-c(gvkey,lpermco))
            , by=c("cnms"="conm")
  ) %>% 
  filter(!is.na(cust_permno),
         (datadate >= linkdt) & (datadate <= linkenddt | is.na(linkenddt))) %>%
  select(permno,datadate,cust_permno) %>% 
  arrange(permno,datadate)

day(seg_customer2$datadate) = 28 # ac: my hack for  day problems for monthly data

## interpolate customer data to monthly w.r.t. time_avail_m (datadate+6 months)
# we're treating crsp dates - 1 month as time_avail_m since these are dates at which we care about data available
tempm0 = m_crsp %>%
  filter(permno %in% unique(seg_customer2$permno)) %>%
  mutate(time_avail_m = date %m-% months(1)) %>%
  select(permno,time_avail_m)

day(tempm0$time_avail_m) = 28


# make customer data wide so we have one entry per permno-datadate and replace NA by -1 to indicate observed lack of customers.  Also make sure to sort first to keep things clean
temp1 = seg_customer2 %>%
  arrange(permno,datadate,cust_permno) %>%
  group_by(permno,datadate) %>%
  mutate(customeri = row_number()) %>%
  spread(customeri, cust_permno,sep="") %>%
  as.data.frame

temp1[is.na(temp1)] = -1


## check if there is customer data next year, if not, make a row of -1 to avoid stale data

temp1b = temp1 %>% arrange(permno,datadate) %>% # lastenry = 1 if missing data for permno next year
  mutate(
    diffpermno = lead(permno)-permno
    ,dyear = year(lead(datadate))-year(datadate)
    ,lastentry = (diffpermno>0) & (dyear != 1)
  )

tempstop = temp1b %>% filter(lastentry) %>%
  mutate(datadate = datadate %m+% years(1)) %>% 
  select(-c(diffpermno,dyear,lastentry))

tempstop[,3:dim(tempstop)[2]] = -1

temp1c = rbind(temp1,tempstop) %>% 
  arrange(permno,datadate)

# use crsp permno-dates as a frame and merge on wide customer data with lag
tempm1 = tempm0 %>% 
  left_join(temp1c %>%
              mutate(time_avail_m = datadate %m+% months(6))
            , 
            by = c("permno","time_avail_m")
  ) %>% 
  select(-c(datadate))

# fill in with most recent available customer 
seg_customer3 =  tempm1 %>%
  arrange(permno,time_avail_m) %>%
  group_by(permno) %>%
  fill(-permno,-time_avail_m) %>% 
  # convert back to long, remove na's and -1's
  gather(customeri,cust_permno,-c(permno,time_avail_m)) %>% 
  filter(!is.na(cust_permno) & (cust_permno > 0)) %>% 
  select(-c(customeri))


## merge m_crsp returns and compute average customer portfolio returns 
tempc = m_crsp %>% 
  filter(permno %in% unique(seg_customer3$cust_permno)) %>%
  mutate(time_avail_m = date,
         cust_permno = permno,
         cust_ret = ret) %>% # return for month t is available in month t
  select(cust_permno,cust_ret,time_avail_m) %>% 
  filter(!is.na(cust_ret))

day(tempc$time_avail_m) = 28

customerMom = left_join(seg_customer3, tempc,
                        by=c("time_avail_m","cust_permno")) %>% 
  filter(!is.na(cust_ret)) %>%  # loses about 12% of the sample, probably dues to poor name matching (see top)
  group_by(time_avail_m,permno) %>%
  summarize(CustMom = mean(cust_ret)) %>% 
  ungroup()

## write to disk
data.table::fwrite(customerMom, file = paste0(arg1, '/Signals/Data/Intermediate/customerMom.csv')) 




