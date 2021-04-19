# creates predictors that are simple transformation of CRSP data

### READ DATA

crsp = read_fst(paste0(pathDataIntermediate,'m_crsp.fst'))

### MAKE STreversal
if (!file.exists(paste0(pathPredictors, 'STreversal.csv'))) {
    
    temp = crsp %>%
        select(permno, date, ret) %>%
        mutate(
            STreversal = if_else(is.na(ret), 0, ret)
            , yyyymm = year(date)*100 + month(date)
        ) %>%
        filter(!is.na(STreversal)) %>%
        select(permno, yyyymm, STreversal)
    
    write_csv(temp, paste0(pathPredictors, 'STreversal.csv'))
    
}

### MAKE Price
if (!file.exists(paste0(pathPredictors, 'Price.csv'))) {
    
    temp = crsp %>%
        select(permno, date, prc) %>%
        mutate(
            Price = log(abs(prc))
            , yyyymm = year(date)*100 + month(date)        
        ) %>%
        filter(!is.na(Price)) %>%
        select(permno, yyyymm, Price)
    
    write_csv(temp, paste0(pathPredictors, 'Price.csv'))
    
}

### MAKE Size
if (!file.exists(paste0(pathPredictors, 'Size.csv'))) {
    
    temp = crsp %>%
        select(permno, date, shrout, prc) %>%
        filter(shrout > 0) %>%    
        mutate(
            Size = log(shrout*abs(prc))
            , yyyymm = year(date)*100 + month(date)        
        ) %>%
        filter(!is.na(Size)) %>%
        select(permno, yyyymm, Size)
    
    write_csv(temp, paste0(pathPredictors, 'Size.csv'))
    
}
