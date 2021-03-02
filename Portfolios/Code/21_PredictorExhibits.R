## Exhibits for paper

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

tryCatch(
  source("00_SettingsAndTools.R", echo = TRUE),
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



# Import factor returns from Kenneth French's website ---------------------

# FF 5 factors
download.file("http://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Research_Data_5_Factors_2x3_CSV.zip",
              destfile = paste0(pathDataIntermediate, "temp.zip"),
              method = dlmethod
)

# incovenenient setwd because of a peculiarity of unzip(), see
# https://stackoverflow.com/questions/15226150/r-exdir-does-not-exist-error
setwd(pathDataIntermediate)
unzip("temp.zip") #, exdir = pathDataIntermediate)
setwd(pathCode)

# Momentum (FF style)
download.file("https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/ftp/F-F_Momentum_Factor_CSV.zip",
              destfile = paste0(pathDataIntermediate, "temp.zip"),
              method = dlmethod
)

setwd(pathDataIntermediate)
unzip("temp.zip")
setwd(pathCode)

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

df <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx")) %>%
  mutate(success = 1 * (round(tstat, digits = 2) >= 1.96))

# Check if predictor summary has in-sample returns only
if (sum(df$samptype == 'insamp') != nrow(df)) {
  message('Mixing different sample types below!!')
}

df_meta <- read_xlsx(
  path = paste0(pathProject, "SignalDocumentation.xlsx"),
  sheet = "BasicInfo"
) %>%
  mutate_at(
    .vars = vars(starts_with("Cat.")),
    .funs = list(str_to_title)
  )

# Use most recent Category labels
df <- df %>%
  select(signalname, success, tstat) %>%
  left_join(df_meta %>%
    select(Acronym, starts_with("Cat.")),
  by = c("signalname" = "Acronym")
  )


# Replication success by data category (for baseline ones)
labelData <- df %>%
  filter(Cat.Signal == "Predictor") %>%
  group_by(Cat.Data) %>%
  summarise(
    rate = mean(success),
    n = n()
  ) %>%
  mutate(rate = paste(round(100 * rate, 0) %>% as.character(), "%")) %>%
  ungroup()

df %>%
  filter(Cat.Signal == "Predictor") %>%
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
  filter(Cat.Signal == "Predictor") %>%
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
        samptype == 'insamp', Cat.Signal == 'Predictor', port == 'LS'
    ) %>%
    select(signalname, tstat) %>%
    left_join(
        docnew, by='signalname'
    ) %>%
    transmute(signalname, 
              tstatRep = abs(tstat), 
              tstatOP = abs(as.numeric(T.Stat)),
              PredictabilityOP = Predictability.in.OP,
              ReplicationType = Signal.Rep.Quality,
              OPTest = Test.in.OP)


df_plot = df %>% 
  filter(PredictabilityOP == '1_clear', ReplicationType == '1_good') %>%
  filter(!is.na(OPTest)) %>% 
  mutate(grouper = case_when(
    grepl('port sort', OPTest, ignore.case = TRUE) ~ 'Portfolio sort',
    grepl('event', OPTest, ignore.case = TRUE)     ~ 'Event Study',
    grepl('LS', OPTest, ignore.case = FALSE)        ~ 'Portfolio sort',
    grepl('reg', OPTest, ignore.case = TRUE)       ~ 'Regression',
    TRUE ~ 'Other'
  )) %>% 
  filter(
      grouper == 'Portfolio sort' & !grepl('nonstandard', OPTest)
  ) 

reg = lm(tstatRep ~ tstatOP, data = df_plot) %>% summary()

df_plot %>% 
  ggplot(aes(y = tstatRep, x = tstatOP, label=signalname)) +
  # ggplot(aes(x = tstatRep, y = tstatOP, label=signalname, group = grouper, color = grouper)) +
  geom_point() +
  geom_smooth(method = 'lm') +
  labs(y = 't-stat reproduction', x = 't-stat original study', 
       title = paste0('y = ', round(reg$coefficients[1], 2), ' + ', round(reg$coefficients[2], 2), ' * x, R2 = ', round(100*reg$r.squared, 2), '%')) +
  geom_abline(intercept = 0, slope = 1) +
  ggrepel::geom_text_repel() +
  coord_cartesian(xlim = c(0, 17), ylim = c(0, 17)) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig_tstathand_vs_tstatOP_Labels.png"), width = 10, height = 8)


df_plot %>% 
  ggplot(aes(y = tstatRep, x = tstatOP, label=signalname)) +
  geom_point() +
  geom_smooth(method = 'lm') +
  labs(y = 't-stat reproduction', x = 't-stat original study', 
       title = paste0('y = ', round(reg$coefficients[1], 2), ' + ', round(reg$coefficients[2], 2), ' * x, R2 = ', round(100*reg$r.squared, 2), '%')) +
  geom_abline(intercept = 0, slope = 1) +
  theme_minimal(base_size = optFontsize, base_family = optFontFamily)

ggsave(filename = paste0(pathResults, "fig_tstathand_vs_tstatOP.png"), width = 10, height = 8)




# Big summary table for paper ---------------------------------------------

basicInfo <- read_xlsx(
  path = paste0(pathProject, "SignalDocumentation.xlsx"),
  sheet = "BasicInfo"
) %>%
  filter(Cat.Signal != "Drop")

stats <- read_xlsx(
  path = paste0(pathDataPortfolios, "PredictorSummary.xlsx")
)


# Merge data
# alldocumentation is created in 00_SettingsAndTools.R
df_merge <- alldocumentation %>%
  inner_join(stats %>%
    select(signalname, tstat, rbar),
  by = c("signalname")
  ) %>%
  transmute(Authors,
    Year = as.integer(Year),
    Predictor = LongDescription,
    `Sample Start` = as.integer(SampleStartYear),
    `Sample End` = as.integer(SampleEndYear),
    `Mean Return` = round(rbar, digits = 2),
    `t-stat` = round(tstat, digits = 2),
#    Cat.Signal,
    Category = Predictability.in.OP %>%
      factor(
        levels = c("no_evidence", "4_not", "3_maybe", "2_likely", "1_clear"),
        labels = c("no evidence", "not", "maybe", "likely", "clear")
      )
  ) %>%
  arrange(Authors, Year)




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

# Create Latex output table 1: Likely predictors
outputtable1 <- xtable(df_merge %>%
  filter(Category == "likely") %>%
  select(-Category))


print(outputtable1,
  include.rownames = FALSE,
  include.colnames = FALSE,
  hline.after = NULL,
  only.contents = TRUE,
  file = paste0(pathResults, "bigSignalTableLikely.tex")
)
