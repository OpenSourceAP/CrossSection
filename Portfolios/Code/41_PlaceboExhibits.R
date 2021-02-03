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
  source("00_SettingsAndFunctions.R", echo = TRUE),
  error = function(cond) {
    message("Error: 00_SettingsAndFunctions.R not found.  please setwd to pathProject/Portfolios/Code/")
  }
)

# check system for dl method
dlmethod <- "auto"
sysinfo <- Sys.info()
if (sysinfo[1] == "Linux") {
  dlmethod <- "wget"
}


# Predictor t-stat in extended dataset ------------------------------------

stats <- read_xlsx(paste0(pathDataPortfolios, "PredictorSummary.xlsx"),
                   sheet = 'ls_insamp_only') %>%
  mutate(success = 1 * (round(tstat, digits = 2) >= 1.96)) %>% 
  bind_rows(
    read_xlsx(paste0(pathDataPortfolios, "PlaceboSummary.xlsx"),
              sheet = 'ls_insamp_only') %>%
      mutate(success = 1 * (round(tstat, digits = 2) >= 1.96))  
  )

df_meta <- read_xlsx(
  path = paste0(pathProject, "SignalDocumentation.xlsx"),
  sheet = "BasicInfo"
) %>%
  mutate_at(
    .vars = vars(starts_with("Cat.")),
    .funs = list(str_to_title)
  ) %>% 
  filter(Cat.Signal != 'Drop')


# Merge data
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
              Cat.Signal,
            Category = `Predictability in OP` %>%
              factor(
                levels = c("no_evidence", "4_not", "3_maybe", "2_likely", "1_clear"),
                labels = c("no evidence", "not", "maybe", "likely", "clear")
              )
  ) %>%
  arrange(Authors, Year)


df_merge %>%
  transmute(Category, tstat = abs(`t-stat`)) %>% 
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
                        filter(Cat.Signal == 'Placebo') %>%
                        arrange(desc(Category), Authors, Year) %>%
                        select(-Cat.Signal)
)

print(outputtable2,
      include.rownames = FALSE,
      include.colnames = FALSE,
      hline.after = NULL,
      only.contents = TRUE,
      file = paste0(pathResults, "bigSignalTablePlacebos.tex")
)
