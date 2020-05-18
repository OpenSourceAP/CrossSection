## Exhibits for paper

### ENVIRONMENT ###
rm(list=ls())
options(stringsAsFactors = FALSE)
options(scipen=999)
optFontsize = 20  # Fix fontsize for graphs here
optFontFamily = 'Palatino Linotype'
library(extrafont)
loadfonts()

library(data.table)
library(tidyverse)
library(readxl)  # readxl is much faster and cleaner than read.xlsx
library(lubridate)
library(feather)
library(xtable)
options(xtable.floating = FALSE)

# For fast calculation of stock-level correlations
library(ccaPP)
library(foreach)
library(doParallel)
cores = detectCores()
library(tictoc)


if (Sys.getenv("USERNAME") != 'Tom') {
  setwd("/cm/chen/anomalies.com/code.fed")
  pathSignalFile = '../DataOutput/'
  pathCostFile   = '../DataOutput/'
  pathSummary    = '../DataSummary/'
  pathResults    = '../Exhibits/'
  pathStratMonth = '../DataStratMonth/'
} else {
  pathSignalFile = '../DataClean/'
  pathCostFile   = '../DataClean/'
  pathSummary    = 'C:/Users/Tom/Google Drive/anomalies.com/DataSummary/'
  pathResults    = 'C:/Users/Tom/Google Drive/anomalies.com/Exhibits/'
  pathStratMonth = 'C:/Users/Tom/Google Drive/anomalies.com/DataStratMonth/'  
}




# Figure 1 (stock): Correlations (stock level) ----------------------------

# Signal names
temp1 = read_xlsx(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet = 'BasicInfo'
) 

prds = temp1 %>% 
  filter( (Cat.Predictor == '1_clear' | Cat.Predictor == '2_likely'), Cat.Variant == '1_original') %>% 
  pull(Acronym)

signals = read_feather(paste0(pathSignalFile, 'temp.feather'),
                       columns = c("permno","date", prds))

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

# Figure 1 (Port): Correlations (Portfolio level) -------------------------

## import baseline returns
portbase = fread(paste0(pathStratMonth, 'retWide_SignalMonth_base.csv')) %>% 
  as_tibble() %>% 
  mutate(date = ymd(date) %>% 
           floor_date(unit = 'month'))

## import header data
temp1 = read_xlsx(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet = 'BasicInfo'
) 

# Subset to baseline predictors
clearPreds = temp1 %>% 
  filter( (Cat.Predictor == '1_clear' | Cat.Predictor == '2_likely'), Cat.Variant == '1_original') %>% 
  pull(Acronym)

portbase = portbase %>%
  select(all_of(clearPreds), date)

## Import factor returns
df_FF3 = read_csv('../DataRaw/mFamaFrench.csv') %>% 
  mutate(date = ymd(date))

download.file('http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip',
              destfile = 'temp.zip')
unzip('temp.zip')

df_OPInv = read_csv('F-F_Research_Data_5_Factors_2x3.CSV', skip = 3) %>% 
  mutate(date = as.Date(paste0(as.character(X1), '01'), format='%Y%m%d') %>% 
           ymd()) %>% 
  filter(!is.na(date)) %>% 
  mutate_at(.vars = vars(RMW, CMA),
            .funs = list(as.numeric))


# Fig 1a: Pairwise correlation of strategy returns
temp = cor(portbase %>% select(-date), 
           use = 'pairwise.complete.obs')

# To avoid double counting
temp = temp[lower.tri(temp)]

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram() + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise correlation coefficient',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1aPort_pairwisecorrelations.png'), width = 10, height = 8)


allRhos = tibble(rho = temp, series = 'Pairwise')

# Fig 1b: Correlation with SMB
tempRets = portbase %>% 
  inner_join(df_FF3 %>% 
               select(date, smb))

temp = cor(tempRets %>% select(-date, -smb),
           tempRets %>% select(smb),
           use = 'pairwise.complete.obs')

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise correlation coefficient',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1bPort_correlationSMB.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Size'))


# Fig 1c: Correlation with BM
tempRets = portbase %>% 
  inner_join(df_FF3 %>% 
               select(date, hml))

temp = cor(tempRets %>% select(-date, -hml),
           tempRets %>% select(hml),
           use = 'pairwise.complete.obs')

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise correlation coefficient',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1cPort_correlationHML.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Value'))

