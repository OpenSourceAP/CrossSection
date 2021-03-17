## 2020 02 Andrew
## Manual data download:
##  Pre-1996: https://www.bea.gov/industry/input-output-accounts-data, Click: "Historical Make-Use Tables"
##  1997-present: download zip file: https://apps.bea.gov//industry/iTables%20Static%20Files/AllTablesSUP.zip
##    But keep only Supply_1997-2018_SUM.xlsx (a.k.a. Make)  and Use_SUT_Framework_1997-2018_SUM.xlsx (a.k.a. Use)
## The summary files have roughly 70 industries,
## Based on Menzly-Ozbas Section A.2, there is about a 5-year lag between the survey date and release date
## (I know that seems very long)
## A strict reproduction would use SIC data pre 1997, and use data from here
## https://www.bea.gov/industry/historical-benchmark-input-output-tables
## But every survey year in that data is in a different format and
## the predicability is so strong that it shouldn't matter much

## I'm also sticking to just naisch in Compustat, which isn't really available
## until 1985.  SICH begins in 1987

## for interpretations of IO tables, see Concepts and Methods of the U.S. Input-Output Accounts, section "Composition of the I-O Accounts"


## supplier momentum: weights for an industry's total purchases from other industries: industry comes from cols of use table, matched industries from from rows.  Name means the returns of the supplying firms 

## customer momentum: weights for an industry are its total sales to other industries: industry comes from rows of make (a.k.a. supply) table, matched industries come from cols.  Name means the returns of the customer firms

# need to update end date in filenames (first version used end year 2018, then it was 2019)

rm(list = ls())

# Check for and potentially install missing packages
install.packages(setdiff(c('tidyverse', 'zoo', 'tm', 'data.table'), rownames(installed.packages())))

library(tidyverse) # should be better than xlsx.  definitely faster
library(data.table)
library(stringr)
library(readxl)
library(lubridate)

# Parse arguments
args = commandArgs(trailingOnly = "TRUE")
if (length(args)) {
  arg1 <- args[1]
} else {
  message('Supply path')
}


# check system for dl method
dlmethod = 'auto'
sysinfo = Sys.info()
if (sysinfo[1] == "Linux") {
    dlmethod = 'wget'
}


