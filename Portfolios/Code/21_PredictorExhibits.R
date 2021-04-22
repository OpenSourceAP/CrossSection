## Exhibits for paper


# Import factor returns from Kenneth French's website ---------------------

# FF 5 factors
download.file("http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip",
              destfile = paste0(pathDataIntermediate, "temp.zip"),
              method = dlmethod
)

# inconvenient setwd because of a peculiarity of unzip(), see
# https://stackoverflow.com/questions/15226150/r-exdir-does-not-exist-error
temp = getwd()
setwd(pathDataIntermediate)
unzip("temp.zip") #, exdir = pathDataIntermediate)
setwd(temp)

# Momentum (FF style)
download.file("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip",
              destfile = paste0(pathDataIntermediate, "temp.zip"),
              method = dlmethod
)

setwd(pathDataIntermediate)
unzip("temp.zip")
setwd(temp)

# join
ff <- read_csv(
  paste0(pathDataIntermediate, "F-F_Research_Data_5_Factors_2x3.CSV"),
  skip = 3) %>%
  mutate(date = as.Date(paste0(as.character(X1), "28"), format = "%Y%m%d") %>%
           ymd()) %>%
  filter(!is.na(date)) %>%
  mutate_at(
    .vars = vars(SMB, HML, RMW, CMA),
    .funs = list(as.numeric)
  ) %>%
  select(-X1) %>% 
  full_join(
    read_csv(
      paste0(pathDataIntermediate, "F-F_Momentum_Factor.CSV"),
      skip = 13
    ) %>%
      mutate(date = as.Date(paste0(as.character(X1), "28"), format = "%Y%m%d") %>%
               ymd()) %>%
      filter(!is.na(date)) %>%
      mutate_at(
        .vars = vars(Mom),
        .funs = list(as.numeric)
      ) %>%
      select(-X1)
  ) %>% 
  select(date, SMB, HML, RMW, CMA, Mom) %>% 
  arrange(date)


# Figure 1 (Port): Correlations (Portfolio level) -------------------------

## import baseline returns (clear/likely)
retwide <- read_csv(paste0(pathDataPortfolios, "PredictorLSretWide.csv")) %>%
  mutate(
    date = as.Date(
      paste0(substr(date, 1, 8), "28")
    )
  )

# Fig 1a: Pairwise correlation of strategy returns
temp <- cor(retwide %>% select(-date),
  use = "pairwise.complete.obs"
)

# To avoid double counting
temp <- temp[lower.tri(temp)]


tibble(rho = temp) %>%
  ggplot(aes(x = rho)) +
  geom_histogram() +
  coord_cartesian(xlim = c(-1, 1)) +
  labs(
    x = "Pairwise correlation coefficient",
    y = "Count"
  ) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)


ggsave(filename = paste0(pathResults, "fig1aPort_pairwisecorrelations.png"), width = 10, height = 8)


allRhos <- tibble(rho = temp, series = "Pairwise")

# Fig 1b: Correlation with SMB
tempRets <- retwide %>%
  inner_join(ff %>%
    select(date, SMB))

temp <- cor(
  tempRets %>% select(-date, -SMB),
  tempRets %>% select(SMB),
  use = "pairwise.complete.obs"
)

tibble(rho = temp) %>%
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) +
  coord_cartesian(xlim = c(-1, 1)) +
  labs(
    x = "Pairwise correlation coefficient",
    y = "Count"
  ) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig1bPort_correlationSMB.png"), width = 10, height = 8)

allRhos <- rbind(
  allRhos,
  tibble(rho = temp, series = "Size")
)


# Fig 1c: Correlation with BM
tempRets <- retwide %>%
  inner_join(ff %>%
    select(date, HML))

temp <- cor(
  tempRets %>% select(-date, -HML),
  tempRets %>% select(HML),
  use = "pairwise.complete.obs"
)

