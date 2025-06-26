# DataDownloads Script Documentation

## A_CCMLinkingTable.do

### 1. CCMLinkingTable.csv

Size: 3.11 MB
Rows: 31,875
Columns: 14

All Columns:
  1. gvkey <dbl>             2. conm <chr>             3. tic <chr>
  4. cusip <chr>             5. cik <dbl>              6. sic <dbl>
  7. naics <dbl>             8. linkprim <chr>         9. linktype <chr>
 10. liid <chr>             11. lpermno <dbl>         12. lpermco <dbl>
 13. linkdt <chr>           14. linkenddt <chr>

Sample Data:
```
  gvkey conm            tic    cusip     cik      sic   ... linktype liid  lpermno lpermco linkdt    linkenddt
  <dbl> <chr>           <chr>  <chr>     <dbl>    <dbl> ... <chr>    <chr> <dbl>   <dbl>   <chr>     <chr>    
1  1000 A & E PLASTIK … AE.2   000032102 NA        3089 ... LU       01      25881   23369 13nov1970 30jun1978
2  1001 A & M FOOD SER… AMFD.  000165100 7.24e+05  5812 ... LU       01      10015    6398 20sep1983 31jul1986
3  1002 AAI CORP        AAIC.1 000352104 1.31e+06  3825 ... LC       01      10023   22159 14dec1972 05jun1973
4  1003 A.A. IMPORTING… ANTQ   000354100 7.30e+05  5712 ... LU       01      10031    6672 07dec1983 16aug1989
```
... with 31,871 more rows

IDENTIFIERS:
- stock: lpermno
- time: linkdt

### 2. CCMLinkingTable.dta

Size: 2.74 MB
Rows: 31,875
Columns: 14

All Columns:
  1. gvkey <chr>             2. conm <chr>             3. tic <chr>
  4. cusip <chr>             5. cik <chr>              6. sic <chr>
  7. naics <chr>             8. linkprim <chr>         9. linktype <chr>
 10. liid <chr>             11. permno <dbl>          12. lpermco <dbl>
 13. timeLinkStart_d <date> 14. timeLinkEnd_d <date>

Sample Data:
```
  gvkey  conm            tic    cusip     cik        sic   naics  linkprim linktype liid  permno lpermco timeLinkStart_d timeLinkEnd_d
  <chr>  <chr>           <chr>  <chr>     <chr>      <chr> <chr>  <chr>    <chr>    <chr> <dbl>  <dbl>   <date>          <date>       
1 001000 A & E PLASTIK … AE.2   000032102            3089         P        LU       01     25881   23369 1970-11-13      1978-06-30   
2 001001 A & M FOOD SER… AMFD.  000165100 0000723576 5812  722    P        LU       01     10015    6398 1983-09-20      1986-07-31   
3 001002 AAI CORP        AAIC.1 000352104 0001306124 3825         C        LC       01     10023   22159 1972-12-14      1973-06-05   
4 001003 A.A. IMPORTING… ANTQ   000354100 0000730052 5712  442110 C        LU       01     10031    6672 1983-12-07      1989-08-16   
```
... with 31,871 more rows

IDENTIFIERS:
- stock: gvkey
- time: timeLinkStart_d

## B_CompustatAnnual.do

### 3. CompustatAnnual.csv

Size: 222.87 MB
Rows: 516,269
Columns: 110

All Columns:
  1. gvkey <dbl>              2. datadate <chr>           3. conm <chr>
  4. fyear <dbl>              5. tic <chr>               6. cusip <chr>
  7. naicsh <dbl>             8. sich <dbl>              9. aco <dbl>
 10. act <dbl>              11. ajex <dbl>             12. am <dbl>
 13. ao <dbl>               14. ap <dbl>               15. at <dbl>
 16. capx <dbl>             17. ceq <dbl>              18. ceqt <dbl>
 19. che <dbl>              20. cogs <dbl>             21. csho <dbl>
 ... (110 columns total)

Sample Data:
```
  gvkey datadate  conm            fyear tic   cusip     ... xacc  xad   xint  xrd   xpp   xsga 
  <dbl> <chr>     <chr>           <dbl> <chr> <chr>     ... <dbl> <dbl> <dbl> <dbl> <dbl> <dbl>
1  1000 31dec1961 A & E PLASTIK …  1961 AE.2  000032102 ... NA    NA    NA    NA    NA    NA   
2  1000 31dec1962 A & E PLASTIK …  1962 AE.2  000032102 ... NA    NA     0.01 NA    NA    NA   
3  1000 31dec1963 A & E PLASTIK …  1963 AE.2  000032102 ... NA    NA     0.02 NA    NA    0.346
4  1000 31dec1964 A & E PLASTIK …  1964 AE.2  000032102 ... NA    NA    0.033 NA    NA    0.431
```
... with 516,265 more rows

IDENTIFIERS:
- stock: gvkey
- time: datadate

### 4. a_aCompustat.dta

Size: 265.25 MB
Rows: 302,232
Columns: 122

All Columns:
  1. gvkey <dbl>              2. datadate <date>          3. conm <chr>
  4. fyear <dbl>              5. tic <chr>               6. cusip <chr>
  7. naicsh <dbl>             8. sich <dbl>              9. aco <dbl>
 10. act <dbl>              11. ajex <dbl>             12. am <dbl>
 13. ao <dbl>               14. ap <dbl>               15. at <dbl>
 16. capx <dbl>             17. ceq <dbl>              18. ceqt <dbl>
 19. che <dbl>              20. cogs <dbl>             21. csho <dbl>
 ... (122 columns total)

