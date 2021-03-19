# Predictor t-stat in extended dataset ------------------------------------

# Define relevant set
docnew = readdocumentation() %>% 
  filter(Predictability.in.OP != '9_drop') %>% 
  mutate(Category = Predictability.in.OP %>%
  factor(
    levels = c("indirect", "4_not", "3_maybe", "2_likely", "1_clear"),
    labels = c("Indirect Evidence", "Not Predictor"
             , "maybe", "Likely Predictor", "Clear Predictor"))
  )

# Add stats
stats <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                   sheet = 'short') %>%
  transmute(signalname, 
            success = 1 * (round(tstat, digits = 2) >= 1.96),
            tstat, rbar) %>% 
  bind_rows(
    read_xlsx(paste0(pathDataPortfolios, "PlaceboSummary.xlsx"),
              sheet = 'ls_insamp_only') %>%
      transmute(signalname, 
                success = 1 * (round(tstat, digits = 2) >= 1.96),
                tstat, rbar)  
  )


statsFull <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                   sheet = 'full') %>%
  filter(samptype == 'postpub', port == 'LS') %>% 
  transmute(signalname, `t-stat PS` = tstat) %>% 
  bind_rows(
    read_xlsx(paste0(pathDataPortfolios, "PlaceboSummary.xlsx"),
              sheet = 'full') %>% 
      filter(samptype == 'postpub', port == 'LS') %>% 
      transmute(signalname, `t-stat PS` = tstat)
  )

# Merge data
df_merge <- docnew %>%
  left_join(stats %>%
               select(signalname, tstat, rbar),
             by = c("signalname")
  ) %>%
  left_join(statsFull) %>% 
  transmute(
    ref = paste0(Authors, ' (', Year, ')'),
    Predictor = LongDescription,
    signalname,
    sample = paste0(SampleStartYear,'-',SampleEndYear),
    `Mean Return` = round(rbar, digits = 2),
    `t-stat IS` = round(tstat, digits = 2),
    Evidence = Evidence.Summary,
    Category    
  ) %>%
    mutate(
        ref = if_else(ref == 'NA (NA)', '', ref)
    ) %>%    
  arrange(ref) 


df_merge %>%
  transmute(Category, tstat = abs(`t-stat IS`)) %>% 
  ggplot(aes(x = Category, y = tstat)) +
  geom_jitter(width = .2, height = 0) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  #  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(y = 't-statistic',
       x = '') +
  coord_flip() +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, "fig2b_reprate_PredictorPlacebo_Jitter.png"), width = 10, height = 8)


# # Create Latex output table 2: Placebos
temp = df_merge %>%
    filter(Category %in% c('Not Predictor', 'Indirect Evidence'))  %>%
    arrange(ref) %>%
    select(ref, Predictor, signalname, Category, `Mean Return`, `t-stat IS`, Evidence)
outputtable2 = xtable(temp)

print(outputtable2,
      include.rownames = FALSE,
      include.colnames = FALSE,
      hline.after = NULL,
      only.contents = TRUE,
      file = paste0(pathResults, "bigSignalTablePlacebos.tex")
)


# McLean and Pontiff style graphs -----------------------------------------
# (placed after placebo creation because we classify a few of MP's predictors as placebos)

# stats
stats <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                   sheet = 'short') %>%
  select(signalname, tstat, rbar) %>% 
  bind_rows(
    read_xlsx(paste0(pathDataPortfolios, "PlaceboSummary.xlsx"),
              sheet = 'ls_insamp_only') %>% 
      select(signalname, tstat, rbar)
    )

statsFull <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                       sheet = 'full') %>%
  filter(samptype == 'postpub', port == 'LS') %>% 
  select(signalname, tstat, rbar) %>% 
  bind_rows(
    read_xlsx(paste0(pathDataPortfolios, "PlaceboSummary.xlsx"),
              sheet = 'full') %>% 
      filter(samptype == 'postpub', port == 'LS') %>% 
      select(signalname, tstat, rbar)
  )

mpSignals = read_xlsx(
  paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet = 'MP'
) %>%
  filter(ClosestMatch != '_missing_')

# Merge data
# alldocumentation is created in 00_SettingsAndTools.R
df_merge <- alldocumentation %>%
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
plotret = df_merge %>%
  mutate(inMPStr = ifelse(inMP, 'in MP (2016)', 'not in MP (2016)')) %>% 
  ggplot(aes(x = DeclineRBar, y = rbar, shape = inMPStr)) +
  geom_smooth(method = 'lm', color = 'black') +
  geom_point(aes(fill = CatPredPlacebo), size = 3) +
  # 45 deg line
  geom_abline(intercept = 0, slope = 1, linetype = 'dotted') +    
  # Add 0,0 as reference lines
  geom_hline(yintercept = 0, linetype = 1) +
  geom_vline(xintercept = 0, linetype = 1) +
  scale_shape_manual(values = c(21, 24)) +
  scale_fill_manual(
    values = c(NA, "black"),
    guide = FALSE) + #guide_legend(override.aes = list(shape = 21))) +
  labs(x = 'Decline in return post-publication', 
       y = 'In-Sample return',
       shape = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = c(0, 1), legend.justification = c(0, 1)) +
  coord_trans(xlim = c(-1.0, 2), ylim = c(0, 2.5))     


