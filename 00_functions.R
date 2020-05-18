# Function used in portfolio constructions

balanced_matrix = function(data,varname,keys) {
  
  data = data %>% rename(value = varname)
  
  ## append long data to get all rebdate-permno combinations
  
  # find missing permnos and missing dates
  temppermno = setdiff(keys$allpermno,unique(data$permno))
  tempdate   = as.Date(setdiff(keys$alldate,unique(data$date)),origin = "1970-01-01")
  
  # fix special case where there is nothing to add
  if (length(temppermno) == 0){
    temppermno = keys$allpermno[1]
  }  
  if (length(tempdate) == 0){
    tempdate = keys$alldate[1]
  }  
  
  # add to long data
  tempcomb = expand.grid(temppermno,tempdate) %>% rename(permno = Var1, date = Var2)
  if ( dim(tempcomb)[1] > 0 ){
    tempcomb$value = NA
    data2 = rbind(data,tempcomb)
  } else {
    data2 = data
  }
  
  ## this takes a lot of time
  # tempwide1 = data2 %>% spread(permno,value)
  tempwide1 = dcast(data2 %>% as.data.table, date ~ permno, value.var = "value") %>%
    as.data.frame() # dcast is faster than spread by about 3x
  
  # clean up
  wide = tempwide1[,-1] %>% as.matrix()
  row.names(wide) = as.character(tempwide1$date)
  return(wide)
}

