#### GLOBAL SETTINGS

quickrun =  T# use T if you want to run quickly for testing
quickrunlist = c('BM','Mom12m')
feed.verbose = T # use T if you want lots of feedback

options(dplyr.summarise.inform = FALSE)

#### PATHS

pathProject = '/cm/chen/anomalies.com/cfr1/'
pathPredictors = paste0(pathProject, 'Signals/Data/Predictors/')
pathPlacebos = paste0(pathProject, 'Signals/Data/Placebos/')
pathCRSPPredictors = paste0(pathProject, 'Signals/Data/CRSPPredictors/')
pathtemp = paste0(pathProject, 'Signals/Data/temp/')

pathCode = paste0(pathProject, 'Portfolios/Code/')
pathDataIntermediate = paste0(pathProject, 'Portfolios/Data/Intermediate/')
pathDataPortfolios = paste0(pathProject, 'Portfolios/Data/Portfolios/')
pathDataSummary = paste0(pathProject, 'Portfolios/Data/Summary/')

pathResults = paste0(pathProject, 'Results/')

dir.create(paste0(pathDataPortfolios))
dir.create(paste0(pathDataIntermediate))
dir.create(paste0(pathCRSPPredictors))

#### PACKAGES

options(stringsAsFactors = FALSE)
library(tidyverse)
library(lubridate)
library(readxl)
library(writexl)
library(pryr)
library(fst)

# for WRDS access
library(RPostgres)
library(getPass)

#### FUNCTION FOR READING IN DOCUMENTATION

readdocumentation = function(){

    # little function for converting string NA into numeric NA
    as.num = function(x, na.strings = c("NA",'None','none')) {
        stopifnot(is.character(x))
        na = x %in% na.strings
        x[na] = 0
        x = as.numeric(x)
        x[na] = NA_real_
        x
    }
    
    ## load signal header
    temp1 = read_excel(
        paste0(pathProject, 'SignalDocumentation.xlsx')
      , sheet = 'BasicInfo'
    ) %>%
        rename(signalname = Acronym)  %>%
        select(-Authors) %>% 
        # Format order of category labels
        mutate(Cat.Data = as_factor(Cat.Data) %>% 
                   factor(levels = c('Accounting', 'Analyst', 'Event', 'Options', 'Price', 'Trading', '13F', 'Other'))) %>% 
        # Make economic category proper
        mutate(Cat.Economic = str_to_title(Cat.Economic)) %>%
        mutate(
            assignport = if_else(Cat.Form=='continuous',T,F)
        )
    
    temp2 = read_excel(
        paste0(pathProject, 'SignalDocumentation.xlsx')
      , sheet = 'AddInfo'
    ) %>% rename(
            signalname = Acronym
          , sweight = 'Stock Weight'
          , q_cut = 'LS Quantile'
          , q_filt = 'Quantile Filter'  
          , portper = 'Portfolio Period'
          , startmonth = 'Start Month'
          , filterstr = 'Filter'
        ) %>%
        mutate_at(
            c('q_cut','portper','startmonth')
            , .funs = as.num
            , 
        ) %>%
        mutate(
            filterstr = if_else(filterstr %in% c('NA','None','none')
              , NA_character_
              , filterstr)
        ) %>%
        select(-c(starts_with('Note')))
    
        
    # merge
    alldocumentation = temp1 %>% left_join(temp2, by="signalname") %>%
        arrange(signalname)
}

## run readdocumentaiton
alldocumentation = readdocumentation()

#### FUNCTION FOR TURNING SIGNAL CSV TO K PORTFOLIOS