Sample Data:
```
  gvkey datadate   conm            fyear tic   cusip     ... cik   sic   naics permno lpermco time_avail_m
  <dbl> <date>     <chr>           <dbl> <chr> <chr>     ... <chr> <chr> <chr> <dbl>  <dbl>   <date>      
1  1000 1970-12-31 A & E PLASTIK …  1970 AE.2  000032102 ...       3089         25881   23369 1971-06-01  
2  1000 1971-12-31 A & E PLASTIK …  1971 AE.2  000032102 ...       3089         25881   23369 1972-06-01  
3  1000 1972-12-31 A & E PLASTIK …  1972 AE.2  000032102 ...       3089         25881   23369 1973-06-01  
4  1000 1973-12-31 A & E PLASTIK …  1973 AE.2  000032102 ...       3089         25881   23369 1974-06-01  
```
... with 302,228 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

### 5. m_aCompustat.dta

Size: 3180.02 MB
Rows: 3,624,363
Columns: 122

All Columns:
  1. gvkey <dbl>              2. datadate <date>          3. conm <chr>
  4. fyear <dbl>              5. tic <chr>               6. cusip <chr>
  7. naicsh <dbl>             8. sich <dbl>              9. aco <dbl>
 10. act <dbl>              11. ajex <dbl>             12. am <dbl>
 13. ao <dbl>               14. ap <dbl>               15. at <dbl>
 ... (122 columns total)

Sample Data:
```
  gvkey datadate   conm            fyear tic   cusip     ... cik   sic   naics  permno lpermco time_avail_m
  <dbl> <date>     <chr>           <dbl> <chr> <chr>     ... <chr> <chr> <chr>  <dbl>  <dbl>   <date>      
1 13007 1986-10-31 OPTIMUM MANUFA…  1986 OMFGA 683916100 ...       3942  339931  10000    7952 1987-04-01  
2 13007 1986-10-31 OPTIMUM MANUFA…  1986 OMFGA 683916100 ...       3942  339931  10000    7952 1987-05-01  
3 13007 1986-10-31 OPTIMUM MANUFA…  1986 OMFGA 683916100 ...       3942  339931  10000    7952 1987-06-01  
4 13007 1986-10-31 OPTIMUM MANUFA…  1986 OMFGA 683916100 ...       3942  339931  10000    7952 1987-07-01  
```
... with 3,624,359 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## C_CompustatQuarterly.do

### 6. m_QCompustat.dta

Size: 2531.93 MB
Rows: 5,429,199
Columns: 68

All Columns:
  1. gvkey <dbl>              2. datadateq <date>         3. fyearq <dbl>
  4. fqtr <dbl>               5. datacqtr <chr>           6. datafqtr <chr>
  7. acoq <dbl>               8. actq <dbl>              9. ajexq <dbl>
 10. aoq <dbl>              11. apq <dbl>              12. atq <dbl>
 13. capxq <dbl>            14. ceqq <dbl>             15. cheq <dbl>
 ... (68 columns total)

Sample Data:
```
  gvkey datadateq  fyearq fqtr  datacqtr datafqtr ... capxy time_avail_m sstkyq prstkcyq oancfyq foptyq
  <dbl> <date>     <dbl>  <dbl> <chr>    <chr>    ... <dbl> <date>       <dbl>  <dbl>    <dbl>   <dbl> 
1  1000 1966-03-31   1966     1 1966Q1   1966Q1   ... NA    1966-06-01      0.0      0.0 NA      NA    
2  1000 1966-03-31   1966     1 1966Q1   1966Q1   ... NA    1966-07-01      0.0      0.0 NA      NA    
3  1000 1966-03-31   1966     1 1966Q1   1966Q1   ... NA    1966-08-01      0.0      0.0 NA      NA    
4  1000 1966-06-30   1966     2 1966Q2   1966Q2   ... NA    1966-09-01      0.0      0.0 NA      NA    
```
... with 5,429,195 more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## D_CompustatPensions.do

### 7. CompustatPensions.dta

Size: 10.07 MB
Rows: 105,133
Columns: 8

All Columns:
  1. gvkey <chr>              2. datadate <date>          3. paddml <dbl>
  4. pbnaa <dbl>              5. pbnvv <dbl>             6. pbpro <dbl>
  7. pbpru <dbl>              8. pcupsu <dbl>

Sample Data:
```
  gvkey datadate   paddml pbnaa pbnvv pbpro pbpru pcupsu
  <chr> <date>     <dbl>  <dbl> <dbl> <dbl> <dbl> <dbl>
1 001003 1988-12-31  0.109 0.103 0.108   0.2  0.05  0.026
2 001003 1989-12-31  0.126 0.111 0.136  0.24  0.05  0.027
3 001003 1990-12-31  0.178 0.178 0.148  0.13  0.05   0.04
4 001003 1991-12-31  0.222 0.186 0.177  0.18  0.05  0.038
```
... with 105,129 more rows

IDENTIFIERS:
- stock: gvkey
- time: datadate

## E_CompustatBusinessSegments.do

### 8. CompustatSegments.dta

Size: 387.82 MB
Rows: 2,766,341
Columns: 9

All Columns:
  1. gvkey <dbl>              2. datadate <date>          3. stype <chr>
  4. sid <dbl>                5. sales <dbl>             6. srcdate <date>
  7. naicsh <dbl>             8. sics1 <dbl>             9. snms <chr>

