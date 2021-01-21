## exhibits that use only signals or documentation

### ENVIRONMENT ###
rm(list=ls())
options(stringsAsFactors = FALSE)
options(scipen=999)
optFontsize = 20  # Fix fontsize for graphs here
# optFontFamily = 'Palatino Linotype' # doesn't agree with linux command line
optFontFamily = '' # works with linux command line
library(extrafont)
loadfonts()

library(data.table)
library(tidyverse)
library(readxl)  # readxl is much faster and cleaner than read.xlsx
library(lubridate)
library(feather)
library(xtable)
options(xtable.floating = FALSE)
library(ggpubr)

source('00_SettingsAndFunctions.R')


# Big description table for appendix ------------------------------------------

basicInfo = read_xlsx(
  path = paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet ='BasicInfo'
) %>% 
  filter(Cat.Predictor != '9_drop')

constructionInfo = read_xlsx(
  path = paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet ='Construction'
) %>% 
  select(Acronym, SampleStartYear, SampleEndYear, ConstructionText)

df_merge = basicInfo %>% 
  left_join(constructionInfo) %>% 
  transmute(Authors, 
            Year = as.integer(Year), 
            Predictor = LongDescription, 
            Acronym,
            `Sample Start` = as.integer(SampleStartYear), 
            `Sample End` = as.integer(SampleEndYear),
            Construction = ConstructionText,
            Category = Cat.Predictor %>%
              factor(levels = c('4_not', '3_maybe', '2_likely', '1_clear'),
                     labels = c('not', 'maybe', 'likely', 'clear')),
            Variant = Cat.Variant %>%
              factor(levels = c('1_original', '2_lag', '2_quarterly', '2_risk_model'),
                     labels = c('Original', 'Lag structure', 'Quarterly', 'Risk Model'))
  ) %>% 
  arrange(Authors, Year)

outputtable3 = xtable(df_merge)

print(outputtable3, 
      include.rownames = FALSE,
      include.colnames = FALSE,
      hline.after = NULL,
      only.contents = TRUE,
      file = paste0(pathResults, "bigConstructionTable.tex")
)


# Figure 1 (stock): Correlations (stock level) ----------------------------

## # Signal names
## temp1 = read_xlsx(
##     path = paste0(pathProject,'SignalDocumentation.xlsx')
##   , sheet = 'BasicInfo'
## ) 

## prds = temp1 %>% 
##   filter( (Cat.Predictor == '1_clear' | Cat.Predictor == '2_likely'), Cat.Variant == '1_original') %>% 
##   pull(Acronym)
## signals = read_feather(paste0(pathSignalFile, 'temp.feather'),
##                        columns = c("permno","date", prds))


xxx

csvlist = list.files(
    paste0(pathProject, 'Signals/Data/Predictors/')
    , pattern = '.csv'
)


signals = tibble()
#for (i in 1:length(csvlist)){
    for (i in 1:5){
    print(paste0('reading ', csvlist[i]))

    tempsignalname = substr(csvlist[i],1,nchar(csvlist[i])-4)
    
    temp = fread(paste0(
        pathProject
        , 'Signals/Data/Predictors/'
        ,csvlist[i]
    )) %>%
        rename(signal = !!tempsignalname) %>%
        mutate(signalname = tempsignalname)

    
    signals = rbind(signals,temp)
    
} # for i = 1:length csvlist




# Fig 1a: Pairwise rank correlation of signals
# Note: This computation requires to compute N*(N-1)/2 pairwise rank correlations
#       for roughly 3m rows each. Base cor() takes 3s for each. ccaPP::corSpearman() needs
#       .9s for each. In addition, I parallelize this task for speed reasons.

# Create loop list (there's probably an easier way to get unique pairs)
temp1 = expand.grid(1:length(prds), 1:length(prds)) %>% 
  filter(Var1 > Var2)

loopList = data.frame(Var1 = prds[temp1[, 1]],
                      Var2 = prds[temp1[, 2]])

tic()
cl = makeCluster(cores[1] - 1) 
registerDoParallel(cl)

temp = foreach (i = 1:nrow(loopList),
                .combine = 'c',
                .packages = c('dplyr', 'ccaPP', 'feather')) %dopar% {
                  
                  tempSignals = read_feather(paste0(pathSignalFile, 'temp.feather'),
                                             columns = loopList[i, ] %>% as.character()) %>%
                    filter(complete.cases(.) == TRUE) %>%
                    as.matrix()
                  
                  # If you have a lot of memory, use the block below instead of 
                  # loading pairs of signal to speed things up more
                  
                  # tempSignals = signals %>%
                  #   select(loopList[i,1], loopList[i,2]) %>%
                  #   filter(complete.cases(.) == TRUE) %>%
                  #   as.matrix()
                  
                  corSpearman(x = tempSignals[, 1], 
                              y = tempSignals[, 2], 
                              consistent = FALSE)
                  
                }

