# For baseline portfolio tests
# Andrew Chen 2020 01


rm(list=ls())

### ENVIRONMENT AND DATA ###

tryCatch(        
    source('00_SettingsAndFunctions.R')
  , error = function(cond){
      message('Error: 00_SettingsAndFunctions.R.  please check wd set to pathProject/Portfolios/Code/')          
  }
)

source('setup_crspm.r', echo = T)

######################################################################
### SELECT SIGNALS
######################################################################
# 2021 01 I took out the holdper == 1 requirement and added likely predictors
source('00_SettingsAndFunctions.R', echo = T)
strategylist0 = alldocumentation %>% filter(Cat.Signal == 'Predictor') 
strategylist0 = ifquickrun()

#####################################################################
### BASE PORTS
#####################################################################
port = loop_over_strategies(
    strategylist0 
)

# feedback
checkport(port)


## EXPORT
writestandard(port, pathDataPortfolios, 'PredictorPortsFull.csv')

### OUTPUT WIDE ###
portlswide = port %>%
    filter(port == 'LS') %>%    
    select(date,signalname,ret) %>%
    pivot_wider(names_from=signalname,values_from=ret)

writestandard(
    portlswide
  , pathDataPortfolios
  , 'PredictorLSretWide.csv'
)

# SUMMARY STATS BY SIGNAL -------------------------------------------------
# it makes sense to output summary here but not in the check stuff

# 

## define samples
sumbase = sumportmonth(
    port, groupme = c('signalname','port','samptype'), Nstocksmin = 20
)

sumbase2 = sumbase %>%
    left_join(
        alldocumentation %>%
        select(signalname, Authors, Cat.Predictor, Cat.Variant
             , SampleStartYear, SampleEndYear
               , weight_me, q_cut, holdper)
        , by = 'signalname'
    )


## export
write_xlsx(
    list(
        ls_insamp_only = sumbase2 %>%
              filter(
                  samptype == 'insamp'
                  , port == 'LS'
              ) %>%
              mutate(
                  tstat = round(tstat,2)                  
                  , rbar = round(rbar,3)
                  , vol = round(vol,3)
              ) %>%
              arrange(tstat)
        , full = sumbase2        
    )
  , paste0(pathDataPortfolios, 'PredictorSummary.xlsx')
)


# FEEDBACK ON ERRORS -------------------------------------------------

print('The following ports are computed succesfully')
print(
    sumbase %>% filter(port=='LS',samptype=='insamp') %>% arrange(tstat) %>% as.data.frame
)

print('The following ports failed to compute')
print(
    sumbase %>% filter(is.na(port)) %>% arrange(tstat) %>% as.data.frame
)