tibble(rho = temp) %>%
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) +
  coord_cartesian(xlim = c(-1, 1)) +
  labs(
    x = "Pairwise correlation coefficient",
    y = "Count"
  ) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig1cPort_correlationHML.png"), width = 10, height = 8)

allRhos <- rbind(
  allRhos,
  tibble(rho = temp, series = "Value")
)

# Fig 1d: Correlation with Mom
# should be same as UMD
tempRets <- retwide %>%
  inner_join(ff %>%
    select(date, Mom))

temp <- cor(
  tempRets %>% select(-date, -Mom),
  tempRets %>% select(Mom),
  use = "pairwise.complete.obs"
)

tibble(rho = temp) %>%
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) +
  coord_cartesian(xlim = c(-1, 1)) +
  labs(
    x = "Pairwise correlation coefficient",
    y = "Count"
  ) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig1dPort_correlationMom.png"), width = 10, height = 8)

allRhos <- rbind(
  allRhos,
  tibble(rho = temp, series = "Momentum")
)

# Fig 1e: Correlation with OP
tempRets <- retwide %>%
  inner_join(ff %>%
    select(date, RMW))

temp <- cor(
  tempRets %>% select(-date, -RMW),
  tempRets %>% select(RMW),
  use = "pairwise.complete.obs"
)

tibble(rho = temp) %>%
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) +
  coord_cartesian(xlim = c(-1, 1)) +
  labs(
    x = "Pairwise correlation coefficient",
    y = "Count"
  ) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig1ePort_correlationOP.png"), width = 10, height = 8)

allRhos <- rbind(
  allRhos,
  tibble(rho = temp, series = "Profitability")
)

# Fig 1f: Correlation with Inv
tempRets <- retwide %>%
  inner_join(ff %>%
    select(date, CMA))

temp <- cor(
  tempRets %>% select(-date, -CMA),
  tempRets %>% select(CMA),
  use = "pairwise.complete.obs"
)

tibble(rho = temp) %>%
  ggplot(aes(x = rho)) +
  geom_histogram(bins = 25) +
  coord_cartesian(xlim = c(-1, 1)) +
  labs(
    x = "Pairwise correlation coefficient",
    y = "Count"
  ) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig1fPort_correlationCMA.png"), width = 10, height = 8)

allRhos <- rbind(
  allRhos,
  tibble(rho = temp, series = "Investment")
)


# Print all correlations together
allRhos %>%
  mutate(series = factor(series, levels = c("Pairwise", "Size", "Value", "Momentum", "Profitability", "Investment"))) %>%
  ggplot(aes(x = rho)) +
  geom_histogram() +
  coord_cartesian(xlim = c(-1, 1)) +
  labs(
    x = "Correlation coefficient",
    y = "Count"
  ) +
  facet_wrap(~series, scales = "free_y") +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig1Port_jointly.png"), width = 10, height = 8)

# Figure 2: Replication rates ---------------------------------------------

df0 <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                sheet = 'short') %>%
  mutate(success = 1 * (round(tstat, digits = 2) >= 1.96)) %>%
    select(signalname, tstat, success, T.Stat)

# Check if predictor summary has in-sample returns only
if (sum(df0$samptype == 'insamp') != nrow(df0)) {
  message('Mixing different sample types below!!')
}

# Use most recent Category labels and keep comparable predictors only
df_meta <- readdocumentation() %>%
    mutate(
        comparable = Cat.Signal == 'Predictor'
        & Predictability.in.OP == '1_clear'
        & Signal.Rep.Quality != '4_lack_data'
    ) %>%
    select(signalname, Cat.Data, comparable
         , Predictability.in.OP, Signal.Rep.Quality ) %>%
    mutate(
        Cat.Data = replace(Cat.Data, Cat.Data == 'Options', 'Other')
    ) 

df <- df0 %>%
    select(signalname, success, tstat) %>%
    left_join(df_meta) %>%
    filter(comparable)