Sample Data:
```
  gvkey datadate   stype  sid   sales  srcdate    naicsh sics1 snms
  <dbl> <date>     <chr>  <dbl> <dbl>  <date>     <dbl>  <dbl> <chr>
1  1000 1976-12-31 BUSSEG    10  45.34 1977-03-15 NA     3089 INJECTION MOLDED PLASTIC PRODUCTS
2  1000 1977-12-31 BUSSEG    10  47.03 1978-03-13 NA     3089 INJECTION MOLDED PLASTIC PRODUCTS
3  1000 1978-12-31 BUSSEG    10  34.36 1979-03-14 NA     3089 INJECTION MOLDED PLASTIC PRODUCTS
4  1000 1979-12-31 BUSSEG    10  37.75 1980-03-19 NA     3089 INJECTION MOLDED PLASTIC PRODUCTS
```
... with 2,766,337 more rows

IDENTIFIERS:
- stock: gvkey
- time: datadate

## F_CompustatCustomerSegments.do

### 9. CompustatSegmentDataCustomers.csv

Size: 9.12 MB
Rows: 61,175
Columns: 13

All Columns:
  1. gvkey <dbl>              2. datadate <chr>           3. stype <chr>
  4. sid <dbl>                5. cnms <chr>              6. srcdate <chr>
  7. salecs <dbl>             8. opscs <dbl>             9. cnms2 <chr>
 10. cnms3 <chr>            11. cnms4 <chr>            12. cnms5 <chr>
 13. cnms6 <chr>

Sample Data:
```
  gvkey datadate  stype   sid   cnms              srcdate   salecs opscs cnms2
  <dbl> <chr>     <chr>   <dbl> <chr>             <chr>     <dbl>  <dbl> <chr>
1  1001 19850731 COUSEG     10 U.S. GOVERNMENT  19851115   1.9   NA    NA
2  1001 19860731 COUSEG     10 U.S. GOVERNMENT  19861020   4.3   NA    NA
3  1001 19870731 COUSEG     10 U.S. GOVERNMENT  19871022   5.6   NA    NA
4  1001 19880731 COUSEG     10 U.S. GOVERNMENT  19881019   8.1   NA    NA
```
... with 61,171 more rows

IDENTIFIERS:
- stock: gvkey
- time: datadate

## G_CompustatShortInterest.do

### 10. monthlyShortInterest.dta

Size: 49.29 MB
Rows: 859,088
Columns: 4

All Columns:
  1. gvkey <dbl>              2. time_m <date>            3. shortint <dbl>
  4. shortintadj <dbl>

Sample Data:
```
  gvkey time_m     shortint shortintadj
  <dbl> <date>     <dbl>    <dbl>
1  1000 1988-07-31  0.03     0.03
2  1000 1988-08-31  0.03     0.03
3  1000 1988-09-30  0.03     0.03
4  1000 1988-10-31  0.03     0.03
```
... with 859,084 more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## H_CRSPDistributions.do

### 11. CRSPdistributions.dta

Size: 65.17 MB
Rows: 1,447,772
Columns: 7

All Columns:
  1. permno <dbl>             2. distcd <dbl>             3. divamt <dbl>
  4. facshr <dbl>             5. dclrdt <date>           6. exdt <date>
  7. rcrddt <date>

Sample Data:
```
  permno distcd divamt facshr dclrdt     exdt       rcrddt
  <dbl>  <dbl>  <dbl>  <dbl>  <date>     <date>     <date>
1  10001   1232   0.25   1.0  1972-05-26 1972-06-15 1972-06-01
2  10001   1232   0.25   1.0  1972-08-25 1972-09-15 1972-09-01
3  10001   1232   0.25   1.0  1972-11-24 1972-12-15 1972-12-01
4  10001   1232   0.25   1.0  1973-02-23 1973-03-15 1973-03-01
```
... with 1,447,768 more rows

IDENTIFIERS:
- stock: permno
- time: exdt

## I_CRSPmonthly.do

### 12. mCRSP.csv

Size: 274.87 MB
Rows: 4,219,648
Columns: 7

All Columns:
  1. permno <dbl>             2. date <chr>               3. ret <dbl>
  4. retx <dbl>               5. vol <dbl>               6. prc <dbl>
  7. shrout <dbl>

Sample Data:
```
  permno date     ret    retx   vol    prc    shrout
  <dbl>  <chr>    <dbl>  <dbl>  <dbl>  <dbl>  <dbl>
1  10001 19720131  0.087  0.087    18   6.25  1600
2  10001 19720229 -0.040 -0.040    15   6.00  1600
3  10001 19720331  0.083  0.083    10   6.50  1600
4  10001 19720428 -0.038 -0.038    25   6.25  1600
```
... with 4,219,644 more rows

IDENTIFIERS:
- stock: permno
- time: date

### 13. monthlyCRSP.dta

Size: 417.71 MB
Rows: 4,219,648
Columns: 9

All Columns:
  1. permno <dbl>             2. time_m <date>            3. ret <dbl>
  4. retx <dbl>               5. vol <dbl>               6. prc <dbl>
  7. shrout <dbl>             8. mve_c <dbl>             9. exchcd <dbl>

Sample Data:
```
  permno time_m     ret    retx   vol    prc    shrout mve_c  exchcd
  <dbl>  <date>     <dbl>  <dbl>  <dbl>  <dbl>  <dbl>  <dbl>  <dbl>
1  10001 1972-01-31  0.087  0.087    18   6.25  1600   10.0     3
2  10001 1972-02-29 -0.040 -0.040    15   6.00  1600    9.6     3
3  10001 1972-03-31  0.083  0.083    10   6.50  1600   10.4     3
4  10001 1972-04-28 -0.038 -0.038    25   6.25  1600   10.0     3
```
... with 4,219,644 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## I2_CRSPmonthlyraw.do

