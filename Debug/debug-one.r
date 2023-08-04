
# ENVIRONMENT ####
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
rm(list = ls())
# ENTER PROJECT PATH HERE (i.e. this should be the path to your local repo folder & location of SignalDoc.csv)
# if using Rstudio, pathProject = paste0(getwd(), '/') should work
pathProject = paste0(getwd(), '/')
# pathProject = "/cm/chen/openap/release_2023/CrossSection-andrew/"

quickrun =  F # use T if you want to run quickly for testing
quickrunlist = c('Accruals','AM') # list of signals to use for quickrun
skipdaily = T # use T to skip daily CRSP which is very slow
feed.verbose = F # use T if you want lots of feedback

# Check whether project path is set correctly
if (!dir.exists(paste0(pathProject, 'Portfolios'))) {
    stop('Project path not set correctly')
}

# setwd to folder with all R scripts for convenience
setwd(paste0(pathProject,'Portfolios/Code/'))

source('00_SettingsAndTools.R', echo=T)
source('01_PortfolioFunction.R', echo=T)

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# For baseline portfolio tests
# Andrew Chen 2020 01

# ENVIRONMENT AND DATA ====
crspinfo = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspminfo.fst')
) %>% # me, screens, 
  setDT()
crspret = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspmret.fst')
) %>% # returns
  setDT()

# SELECT SIGNALS AND CHECK FOR CSVS ====

source('00_SettingsAndTools.R', echo=T)

strategylist0 <- alldocumentation %>%
  filter(signalname %in% c('BM'))

# strategylist0$Cat.Form = 'continuous'
# strategylist0$q_cut = 0.2
# strategylist0$sweight = 'EW'
# strategylist0$filterstr = 'me>me_nyse20'

strategylist0$SampleStartYear = 1962
strategylist0$SampleEndYear = 1976
strategylist0$q_cut = 0.1

# BASE PORTS ===
port <- loop_over_strategies(
  strategylist0
)

# feedback
checkport(port)



# check gaps  -------------------------------------------------------------



port = port %>% 
  mutate(year = year(date), month = month(date))


checkdat = data.table(
  date = as.Date(seq(min(port$date), max(port$date), by='month'))
) %>% 
  mutate(
    year = year(date), month = month(date)
  ) %>% 
  select(-date)

checkdat = checkdat %>% 
  expand_grid(
    port = unique(port$port)
  ) %>% 
  left_join(port, by = c('year','month','port')) 

checkdat

checkdat %>% 
  filter(year > 1926) %>% 
  group_by(port) %>% 
  summarize(
    nmiss = sum(is.na(ret))
  )


checkdat %>% filter(is.na(ret))

checkdat %>% filter(is.na(ret)) %>% 
  distinct(year, month) %>% 
  left_join(checkdat, by = c('year','month')) %>% 
  print(n=40)