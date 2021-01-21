# copied from setup_crspm.r
# 2021 01 AC


## load daily CRSP 
# I've seen weird issues with daily crsp splits for prices (Google in 2014?)
# but that shouldn't affect returns -ac
crspd = read_fst(paste0(pathDataIntermediate, 'd_crsp.fst')) %>%
    select(permno,date,ret) %>%
    mutate(
        date = as.Date(date)
        , yyyymm = year(date)*100+month(date)        
    )

## load monthly CRSP
crspm = read_fst(paste0(pathDataIntermediate, 'm_crsp.fst')) %>%
    mutate(
        date = as.Date(date)
    ) %>%
    mutate(
        me = abs(prc)*shrout
      , yyyymm = year(date)*100+month(date)
    )

templag = crspm %>% select(permno, yyyymm, me) %>%
    mutate(
        yyyymm = yyyymm + 1
      , yyyymm = if_else(yyyymm %% 100 == 13, yyyymm+100-12,yyyymm)
    ) %>%
    transmute(permno, yyyymm, melag = me)



## create crspret for returns (daily)  and crspinfo for screens (monthly)
# subset into two smaller datasets, good for memory I think
gc()
crspret = crspd %>% select(permno, date, yyyymm, ret) %>%
    left_join(templag, by=c('permno','yyyymm')) %>%
    arrange(permno, yyyymm)

gc()
crspinfo = crspm %>%  select(permno, yyyymm, prc, exchcd,me) %>%
    arrange(permno, yyyymm)

rm(crspd,crspm)