### 14. monthlyCRSPraw.dta

Size: 417.71 MB
Rows: 4,219,648
Columns: 9

All Columns:
  1. permno <dbl>             2. time_m <date>            3. ret <dbl>
  4. retx <dbl>               5. vol <dbl>               6. prc <dbl>
  7. shrout <dbl>             8. mve_c <dbl>             9. exchcd <dbl>

Sample Data:
```
  permno time_m     ret    retx   vol    prc    shrout mve_c  exchcd
  <dbl>  <date>     <dbl>  <dbl>  <dbl>  <dbl>  <dbl>  <dbl>  <dbl>
1  10001 1972-01-31  0.087  0.087    18   6.25  1600   10.0     3
2  10001 1972-02-29 -0.040 -0.040    15   6.00  1600    9.6     3
3  10001 1972-03-31  0.083  0.083    10   6.50  1600   10.4     3
4  10001 1972-04-28 -0.038 -0.038    25   6.25  1600   10.0     3
```
... with 4,219,644 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## J_CRSPdaily.do

### 15. dailyCRSP.dta

Size: 3901.67 MB
Rows: 107,662,961
Columns: 7

All Columns:
  1. permno <dbl>             2. time_d <date>            3. ret <dbl>
  4. vol <dbl>                5. shrout <dbl>            6. prc <dbl>
  7. cfacpr <dbl>

Sample Data:
```
  permno time_d     ret     vol      shrout   prc    cfacpr
  <dbl>  <date>     <dbl>   <dbl>    <dbl>    <dbl>  <dbl>
1  10006 1932-01-02 -0.0185      200      600  6.625   7.26
2  10014 1932-01-02 -0.0783 1.90e+03 1.44e+03  13.25   1.05
3  10022 1932-01-02 -0.0213        0      200    -23      9
4  10030 1932-01-02  0.1552        0      628 -16.75 2.3957
```
... with 107,662,957 more rows

IDENTIFIERS:
- stock: permno
- time: time_d

### 16. dailyCRSPprc.dta

Size: 2784.86 MB
Rows: 107,662,961
Columns: 5

All Columns:
  1. permno <dbl>             2. time_d <date>            3. prc <dbl>
  4. shrout <dbl>             5. cfacpr <dbl>

Sample Data:
```
  permno time_d     prc    shrout cfacpr
  <dbl>  <date>     <dbl>  <dbl>  <dbl>
1  10006 1932-01-02  6.625    600   7.26
2  10014 1932-01-02  13.25   1440   1.05
3  10022 1932-01-02    -23    200      9
4  10030 1932-01-02 -16.75    628 2.3957
```
... with 107,662,957 more rows

IDENTIFIERS:
- stock: permno
- time: time_d

## K_CRSPAcquisitions.do

### 17. m_CRSPAcquisitions.dta

Size: 0.03 MB
Rows: 5,632
Columns: 2

All Columns:
1. permno <dbl>
  2. SpinoffCo <dbl>

Sample Data:
```
permno SpinoffCo
  <dbl>  <dbl>    
1  35263         1
2  10569         1
3  23588         1
4  13856         1
```
... with more rows

IDENTIFIERS:
- stock: permno

## L_IBES_EPS_Unadj.do

### 18. IBES_EPS_Unadj.dta

Size: 284.23 MB
Rows: 7,842,868
Columns: 9

All Columns:
1. tickerIBES <chr>
  2. statpers <date>
  3. fpi <chr>
  4. numest <dbl>
  5. medest <dbl>
  6. meanest <dbl>
  7. stdev <dbl>
  8. fpedats <date>
  9. time_avail_m <date>

Sample Data:
```
tickerIBES statpers   fpi   numest medest meanest stdev fpedats    time_avail_m
  <chr>      <date>     <chr> <dbl>  <dbl>  <dbl>   <dbl> <date>     <date>      
1 0000       2014-04-17 1          4   0.51    0.52  0.03 2014-12-31 2014-04-01  
2 0000       2014-05-15 1          4   0.58    0.56  0.04 2014-12-31 2014-05-01  
3 0000       2014-06-19 1          4   0.58    0.56  0.04 2014-12-31 2014-06-01  
4 0000       2014-07-17 1          3   0.58    0.56  0.05 2014-12-31 2014-07-01
```
... with more rows

IDENTIFIERS:
- stock: tickerIBES
- time: time_avail_m

## L2_IBES_EPS_Adj.do

### 19. IBES_EPS_Adj.dta

Size: 918.78 MB
Rows: 14,596,983
Columns: 14

All Columns:
1. fpi <chr>
  2. tickerIBES <chr>
  3. statpers <date>
  4. fpedats <date>
  5. anndats_act <date>
  6. meanest <dbl>
  7. actual <dbl>
  8. medest <dbl>
  9. stdev <dbl>
 10. numest <dbl>
 11. prdays <date>
 12. price <dbl>
 13. shout <dbl>
 14. time_avail_m <date>

Sample Data:
```
fpi   tickerIBES statpers   fpedats    anndats_act meanest actual medest stdev numest prdays     price shout  time_avail_m
  <chr> <chr>      <date>     <date>     <date>      <dbl>   <dbl>  <dbl>  <dbl> <dbl>  <date>     <dbl> <dbl>  <date>      
1 1     0000       2014-04-17 2014-12-31 2015-01-30     0.52   1.21   0.51  0.03      4 2014-04-16 13.75 72.276 2014-04-01  
2 1     0000       2014-05-15 2014-12-31 2015-01-30     0.56   1.21   0.58  0.04      4 2014-05-14  13.3 69.978 2014-05-01  
3 1     0000       2014-06-19 2014-12-31 2015-01-30     0.56   1.21   0.58  0.04      4 2014-06-18  14.4 69.992 2014-06-01  
4 1     0000       2014-07-17 2014-12-31 2015-01-30     0.56   1.21   0.58  0.05      3 2014-07-16 14.11 69.992 2014-07-01
```
... with more rows