# Fig 1d: Correlation with UMD
tempRets = portbase %>% 
  inner_join(df_FF3 %>% 
               select(date, umd))

temp = cor(tempRets %>% select(-date, -umd),
           tempRets %>% select(umd),
           use = 'pairwise.complete.obs')

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise correlation coefficient',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1dPort_correlationUMD.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Momentum'))

# Fig 1e: Correlation with OP
tempRets = portbase %>% 
  inner_join(df_OPInv %>% 
               select(date, RMW))

temp = cor(tempRets %>% select(-date, -RMW),
           tempRets %>% select(RMW),
           use = 'pairwise.complete.obs')

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise correlation coefficient',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1ePort_correlationOP.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Profitability'))

# Fig 1f: Correlation with Inv
tempRets = portbase %>% 
  inner_join(df_OPInv %>% 
               select(date, CMA))

temp = cor(tempRets %>% select(-date, -CMA),
           tempRets %>% select(CMA),
           use = 'pairwise.complete.obs')

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise correlation coefficient',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1fPort_correlationCMA.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Investment'))


# Print all correlations together
allRhos %>% 
  mutate(series = factor(series, levels = c('Pairwise', 'Size', 'Value', 'Momentum', 'Profitability', 'Investment'))) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram() +
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Correlation coefficient',
       y = 'Count') +
  facet_wrap(~series, scales = 'free_y') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1Port_jointly.png'), width = 10, height = 8)


# Figure 2: Replication rates ---------------------------------------------

df = read_xlsx(paste0(pathSummary, 'SignalSummaryBase.xlsx')) %>% 
  mutate(success = 1*(round(tstat, digits = 2) >=1.96))

df_meta = read_xlsx(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet = 'BasicInfo'
) %>% 
  mutate_at(.vars = vars(starts_with('Cat.')),
            .funs = list(str_to_title))

# Use most recent Category labels
df = df %>% 
  select(signalname, success, tstat) %>% 
  left_join(df_meta %>% 
              select(Acronym, starts_with('Cat.')),
            by = c('signalname' = 'Acronym'))

# Replication rates by predictor category
labelData = df %>% 
  filter(Cat.Predictor != '9_drop', Cat.Variant == '1_original') %>% 
  group_by(Cat.Predictor) %>%
  summarise(rate = mean(success),
            n = n()) %>% 
  mutate(rate = paste(round(100*rate, 0) %>% as.character(), '%')) %>% 
  ungroup()

df %>%
  filter(Cat.Predictor != '9_drop', Cat.Variant == '1_original') %>% 
  group_by(Cat.Predictor, success) %>%
  count() %>% 
  ggplot(aes(x = Cat.Predictor %>% 
               factor(levels = c('4_not', '3_maybe', '2_likely', '1_clear'),
                      labels = c('not', 'maybe', 'likely', 'clear')), y = n, 
             fill = factor(success, levels = c(0, 1), labels = c('No', 'Yes')))) +
  geom_col(position = 'stack') +
  labs(y = 'Number of predictors',
       x = 'Predictor Category',
       fill = '|t-stat| > 1.96') +
  scale_fill_manual(values = c(rep(c("gray75", "gray45")))) +
  guides(fill = guide_legend(reverse = TRUE)) +
  coord_flip() +
  geom_text(data = labelData,
            aes(label = rate, fill = NA),
            nudge_y = 8) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig2a_reprate_predictorCategories.png'), width = 10, height = 8)

# Alternative representation: Reprate predictor categories
df %>%
  filter(Cat.Predictor != '9_drop', Cat.Variant == '1_original') %>% 
  transmute(Cat.Predictor, success, tstat = abs(tstat)) %>% 
  ggplot(aes(x = Cat.Predictor %>% 
               factor(levels = c('4_not', '3_maybe', '2_likely', '1_clear'),
                      labels = c('not', 'maybe', 'likely', 'clear')), y = tstat)) +
  geom_jitter(width = .2, height = 0) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  #  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(y = 't-statistic',
       x = 'Predictor Category') +
  coord_flip() +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig2a_reprate_predictorCategoriesJitter.png'), width = 10, height = 8)


# Replication success by data category (for baseline ones)
labelData = df %>% 
  filter(Cat.Predictor == '1_clear', Cat.Variant == '1_original') %>% 
  group_by(Cat.Data) %>%
  summarise(rate = mean(success),
            n = n()) %>% 
  mutate(rate = paste(round(100*rate, 0) %>% as.character(), '%')) %>% 
  ungroup()