# In-sample t-stat
plott = df_merge %>% 
  mutate(inMPStr = ifelse(inMP, 'in MP (2016)', 'not in MP (2016)')) %>% 
  ggplot(aes(x = DeclineRBar, y = tstat, shape = inMPStr)) +
  geom_smooth(method = 'lm', color = 'black') +
  geom_point(aes(fill = CatPredPlacebo), size = 3) +
  # Add 0,0 as reference lines
  geom_hline(yintercept = 0, linetype = 1) +
  geom_vline(xintercept = 0, linetype = 1) +
  scale_shape_manual(values = c(21, 24)) +
  scale_fill_manual(
    values = c(NA, "black"),
    guide = FALSE) + #guide_legend(override.aes = list(shape = 21))) +
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




# Replication rate vis-a-vis other studies --------------------------------

mpSignals = read_xlsx(
  paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet = 'MP'
) %>%
  filter(ClosestMatch != '_missing_')

hxzSignals = read_xlsx(
  paste0(pathProject, 'SignalDocumentation.xlsx')
  , sheet = 'HXZ'
) %>%
  filter(ClosestMatch != '_missing_')

stats <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                   sheet = 'short') %>%
  select(signalname, tstat, rbar) %>% 
  bind_rows(
    read_xlsx(paste0(pathDataPortfolios, "PlaceboSummary.xlsx"),
              sheet = 'ls_insamp_only') %>% 
      select(signalname, tstat, rbar)
  ) %>%
    left_join(
        readdocumentation() %>%
        select(signalname, Cat.Signal, Predictability.in.OP) %>%
        mutate(
            Cat.Signal = if_else(Cat.Signal=='Predictor','Clear or Likely',Cat.Signal)
            , Cat.Signal = if_else(Cat.Signal=='Placebo','Indirect or Not',Cat.Signal)
        )
    )

df_tmp = stats %>%
    # Add flag for whether in MP or HXZ
    transmute(
        signalname,
        tstat = abs(tstat),
        PredOP = factor(Predictability.in.OP, 
                        levels =
                            c('1_clear', '2_likely', '3_maybe', 'indirect', '4_not'), 
                        labels =
                            c('Clear Predictor', 'Likely Predictor', 'Indirect Signal', 'Indirect Signal', 'Not Predictor')),
        Cat.Signal,
        inMP = signalname %in% mpSignals$ClosestMatch,
        inHXZ = signalname %in% hxzSignals$ClosestMatch) 

# Our study
df_tmp %>% 
  ggplot(aes(x = fct_rev(PredOP), y = tstat, shape = Cat.Signal)) +
  geom_jitter(width = .2, height = 0, size = 3) +
  scale_shape_manual(values = c(19, 2)) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  labs(y = 't-statistic',
       x = '',
       shape = '') +
  coord_flip() +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = c(0.8, 0.1))

ggsave(filename = paste0(pathResults, 'fig_reprate_ourstudy.png'), width = 12, height = 8)

# HXZ
df_tmp %>% 
  filter(inHXZ) %>% 
  ggplot(aes(x = fct_rev(PredOP), y = tstat, shape = Cat.Signal)) +
  geom_jitter(width = .2, height = 0, size = 4) +
  scale_shape_manual(values = c(19, 2), guide = F) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  labs(y = 't-statistic',
       x = '',
       shape = '') +
  coord_flip() +
  theme_minimal(base_size = optFontsize + 4, base_family = optFontFamily) +
  theme(legend.position = c(.8, .15))


ggsave(filename = paste0(pathResults, 'fig_reprate_HXZ.png'), width = 12, height = 8)

# MP
df_tmp %>% 
  filter(inMP) %>% 
  ggplot(aes(x = fct_rev(PredOP), y = tstat, shape = Cat.Signal)) +
  geom_jitter(width = .2, height = 0, size = 4) +
  scale_shape_manual(values = c(19, 2)) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  labs(y = 't-statistic',
       x = '',
       shape = '') +
  coord_flip() +
  theme_minimal(base_size = optFontsize + 4, base_family = optFontFamily)  +
  theme(legend.position = c(.8, .2))


ggsave(filename = paste0(pathResults, 'fig_reprate_MP.png'), width = 12, height = 8)


# manual counts
df_tmp %>% filter(inHXZ) %>% group_by(PredOP) %>% summarize(sum(tstat<1.96), n())
df_tmp %>% filter(inHXZ) %>% summarize(fail = sum(tstat<1.96), n(), fail/n())
df_tmp %>% filter(inHXZ,PredOP=='Clear') %>% arrange(tstat)

df_tmp %>% filter(inMP) %>% summarize(sum(tstat<1.5)/n(), sum(tstat<1.96)/n())

df_tmp %>% filter(inMP,PredOP == 'Clear')%>%
    summarize(sum(tstat<1.5)/n(), sum(tstat<1.96)/n())
