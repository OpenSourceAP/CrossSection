# Notes -------------------------------------------
# 2024 08 Andrew: For dealing with the strange data in the 2024 08 version of OptionMetrics Data. The data does not seem right. The implied vols are significantly revised relative to 2023 08. We did not see similar revisions in previous years. 
# To deal with this, we will use the 2023 08 Data Release for signals based on OptionMetrics. This script takes care of this splicing in a somewhat ad-hoc fashion. It's not written for computational reproducibility, but just to track what was done in 2024 08.

# This script is meant to be run after the signals code but before running the portfolios code.

# Setup -------------------------------------------
rm(list=ls())
library(tidyverse)
library(data.table)
library(fs)


# set paths
path_transfer_data = 'D:/Dropbox/AC-OPENAP/transfer_data/2024-08/'
pathProject = 'D:/Dropbox/AC-OPENAP/CrossSection/'
path_temp = 'D:/Dropbox/AC-OPENAP/temp/'
path_vintage = 'D:/Gdrive/Work/Public/Open AP/Data Release 2023.08/'

# create target folders
dir.create(paste0(pathProject, 'Signals/Data/'))
dir.create(paste0(pathProject, 'Signals/Data/Predictors/'))
dir.create(paste0(pathProject, 'Signals/Data/Placebos/'))

# Retrieve signals list -------------------------------

signaldoc = fread(paste0(pathProject, 'SignalDoc.csv')) %>% select(Acronym, Cat.Data, Cat.Signal)

# Move 2024 08 Vintage (except options) -------------------------------------------
setwd(path_transfer_data)

# move predictors, but not options-based
unzip(zipfile = 'Predictors.zip', exdir = path_temp)
files = list.files(paste0(path_temp, 'Signals/Data/Predictors/'))
acronyms = str_remove(files, '.csv')
move_me = acronyms[!acronyms %in% signaldoc$Acronym[signaldoc$Cat.Data == 'Options']]
file.rename(paste0(path_temp, 'Signals/Data/Predictors/', move_me, '.csv'), paste0(pathProject, 'Signals/Data/Predictors/', move_me, '.csv'))

# move placebos (none are options-based, but just to be safe)
unzip(zipfile = 'Placebos.zip', exdir = path_temp)
files = list.files(paste0(path_temp, 'Signals/Data/Placebos/'))
acronyms = str_remove(files, '.csv')
move_me = acronyms[!acronyms %in% signaldoc$Acronym[signaldoc$Cat.Data == 'Options']]
file.rename(paste0(path_temp, 'Signals/Data/Placebos/', move_me, '.csv'), paste0(pathProject, 'Signals/Data/Placebos/', move_me, '.csv'))

# clean up temp folder
unlink(paste0(path_temp, 'Signals'), recursive = TRUE)

# Move Options Signals from 2023.08 Vintage -------------------------------------------
setwd(paste0(path_vintage, 'Firm Level Characteristics/Individual/Predictors/'))
copy_me = paste0(signaldoc$Acronym[signaldoc$Cat.Data == 'Options'], '.csv')
file.copy(copy_me, paste0(pathProject, 'Signals/Data/Predictors/', copy_me))

# Check -------------------------------------------
inproj_predictors = list.files(paste0(pathProject, 'Signals/Data/Predictors/')) %>% str_remove('.csv')
inproj_placebos = list.files(paste0(pathProject, 'Signals/Data/Placebos/')) %>% str_remove('.csv')

print('Predictor Matches:')
sort(signaldoc[Cat.Signal == 'Predictor']$Acronym) == sort(inproj_predictors)

print('Placebo Matches:')
sort(signaldoc[Cat.Signal == 'Placebo']$Acronym) == sort(inproj_placebos)



