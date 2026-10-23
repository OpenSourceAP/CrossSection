# Run: sourced by master.R after config.R.
# Inputs: portfolio_config, SignalDoc.csv and installed R dependencies.
# Outputs: validated configuration, paths, loaded documentation and helpers.

#### CONFIGURATION HELPERS

portfolio_validate_config <- function(config) {
  fail <- function(name) stop("Invalid portfolio_config$", name, call. = FALSE)
  keys <- function(x, expected, name) {
    if (!is.list(x) || anyDuplicated(names(x)) ||
        !setequal(names(x), expected) || length(x) != length(expected)) fail(name)
  }
  number <- function(x, name, minimum = 0, integer = FALSE) {
    if (!is.numeric(x) || length(x) != 1L || is.na(x) || !is.finite(x) ||
        x < minimum || (integer && (x != floor(x) || x > .Machine$integer.max))) fail(name)
  }
  keys(config, c("signal_source", "paths", "run", "resources", "daily"), "fields")
  if (!is.character(config$signal_source) || length(config$signal_source) != 1L ||
      !config$signal_source %in% c("Python", "Stata")) fail("signal_source")
  keys(config$paths, "output_root", "paths")
  root <- config$paths$output_root
  if (!is.null(root) && (!is.character(root) || length(root) != 1L ||
                        is.na(root) || !nzchar(trimws(root)))) fail("paths$output_root")
  keys(config$run, c("daily", "exhibits", "quick", "quick_signals", "verbose"), "run")
  for (name in c("daily", "exhibits", "quick", "verbose")) {
    x <- config$run[[name]]
    if (!is.logical(x) || length(x) != 1L || is.na(x)) fail(paste0("run$", name))
  }
  signals <- config$run$quick_signals
  if (!is.character(signals) || !length(signals) || anyNA(signals) ||
      any(!nzchar(trimws(signals))) || anyDuplicated(signals)) fail("run$quick_signals")
  keys(config$resources, c("max_workers", "gib_per_worker"), "resources")
  number(config$resources$max_workers, "resources$max_workers", 1, TRUE)
  gib <- config$resources$gib_per_worker
  if (!is.numeric(gib) || length(gib) != 2L || !setequal(names(gib), c("monthly", "daily")) ||
      any(!is.finite(gib) | gib <= 0)) fail("resources$gib_per_worker")
  keys(config$daily, "min_stocks", "daily")
  number(config$daily$min_stocks, "daily$min_stocks", 1, TRUE)
  config
}

portfolio_paths <- function(config, project_root) {
  config <- portfolio_validate_config(config)
  project_root <- normalizePath(project_root, mustWork = TRUE)
  output_root <- config$paths$output_root
  if (is.null(output_root)) output_root <- project_root
  output_root <- path.expand(output_root)
  if (!grepl("^(/|[A-Za-z]:[/\\\\])", output_root)) output_root <- file.path(project_root, output_root)
  output_root <- normalizePath(output_root, mustWork = FALSE)
  slash <- function(...) paste0(file.path(...), "/")
  signal_folder <- if (config$signal_source == "Python") "pyData" else "Data"
  list(
    pathProject = slash(project_root), pathOutputRoot = slash(output_root),
    signalDataFolder = signal_folder,
    pathPredictors = slash(project_root, "Signals", signal_folder, "Predictors"),
    pathPlacebos = slash(project_root, "Signals", signal_folder, "Placebos"),
    pathCRSPPredictors = slash(project_root, "Signals", signal_folder, "CRSPPredictors"),
    pathtemp = slash(project_root, "Signals", signal_folder, "temp"),
    pathSignalsIntermediate = slash(project_root, "Signals", "pyData", "Intermediate"),
    pathCode = slash(project_root, "Portfolios", "Code"),
    pathDataIntermediate = slash(output_root, "Portfolios", "Data", "Intermediate"),
    pathDataPortfolios = slash(output_root, "Portfolios", "Data", "Portfolios"),
    pathDataSummary = slash(output_root, "Portfolios", "Data", "Summary"),
    pathDataDaily = slash(output_root, "Portfolios", "Data", "DailyPortfolios"),
    pathResults = slash(output_root, "Results")
  )
}

