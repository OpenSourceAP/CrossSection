### ENVIRONMENT ###
rm(list = ls())
options(stringsAsFactors = FALSE)
options(scipen = 999)
optFontsize <- 20 # Fix fontsize for graphs here
optFontFamily = 'Palatino Linotype' # doesn't agree with linux command line
#optFontFamily <- "" # works with linux command line
library(extrafont)
loadfonts()

library(tidyverse)
library(readxl)
library(lubridate)
library(xtable)
options(xtable.floating = FALSE)

pathProject = getwd()

tryCatch(
  source(paste0(pathProject, '/Portfolios/Code/00_SettingsAndTools.R')),
  error = function(cond) {
    message("Error: 00_SettingsAndTools.R not found.  please setwd to pathProject/Portfolios/Code/")
  }
)

# check system for dl method
dlmethod <- "auto"
sysinfo <- Sys.info()
if (sysinfo[1] == "Linux") {
  dlmethod <- "wget"
}


### LOAD PORT-MONTH RETURNS AND SUMMARIZE ----

## summarize alt holding period 
holdperlist = c(1,3,6,12)

sumholdper = tibble()
for (i in seq(1,length(holdperlist))){

    tempport = read.csv(paste0(pathDataPortfolios,'CheckPredictorLS_HoldPer_', holdperlist[i], '.csv')) %>%
        mutate(port = 'LS', signallag = NA_real_)

    tempsum =   sumportmonth(tempport, c('signalname','samptype','port')
                           , Nstocksmin = 20)   %>%
        as_tibble() %>%
        mutate(portperiod = holdperlist[i]) %>%
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
        mutate(port = 'LS', signallag = NA_real_)

    tempsum =   sumportmonth(tempport, c('signalname','samptype','port')
                           , Nstocksmin = 20)   %>%
        as_tibble() %>%
        mutate(screen = screenlist[i]) %>%
        filter(samptype == 'insamp')
    
    sumliqscreen = rbind(sumliqscreen,tempsum)
}

# add baseline
tempport = read.csv(paste0(pathDataPortfolios,'PredictorPortsFull.csv')) %>%
    filter(port == 'LS') 

tempsum = sumportmonth(tempport, c('signalname','samptype','port'), Nstocksmin = 20)  %>%
    as_tibble() %>%
    mutate(screen = 'none') %>%
    filter(samptype == 'insamp')

sumliqscreen = rbind(sumliqscreen,tempsum)

## Summarize decile sorts
portDeciles   = read.csv(paste0(pathDataPortfolios, 'CheckPredictorPorts_Deciles.csv')) 

sumDeciles = sumportmonth(portDeciles, c('signalname','samptype','port')
                         , Nstocksmin = 20)   %>%
  as_tibble() 



# Figures: Holding periods -------------------------------------------------

df = sumholdper

## plot densities
p1 = df %>% mutate(portperiod = factor(portperiod, levels = c(1, 3, 6, 12), 
                                    labels = c('1 month', '3 months', '6 months', '12 months'))) %>% 
  ggplot(aes(x = rbar, 
             color = portperiod, group = portperiod, fill = portperiod)) + 
  geom_density(alpha = .3, adjust = 1.1) +
  scale_color_discrete(guide = FALSE) + 
  labs(x = 'Mean Return In-Sample (% per month)',
       y = 'Density',
       fill = 'Rebalancing frequency') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)


