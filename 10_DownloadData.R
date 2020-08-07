## Settings previously in .RProfile
library(RPostgres)
if (!exists("wrds")) {
  wrds <- dbConnect(Postgres(),
                    host='wrds-pgdata.wharton.upenn.edu',
                    port=9737,
                    dbname='wrds',
                    user=rstudioapi::askForPassword("Database username"),
                    password=rstudioapi::askForPassword("Database password"),
                    sslmode='require')
}



## Packages and settings --------------------------------------------------
options(stringsAsFactors = FALSE)
library(tidyverse)
library(readxl)
library(lubridate)

numRowsToPull = -1  # Set to -1 to get all data, set to positive value for testing


# Compustat annual --------------------------------------------------------

# Variables to download
varsCompustatA = c("aco", "act", "ajex", "am", "ao", "ap", "at", "capx", "ceq", "che", "cogs", "csho", "cshrc", "dcpstk", "dcvt", "dlc", "dlcch", "dltis", 
                    "dltr", "dltt", "dm", "dp", "drc", "drlt", "dv", "dvc", "dvp", "dvpa", "dvpd", "dvpsx_c", "dvt", "ebit", "ebitda", "emp", "epspi", "epspx", 
                    "fatb", "fatl", "ffo", "fincf", "fopt", "gdwl", "gdwlia", "gdwlip", "gwo", "ib", "ibc", "intan", "invt",
                    "ivao", "ivncf", "ivst", "lco", "lct", "lo", "lt", "mib", "msa", "ni", "nopi", "oancf", "ob", "oiadp", "oibdp", "pi", "ppegt",
                    "ppent", "prcc_c", "prcc_f", "prstkc", "prstkcc", "pstk", "pstkl", "pstkrv",  "re", "rect", "recta", "revt", "sale", "scstkc", "seq", "spi", 
                    "sstk", "tstkp", "txdi", "txditc", "txfo", "txfed", "txp", "txt", "xacc", "xad", "xint", "xrd", "xpp", "xsga"
)