portfolio_check_dependencies <- function(config) {
  packages <- c("here", "tidyverse", "lubridate", "readxl", "writexl", "fst", "arrow", "data.table", "ps")
  if (config$run$exhibits && !config$run$quick) {
    packages <- c(packages, "extrafont", "xtable", "gridExtra", "ggrepel")
  }
  if (config$run$daily) packages <- c(packages, "lme4")
  missing <- packages[!vapply(packages, requireNamespace, logical(1), quietly = TRUE)]
  if (length(missing)) stop("Missing R packages: ", paste(missing, collapse = ", "),
                            ". Ask the environment owner to install them before running.", call. = FALSE)
  invisible(packages)
}

#### INITIALIZE CONFIGURATION

portfolio_config <- portfolio_validate_config(portfolio_config)
portfolio_check_dependencies(portfolio_config)
portfolio_root <- here::here()

# Compatibility globals for the existing calculation scripts.
SignalSource <- portfolio_config$signal_source
quickrun <- portfolio_config$run$quick
quickrunlist <- portfolio_config$run$quick_signals
skipdaily <- !portfolio_config$run$daily
feed.verbose <- portfolio_config$run$verbose
runexhibits <- portfolio_config$run$exhibits && !quickrun
list2env(portfolio_paths(portfolio_config, portfolio_root), envir = environment())

#### GLOBAL SETTINGS

options(dplyr.summarise.inform = FALSE)

# Create generated-output folders after configuration and dependency checks.
for (path in c(pathResults, pathDataPortfolios, pathDataIntermediate, pathDataSummary)) {
  dir.create(path, recursive = TRUE, showWarnings = FALSE)
}
# grid.arrange() and printed plots can open R's default PDF device before ggsave.
# Keep that incidental file inside the output root as well.
if (!interactive()) options(device = local({
  plot_file <- file.path(pathResults, 'Rplots.pdf')
  function(...) grDevices::pdf(file = plot_file, ...)
}))

#### PACKAGES
options(stringsAsFactors = FALSE)
library(tidyverse)
library(lubridate)
library(readxl)
library(writexl)
library(fst)
library(arrow)
library(data.table)

### EXHIBITS SETTINGS ###
options(scipen = 999)
optFontsize <- 20
optFontFamily <- ''
dlmethod <- if (Sys.info()[['sysname']] == 'Linux') 'wget' else 'auto'
if (runexhibits) {
  library(extrafont)
  loadfonts()
  library(xtable)
  options(xtable.floating = FALSE)
  library(gridExtra)
  library(ggrepel)
  if (Sys.info()[['sysname']] != 'Linux' && 'Palatino Linotype' %in% fonts()) {
    optFontFamily <- 'Palatino Linotype'
  }
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
    alldocumentation = read_csv(
        paste0(pathProject, 'SignalDoc.csv')
    ) %>%
        rename(signalname = Acronym)  %>%
        # Format order of category labels
        mutate(Cat.Data = as_factor(Cat.Data) %>% 
                   factor(levels = c('Accounting', 'Analyst', 'Event', 'Options', 'Price', 'Trading', '13F', 'Other'))) %>% 
        # Make economic category proper
        mutate(Cat.Economic = str_to_title(Cat.Economic)) %>% 
        # Clean column names
        rename(
          sweight = 'Stock Weight'
          , q_cut = 'LS Quantile'
          , q_filt = 'Quantile Filter'  
          , portperiod = 'Portfolio Period'
          , startmonth = 'Start Month'
          , filterstr = 'Filter'
        ) %>%
        mutate(
            filterstr = if_else(filterstr %in% c('NA','None','none')
              , NA_character_
              , filterstr)
        ) %>%
        select(-c(starts_with('Note'))) %>% 
        arrange(signalname)   
    

    
    names(alldocumentation) = make.names(names(alldocumentation))

    return(alldocumentation)

    
} # end function

## run readdocumentaiton
alldocumentation = readdocumentation()