p2 = df %>% mutate(portperiod = factor(portperiod, levels = c(1, 3, 6, 12), 
                                    labels = c('1 month', '3 months', '6 months', '12 months'))) %>% 
  ggplot(aes(x = tstat, 
             color = portperiod, group = portperiod, fill = portperiod)) + 
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
  mutate(portperiod = factor(portperiod, levels = c(1, 3, 6, 12), 
                          labels = c('1 month', '3 months', '6 months', '12 months'))) %>%
  group_by(portperiod) %>% 
  summarise(`Mean Return` = mean(rbar),
            `t-statistic` = mean(tstat)) %>% 
  gather(key = 'key', value = 'value', -portperiod) %>% 
  ggplot(aes(x = portperiod, y = value)) +
  geom_col() +
  facet_wrap(~key, scales = 'free_y') +
  labs(x = 'Rebalancing frequency', y = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_means.png'), width = 12, height = 8)


# Boxplots
df %>% 
  mutate(portperiod = factor(portperiod, levels = c(1, 3, 6, 12), 
                          labels = c('1 month', '3 months', '6 months', '12 months'))) %>%
  transmute(portperiod,
            Return = rbar,
            `t-statistic` = tstat) %>% 
  gather(key = 'key', value = 'value', -portperiod) %>% 
  ggplot(aes(x = portperiod, y = value)) +
  geom_boxplot(outlier.shape = NA) +
  labs(x = 'Rebalancing frequency', y = '') +
  facet_wrap(~key, scales = 'free_y') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_boxplot.png'), width = 12, height = 8)

# Boxplots (mean ret only)
df %>% 
  mutate(portperiod = factor(portperiod, levels = c(1, 3, 6, 12), 
                          labels = c('1 month', '3 months', '6 months', '12 months'))) %>%
  transmute(portperiod,
            Return = rbar) %>% 
  gather(key = 'key', value = 'value', -portperiod) %>% 
  ggplot(aes(x = portperiod, y = value)) +
  geom_boxplot(outlier.shape = NA) +
  labs(x = 'Rebalancing frequency', y = 'Mean Return (ppt per month)') +
  coord_cartesian(ylim = c(0, 1.7)) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_boxplot_mean.png'), width = 12, height = 8)

# Jitter and boxplots
df %>% 
  mutate(portperiod = factor(portperiod, levels = c(1, 3, 6, 12), 
                          labels = c('1 month', '3 months', '6 months', '12 months'))) %>%
  transmute(portperiod,
            Return = rbar) %>% 
  gather(key = 'key', value = 'value', -portperiod) %>% 
  ggplot(aes(x = portperiod, y = value)) +
  geom_jitter(width = .2, height = 0) +
  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(x = 'Rebalancing frequency', y = 'Mean Return (ppt per month)') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_boxplot_meanJitter.png'), width = 12, height = 8)


# Figures: Liquidity screens -----------------------------------------------

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


# Figures: Deciles ----------------------------- --------------------------------------------------

sumDeciles %>% 
  filter(port != 'LS', samptype == 'insamp', Nlong > 100) %>% 
  group_by(signalname) %>% 
  mutate(Increase = ifelse(port != '01' & rbar >= lag(rbar, n =1), 'Increase', 'No increase')) %>% 
  ungroup() %>% 
  ggplot(aes(x = port, y = rbar, shape = factor(Increase, levels = c('Increase', 'No increase')))) +
  geom_jitter(width = .2, height = 0, size = 2.3) +
  scale_shape_manual(values = c(19, 2)) +
  geom_boxplot(aes(x = port, y = rbar), inherit.aes = FALSE, alpha = 0, outlier.shape = NA, coef = 0) +
  labs(x = 'Decile Portfolio', y = 'Mean Return in-sample (ppt per month)', shape = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = c(.2, .8))

# Save
ggsave(filename = paste0(pathResults, 'fig_Decile_boxplot_meanJitter.png'), width = 12, height = 8)

# not used currently
sumDeciles %>% 
  filter(port != 'LS', samptype == 'insamp', Nlong > 100) %>% 
  group_by(signalname) %>% 
  mutate(Increase = ifelse(port != '01' & rbar >= lag(rbar, n =1), 'Increase', 'No increase')) %>% 
  ungroup() %>% 
  ggplot(aes(x = port, y = rbar, shape = factor(Increase, levels = c('No increase', 'Increase')))) +
  geom_jitter(width = .2, height = 0, size = 2.3) +
  scale_shape_manual(values = c(2, 19)) +
  geom_boxplot(aes(x = port, y = rbar), inherit.aes = FALSE, alpha = 0, outlier.shape = NA, coef = 0) +
  labs(x = 'Decile Portfolio', y = 'Mean Return in-sample (ppt per month)', shape = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = c(.2, .8)) +
  geom_line(data = sumDeciles %>% 
              #  filter(port != 'LS', samptype == 'insamp', rbar < 10) %>% 
              filter(port != 'LS', samptype == 'insamp', Nlong > 100) %>% 
              group_by(signalname) %>% 
              mutate(Increase = ifelse(port != '01' & rbar >= lag(rbar, n =1), 1, 0)) %>% 
              group_by(port) %>% 
              summarise(meanIncrease = mean(Increase)) %>% 
              ungroup() %>% 
              filter(port !='01'),
            aes(x = port, y = 4*meanIncrease, group = 1), inherit.aes = FALSE, size = 1.5, color ='grey') +
  scale_y_continuous(sec.axis = sec_axis(~./4, name = "Share of increasing portfolio returns")) +
  theme(axis.text.y.right=element_text(colour='grey'),
        axis.ticks.y.right=element_line(colour='grey'),
        axis.title.y.right=element_text(colour='grey'))