a_Compustat = 
  # Build query
  paste0("a.", varsCompustatA) %>% 
  paste0(collapse = ',') %>% 
  paste0("select a.gvkey, a.datadate, a.conm, a.fyear, a.tic, a.cusip, a.naicsh, a.sich, ", 
         .,
         " from COMP.FUNDA as a
           where a.consol = 'C'
           and a.popsrc = 'D'
           and a.datafmt = 'STD'
           and a.curcd = 'USD'
           and a.indfmt = 'INDL' ", collapse = "") %>% 
  str_replace_all("[\r\n]" , "") %>% 
  # Send query
  dbSendQuery(conn = wrds, statement = .) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(a_Compustat, file = '../DataRaw/CompustatAnnual.csv')



# Compustat Quarterly -----------------------------------------------------

# Variables to download
varsCompustatQ = c("acoq", "actq", "ajexq", "apq", "atq", "ceqq", "cheq", "cogsq", "cshoq", "cshprq", "dpq", "dlcq", "dlttq", 
                   "drcq", "drltq", "dvpsxq", "epspiq", "epspxq", "fopty", "gdwlq", "ibq", "invtq", "intanq", "ivaoq", "lcoq", "lctq", 
                   "loq", "ltq", "mibq", "niq", "oancfy", "oiadpq", "oibdpq", "piq", "ppentq", "ppegtq", "prstkcy", "prccq", "pstkq", "rdq", "req",
                   "rectq", "revtq", "saleq", "seqq", "sstky", "txdiq", 
                   "txditcq", "txpq", "txtq", "xaccq", "xintq", "xsgaq", "xrdq")

q_Compustat = 
  # Build query
  paste0("a.", varsCompustatQ) %>% 
  paste0(collapse = ',') %>% 
  paste0("select a.gvkey, a.datadate, a.fyearq, a.fqtr, a.datacqtr, a.datafqtr, ", 
         .,
         " from COMP.FUNDQ as a
           where a.consol = 'C'
           and a.popsrc = 'D'
           and a.datafmt = 'STD'
           and a.curcdq = 'USD'  -- Only USD?
           and a.indfmt = 'INDL' ", collapse = "") %>% 
  str_replace_all("[\r\n]" , "") %>% 
  # Send query
  dbSendQuery(conn = wrds, statement = .) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(q_Compustat, file = '../DataRaw/CompustatQuarterly.csv')


# Compustat pensions ------------------------------------------------------

pensions = dbSendQuery(conn = wrds, 
                       statement = 
                         "select a.gvkey, a.datadate, a.paddml, a.pbnaa, a.pbnvv, a.pbpro, a.pbpru, a.pcupsu, a.pplao, a.pplau
                     from comp.aco_pnfnda as a
                     where a.indfmt = 'INDL'
                     and a.popsrc = 'D'
                     and a.datafmt = 'STD'
                     and a.consol = 'C'
                     "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(pensions, file = '../DataRaw/CompustatPensions.csv')




# Compustat segments ------------------------------------------------------

segments = dbSendQuery(conn = wrds, statement = 
                         "select a.gvkey, a.datadate, a.stype, a.sid, a.sales, a.srcdate, a.naicsh, a.sics1, a.snms
                       from compseg.wrds_segmerged as a
                       "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(segments, file = '../DataRaw/CompustatSegmentData.csv')


# Compustat Customer Segments ---------------------------------------------

seg_customer = dbSendQuery(
  conn=wrds,
  statement="select a.*
  from compseg.wrds_seg_customer as a 
  "
) %>% 
  dbFetch(res, n = numRowsToPull) %>% 
  mutate(datadate = srcdate) %>% 
  select(-srcdate)

data.table::fwrite(seg_customer, file = '../DataRaw/CompustatSegmentDataCustomers.csv')

# Compustat short interest ------------------------------------------------

shortinterest = dbSendQuery(conn = wrds, 
                            statement = 
                              "select a.gvkey, a.iid, a.shortint, a.shortintadj, a.datadate
                       from comp.sec_shortint as a
                       "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(shortinterest, file = '../DataRaw/CompustatShortInterest.csv')




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
  dbFetch(n = numRowsToPull)

data.table::fwrite(m_crsp, file = '../DataRaw/mCRSP.csv')


# CRSP Distributions ------------------------------------------------------
m_dist = dbSendQuery(conn = wrds, statement = 
                       "select d.permno, d.divamt, d.distcd, d.facshr, d.rcrddt
                     from crsp.msedist as d") %>% 
  dbFetch(n = numRowsToPull)

data.table::fwrite(m_dist, file = '../DataRaw/mCRSPdistributions.csv')


# CRSP daily --------------------------------------------------------------

d_crsp = dbSendQuery(conn = wrds, statement = 
                       "select a.permno, a.date, a.ret, a.vol, a.shrout, a.prc, a.cfacshr
                     from crsp.dsf as a
                     "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(d_crsp, file = '../DataRaw/d_CRSP.csv')



# Credit ratings ----------------------------------------------------------

ratings = dbSendQuery(conn = wrds, statement = 
                        "select gvkey, datadate, splticrm -- , spsdrm, spsticrm 
                     from comp.adsprate
                     -- where splticrm is not null"
)  %>%
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(ratings, file = '../DataRaw/ratings.csv')


# CRSP acquisitions -------------------------------------------------------

acq = dbSendQuery(conn = wrds, statement = 
                    "select a.permno, a.distcd, a.exdt, a.acperm
                      from crsp.msedist as a
                      "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(acq, file = '../DataRaw/mCRSPDistributionInfo.csv')

# IBES --------------------------------------------------------------------

# EPS analyst expectations
eps = dbSendQuery(conn = wrds, 
                  statement = 
                 "
                  select a.ticker, a.statpers, a.measure, a.fpi, a.numest, a.medest, 
                         a.meanest, a.stdev, a.fpedats, a.actual, a.anndats_act
                  from ibes.statsum_epsus as a
                  where a.fpi = '0' or a.fpi = '1' or a.fpi = '6'
                 "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(eps, file = '../DataRaw/IBES.csv')


# EPS unadjusted actuals
epsAct = dbSendQuery(conn = wrds, 
                  statement = 
                    "
                  select a.ticker, a.statpers, a.measure, a.int0a, a.shout, a.fy0a
                  from ibes.actpsumu_epsus as a
                  where measure = 'EPS'
                  "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(epsAct, file = '../DataRaw/IBESUnadjustedActuals.csv')


# IBES analyst recommendations file
recd = dbSendQuery(conn = wrds, 
                     statement = 
                       "
                       select a.ticker, a.estimid, a.ereccd, a.etext, a.ireccd, a.itext, a.emaskcd, 
                              a.amaskcd, a.anndats
                       from ibes.recddet as a
                       where a.usfirm = '1'
                       "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(recd, file = '../DataRaw/IBES_Recommendations.csv')




# Linking tables ----------------------------------------------------------

# Manual attempt
# ccm = dbSendQuery(conn = wrds, 
#                   statement = 
#                     "
#                      select distinct a.gvkey, a.conm, a.tic, a.cusip, -- a.cik, a.sich, a.naicsh, -- a.tsymbol, (tsymbol adds duplicates)
#                             b.lpermno, b.lpermco, b.linkdt, b.linkenddt, b.liid, b.linkprim
#                      from compd.funda as a, crsp.ccmxpf_lnkhist as b
#                      where a.gvkey=b.gvkey 
#                      and b.linkprim in ('P', 'C') 
#                      and b.LINKTYPE in ('LU', 'LC') 
#                      and a.datadate>= b.linkdt 
#                      and (a.datadate <= b.linkenddt or b.linkenddt is null) 
#                      and a.consol = 'C'
#                      and a.popsrc = 'D'
#                      and a.datafmt = 'STD'
#                      and a.curcd = 'USD'
#                      and a.indfmt = 'INDL'
#                      "
# ) %>% 
#   # Pull data
#   dbFetch(n = -1) %>% 
#   # If more than one row for lpermno, date range, keep prioritized link
#   distinct()

# Replicating WRDS web interface query (see email correspondence with WRDS)
ccm = dbSendQuery(conn = wrds, 
                  statement = 
                    "
                     select a.gvkey, a.conm, a.tic, a.cusip, a.cik, a.sic, a.naics, b.linkprim, b.linktype, b.liid,
                            b.lpermno, b.lpermco, b.linkdt, b.linkenddt
                     from comp.names as a
                     inner join crsp.ccmxpf_lnkhist as b
                     on a.gvkey = b.gvkey
                     where b.linktype in ('LC', 'LU')
                     and b.linkprim in ('P', 'C')
                     order by a.gvkey
                     "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull) 


data.table::fwrite(ccm, file = '../DataRaw/CCMLinkingTable.csv')


# IPO dates ---------------------------------------------------------------
tmp <- tempfile()
download.file('https://site.warrington.ufl.edu/ritter/files/2019/05/age19752019.xlsx', 
              destfile = tmp, 
              method = 'curl')
 
ipos = read_excel(path = tmp) %>% 
  transmute(Founding = Founding,
            Offerdate = `Offer date`,
            CRSPperm = `CRSP perm`)
  
data.table::fwrite(ipos, file = '../DataRaw/IPODates.csv')

# FRED data ---------------------------------------------------------------

# CPI
cpi = fredr(series_id = 'CPIAUCSL') %>% 
  select(-series_id)

data.table::fwrite(cpi, file = '../DataRaw/CPI.csv')

# GNP deflator
gnpdefl  = fredr(series_id = 'GNPCTPI') %>% 
  select(-series_id)

data.table::fwrite(gnpdefl, file = '../DataRaw/GNPCTPI.csv')


# Broker-Dealer financial assets and liabilities
temp = fredr(series_id = 'BOGZ1FL664090005Q') %>% 
  transmute(date,
            assets = value) %>% 
  full_join(fredr(series_id = 'BOGZ1FL664190005Q') %>% 
              transmute(date, 
                        liab = value)) %>% 
  full_join(fredr(series_id = 'BOGZ1FL665080003Q') %>% 
              transmute(date, 
                        equity = value)) %>% 
  filter(year(date) >= 1968) %>%
  mutate(
    lev = assets/equity  # /(assets-liab)
    , levfacnsa = log(lev) - log(dplyr::lag(lev,1))
    , qtr = quarter(date)
    , year = year(date)
  )

## compute seasonal adjustment
temp0 = temp
tempw1 = temp0 %>% 
  select(year,levfacnsa,qtr) %>%
  spread(qtr,levfacnsa)

tempmat = tempw1[,2:5] %>% as.matrix
rownames(tempmat) = tempw1$year

qtrmeanavail = array(0L,dim(tempmat))
for (t in seq(3,dim(tempmat)[1])){
  qtrmeanavail[t,] = colMeans(tempmat[1:t-1,],na.rm=T)
}

## adjust in wide matrix format and reshape back (last step)
tempmatsa = tempmat - qtrmeanavail
tempw2 = tempmatsa %>% as.data.frame %>%
  mutate(year = rownames(tempmatsa))

templong = tempw2 %>%
  gather(qtr,levfac,-year) %>%
  mutate(year = as.numeric(year), qtr = as.numeric(qtr)) %>%
  arrange(year,qtr)

brokerLev = templong %>% filter(!is.na(levfac))

data.table::fwrite(brokerLev, file = '../DataRaw/brokerLev.csv')


# 3-month T-bill rate (quarterly)
temp = fredr(series_id = 'TB3MS', 
             frequency = 'q',
             aggregation_method = 'avg') %>% 
  transmute(
    TbillRate3M = value/100
  , qtr = quarter(date)
  , year = year(date))

data.table::fwrite(temp, file = '../DataRaw/TBill3M.csv')

# VIX data
vix = fredr(series_id = 'VXOCLS') %>% 
  select(-series_id)

data.table::fwrite(vix, file = '../DataRaw/VIX.csv')

# Factors (Fama French, Liquidity) ----------------------------------------

# Daily
dff = dbSendQuery(conn = wrds, 
                  statement = 
                    "
                     select date, mktrf, smb, hml, rf, umd 
                     from ff.factors_daily
                     "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(dff, file = '../DataRaw/dFamaFrench.csv')


# Monthly
mff = dbSendQuery(conn = wrds, 
                  statement = 
                    "
                     select date, mktrf, smb, hml, rf, umd 
                     from ff.factors_monthly
                     "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(mff, file = '../DataRaw/mFamaFrench.csv')

# Liquidity factor (Use more recent data from Pastor's website?)
# https://faculty.chicagobooth.edu/lubos.pastor/research/liq_data_1962_2018.txt

mLiquidity = dbSendQuery(conn = wrds, 
                         statement = 
                           "
                         select date, ps_innov 
                         from ff.liq_ps
                         "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(mLiquidity, file = '../DataRaw/mLiquidityFactor.csv')

# Market returns ----------------------------------------------------------

# Value-weighted and equal-weighted market returns from CRSP (monthly)
mMarket = dbSendQuery(conn = wrds, 
                  statement = 
                    "
                     select date, vwretd, ewretd, usdval 
                     from crsp.msi
                     "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(mMarket, file = '../DataRaw/mMarket.csv')

# Value-weighted and equal-weighted market returns from CRSP (daily)
dMarket = dbSendQuery(conn = wrds, 
                      statement = 
                        "
                      select date, vwretd, ewretd, usdval 
                      from crsp.dsi
                      "
) %>% 
  # Pull data
  dbFetch(n = numRowsToPull)

data.table::fwrite(dMarket, file = '../DataRaw/dMarket.csv')



# OptionMetrics  --------------------------------------------------------

# in a separate file because it's so involved
# takes about 3 hours
# tic = proc.time()
# source("11_DownloadOptionsAndProcess.R")
# timer_min = (proc.time() - tic)/60
# timer_min


# 13F data ----------------------------------------------------------------

# also in a separate file because it's so involved
# takes about 20 min
# print("13f download and process")
# tic = proc.time()
# source("1c_Download13FAndProcess.R")
# timer_min = (proc.time() - tic)/60
# timer_min


# Patent citation data ----------------------------------------------------

tmp <- tempfile()
# Download 1
download.file("http://www.nber.org/~jbessen/dynass.dta.zip",
              destfile = tmp,
              method = 'auto')

dynass = haven::read_dta(unz(tmp,"dynass.dta"))

data.table::fwrite(dynass, file = '../DataRaw/dynass.csv')

# Download 2
download.file("http://www.nber.org/~jbessen/cite76_06.dta.zip",
              destfile = tmp,
              method = 'auto')

cite76_06 = haven::read_dta(unz(tmp,"cite76_06.dta"))

data.table::fwrite(cite76_06, file = '../DataRaw/cite76_06.csv')

# Download 3
download.file("http://www.nber.org/~jbessen/pat76_06_assg.dta.zip",
              destfile = tmp,
              method = 'auto')

pat76_06_assg = haven::read_dta(unz(tmp,"pat76_06_assg.dta"))

data.table::fwrite(pat76_06_assg, file = '../DataRaw/pat76_06_assg.csv')


# Q Factor Model ----------------------------------------------------------

df = read.csv(file = 'http://global-q.org/uploads/1/2/2/6/122679606/q5_factors_daily_2019.csv') %>% 
  select(-R_EG)

data.table::fwrite(df, file = '../DataRaw/D_qfactor.csv')


# Input-Output data -------------------------------------------------------

# Make table before 1997
download.file("https://apps.bea.gov/industry/xls/io-annual/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx",
              destfile = '../DataRaw/IOMake_Before_Redefinitions_1963-1996_Summary.xlsx', 
              mode = 'wb')

# Use table before 1997
download.file("https://apps.bea.gov/industry/xls/io-annual/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx",
              destfile = '../DataRaw/IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx', 
              mode = 'wb')

# Tables starting in 1997
tmp = tempfile()
download.file("https://apps.bea.gov//industry/iTables%20Static%20Files/AllTablesSUP.zip",
              destfile = tmp, 
              method = 'auto')

unzip(tmp, 
      files = c('Supply_1997-2018_SUM.xlsx', 'Use_SUT_Framework_1997-2018_SUM.xlsx'),
      exdir = '../DataRaw')



# Sin stock classification ------------------------------------------------

# These data are originally from the pdf available here:
# http://www.columbia.edu/~hh2679/sinstocks.pdf
download.file('https://drive.google.com/uc?export=download&id=1U0xQw9CwKJAVZYHbur8p_jj24vLtVwBu',
              destfile = '../DataRaw/SinStocksHong.xlsx',
              mode = 'wb')

# PIN data ----------------------------------------------------------------

# These data are originally from here: https://sites.google.com/site/hvidkjaer/data
download.file('https://drive.google.com/uc?export=download&id=15RU_gxWS0rZ8Jyq7MFAno3cLKbB1_P0T',
              destfile = '../DataRaw/pin1983-2001.dat')
