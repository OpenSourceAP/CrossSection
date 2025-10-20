# """
# Inputs: Requires credentials for Google Drive, `00_settings.yaml`, and Signal/Portfolio files stored under `pathStorage`.
# Outputs: Downloads legacy portfolio data to `Shipping/Data/temp/` and writes comparison diagnostics to `storage_checks_part2.txt`.
# How to run: Execute after sourcing `00_functions.r`; this script loads helpers automatically.
# Example: `Rscript 4_old_vs_new_check.R`
# """

library(tidyverse)
library(data.table)
library(googledrive)

tryCatch(
  source('00_functions.r'),
  error = function(err) {
    alt_path <- file.path('Shipping', 'Code', '00_functions.r')
    if (file.exists(alt_path)) {
      source(alt_path)
    } else {
      stop(err)
    }
  }
)

paths <- shipping_bootstrap(auth_drive = TRUE)
list2env(paths, envir = environment())

if (is.null(OLD_PATH_RELEASES)) {
  stop('OLD_PATH_RELEASES must be defined in 00_settings.yaml to locate the legacy release folder.')
}

path_temp <- paths$data_temp_dir

# Compare old and new returns from PredictorPortsFull.csv, where
# old returns correspond to the last version of OpenAssetPricing,
# and new returns correspond to the most recent release.

# Prints simple tables to terminal 

#=====================================================================#
# Load data                                                  ====
#=====================================================================#

# download old data
FILENAME = 'PredictorPortsFull.csv'
OLD_PATH_RELEASES %>% drive_ls() %>%
  filter(name == "Portfolios") %>% drive_ls() %>% 
  filter(name == 'Full Sets OP') %>% drive_ls() %>% 
  filter(name == FILENAME) %>% 
  drive_download(path = file.path(path_temp, FILENAME), overwrite = TRUE)

# import
if (grepl('.csv',FILENAME)){
  old_PredictorPortsFull <- fread(file.path(path_temp, FILENAME))
} else{
  unzipped_dir <- file.path(path_temp, 'unzipped')
  if (dir.exists(unzipped_dir)) {
    unlink(unzipped_dir, recursive = TRUE)
  }
  unzip(zipfile = file.path(path_temp, FILENAME), exdir = unzipped_dir)
  on.exit({
    if (dir.exists(unzipped_dir)) {
      unlink(unzipped_dir, recursive = TRUE)
    }
  }, add = TRUE)
  old_PredictorPortsFull <- fread(
    file.path(unzipped_dir, paste0(substr(FILENAME, 1,(nchar(FILENAME)-4)), '.csv'))
  )
}

# # download new data
# id <-  NEW_PATH_RELEASES %>% drive_ls() %>%
#   filter(name == "Portfolios") %>% drive_ls() %>% 
#   filter(name == 'Full Sets OP') %>% drive_ls() %>% 
#   filter(name == FILENAME) %>% 
#   drive_download(path = paste0("../Data/temp/",FILENAME), overwrite = TRUE)

# # import
# if (grepl('.csv',FILENAME)){
#   new_PredictorPortsFull <- fread(paste0("../Data/temp/",FILENAME))
# } else{
#   unzip(zipfile = paste0('../Data/temp',FILENAME), exdir = 'temp')
#   new_PredictorPortsFull <- fread(
#     paste0("../Data/temp/",substr(FILENAME, 1,(nchar(FILENAME)-4)),'.csv')
#   )
# }

# load new data
new_PredictorPortsFull <- fread(
  file.path(pathStorage,'Portfolios/Full Sets OP',FILENAME)
)

# load signal doc
SignalDoc <- fread(
  file.path(pathStorage,'SignalDoc.csv')
)


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
  ) %>% 
  mutate(
    date = as.Date(date)
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
write.csv(check, file.path(path_temp, 'PredictorPortsCheck.csv'), row.names = FALSE)



#=====================================================================#
# Summary stats output to pathStorage/storage_checks_part2.txt ====
#=====================================================================#

sink(file.path(pathStorage,'storage_checks_part2.txt'))
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