signal_to_ports = function(
                            signalname
                           , assignport = T
                           , q_cut = NA
                           , sweight = NA
                           , Sign = NA
                           , startmonth = NA
                           , portper = NA
                           , q_filt = NA
                           , filterstr = NA
                            ) {
    
    ### IMPLEMENTATION DEFAULTS AND SETTINGS
    if (is.na(sweight)) {sweight = 'EW'}
    if (is.na(Sign)) {Sign = 1}
    if (is.na(startmonth)) {startmonth = 6}
    if (is.na(portper)) {portper = 1}
    if (is.na(q_cut)) {q_cut=0.2}
    

    
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

    if (feed.verbose) {print('loading signal data and applying filters')}
    ## load signal data 
    # about twice as fast as regular read.csv
    signal = read.table(
        csvname
      , header = T, sep = ',', quote = ""
      , stringsAsFactors = F, comment.char = ""
      , colClasses = c('integer','integer','numeric')
      , check.names = F
    ) %>%
        as_tibble() %>%
        rename(signal = !!signalname) %>%
        filter(!is.na(signal))
    
    ## add crsp prc exchcd me for implementation adjustments
    # sometimes get the follwoing error
    # Error: cons memory exhausted (limit reached?)
    # Error: no more error handlers available (recursive errors?); invoking 'abort' restart
    gc()
    signal = left_join(
        signal
      , crspinfo 
      , by = c('permno','yyyymm')
    )
    
    ## apply filters
    # note the signal dataset is lagged further down, so
    # filtering here does not look ahead        
    if (!is.na(filterstr)){
        evalme = paste0('signal = signal %>% filter('
                      , filterstr
                      , ')')      
        eval(parse(text=evalme))        
    }

    
    
    ### ASSIGN TO PORTOFOLIOS (INITIAL)
    temp0 = signal
    
    # implementation adjustments will be applied later
    # this is a verbose way to do this, but it's easier to dissect and debug 
    if (feed.verbose) {print('assigning stocks to portfolios')}
    
    if (assignport){
        
        ## create breakpoints        # subset to firms used for breakpoints, right now only exclude based on q_filt
        tempbreak = temp0
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

        ## assign to portfolios
        # the extreme portfolios get the 'benefit of the doubt' in the inequalities
        
        # initialize
        temp1 = temp0 %>%
            left_join(breaklist, by = 'yyyymm') %>%        
            mutate(port = NA_integer_) 

        # assign sequentially
        temp1 = temp1 %>%
            mutate(port = if_else(signal <= break1, as.integer(1), port) )

        if (length(plist) >= 2) {
            for (porti in seq(2,length(plist))){        
                breakstr = paste0('break',porti)
                id = is.na(temp1$port) & (temp1$signal < temp1[breakstr])
                temp1$port[id] = porti                        
            } # for porti
        }
        
        breakstr = paste0('break',length(plist))
        id = is.na(temp1$port) & (temp1$signal >= temp1[breakstr])
        temp1$port[id] = length(plist) + 1       
        

    } else {
        
        ## assignport == F
        # here we assume the signal is the port, and for now assume binary
        # binary signals are all 0 or 1, so to make ports
        # we just map this into 1 or 2
        temp1 = temp0 %>% mutate( port = signal + 1)
        
    } # if !is.na(q_cut)

    ## sign the portfolios
    if (Sign == -1) {
        temp1$port = max(temp1$port) + 1 - temp1$port
    }    
    
    signal = temp1 %>% select(-starts_with('break'))
    
    ## APPLY IMPLEMENTATION ADJUSTMENTS
    temp0 = signal
    
    # make all na except  "rebalancing months", which is actually signal updating months
    # and then fill na with stale data

    # find months that portfolio assignements are updated
    rebmonths =  (
        startmonth
        + seq(0,12)*portper
    ) %% 12
    rebmonths[rebmonths == 0] = 12
    rebmonths = sort(unique(rebmonths))
        
    temp0 =  temp0 %>%
        mutate(
            port = if_else(
            (yyyymm %% 100) %in% rebmonths
          , port
          , NA_real_
            )
        ) %>%
        arrange(permno,yyyymm) %>%
        group_by(permno) %>%
        fill(port) %>%
        filter(!is.na(port))                   

    signal = temp0
    
    ### CREATE PORTFOLIOS
    # this can be slow with daily data, about 20 sec per signal
    # using data.table is only about 2x faster, not worth it
    # filtering first by date actually makes things a bit slower


    ### ASSIGN TO PORTFOLIOS AND SIGN
    # lag signals: note port could by called portlag here
    signallag =  signal %>%
        mutate(
            yyyymm = yyyymm + 1
          , yyyymm = if_else(yyyymm %% 100 == 13, yyyymm+100-12,yyyymm)
        ) %>%
        transmute(
            permno
          , yyyymm
          , signallag = signal
          , port
        ) %>%
        arrange(permno, yyyymm)    
    
    if (feed.verbose) {print('joining lagged signals onto crsp returns')}
    gc()
    
    # R scoping implies crspret won't be modified outside of the function
    crspret = crspret %>%
        inner_join(
            signallag
          , by = c('permno','yyyymm')
        )         
    
    if (sweight == 'VW'){
        crspret$weight = crspret$melag
    } else {
        crspret$weight = 1
    }    
    

    if (feed.verbose) {print('calculating portfolio returns')}
    # takes about 25 sec for daily data
    # data.table is about 2x as fast, prob not worth it
    port = crspret %>%
        filter(!is.na(port),!is.na(ret),!is.na(weight)) %>%
        group_by(port, date) %>%
        summarize(
            ret = weighted.mean(ret, weight)
          , signallag = weighted.mean(signallag, weight)
          , Nstocks = n()
        )

    tempmax = max(port$port)
    templs = port %>%
        mutate(
            portls = if_else(port == tempmax, 'L', '?')
           ,portls = if_else(port == 1, 'S', portls)
        )   %>%
        filter(portls %in% c('L','S')) %>%
        pivot_wider(
            id_cols = c(date, portls, ret, Nstocks)
          , names_from = portls
          , values_from = c(ret,Nstocks)
        ) %>%
        filter(!is.na(ret_L),!is.na(ret_S)) %>%
        mutate(
            ret = ret_L - ret_S
          , Nstocks = Nstocks_L + Nstocks_S
          , port = 'LS'
          , signallag = NA
        ) %>%
        select(port,date,ret,signallag,Nstocks)        

    # convert port to string and pad left if deciles for ease
    if (is.na(q_cut) | (1/q_cut < 10)) {        
        port = port %>% mutate(port = sprintf('%01d',port))
    } else {
        port = port %>% mutate(port = sprintf('%02d',port))
    }

    port = port %>%
        rbind(
            templs
        ) %>%
        select(port,date,ret,signallag,Nstocks)        
    
    
    if (feed.verbose){
        print(paste0('end of signal_to_ports memory used = '))
        print(mem_used())
    }    
    gc()
    if (feed.verbose){print(gc(T))}

    return(port)
    
} ### end function