### FUNCTION checking which signals have been created

checkSignals = function(docs = alldocumentation, pathProj = pathProject) {

  # Classification in SignalDoc
  prdsPredictor = alldocumentation %>% 
    filter(Cat.Signal == 'Predictor') %>% 
    pull(signalname)
  
  prdsPlacebo = alldocumentation %>% 
    filter(Cat.Signal == 'Placebo') %>% 
    pull(signalname)

  # Created signals
  flsPredictors = list.files(paste0(pathProj, 'Signals/', signalDataFolder, '/Predictors/'))
  flsPlacebos = list.files(paste0(pathProj, 'Signals/', signalDataFolder, '/Placebos/'))

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
    message('The following Predictors in SignalDoc have not been created in Data/Predictors:')
    print(predNotInData)
  }
  
  if (!is.null(placeboNotInData)) {
    message('The following Placebos in SignalDoc have not been created in Data/Placebos:')
    print(placeboNotInData)
  }
  
  if (is.null(predNotInData) & is.null(placeboNotInData)) {
    message('All predictors and placebos were created.')
  }
  
} # end function

# predictors built directly from CRSP by Signals/pyCode; not in the public signal zips
crsp_predictors = c('Price', 'Size', 'STreversal')

# Check that the CRSP inputs produced by Signals/pyCode exist. These are the
# only inputs that cannot be downloaded from the data page: the CRSP parquet
# files and the three CRSP predictors. Signals/pyCode/crsp_only.py makes them.
check_crsp_inputs <- function(path_proj = pathProject, skip_daily = skipdaily) {
  required <- c(
    paste0(path_proj, 'Signals/pyData/Intermediate/monthlyCRSP.parquet'),
    paste0(path_proj, 'Signals/pyData/Predictors/', crsp_predictors, '.csv')
  )
  if (!skip_daily) {
    required <- c(required, paste0(path_proj, 'Signals/pyData/Intermediate/dailyCRSP.parquet'))
  }
  missing <- required[!file.exists(required)]
  if (length(missing) > 0) {
    message('Missing CRSP inputs:')
    for (f in missing) message('  - ', f)
    stop(paste0(
      'CRSP inputs not found. From Signals/pyCode/ run: python crsp_only.py',
      if (skip_daily) ' --skip-daily' else '',
      '\n(or run the full signals pipeline, python master.py)'
    ))
  }
  message('CRSP input check: all CRSP parquet files and CRSP predictors found.')
  invisible(TRUE)
}

check_signal_csvs <- function(path_proj = pathProject, signal_source = SignalSource) {
  signal_doc_path <- file.path(path_proj, 'SignalDoc.csv')
  signal_folder <- if (identical(signal_source, 'Python')) 'pyData' else 'Data'
  predictors_dir <- file.path(path_proj, 'Signals', signal_folder, 'Predictors')
  placebos_dir <- file.path(path_proj, 'Signals', signal_folder, 'Placebos')

  if (!file.exists(signal_doc_path)) {
    stop('SignalDoc.csv not found at the discovered project root.')
  }

  if (!dir.exists(predictors_dir) || !dir.exists(placebos_dir)) {
    stop('Signals/pyCode directories not found. Please run the signals pipeline first.')
  }

  signal_doc <- read.csv(signal_doc_path, stringsAsFactors = FALSE)
  expected_signals <- unique(signal_doc$Acronym[signal_doc$Acronym != '' & signal_doc$Cat.Signal != 'Drop'])
  expected_signals <- sort(expected_signals)

  predictor_files <- tools::file_path_sans_ext(list.files(predictors_dir, pattern = '\\.csv$', ignore.case = TRUE))
  placebo_files <- tools::file_path_sans_ext(list.files(placebos_dir, pattern = '\\.csv$', ignore.case = TRUE))

  all_signal_files <- sort(unique(c(predictor_files, placebo_files)))
  missing_signals <- setdiff(expected_signals, all_signal_files)
  # the CRSP predictors are checked separately by check_crsp_inputs()
  missing_signals <- setdiff(missing_signals, crsp_predictors)
  extra_files <- setdiff(all_signal_files, expected_signals)

  if (length(missing_signals) == 0) {
    message('Signal completeness check: all expected signals found in pyCode/Predictors and pyCode/Placebos.')
  } else {
    warning(sprintf('Signal completeness check: %d missing signal CSV(s) detected.', length(missing_signals)))
    for (signal_name in missing_signals) {
      message(sprintf('  - Missing CSV: %s', signal_name))
    }
  }

  if (length(extra_files) > 0) {
    message(sprintf('Found %d extra CSV(s) not documented in SignalDoc.csv:', length(extra_files)))
    for (signal_name in extra_files) {
      in_predictors <- signal_name %in% predictor_files
      in_placebos <- signal_name %in% placebo_files
      location <- paste(c(if (in_predictors) 'Predictors' else NULL,
                          if (in_placebos) 'Placebos' else NULL), collapse = ', ')
      message(sprintf('  - Extra CSV: %s (%s)', signal_name, location))
    }
  }

  invisible(length(missing_signals) == 0)
}


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

    
    sumport = sumportmonth(port,Nstocksmin=1) %>%
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

    return(sumport)
    
    
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


