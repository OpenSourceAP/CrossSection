# For making FF1993 style factors from individual csvs on gdrive
# Andrew 2021 05

# FF1993 style is based on WRDS:
# https://wrds-www.wharton.upenn.edu/pages/support/applications/risk-factors-and-industry-benchmarks/fama-french-factors/

# Load packages (Maybe some need to be added to 0_SettingsAndTools)
library(tidyverse)
library(data.table)
library(googledrive)
library(getPass)
library(RPostgres)
library(dint)

###############
# Environment #
###############

# Root of April 2021 release on Gdrive
pathRelease = 'https://drive.google.com/drive/folders/1I6nMmo8k_zGCcp9tUvmMedKTAkb9734R'
url_prefix = 'https://drive.google.com/uc?export=download&id='

strategylist0 <- alldocumentation %>% 
  filter(Cat.Signal == "Predictor") %>%
  filter(Cat.Form == 'continuous')

#############
# CRSP Data #
#############

# login to wrds
user = getPass('wrds username: ')
pass = getPass('wrds password: ')

# Connect to WRDS database
wrds = dbConnect(
  Postgres()
  , host='wrds-pgdata.wharton.upenn.edu'
  , port=9737
  , dbname='wrds'
  , user=user
  , password=pass
  , sslmode='require'
)

# Write query
q <- "select a.permno, a.permco, a.date, a.ret, a.retx, a.vol, a.shrout, a.prc, a.cfacshr, a.bidlo, a.askhi,
      b.shrcd, b.exchcd, b.siccd, b.ticker, b.shrcls,  -- from identifying info table
      c.dlstcd, c.dlret                                -- from delistings table
      from crsp.msf as a
      left join crsp.msenames as b
      on a.permno=b.permno
      and b.namedt<=a.date
      and a.date<=b.nameendt
      left join crsp.msedelist as c
      on a.permno=c.permno
      and date_trunc('month', a.date) = date_trunc('month', c.dlstdt)
      "

# Submit query and fetch results
# Follows in part: https://wrds-www.wharton.upenn.edu/pages/support/research-wrds/macros/wrds-macro-crspmerge/
crspraw = dbSendQuery(conn = wrds, statement = q) %>%
  dbFetch(n = -1) %>%
  setDT()

# Incorporate delisting return (follows WRDS)
crsp = crspraw %>%
  mutate(
    dlret = if_else(is.na(dlret), 0, dlret)
    , ret = ret + dlret
    , ret = ifelse(is.na(ret) & ( dlret != 0), dlret, ret)
  ) %>% 
  # convert ret to pct, other formatting
  mutate(
    ret = 100 * ret
    , date = as.Date(date)
    , me = abs(prc) * shrout
    , yyyymm = year(date) * 100 + month(date)
  )

###########################
# Connect to Google Drive #
###########################

# Connect to Google Drive. This prompts a login.
target_dribble = pathRelease %>% drive_ls() %>% 
  filter(name == 'Firm Level Characteristics') %>%  drive_ls() %>% 
  filter(name == 'Individual') %>%  drive_ls() %>% 
  filter(name == 'Predictors') %>%  drive_ls() %>% 
  rename(signalname = name) %>% 
  arrange(signalname)

# Remove csv extension
target_dribble$signalname = gsub(".csv", "", target_dribble$signalname)

# We only care about continuous signals for the 2x3 portfolios
target_dribble <- semi_join(target_dribble, strategylistcts, by = "signalname")

# Get the number of signals available in Google Drive folder.
num_signals = nrow(target_dribble)

##################
# 2x3 Portfolios #
##################

