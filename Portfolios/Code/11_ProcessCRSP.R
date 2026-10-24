# Processes the CRSP v2 (CIZ) parquet files written by Signals/pyCode into the
# intermediate files used by the portfolio code.
#
# Inputs (Signals/pyData/Intermediate/, from DataDownloads/CRSPMonthly.py and CRSPDaily.py,
#         or from Signals/pyCode/crsp_only.py):
#   monthlyCRSP.parquet
#   dailyCRSP.parquet (only if !skipdaily)
# Outputs (Portfolios/Data/Intermediate/):
#   crspmret.fst   permno, date (month-end trading date), yyyymm, ret (pct), melag
#   crspminfo.fst  permno, yyyymm, prc, exchcd, me (millions), shrcd, me_nyse10, me_nyse20
#   crspdret.fst   permno, date, yyyymm, ret (pct), passgain, melag (only if !skipdaily)
#
# Returns are taken as they come from CIZ: mthret already includes the delisting
# return where CRSP has one (mthdelflg A, P, V). The legacy -35%/-55% imputation
# for missing delisting returns is not applied. See Docs/CRSP-v2-Migration.md.
# 2021 04, migrated to CRSP v2 2026 10


# ==== MONTHLY CRSP SETUP ==== 
crspm = arrow::read_parquet(paste0(pathSignalsIntermediate, 'monthlyCRSP.parquet')) %>%
  as_tibble()

# date: the month's last trading date (mthcaldt), as in legacy msf.date, so that
# portfolio output keeps month-end dates. Parquet files written before 2026-10
# lack this column; fall back to the last calendar day of the month.
if (!'date' %in% colnames(crspm)) {
  print('monthlyCRSP.parquet has no date column (older download); using last calendar day of month')
  crspm$date = ceiling_date(as.Date(crspm$time_avail_m), 'month') - days(1)
}

# convert ret to pct, other formatting
# me is in millions of dollars (mve_c); the legacy portfolio code had it in
# thousands. Downstream uses are relative only (breakpoints, weights, screens).
# arrow reads time_avail_m as a POSIXct in the session's local timezone, so
# month() on it gives the previous month west of UTC. as.Date() converts in UTC.
crspm = crspm %>%
  transmute(
    permno = as.integer(permno)
    , date = as.Date(date)
    , yyyymm = year(as.Date(time_avail_m)) * 100 + month(as.Date(time_avail_m))
    , ret = 100*ret
    , prc
    , exchcd
    , shrcd
    , me = mve_c
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
write_fst(crspmret, paste0(pathDataIntermediate, 'crspmret.fst'))
write_fst(crspminfo, paste0(pathDataIntermediate, 'crspminfo.fst'))

## clean up
# Remove only this script's data objects: pattern-based rm() also deleted
# globals such as pathtemp, crsp_predictors and check_crsp_inputs.
rm(crspm, crspmret, crspminfo, templag, tempcut)


# ==== DAILY CRSP SETUP ====
if (!skipdaily){
  
  # unlike monthly crsp, we try to do this in place for memory mgmt
  # dailyCRSP.parquet holds regular trading days only; CIZ's separate
  # delisting-event rows are excluded (see DataDownloads/CRSPDaily.py)
  crspdret = arrow::read_parquet(
    paste0(pathSignalsIntermediate, 'dailyCRSP.parquet')
    , col_select = c('permno', 'time_d', 'ret')
  ) %>% setDT()
  
  # drop na, reformat 
  crspdret = crspdret[
    !is.na(ret)  
  ][
    , ':=' (
      permno = as.integer(permno)
      , ret = 100*ret
      , date = as.Date(time_d)
    )
  ][
    , time_d := NULL
  ][
    , yyyymm := year(date)*100+month(date)
  ][
    order(permno,date)
  ]
  
  gc()
  
  ## Calculate passive within-month gains (calc in place) 
  setkeyv(crspdret, c('permno','yyyymm')) # hopefully this speeds up the passive gain calc
  crspdret = crspdret[
    , passgain := data.table::shift(ret, fill=0, type='lag'), by = c('permno','yyyymm')
  ][
    , passgain := cumprod(1+passgain/100), by=c('permno','yyyymm')
  ] 
  
  # merge on last month's lagged me for fast (monthly-rebalanced) value-weighting
  # other monthly info (e.g. exchcd) is used only in port assignments
  templag = read_fst(
    paste0(pathDataIntermediate, 'crspminfo.fst')
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
  setcolorder(crspdret, c('permno','date','ret','yyyymm','passgain','melag'))
  write_fst(crspdret, paste0(pathDataIntermediate, 'crspdret.fst'))
  
}


if (!skipdaily) rm(crspdret, templag)
