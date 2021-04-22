### LOAD PORT-MONTH RETURNS AND SUMMARIZE ----

## summarize alt holding period 
holdperlist = as.character(c(1,3,6,12))

sumholdper = tibble()
for (i in seq(1,length(holdperlist))){

    tempport = read.csv(paste0(pathDataPortfolios,'PredictorAltPorts_HoldPer_', holdperlist[i], '.csv')) %>%
        filter(port == 'LS')

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
     'PredictorAltPorts_LiqScreen_ME_gt_NYSE20pct.csv'
    , 'PredictorAltPorts_LiqScreen_NYSEonly.csv'
    , 'PredictorAltPorts_LiqScreen_Price_gt_5.csv'
    , 'PredictorAltPorts_LiqScreen_VWforce.csv'
)
screenlist = c('me','nyse','price','vwforce')
 
sumliqscreen = tibble()
for (i in seq(1,length(csvlist))){

    tempport = read.csv(paste0(pathDataPortfolios,csvlist[i])) %>%  
        filter(port == 'LS')

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
portDeciles = read.csv(paste0(pathDataPortfolios, 'PredictorAltPorts_Deciles.csv')) 

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

df = sumholdper %>% filter(port == 'LS')
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
  labs(x = 'Liquidity screen', y = 'Mean Return (% monthly, in-sample)') +
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


#### CHECK VW FOR QUINT AND DEC ####
# not used in paper, but good to check
all = rbind(
  read.csv(paste0(pathDataPortfolios,'PredictorAltPorts_Deciles.csv')) %>%
    mutate(q_cut = 0.1, sweight = 'EW')
  , read.csv(paste0(pathDataPortfolios,'PredictorAltPorts_DecilesVW.csv')) %>%
    mutate(q_cut = 0.1, sweight = 'VW')
  , read.csv(paste0(pathDataPortfolios,'PredictorAltPorts_Quintiles.csv')) %>%
    mutate(q_cut = 0.2, sweight = 'EW')
  , read.csv(paste0(pathDataPortfolios,'PredictorAltPorts_QuintilesVW.csv')) %>%
    mutate(q_cut = 0.2, sweight = 'VW')
)

sumall = sumportmonth(all,c('samptype','signalname','q_cut','sweight','port'))

sumimp = sumall %>% 
  filter(port != 'LS', samptype == 'insamp') %>%
  group_by(q_cut,sweight,port) %>%
  summarize(rbar = mean(rbar))

p1 = ggplot(
  sumimp %>% filter(q_cut == 0.1)
  , aes(x=port, y=rbar, group = sweight)
) +
  geom_line(aes(color=sweight)) +
  geom_point(aes(color=sweight)) +
  theme_minimal() +
  labs(title = 'Simple Check on Forced Quantile Implementations')

p2 = ggplot(
  sumimp %>% filter(q_cut == 0.2)
  , aes(x=port, y=rbar, group = sweight)
) +
  geom_line(aes(color=sweight)) +
  geom_point(aes(color=sweight)) +
  theme_minimal()

pboth = grid.arrange(p1,p2,nrow=2)

# Save
ggsave(filename = paste0(pathResults, 'xfig_altquant_check.png'), plot=pboth, width = 12, height = 8)