#############################################################################
loop_over_strategies = function(
                                strategylist
                              , saveportcsv = F
                              , saveportpath = NA
                              , saveportNmin = 20
                                ){
   
    # fill in missing fields
        req_col = c(
            'q_cut'
            ,'sweight'
            ,'Sign'
            ,'startmonth'
            ,'portper'
            ,'q_filt'
            ,'filterstr'
        )
    
        for (fni in 1:length(req_col)){
            if (!req_col[fni] %in% colnames(strategylist)){
                strategylist[,req_col[fni]] = NA
            }
        }

    Nstrat = dim(strategylist)[1]

    # making allport a list instead of dataframe seems to be better for memory
    # http://adv-r.had.co.nz/memory.html
    allport = list()
    for (i in seq(1,Nstrat)){
        print(paste0(i,'/',Nstrat,': ',strategylist$signalname[i]))
        strategylist[
            i
           , c( 'signalname'
             , 'assignport'
             , 'q_cut'
             , 'sweight'
             , 'portper'
             , 'q_filt'
             , 'filterstr'
               )
        ] %>% as.data.frame %>% print()
        
        start_time <- Sys.time()        
        
        tempport = tibble()

        ##   # using tryCatch maybe causing errors?
        
        tempport = tryCatch(
        {
            expr = signal_to_ports(
                strategylist$signalname[i]
              , strategylist$assignport[i]
              , strategylist$q_cut[i]
              , strategylist$sweight[i]
              , strategylist$Sign[i]
              , strategylist$startmonth[i]
              , strategylist$portper[i]
              , strategylist$q_filt[i]
              , strategylist$filterstr[i]
            )
        }
      , error = function(e){
          print('error in signal_to_ports, returning df with NA')
          data.frame(
              port = NA
            , date = NA
            , ret = NA
            , signallag = NA
            , Nstocks = NA
          )
      }
      )

        tempport = tempport  %>%
            mutate(signalname = strategylist$signalname[i]) %>%
            select(signalname,port,date,ret,signallag,Nstocks)

        # save individual port if requested
        if (saveportcsv){

            print(paste0('saving wide port to ', saveportpath))

            tempwide = tempport %>%
                filter(Nstocks >= saveportNmin) %>%
                select(port,date,ret) %>%
                pivot_wider(names_from=port,values_from=ret,names_prefix='port')

            writestandard(
                tempwide
              , saveportpath
              , paste0(strategylist$signalname[i], '_ret.csv')
            )
            
            
        } # if saveportcsv
        
        
        allport[[i]] = tempport

        end_time <- Sys.time()
        print(end_time - start_time)

        # garbage collection
        gc()
#        print(gc(T))
        
        

    } # i

    # turn list into data frame (memory mgmt)
    allport = do.call(rbind.data.frame, allport) %>%
        ungroup()

    return(allport)
    
    
} # end function