df %>%
  filter(Cat.Predictor == '1_clear', Cat.Variant == '1_original') %>% 
  group_by(Cat.Data, success) %>%
  count() %>% 
  ggplot(aes(x = Cat.Data %>% fct_rev() %>% relevel('Other'), y = n, 
             fill = factor(success, levels = c(0, 1), labels = c('No', 'Yes')))) +
  geom_col(position = 'stack') +
  labs(y = 'Number of predictors',
       x = 'Data Category',
       fill = '|t-stat| > 1.96') +
  scale_fill_manual(values = c(rep(c("gray75", "gray45")))) +
  guides(fill = guide_legend(reverse = TRUE)) +
  coord_flip() +
  geom_text(data = labelData,
            aes(label = rate, fill = NA),
            nudge_y = 5) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig2b_reprate_data.png'), width = 10, height = 8)

# Alternatively: Jitter plot
df %>%
  filter(Cat.Predictor == '1_clear', Cat.Variant == '1_original') %>% 
  transmute(Cat.Data, success, tstat = abs(tstat)) %>% 
  ggplot(aes(x = Cat.Data %>% fct_rev() %>% relevel('Other'), 
             y = tstat)) +
  geom_jitter(width = .15, height = 0) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  labs(y = 't-statistic',
       x = 'Predictor Category') +
  coord_flip() +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig2b_reprate_data_Jitter.png'), width = 10, height = 8)


# Replication success by economic category
labelData = df %>% 
  filter(Cat.Predictor == '1_clear', Cat.Variant == '1_original') %>% 
  group_by(Cat.Economic) %>%
  summarise(rate = mean(success),
            n = n()) %>% 
  mutate(rate = paste(round(100*rate, 0) %>% as.character(), '%')) %>% 
  ungroup()

df %>%
  filter(Cat.Predictor == '1_clear', Cat.Variant == '1_original') %>% 
  group_by(Cat.Economic, success) %>%
  count() %>% 
  ggplot(aes(x = Cat.Economic %>% fct_rev() %>% relevel('Other'), y = n, 
             fill = factor(success, levels = c(0, 1), labels = c('No', 'Yes')))) +
  geom_col(position = 'stack') +
  labs(y = 'Number of predictors',
       x = 'Economic Category',
       fill = '|t-stat| > 1.96') +
  scale_fill_manual(values = c(rep(c("gray75", "gray45")))) +
  guides(fill = guide_legend(reverse = TRUE)) +
  coord_flip() +
  geom_text(data = labelData,
            aes(label = rate, fill = NA),
            nudge_y = 2) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig2c_reprate_economic.png'), width = 10, height = 8)


# Replication success for variants of clear predictors
labelData = df %>% 
  filter(Cat.Predictor == '1_clear', Cat.Variant != '1_original') %>% 
  mutate(Cat.Variant = factor(Cat.Variant, 
                              levels = c('2_lag', '2_quarterly', '2_risk_model'),
                              labels = c('Lag structure', 'Quarterly', 'Risk Model'))) %>% 
  group_by(Cat.Variant) %>%
  summarise(rate = mean(success),
            n = n()) %>% 
  mutate(rate = paste(round(100*rate, 0) %>% as.character(), '%')) %>% 
  ungroup()

df %>%
  filter(Cat.Predictor == '1_clear', Cat.Variant != '1_original') %>% 
  mutate(Cat.Variant = factor(Cat.Variant, 
                              levels = c('2_lag', '2_quarterly', '2_risk_model'),
                              labels = c('Lag structure', 'Quarterly', 'Risk Model'))) %>% 
  group_by(Cat.Variant, success) %>%
  count() %>% 
  ggplot(aes(x = Cat.Variant %>% fct_rev(), y = n, 
             fill = factor(success, levels = c(0, 1), labels = c('No', 'Yes')))) +
  geom_col(position = 'stack') +
  labs(y = 'Number of predictors',
       x = 'Variant',
       fill = '|t-stat| > 1.96') +
  scale_fill_manual(values = c(rep(c("gray75", "gray45")))) +
  guides(fill = guide_legend(reverse = TRUE)) +
  coord_flip() +
  geom_text(data = labelData,
            aes(label = rate, fill = NA),
            nudge_y = 5) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'figX_reprate_VariantsClear.png'), width = 10, height = 8)



