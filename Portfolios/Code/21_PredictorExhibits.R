## Exhibits for paper

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

tryCatch(        
    source('00_SettingsAndFunctions.R', echo=TRUE)
  , error = function(cond){
      message('Error: 00_SettingsAndFunctions.R not found.  please setwd to pathProject/Portfolios/Code/')          
  }
)
    
# check system for dl method
dlmethod = 'auto'
sysinfo = Sys.info()
if (sysinfo[1] == "Linux") {
    dlmethod = 'wget'
}


# Figure 1 (Port): Correlations (Portfolio level) -------------------------

## import baseline returns
# 2021 01 ac: now portbase is only clear / likely original 
retwide = fread(paste0(pathDataPortfolios, 'PredictorLSretWide.csv')) %>% 
    as_tibble() %>% 
    mutate(
        date = as.Date(
            paste0(substr(date,1,8), '28')
        )
    )

## Import factor returns

# FF 5 factors
download.file(    'http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip'
            , destfile = paste0(pathDataIntermediate, 'temp.zip')
            , method = dlmethod
              )
setwd(pathDataIntermediate)
unzip('temp.zip')
setwd(pathCode)

# Momentum (FF style)
download.file(    'https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip'
            , destfile = paste0(pathDataIntermediate, 'temp.zip')
            , method = dlmethod
              )
setwd(pathDataIntermediate)
unzip('temp.zip')
setwd(pathCode)

# join
tempa = read_csv(
    paste0(pathDataIntermediate, 'F-F_Research_Data_5_Factors_2x3.CSV')
  , skip = 3) %>% 
    mutate(date = as.Date(paste0(as.character(X1), '28'), format='%Y%m%d') %>% 
               ymd()) %>% 
    filter(!is.na(date)) %>% 
    mutate_at(.vars = vars(SMB, HML, RMW, CMA),
              .funs = list(as.numeric)) %>%
    select(-X1)

tempb = read_csv(
    paste0(pathDataIntermediate, 'F-F_Momentum_Factor.CSV')
  , skip = 13) %>% 
    mutate(date = as.Date(paste0(as.character(X1), '28'), format='%Y%m%d') %>% 
               ymd()) %>% 
    filter(!is.na(date)) %>% 
    mutate_at(.vars = vars(Mom),
              .funs = list(as.numeric)) %>%
    select(-X1)

ff = full_join(tempa, tempb, by = 'date') %>%
    transmute(date, SMB, HML, RMW, CMA, Mom)

# Fig 1a: Pairwise correlation of strategy returns
temp = cor(retwide %>% select(-date), 
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
tempRets = retwide %>% 
  inner_join(ff %>% 
               select(date, SMB))

temp = cor(tempRets %>% select(-date, -SMB),
           tempRets %>% select(SMB),
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
tempRets = retwide %>% 
  inner_join(ff %>% 
               select(date, HML))

temp = cor(tempRets %>% select(-date, -HML),
           tempRets %>% select(HML),
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

# Fig 1d: Correlation with Mom
# should be same as UMD
tempRets = retwide %>% 
  inner_join(ff %>% 
               select(date, Mom))

temp = cor(tempRets %>% select(-date, -Mom),
           tempRets %>% select(Mom),
           use = 'pairwise.complete.obs')

tibble(rho = temp) %>% 
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) + 
  coord_cartesian(xlim = c(-1,1)) +
  labs(x = 'Pairwise correlation coefficient',
       y = 'Count') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, 'fig1dPort_correlationMom.png'), width = 10, height = 8)

allRhos = rbind(allRhos,
                tibble(rho = temp, series = 'Momentum'))

# Fig 1e: Correlation with OP
tempRets = retwide %>% 
  inner_join(ff %>% 
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
tempRets = retwide %>% 
  inner_join(ff %>% 
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

df = read_xlsx(paste0(pathDataPortfolios, 'PredictorSummary.xlsx')) %>% 
  mutate(success = 1*(round(tstat, digits = 2) >=1.96))

df_meta = read_xlsx(
  path = paste0(pathProject, 'SignalDocumentation.xlsx')
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


# Replication success by data category (for baseline ones)
labelData = df %>% 
  filter(Cat.Signal == 'Predictor') %>% 
  group_by(Cat.Data) %>%
  summarise(rate = mean(success),
            n = n()) %>% 
  mutate(rate = paste(round(100*rate, 0) %>% as.character(), '%')) %>% 
  ungroup()

df %>%
  filter(Cat.Signal == 'Predictor') %>% 
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
  filter(Cat.Signal == 'Predictor') %>% 
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





# Big summary table for paper ---------------------------------------------

basicInfo = read_xlsx(
  path = paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet ='BasicInfo'
) %>% 
  filter(Cat.Signal != 'Drop')

stats =  read_xlsx(
    path = paste0(pathDataPortfolios, 'PredictorSummary.xlsx')
) 


# Merge data
# alldocumentation is created in 00_SettingsAndFunctions.R
df_merge = alldocumentation %>% 
  left_join(stats %>% 
              select(signalname, tstat, rbar),
            by = c('signalname')) %>% 
  transmute(Authors, 
            Year = as.integer(Year), 
            Predictor = LongDescription, 
            `Sample Start` = as.integer(SampleStartYear), 
            `Sample End` = as.integer(SampleEndYear),
            `Mean Return` = round(rbar, digits = 2),
            `t-stat` = round(tstat, digits = 2),
            Cat.Signal,
            Category = `Predictability in OP` %>% 
              factor(
                  levels = c('no_evidence','4_not', '3_maybe', '2_likely', '1_clear'),

                  labels = c('no evidence','not', 'maybe', 'likely', 'clear'))            
            ) %>% 
  arrange(Authors, Year)

        


# Create Latex output table 1: Clear predictors
outputtable1 = xtable(df_merge %>% 
                        filter(Category == 'clear', Cat.Signal == 'Predictor') %>% 
                        select(-Category, -Cat.Signal)
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
                        filter(Category == 'likely', Cat.Signal == 'Predictor') %>% 
                        select(-Category, -Cat.Signal)
)


print(outputtable1, 
      include.rownames = FALSE,
      include.colnames = FALSE,
      hline.after = NULL,
      only.contents = TRUE,
      file = paste0(pathResults, "bigSignalTableLikely.tex")
)



