# Andrew chen 2021 03 15
# Add CRSP predictors to the wide signal data
# for Conveneince
# made from 10_DownloadCRSP.R and 11_CreateCRSPPredictors.R

rm(list = ls())
source('00_settings.r')

# for WRDS access
library(RPostgres)
library(getPass)



## EMACS ESS WORKAROUND
# hopefully this works in Rstudio...
user = getPass('wrds username: ')
pass = getPass('wrds password: ')


wrds <- dbConnect(Postgres(),
                    host='wrds-pgdata.wharton.upenn.edu',
                    port=9737,
                    dbname='wrds',
                    user=user,
                    password=pass,
                    sslmode='require')






# CRSP monthly ------------------------------------------------------------
numRowsToPull = -1  # Set to -1 for all rows and to some positive value for testing

# Follows in part: https://wrds-www.wharton.upenn.edu/pages/support/research-wrds/macros/wrds-macro-crspmerge/

m_crsp = dbSendQuery(conn = wrds, statement = 
                   "select a.permno, a.permco, a.date, a.ret, a.retx, a.vol, a.shrout, a.prc, a.cfacshr, a.bidlo, a.askhi,
                     b.shrcd, b.exchcd, b.siccd, b.ticker, b.shrcls,  -- from identifying info table
                     c.dlstcd, c.dlret                                -- from delistings table
                     from crsp.msf as a
                     left join crsp.msenames as b
                     on a.permno=b.permno
                     and b.namedt<=a.date
                     and a.date<=b.nameendt
                     left join crsp.msedelist as c
                     on a.permno=c.permno 
                     and date_trunc('month', a.date) = date_trunc('month', c.dlstdt)
                     "
) %>% 
    # Pull data
    dbFetch(n = numRowsToPull) %>%
    as_tibble()


# incorporate delisting return
# GHZ cite Johnson and Zhao (2007), Shumway and Warther (1999)

m_crsp2 = m_crsp %>%
    mutate(
        dlret = ifelse(
            is.na(dlret)
            & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584))
            & (exchcd == 1 | exchcd == 2)
          , -0.35
          , dlret
        )
      , dlret = ifelse(
            is.na(dlret)
            & (dlstcd == 500 | (dlstcd >=520 & dlstcd <=584))
            & (exchcd == 3)
          , -0.55
          , dlret
        )
      , dlret = ifelse(
            dlret < -1 & !is.na(dlret)
          , -1
          , dlret
        )
      , dlret = ifelse(
            is.na(dlret)
          , 0
          , dlret
        )
       , ret = ret + dlret
       , ret = ifelse(
             is.na(ret) & ( dlret != 0)
             , dlret
             , ret
         )
    ) %>%
    mutate(
        ret = 100*ret
    )


### MAKE STreversal, Price, Size
crspsignals = m_crsp2 %>%
    mutate(
        yyyymm = year(date)*100 + month(date)        
        , STreversal = if_else(is.na(ret), 0, ret)
      , Price = log(abs(prc))
      , Size = log(shrout*abs(prc))        
    ) %>%
    select(permno, yyyymm, STreversal, Price, Size)

# signed version (separated for clarity)
signedcrspsignals = crspsignals %>%
    mutate(STreversal = -1*STreversal
         , Price = -1*Price
         , Size = -1*Size)

### MERGE WITH PACKED AND SIGNED DOWNLOADABLE PREDICTORS

dlsignals = fread(paste0(pathStorage, '/temp/signed_predictors_dl_wide.csv'))

allpredictors = merge(
    dlsignals %>% select(-V1)
   , signedcrspsignals
  , by=c('permno','yyyymm'), all=T
)        

# save to storage
write.csv(allpredictors, paste0(pathStorage, '/temp/signed_predictors_all_wide.csv'))
