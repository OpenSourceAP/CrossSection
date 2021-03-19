## exhibits that use only signals or documentation

### ENVIRONMENT ###
# For fast calculation of stock-level correlations
install.packages(setdiff(c('ccaPP', 'foreach', 'doParallel', 'tictoc'), 
                         rownames(installed.packages())))

library(ccaPP)
library(foreach)
library(doParallel)
cores = detectCores()
library(tictoc)


# Figure N: Dataset Coverage -------------------

# first count for each paper
count.us = readdocumentation() %>%
    filter(Predictability.in.OP != '9_drop') %>%
    mutate(bench = Cat.Signal == 'Predictor') %>%
    group_by(Predictability.in.OP) %>%
    summarize(
        bench = sum(bench), extended = n()
    )

count.mp = read_excel(
        paste0(pathProject, 'SignalDocumentation.xlsx')
      , sheet = 'MP'
    ) %>%
    mutate(covered = ClosestMatch != '_missing_') %>%
    group_by(Predictability.in.OP) %>%
    summarize(
        n = n(), covered = sum(covered)
    ) %>%
    mutate(pctcov = covered/n*100)

count.ghz = read_excel(
        paste0(pathProject, 'SignalDocumentation.xlsx')
      , sheet = 'GHZ'
    ) %>%
    mutate(covered = ClosestMatch != '_missing_') %>%
    group_by(Predictability.in.OP) %>%
    summarize(
        n = n(), covered = sum(covered)
    ) %>%
    mutate(pctcov = covered/n*100)

count.hlz = read_excel(
        paste0(pathProject, 'SignalDocumentation.xlsx')
      , sheet = 'HLZ'
    ) %>%
    mutate(
        covered = Coverage != 'zz missing'
    ) %>%
    select('Risk factor', Predictability.in.OP
         , covered, Coverage) %>%    
    group_by(Predictability.in.OP) %>%
    summarize(
        n = n(), covered = sum(covered)
    ) %>%
    mutate(pctcov = covered/n*100)


count.hxz = read_excel(
        paste0(pathProject, 'SignalDocumentation.xlsx')
      , sheet = 'HXZ'
    ) %>%
    mutate(covered = ClosestMatch != '_missing_') %>%
    select(HXZname, ClosestMatch, covered
         , Predictability.in.OP.ignoring.holdper
         , holdper)  %>%    
    group_by(ClosestMatch) %>%
    mutate(holdalt = row_number()) %>%
    ungroup() %>%
    mutate(
       Predictability.in.OP = if_else(
            holdalt == 1
          , Predictability.in.OP.ignoring.holdper
          , 'z0_altholdper'
        )
    ) %>%
    group_by(Predictability.in.OP) %>%
    summarize(
        n = n(), covered = sum(covered)
    ) %>%
    mutate(pctcov = covered/n*100)


# merge
tab.n = count.us %>%
    full_join(
        count.mp %>% transmute(Predictability.in.OP, mp = n)
    ) %>%
    full_join(
        count.ghz %>% transmute(Predictability.in.OP, ghz = n)
    ) %>%
    full_join(
        count.hlz %>% transmute(Predictability.in.OP, hlz = n)
    ) %>%
    full_join(
        count.hxz %>% transmute(Predictability.in.OP, hxz = n)
    ) %>%
    replace(is.na(.),0) %>%
    arrange(Predictability.in.OP)

tab.pctcov = count.mp %>%
    transmute(Predictability.in.OP, mp = pctcov) %>%
        full_join(
            count.ghz %>% transmute(Predictability.in.OP, ghz = pctcov)
        ) %>%
        full_join(
            count.hlz %>% transmute(Predictability.in.OP, hlz = pctcov)
        ) %>%
        full_join(
            count.hxz %>% transmute(Predictability.in.OP, hxz = pctcov)
        ) %>%
        replace(is.na(.),0) 

# write to disk
write_xlsx(
    list(n = tab.n, pctcov = tab.pctcov)
  , paste0(pathResults,'coverage.xlsx')
)


# Figure 1 (stock): Correlations (stock level) ----------------------------

# Check which signals have been creatd
checkSignals()

# Focus on Predictors
prds = alldocumentation %>% 
  filter(Cat.Signal == 'Predictor') %>% 
  pull(signalname)

signs = alldocumentation %>% 
  filter(Cat.Signal == 'Predictor') %>% 
  pull(Sign)

# Create table with all Predictors
signals = read_csv(paste0(pathPredictors, prds[1], '.csv')) %>% 
  select(permno, yyyymm)

for (i in 1:length(prds)){

  if (file.exists(paste0(pathPredictors, prds[i], '.csv'))) {
      tempin = read_csv(paste0(pathPredictors, prds[i], '.csv'))
      tempin[,3] = signs[i]*tempin[,3] # sign according top OP
      
    signals = signals %>% full_join(tempin)
      
    print(mem_used())
    gc()
    
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
                  #  gc()
                    
                    corSpearman(x = tempSignals[, 1], 
                                y = tempSignals[, 2], 
                                consistent = FALSE)
                   # gc()

                  #  print(mem_used())
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