# Replication rates by predictor category (incl variants)
labelData = df %>% 
  filter(Cat.Predictor != '9_drop') %>%
  filter(Cat.Variant == '1_original' | (Cat.Variant != '1_original' & Cat.Predictor == '1_clear')) %>% 
  mutate(Cat.Predictor = ifelse(Cat.Variant != '1_original', 'Variant', Cat.Predictor)) %>% 
  group_by(Cat.Predictor) %>%
  summarise(rate = mean(success),
            n = n()) %>% 
  mutate(rate = paste(round(100*rate, 0) %>% as.character(), '%')) %>% 
  ungroup()

df %>%
  filter(Cat.Predictor != '9_drop') %>%
  filter(Cat.Variant == '1_original' | (Cat.Variant != '1_original' & Cat.Predictor == '1_clear')) %>% 
  mutate(Cat.Predictor = ifelse(Cat.Variant != '1_original', 'Variant', Cat.Predictor)) %>% 
  group_by(Cat.Predictor, success) %>%
  count() %>% 
  ggplot(aes(x = Cat.Predictor %>% 
               factor(levels = c('Variant', '4_not', '3_maybe', '2_likely', '1_clear'),
                      labels = c('variant', 'not', 'maybe', 'likely', 'clear')), y = n, 
             fill = factor(success, levels = c(0, 1), labels = c('No', 'Yes')))) +
  geom_col(position = 'stack') +
  labs(y = 'Number of predictors',
       x = 'Predictor Category',
       fill = '|t-stat| > 1.96') +
  scale_fill_manual(values = c(rep(c("gray75", "gray45")))) +
  guides(fill = guide_legend(reverse = TRUE)) +
  coord_flip() +
  geom_text(data = labelData,
            aes(label = rate, fill = NA),
            nudge_y = 8) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'figX_reprate_inclVariantsClear.png'), width = 10, height = 8)



# Figure: Holding periods -------------------------------------------------

## import summary stats
df = read_xlsx(paste0(pathSummary, 'SignalSummaryHoldPer.xlsx')) %>% 
  filter(Cat.Predictor == '1_clear', Cat.Variant == '1_original')

## plot densities
p1 = df %>% mutate(holdper = factor(holdper, levels = c(1, 3, 6, 12), 
                                    labels = c('1 month', '3 months', '6 months', '12 months'))) %>% 
  ggplot(aes(x = abs(ret), 
             color = holdper, group = holdper, fill = holdper)) + 
  geom_density(alpha = .3, adjust = 1.1) +
  scale_color_discrete(guide = FALSE) + 
  labs(x = 'Mean Return In-Sample (% per month)',
       y = 'Density',
       fill = 'Rebalancing frequency') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)


p2 = df %>% mutate(holdper = factor(holdper, levels = c(1, 3, 6, 12), 
                                    labels = c('1 month', '3 months', '6 months', '12 months'))) %>% 
  ggplot(aes(x = abs(tstat), 
             color = holdper, group = holdper, fill = holdper)) + 
  geom_density(alpha = .3, adjust = 1.1) +
  scale_color_discrete(guide = FALSE) + 
  labs(x = 't-stat In-Sample',
       y = 'Density',
       fill = 'Rebalancing frequency') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggpubr::ggarrange(p1, p2, common.legend = TRUE)

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_dist.png'), width = 12, height = 8)


