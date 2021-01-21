# setup that is reused for many strategies
# 2021 01 AC


## load CRSP data
# keep around me and melag for sanity
crsp = read_fst(paste0(pathDataIntermediate, 'm_crsp.fst')) %>%
    mutate(
        date = as.Date(date)
    ) %>%
    mutate(
        me = abs(prc)*shrout
      , yyyymm = year(date)*100+month(date)
    ) 

templag = crsp %>% select(permno, yyyymm, me) %>%
    mutate(
        yyyymm = yyyymm + 1
      , yyyymm = if_else(yyyymm %% 100 == 13, yyyymm+100-12,yyyymm)
    ) %>%
    transmute(permno, yyyymm, melag = me)

## subset into two smaller datasets for cleanliness
gc()
crspret = crsp %>% select(permno, date, yyyymm, ret) %>%
    left_join(templag, by=c('permno','yyyymm')) %>%
    arrange(permno, yyyymm)
gc()
crspinfo = crsp %>% select(permno, yyyymm, prc, exchcd, me)  %>%
    arrange(permno, yyyymm)

# add info for easy me quantile screens
tempcut = crspinfo %>%
    filter(exchcd == 1) %>%
    group_by(yyyymm) %>%    
    summarize(
        me_nyse10 = quantile(me, probs=0.1, na.rm = T)
        , me_nyse20 = quantile(me, probs=0.2, na.rm = T)
    )
crspinfo = crspinfo %>%
    left_join(tempcut, by='yyyymm')

rm(crsp, templag, tempcut)