IDENTIFIERS:
- stock: tickerIBES
- time: time_avail_m

## M_IBES_Recommendations.do

### 20. IBES_Recommendations.dta

Size: 54.40 MB
Rows: 864,089
Columns: 11

All Columns:
1. tickerIBES <chr>
  2. amaskcd <dbl>
  3. anndats <date>
  4. time_avail_m <date>
  5. ireccd <dbl>
  6. estimid <chr>
  7. ereccd <chr>
  8. etext <chr>
  9. itext <chr>
 10. emaskcd <dbl>
 11. actdats <date>

Sample Data:
```
tickerIBES amaskcd anndats    time_avail_m ireccd estimid  ereccd etext      itext      emaskcd actdats   
  <chr>      <dbl>   <date>     <date>       <dbl>  <chr>    <chr>  <chr>      <chr>      <dbl>   <date>    
1 0000         71182 2014-03-10 2014-03-01        2 RBCDOMIN 2      OUTPERFORM BUY            659 2014-03-10
2 0000         79092 2014-03-10 2014-03-01        2 JPMORGAN        OVERWEIGHT BUY           1243 2014-03-11
3 0000        119962 2014-03-09 2014-03-01        2 KEEFE    2      OUTPERFORM BUY           1308 2014-03-11
4 0000         80474 2014-03-10 2014-03-01        1 RAYMOND  1      STRONG BUY STRONG BUY    1929 2014-03-11
```
... with more rows

IDENTIFIERS:
- stock: tickerIBES
- time: time_avail_m

## N_IBES_UnadjustedActuals.do

### 21. IBES_UnadjustedActuals.dta

Size: 320.77 MB
Rows: 2,669,344
Columns: 19

All Columns:
1. tickerIBES <chr>
  2. cusip <chr>
  3. oftic <chr>
  4. cname <chr>
  5. measure <chr>
  6. fy0a <dbl>
  7. curcode <chr>
  8. fvyrgro <dbl>
  9. fvyrsta <dbl>
 10. usfirm <dbl>
 11. fy0edats <date>
 12. int0a <dbl>
 13. int0dats <date>
 14. price <dbl>
 15. prdays <date>
 16. shoutIBESUnadj <dbl>
 17. iadiv <dbl>
 18. curr_price <chr>
 19. time_avail_m <date>

Sample Data:
```
tickerIBES cusip    oftic cname           measure fy0a  curcode fvyrgro fvyrsta usfirm fy0edats   int0a int0dats   price prdays     shoutIBESUnadj iadiv curr_price time_avail_m
  <chr>      <chr>    <chr> <chr>           <chr>   <dbl> <chr>   <dbl>   <dbl>   <dbl>  <date>     <dbl> <date>     <dbl> <date>     <dbl>          <dbl> <chr>      <date>      
1 0000       87482X10 TLMR  TALMER BANCORP… EPS     NA    USD     NA      NA           1 2013-12-31 NA    2013-12-31 13.75 2014-04-16         72.276 NA    USD        2014-04-01  
2 0000       87482X10 TLMR  TALMER BANCORP… EPS     NA    USD     NA      NA           1 2013-12-31  0.12 2014-03-31  13.3 2014-05-14         69.978 NA    USD        2014-05-01  
3 0000       87482X10 TLMR  TALMER BANCORP… EPS     NA    USD     NA      NA           1 2013-12-31  0.12 2014-03-31  14.4 2014-06-18         69.992 NA    USD        2014-06-01  
4 0000       87482X10 TLMR  TALMER BANCORP… EPS     NA    USD     NA      NA           1 2013-12-31  0.12 2014-03-31 14.11 2014-07-16         69.992 NA    USD        2014-07-01
```
... with more rows

IDENTIFIERS:
- stock: tickerIBES
- time: time_avail_m

## O_Daily_Fama-French.do

### 22. dailyFF.dta

Size: 1.04 MB
Rows: 25,982
Columns: 6

All Columns:
1. time_d <date>
  2. mktrf <dbl>
  3. smb <dbl>
  4. hml <dbl>
  5. rf <dbl>
  6. umd <dbl>

Sample Data:
```
time_d     mktrf  smb     hml     rf     umd  
  <date>     <dbl>  <dbl>   <dbl>   <dbl>  <dbl>
1 1926-07-01 0.0009 -0.0025 -0.0027 0.0001 NA   
2 1926-07-02 0.0045 -0.0033 -0.0006 0.0001 NA   
3 1926-07-06 0.0017   0.003 -0.0039 0.0001 NA   
4 1926-07-07 0.0009 -0.0058  0.0002 0.0001 NA
```
... with more rows

IDENTIFIERS:
- time: time_d

## P_Monthly_Fama-French.do

### 23. monthlyFF.dta

Size: 0.05 MB
Rows: 1,186
Columns: 6

All Columns:
1. mktrf <dbl>
  2. smb <dbl>
  3. hml <dbl>
  4. rf <dbl>
  5. umd <dbl>
  6. time_avail_m <date>

Sample Data:
```
mktrf   smb     hml     rf     umd   time_avail_m
  <dbl>   <dbl>   <dbl>   <dbl>  <dbl> <date>      
1  0.0289 -0.0255 -0.0239 0.0022 NA    1926-07-01  
2  0.0264 -0.0114  0.0381 0.0025 NA    1926-08-01  
3  0.0038 -0.0136  0.0005 0.0023 NA    1926-09-01  
4 -0.0327 -0.0014  0.0082 0.0032 NA    1926-10-01
```
... with more rows

