
# Compare old and new returns from PredictorPortsFull.csv, where
# old returns correspond to the last version of OpenAssetPricing,
# and new returns correspond to the most recent release.

# Prints simple tables to terminal 

# ENVIRONMENT ====
rm(list = ls())
library(tidyverse)
library(data.table)
library(googledrive)
library(gridExtra)

pathProject = 'D:/Dropbox/AC-OPENAP/CrossSection/' 
setwd(paste0(pathProject,'Shipping/Code/'))

dir.create('../Data/temp')
 
# root of August 2023 release
OLD_PATH_RELEASES = 'https://drive.google.com/drive/folders/1EP6oEabyZRamveGNyzYU0u6qJ-N43Qfq'

# root of August 2024
NEW_PATH_RELEASES = 'https://drive.google.com/drive/folders/1-PqsR-tOjv3-U9DRHw85X-VznYlu-Sfc'

# use this for original papers
SUBDIR = 'Full Sets OP'; FILENAME = 'PredictorPortsFull.csv'

# use this for VW or whatever else
# SUBDIR = 'Full Sets Alt'; FILENAME = 'PredictorAltPorts_QuintilesVW.zip'
# SUBDIR = 'Full Sets Alt'; FILENAME = 'PredictorAltPorts_LiqScreen_VWforce.zip'

#=====================================================================#
# Download files                                                  ====
#=====================================================================#

# download old data
OLD_PATH_RELEASES %>% drive_ls() %>%
  filter(name == "Portfolios") %>% drive_ls() %>% 
  filter(name == SUBDIR) %>% drive_ls() %>% 
  filter(name == FILENAME) %>% 
  drive_download(path = paste0("../Data/temp/",FILENAME), overwrite = TRUE)

# import
if (grepl('.csv',FILENAME)){
  old_PredictorPortsFull <- fread(paste0("../Data/temp/",FILENAME))
} else{
  unzip(zipfile = paste0('../Data/temp',FILENAME), exdir = 'temp')
  old_PredictorPortsFull <- fread(
    paste0("../Data/temp/",substr(FILENAME, 1,(nchar(FILENAME)-4)),'.csv')
  )
}

# download new data
id <-  NEW_PATH_RELEASES %>% drive_ls() %>%
  filter(name == "Portfolios") %>% drive_ls() %>% 
  filter(name == SUBDIR) %>% drive_ls() %>% 
  filter(name == FILENAME) %>% 
  drive_download(path = paste0("../Data/temp/",FILENAME), overwrite = TRUE)

# import
if (grepl('.csv',FILENAME)){
  new_PredictorPortsFull <- fread(paste0("../Data/temp/",FILENAME))
} else{
  unzip(zipfile = paste0('../Data/temp',FILENAME), exdir = 'temp')
  new_PredictorPortsFull <- fread(
    paste0("../Data/temp/",substr(FILENAME, 1,(nchar(FILENAME)-4)),'.csv')
  )
}

# download signal doc
NEW_PATH_RELEASES %>% drive_ls() %>% 
  filter(name == "SignalDoc.csv") %>% 
  drive_download(path = "../Data/temp/SignalDoc.csv", overwrite = TRUE)

SignalDoc <- fread("../Data/temp/SignalDoc.csv")



#=====================================================================#
# Mutate dataframes and join                                      ====
#=====================================================================#

# Join and keep observations that match
PredictorPortsFull <- inner_join(
  old_PredictorPortsFull %>% 
    select(-signallag, -Nlong, -Nshort) %>% 
    rename(old_ret = ret) %>% 
    mutate(port = if_else(nchar(port)==2, port, paste0('0',port)))
  , new_PredictorPortsFull %>% 
    select(-signallag, -Nlong, -Nshort) %>% 
    rename(new_ret = ret) %>% 
    mutate(port = if_else(nchar(port)==2, port, paste0('0',port)))
  , by = c("signalname", "port", "date")
  )

# Keep only relevant variables
SignalDoc <- SignalDoc %>% 
  select(Acronym, Year, SampleStartYear, SampleEndYear) %>% 
  rename(YearPub = Year)

# Bring sample years
PredictorPortsFull <- inner_join(
  PredictorPortsFull, SignalDoc,
  by = c("signalname" = "Acronym")) %>% 
  # Classify observations as in-sample or post-publication
  mutate(
    yr = year(date),
    samptype = case_when(
      SampleStartYear <= yr & yr <= SampleEndYear ~ "in-samp",
      yr > YearPub ~ "post-pub"
    )
  )

#=====================================================================#
# Run regressions and export results                              ====
#=====================================================================#

# Regression by group. New returns on old returns
temp1 <- PredictorPortsFull[
  !is.na(samptype)
  , list(
  intercept = coef(lm(new_ret ~ old_ret))[1],
  slope = coef(lm(new_ret ~ old_ret))[2],
  rsq = summary(lm(new_ret ~ old_ret))$r.squared*100,
  new_rbar = mean(new_ret), 
  old_rbar = mean(old_ret)
  )
  , by = c("signalname", "port", "samptype")
  ]

temp2 = PredictorPortsFull[
  year(date) >= SampleStartYear
  , list(
  intercept = coef(lm(new_ret ~ old_ret))[1],
  slope = coef(lm(new_ret ~ old_ret))[2],
  rsq = summary(lm(new_ret ~ old_ret))$r.squared*100,
  new_rbar = mean(new_ret), 
  old_rbar = mean(old_ret)
  )
  , by = c("signalname", "port")
  ] %>% 
  mutate(samptype = 'full-samp')

check = rbind(temp1,temp2) %>% arrange(signalname,port,samptype)


# Export results
write.csv(check, "../Data/temp/PredictorPortsCheck.csv", row.names = FALSE)



#=====================================================================#
# Summary stats output to console ====
#=====================================================================#

check_ls = check %>% 
  filter(port == 'LS', !is.na(samptype), !is.na(slope)) 

check_ls %>% 
  filter(!is.na(samptype)) %>% 
  summarize(
    quantile(slope, 0.05),     quantile(rsq, 0.05)
  )

sumstat = check_ls %>% 
  group_by(samptype) %>% 
  summarize(
      p05 = quantile(rsq, 0.05)
    , p10 = quantile(rsq, 0.10)
    , p25 = quantile(rsq, 0.25)
    , p50 = quantile(rsq, 0.50)
  ) %>% 
  as.data.frame()

print('Rsq from regressing new long-short OP returns on old')
print(sumstat)

check_ls %>% 
  filter(rsq < 98.4) %>% 
  arrange(samptype, rsq) %>% 
  mutate(
    dret = new_rbar - old_rbar
  ) %>% 
  group_by(samptype) %>% 
  summarize(
    mean(abs(dret)), mean(dret)
  )
  
#=====================================================================#
# Check low Rsq ====
#=====================================================================#

print('20 signals with lowest Rsq')
check_ls %>% 
  select(signalname, samptype, rsq, new_rbar, old_rbar) %>% 
  filter(samptype == 'full-samp') %>% 
  arrange(rsq) %>% 
  head(20) %>% 
  print()