### DECLARE BIG ASS FUNCTION THAT DOES ALMOST EVERYTHING
generate_one_iomom = function(sheet63,sheet97) {
  
  if (grepl('Use_',sheet97)){
    momtype = 'supplier'
  } else {
    momtype = 'customer'
  }
  
  ### READ IN IO TABLES ###
  
  ## initialize
  indweight = data.frame()
  
  ## read in 1963-1996
  yearlist = excel_sheets(sheet63)
  yearlist = yearlist[-c(1,2)]
  for (year in yearlist){
    
    # read in io matrix and clean up
    temp1 = read_excel(sheet63, year, skip = 6) %>%
      rename(beaind = Code) %>%
      select(-c(2)) %>%
      mutate_at(vars(-beaind), as.numeric) %>%
      as.data.frame()    
    
    # transpose (carefully) if we're using use table (finding momentum of suppliers)
    if (momtype == 'supplier'){
      tempa = temp1 %>% select(-c(beaind))
      rownames(tempa) = temp1$beaind
      tempb = tempa %>% as.matrix %>% t() %>% as.data.frame
      # add industry column
      tempc = data.frame(
        beaind = rownames(tempb)
      )        
      temp1 = cbind(tempc,tempb)
      rownames(temp1) = NULL                
    } # if momtype
    
    # convert to long and add year
    temp2 = temp1 %>%
      pivot_longer(-c(beaind), names_to = "beaindmatch")  %>%
      rename(weight = value) %>%
      filter(!is.na(weight)) %>%
      mutate(year_avail = as.numeric(year)+5)
    
    indweight = rbind(indweight,temp2)
    
  } # for year in yearlist
  
  
  
  ## read in 1997-present
  yearlist = excel_sheets(sheet97)
  for (year in yearlist){
    
    # read in io matrix and clean up
    temp1 = read_excel(sheet97, year, skip = 5) %>%
      rename(beaind = "...1") %>%
      filter(beaind != "IOCode") %>%
      select(-c(2)) %>%
      mutate_at(vars(-beaind), as.numeric) %>%
      as.data.frame()
    
    # transpose (carefully) if we're using use table (finding momentum of suppliers)
    if (momtype == 'supplier'){
      tempa = temp1 %>% select(-c(beaind))
      rownames(tempa) = temp1$beaind
      tempb = tempa %>% as.matrix %>% t() %>% as.data.frame
      # add industry column
      tempc = data.frame(
        beaind = rownames(tempb)
      )        
      temp = cbind(tempc,tempb)
      rownames(temp) = NULL                
    } # if momtype
    
    
    # convert to long and add year
    temp2 = temp1 %>%
      pivot_longer(-c(beaind), names_to = "beaindmatch")  %>%
      rename(weight = value) %>%
      filter(!is.na(weight)) %>%
      mutate(year_avail = as.numeric(year)+5)
    
    indweight = rbind(indweight,temp2)        
    
  } # for year in yearlist
  
  
  
  ### ASSIGN COMPUSTAT FIRM-YEARS TO BEA INDUSTRIES ###
  ## list of beainds by year, with naics prefix in numeric
  indlist = indweight %>% select(year_avail, beaind) %>% distinct() %>%
    mutate(
      naicspre = as.numeric(gsub("([0-9]+).*$", "\\1", beaind))
    ) %>%
    filter(!is.na(naicspre))
  
  
  ## add beaind to compustat
  # note: codes are constant within 3 groups of years
  # create 2, 3, 4, digit naics for merging
  temp1 = comp0 %>%
    mutate(
      naics2 = floor(naics6/1e4)
      ,naics3 = floor(naics6/1e3)
      ,naics4 = floor(naics6/1e2)
    ) 
  
  # merge: this loses about half of firm-months 
  temp2 = temp1 %>%
    left_join(
      indlist %>% rename(beaind2 = beaind)
      , by = c("year_avail" , "naics2" = "naicspre")
    ) %>%
    left_join(
      indlist %>% rename(beaind3 = beaind)
      , by = c("year_avail", "naics3" = "naicspre")
    ) %>%
    left_join(
      indlist %>% rename(beaind4 = beaind)
      , by = c("year_avail", "naics4" = "naicspre")
    ) %>%
    mutate(
      beaind = coalesce(beaind4, beaind3, beaind2)
    ) %>%
    select(gvkey, year_avail, naics6, beaind) %>%
    filter(!is.na(beaind))
  
  comp = temp2
  rm(list = ls(pattern = '^temp'))
  
  ### CREATE BEA INDUSTRY RETURNS
  # add gvkey to crsp
  temp1 = crsp0 %>%
    left_join(
      ccm0
      , by = c("permno")
    ) %>%
    filter(date >= linkdt, date <= linkenddt) %>%
    select(permno,date,ret,mve_c,gvkey) %>%
    mutate(year = year(date), month = month(date))
  # add bea industries
  temp2 = left_join(temp1, comp, by=c("gvkey","year"="year_avail")) %>%
    filter(!is.na(beaind))
  
  crsp2 = temp2 
  
  ## create industry returns
  temp = crsp2 %>% group_by(year,month,beaind) %>%
    summarize(
      ret = weighted.mean(ret,mve_c)
      , n = n()
    ) %>% arrange(year,month,beaind) %>% 
    ungroup()
  
  ## remove years where NAICS is unavailable
  # temp %>% group_by(year,month) %>% summarize(n = sum(n))  # this shows availabilitliy
  temp = temp %>% filter(year >= 1986)
  
  indret = temp
  
  
  ### CREATE MATCHED INDUSTRY RETURN
  
  # expand indweights to beaind-year-month-beaindmatch  and remove own-industry weights
  temp1 = left_join(    
    indret %>% select(year,month)
    , indweight %>% filter(beaind != beaindmatch) 
    , by = c("year"="year_avail")
  )
  # add matched-industry's returns
  temp2 = temp1 %>%
    left_join(
      indret %>% rename(retmatch = ret) %>% select(-n)
      , by = c("beaindmatch"="beaind","year","month")
    ) %>%
    filter(!is.na(retmatch))
  # find means using IO weights
  temp3 = temp2 %>% group_by(year,month,beaind) %>%
    summarize(
      retmatch = weighted.mean(retmatch,weight)
    ) %>% 
    ungroup()
  matchret = temp3
  
  
  
  ### CREATE FIRM LEVEL SIGNAL
  
  ## assign industries to portfolios each month
  tempportind = matchret %>%
    filter(!is.na(retmatch)) %>%
    group_by(year,month) %>%
    mutate(portind = findInterval(
      retmatch, quantile(retmatch, 0:10/10), rightmost.closed=T
    ))
  
  ## assign gvkey-months to industry portfolios    
  iomom = crossing(
    comp
    , data.frame(month_avail = 1:12)
  ) %>%
    left_join(
      tempportind %>% select(year,month,beaind,portind)
      , by = c("year_avail"="year","month_avail"="month","beaind")
    )
  
  ## check stock assignments (from industry sorts)
  print("checking stock assignments:")    
  temp = crsp2 %>% left_join(
    iomom
    , by=c('gvkey','year'='year_avail','month'='month_avail')
  ) %>%
    mutate(
      iomom = dplyr::lag(portind, n = 1, default = NA)
    ) %>%
    group_by(year,month,iomom) %>%
    summarize(
      ret = mean(ret,na.rm=T)
      , nind = n()
    )  %>%
    arrange(year,month,iomom) %>%
    pivot_wider(-nind,names_from=iomom,values_from=ret,names_prefix='port')  %>%
    mutate(portLS = port10-port1)    
  
  temp2 = temp %>%
    filter(year >= 1986, year <= 2005) %>%
    pivot_longer( contains('port'), names_to='port' ) %>%
    rename(ret = value) %>%
    group_by(port) %>%    
    summarize(
      mean  = mean(ret,na.rm=T) ,
      vol = sd(ret,na.rm=T) ,
      nmonths = n(),
      tstat = mean/vol*sqrt(nmonths)          
    )
  
  print(temp2)
  
  return(iomom)
  
} # END BIG ASS FUNCTION

