# pack portfolios for shipping
# Created 2021 04
# takes about 20 min

# ==== ENVIRONMENT ====
starttime = Sys.time()

dir.create(paste0(pathStorage,'Portfolios/'))
dir.create(paste0(pathStorage,'Portfolios/Full Sets OP/'))
dir.create(paste0(pathStorage,'Portfolios/Full Sets Alt/'))
dir.create(paste0(pathStorage,'Portfolios/Individual/'))
dir.create(paste0(pathStorage,'DailyPortfolios/'))

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
  
  dir.create(pathout)
  
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