#stop cluster
stopCluster(cl)

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram() + 
  labs(x = 'Pairwise rank correlation',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1aStock_pairwisecorrelations.png'), width = 10, height = 8)

toc()


allRhos = tibble(rho = temp, series = 'Pairwise')


# Fig 1b: Rank correlation with size
loopList = expand.grid(prds, 'Size', stringsAsFactors = FALSE) %>% 
  filter(Var1 != Var2)

cl = makeCluster(cores[1] - 1) 
registerDoParallel(cl)

rhos = foreach (i = 1:nrow(loopList),
                .combine = 'c',
                .packages = c('dplyr', 'ccaPP', 'feather')) %dopar% {
                  
                  tempSignals = read_feather(paste0(pathSignalFile, 'temp.feather'),
                                             columns = loopList[i, ] %>% as.character()) %>%
                    filter(complete.cases(.) == TRUE) %>%
                    as.matrix()
                  
                  corSpearman(x = tempSignals[, 1], 
                              y = tempSignals[, 2], 
                              consistent = FALSE)
                  
                }

#stop cluster
stopCluster(cl)

tibble(rho = rhos) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise rank correlation',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1bStock_correlationSize.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = rhos, series = 'Size'))


# Fig 1c: Rank correlation with value
loopList = expand.grid(prds, 'BM', stringsAsFactors = FALSE) %>% 
  filter(Var1 != Var2)

cl = makeCluster(cores[1] - 1) 
registerDoParallel(cl)

temp = foreach (i = 1:nrow(loopList),
                .combine = 'c',
                .packages = c('dplyr', 'ccaPP', 'feather')) %dopar% {
                  
                  tempSignals = read_feather(paste0(pathSignalFile, 'temp.feather'),
                                             columns = loopList[i, ] %>% as.character()) %>%
                    filter(complete.cases(.) == TRUE) %>%
                    as.matrix()
                  
                  corSpearman(x = tempSignals[, 1], 
                              y = tempSignals[, 2], 
                              consistent = FALSE)
                  
                }

#stop cluster
stopCluster(cl)

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise rank correlation',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1cStock_correlationBM.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'BM'))


# Fig 1d: Rank correlation with Momentum
loopList = expand.grid(prds, 'Mom12m', stringsAsFactors = FALSE) %>% 
  filter(Var1 != Var2)

cl = makeCluster(cores[1] - 1) 
registerDoParallel(cl)

temp = foreach (i = 1:nrow(loopList),
                .combine = 'c',
                .packages = c('dplyr', 'ccaPP', 'feather')) %dopar% {
                  
                  tempSignals = read_feather(paste0(pathSignalFile, 'temp.feather'),
                                             columns = loopList[i, ] %>% as.character()) %>%
                    filter(complete.cases(.) == TRUE) %>%
                    as.matrix()
                  
                  corSpearman(x = tempSignals[, 1], 
                              y = tempSignals[, 2], 
                              consistent = FALSE)
                  
                }

#stop cluster
stopCluster(cl)


tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise rank correlation',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1dStock_correlationMom12m.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Momentum (12m)'))


# Fig 1e: Rank correlation with Profitability
loopList = expand.grid(prds, 'GP', stringsAsFactors = FALSE) %>% 
  filter(Var1 != Var2)

cl = makeCluster(cores[1] - 1) 
registerDoParallel(cl)

temp = foreach (i = 1:nrow(loopList),
                .combine = 'c',
                .packages = c('dplyr', 'ccaPP', 'feather')) %dopar% {
                  
                  tempSignals = read_feather(paste0(pathSignalFile, 'temp.feather'),
                                             columns = loopList[i, ] %>% as.character()) %>%
                    filter(complete.cases(.) == TRUE) %>%
                    as.matrix()
                  
                  corSpearman(x = tempSignals[, 1], 
                              y = tempSignals[, 2], 
                              consistent = FALSE)
                  
                }

#stop cluster
stopCluster(cl)

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise rank correlation',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1eStock_correlationGP.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Profitability'))


# Fig 1f: Rank correlation with Investment (Asset Growth)
loopList = expand.grid(prds, 'AssetGrowth', stringsAsFactors = FALSE) %>% 
  filter(Var1 != Var2)

cl = makeCluster(cores[1] - 1) 
registerDoParallel(cl)

temp = foreach (i = 1:nrow(loopList),
                .combine = 'c',
                .packages = c('dplyr', 'ccaPP', 'feather')) %dopar% {
                  
                  tempSignals = read_feather(paste0(pathSignalFile, 'temp.feather'),
                                             columns = loopList[i, ] %>% as.character()) %>%
                    filter(complete.cases(.) == TRUE) %>%
                    as.matrix()
                  
                  corSpearman(x = tempSignals[, 1], 
                              y = tempSignals[, 2], 
                              consistent = FALSE)
                  
                }

#stop cluster
stopCluster(cl)

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise rank correlation',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1fStock_correlationAssetGrowth.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Investment'))


# Print all correlations on same axis
allRhos %>% 
  #  mutate(series = factor(series, levels = c('Pairwise', 'Size', 'Value', 'Momentum', 'Profitability', 'Investment'))) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram() +
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Correlation coefficient',
       y = 'Count') +
  facet_wrap(~series, scales = 'free_y') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1Stock_jointly.png'), width = 10, height = 8)

# save correlations
saveRDS(allRhos, file = paste0(pathResults, 'rhoStockLevel.RDS'))
