#### GLOBAL SETTINGS

options(dplyr.summarise.inform = FALSE)

#### PATHS
pathPredictors = paste0(pathProject, 'Signals/Data/Predictors/')
pathPlacebos = paste0(pathProject, 'Signals/Data/Placebos/')
pathCRSPPredictors = paste0(pathProject, 'Signals/Data/CRSPPredictors/')
pathtemp = paste0(pathProject, 'Signals/Data/temp/')

pathCode = paste0(pathProject, 'Portfolios/Code/')
pathDataIntermediate = paste0(pathProject, 'Portfolios/Data/Intermediate/')
pathDataPortfolios = paste0(pathProject, 'Portfolios/Data/Portfolios/')
pathDataSummary = paste0(pathProject, 'Portfolios/Data/Summary/')

pathResults = paste0(pathProject, 'Results/')

## Create folders if they don't exist
# Portfolios/ paths
dir.create(pathResults)
dir.create(paste0(pathProject, 'Portfolios/Data'))
dir.create(paste0(pathDataPortfolios))
dir.create(paste0(pathDataIntermediate))

# Signals/Data/ paths
dir.create(paste0(pathProject,'Signals/Data/'))
dir.create(paste0(pathPredictors))
dir.create(paste0(pathPlacebos))
dir.create(paste0(pathtemp))


#### PACKAGES
# Check for and potentially install missing packages
install.packages(setdiff(c('tidyverse', 'lubridate', 'readxl', 'writexl', 'pryr', 'fst',
                           'RPostgres', 'getPass', 'xtable', 'gridExtra',
                           'ggrepel','data.table'), 
                         rownames(installed.packages())))

# Use the extrafonts package, to get nicer fonts for output figures
# Code issues warnings when not installed but runs nevertheless
# See https://cran.r-project.org/web/packages/extrafont/README.html
if (!'extrafont' %in% rownames(installed.packages())) {
  install.packages('extrafont')
  extrafont::font_import()
}


options(stringsAsFactors = FALSE)
library(tidyverse)
library(lubridate)
library(readxl)
library(writexl)
library(pryr)
library(fst)
library(data.table) # for handling daily crsp

# for WRDS access
library(RPostgres)
library(getPass)


### EXHIBITS SETTINGS ###
options(stringsAsFactors = FALSE)
options(scipen = 999)
optFontsize <- 20 # Fix fontsize for graphs here

library(extrafont)
loadfonts()

library(xtable)
options(xtable.floating = FALSE)
library(gridExtra)
library(ggrepel)

# system dependent settings 
dlmethod <- "auto"

if ('Palatino Linotype' %in% fonts()) {
  optFontFamily = 'Palatino Linotype'
} else {
  optFontFamily = ''
}

sysinfo <- Sys.info()
if (sysinfo[1] == "Linux") {
  dlmethod <- "wget"
  optFontFamily <- "" # necessary for linux command line  
}

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
        # Format order of category labels
        mutate(Cat.Data = as_factor(Cat.Data) %>% 
                   factor(levels = c('Accounting', 'Analyst', 'Event', 'Options', 'Price', 'Trading', '13F', 'Other'))) %>% 
        # Make economic category proper
        mutate(Cat.Economic = str_to_title(Cat.Economic))
    
    temp2 = read_excel(
        paste0(pathProject, 'SignalDocumentation.xlsx')
      , sheet = 'AddInfo'
    ) %>%
        select(-Authors) %>%         
        rename(
            signalname = Acronym
          , sweight = 'Stock Weight'
          , q_cut = 'LS Quantile'
          , q_filt = 'Quantile Filter'  
          , portperiod = 'Portfolio Period'
          , startmonth = 'Start Month'
          , filterstr = 'Filter'
        ) %>%
        mutate_at(
            c('q_cut','portperiod','startmonth')
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
    
    # clean up
    alldocumentation = alldocumentation %>%
        mutate(Sign = as.numeric(Sign))
    
    names(alldocumentation) = make.names(names(alldocumentation))

    return(alldocumentation)

    
} # end function

## run readdocumentaiton
alldocumentation = readdocumentation()


### FUNCTION checking which signals have been created