# Replication success by data category (for baseline ones)
labelData <- df %>%
  group_by(Cat.Data) %>%
  summarise(
    rate = mean(success),
    n = n()
  ) %>%
  mutate(rate = paste(round(100 * rate, 0) %>% as.character(), "%")) %>%
  ungroup()

df %>%
  group_by(Cat.Data, success) %>%
  count() %>%
  ggplot(aes(
    x = Cat.Data %>% fct_rev() %>% relevel("Other"), y = n,
    fill = factor(success, levels = c(0, 1), labels = c("No", "Yes"))
  )) +
  geom_col(position = "stack") +
  labs(
    y = "Number of predictors",
    x = "Data Category",
    fill = "|t-stat| > 1.96"
  ) +
  scale_fill_manual(values = c(rep(c("gray75", "gray45")))) +
  guides(fill = guide_legend(reverse = TRUE)) +
  coord_flip() +
  geom_text(
    data = labelData,
    aes(label = rate, fill = NA),
    nudge_y = 5
  ) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig2b_reprate_data.png"), width = 10, height = 8)


# Alternatively: Jitter plot
df %>%
  transmute(Cat.Data, success, tstat = abs(tstat)) %>%
  ggplot(aes(
    x = Cat.Data %>% fct_rev() %>% relevel("Other"),
    y = tstat
  )) +
  geom_jitter(width = .15, height = 0) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  labs(
    y = "t-statistic",
    x = "Predictor Category"
  ) +
  coord_flip() +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig2b_reprate_data_Jitter.png"), width = 10, height = 8)


# Scatter of replication t-stat vs OP t-stat ------------------------------

docnew = readdocumentation() # for easy updating of documentation

df <- read_xlsx(
        paste0(pathDataPortfolios, "PredictorSummary.xlsx")
      , sheet = 'full'
    ) %>%
    filter(
        samptype == 'insamp', port == 'LS'
    ) %>%
    select(signalname, tstat) %>%
    left_join(
        docnew, by='signalname'
    ) %>%
    transmute(signalname,
              Authors,
              tstatRep = abs(tstat), 
              tstatOP = abs(as.numeric(T.Stat)),
              PredOP = Predictability.in.OP,
              RepType = Signal.Rep.Quality,
              OPTest = Test.in.OP,
              Evidence.Summary) %>%
    mutate(
        porttest = grepl('port sort', OPTest, ignore.case = TRUE)
        | grepl('LS', OPTest, ignore.case = FALSE)   
        | grepl('double sort', OPTest, ignore.case = FALSE)
        , standard = !( grepl('nonstandard', OPTest) | grepl('FF3 style', OPTest) )
    ) %>%
  filter(
      PredOP %in% c('1_clear', '2_likely')
  )

    
# select comparable only
df_plot = df %>%    
  filter(
      !is.na(OPTest), porttest
     , RepType %in% c('1_good','2_fair')
  ) 


# regression
reg = lm(tstatRep ~ tstatOP, data = df_plot) %>% summary()
regstr  = paste0(
    '[t reproduction] = ', round(reg$coefficients[1], 2)
  , ' + ', format(round(reg$coefficients[2], 2), nsmall = 2)
  , ' [t original], R-sq = ', round(100*reg$r.squared, 0), '%'
)

ablines = tibble(slope = c(1, round(reg$coefficients[2], 2)), 
                 intercept = c(0, round(reg$coefficients[1], 2)),
                 group = factor(x = c('45 degree line', 'OLS fit'),
                                levels = c('OLS fit', '45 degree line')))