#### PARALLEL JOBS ####
# Run named jobs on PSOCK workers and return their results in job order. Free
# workers take the next job in list order. Workers start as fresh R sessions:
#   globals: named list assigned in each worker's global environment
#   setup(): runs once per worker after globals, e.g. to load shared data
#   run_job(job): runs one job in a worker; write outputs to disk and return
#     something small
# Functions in globals, setup and run_job run with the worker's global
# environment, so they see the globals but not this session's workspace.
# A failed job is reported after the other jobs finish, then the stage stops.
portfolio_run_jobs = function(stage, jobs, run_job, setup = function() NULL, globals = list()){
  stopifnot(is.list(jobs), length(jobs) > 0, !is.null(names(jobs)), !anyDuplicated(names(jobs)))
  # Send functions without their defining environment (often the whole workspace).
  to_global = function(x) { if (is.function(x)) environment(x) = globalenv(); x }
  globals = lapply(globals, to_global)

  workers = min(portfolio_n_workers(stage), length(jobs))
  cluster = parallel::makePSOCKcluster(workers, outfile = '')
  pids = unlist(parallel::clusterCall(cluster, Sys.getpid))
  finished = FALSE
  on.exit({
    # Busy workers ignore stopCluster until their job ends, so kill them after
    # an error or interrupt.
    if (!finished) tools::pskill(pids)
    try(parallel::stopCluster(cluster), silent = TRUE)
  })

  parallel::clusterCall(cluster, function(globals, setup){
    list2env(globals, envir = globalenv())
    setup()
    NULL
  }, globals, to_global(setup))

  run_one = to_global(function(name, job, run_job){
    start = Sys.time()
    message('[', name, '] started on worker ', Sys.getpid())
    out = tryCatch(list(result = run_job(job), error = NA_character_)
                 , error = function(e) list(result = NULL, error = conditionMessage(e)))
    out$minutes = as.numeric(difftime(Sys.time(), start, units = 'mins'))
    message('[', name, '] ', if (is.na(out$error)) 'finished' else 'FAILED'
          , sprintf(' after %.1f min', out$minutes))
    out
  })
  status = parallel::clusterMap(cluster, run_one, names(jobs), jobs
                              , MoreArgs = list(run_job = to_global(run_job))
                              , .scheduling = 'dynamic', SIMPLIFY = FALSE)
  finished = TRUE
  names(status) = names(jobs)

  for (name in names(status)) {
    message(sprintf('[%s] %s: %.1f min', stage, name, status[[name]]$minutes))
  }
  failed = Filter(function(x) !is.na(x$error), status)
  if (length(failed)) {
    stop('[', stage, '] failed jobs:\n'
       , paste0('  ', names(failed), ': ', vapply(failed, `[[`, '', 'error'), collapse = '\n')
       , call. = FALSE)
  }
  lapply(status, `[[`, 'result')
} # end function