# Initialize location in memory to store results
port <- NULL
# Loop over the signals
for(s in 1:num_signals){
  
  # Get signal name
  signal_name = target_dribble$signalname[s]
  
  print(paste0("Processing Signal No. ", s, " ===> ", signal_name))
  
  # Download data
  signal = fread(
    paste0(url_prefix, target_dribble$id[s])
  ) %>% 
    rename(signal = !!signal_name)
  
  # ==== ASSIGN TO 2X3 PORTFOLIOS ====
  
  # Keep value of signal corresponding to June.
  # Full join to keep as many market equity observations
  # as possible (FF1993, page 8)
  signaljune = signal %>% 
    filter(yyyymm %% 100 == 6) %>% 
    full_join(
      crsp %>% 
        filter(yyyymm %% 100 == 6) %>%  
        select(permno, yyyymm, me, exchcd, shrcd)
      , by = c('permno','yyyymm')
    )
  
  # For NYSE subset, compute signal quantiles for high and low
  # as well as median ME. FF93 is unclear about the shrcd screen
  # here, but WRDS does it
  nysebreaks = signaljune %>% 
    filter(exchcd == 1, shrcd %in% c(10, 11)) %>%
    group_by(yyyymm) %>% 
    summarise(
      qsignal_l = quantile(signal, 0.3, na.rm = T)
      , qsignal_h = quantile(signal, 0.7, na.rm = T)
      , qme_mid = quantile(me, 0.5, na.rm = T)
    )
  
  # Only exchcd in (1,2,3), shrcd in (10,11), (FF1993 p8-9)
  # We already exclude negative BE
  port6 = signaljune %>% 
    filter(
      exchcd %in% c(1, 2, 3)
      , shrcd %in% c(10, 11)
    ) %>% 
    left_join(nysebreaks, by = c('yyyymm')) %>% 
    mutate(
      q_signal = case_when(
        signal <= qsignal_l ~ 'L'
        , signal <= qsignal_h ~ 'M'
        , signal > qsignal_h ~ 'H'
      )
      , q_me = case_when(
        me <= qme_mid ~ 'S'
        , me > qme_mid ~ 'B'
      )
      , port6 = paste0(q_me, q_signal)
    ) %>% 
    select(
      permno, yyyymm, port6, signal
    )
  
  # ==== FIND MONTHLY FACTOR RETURNS ====
  
  # Find VW returns, signal lag, and number of firms
  # for a given portfolio
  port6ret = crsp %>% 
    select(permno, yyyymm, ret, me) %>% 
    left_join(port6, by = c('permno', 'yyyymm')) %>% 
    # Fill and lag 
    group_by(permno) %>% 
    arrange(permno, yyyymm) %>% 
    fill(port6) %>% 
    fill(signal) %>% 
    mutate(
      port6_lag = lag(port6)
      , signal_lag = lag(signal)
      , me_lag = lag(me)
    ) %>% 
    filter(!is.na(me_lag)) %>% 
    # Find value-weighted returns and signal by port6_lag month
    group_by(port6_lag, yyyymm) %>% 
    summarize(
      ret_vw = weighted.mean(ret, me_lag, na.rm = TRUE)
      , signallag = weighted.mean(signal_lag, me_lag, na.rm = TRUE)
      , n_firms = n()
    ) %>% 
    ungroup() %>% 
    # Organize and mutate columns
    rename(
      port = port6_lag
      , ret = ret_vw
      , Nlong = n_firms
    ) %>% 
    mutate(
      signalname = !!signal_name
      , date = last_of_month(as.Date(paste0(as.character(yyyymm), "01"), format = "%Y%m%d"))
      , Nshort = 0L
    ) %>% 
    filter(port %in% c("SL", "SM", "SH", "BL", "BM", "BH")) %>% 
    select(signalname, port, date, ret, signallag, Nlong, Nshort)
  
  # Equal-weight extreme portfolios to make FF1993-style factor
  ff93style_ret = port6ret[,c("port", "date", "ret")] %>% 
    pivot_wider(
      names_from = port, values_from = ret
    ) %>% 
    mutate(
      ret = 0.5*(SH + BH) - 0.5*(SL + BL)
    ) %>% 
    select(date, ret)
  
  # Get number of firms in long-short stocks
  ff93style_N = port6ret[,c("port", "date", "Nlong")] %>% 
    pivot_wider(
      names_from = port, values_from = Nlong
    ) %>% 
    mutate(
      Nlong = SH + BH
      , Nshort = SL + BL
    ) %>% 
    select(date, Nlong, Nshort)
  
  ff93style <- merge(ff93style_ret, ff93style_N, by = "date") %>% 
    mutate(
      signalname = !!signal_name
      , port = "LS"
      , signallag = NA
      , Nshort = if_else(is.na(ret), NA_integer_, Nshort)
      , Nlong = if_else(is.na(ret), NA_integer_, Nlong)
    ) %>%
    select(signalname, port, date, ret, signallag, Nlong, Nshort)
  
  # Append LS portfolios to 2x3 portfolios dataframe and sort  
  df <- rbind(port6ret, ff93style) %>% 
    mutate(
      port = factor(
        port, 
        levels = c("SL", "SM", "SH", "BL", "BM", "BH", "LS")
      )
    ) %>% 
    arrange(port, date)
  
  port <- rbind(port, df)
  
}

rm(
  crsp, crspraw, df, ff93style, ff93style_N, ff93style_ret,
  num_signals, nysebreaks, pass, pathRelease, port6, q, signal,
  signal_name, signaljune, strategylist0, url_prefix, user,
  wrds, port6ret, s
)

writestandard(
  port,
  pathDataPortfolios,
  paste0("Predictor2x3Ports.csv")
)