df_plot %>%
    mutate(
        PredOP
        = factor(PredOP
               , levels = c('1_clear', '2_likely', '4_not')
               , labels = c('Clear', 'Likely', 'Not'))
    ) %>% 
    ggplot(aes(y = tstatRep, x = tstatOP)) +
    geom_point(size =4, aes(shape = PredOP)) +
    scale_shape_manual(values=c(19,2,3)) +
    geom_abline(data = ablines, aes(slope = slope, intercept = intercept, linetype = group)) +    
    annotate('text',x=3.3, y=14, label = regstr, size = 8) +
    coord_trans(x='log10', y='log10', xlim = c(1.5, 17), ylim = c(1.0, 15)) +
#    coord_trans(x='log10', y='log10', xlim = c(0.5, 17), ylim = c(0.5, 15)) +    
    labs(y = 't-stat reproduction', 
         x = 't-stat original study', 
         linetype = '',
         shape = 'Predictor Category') + 
    ggrepel::geom_text_repel(aes(label=signalname)) +
    scale_x_continuous(breaks=c(2, 5, 10, 15)) +
    scale_y_continuous(breaks=c(2, 5, 10, 15)) +
    theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
    theme(legend.position = c(.8, .25)) 


temp = 1.5
ggsave(filename = paste0(pathResults, "fig_tstathand_vs_tstatOP.png")
     , width = 10*temp, height = 6*temp)

# hand examine for comparables
df_plot %>% filter(PredOP == '2_likely', !is.na(tstatOP)) %>%
    select(signalname, Authors, tstatRep, tstatOP, RepType) %>% arrange(Authors)


df %>% filter(porttest, !is.na(tstatOP), !RepType %in% c('1_good','2_fair')) %>%
    select(signalname, Authors, tstatRep, tstatOP, RepType) %>% arrange(Authors)

# McLean and Pontiff style graphs -----------------------------------------

# stats
stats <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                   sheet = 'short') %>%
  select(signalname, tstat, rbar)

statsFull <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                       sheet = 'full') %>%
  filter(samptype == 'postpub', port == 'LS') %>% 
  select(signalname, tstat, rbar) 

mpSignals = read_xlsx(
  paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet = 'MP'
) %>%
  filter(ClosestMatch != '_missing_')

# Merge data
# alldocumentation is created in 00_SettingsAndTools.R
df_merge <- readdocumentation() %>%
  # Add flag for whether in MP
  mutate(inMP = signalname %in% mpSignals$ClosestMatch) %>% 
  filter(Cat.Signal == 'Predictor' | inMP) %>% 
  left_join(stats, by = c("signalname")) %>%
  left_join(statsFull %>% 
              transmute(signalname, tstatPS = tstat, rbarPS = rbar),
            by = 'signalname') %>% 
  # for easier comparison, make sure all negative t-stats -> abs()
  mutate_at(.vars = vars(tstat, tstatPS, rbar, rbarPS),
            .funs = list(~ifelse(tstat <0, abs(.), .))) %>% 
  transmute(signalname,
            tstat, tstatPS, DeclineTstat = tstat - tstatPS,
            rbar, rbarPS, DeclineRBar = rbar - rbarPS,
            Category = Predictability.in.OP %>%
              factor(
                levels = c("indirect", "4_not", "3_maybe", "2_likely", "1_clear"),
                labels = c("no evidence", "not", "maybe", "likely", "clear")
              ),
            CatPredPlacebo = Cat.Signal,
            inMP
  ) %>% 
  filter(signalname != 'IO_ShortInterest') %>%
    filter(Category %in% c('clear','likely')) 


# In-sample return
plotret =  df_merge %>%
  mutate(inMPStr = ifelse(inMP, 'in MP (2016)', 'not in MP (2016)')) %>% 
  ggplot(aes(x = DeclineRBar, y = rbar)) +
  geom_smooth(method = 'lm', color = 'black', aes(linetype = inMPStr), show.legend = F) +
  geom_point(aes(shape = inMPStr), size = 2) +
  scale_shape_manual(values = c(19, 2)) +
    # 45 deg line
  geom_abline(intercept = 0, slope = 1, linetype = 'dotted') +    
  # Add 0,0 as reference lines
  geom_hline(yintercept = 0, linetype = 1) +
  geom_vline(xintercept = 0, linetype = 1) +
  labs(x = 'Decline in return post-publication', 
       y = 'In-Sample return',
       shape = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = c(0, 1), legend.justification = c(0, 1)) +
  coord_trans(xlim = c(-1.0, 2), ylim = c(0, 2.5))     

