
# Environment -------------------------------------------------------------


## LOGIN TO WRDS
user = getPass('wrds username: ')
pass = getPass('wrds password: ')

wrds <- dbConnect(Postgres(),
                    host='wrds-pgdata.wharton.upenn.edu',
                    port=9737,
                    dbname='wrds',
                    user=user,
                    password=pass,
                    sslmode='require')

numRowsToPull = -1  # Set to -1 for all rows and to some positive value for testing

# CRSP monthly ------------------------------------------------------------
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

m_crsp2$passgainm = 1 # passive gain within the month is always 1 here


# write to disk (dlret adjusted)
write_fst(m_crsp2, paste0(pathProject,'Portfolios/Data/Intermediate/m_crsp.fst'))


# write to disk (no dlret adjustment)
write_fst(
    m_crsp %>% mutate(ret = ret*100, dlret = dlret*100) 
  , paste0(pathProject,'Portfolios/Data/Intermediate/m_crsp_nodelistadj.fst')
)



# CRSP daily --------------------------------------------------------------

for (year in seq(1926,year(Sys.time()))){
  print(paste0('downloading daily crsp for year ',year))
  query = paste0(
    "select a.permno, a.date, a.ret, a.shrout, a.prc, a.cfacshr
                     from crsp.dsf as a
                     where date >= "
    , "\'", year,"-01-01\'"
    ,"and date <= "
    , "\'", year,"-12-31\'"
  )
  
  temp_d_crsp = dbSendQuery(conn = wrds, statement = query) %>% 
    # Pull data
    dbFetch(n = numRowsToPull)
  
  if (year==1926){
    d_crsp = temp_d_crsp
  } else
    d_crsp = rbind(d_crsp,temp_d_crsp)
} # for year in seq

# convert ret to pct
d_crsp = d_crsp %>%
    mutate(
        ret = 100*ret
    )


## Calculate passive within-month gains 
d_crsp = data.table(d_crsp)

# create month index
d_crsp = d_crsp[
  , temp := as.Date(date)
        ][
  , yyyymm := year(temp)*100 + month(temp)
][
  , !c('temp')
]
setkey(d_crsp, c('permno','yyyymm')) # not sure this helps

# find passive gain within months (in place) 
d_crsp = d_crsp[
  !is.na(ret)
][
  order(permno,date)
][
  , passgainm := shift(ret, fill=0, type='lag'), by = c('permno','yyyymm')
][
  , passgainm := cumprod(1+passgainm/100), by=c('permno','yyyymm')
] 

write_fst(d_crsp, paste0(pathProject,'Portfolios/Data/Intermediate/d_crsp.fst'))

rm(d_crsp, m_crsp, m_crsp2)