### FUNCTION FOR SUMMARIZING PORTMONTH DATASET
sumportmonth = function(
                        portret,
                        groupme = c('signalname','samptype'),
                        Nstocksmin = 20){
    
    temp =  portret %>%
        left_join(
            alldocumentation %>%
            transmute(signalname, SampleStartYear, SampleEndYear, PubYear = Year, Cat.Signal)
          , by=c("signalname")
        ) %>%
        mutate(
            samptype = case_when(
                year(date) >= SampleStartYear & year(date) <= SampleEndYear ~ "insamp"
               ,year(date) > SampleEndYear & year(date) <= PubYear ~ "between"            
               ,year(date) > PubYear ~ "postpub",
                TRUE ~ NA_character_
            )
        ) %>%
        select(-c(SampleStartYear, SampleEndYear, PubYear))
    
    tempsum = temp %>%
        filter(
            (Nstocks >= Nstocksmin) | is.na(date)
        ) %>%
        group_by_at(vars(all_of(groupme))) %>%
        summarize(
          rbar = mean(ret), vol = sd(ret), T = n()
          ,  tstat = rbar/vol*sqrt(T)
          , .groups='keep'
        ) %>%
        ungroup
    
} # end function


### FUNCTION FOR STANDARD CSV EXPORT
writestandard = function(df, path, filename){
    write.table(df
              , file = paste0(path, filename)
              , sep = ","
              , col.names = T
              , row.names = F
              , qmethod = "double"
              , quote = F              
                )
    
} # end function


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


### CHECK PORTFOLIOS ###
checkport = function(
                     port
                   , groupme = c('signalname','port')                     
                     ){
    
    port = port %>% left_join(
            alldocumentation %>%
            transmute(signalname, SampleStartYear, SampleEndYear, PubYear = Year, Cat.Signal)
          , by=c("signalname")
        ) %>%
        mutate(
            samptype = case_when(
                year(date) >= SampleStartYear & year(date) <= SampleEndYear ~ "insamp"
               ,year(date) > SampleEndYear & year(date) <= PubYear ~ "between"            
               ,year(date) > PubYear ~ "postpub",
                TRUE ~ NA_character_
            )
        ) %>%
        select(-c(SampleStartYear, SampleEndYear, PubYear)) %>%
        filter(samptype == 'insamp')

    
    port %>%
        group_by_at(vars(all_of(groupme))) %>%
        summarize(
           rbar = round(mean(ret),2)
           ,tstat = round(mean(ret)/sd(ret)*sqrt(n()),2)
           ,vol = round(sd(ret),2)
           ,T=n()
           ,mean(Nstocks)
           ,mean(signallag)
           ,samptype = 'insamp'
        ) %>%
        as.data.frame %>%
        print()
    
    port %>%
        mutate(Nok = if_else(Nstocks >= 20,'N>=20','N<20')) %>%
        group_by(signalname,Nok) %>%
        summarize(nportmonths = n()) %>%
        select(signalname, Nok, nportmonths) %>%
        pivot_wider(names_from = Nok
                  , values_from=nportmonths
                  , names_prefix = 'periods w/ ') %>%
        mutate(samptype = 'insamp') %>%
        as.data.frame %>%
        print()
    
} # end function


### FILL N TIMES FUNCTION ###
# allow for flexible padding and filling of signals
# groups together adjacent NAs then fills in with most recent NAs as long as there is one n space nearby
# https://stackoverflow.com/questions/52315161/limit-na-locf-in-zoo-package
# not being used right now 2021 01
fill_ntimes = function(x,n){
    ave(
        x,
        cumsum(!is.na(x)),
        FUN = function(x) ifelse(seq_along(x) <= n+1, x[1], NA)
    )
}


### FUNCTION FOR QUICK TESTING ALL SCRIPTS
ifquickrun = function(){
    if (quickrun) {
        print('running quickly')        
        strategylist0 = strategylist0 %>%
            filter(
                signalname %in% quickrunlist
            )        
    }
    return(strategylist0)
}
