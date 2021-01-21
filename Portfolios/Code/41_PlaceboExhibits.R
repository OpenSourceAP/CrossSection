
basicInfo = read_xlsx(
  path = paste0('SignalDocumentation.xlsx')
  , sheet ='BasicInfo'
) %>% 
  filter(Cat.Predictor != '9_drop')

constructionInfo = read_xlsx(
  path = paste0('SignalDocumentation.xlsx')
  , sheet ='Construction'
) %>% 
  select(Acronym, SampleStartYear, SampleEndYear)

stats =  read_xlsx(
  path = paste0(pathSummary, 'SignalSummaryBase.xlsx')
) 


# Merge data
df_merge = basicInfo %>% 
  left_join(constructionInfo) %>% 
  left_join(stats %>% 
              select(signalname, tstat, ret),
            by = c('Acronym' = 'signalname')) %>% 
  transmute(Authors, 
            Year = as.integer(Year), 
            Predictor = LongDescription, 
            `Sample Start` = as.integer(SampleStartYear), 
            `Sample End` = as.integer(SampleEndYear),
            `Mean Return` = round(ret, digits = 2),
            `t-stat` = round(tstat, digits = 2),
            Category = Cat.Predictor %>% 
              factor(levels = c('4_not', '3_maybe', '2_likely', '1_clear'),
                     labels = c('not', 'maybe', 'likely', 'clear')),
            Variant = Cat.Variant %>% 
              factor(levels = c('1_original', '2_lag', '2_quarterly', '2_risk_model'),
                     labels = c('Original', 'Lag structure', 'Quarterly', 'Risk Model'))) %>% 
  arrange(Authors, Year)


## # Create Latex output table 2: Extended dataset
## for later
## outputtable2 = xtable(df_merge %>% 
##                         filter(Variant == 'Original' & Category != 'clear' & Category != 'likely') %>% 
##                         arrange(desc(Category), Authors, Year) %>% 
##                         select(-Variant)
## )


## print(outputtable2, 
##       include.rownames = FALSE,
##       include.colnames = FALSE,
##       hline.after = NULL,
##       only.contents = TRUE,
##       file = paste0(pathResults, "bigSignalTableExtended.tex")
## )

