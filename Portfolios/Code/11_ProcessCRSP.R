# processes CRSP download
# separate from the download file in case you need to patch the download and
# don't want to wait an hour to test the code
# 2021 04


# ==== MONTHLY CRSP SETUP ==== 
crspm = read_fst(paste0(pathProject,'Portfolios/Data/Intermediate/m_crsp_raw.fst'))

# incorporate delisting return
# GHZ cite Johnson and Zhao (2007), Shumway and Warther (1999)
# but the way HXZ does this might be a bit better
crspm = crspm %>%
  mutate(
    dlret = ifelse(
      is.na(dlret)
      & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584))
      & (exchcd == 1 | exchcd == 2)
      , -0.35
      , dlret
    )
    , dlret = ifelse(
      is.na(dlret)
      & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584))
      & (exchcd == 3)
      , -0.55
      , dlret
    )
    , dlret = ifelse(
      dlret < -1 & !is.na(dlret)
      , -1
      , dlret
    )
    , dlret = ifelse(
      is.na(dlret)
      , 0
      , dlret
    )
    , ret = ret + dlret
    , ret = ifelse(
      is.na(ret) & ( dlret != 0)
      , dlret
      , ret
    )
  )

# convert ret to pct, other formatting
crspm = crspm %>%
  mutate(
    ret = 100*ret
    , date = as.Date(date)
    , me = abs(prc) * shrout
    , yyyymm = year(date) * 100 + month(date)    
  )

# keep around me and melag for sanity
templag <- crspm %>%
  select(permno, yyyymm, me) %>%
  mutate(
    yyyymm = yyyymm + 1,
    yyyymm = if_else(yyyymm %% 100 == 13, yyyymm + 100 - 12, yyyymm)
  ) %>%
  transmute(permno, yyyymm, melag = me)

## subset into two smaller datasets for cleanliness
gc()
crspmret <- crspm %>%
  select(permno, date, yyyymm, ret) %>%
  filter(!is.na(ret)) %>%
  left_join(templag, by = c("permno", "yyyymm")) %>%
  arrange(permno, yyyymm)
gc()
crspminfo <- crspm %>%
  select(permno, yyyymm, prc, exchcd, me, shrcd) %>%
  arrange(permno, yyyymm)

# add info for easy me quantile screens
tempcut <- crspminfo %>%
  filter(exchcd == 1) %>%
  group_by(yyyymm) %>%
  summarize(
    me_nyse10 = quantile(me, probs = 0.1, na.rm = T),
    me_nyse20 = quantile(me, probs = 0.2, na.rm = T)
  )
crspminfo <- crspminfo %>%
  left_join(tempcut, by = "yyyymm")


# write to disk
write_fst(crspmret, paste0(pathProject,'Portfolios/Data/Intermediate/crspmret.fst'))
write_fst(crspminfo, paste0(pathProject,'Portfolios/Data/Intermediate/crspminfo.fst'))

## clean up
rm(list=ls(pattern='crsp'))
rm(list=ls(pattern='temp'))


# ==== DAILY CRSP SETUP ====
if (!skipdaily){
  
  # unlike monthly crsp, we try to do this in place for memory mgmt
  crspdret = read_fst(
    paste0(pathProject,'Portfolios/Data/Intermediate/d_crsp_raw.fst')
    , columns = c('permno','date','ret')
  ) %>% setDT()
  
  # drop na, reformat 
  crspdret = crspdret[
    !is.na(ret)  
  ][
    , ':=' (
      ret = 100*ret
      , date = as.Date(date)
      , yyyymm = year(date)*100+month(date) 
    )
  ][
    order(permno,date)
  ]
  
  gc()
  
  ## Calculate passive within-month gains (calc in place) 
  setkeyv(crspdret, c('permno','yyyymm')) # hopefully this speeds up the passive gain calc
  crspdret = crspdret[
    , passgain := shift(ret, fill=0, type='lag'), by = c('permno','yyyymm')
  ][
    , passgain := cumprod(1+passgain/100), by=c('permno','yyyymm')
  ] 
  
  # merge on last month's lagged me for fast (monthly-rebalanced) value-weighting
  # other monthly info (e.g. exchcd) is used only in port assignments
  templag = read_fst(
    paste0(pathProject,'Portfolios/Data/Intermediate/crspminfo.fst')
    , columns = c('permno','yyyymm','me')
  ) %>% 
    setDT() %>%
    mutate(
      yyyymm = yyyymm + 1
      , yyyymm = if_else(yyyymm %% 100 == 13, yyyymm+100-12,yyyymm)
    ) %>%
    transmute(permno, yyyymm, melag = me)
  setkeyv(templag, c('permno','yyyymm'))
  
  # left join update by reference
  crspdret[templag, on = c('permno','yyyymm'), melag := i.melag]
  
  # write to disk
  write_fst(crspdret, paste0(pathProject,'Portfolios/Data/Intermediate/crspdret.fst'))
  
}


rm(list=ls(pattern='crsp'))
