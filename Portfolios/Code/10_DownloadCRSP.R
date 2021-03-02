## This is redundant with Signals/Code/DataDownloads/I_CRSPmonthly.do, as well as with the size and price signal do files, but having this script allows the user to just download the shareable signal csvs and ignore all of the Signal code.

## Andrew Chen 2020 12

## Rstudio version
## wrds <- dbConnect(Postgres(),
##                     host='wrds-pgdata.wharton.upenn.edu',
##                     port=9737,
##                     dbname='wrds',
##                     user=rstudioapi::askForPassword("Database username"),
##                     password=rstudioapi::askForPassword("Database password"),
##                     sslmode='require')



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
    )

# convert ret to pct
m_crsp2 = m_crsp2 %>%
    mutate(
        ret = 100*ret
    )

# write to disk (dlret adjusted)
write_fst(m_crsp2, paste0(pathProject,'Portfolios/Data/Intermediate/m_crsp.fst'))


# write to disk (no dlret adjustment)
write_fst(
    m_crsp %>% mutate(ret = ret*100, dlret = dlret*100) 
  , paste0(pathProject,'Portfolios/Data/Intermediate/m_crsp_nodelistadj.fst')
)


# CRSP daily --------------------------------------------------------------

d_crsp = dbSendQuery(conn = wrds, statement = 
                       "select a.permno, a.date, a.ret, a.shrout, a.prc, a.cfacshr
                     from crsp.dsf as a
                     "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)


# convert ret to pct
d_crsp = d_crsp %>%
    mutate(
        ret = 100*ret
    )


write_fst(d_crsp, paste0(pathProject,'Portfolios/Data/Intermediate/d_crsp.fst'))