## calculates portfolio returns.  wide contains a bunch of balanced matricies with "supporting" info.  wide_signal is one balanced matrix with signal data.
portfolio_returns = function(
  user,
  keys,
  wide,
  wide_signal
) {
  
  print("calculating portfolio")
  
  ## rebalancing indicator matrix
  # note: in principle can include staggered rebalancing here
  
  # create logical vector 1 = rebalance
  tfirst = min(which(month(keys$alldate) == user$startingmonth))  
  temp = data.frame(
    date = keys$alldate
    ,t = seq(1,keys$Ndate,1)
  ) %>% mutate( reb = (t-tfirst)%%user$holdper == 0 )
  reb = temp$reb  
  
  ## check for continuity and force if necessary
  if (!is.na(user$q_cut)){    
    qcheck = quantile(wide_signal,seq(0,1,0.25),na.rm=T) %>% unique() %>% abs() %>% sort()
    
    if (length(qcheck) == 2){
      if (all(qcheck == c(0,1))){
        print("portfolio_returns warning: requested q_cut but signal is binary")
        print("forcing q_cut = na")
        user$q_cut = NA
      }
    }
  }
  
  
  ## calculate enter / hold cutoffs
  signal_for_break = wide_signal
  if (user$nyse_q){
      signal_for_break[wide$nyse == 0] = NA
  } # if (user$nyse_q)
  
  if (!is.na(user$q_cut)){
    
    q_enter = user$q_cut
    q_hold  = user$q_cut + user$q_spread
    
    tempq = apply(
      signal_for_break, 1, quantile
      , probs = c(0, q_enter, q_hold, 1-q_hold, 1-q_enter, 1)
      , na.rm=TRUE
    ) %>% t()
    
    cutoff = data.frame(
      min = tempq[,1]
      ,s_enter = tempq[,2]
      ,s_hold = tempq[,3]
      ,l_enter = tempq[,4]
      ,l_hold = tempq[,5]      
      , max = tempq[,6]
    )
    
  } else {
    
    ## discrete cutoff is just 0.5 or -0.5
    ## no buy-hold spread for discrete
    tempq = apply(
      signal_for_break, 1, quantile, probs = c(0, 1), na.rm=TRUE
    ) %>% t()
    
    tempcut = user$Sign*0.5
    
    cutoff = data.frame(
      min = tempq[,1]
      ,s_enter = array(tempcut, dim(wide$ret)[1])
      ,s_hold = array(tempcut, dim(wide$ret)[1])
      ,l_enter = array(tempcut, dim(wide$ret)[1])
      ,l_hold = array(tempcut, dim(wide$ret)[1])
      , max = tempq[,2]
    )      
    
  } # !is.na(user$q_cut)
  
  rm(signal_for_break, tempq)
  
  ### TRACK PORTFOLIO MONTH BY MONTH ###
  rm(list=ls(pattern="temp"))
  
  print("recursively updating weights")
  # this takes 80% of the time
  # weights are end-of-month
   
  
  ## determine first month that has any position
  anylong  = cutoff$max >= cutoff$l_enter
  anyshort = cutoff$min <= cutoff$l_enter
  anyls    = anylong & anyshort
  
  switch(as.character(user$ls_sign),
         "1" = {anyenter = anylong},
         "-1" = {anyenter = anyshort},
         "0" = {anyenter = anyls}
  ) # switch user$ls_sign
    
  # begin with first month that has rebalancing and 1 enter signal
  tfirst = min(which(
    anyenter & reb
  ))
    
  # error checking
  if (!is.finite(tfirst)){
      print('error: tfirst is not finite')
      print('this probably means there are no enter signals anywhere')
      print('returning empty data frame')
      port = data.frame()
      return(port)
      
      stop()
  }      
  
  
  ## initialize 
  portret = array(NA, dim(wide$ret)[1])
  portcost = array(NA, dim(wide$ret)[1])
  portturn = array(NA, dim(wide$ret)[1])
  portNlong = array(NA, dim(wide$ret)[1])
  portNshort = array(NA, dim(wide$ret)[1])        
  portNstocks = array(NA, dim(wide$ret)[1])
  
  
  t = tfirst
  l_enter = wide_signal[t,] >= cutoff$l_enter[t]
  s_enter = wide_signal[t,] <= cutoff$s_enter[t]
  l_id_lag = which(l_enter)    
  s_id_lag = which(s_enter)
  
  wlag = array(NA, keys$Npermno)
  switch(as.character(user$ls_sign),
         "1" = {wlag[l_id_lag] = 1},
         "-1" = {wlag[s_id_lag] = -1},
         "0" = {
           wlag[l_id_lag] = 1
           wlag[s_id_lag] = -1
           wlag[intersect(l_id_lag,s_id_lag)] = 0 # this ensures no stock is in both legs
         } 
  ) # switch user$ls_sign
  
  if (user$weight_me){
    wlag = wlag*wide$me[t,]
  }
  
  
  wlag[l_id_lag] = wlag[l_id_lag]/abs(sum(wlag[l_id_lag]))
  wlag[s_id_lag] = wlag[s_id_lag]/abs(sum(wlag[s_id_lag]))
    
  
  ## recursively update weights
  for ( t in seq(tfirst+1,dim(wide$ret)[1]) ){
    
    # calculate port return for month t
    # AC: if ret[t,i] is missing but wlag[i] != 0,
    # we  implicitly assume that the
    # money in stock i is held in cash (no return, so the
    # stock delisted in the middle of t-1, and so we should have ended up
    # finding no stock to buy at the end of t-1
    # I think the more common assumption is that the stock is sold
    # and redistributed to the rest of the portfolio, but that's
    # more complicated and harder to code in this matrix format
    portret[t] =   sum(wlag*wide$ret[t,], na.rm=T)
    
    # passive is just last month's weights times 1+sign*wide$ret
    # this assumes if the return is missing,
    # the passive portfolio does not invest in it
    # this is needed for calculating trading costs
    wpass = wlag*(1+sign(wlag)*wide$ret[t,]/100)
    wpass[l_id_lag] = wpass[l_id_lag]/abs(sum(wpass[l_id_lag],na.rm=T))
    wpass[s_id_lag] = wpass[s_id_lag]/abs(sum(wpass[s_id_lag],na.rm=T))
    
    if (reb[t]) {
      ## here we rebalance
      
      # enter / hold        
      l_enter = wide_signal[t,] >= cutoff$l_enter[t]
      l_hold = (wlag!=0) & (wide_signal[t,]  >= cutoff$l_hold[t])
      l_id = which(l_enter | l_hold)
      
      s_enter = wide_signal[t,] <= cutoff$s_enter[t]
      s_hold = (wlag!=0) & (wide_signal[t,]  <= cutoff$s_hold[t])
      s_id = which(s_enter | s_hold)
      
      w = array(NA, keys$Npermno)
      switch(as.character(user$ls_sign),
             "1" = {w[l_id] = 1},
             "-1" = {w[s_id] = -1},
             "0" = {
               w[l_id] = 1
               w[s_id] = -1
               w[intersect(l_id,s_id)] = 0 # this ensures no stock is in both legs
             } 
      ) # switch user$ls_sign       
      # stock weighting
      if (user$weight_me){
        w = w*wide$me[t,]
      } # if (user$weight_me)
      # finally, normalize
      w[l_id] = w[l_id]/abs(sum(w[l_id]))
      w[s_id] = w[s_id]/abs(sum(w[s_id]))
      
    } else {
      ## here we're passive, but we actually do a mini-rebalance
      ## to have the same weights as we had when we last took on
      ## signals (real rebalance
      w = wlag
      l_id = which(w>0)
      s_id = which(w<0)  
    } # end if reb[t] 
    
    ## fix rare case of no enter signals (despite there having been enter signals earlier)
    if (sum(!is.na(w))==0){
      w = wlag
      l_id = which(w>0)
      s_id = which(w<0)        
    }
    
    # trading costs
    ## note this is 2-sided turnover, not the 1-sided turnover reported in Novy-Marx and Velikov 2015
    ## To get 1-sided turnover, just divide 2-sided turnover by 2
    ## 2-sided turnover example: suppose w = $[1 -1] and w_pass = $[-1 1].  Then you had to
    ## trade $2 worth of stock 1 and $2 worth of stock 2, for $4 of trades.  Most people would call
    ## this 100% turnover of each leg, or 200% turnover of both legs
    
    temptrade = (w %>% replace_na(0)) - (wpass %>% replace_na(0))      
    portcost[t] = sum(abs(temptrade)*wide$cost[t,],na.rm=T)
    portturn[t] = 100*sum(abs(temptrade)/2,na.rm=T)
    portNlong[t] = length(l_id)
    portNshort[t] = length(s_id)
    portNstocks[t] = portNlong[t] + portNshort[t]
    
    # update for next time
    wlag = w
    l_id_lag = l_id
    s_id_lag = s_id
    
  } # for t
  
  ## replace returns with NA if no stocks
  switch(as.character(user$ls_sign),
         "1" = {noport = (portNlong == 0)},
         "-1" = {noport = (portNshort == 0)},
         "0" = {noport = (portNlong == 0) | (portNshort==0)} 
  ) # switch user$ls_sign
  portret[noport] = NA
  portcost[noport] = NA
  portturn[noport] = NA        
  
  # store
  port = data.frame(
    date = rownames(wide$ret)
    ,return = portret
    ,cost   = portcost
    ,turn2sided = portturn # note: this is 2-sided turnover in pct
    ,Nlong  = portNlong
    ,Nshort = portNshort
    ,Nstocks = portNstocks
  ) %>% filter(!is.na(return))
  
  return(port)
  
  
} # end function