### READ IN RAW DATA 

# read compustat, turn to annual, lag data by one year for simplicity
# being lazy about timing, this is ridiculously conservative.  Code doesn't handle monthly cleanly
comp0 = fread(paste0(arg1, '/Signals/Data/Intermediate/CompustatAnnual.csv')) %>%
  as.data.frame()  %>%
  mutate(
    naicsstr = str_pad(
      as.character(naicsh), 6, side = c("right"), pad = "0"
    )
    , naics6 = as.numeric(naicsstr)
    , year_avail = year(dmy(datadate) %m+% months(6) )+1
  ) %>%
  filter(!is.na(naics6)) %>%
  select(gvkey, year_avail, naics6, datadate)

# read crsp
crsp0 = fread(paste0(arg1, '/Signals/Data/Intermediate/mCRSP.csv')) %>%
  transmute(
    permno
    , date = dmy(date)
    , ret=100*ret
    , mve_c = abs(prc)*shrout
  ) %>%
  filter(!is.na(ret),!is.na(mve_c))

# read ccm, replacing missing linkenddt with date of apocalypse fortold (fourtold?) in lost papyrus
ccm0  = fread(paste0(arg1, '/Signals/Data/Intermediate//CCMLinkingTable.csv')) %>%
  mutate(linkenddt = ifelse(linkenddt=="", "31dec3000", linkenddt)) %>% 
  transmute(
    gvkey
    , permno = lpermno
    , linkprim
    , linkdt = dmy(linkdt)
    , linkenddt = dmy(linkenddt)
  ) 

### MAKE TWO FLAVORS OF MOMENTUM AND MERGE

# Make table before 1997
download.file("https://apps.bea.gov/industry/xls/io-annual/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx",
              destfile = paste0(arg1, '/Signals/Data/Intermediate//IOMake_Before_Redefinitions_1963-1996_Summary.xlsx'), 
              method = dlmethod,
              mode = 'wb'
              )

# Use table before 1997
download.file("https://apps.bea.gov/industry/xls/io-annual/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx",
              destfile = paste0(arg1, '/Signals/Data/Intermediate//IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx'),
              method = dlmethod,
              mode = 'wb')

# Tables starting in 1997
tmp = tempfile()
download.file("https://apps.bea.gov//industry/iTables%20Static%20Files/AllTablesSUP.zip",
              destfile = tmp, 
              method = dlmethod)

unzip(tmp, 
      files = c('Supply_1997-2019_SUM.xlsx', 'Use_SUT_Framework_1997-2019_SUM.xlsx'),
      exdir = paste0(arg1, '/Signals/Data/Intermediate'))


## customer momentum: weights for an industry are its total sales to other industries: industry comes from rows of make table, matched industries come from cols
sheet97 = paste0(arg1, '/Signals/Data/Intermediate/Supply_1997-2019_SUM.xlsx')
sheet63 = paste0(arg1, '/Signals/Data/Intermediate/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx')

iomomcust = generate_one_iomom(sheet63,sheet97)

## supplier momentum: weights for an industry's total purchases from other industries: industry comes from cols of use table, matched industries from from rows
sheet97 = paste0(arg1, '/Signals/Data/Intermediate/Use_SUT_Framework_1997-2019_SUM.xlsx')
sheet63 = paste0(arg1, '/Signals/Data/Intermediate/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx')
iomomsupp = generate_one_iomom(sheet63,sheet97)


iomom = left_join(
  iomomcust %>% transmute(
    gvkey
    , year_avail
    , month_avail
    , iomom_cust = portind
  )
  ,
  iomomsupp %>% transmute(
    gvkey
    , year_avail
    , month_avail
    , iomom_supp = portind
  )
)

iomom = iomom %>% filter( !( is.na(iomom_cust) & is.na(iomom_supp)) )

### SAVE
haven::write_dta(iomom, path = paste0(arg1, '/Signals/Data/Intermediate/InputOutputMomentum.dta'))
#data.table::fwrite(iomom, file = '../Data/InputOutputMomentum.csv') 