checkSignals = function(docs = alldocumentation, pathProj = pathProject) {

  # Classification in SignalDocumentation  
  prdsPredictor = alldocumentation %>% 
    filter(Cat.Signal == 'Predictor') %>% 
    pull(signalname)
  
  prdsPlacebo = alldocumentation %>% 
    filter(Cat.Signal == 'Placebo') %>% 
    pull(signalname)

  # Created signals
  flsPredictors = list.files(paste0(pathProj, 'Signals/Data/Predictors/'))
  flsPlacebos = list.files(paste0(pathProj, 'Signals/Data/Placebos/'))

  # Predictor in Data/Predictor?
  predNotInData = c()
  for (p in prdsPredictor) {
    if (sum(grepl(p, flsPredictors, ignore.case = TRUE)) ==0) {
      predNotInData = c(predNotInData, p)
    }
  }
  
  # Placebo in Data/Placebo?
  placeboNotInData = c()
  for (p in prdsPlacebo) {
    if (sum(grepl(p, flsPlacebos, ignore.case = TRUE)) ==0) {
      placeboNotInData = c(placeboNotInData, p)
    }
  }
  
  # Output warnings
  if (!is.null(predNotInData)) {
    message('The following Predictors in SignalDocumentation have not been created in Data/Predictors:')
    print(predNotInData)
  }
  
  if (!is.null(placeboNotInData)) {
    message('The following Placebos in SignalDocumentation have not been created in Data/Placebos:')
    print(placeboNotInData)
  }
  
  if (is.null(predNotInData) & is.null(placeboNotInData)) {
    message('All predictors and placebos were created.')
  }
  
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


### FUNCTION FOR SUMMARIZING PORTMONTH DATASET
sumportmonth = function(
                        portret,
                        groupme = c('signalname','samptype','port'),
                        Nstocksmin = 20){
    
    temp =  portret %>%
        left_join(
            alldocumentation %>%
            select(signalname, SampleStartYear, SampleEndYear, Year)
          , by=c("signalname")
        ) %>%
        mutate(
            samptype = case_when(
                year(date) >= SampleStartYear & year(date) <= SampleEndYear ~ "insamp"
               ,year(date) > SampleEndYear & year(date) <= Year ~ "between"            
               ,year(date) > Year ~ "postpub",
                TRUE ~ NA_character_
            )
        ) %>%
        select(-c(SampleStartYear, SampleEndYear, Year))

    # summarize
    tempsum = temp %>%
        mutate(
            Ncheck = if_else(port != 'LS', Nlong, as.integer(pmin(Nlong,Nshort)) )
        ) %>%
        filter(
            (Ncheck >= Nstocksmin) 
        ) %>%
        group_by_at(vars(all_of(groupme))) %>%
        summarize(
           tstat = round(mean(ret)/sd(ret)*sqrt(n()),2)
           ,rbar = round(mean(ret),2)
           ,vol = round(sd(ret),2)
           ,T=n()
           ,Nlong = round(mean(Nlong),1)
           ,Nshort = round(mean(Nshort),1)
           ,signallag = round(mean(signallag),3)            
        ) %>%
        ungroup %>%
        arrange(samptype, signalname, port)
            
    
} # end function


### CHECK PORTFOLIOS ###
checkport = function(
                     port
                   , groupme = c('signalname','port')                     
                     ){

    
    sumportmonth(port,Nstocksmin=1) %>%
        filter(samptype == 'insamp') %>%
        as.data.frame %>%
        print()
    
    port %>%
        mutate(
            Nok = if_else(Nlong >= 20,'Nlong>=20','Nlong<20')
        ) %>%
        group_by(signalname,port,Nok) %>%
        summarize(nportmonths = n()) %>%
        select(signalname, Nok, nportmonths) %>%
        pivot_wider(names_from = Nok
                  , values_from=nportmonths
                  , names_prefix = 't w/ ') %>%
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







#############################################################################
loop_over_strategies = function(
                                strategylist
                              , saveportcsv = F
                              , saveportpath = NA
                              , saveportNmin = 1
                              , passive_gain = F
                                ){   

    Nstrat = dim(strategylist)[1]

    # making allport a list instead of dataframe seems to be better for memory
    # http://adv-r.had.co.nz/memory.html
    allport = list()
    for (i in seq(1,Nstrat)){
        
        print(paste0(i,'/',Nstrat,': ',strategylist$signalname[i]))
        strategylist[
            i
          , c( 'signalname'
            , 'Cat.Form'
            , 'q_cut'
            , 'sweight'
            , 'portperiod'
            , 'q_filt'
            , 'filterstr'
              )
        ] %>% as.data.frame %>% print()
        
        start_time <- Sys.time()                
        
        tempport = tryCatch(
        {
            expr = signalname_to_ports(
                signalname = strategylist$signalname[i]
              , Cat.Form = strategylist$Cat.Form[i]
              , q_cut = strategylist$q_cut[i]
              , sweight = strategylist$sweight[i]
              , Sign = strategylist$Sign[i]
              , startmonth = strategylist$startmonth[i]
              , portperiod = strategylist$portperiod[i]
              , q_filt = strategylist$q_filt[i]
              , filterstr = strategylist$filterstr[i]
              , passive_gain = passive_gain
            )
            
        }
      , error = function(e){
          print('error in signalname_to_longports, returning df with NA')
          data.frame(
              matrix(ncol = dim(allport[[i-1]])[2], nrow = 1)
          ) 
      }
      ) # tryCatch

        if (is.na(tempport[1,1])){
            colnames(tempport) = colnames(allport[[1]]) # assume strat 1 worked ok
            tempport$signalname = strategylist$signalname[1]
        }
        

        # save individual port to disk if requested
        if (saveportcsv){

            print(paste0('saving wide port to ', saveportpath))

            tempwide = tempport %>%
                filter(Nlong >= saveportNmin) %>%
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
        

    } # i

    
    # turn list into data frame (memory mgmt)
    allport = do.call(rbind.data.frame, allport) 

    return(allport)
    
    
} # end function