# In-sample t-stat
plott =  df_merge %>% 
  mutate(inMPStr = ifelse(inMP, 'in MP (2016)', 'not in MP (2016)')) %>% 
  ggplot(aes(x = DeclineRBar, y = tstat)) +
  geom_smooth(method = 'lm', color = 'black', aes(linetype = inMPStr), show.legend = FALSE) +
  geom_point(aes(shape = inMPStr), size = 2) +
  scale_shape_manual(values = c(19, 2)) +
  # Add 0,0 as reference lines
  geom_hline(yintercept = 0, linetype = 1) +
  geom_vline(xintercept = 0, linetype = 1) +
  labs(x = 'Decline in return post-publication', 
       y = 'In-Sample t-statistic',
       shape = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = c(0, 1), legend.justification = c(0, 1)) +
  coord_trans(xlim = c(-1.0, 2), ylim = c(0, 14)) +
  scale_y_continuous(breaks=seq(0,14,2))


plotboth = grid.arrange(plotret,plott,nrow=2)

ggsave(filename = paste0(pathResults, 'fig5_MP_both.png')
     , plot = plotboth
     , width = 7, height = 8)

# manual inspection 
df_merge %>% filter(inMP) %>% select(signalname, tstat, Category) %>% arrange(tstat)

df_merge %>% filter(inMP) %>% summarize(mean(rbar), sd(rbar), sum(tstat>1.5))





# Big summary table for paper ---------------------------------------------

stats <- read_xlsx(
  path = paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
  sheet = 'short'
)

statsFull <- read_xlsx(
  path = paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
  sheet = 'full'
)

# Merge data
# alldocumentation is created in 00_SettingsAndTools.R
df_merge <- readdocumentation() %>%
  filter(Cat.Signal == 'Predictor') %>% 
  left_join(stats %>%
    select(signalname, tstat, rbar),
  by = c("signalname")
  ) %>%
  left_join(statsFull %>% 
               filter(samptype == 'postpub', port == 'LS') %>% 
               transmute(signalname, `t-stat PS` = tstat),
             by = 'signalname') %>% 
  transmute(
    ref = paste0(Authors, ' (', Year, ')'),
    Predictor = LongDescription,
    signalname,
    sample = paste0(SampleStartYear,'-',SampleEndYear),
    `Mean Return` = round(rbar, digits = 2),
    `t-stat IS` = round(tstat, digits = 2),
    Evidence = Evidence.Summary,        
    Category = Predictability.in.OP %>%
      factor(
        levels = c("indirect", "4_not", "3_maybe", "2_likely", "1_clear"),
        labels = c("no evidence", "not", "maybe", "likely", "clear")
      )
  ) %>%
  arrange(ref) 



# Create Latex output table 1: Clear Predictors
outputtable1 <- xtable(df_merge %>%
  filter(Category == "clear") %>%
  select(-Category))


print(outputtable1,
  include.rownames = FALSE,
  include.colnames = FALSE,
  hline.after = NULL,
  only.contents = TRUE,
  file = paste0(pathResults, "bigSignalTableClear.tex")
)

# Create Latex output table 2: Likely predictors
outputtable2 <- xtable(df_merge %>%
  filter(Category == "likely") %>%
  select(-Category))


print(outputtable2,
  include.rownames = FALSE,
  include.colnames = FALSE,
  hline.after = NULL,
  only.contents = TRUE,
  file = paste0(pathResults, "bigSignalTableLikely.tex")
)




