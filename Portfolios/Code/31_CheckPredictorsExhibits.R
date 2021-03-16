### LOAD PORT-MONTH RETURNS AND SUMMARIZE ----

## summarize alt holding period 
holdperlist = as.character(c(1,3,6,12))

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

# add baseline
tempport = read.csv(paste0(pathDataPortfolios,'PredictorPortsFull.csv')) %>%
    filter(port == 'LS') 

tempsum = sumportmonth(tempport, c('signalname','samptype','port'), Nstocksmin = 20)  %>%
    as_tibble() %>%
    mutate(portperiod = 'base') %>%
    filter(samptype == 'insamp')

sumholdper = rbind(sumholdper,tempsum)

## summarize alt liq screens
csvlist = c(
     'CheckPredictorLS_LiqScreen_ME_gt_NYSE20pct.csv'
    , 'CheckPredictorLS_LiqScreen_NYSEonly.csv'
    , 'CheckPredictorLS_LiqScreen_Price_gt_5.csv'
    , 'CheckPredictorLS_LiqScreen_VWforce.csv'
)
screenlist = c('me','nyse','price','vwforce')
 
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
portDeciles = read.csv(paste0(pathDataPortfolios, 'CheckPredictorPorts_Deciles.csv')) 

sumDeciles =   sumportmonth(portDeciles, c('signalname','samptype','port')
                         , Nstocksmin = 20)   %>%
  as_tibble() 


# Figures: Monotonicity  -------------------------------------------------

sumDeciles %>% 
  filter(port != 'LS', samptype == 'insamp', Nlong > 100) %>% 
  group_by(signalname) %>% 
  mutate(
      Increase = ifelse(port != '01' & rbar >= lag(rbar, n =1), 'Increase', 'No increase')
  ) %>% 
  ungroup() %>% 
  ggplot(aes(x = port, y = rbar, shape = factor(Increase, levels = c('Increase', 'No increase')))) +
  geom_jitter(width = .2, height = 0, size = 2.3) +
  scale_shape_manual(values = c(19, 2)) +
  geom_boxplot(aes(x = port, y = rbar), inherit.aes = FALSE, alpha = 0, outlier.shape = NA, coef = 0) +
  labs(x = 'Decile Portfolio', y = 'Mean Return (% monthly, in-sample)', shape = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = c(.2, .8)) 
    

# Save
ggsave(filename = paste0(pathResults, 'fig_mono.png'), width = 12, height = 8)


# Figures: Holding periods -------------------------------------------------

df = sumholdper
xlevels = c('base','1','3','6','12')
xlabels = c('Original Papers','1 month', '3 months', '6 months', '12 months')

# Jitter and boxplots
df %>% 
  mutate(portperiod = factor(portperiod, levels = xlevels, labels = xlabels)) %>%
  transmute(portperiod,
            Return = rbar) %>% 
  gather(key = 'key', value = 'value', -portperiod) %>% 
  ggplot(aes(x = portperiod, y = value)) +
  geom_jitter(width = .2, height = 0) +
  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(x = 'Rebalancing frequency', y = 'Mean Return (% monthly, in-sample)') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
    ylim(-0.5,2)

# Save
ggsave(filename = paste0(pathResults, 'fig4_holding_period_boxplot_meanJitter.png'), width = 12, height = 8)


# Figures: Liquidity screens -----------------------------------------------

df = sumliqscreen

xlevels = c('none', 'price', 'nyse', 'me','vwforce')
xlabels = c('Original Papers', 'Price>5', 'NYSE only', 'ME > NYSE 20 pct','VW force')


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
  labs(x = 'Liquity screen', y = 'Mean Return (% monthly, in-sample)') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
    ylim(-0.5,2)

# Save
ggsave(filename = paste0(pathResults, 'fig4_liquidity_boxplot_meanJitter.png'), width = 12, height = 8)


# Figures: Deciles --------------------------------------------------------

sumDeciles %>% 
  filter(port != 'LS', samptype == 'insamp', rbar < 10) %>% 
  ggplot(aes(x = port, y = rbar)) +
  geom_jitter(width = .2, height = 0) +
  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(x = 'Decile Portfolio', y = 'Mean Return in-sample (ppt per month)') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

# Save
ggsave(filename = paste0(pathResults, 'fig_Decile_boxplot_meanJitter.png'), width = 12, height = 8)


