# creates predictors that are simple transformation of CRSP data

### READ DATA

crspret  = read_fst(paste0(pathDataIntermediate,'crspmret.fst'))
crspinfo = read_fst(paste0(pathDataIntermediate,'crspminfo.fst'))

### MAKE STreversal
if (!file.exists(paste0(pathPredictors, 'STreversal.csv'))) {
    
    temp = crspret %>%
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
    
    temp = crspinfo %>%
        select(permno, yyyymm, prc) %>%
        mutate(
            Price = log(abs(prc))
        ) %>%
        filter(!is.na(Price)) %>%
        select(permno, yyyymm, Price)
    
    write_csv(temp, paste0(pathPredictors, 'Price.csv'))
    
}

### MAKE Size
if (!file.exists(paste0(pathPredictors, 'Size.csv'))) {
    
    temp = crspinfo %>%
        select(permno, yyyymm, me) %>%
        mutate(
            Size = log(me)
        ) %>%
        filter(!is.na(Size)) %>%
        select(permno, yyyymm, Size)
    
    write_csv(temp, paste0(pathPredictors, 'Size.csv'))
    
}
