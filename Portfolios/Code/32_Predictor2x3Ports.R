# For making FF1993 style factors from individual csvs on gdrive
# Andrew 2021 05

# Made into loop 2022 03 

# FF1993 style is based on WRDS:
# https://wrds-www.wharton.upenn.edu/pages/support/applications/risk-factors-and-industry-benchmarks/fama-french-factors/

# ENVIRONMENT AND DATA ====
crspinfo = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspminfo.fst')
) %>% # me, screens, 
  setDT()
crspret = read.fst(
  paste0(pathProject,'Portfolios/Data/Intermediate/crspmret.fst')
) %>% # returns
  setDT()

# SELECT SIGNALS 
strategylist <- alldocumentation %>% filter(Cat.Signal == "Predictor") %>% 
  filter(Cat.Form == 'continuous')
strategylist <- ifquickrun()

# FUNCTION FOR CONVERTING SIGNALNAME TO 2X3 PORTS ====
# analogous to signalname_to_ports in 01_PortFolioFunction.R

signalname_to_2x3 = function(signalname){
  # Import signal and sign
  signal = import_signal(signalname, NA, strategylist$Sign[s])
  
  # ASSIGN TO 2X3 PORTFOLIOS 
  
  # Keep value of signal corresponding to June.
  # Full join to keep as many market equity observations
  # as possible (FF1993, page 8)
  signaljune = signal %>% 
    filter(yyyymm %% 100 == 6) 
  
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
  
  # FIND MONTHLY FACTOR RETURNS 
  
  # Find VW returns, signal lag, and number of firms
  # for a given portfolio
  port6ret = crspret %>% 
    select(permno, date, yyyymm, ret, melag) %>% 
    left_join(port6, by = c('permno', 'yyyymm')) %>% 
    # Fill and lag 
    group_by(permno) %>% 
    arrange(permno, yyyymm) %>% 
    fill(port6) %>% 
    fill(signal) %>% 
    mutate(
      port6_lag = lag(port6)
      , signal_lag = lag(signal)
    ) %>% 
    filter(!is.na(melag)) %>% 
    # Find value-weighted returns and signal by port6_lag month
    group_by(port6_lag, yyyymm) %>% 
    summarize(
      ret_vw = weighted.mean(ret, melag, na.rm = TRUE)
      , signallag = weighted.mean(signal_lag, melag, na.rm = TRUE)
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
      signalname = !!signalname
      , date = last_of_month(as.Date(paste0(as.character(yyyymm), "01"), format = "%Y%m%d"))
      , Nshort = 0L
    ) %>% 
    filter(port %in% c("SL", "SM", "SH", "BL", "BM", "BH")) %>% 
    select(signalname, port, date, ret, signallag, Nlong, Nshort)
  
  # Equal-weight extreme portfolios to make FF1993-style factor
  portls_ret = port6ret[,c("port", "date", "ret")] %>% 
    pivot_wider(
      names_from = port, values_from = ret
    ) %>% 
    mutate(
      ret = 0.5*(SH + BH) - 0.5*(SL + BL)
    ) %>% 
    select(date, ret)
  
  # Get number of firms in long-short stocks
  portls_N = port6ret[,c("port", "date", "Nlong")] %>% 
    pivot_wider(
      names_from = port, values_from = Nlong
    ) %>% 
    mutate(
      Nlong = SH + BH
      , Nshort = SL + BL
    ) %>% 
    select(date, Nlong, Nshort)
  
  # merge returns with number of firms and fill in LS info
  portls <- merge(portls_ret, portls_N, by = "date") %>% 
    mutate(
      signalname = !!signalname
      , port = "LS"
      , signallag = NA
      , Nshort = if_else(is.na(ret), NA_integer_, Nshort)
      , Nlong = if_else(is.na(ret), NA_integer_, Nlong)
    ) %>%
    select(signalname, port, date, ret, signallag, Nlong, Nshort)
  
  # Append LS portfolios to 2x3 portfolios dataframe and sort  
  port <- rbind(port6ret, portls) %>% 
    mutate(
      port = factor(
        port, 
        levels = c("SL", "SM", "SH", "BL", "BM", "BH", "LS")
      )
    ) %>% 
    arrange(port, date)  
  
  
} # end signalname_to_2x3

# LOOP OVER SIGNALS ====
num_signals = nrow(strategylist)
num_signals = 20

# Initialize location in memory to store results
allport = list()

# Loop over the signals
for(s in 1:num_signals){
  
  # Get signal name
  signalname = strategylist$signalname[s]
  
  print(paste0("Processing Signal No. ", s, " ===> ", signalname))
  
  tempport = tryCatch(
    {
      expr = signalname_to_2x3(
        signalname = strategylist$signalname[s]
      )
      
    }
    , error = function(e){
      print('error in signalname_to_2x3, returning df with NA')
      data.frame(
        matrix(ncol = dim(allport[[s-1]])[2], nrow = 1)
      ) 
    }
  ) # tryCatch
  
  # add column names if signalname_to_2x3 failed
  if (is.na(tempport[1,1])){
    colnames(tempport) = colnames(allport[[1]]) # assume strat 1 worked ok
    tempport$signalname = strategylist$signalname[1]
  }  
  
  allport[[s]] = tempport
  
} # for s in 1:num_signals


allport = do.call(rbind.data.frame, allport) 

# WRITE TO DISK  ====
writestandard(
  port,
  pathDataPortfolios,
  "PredictorAltPorts_FF93style.csv"
)