IDENTIFIERS:
- time: time_avail_m

## Q_MarketReturns.do

### 24. monthlyMarket.dta

Size: 0.03 MB
Rows: 1,189
Columns: 4

All Columns:
1. vwretd <dbl>
  2. ewretd <dbl>
  3. usdval <dbl>
  4. time_avail_m <date>

Sample Data:
```
vwretd ewretd  usdval   time_avail_m
  <dbl>  <dbl>   <dbl>    <date>      
1 NA     NA      NA       1925-12-01  
2 0.0006  0.0232 2.74e+07 1926-01-01  
3 -0.033 -0.0535 2.76e+07 1926-02-01  
4 -0.064 -0.0968 2.67e+07 1926-03-01
```
... with more rows

IDENTIFIERS:
- time: time_avail_m

## R_MonthlyLiquidityFactor.do

### 25. monthlyLiquidity.dta

Size: 0.01 MB
Rows: 749
Columns: 2

All Columns:
1. ps_innov <dbl>
  2. time_avail_m <date>

Sample Data:
```
ps_innov time_avail_m
  <dbl>    <date>      
1   0.0043 1962-08-01  
2   0.0118 1962-09-01  
3   -0.074 1962-10-01  
4   0.0282 1962-11-01
```
... with more rows

IDENTIFIERS:
- time: time_avail_m

## S_QFactorModel.do

### 26. d_qfactor.dta

Size: 0.31 MB
Rows: 13,340
Columns: 6

All Columns:
1. r_f_qfac <dbl>
  2. r_mkt_qfac <dbl>
  3. r_me_qfac <dbl>
  4. r_ia_qfac <dbl>
  5. r_roe_qfac <dbl>
  6. time_d <date>

Sample Data:
```
r_f_qfac r_mkt_qfac r_me_qfac r_ia_qfac      r_roe_qfac   time_d    
  <dbl>    <dbl>      <dbl>     <dbl>          <dbl>        <date>    
1 0.000187   0.000767  0.004675       0.001528    -0.007185 1967-01-03
2 0.000187   0.001548  -0.00356 -0.00042199998    -0.002235 1967-01-04
3 0.000187   0.012869  0.004346      -0.005605     0.000651 1967-01-05
4 0.000187   0.007257  0.006548       0.008974 0.0035569998 1967-01-06
```
... with more rows

IDENTIFIERS:
- time: time_d

## T_VIX.do

### 27. d_vix.dta

Size: 0.10 MB
Rows: 10,293
Columns: 3

All Columns:
1. time_d <date>
  2. vix <dbl>
  3. dVIX <dbl>

Sample Data:
```
time_d     vix   dVIX       
  <date>     <dbl> <dbl>      
1 1986-01-02 18.07 NA         
2 1986-01-03 17.96 -0.11000061
3 1986-01-06 17.05 -0.90999985
4 1986-01-07 17.39  0.34000015
```
... with more rows

IDENTIFIERS:
- time: time_d

## U_GNPDeflator.do

### 28. GNPdefl.dta

Size: 0.01 MB
Rows: 939
Columns: 2

All Columns:
1. time_avail_m <date>
  2. gnpdefl <dbl>

Sample Data:
```
time_avail_m gnpdefl    
  <date>       <dbl>      
1 1947-04-01   0.111269996
2 1947-05-01   0.111269996
3 1947-06-01   0.111269996
4 1947-07-01   0.112799995
```
... with more rows

IDENTIFIERS:
- time: time_avail_m

## V_TBill3M.do

### 29. TBill3M.dta

Size: 0.00 MB
Rows: 366
Columns: 3

All Columns:
1. TbillRate3M <dbl>
  2. qtr <dbl>
  3. year <dbl>

Sample Data:
```
TbillRate3M  qtr   year 
  <dbl>        <dbl> <dbl>
1       0.0053     1  1934
2       0.0015     2  1934
3 0.0018000001     3  1934
4       0.0025     4  1934
```
... with more rows

IDENTIFIERS:
- time: time_avail_m

## W_BrokerDealerLeverage.do

### 30. brokerLev.dta

Size: 0.00 MB
Rows: 229
Columns: 3

All Columns:
1. qtr <dbl>
  2. year <dbl>
  3. levfac <dbl>

Sample Data:
```
qtr   year  levfac      
  <dbl> <dbl> <dbl>       
1     1  1968 NA          
2     2  1968  0.023065105
3     3  1968    0.0799101
4     4  1968 -0.029995056
```
... with more rows

IDENTIFIERS:
- time: time_avail_m

## X_SPCreditRatings.do

### 31. m_SP_creditratings.dta

Size: 20.19 MB
Rows: 3,023,652
Columns: 3

All Columns:
1. gvkey <dbl>
  2. time_avail_m <date>
  3. credrat <dbl>

Sample Data:
```
gvkey time_avail_m credrat
  <dbl> <date>       <dbl>  
1  1003 2004-06-01         0
2  1003 2004-07-01         0
3  1003 2004-08-01         0
4  1003 2004-09-01         0
```
... with more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## X2_CIQCreditRatings.do

### 32. m_CIQ_creditratings.dta

Size: 16.61 MB
Rows: 229,090
Columns: 11

