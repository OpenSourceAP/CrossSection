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

source('00_SettingsAndFunctions.R')

# For fast calculation of stock-level correlations
library(ccaPP)
library(foreach)
library(doParallel)
cores = detectCores()
library(tictoc)

# Figure 1 (stock): Correlations (stock level) ----------------------------

# Check which signals have been creatd
checkSignals()

# Focus on Predictors
prds = alldocumentation %>% 
  filter(Cat.Signal == 'Predictor') %>% 
  pull(signalname)

# Create table with all Predictors
signals = read_csv(paste0(pathPredictors, prds[1], '.csv')) %>% 
  select(permno, yyyymm)

for (i in prds){

  if (file.exists(paste0(pathPredictors, i, '.csv'))) {
    signals = signals %>% 
      full_join(
        read_csv(paste0(pathPredictors, i, '.csv')) 
      ) 
  } else {
    message(paste(i, ' does not exist in Data/Predictors folder'))
  }
} 


# Create loop list (there's probably an easier way to get unique pairs)
prds = names(signals %>% select(-permno, -yyyymm))

temp1 = expand.grid(1:length(prds), 1:length(prds)) %>% 
  filter(Var1 > Var2)

loopList = data.frame(Var1 = prds[temp1[, 1]],
                      Var2 = prds[temp1[, 2]])

# Fig 1a: Pairwise rank correlation of signals
# Note: This computation requires to compute N*(N-1)/2 pairwise rank correlations
#       for roughly 3m rows each. Base cor() takes 3s for each. ccaPP::corSpearman() needs
#       .9s for each. In addition, I parallelize this task for speed reasons.

# Save data to go easier on memory
write_fst(signals, path = paste0(pathDataIntermediate, 'temp.fst'))
rm(signals)

tic()
cl = makeCluster(cores[1] - 1) 
registerDoParallel(cl)

temp = foreach (i = 1:nrow(loopList),
                .combine = 'c',
                .packages = c('dplyr', 'ccaPP', 'fst')) %dopar% {
                  
                  tempSignals = read_fst(paste0(pathDataIntermediate, 'temp.fst'),
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
  geom_histogram() + 
  labs(x = 'Pairwise rank correlation',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1aStock_pairwisecorrelations.png'), width = 10, height = 8)

toc()

allRhos = tibble(rho = temp, series = 'Pairwise')


# Rank correlations with various standard predictors
vars = c('Size', 'BM', 'Mom12m', 'GP', 'AssetGrowth')

for (vv in vars) {

    print(vv)

  # Create grid
  loopList = expand.grid(prds, vv, stringsAsFactors = FALSE) %>% 
    filter(Var1 != Var2)

  # Start cluster
  cl = makeCluster(cores[1] - 1) 
  registerDoParallel(cl)

  # compute correlations
  rhos = foreach (i = 1:nrow(loopList),
                  .combine = 'c',
                  .packages = c('dplyr', 'ccaPP', 'fst')) %dopar% {
                    
                    tempSignals = read_fst(paste0(pathDataIntermediate, 'temp.fst'),
                                           columns = loopList[i, ] %>% as.character()) %>%
                      filter(complete.cases(.) == TRUE) %>%
                      as.matrix()
                    
                    corSpearman(x = tempSignals[, 1], 
                                y = tempSignals[, 2], 
                                consistent = FALSE)
                    
                  }
  
  #stop cluster
  stopCluster(cl)

  # Plot histogram  
  tibble(rho = rhos) %>% 
    ggplot(aes(x = rho)) +
    geom_histogram(bins = 25) + 
    coord_cartesian(xlim = c(-1,1)) +
    labs(x = 'Pairwise rank correlation',
         y = 'Count') +
    theme_minimal(base_size = optFontsize, base_family = optFontFamily) 
  
  ggsave(filename = paste0(pathResults, 'fig1SignalCorrelationWith_', vv, '.png'), width = 10, height = 8)
  
  allRhos = rbind(allRhos,
                  tibble(rho = rhos, series = vv))

  rm(loopList, rhos)  
  
}

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
