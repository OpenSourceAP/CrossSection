# creates predictors that are simple transformation of CRSP data

source('00_SettingsAndFunctions.R')


### READ DATA

crsp = read_fst(paste0(pathDataIntermediate,'m_crsp.fst'))


### MAKE Mom1m
temp = crsp %>%
    select(permno, date, ret) %>%
    mutate(
        Mom1m = if_else(is.na(ret), 0, ret)
        , yyyymm = year(date)*100 + month(date)
    ) %>%
    filter(!is.na(Mom1m)) %>%
    select(permno, yyyymm, Mom1m)
    
write.csv(temp, paste0(pathCRSPPredictors, 'Mom1m.csv'),row.names=F,quote=F)


### MAKE Price
temp = crsp %>%
    select(permno, date, prc) %>%
    mutate(
        Price = log(abs(prc))
        , yyyymm = year(date)*100 + month(date)        
    ) %>%
    filter(!is.na(Price)) %>%
    select(permno, yyyymm, Price)
    
write.csv(temp, paste0(pathCRSPPredictors, 'Price.csv'),row.names=F,quote=F)


### MAKE Size
# in daily data, I think you want cfacprc to be safe
temp = crsp %>%
    select(permno, date, shrout, prc) %>%
    filter(shrout > 0) %>%    
    mutate(
        Size = log(shrout*abs(prc))
        , yyyymm = year(date)*100 + month(date)        
    ) %>%
    filter(!is.na(Size)) %>%
    select(permno, yyyymm, Size)
    
write.csv(temp, paste0(pathCRSPPredictors, 'Size.csv'),row.names=F,quote=F)