All Columns:
1. gvkey <dbl>
  2. ticker <chr>
  3. ratingdate <date>
  4. ratingtime <date>
  5. ratingactionword <chr>
  6. currentratingsymbol <chr>
  7. entity_id <chr>
  8. instrument_id <chr>
  9. security_id <chr>
 10. source <dbl>
 11. time_avail_m <date>

Sample Data:
```
gvkey ticker ratingdate ratingtime ratingactionword currentratingsymbol entity_id instrument_id security_id source time_avail_m
  <dbl> <chr>  <date>     <date>     <chr>           <chr>           <chr>     <chr>         <chr>       <dbl>  <date>      
1  1004 ARZ    1987-05-28 1960-01-01 New Rating      BBB             109880                                   1 1987-05-01  
2  1004 ARZ    1989-08-14 1960-01-01 New Rating      BBB prelim                206198                         2 1989-08-01  
3  1004 ARZ    1989-10-26 1960-01-01 New Rating      BBB                                     14               3 1989-10-01  
4  1004 ARZ    1991-08-27 1960-01-01 New Rating      BBB prelim                206197                         2 1991-08-01
```
... with more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## ZA_IPODates.do

### 33. IPODates.dta

*File not found in Data/Intermediate/ directory*

IDENTIFIERS:
- stock: ticker

## ZB_PIN.do

### 34. pin_monthly.dta

Size: 7.53 MB
Rows: 254,472
Columns: 10

All Columns:
1. permno <dbl>
  2. year <dbl>
  3. a <dbl>
  4. eb <dbl>
  5. es <dbl>
  6. u <dbl>
  7. d <dbl>
  8. month <dbl>
  9. modate <date>
 10. time_avail_m <date>

Sample Data:
```
permno year  a          eb        es        u         d         month modate     time_avail_m
  <dbl>  <dbl> <dbl>      <dbl>     <dbl>     <dbl>     <dbl>     <dbl> <date>     <date>      
1  10057  1993 0.23012744 5.4697137 5.7433333 10.506811 0.6051814     1 1993-01-01 1993-12-01  
2  10057  1993 0.23012744 5.4697137 5.7433333 10.506811 0.6051814     2 1993-02-01 1994-01-01  
3  10057  1993 0.23012744 5.4697137 5.7433333 10.506811 0.6051814     3 1993-03-01 1994-02-01  
4  10057  1993 0.23012744 5.4697137 5.7433333 10.506811 0.6051814     4 1993-04-01 1994-03-01
```
... with more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZC_GovernanceIndex.do

### 35. GovIndex.dta

Size: 3.91 MB
Rows: 511,674
Columns: 3

All Columns:
1. ticker <chr>
  2. G <dbl>
  3. time_avail_m <date>

Sample Data:
```
ticker G     time_avail_m
  <chr>  <dbl> <date>      
1 A          7 2002-01-01  
2 A          7 2002-02-01  
3 A          7 2002-03-01  
4 A          7 2002-04-01
```
... with more rows

IDENTIFIERS:
- stock: ticker
- time: time_avail_m

## ZD_CorwinSchultz.do

### 36. BAspreadsCorwin.dta

Size: 42.74 MB
Rows: 4,481,622
Columns: 3

All Columns:
1. permno <dbl>
  2. BidAskSpread <dbl>
  3. time_avail_m <date>

Sample Data:
```
permno BidAskSpread time_avail_m
  <dbl>  <dbl>        <date>      
1  10001  0.054474052 1986-09-01  
2  10001  0.038854547 1986-10-01  
3  10001  0.054440375 1986-11-01  
4  10001   0.04141999 1986-12-01
```
... with more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZE_13F.do

### 37. TR_13F.dta

Size: 52.43 MB
Rows: 2,617,435
Columns: 7

All Columns:
1. permno <dbl>
  2. numinstown <dbl>
  3. dbreadth <dbl>
  4. instown_perc <dbl>
  5. maxinstown_perc <dbl>
  6. numinstblock <dbl>
  7. time_avail_m <date>

Sample Data:
```
permno numinstown dbreadth instown_perc maxinstown_perc numinstblock time_avail_m
  <dbl>  <dbl>      <dbl>    <dbl>        <dbl>           <dbl>        <date>      
1  10001          1 NA              8.073        8.072654            1 1986-09-01  
2  10001          1 NA              8.073        8.072654            1 1986-10-01  
3  10001          1 NA              8.073        8.072654            1 1986-11-01  
4  10001          1      0.0        8.073        8.072654            1 1986-12-01
```
... with more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZF_CRSPIBESLink.do

### 38. IBESCRSPLinkingTable.dta

Size: 0.21 MB
Rows: 21,602
Columns: 2

All Columns:
1. tickerIBES <chr>
  2. permno <dbl>

Sample Data:
```
tickerIBES permno
  <chr>      <dbl> 
1 GFGC        10001
2 BTFG        10002
3 GCBK        10003
4 GACO        10008
```
... with more rows

IDENTIFIERS:
- stock: permno

## ZG_BidaskTAQ.do

### 39. hf_spread.dta

Size: 31.12 MB
Rows: 3,262,927
Columns: 3

All Columns:
1. permno <dbl>
  2. time_avail_m <date>
  3. hf_spread <dbl>

Sample Data:
```
permno time_avail_m hf_spread
  <dbl>  <date>       <dbl>    
1  10001 1987-01-01   3.9747007
2  10001 1987-02-01   3.8981328
3  10001 1987-03-01   6.3723655
4  10001 1987-06-01    8.661661
```
... with more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZH_OptionMetrics.do

### 40. OptionMetricsVolume.dta

Size: 15.54 MB
Rows: 1,163,966
Columns: 4

