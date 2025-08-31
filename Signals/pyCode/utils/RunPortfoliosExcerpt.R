#%%
rm(list = ls())
# ENTER PROJECT PATH HERE (i.e. this should be the path to your local repo folder & location of SignalDoc.csv)
# if using Rstudio, pathProject = paste0(getwd(), '/') should work
pathProject = '/Users/chen1678/Library/CloudStorage/Dropbox/oap-ac/CrossSection/'

SignalSource = "Python" # use "Stata" for legacy signals (Signals/Data/) or "Python" for new signals (Signals/pyData/)

quickrun =  F # use T if you want to run quickly for testing
quickrunlist = c('MomOffSeason') # list of signals to use for quickrun
feed.verbose = F # use T if you want lots of feedback

# setwd to folder with all R scripts for convenience
setwd(paste0(pathProject,'Portfolios/Code/'))

source('00_SettingsAndTools.R', echo=T)
source('01_PortfolioFunction.R', echo=T)

#%%

tic = Sys.time()
source('20_PredictorPorts.R', echo=T) # 10 min
source('21_PredictorExhibits.R', echo=T)
toc = Sys.time()
print(paste0("Time taken: ", round(as.numeric(difftime(toc, tic, units = "mins")), 2), " minutes"))


#%%
# Copy the results folder to Human/ (assume SignalSource == 'Python')
results_folder <- paste0(pathProject, "Results/")
human_folder <- paste0(pathProject, "Signals/Human/")

list.files(results_folder)

file.copy(from = results_folder, to = human_folder, recursive = TRUE, overwrite = TRUE)
cat("Results folder copied to Human/\n")

portsumfile = paste0(pathProject, "Portfolios/Data/Portfolios/PredictorSummary.xlsx")

file.copy(from = portsumfile, to = paste0(human_folder, 'Results/'), overwrite = TRUE)