# Plot means as bars
df %>% 
  mutate(holdper = factor(holdper, levels = c(1, 3, 6, 12), 
                          labels = c('1 month', '3 months', '6 months', '12 months'))) %>%
  group_by(holdper) %>% 
  summarise(`Mean Return` = mean(abs(ret)),
            `t-statistic` = mean(abs(tstat))) %>% 
  gather(key = 'key', value = 'value', -holdper) %>% 
  ggplot(aes(x = holdper, y = value)) +
  geom_col() +
  facet_wrap(~key, scales = 'free_y') +
  labs(x = 'Rebalancing frequency', y = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_means.png'), width = 12, height = 8)


# Boxplots
df %>% 
  mutate(holdper = factor(holdper, levels = c(1, 3, 6, 12), 
                          labels = c('1 month', '3 months', '6 months', '12 months'))) %>%
  transmute(holdper,
            Return = abs(ret),
            `t-statistic` = abs(tstat)) %>% 
  gather(key = 'key', value = 'value', -holdper) %>% 
  ggplot(aes(x = holdper, y = value)) +
  geom_boxplot(outlier.shape = NA) +
  labs(x = 'Rebalancing frequency', y = '') +
  facet_wrap(~key, scales = 'free_y') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_boxplot.png'), width = 12, height = 8)

# Boxplots (mean ret only)
df %>% 
  mutate(holdper = factor(holdper, levels = c(1, 3, 6, 12), 
                          labels = c('1 month', '3 months', '6 months', '12 months'))) %>%
  transmute(holdper,
            Return = abs(ret)) %>% 
  gather(key = 'key', value = 'value', -holdper) %>% 
  ggplot(aes(x = holdper, y = value)) +
  geom_boxplot(outlier.shape = NA) +
  labs(x = 'Rebalancing frequency', y = 'Mean Return (ppt per month)') +
  coord_cartesian(ylim = c(0, 1.7)) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_boxplot_mean.png'), width = 12, height = 8)

# Jitter and boxplots
df %>% 
  mutate(holdper = factor(holdper, levels = c(1, 3, 6, 12), 
                          labels = c('1 month', '3 months', '6 months', '12 months'))) %>%
  transmute(holdper,
            Return = abs(ret)) %>% 
  gather(key = 'key', value = 'value', -holdper) %>% 
  ggplot(aes(x = holdper, y = value)) +
  geom_jitter(width = .2, height = 0) +
  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(x = 'Rebalancing frequency', y = 'Mean Return (ppt per month)') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_boxplot_meanJitter.png'), width = 12, height = 8)


# Figure: Liquidity screens -----------------------------------------------

## import summary stats
df = read_xlsx(paste0(pathSummary, 'SignalSummaryLiqScreens.xlsx')) %>% 
  filter(Cat.Predictor == '1_clear', Cat.Variant == '1_original')

## plot densities
p1 = df %>% mutate(screen = factor(screen, levels = c('none', 'me', 'nyse', 'price'), 
                                   labels = c('None', 'Market Equity', 'NYSE', 'Price'))) %>% 
  ggplot(aes(x = abs(ret), 
             color = screen, group = screen, fill = screen)) + 
  geom_density(alpha = .3, adjust = 1.1) +
  scale_color_discrete(guide = FALSE) + 
  labs(x = 'Mean Return In-Sample (% per month)',
       y = 'Density',
       fill = 'Liquidity screen') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)


p2 = df %>% mutate(screen = factor(screen, levels = c('none', 'me', 'nyse', 'price'), 
                                   labels = c('None', 'Market Equity', 'NYSE', 'Price'))) %>% 
  ggplot(aes(x = abs(tstat), 
             color = screen, group = screen, fill = screen)) + 
  geom_density(alpha = .3, adjust = 1.1) +
  scale_color_discrete(guide = FALSE) + 
  labs(x = 't-stat In-Sample',
       y = 'Density',
       fill = 'Holding period') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggpubr::ggarrange(p1, p2, common.legend = TRUE)

# Save
ggsave(filename = paste0(pathResults, 'fig4_liquidity_dist.png'), width = 12, height = 8)