many_ports_longlist = function(
  longlist
  , keys
  , wide  
  , signalPath
  , customscreen = NULL
) {
  
  ## longlist is a long list of settings, with q_cut, q_spread, etc listed for each signal
  ## The intention is to read in settings from a spreadsheet
  
  default = list(
    ls_sign = 0
    ,q_cut   = 0.2
    ,q_spread  = 0
    ,nyse_q = F
    ,weight_me = F
    ,holdper  = 1
    ,startingmonth = 6
    ,FilterPrice = NA
    ,FilterExchange = NA
    ,Sign = 1
  )
  
  
  
  ## fill out longlist with defaults
  longlistfull = longlist
  for (tempname in names(default)){
    if ( !tempname %in% colnames(longlistfull)){
      longlistfull[[tempname]] = default[[tempname]]
    }
  }
  longlistfull$weight_me = replace_na(longlistfull$weight_me, 0)       
  longlistfull$FilterPrice = replace_na(longlistfull$FilterPrice, 0)
  longlistfull$FilterExchange = replace_na(longlistfull$FilterExchange, '1;2;3')    
  longlistfull$Sign = replace_na(longlistfull$Sign, 1)    
  
  
  ## loop over portfolios
  
  allport = tibble() 
  for (porti in seq(1,dim(longlistfull)[1])) {
    
    
    ## focus on one signal from big dataset
    print("reading big signal-firm-month data")
    onesignal = read_feather(paste0(signalPath, 'temp.feather'),
                             columns = c("permno","date",longlist$signalname[porti],"prc","exchcd")) %>% 
      rename(signalcurr = longlist$signalname[porti]) %>%
      filter(!(is.na(signalcurr)))
      
    
    ## apply filters and sign
    tempexchlist = strsplit(longlistfull$FilterExchange[porti],";") %>%
      unlist() %>% as.character() %>% as.numeric()     
    
    onesignal = onesignal %>%
      mutate(
        signalcurr = ifelse(abs(prc) > longlistfull$FilterPrice[porti], signalcurr, NA)
        ,signalcurr = ifelse(exchcd %in% tempexchlist, signalcurr, NA)
        ,signalcurr = longlistfull$Sign[porti]*signalcurr                
      )

      if (!is.null(customscreen)){
          onesignal = onesignal %>%
              left_join(customscreen, by=c('permno','date')) %>%
              mutate(
                  signalcurr = ifelse(keep, signalcurr, NA)
              )
      } # if !is.null(customscreen)
      
    ## clean up
    onesignal = onesignal %>% select(permno, date, signalcurr) %>%
      filter(!is.na(signalcurr))
    
    print("turning long signal data to wide_signal")
    start_time <- Sys.time()      
    wide_signal = balanced_matrix(onesignal,"signalcurr",keys)    
    end_time <- Sys.time()
    print(end_time - start_time)
    
    rm(onesignal)      
    
    
    # compile portfolio settings
    portset = longlistfull[porti,] %>% as.list
    
    # feedback
    print("many_ports_longlist ==============  ")
    print(paste0("porti = ",porti))
    print(as.data.frame(portset))      
    start_time <- Sys.time()
    
    
    
    # calculate portfolio
    tempport = portfolio_returns(
      portset
      ,keys
      ,wide
      ,wide_signal
    )
      
  
      if (dim(tempport)[1]>0){

          # feedback
          print("full sample stats:")
          tempport %>% filter(!is.na(return)) %>%
              summarize(
                  ret = mean(return)
                , tstat = mean(return)/sd(return)*sqrt(n())
                , cost = mean(cost)) %>%
              print()

          # add portfolio info and clean up        
          tempport$signalname    = portset$signalname
          tempport$ls_sign       = portset$ls_sign
          tempport$q_cut         = portset$q_cut
          tempport$q_spread      = portset$q_spread
          tempport$nyse_q     = portset$nyse_q
          tempport$weight_me     = portset$weight_me
          tempport$holdper = portset$holdper              
          tempport = tempport %>% filter(!is.na(return))
      } else {
          tempport = data.frame()
      }                          
    
    # append to big dataset
    allport = rbind(allport,tempport)
    
    end_time <- Sys.time()
    print(end_time - start_time)
    
    
    rm(wide_signal, tempport)
    
    
  } # for porti
  
  
  tempnet   = allport %>% mutate(return = return - cost, rettype = 'net')
  tempgross = allport %>% mutate(rettype = 'gross')
  allport   = rbind(tempnet,tempgross)    
  
  return(allport)  
} # --- end function  



