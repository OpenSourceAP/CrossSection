# copied from setup_crspm.r
# Seems to run out of memory in newer Rstudio / R, on my 8 gb ram home pc - ac
# was fixed by buying more ram - ac
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
crspinfo = crspm %>%  select(permno, yyyymm, prc, exchcd, me, shrcd) %>%
    arrange(permno, yyyymm)

# add info for easy me quantile screens
tempcut <- crspinfo %>%
  filter(exchcd == 1) %>%
  group_by(yyyymm) %>%
  summarize(
    me_nyse10 = quantile(me, probs = 0.1, na.rm = T),
    me_nyse20 = quantile(me, probs = 0.2, na.rm = T)
  )

crspinfo <- crspinfo %>%
  left_join(tempcut, by = "yyyymm")


rm(crspd,crspm)
