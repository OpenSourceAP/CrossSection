#%%

args = commandArgs(trailingOnly=TRUE)

#%% ====
# From master.R 
pathProject = '~/Dropbox/oap-ac/CrossSection/'
SignalSource = "Python" # use "Stata" for legacy signals (Signals/Data/) or "Python" for new signals (Signals/pyData/)

setwd(paste0(pathProject,'Portfolios/Code/'))
source('00_SettingsAndTools.R', echo=T)
source('01_PortfolioFunction.R', echo=T)

# Default values
quickrun = T # use T if you want to run quickly for testing
quickrunlist = c('OptionVolume1','OptionVolume2') # default list

# Parse command line arguments for quickrunlist
if (length(args) > 0) {
  quickrunlist = args
}
skipdaily = T # use T to skip daily CRSP which is very slow
feed.verbose = F # use T if you want lots of feedback

# ENVIRONMENT AND DATA 
crspinfo = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspminfo.fst')
) %>% # me, screens, 
  setDT()
crspret = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspmret.fst')
) %>% # returns
  setDT()

#%%

# SELECT SIGNALS AND CHECK FOR CSVS ===

strategylist0 <- alldocumentation %>% filter(Cat.Signal == "Predictor")
strategylist0 <- ifquickrun()

csvlist = list.files(pathPredictors) %>% as_tibble() %>% rename(signalname=value) %>%
  mutate(
    signalname = substr(signalname,1,str_length(signalname)-4)
    , in_csv = 1
  )

missing = strategylist0 %>% select(signalname) %>% left_join(csvlist) %>%
  filter(is.na(in_csv)) # note: CRSP predictors are put into pathPredictors by 11_CreateCRSPPredictors.R

if (dim(missing)[1]>0){
  print('Warning: the following predictor signal csvs are missing:')
  print(missing$signalname)
  
  temp = readline('press enter to continue, type quit to quit: ')
  if (temp=='quit'){print('erroring out'); stop()}
}

# BASE PORTS 
port <- loop_over_strategies(
  strategylist0
)

# feedback
sumnew0 = checkport(port)

#%% compare

library(readxl)

# compare with old xlsx
sumold0 = read_xlsx(paste0(pathProject, 'Signals/pyCode/StataComparison/PredictorSummary2024.xlsx'))

sumold = sumold0 %>% select(signalname, tstat, rbar, vol, T, Nlong, Nshort)  %>% 
  filter(signalname %in% quickrunlist)

new_vs = sumnew0 %>% 
  filter(port == "LS") %>%
  select(signalname, tstat, rbar, vol, T, Nlong, Nshort)  %>% 
  pivot_longer(cols = !signalname, names_to = "metric", values_to = "new") %>% 
  left_join(
    sumold0 %>% select(signalname, tstat, rbar, vol, T, Nlong, Nshort) %>% 
      pivot_longer(cols = !signalname, names_to = "metric", values_to = "old")
  ) %>% 
  mutate(
    diff = new - old
  )

print('===============================================')
print('\n\n New vs old portfolios:')
print(new_vs)

#%%
# save  to md file

# first jsut t-stats
tstat = new_vs %>% filter(metric == 'tstat')

txt <- capture.output(print(format(tstat, justify = "right"), row.names = FALSE))
writeLines(txt, paste0(pathProject, 'Signals/Logs/TestOutPortFocused.md'))

# Save t-stat comparison as CSV for Python integration
write.csv(tstat, paste0(pathProject, 'Signals/Logs/TestOutPortFocused.csv'), row.names = FALSE)

# then all 
cat('\n\n All metrics:\n', file = paste0(pathProject, 'Signals/Logs/TestOutPortFocused.md'), append = TRUE)


txt <- capture.output(print(format(new_vs, justify = "right"), row.names = FALSE))
cat(
  paste0(txt, '\n'), 
  file = paste0(pathProject, 'Signals/Logs/TestOutPortFocused.md'), 
  append = TRUE)

#%%