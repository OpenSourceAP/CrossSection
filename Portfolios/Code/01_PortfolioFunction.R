#### FUNCTION FOR TURNING SIGNAL CSV TO K PORTFOLIOS
# this is mostly one big function.  It's so big, it needs its own file otherwise
# I get lost.


import_signal = function(signalname,filterstr,Sign){
  # this is useful to have outside of signalname_to_longports in case
  # you just want to look at the signals
  
  ### LOAD SIGNAL DATA AND APPLY FILTERS
  if (file.exists(paste0(pathPredictors,signalname,'.csv'))){
    csvname = paste0(pathPredictors,signalname,'.csv')
  } else if (file.exists(paste0(pathCRSPPredictors,signalname,'.csv'))){
    csvname = paste0(pathCRSPPredictors,signalname,'.csv')                
  } else if (file.exists(paste0(pathPlacebos,signalname,'.csv'))){
    csvname = paste0(pathPlacebos,signalname,'.csv')
  } else if (file.exists(paste0(pathtemp,signalname,'.csv'))){
    csvname = paste0(pathtemp,signalname,'.csv')                
  } else {
    print('error: signalname csv not found')
    stop('error: signalname csv not found')
  }
  
  ## load signal data 
  # previously had problems with fread and memory leaks, but seems like upgrading
  # R might have fixed it.
  signal = fread(csvname) %>%
    as_tibble() %>%
    rename(signal = !!signalname) %>%
    filter(!is.na(signal))    
  
  ## add crsp prc exchcd me for implementation adjustments
  # sometimes get the following error
  # Error: cons memory exhausted (limit reached?)
  # Error: no more error handlers available (recursive errors?); invoking 'abort' restart
  gc()
  signal = left_join(
    signal
    , crspinfo 
    , by = c('permno','yyyymm')
  )
  
  ## apply filters and sign
  # note the signal dataset is lagged further down, so
  # filtering here does not look ahead        
  if (!is.na(filterstr)){
    evalme = paste0('signal = signal %>% filter('
                    , filterstr
                    , ')')      
    eval(parse(text=evalme))        
  }
  
  ## sign
  signal$signal = signal$signal*Sign
  
  return(signal)
  
} # end sub function



