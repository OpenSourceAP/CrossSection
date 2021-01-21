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

source('setup_crspm.r')

# pathDataPortfolios = '/cm/chen/anomalies.com/cfr1/Portfolios/Data/Portfolios - Copy/'

### LOAD PORT-MONTH RETURNS AND SUMMARIZE

## summarize alt holding period 
csvlist = c(
    'CheckPredictorLS_HoldPer_1.csv'
    , 'CheckPredictorLS_HoldPer_3.csv'
    , 'CheckPredictorLS_HoldPer_6.csv'
    , 'CheckPredictorLS_HoldPer_12.csv'    
)

holdperlist = c(1,3,6,12)

sumholdper = tibble()
for (i in seq(1,length(holdperlist))){

    tempport = read.csv(paste0(pathDataPortfolios,csvlist[i])) %>%
        select(signalname,date,ret,Nstocks)

    tempsum = sumportmonth(tempport, c('signalname','samptype'), Nstocksmin = 20)  %>%
        as_tibble() %>%
        mutate(holdper = holdperlist[i]) %>%
        filter(samptype == 'insamp')
    
    sumholdper = rbind(sumholdper,tempsum)
}


## summarize alt liq screens
csvlist = c(
     'CheckPredictorLS_LiqScreen_ME_gt_NYSE20pct.csv'
    , 'CheckPredictorLS_LiqScreen_NYSEonly.csv'
    , 'CheckPredictorLS_LiqScreen_Price_gt_5.csv'
)
screenlist = c('me','nyse','price')
 
sumliqscreen = tibble()
for (i in seq(1,length(csvlist))){

    tempport = read.csv(paste0(pathDataPortfolios,csvlist[i])) %>%
        select(signalname,date,ret,Nstocks)

    tempsum = sumportmonth(tempport, c('signalname','samptype'), Nstocksmin = 20)  %>%
        as_tibble() %>%
        mutate(screen = screenlist[i]) %>%
        filter(samptype == 'insamp')
    
    sumliqscreen = rbind(sumliqscreen,tempsum)
}

# add baseline
tempport = read.csv(paste0(pathDataPortfolios,'PredictorPortsFull.csv')) %>%
    filter(port == 'LS') %>%
    select(signalname,date,ret,Nstocks)
tempsum = sumportmonth(tempport, c('signalname','samptype'), Nstocksmin = 20)  %>%
    as_tibble() %>%
    mutate(screen = 'none') %>%
    filter(samptype == 'insamp')
sumliqscreen = rbind(sumliqscreen,tempsum)

### MAKE FIGURES FOR HOLDING PERIODS

# Figure: Holding periods -------------------------------------------------

df = sumholdper

## plot densities
p1 = df %>% mutate(holdper = factor(holdper, levels = c(1, 3, 6, 12), 
                                    labels = c('1 month', '3 months', '6 months', '12 months'))) %>% 
  ggplot(aes(x = rbar, 
             color = holdper, group = holdper, fill = holdper)) + 
  geom_density(alpha = .3, adjust = 1.1) +
  scale_color_discrete(guide = FALSE) + 
  labs(x = 'Mean Return In-Sample (% per month)',
       y = 'Density',
       fill = 'Rebalancing frequency') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)


p2 = df %>% mutate(holdper = factor(holdper, levels = c(1, 3, 6, 12), 
                                    labels = c('1 month', '3 months', '6 months', '12 months'))) %>% 
  ggplot(aes(x = tstat, 
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
  summarise(`Mean Return` = mean(rbar),
            `t-statistic` = mean(tstat)) %>% 
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
            Return = rbar,
            `t-statistic` = tstat) %>% 
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
            Return = rbar) %>% 
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
            Return = rbar) %>% 
  gather(key = 'key', value = 'value', -holdper) %>% 
  ggplot(aes(x = holdper, y = value)) +
  geom_jitter(width = .2, height = 0) +
  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(x = 'Rebalancing frequency', y = 'Mean Return (ppt per month)') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_boxplot_meanJitter.png'), width = 12, height = 8)

### MAKE FIGURES FOR LIQUIDITY SCREENS

# Figure: Liquidity screens -----------------------------------------------

df = sumliqscreen

xlevels = c('none', 'price', 'nyse', 'me')
xlabels = c('None', 'Price>5', 'NYSE only', 'ME > NYSE 20 pct')

## plot densities
p1 = df %>% mutate(screen = factor(screen, levels = xlevels, 
                                   labels = xlabels)) %>% 
  ggplot(aes(x = rbar, 
             color = screen, group = screen, fill = screen)) + 
  geom_density(alpha = .3, adjust = 1.1) +
  scale_color_discrete(guide = FALSE) + 
  labs(x = 'Mean Return In-Sample (% per month)',
       y = 'Density',
       fill = 'Liquidity screen') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)


p2 = df %>% mutate(screen = factor(screen, levels = xlevels, 
                                   labels = xlabels)) %>% 
  ggplot(aes(x = tstat, 
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
  mutate(screen = factor(screen, levels = xlevels, 
                         labels = xlabels)) %>% 
  group_by(screen) %>% 
  summarise(`Mean Return` = mean(rbar),
            `t-statistic` = mean(tstat)) %>% 
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
  mutate(screen = factor(screen, levels = xlevels, 
                         labels = xlabels)) %>% 
  transmute(screen,
            Return = rbar,
            `t-statistic` = tstat) %>% 
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
  mutate(screen = factor(screen, levels = xlevels, 
                         labels = xlabels))  %>%
  transmute(screen,
            Return = rbar) %>% 
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
  mutate(screen = factor(screen, levels = xlevels, 
                         labels = xlabels))  %>%
  transmute(screen,
            Return = rbar) %>% 
  gather(key = 'key', value = 'value', -screen) %>% 
  ggplot(aes(x = screen, y = value)) +
  geom_jitter(width = .2, height = 0) +
  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(x = 'Liquity screen', y = 'Mean Return (ppt per month)') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

# Save
ggsave(filename = paste0(pathResults, 'fig4_liquidity_boxplot_meanJitter.png'), width = 12, height = 8)