All Columns:
1. secid <dbl>
  2. optvolume <dbl>
  3. optinterest <dbl>
  4. time_avail_m <date>

Sample Data:
```
secid optvolume optinterest time_avail_m
  <dbl> <dbl>     <dbl>       <date>      
1  5005      1166       70852 1996-01-01  
2  5005      1253       43744 1996-02-01  
3  5005      1326       42539 1996-03-01  
4  5005      3393       56422 1996-04-01
```
... with more rows

IDENTIFIERS:
- stock: secid
- time: time_avail_m

### 41. OptionMetricsVolSurf.dta

Size: 110.10 MB
Rows: 4,617,772
Columns: 7

All Columns:
1. secid <dbl>
  2. days <dbl>
  3. delta <dbl>
  4. cp_flag <chr>
  5. time_avail_m <date>
  6. date <chr>
  7. impl_vol <dbl>

Sample Data:
```
secid days  delta cp_flag time_avail_m date       impl_vol
  <dbl> <dbl> <dbl> <chr>   <date>       <chr>      <dbl>   
1  5005    30    50 C       1996-01-01   1996-01-31 0.549704
2  5005    30    50 C       1996-02-01   1996-02-29 0.664595
3  5005    30    50 C       1996-03-01   1996-03-29 0.784875
4  5005    30    50 C       1996-04-01   1996-04-30 0.874362
```
... with more rows

IDENTIFIERS:
- stock: secid
- time: time_avail_m

### 42. OptionMetricsXZZ.dta

Size: 5.84 MB
Rows: 611,701
Columns: 3

All Columns:
1. secid <dbl>
  2. time_avail_m <date>
  3. skew1 <dbl>

Sample Data:
```
secid time_avail_m skew1      
  <dbl> <date>       <dbl>      
1  5015 1996-01-01      0.053262
2  5015 1996-03-01   -0.02312525
3  5015 1996-04-01      0.005994
4  5015 1996-05-01    0.06860217
```
... with more rows

IDENTIFIERS:
- stock: secid
- time: time_avail_m

### 43. OptionMetricsBH.dta

Size: 68.02 MB
Rows: 2,852,712
Columns: 7

All Columns:
1. secid <dbl>
  2. time_avail_m <date>
  3. cp_flag <chr>
  4. mean_imp_vol <dbl>
  5. mean_day <dbl>
  6. nobs <dbl>
  7. ticker <chr>

Sample Data:
```
secid time_avail_m cp_flag mean_imp_vol mean_day  nobs  ticker
  <dbl> <date>       <chr>   <dbl>        <dbl>     <dbl> <chr> 
1  5005 1996-01-01   BOTH        0.613557      31.0     1 ASTA  
2  5005 1996-01-01   P           0.613557      31.0     1 ASTA  
3  5005 1996-02-01   BOTH       0.5411796      19.2     5 ASTA  
4  5005 1996-02-01   C          0.5790697 19.666666     3 ASTA
```
... with more rows

IDENTIFIERS:
- stock: secid
- time: time_avail_m

## ZI_PatentCitations.do

### 44. PatentDataProcessed.dta

Size: 6.00 MB
Rows: 196,664
Columns: 4

All Columns:
1. gvkey <dbl>
  2. year <dbl>
  3. npat <dbl>
  4. ncitscale <dbl>

Sample Data:
```
gvkey    year     npat  ncitscale
  <dbl>    <dbl>    <dbl> <dbl>    
1 1.00e+03 1.98e+03     4         0
2 1.00e+03 1.98e+03     2         0
3 1.00e+03 1.98e+03     0         0
4 1.00e+03 1.98e+03     0         0
```
... with more rows

IDENTIFIERS:
- stock: gvkey

## ZJ_InputOutputMomentum.do

### 45. InputOutputMomentumProcessed.dta

Size: 110.87 MB
Rows: 2,906,304
Columns: 6

All Columns:
1. gvkey <dbl>
  2. time_avail_m <date>
  3. retmatchcustomer <dbl>
  4. portindcustomer <dbl>
  5. retmatchsupplier <dbl>
  6. portindsupplier <dbl>

Sample Data:
```
gvkey time_avail_m retmatchcustomer portindcustomer retmatchsupplier portindsupplier
  <dbl> <date>       <dbl>           <dbl>           <dbl>           <dbl>          
1  1001 1987-01-01           14.2726               3         13.6843               6
2  1001 1987-02-01           10.0022              10          3.5808               2
3  1001 1987-03-01            3.5746               4          3.1149               2
4  1001 1987-04-01           -1.6125               8         -4.3245               2
```
... with more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## ZK_CustomerMomentum.do

### 46. customerMom.dta

Size: 4.08 MB
Rows: 356,600
Columns: 3

All Columns:
1. permno <dbl>
  2. custmom <dbl>
  3. time_avail_m <date>

Sample Data:
```
permno custmom   time_avail_m
  <dbl>  <dbl>     <date>      
1  76823  0.173333 1976-12-01  
2  76823 -0.090909 1977-01-01  
3  76823    0.0025 1977-02-01  
4  76823  0.113924 1977-03-01
```
... with more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZL_CRSPOPTIONMETRICS.do

### 47. OPTIONMETRICSCRSPLinkingTable.dta

Size: 0.23 MB
Rows: 26,392
Columns: 3

All Columns:
1. secid <dbl>
  2. permno <dbl>
  3. om_score <dbl>

Sample Data:
```
secid  permno om_score
  <dbl>  <dbl>  <dbl>   
1 104332  10001        0
2 110326  10002        0
3   6774  10009        0
4   6518  10011        1
```
... with more rows

IDENTIFIERS:
- stock: permno