# here's the big function
# the inner functions help with memory mgmt (no pass by value)
# while staying organized and allowing for extensions in the future
signalname_to_ports = function(
  signalname
  , Cat.Form = NA
  , q_cut = NA
  , sweight = NA
  , Sign = NA
  , longportname = NA
  , shortportname = NA
  , startmonth = NA
  , portperiod = NA
  , q_filt = NA
  , filterstr = NA
  , passive_gain = F
) {
  
  # SETTINGS AND CHECKS ====

  ## settings
  # we use NA as "function default" and then transform to real defaults here
  # to keep the all defaults in this important function.
  # Otherwise you need defaults in the loop over strategies function
  if (is.na(sweight)) {sweight = 'EW'}
  if (is.na(Sign)) {Sign = 1}
  if (is.na(longportname[1])) {longportname = 'max'}
  if (is.na(shortportname[1])) {shortportname = 'min'}    
  if (is.na(startmonth)) {startmonth = 6}
  if (is.na(portperiod)) {portperiod = 1}
  if (is.na(q_cut)) {q_cut=0.2}
  if (is.na(Cat.Form)) {Cat.Form = 'continuous'}    
  
  ## checks
  if (!exists('crspret')){
    print('error: crspret not in workspace.  Please load Intermediate/crspmret.fst or crspdret.fst as crspret (see 11_ProcessCRSP.R)')
    stop()
  }
  if (!exists('crspinfo')){
    print('error: crspinfo not in workspace.  Please load Intermediate/crspminfo.fst as crspinfo (see 11_ProcessCRSP.R)')
    stop()
  }
  if (passive_gain){
    if (!'passgain' %in% colnames(crspret)){
      print('error: passive_gain = T but crspret does not have a passgain column')
      print('please check the correct crspret is loaded')
      stop()
    }
  }
  if (sweight == 'VW'){
    if (!'melag' %in% colnames(crspret)){
      print('error: sweight == VW but crspret does not have melag column')
      print('please check crsp processing')
      stop()
    }
  }  
  
  # function for sorting portfolios if signal is not already a port assignment
  single_sort = function(q_filt,q_cut){
    ## create breakpoints
    # subset to firms used for breakpoints, right now only exclude based on q_filt
    tempbreak = signal
    if (!is.na(q_filt)) {
      if (q_filt=='NYSE'){
        tempbreak = tempbreak %>% filter(exchcd == 1)
      }
    } # if q_filt
    
    ## create breakpoints
    # turn q_cut into a vector carefully
    if (q_cut <= 1/3){
      plist = c(seq(q_cut,1-2*q_cut,q_cut), 1-q_cut)
    } else {
      plist = unique(c(q_cut,1-q_cut))
    }
    
    # find breakpoints 
    temp = list()
    for (pi in seq(1,length(plist))){
      temp[[pi]] = tempbreak %>% group_by(yyyymm) %>%
        summarize(
          breakpoint = quantile(signal, probs = plist[pi])
        ) %>%
        mutate(breaki = pi)
    } # for pi
    breaklist = do.call(rbind.data.frame, temp) %>%
      pivot_wider(
        names_from=breaki,
        values_from=breakpoint,
        names_prefix = 'break')
    
    # remove degenerate breakpoints (at extremes only)
    if (length(plist) > 1){
      idgood = breaklist[,length(plist)+1] - breaklist[,2] > 0
      breaklist = breaklist[idgood,]
    }
    
    ## assign to portfolios
    # the extreme portfolios get the 'benefit of the doubt' in the inequalities
    
    # initialize
    signal = signal %>%
      left_join(breaklist, by = 'yyyymm') %>%        
      mutate(port = NA_integer_) 
    
    # assign lowest signal
    signal = signal %>%
      mutate(port = if_else(signal <= break1, as.integer(1), port) )
    
    # assign middle
    if (length(plist) >= 2) {
      for (porti in seq(2,length(plist))){        
        breakstr = paste0('break',porti)
        id = is.na(signal$port) & (signal$signal < signal[breakstr])
        signal$port[id] = porti                        
      } # for porti
    }
    
    # assign highest signal
    breakstr = paste0('break',length(plist))
    id = is.na(signal$port) & (signal$signal >= signal[breakstr])
    signal$port[id] = length(plist) + as.integer(1)
    
    signal = signal %>% select(-starts_with('break'))
    
    return(signal)
    
  } ## end sub function
  
  # MAIN WORK ====
  
  # Import signal ====
  if (feed.verbose) {print('loading signal data and applying filters')}
  signal = import_signal(signalname,filterstr,Sign) 
  
  # Assign stocks to portfolios ====
  # (if necessary)
  if (feed.verbose) {print('assigning stocks to portfolios')}    
  
  if (Cat.Form == 'continuous'){
    signal = single_sort(q_filt,q_cut)        
    
  } else if (Cat.Form == 'discrete') {
    # for custom categorical portfolios (e.g. Gov Index, PS, MS)
    # by default we go long "largest" cat and short "smallest" cat      
    support =  signal$signal %>% unique %>% sort
    signal$port = NA_integer_
    for (i in 1:length(support)) {
      signal$port[signal$signal==support[i]] = i            
    }
    
  } else if (Cat.Form == 'custom'){
    # here we just say port = signal (port assigned in previous code)            
    # eventually useful for ff3 style, maybe
    signal = signal %>% mutate(port = signal)
  } # if Cat.Form
  
  # == Portfolio Returns (stock weighting happens here) ====
  # make all na except  "rebalancing months", which is actually signal updating months
  # and then fill na with stale data
  
  # find months that portfolio assignements are updated
  rebmonths =  (
    startmonth
    + seq(0,12)*portperiod
  ) %% 12
  rebmonths[rebmonths == 0] = 12
  rebmonths = sort(unique(rebmonths))
  
  signal =  signal %>%
    mutate(
      port = if_else(
        (yyyymm %% 100) %in% rebmonths
        , port
        , NA_integer_
      )
    ) %>%
    arrange(permno,yyyymm) %>%
    group_by(permno) %>%
    fill(port) %>%
    filter(!is.na(port))                   
  
  ### CREATE PORTFOLIOS
  # this can be slow with daily data, about 20 sec per signal

  ### ASSIGN TO PORTFOLIOS AND SIGN
  # lag signals: note port could by called portlag here
  signallag = setDT(signal)[
    , .(permno, yyyymm, signal, port)
  ][
    , yyyymm := yyyymm + 1
  ][
    , yyyymm := if_else(yyyymm %% 100 == 13, yyyymm+100-12,yyyymm)
  ]
  setnames(signallag, old = 'signal', new = 'signallag')  
  
  if (feed.verbose) {print('joining lagged signals onto crsp returns')}
  gc()
  # scoping implies crspret in the big loop is not affected
  crspret = crspret %>%
    left_join(
      signallag %>% select(permno,yyyymm,signallag, port)
      , by = c('permno','yyyymm')
    )

  ## stock weights
  # equal vs value-weighting
  if (sweight == 'VW'){
    crspret$weight = crspret$melag
  } else {
    crspret$weight = 1
  }    
  # adjustments for passive gains 
  # (this is only used for the daily ports right now)
  if (passive_gain){
    crspret$weight = crspret$weight*crspret$passgain
  }
  
  if (feed.verbose) {print('calculating portfolio returns')}
  port = crspret[
    !is.na(port) & !is.na(ret) & !is.na(weight)
  ][
    , .(
      ret = weighted.mean(ret, weight)
      , signallag = weighted.mean(signallag, weight)
      , Nlong = .N
    )
    , by = list(port,date)
  ]
  
  port = port %>%
    mutate(Nshort = 0) %>%
    select(port,date,ret,signallag,Nlong,Nshort) %>%
    ungroup()
  
  
  if (feed.verbose){
    print(paste0('end of signalname_to_ports memory used = '))
    print(mem_used())
  }    
  gc()
  if (feed.verbose){print(gc(T))}
  
  
  # Add long-short portfolio  ====       
  # allows for ff3 style with something like
  # longportname = c('SH','BH'), shortportname = c('SL','BL')
  # longportname and shortportname come from the function call to signalname_to_ports
  if (longportname[1] == 'max'){
    longportname = max(port$port)
  }
  if (shortportname[1] == 'min'){
    shortportname = min(port$port)
  }
  
  # equal-weight long portfolios
  long = port %>%
    filter(port %in% longportname) %>%
    group_by(date) %>%
    summarize(
      retL = mean(ret), Nlong = sum(Nlong)
    )
  
  short = port %>% 
    filter(port %in% shortportname) %>%
    group_by(date) %>%
    summarize(
      retS = - mean(ret), Nshort = sum(Nlong)
    )
  
  longshort = inner_join(long, short, by='date') %>%
    mutate(
      ret = retL + retS
      , port = 'LS'
      , signallag = NA_real_
    ) %>%
    select(port,date,ret,signallag,Nlong,Nshort)        
  
  
  # convert port to string and pad left if deciles for ease
  if (max(nchar(as.character(port$port %>% unique()))) == 1){
    port = port %>% mutate(port = sprintf('%01d',port))
  } else {
    port = port %>% mutate(port = sprintf('%02d',port))
  }
  
  # bind long with longshort
  port = rbind(port,longshort)
  
  # clean up
  port$signalname = signalname
  
  port = port %>% 
    select(signalname,everything()) %>%
    arrange(signalname,port,date)
  
  return(port)
  
} ### end function