# Plot means as bars
df %>% 
  mutate(screen = factor(screen, levels = c('none', 'me', 'nyse', 'price'), 
                         labels = c('None', 'Market Equity', 'NYSE', 'Price'))) %>% 
  group_by(screen) %>% 
  summarise(`Mean Return` = mean(abs(ret)),
            `t-statistic` = mean(abs(tstat))) %>% 
  gather(key = 'key', value = 'value', -screen) %>% 
  ggplot(aes(x = screen, y = value)) +
  geom_col() +
  facet_wrap(~key, scales = 'free_y') +
  labs(x = 'Liquidity screen', y = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_liquidity_mean.png'), width = 12, height = 8)


# Boxplots
df %>% 
  mutate(screen = factor(screen, levels = c('none', 'me', 'nyse', 'price'), 
                         labels = c('None', 'Market Equity', 'NYSE', 'Price'))) %>% 
  transmute(screen,
            Return = abs(ret),
            `t-statistic` = abs(tstat)) %>% 
  gather(key = 'key', value = 'value', -screen) %>% 
  ggplot(aes(x = screen, y = value)) +
  geom_boxplot(outlier.shape = NA) +
  labs(x = 'Liquidity screen', y = '') +
  facet_wrap(~key, scales = 'free_y') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_liquidity_boxplot.png'), width = 12, height = 8)


# Boxplots (mean ret only)
df %>% 
  mutate(screen = factor(screen, levels = c('none', 'me', 'nyse', 'price'), 
                         labels = c('None', 'Market Equity', 'NYSE', 'Price')))  %>%
  transmute(screen,
            Return = abs(ret)) %>% 
  gather(key = 'key', value = 'value', -screen) %>% 
  ggplot(aes(x = screen, y = value)) +
  geom_boxplot(outlier.shape = NA) +
  labs(x = 'Liquity screen', y = 'Mean Return (ppt per month)') +
  coord_cartesian(ylim = c(0, 1.5)) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_liquidity_boxplot_mean.png'), width = 12, height = 8)

# Jitter and boxplots
df %>% 
  mutate(screen = factor(screen, levels = c('none', 'me', 'nyse', 'price'), 
                         labels = c('None', 'Market Equity', 'NYSE', 'Price')))  %>%
  transmute(screen,
            Return = abs(ret)) %>% 
  gather(key = 'key', value = 'value', -screen) %>% 
  ggplot(aes(x = screen, y = value)) +
  geom_jitter(width = .2, height = 0) +
  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(x = 'Liquity screen', y = 'Mean Return (ppt per month)') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

# Save
ggsave(filename = paste0(pathResults, 'fig4_liquidity_boxplot_meanJitter.png'), width = 12, height = 8)


# Big summary table for paper ---------------------------------------------

basicInfo = read_xlsx(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet ='BasicInfo'
) %>% 
  filter(Cat.Predictor != '9_drop')

constructionInfo = read_xlsx(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet ='Construction'
) %>% 
  select(Acronym, SampleStartYear, SampleEndYear)

stats =  read_xlsx(
  path = paste0(pathSummary, 'SignalSummaryBase.xlsx')
) 


# Merge data
df_merge = basicInfo %>% 
  left_join(constructionInfo) %>% 
  left_join(stats %>% 
              select(signalname, tstat, ret),
            by = c('Acronym' = 'signalname')) %>% 
  transmute(Authors, 
            Year = as.integer(Year), 
            Predictor = LongDescription, 
            `Sample Start` = as.integer(SampleStartYear), 
            `Sample End` = as.integer(SampleEndYear),
            `Mean Return` = round(ret, digits = 2),
            `t-stat` = round(tstat, digits = 2),
            Category = Cat.Predictor %>% 
              factor(levels = c('4_not', '3_maybe', '2_likely', '1_clear'),
                     labels = c('not', 'maybe', 'likely', 'clear')),
            Variant = Cat.Variant %>% 
              factor(levels = c('1_original', '2_lag', '2_quarterly', '2_risk_model'),
                     labels = c('Original', 'Lag structure', 'Quarterly', 'Risk Model'))) %>% 
  arrange(Authors, Year)


# Create Latex output table 1: Clear predictors
outputtable1 = xtable(df_merge %>% 
                        filter(Category == 'clear', Variant == 'Original') %>% 
                        select(-Category, -Variant)
)


print(outputtable1, 
      include.rownames = FALSE,
      include.colnames = FALSE,
      hline.after = NULL,
      only.contents = TRUE,
      file = paste0(pathResults, "bigSignalTableClear.tex")
)

# Create Latex output table 1: Likely predictors
outputtable1 = xtable(df_merge %>% 
                        filter(Category == 'likely', Variant == 'Original') %>% 
                        select(-Category, -Variant)
)


print(outputtable1, 
      include.rownames = FALSE,
      include.colnames = FALSE,
      hline.after = NULL,
      only.contents = TRUE,
      file = paste0(pathResults, "bigSignalTableLikely.tex")
)


# Create Latex output table 2: Extended dataset
outputtable2 = xtable(df_merge %>% 
                        filter(Variant == 'Original' & Category != 'clear' & Category != 'likely') %>% 
                        arrange(desc(Category), Authors, Year) %>% 
                        select(-Variant)
)


print(outputtable2, 
      include.rownames = FALSE,
      include.colnames = FALSE,
      hline.after = NULL,
      only.contents = TRUE,
      file = paste0(pathResults, "bigSignalTableExtended.tex")
)



# Big description table for appendix ------------------------------------------

basicInfo = read_xlsx(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
  , sheet ='BasicInfo'
) %>% 
  filter(Cat.Predictor != '9_drop')

constructionInfo = read_xlsx(
  path = paste0(pathSummary, 'SignalDocumentation.xlsx')
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