## prep_matricies computes a bunch of stuff related to portfolio calculation that can be done outside of the big loop.  It mostly puts long data into wide format
prep_matricies = function(
  signal
  , signalMetadata
  , cost0
  , anomalyNames
){
  
  # initialize final output
  wide = list()
  
  # grab return0, me0, nyse0
  return0 = signalMetadata %>% 
    transmute(permno, date, ret = 100*ret) 
  
  me0 = signalMetadata %>% 
    transmute(permno, date, mve_c)  
  
  nyse0 = signalMetadata %>%
    transmute(permno, date, NYSE = exchcd == 1)
  
  
  ### MAKE MATRICIES FOR ME, COST, RETURNS ###
  
  # data structure info
  keys = list()
  keys$allpermno = unique(signalMetadata$permno) %>% sort()
  keys$alldate = unique(signalMetadata$date) %>% sort()
  keys$Npermno = length(keys$allpermno)
  keys$Ndate   = length(keys$alldate)
  
  keys$allsignal = colnames(signal)[colnames(signal) %in% anomalyNames] %>% 
    sort()
  keys$Nsignal = length(keys$allsignal)
  # store
  wide$keys = keys
  
  # keep only permno-dates that match signals
  return0 = return0 %>% filter(permno %in% keys$allpermno, date %in% keys$alldate)
  me0 = me0 %>% filter(permno %in% keys$allpermno, date %in% keys$alldate)
  cost0 = cost0 %>% filter(permno %in% keys$allpermno, date %in% keys$alldate)
  nyse0 = nyse0 %>% filter(permno %in% keys$allpermno, date %in% keys$alldate)
  
  wide$me   = balanced_matrix(me0, "mve_c", keys)
  wide$cost = balanced_matrix(cost0, "half_spread", keys)
  wide$ret  = balanced_matrix(return0, "ret", keys)
  wide$nyse   = balanced_matrix(nyse0, "NYSE", keys)
  
  return(wide)
} # -- end function


#### memory management stuff ####
# improved list of objects
.ls.objects <- function (pos = 1, pattern, order.by,
                         decreasing=FALSE, head=FALSE, n=5) {
  napply <- function(names, fn) sapply(names, function(x)
    fn(get(x, pos = pos)))
  names <- ls(pos = pos, pattern = pattern)
  obj.class <- napply(names, function(x) as.character(class(x))[1])
  obj.mode <- napply(names, mode)
  obj.type <- ifelse(is.na(obj.class), obj.mode, obj.class)
  obj.prettysize <- napply(names, function(x) {
    format(utils::object.size(x), units = "auto") })
  obj.size <- napply(names, object.size)
  obj.dim <- t(napply(names, function(x)
    as.numeric(dim(x))[1:2]))
  vec <- is.na(obj.dim)[, 1] & (obj.type != "function")
  obj.dim[vec, 1] <- napply(names, length)[vec]
  out <- data.frame(obj.type, obj.size, obj.prettysize, obj.dim)
  names(out) <- c("Type", "Size", "PrettySize", "Length/Rows", "Columns")
  if (!missing(order.by))
    out <- out[order(out[[order.by]], decreasing=decreasing), ]
  if (head)
    out <- head(out, n)
  out
}

# shorthand
lsos <- function(..., n=10) {
  .ls.objects(..., order.by="Size", decreasing=TRUE, head=TRUE, n=n)
}
