# """
# Inputs: Uses `pathStorage`, `pathPortfolios`, and `pathResults` defined by `master_shipping.r` or the caller; consumes portfolio CSVs and result artifacts.
# Outputs: Copies and zips portfolio deliverables plus results into the release tree under `pathStorage`.
# How to run: Called from `master_shipping.r`; can be sourced directly after sourcing `00_settings.txt`.
# Example: `Rscript -e "source('Shipping/Code/master_shipping.r')"` (runs full pipeline including this script).
# """
# pack portfolios for shipping
# Created 2021 04
# takes about 20 min

# ==== ENVIRONMENT ====
starttime = Sys.time()
script_wd = getwd()
on.exit(setwd(script_wd), add = TRUE)

if (!exists('ensure_dir')) {
  ensure_dir = function(path){
    dir.create(path, recursive = TRUE, showWarnings = FALSE)
  }
}

ensure_dir(paste0(pathStorage,'Portfolios/'))
ensure_dir(paste0(pathStorage,'Portfolios/Full Sets OP/'))
ensure_dir(paste0(pathStorage,'Portfolios/Full Sets Alt/'))
ensure_dir(paste0(pathStorage,'Portfolios/Individual/'))
ensure_dir(paste0(pathStorage,'DailyPortfolios/'))
ensure_dir(paste0(pathStorage,'Results/'))

# ==== FULL SETS OP ====
# copy the OP full sets without zipping

flist = list.files(paste0(pathPortfolios))
flist = flist[!grepl('PredictorAlt',flist)]

for (fcurr in flist){
  file.copy(
    from = paste0(pathPortfolios,flist)
    , to = paste0(pathStorage,'Portfolios/Full Sets OP/')
  )
}

# ==== FULL SETS ALT ====

# zip up the full sets of alternative implementations
implist = list.files(paste0(pathPortfolios), pattern='PredictorAlt')  %>%
  str_remove('.csv')

# avoid copying paths into zip
tempdir = getwd()
setwd(pathPortfolios) 

print(paste0('Zipping Predictor Alt csvs ',Sys.time()))
for (impcurr in implist){
  zip(
    zipfile = paste0(pathStorage, 'Portfolios/Full Sets Alt/', impcurr, '.zip')
    , files = paste0(impcurr, '.csv')
  )
}

# zip up placebos 
impcurr = 'PlaceboPortsFull'
zip(
  zipfile = paste0(pathStorage, 'Portfolios/Full Sets Alt/', impcurr, '.zip')
  , files = paste0(impcurr, '.csv')
)

# reset folder
setwd(tempdir)

print(paste0('Done zipping Predictor Alt csvs ',Sys.time()))

# ==== INDIVIDUAL PREDICTOR PORTFOLIO SORTS REPACKING ====

# write indiv function
write_indiv  = function(setname,outfolder){
  
  pathout = paste0(pathStorage,'Portfolios/Individual/',outfolder)
  
  ensure_dir(pathout)
  
  allport = fread(paste0(pathPortfolios, setname))
  signallist = allport %>% distinct(signalname) %>% as.matrix
  
  for (i in 1:length(signallist)){
    tempret = allport %>%
      filter(signalname == signallist[i]) %>%
      select(date, port, ret) %>%
      filter(!is.na(ret)) %>%
      spread(port, ret, sep='')
    
    write.csv(
      tempret, paste0(pathout, signallist[i], '.csv')
    )   
    
  } # for i 
  
} # end function

### WRITE ORIGINAL CUTS
print('writing portfolios individual original cuts')
write_indiv('PredictorPortsFull.csv','Original_Cuts/')

### WRITE ORIGINAL CUTS VW
print('writing portfolios individual original cuts VW')
write_indiv('PredictorAltPorts_LiqScreen_VWforce.csv','Original_CutsVW/')


### WRITE DECILES
print('writing portfolios individual cts deciles')
write_indiv('PredictorAltPorts_Deciles.csv','Cts_Deciles/')

### WRITE QUINTILES
print('writing portfolios individual cts quintiles')
write_indiv('PredictorAltPorts_Quintiles.csv','Cts_Quintiles/')


### WRITE DECILES VW
print('writing portfolios individual cts deciles vw')
write_indiv('PredictorAltPorts_DecilesVW.csv','Cts_DecilesVW/')

### WRITE QUINTILES VW
print('writing portfolios individual cts quintiles vw')
write_indiv('PredictorAltPorts_QuintilesVW.csv','Cts_QuintilesVW/')




# ==== DAILY PORTFOLIOS ====

# setwd to avoid copying paths into zip
tempdir = getwd()
setwd(paste0(pathPortfolios, '../DailyPortfolios/')) 

implist = list.dirs() 
implist = implist[grepl('Predictor',implist)]

print(paste0('Daily Predictor csvs ',Sys.time()))
for (impcurr in implist){
  zip(
    zipfile = paste0(pathStorage, 'DailyPortfolios/', impcurr, '.zip')
    , files = paste0(impcurr)
  )
}

# add the summary xlsx 
file.copy(
  from = 'DailyPortSummary.xlsx'
  , to = paste0(pathStorage, 'DailyPortfolios/')
)


# reset folder
setwd(tempdir)

print(paste0('Done zipping daily portfolio csvs ',Sys.time()))

print(Sys.time() - starttime )

# ==== RESULTS ====
result_wd = getwd()
setwd(pathResults)

flist = list.files()
for (fcurr in flist){
  success = file.copy(
    from = paste0(fcurr)
    , to = paste0(pathStorage,'Results/', fcurr)
  )
  if (!success){
    print(paste0('Failed to copy ', fcurr))
  }
}
setwd(result_wd)
