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


# Predictor t-stat in extended dataset ------------------------------------

# Define relevant set
docnew = alldocumentation %>% 
  filter(Predictability.in.OP != '9_drop') %>% 
  mutate(Category = Predictability.in.OP %>%
  factor(
    levels = c("no_evidence", "4_not", "3_maybe", "2_likely", "1_clear"),
    labels = c("no evidence", "not", "maybe", "likely", "clear"))
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
  transmute(Authors,
            Year = as.integer(Year),
            Predictor = LongDescription,
            `Sample Start` = as.integer(SampleStartYear),
            `Sample End` = as.integer(SampleEndYear),
            `Mean Return` = round(rbar, digits = 2),
            `t-stat IS` = round(tstat, digits = 2),
            `t-stat PS`,
            Evidence = Evidence.Summary,
            Category
  ) %>%
  arrange(Category, Authors, Year)


df_merge %>%
  transmute(Category, tstat = abs(`t-stat IS`)) %>% 
  ggplot(aes(x = Category, y = tstat)) +
  geom_jitter(width = .2, height = 0) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  #  geom_boxplot(alpha = 0, outlier.shape = NA) +
  labs(y = 't-statistic',
       x = 'Predictor Category') +
  coord_flip() +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) 

ggsave(filename = paste0(pathResults, "fig2b_reprate_PredictorPlacebo_Jitter.png"), width = 10, height = 8)


# # Create Latex output table 2: Placebos
outputtable2 = xtable(df_merge %>%
                        filter(Category %in% c('not', 'maybe', 'no evidence')) %>%
                        arrange(desc(Category), Authors, Year) %>%
                        select(-Category)
)

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
                levels = c("no_evidence", "4_not", "3_maybe", "2_likely", "1_clear"),
                labels = c("no evidence", "not", "maybe", "likely", "clear")
              ),
            CatPredPlacebo = Cat.Signal,
            inMP
  )
  


# In-sample t-stat
df_merge %>% 
  filter(signalname != 'IO_ShortInterest') %>% 
  mutate(inMPStr = ifelse(inMP, 'in MP (2016)', 'not in MP (2016)')) %>% 
  ggplot(aes(x = DeclineRBar, y = tstat, shape = inMPStr)) +
  geom_smooth(method = 'lm', color = 'black') +
  geom_point(aes(fill = CatPredPlacebo), size = 3) +
  # Add MP t-stat of 1.5 as reference line
  geom_hline(yintercept = 1.5, linetype = 2) +
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
  theme(legend.position = c(0, 1), legend.justification = c(0, 1))

ggsave(filename = paste0(pathResults, 'fig5_MP_tstat.png'), width = 12, height = 8)


# In-sample return
df_merge %>% 
  filter(signalname != 'IO_ShortInterest') %>% 
  mutate(inMPStr = ifelse(inMP, 'in MP (2016)', 'not in MP (2016)')) %>% 
  ggplot(aes(x = DeclineRBar, y = rbar, shape = inMPStr)) +
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
       y = 'In-Sample return',
       shape = '') +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = c(0, 1), legend.justification = c(0, 1))

ggsave(filename = paste0(pathResults, 'fig5_MP_return.png'), width = 12, height = 8)


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
  select(signalname, tstat, rbar, Cat.Signal, Predictability.in.OP) %>% 
  bind_rows(
    read_xlsx(paste0(pathDataPortfolios, "PlaceboSummary.xlsx"),
              sheet = 'ls_insamp_only') %>% 
      select(signalname, tstat, rbar, Cat.Signal, Predictability.in.OP)
  )

df_tmp = stats %>%
  # Add flag for whether in MP or HXZ
  transmute(tstat = abs(tstat),
            PredOP = factor(Predictability.in.OP, 
                            levels = c('1_clear', '2_likely', '3_maybe', 'no_evidence', '4_not'), 
                            labels = c('Clear', 'Likely', 'Indirect Evidence', 'Indirect Evidence', 'Not')),
            Cat.Signal,
            inMP = signalname %in% mpSignals$ClosestMatch,
            inHXZ = signalname %in% hxzSignals$ClosestMatch) 

# Our study
df_tmp %>% 
  ggplot(aes(x = fct_rev(PredOP), y = tstat, shape = Cat.Signal)) +
  geom_jitter(width = .2, height = 0, size = 3) +
  scale_shape_manual(values = c(2, 19)) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  labs(y = 't-statistic',
       x = '',
       shape = 'Predictor Category') +
  coord_flip() +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily) +
  theme(legend.position = 'top')

ggsave(filename = paste0(pathResults, 'fig_reprate_ourstudy.png'), width = 12, height = 8)

# HXZ
df_tmp %>% 
  filter(inHXZ) %>% 
  ggplot(aes(x = fct_rev(PredOP), y = tstat, shape = Cat.Signal)) +
  geom_jitter(width = .2, height = 0, size = 4) +
  scale_shape_manual(values = c(2, 19)) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  labs(y = 't-statistic',
       x = '',
       shape = 'Predictor Category') +
  coord_flip() +
  theme_minimal(base_size = optFontsize + 4, base_family = optFontFamily) +
  theme(legend.position = c(.8, .1))


ggsave(filename = paste0(pathResults, 'fig_reprate_HXZ.png'), width = 12, height = 8)

# MP
df_tmp %>% 
  filter(inMP) %>% 
  ggplot(aes(x = fct_rev(PredOP), y = tstat, shape = Cat.Signal)) +
  geom_jitter(width = .2, height = 0, size = 4) +
  scale_shape_manual(values = c(2, 19), guide = FALSE) +
  geom_hline(yintercept = 1.96, linetype = "dashed") +
  labs(y = 't-statistic',
       x = '',
       shape = 'Predictor Category') +
  coord_flip() +
  theme_minimal(base_size = optFontsize + 4, base_family = optFontFamily)  +
  theme(legend.position = c(.8, .1))


ggsave(filename = paste0(pathResults, 'fig_reprate_MP.png'), width = 12, height = 8)
