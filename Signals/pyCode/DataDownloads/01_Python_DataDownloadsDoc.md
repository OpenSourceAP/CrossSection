# Python DataDownloads Script Documentation

*Generated on: 2025-06-28 09:52:16*

This document provides comprehensive documentation of Python scripts in the DataDownloads directory and their output files.

## A_CCMLinkingTable.py

CRSP-Compustat Linking Table download script.

### 1. CCMLinkingTable.csv

Size: 3.17 MB
Rows: 1,000
Columns: 14

All Columns:
   1. gvkey <int64>          2. conm <object>          3. tic <object>         
   4. cusip <object>         5. cik <float64>          6. sic <int64>          
   7. naics <float64>        8. linkprim <object>      9. linktype <object>    
  10. liid <object>         11. lpermno <int64>       12. lpermco <float64>    
  13. linkdt <object>       14. linkenddt <object>   

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> conm <chr> tic <chr> cusip <chr> cik <chr> sic <chr> ...
1         1000 A & E PLASTI         AE.2        32102           NA         3089          ...
2         1001 A & M FOOD S        AMFD.       165100     7.24e+05         5812          ...
3         1002     AAI CORP       AAIC.1       352104     1.31e+06         3825          ...
4         1003 A.A. IMPORTI         ANTQ       354100     7.30e+05         5712          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: timeLinkStart_d
### 2. CCMLinkingTable.parquet

Size: 1.95 MB
Rows: 31,879
Columns: 14

All Columns:
   1. gvkey <string>         2. conm <string>          3. tic <string>         
   4. cusip <string>         5. cik <string>           6. sic <string>         
   7. naics <string>         8. linkprim <string>      9. linktype <string>    
  10. liid <string>         11. permno <double>       12. lpermco <double>     
  13. timeLinkStart_d <timestamp[ns]> 14. timeLinkEnd_d <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> conm <chr> tic <chr> cusip <chr> cik <chr> sic <chr> ...
1       001000 A & E PLASTI         AE.2    000032102                      3089          ...
2       001001 A & M FOOD S        AMFD.    000165100   0000723576         5812          ...
3       001002     AAI CORP       AAIC.1    000352104   0001306124         3825          ...
4       001003 A.A. IMPORTI         ANTQ    000354100   0000730052         5712          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: timeLinkStart_d

## B_CompustatAnnual.py

Compustat Annual data download script.

### 1. CompustatAnnual.csv

Size: 0.27 MB
Rows: 524
Columns: 110

All Columns:
   1. gvkey <int64>          2. datadate <object>      3. conm <object>        
   4. fyear <int64>          5. tic <object>           6. cusip <object>       
   7. naicsh <float64>       8. sich <float64>         9. aco <float64>        
  10. act <float64>         11. ajex <float64>        12. am <float64>         
  13. ao <float64>          14. ap <float64>          15. at <float64>         
  16. capx <float64>        17. ceq <float64>         18. ceqt <float64>       
  19. che <float64>         20. cogs <float64>        21. csho <float64>       
  22. cshrc <float64>       23. dcpstk <float64>      24. dcvt <float64>       
  25. dlc <float64>         26. dlcch <float64>       27. dltis <float64>      
  28. dltr <float64>        29. dltt <float64>        30. dm <float64>         
  31. dp <float64>          32. drc <float64>         33. drlt <float64>       
  34. dv <float64>          35. dvc <float64>         36. dvp <float64>        
  37. dvpa <float64>        38. dvpd <float64>        39. dvpsx_c <float64>    
  40. dvt <float64>         41. ebit <float64>        42. ebitda <float64>     
  43. emp <float64>         44. epspi <float64>       45. epspx <float64>      
  46. fatb <float64>        47. fatl <float64>        48. ffo <float64>        
  49. fincf <float64>       50. fopt <float64>        51. gdwl <float64>       
  52. gdwlia <float64>      53. gdwlip <float64>      54. gwo <float64>        
  55. ib <float64>          56. ibcom <float64>       57. intan <float64>      
  58. invt <float64>        59. ivao <float64>        60. ivncf <float64>      
  61. ivst <float64>        62. lco <float64>         63. lct <float64>        
  64. lo <float64>          65. lt <float64>          66. mib <float64>        
  67. msa <float64>         68. ni <float64>          69. nopi <float64>       
  70. oancf <float64>       71. ob <float64>          72. oiadp <float64>      
  73. oibdp <float64>       74. pi <float64>          75. ppenb <float64>      
  76. ppegt <float64>       77. ppenls <float64>      78. ppent <float64>      
  79. prcc_c <float64>      80. prcc_f <float64>      81. prstkc <float64>     
  82. prstkcc <float64>     83. pstk <float64>        84. pstkl <float64>      
  85. pstkrv <float64>      86. re <float64>          87. rect <float64>       
  88. recta <float64>       89. revt <float64>        90. sale <float64>       
  91. scstkc <float64>      92. seq <float64>         93. spi <float64>        
  94. sstk <float64>        95. tstkp <float64>       96. txdb <float64>       
  97. txdi <float64>        98. txditc <float64>      99. txfo <float64>       
  100. txfed <float64>      101. txp <float64>        102. txt <float64>       
  103. wcap <float64>       104. wcapch <float64>     105. xacc <float64>      
  106. xad <float64>        107. xint <float64>       108. xrd <float64>       
  109. xpp <float64>        110. xsga <float64>      

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> datadate <chr> conm <chr> fyear <chr> tic <chr> cusip <chr> ...
1         1000    31dec1970 A & E PLASTI         1970         AE.2        32102          ...
2         1000    31dec1971 A & E PLASTI         1971         AE.2        32102          ...
3         1000    31dec1972 A & E PLASTI         1972         AE.2        32102          ...
4         1000    31dec1973 A & E PLASTI         1973         AE.2        32102          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: datadate
### 2. CompustatAnnual.parquet

Size: 0.28 MB
Rows: 524
Columns: 126

All Columns:
   1. gvkey <string>         2. datadate <timestamp[ns]>  3. conm <string>        
   4. fyear <int64>          5. tic <string>           6. cusip <string>       
   7. naicsh <double>        8. sich <double>          9. aco <double>         
  10. act <double>          11. ajex <double>         12. am <double>          
  13. ao <double>           14. ap <double>           15. at <double>          
  16. capx <double>         17. ceq <double>          18. ceqt <double>        
  19. che <double>          20. cogs <double>         21. csho <double>        
  22. cshrc <double>        23. dcpstk <double>       24. dcvt <double>        
  25. dlc <double>          26. dlcch <double>        27. dltis <double>       
  28. dltr <double>         29. dltt <double>         30. dm <double>          
  31. dp <double>           32. drc <double>          33. drlt <double>        
  34. dv <double>           35. dvc <double>          36. dvp <double>         
  37. dvpa <double>         38. dvpd <null>           39. dvpsx_c <double>     
  40. dvt <double>          41. ebit <double>         42. ebitda <double>      
  43. emp <double>          44. epspi <double>        45. epspx <double>       
  46. fatb <double>         47. fatl <double>         48. ffo <null>           
  49. fincf <double>        50. fopt <double>         51. gdwl <double>        
  52. gdwlia <double>       53. gdwlip <double>       54. gwo <null>           
  55. ib <double>           56. ibcom <double>        57. intan <double>       
  58. invt <double>         59. ivao <double>         60. ivncf <double>       
  61. ivst <double>         62. lco <double>          63. lct <double>         
  64. lo <double>           65. lt <double>           66. mib <double>         
  67. msa <double>          68. ni <double>           69. nopi <double>        
  70. oancf <double>        71. ob <double>           72. oiadp <double>       
  73. oibdp <double>        74. pi <double>           75. ppenb <double>       
  76. ppegt <double>        77. ppenls <double>       78. ppent <double>       
  79. prcc_c <double>       80. prcc_f <double>       81. prstkc <double>      
  82. prstkcc <double>      83. pstk <double>         84. pstkl <double>       
  85. pstkrv <double>       86. re <double>           87. rect <double>        
  88. recta <double>        89. revt <double>         90. sale <double>        
  91. scstkc <double>       92. seq <double>          93. spi <double>         
  94. sstk <double>         95. tstkp <double>        96. txdb <double>        
  97. txdi <double>         98. txditc <double>       99. txfo <double>        
  100. txfed <double>       101. txp <double>         102. txt <double>        
  103. wcap <double>        104. wcapch <double>      105. xacc <double>       
  106. xad <double>         107. xint <double>        108. xrd <double>        
  109. xpp <double>         110. xsga <double>        111. cnum <string>       
  112. cik <string>         113. sic <string>         114. naics <string>      
  115. linkprim <string>    116. linktype <string>    117. liid <string>       
  118. permno <double>      119. lpermco <double>     120. timeLinkStart_d <timestamp[ns]>
  121. timeLinkEnd_d <timestamp[ns]> 122. dr <double>          123. dc <double>         
  124. xad0 <double>        125. xint0 <double>       126. xsga0 <double>      

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> datadate <chr> conm <chr> fyear <chr> tic <chr> cusip <chr> ...
1       001000 1970-12-31 0 A & E PLASTI         1970         AE.2    000032102          ...
2       001000 1971-12-31 0 A & E PLASTI         1971         AE.2    000032102          ...
3       001000 1972-12-31 0 A & E PLASTI         1972         AE.2    000032102          ...
4       001000 1973-12-31 0 A & E PLASTI         1973         AE.2    000032102          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: datadate
### 3. a_aCompustat.parquet

Size: 0.28 MB
Rows: 524
Columns: 122

All Columns:
   1. gvkey <int32>          2. datadate <timestamp[ns]>  3. conm <string>        
   4. fyear <int16>          5. tic <string>           6. cusip <string>       
   7. naicsh <double>        8. sich <double>          9. aco <double>         
  10. act <double>          11. ajex <double>         12. am <double>          
  13. ao <double>           14. ap <double>           15. at <double>          
  16. capx <double>         17. ceq <double>          18. ceqt <double>        
  19. che <double>          20. cogs <double>         21. csho <double>        
  22. cshrc <double>        23. dcpstk <double>       24. dcvt <double>        
  25. dlc <double>          26. dlcch <double>        27. dltis <double>       
  28. dltr <double>         29. dltt <double>         30. dm <double>          
  31. dp <double>           32. drc <double>          33. drlt <double>        
  34. dv <double>           35. dvc <double>          36. dvp <double>         
  37. dvpa <double>         38. dvpd <double>         39. dvpsx_c <double>     
  40. dvt <double>          41. ebit <double>         42. ebitda <double>      
  43. emp <double>          44. epspi <double>        45. epspx <double>       
  46. fatb <double>         47. fatl <double>         48. ffo <double>         
  49. fincf <double>        50. fopt <double>         51. gdwl <double>        
  52. gdwlia <double>       53. gdwlip <double>       54. gwo <double>         
  55. ib <double>           56. ibcom <double>        57. intan <double>       
  58. invt <double>         59. ivao <double>         60. ivncf <double>       
  61. ivst <double>         62. lco <double>          63. lct <double>         
  64. lo <double>           65. lt <double>           66. mib <double>         
  67. msa <double>          68. ni <double>           69. nopi <double>        
  70. oancf <double>        71. ob <double>           72. oiadp <double>       
  73. oibdp <double>        74. pi <double>           75. ppenb <double>       
  76. ppegt <double>        77. ppenls <double>       78. ppent <double>       
  79. prcc_c <double>       80. prcc_f <double>       81. prstkc <double>      
  82. prstkcc <double>      83. pstk <double>         84. pstkl <double>       
  85. pstkrv <double>       86. re <double>           87. rect <double>        
  88. recta <double>        89. revt <double>         90. sale <double>        
  91. scstkc <double>       92. seq <double>          93. spi <double>         
  94. sstk <double>         95. tstkp <double>        96. txdb <double>        
  97. txdi <double>         98. txditc <double>       99. txfo <double>        
  100. txfed <double>       101. txp <double>         102. txt <double>        
  103. wcap <double>        104. wcapch <double>      105. xacc <double>       
  106. xad <double>         107. xint <double>        108. xrd <double>        
  109. xpp <double>         110. xsga <double>        111. cnum <string>       
  112. dr <float>           113. dc <double>          114. xint0 <float>       
  115. xsga0 <float>        116. xad0 <float>         117. cik <string>        
  118. sic <string>         119. naics <string>       120. permno <int32>      
  121. lpermco <int32>      122. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> datadate <chr> conm <chr> fyear <chr> tic <chr> cusip <chr> ...
1         1000 1970-12-31 0 A & E PLASTI         1970         AE.2    000032102          ...
2         1000 1971-12-31 0 A & E PLASTI         1971         AE.2    000032102          ...
3         1000 1972-12-31 0 A & E PLASTI         1972         AE.2    000032102          ...
4         1000 1973-12-31 0 A & E PLASTI         1973         AE.2    000032102          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m
### 4. m_aCompustat.parquet

Size: 0.33 MB
Rows: 6,283
Columns: 122

All Columns:
   1. gvkey <int32>          2. datadate <timestamp[ns]>  3. conm <string>        
   4. fyear <int16>          5. tic <string>           6. cusip <string>       
   7. naicsh <double>        8. sich <double>          9. aco <double>         
  10. act <double>          11. ajex <double>         12. am <double>          
  13. ao <double>           14. ap <double>           15. at <double>          
  16. capx <double>         17. ceq <double>          18. ceqt <double>        
  19. che <double>          20. cogs <double>         21. csho <double>        
  22. cshrc <double>        23. dcpstk <double>       24. dcvt <double>        
  25. dlc <double>          26. dlcch <double>        27. dltis <double>       
  28. dltr <double>         29. dltt <double>         30. dm <double>          
  31. dp <double>           32. drc <double>          33. drlt <double>        
  34. dv <double>           35. dvc <double>          36. dvp <double>         
  37. dvpa <double>         38. dvpd <double>         39. dvpsx_c <double>     
  40. dvt <double>          41. ebit <double>         42. ebitda <double>      
  43. emp <double>          44. epspi <double>        45. epspx <double>       
  46. fatb <double>         47. fatl <double>         48. ffo <double>         
  49. fincf <double>        50. fopt <double>         51. gdwl <double>        
  52. gdwlia <double>       53. gdwlip <double>       54. gwo <double>         
  55. ib <double>           56. ibcom <double>        57. intan <double>       
  58. invt <double>         59. ivao <double>         60. ivncf <double>       
  61. ivst <double>         62. lco <double>          63. lct <double>         
  64. lo <double>           65. lt <double>           66. mib <double>         
  67. msa <double>          68. ni <double>           69. nopi <double>        
  70. oancf <double>        71. ob <double>           72. oiadp <double>       
  73. oibdp <double>        74. pi <double>           75. ppenb <double>       
  76. ppegt <double>        77. ppenls <double>       78. ppent <double>       
  79. prcc_c <double>       80. prcc_f <double>       81. prstkc <double>      
  82. prstkcc <double>      83. pstk <double>         84. pstkl <double>       
  85. pstkrv <double>       86. re <double>           87. rect <double>        
  88. recta <double>        89. revt <double>         90. sale <double>        
  91. scstkc <double>       92. seq <double>          93. spi <double>         
  94. sstk <double>         95. tstkp <double>        96. txdb <double>        
  97. txdi <double>         98. txditc <double>       99. txfo <double>        
  100. txfed <double>       101. txp <double>         102. txt <double>        
  103. wcap <double>        104. wcapch <double>      105. xacc <double>       
  106. xad <double>         107. xint <double>        108. xrd <double>        
  109. xpp <double>         110. xsga <double>        111. cnum <string>       
  112. dr <float>           113. dc <double>          114. xint0 <float>       
  115. xsga0 <float>        116. xad0 <float>         117. cik <string>        
  118. sic <string>         119. naics <string>       120. permno <int32>      
  121. lpermco <int32>      122. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> datadate <chr> conm <chr> fyear <chr> tic <chr> cusip <chr> ...
1         1010 1951-04-30 0 ACF INDUSTRI         1950        4165A    00099V004          ...
2         1010 1951-04-30 0 ACF INDUSTRI         1950        4165A    00099V004          ...
3         1010 1951-04-30 0 ACF INDUSTRI         1950        4165A    00099V004          ...
4         1010 1951-04-30 0 ACF INDUSTRI         1950        4165A    00099V004          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## C_CompustatQuarterly.py

Compustat Quarterly data download script.

### 1. m_QCompustat.parquet

Size: 0.38 MB
Rows: 2,981
Columns: 68

All Columns:
   1. gvkey <int64>          2. datadateq <timestamp[ms]>  3. fyearq <int64>       
   4. fqtr <int64>           5. datacqtr <string>      6. datafqtr <string>    
   7. acoq <double>          8. actq <double>          9. ajexq <double>       
  10. apq <double>          11. atq <double>          12. ceqq <double>        
  13. cheq <double>         14. cogsq <double>        15. cshoq <double>       
  16. cshprq <double>       17. dlcq <double>         18. dlttq <double>       
  19. dpq <double>          20. drcq <double>         21. drltq <double>       
  22. dvpsxq <double>       23. dvpq <double>         24. dvy <double>         
  25. epspiq <double>       26. epspxq <double>       27. fopty <double>       
  28. gdwlq <double>        29. ibq <double>          30. invtq <double>       
  31. intanq <double>       32. ivaoq <double>        33. lcoq <double>        
  34. lctq <double>         35. loq <double>          36. ltq <double>         
  37. mibq <double>         38. niq <double>          39. oancfy <double>      
  40. oiadpq <double>       41. oibdpq <double>       42. piq <double>         
  43. ppentq <double>       44. ppegtq <double>       45. prstkcy <double>     
  46. prccq <double>        47. pstkq <double>        48. rdq <timestamp[ms]>  
  49. req <double>          50. rectq <double>        51. revtq <double>       
  52. saleq <double>        53. seqq <double>         54. sstky <double>       
  55. txdiq <double>        56. txditcq <double>      57. txpq <double>        
  58. txtq <double>         59. xaccq <double>        60. xintq <double>       
  61. xsgaq <double>        62. xrdq <double>         63. capxy <double>       
  64. time_avail_m <timestamp[ns]> 65. sstkyq <double>       66. prstkcyq <double>    
  67. oancfyq <double>      68. foptyq <double>      

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> datadateq <chr> fyearq <chr> fqtr <chr> datacqtr <chr> datafqtr <chr> ...
1         1004 1975-02-28 0         1974            3       1975Q1       1974Q3          ...
2         1014 1987-03-31 0         1987            3       1987Q1       1987Q3          ...
3         1012 1987-10-31 0         1987            4       1987Q3       1987Q4          ...
4         1004 2008-11-30 0         2008            2       2008Q4       2008Q2          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m
### 2. CompustatQuarterly.parquet

Size: 0.38 MB
Rows: 2,981
Columns: 68

All Columns:
   1. gvkey <int64>          2. datadateq <timestamp[ms]>  3. fyearq <int64>       
   4. fqtr <int64>           5. datacqtr <string>      6. datafqtr <string>    
   7. acoq <double>          8. actq <double>          9. ajexq <double>       
  10. apq <double>          11. atq <double>          12. ceqq <double>        
  13. cheq <double>         14. cogsq <double>        15. cshoq <double>       
  16. cshprq <double>       17. dlcq <double>         18. dlttq <double>       
  19. dpq <double>          20. drcq <double>         21. drltq <double>       
  22. dvpsxq <double>       23. dvpq <double>         24. dvy <double>         
  25. epspiq <double>       26. epspxq <double>       27. fopty <double>       
  28. gdwlq <double>        29. ibq <double>          30. invtq <double>       
  31. intanq <double>       32. ivaoq <double>        33. lcoq <double>        
  34. lctq <double>         35. loq <double>          36. ltq <double>         
  37. mibq <double>         38. niq <double>          39. oancfy <double>      
  40. oiadpq <double>       41. oibdpq <double>       42. piq <double>         
  43. ppentq <double>       44. ppegtq <double>       45. prstkcy <double>     
  46. prccq <double>        47. pstkq <double>        48. rdq <timestamp[ms]>  
  49. req <double>          50. rectq <double>        51. revtq <double>       
  52. saleq <double>        53. seqq <double>         54. sstky <double>       
  55. txdiq <double>        56. txditcq <double>      57. txpq <double>        
  58. txtq <double>         59. xaccq <double>        60. xintq <double>       
  61. xsgaq <double>        62. xrdq <double>         63. capxy <double>       
  64. time_avail_m <timestamp[ns]> 65. sstkyq <double>       66. prstkcyq <double>    
  67. oancfyq <double>      68. foptyq <double>      

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> datadateq <chr> fyearq <chr> fqtr <chr> datacqtr <chr> datafqtr <chr> ...
1         1004 1975-02-28 0         1974            3       1975Q1       1974Q3          ...
2         1014 1987-03-31 0         1987            3       1987Q1       1987Q3          ...
3         1012 1987-10-31 0         1987            4       1987Q3       1987Q4          ...
4         1004 2008-11-30 0         2008            2       2008Q4       2008Q2          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: None

## D_CompustatPensions.py

Compustat Pensions data download script - Python equivalent of D_CompustatPensions.do

### 1. CompustatPensions.parquet

Size: 0.02 MB
Rows: 998
Columns: 10

All Columns:
   1. gvkey <int64>          2. paddml <double>        3. pbnaa <double>       
   4. pbnvv <double>         5. pbpro <double>         6. pbpru <double>       
   7. pcupsu <double>        8. pplao <double>         9. pplau <double>       
  10. year <int32>         

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> paddml <chr> pbnaa <chr> pbnvv <chr> pbpro <chr> pbpru <chr> ...
1     1.00e+03           NA           NA           NA           NA           NA          ...
2     1.00e+03           NA           NA           NA           NA           NA          ...
3     1.00e+03           NA           NA           NA           NA           NA          ...
4     1.00e+03           NA           NA           NA           NA           NA          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: year

## E_CompustatBusinessSegments.py

Compustat Business Segments data download script - Python equivalent of E_CompustatBusinessSegments.do

### 1. CompustatSegments.parquet

Size: 0.02 MB
Rows: 1,000
Columns: 9

All Columns:
   1. gvkey <int64>          2. datadate <timestamp[ns]>  3. stype <string>       
   4. sid <int64>            5. sales <double>         6. srcdate <timestamp[ns]>
   7. naicsh <double>        8. sics1 <double>         9. snms <string>        

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> datadate <chr> stype <chr> sid <chr> sales <chr> srcdate <chr> ...
1         1000 1976-12-31 0       BUSSEG            1       34.899 1976-12-31 0          ...
2         1000 1976-12-31 0       BUSSEG            2       18.002 1976-12-31 0          ...
3         1000 1976-12-31 0       BUSSEG            3       13.513 1976-12-31 0          ...
4         1000 1977-12-31 0       BUSSEG            1       41.772 1977-12-31 0          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: datadate

## F_CompustatCustomerSegments.py

Compustat Customer Segments data download script - Python equivalent of F_CompustatCustomerSegments.do

### 1. CompustatSegmentDataCustomers.csv

Size: 39.56 MB
Rows: 1,000
Columns: 10

All Columns:
   1. gvkey <int64>          2. cid <int64>            3. cnms <object>        
   4. ctype <object>         5. gareac <object>        6. gareat <object>      
   7. salecs <float64>       8. sid <int64>            9. stype <object>       
  10. datadate <object>    

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> cid <chr> cnms <chr> ctype <chr> gareac <chr> gareat <chr> ...
1         1004            1           NA       GOVDOM           NA           NA          ...
2         1004            1           NA       GOVDOM           NA           NA          ...
3         1004            1           NA       GOVDOM           NA           NA          ...
4         1004            1           NA       GOVDOM           NA           NA          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: datadate

## G_CompustatShortInterest.py

Compustat Short Interest data download script - Python equivalent of G_CompustatShortInterest.do

### 1. monthlyShortInterest.parquet

Size: 0.01 MB
Rows: 481
Columns: 4

All Columns:
   1. gvkey <int64>          2. time_avail_m <timestamp[ns]>  3. shortint <double>    
   4. shortintadj <double> 

Sample Data:
```
   1  2  3  4
  gvkey <chr> time_avail_m <chr> shortint <chr> shortintadj <chr>
1         1004 2006-07-01 0     4.78e+06     4.78e+06
2         1004 2006-08-01 0     6.12e+06     6.12e+06
3         1004 2006-09-01 0     6.01e+06     6.01e+06
4         1004 2006-10-01 0     5.39e+06     5.39e+06
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## H_CRSPDistributions.py

CRSP Distributions data download script - Python equivalent of H_CRSPDistributions.do

### 1. CRSPdistributions.parquet

Size: 13.00 MB
Rows: 1,060,934
Columns: 12

All Columns:
   1. permno <int64>         2. divamt <double>        3. distcd <int64>       
   4. facshr <double>        5. rcrddt <timestamp[ns]>  6. exdt <timestamp[ns]> 
   7. paydt <timestamp[ns]>  8. cd1 <int64>            9. cd2 <int64>          
  10. cd3 <int64>           11. cd4 <int64>           12. __index_level_0__ <int64>

Sample Data:
```
   1  2  3  4  5  6  7
  permno <chr> divamt <chr> distcd <chr> facshr <chr> rcrddt <chr> exdt <chr> ...
1        10001        0.054         1222          0.0 2007-12-10 0 2007-12-06 0          ...
2        10001        0.054         1222          0.0 2008-01-14 0 2008-01-10 0          ...
3        10001        0.036         1222          0.0 2008-02-13 0 2008-02-11 0          ...
4        10001        0.036         1222          0.0 2008-03-13 0 2008-03-11 0          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: exdt

## I2_CRSPmonthlyraw.py

CRSP Monthly Raw data download script - Python equivalent of I2_CRSPmonthlyraw.do

### 1. monthlyCRSPraw.parquet

Size: 150.29 MB
Rows: 5,153,763
Columns: 17

All Columns:
   1. permno <int64>         2. ret <double>           3. retx <double>        
   4. vol <double>           5. shrout <double>        6. prc <double>         
   7. cfacshr <double>       8. bidlo <double>         9. askhi <double>       
  10. shrcd <double>        11. exchcd <double>       12. sicCRSP <double>     
  13. ticker <string>       14. shrcls <string>       15. sic2D <double>       
  16. time_avail_m <timestamp[ns]> 17. mve_c <double>       

Sample Data:
```
   1  2  3  4  5  6  7
  permno <chr> ret <chr> retx <chr> vol <chr> shrout <chr> prc <chr> ...
1        10000           NA           NA           NA           NA           NA          ...
2        10000           NA           NA       0.1771         3.68       -4.375          ...
3        10000    -0.257143    -0.257143       0.0828         3.68        -3.25          ...
4        10000     0.365385     0.365385       0.1078         3.68      -4.4375          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## I_CRSPmonthly.py

CRSP Monthly data download script - Python equivalent of I_CRSPmonthly.do

### 1. mCRSP.csv

Size: 484.04 MB
Rows: 1,000
Columns: 18

All Columns:
   1. permno <int64>         2. permco <int64>         3. date <object>        
   4. ret <float64>          5. retx <float64>         6. vol <float64>        
   7. shrout <float64>       8. prc <float64>          9. cfacshr <float64>    
  10. bidlo <float64>       11. askhi <float64>       12. shrcd <float64>      
  13. exchcd <float64>      14. siccd <float64>       15. ticker <object>      
  16. shrcls <object>       17. dlstcd <float64>      18. dlret <float64>      

Sample Data:
```
   1  2  3  4  5  6  7
  permno <chr> permco <chr> date <chr> ret <chr> retx <chr> vol <chr> ...
1        10000         7952    31dec1985           NA           NA           NA          ...
2        10000         7952    31jan1986           NA           NA     1.77e+03          ...
3        10000         7952    28feb1986    -0.257143    -0.257143        828.0          ...
4        10000         7952    31mar1986     0.365385     0.365385     1.08e+03          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: date
### 2. monthlyCRSP.parquet

Size: 150.93 MB
Rows: 5,153,763
Columns: 17

All Columns:
   1. permno <int64>         2. ret <double>           3. retx <double>        
   4. vol <double>           5. shrout <double>        6. prc <double>         
   7. cfacshr <double>       8. bidlo <double>         9. askhi <double>       
  10. shrcd <double>        11. exchcd <double>       12. sicCRSP <double>     
  13. ticker <string>       14. shrcls <string>       15. sic2D <double>       
  16. time_avail_m <timestamp[ns]> 17. mve_c <double>       

Sample Data:
```
   1  2  3  4  5  6  7
  permno <chr> ret <chr> retx <chr> vol <chr> shrout <chr> prc <chr> ...
1        10000           NA           NA           NA           NA           NA          ...
2        10000           NA           NA       0.1771         3.68       -4.375          ...
3        10000    -0.257143    -0.257143       0.0828         3.68        -3.25          ...
4        10000 0.3653850000     0.365385       0.1078         3.68      -4.4375          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## J_CRSPdaily.py

CRSP Daily data download script - Python equivalent of J_CRSPdaily.do

### 1. dailyCRSP.parquet

Size: 68.51 MB
Rows: 4,136,543
Columns: 7

All Columns:
   1. permno <int32>         2. time_d <timestamp[ns]>  3. ret <double>         
   4. vol <double>           5. shrout <double>        6. prc <double>         
   7. cfacpr <double>      

Sample Data:
```
   1  2  3  4  5  6  7
  permno <chr> time_d <chr> ret <chr> vol <chr> shrout <chr> prc <chr> ...
1        10026 2020-01-02 0    -0.014056     8.83e+04     1.89e+04    181.67999          ...
2        10028 2020-01-02 0     0.022222     4.40e+03     2.69e+04         1.38          ...
3        10032 2020-01-02 0     0.003769     8.21e+04     2.92e+04        77.23          ...
4        10044 2020-01-02 0    -0.019502     1.54e+04     6.00e+03         9.05          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_d
### 2. dailyCRSPprc.parquet

Size: 28.78 MB
Rows: 4,136,543
Columns: 5

All Columns:
   1. permno <int32>         2. time_d <timestamp[ns]>  3. shrout <double>      
   4. prc <double>           5. cfacpr <double>      

Sample Data:
```
   1  2  3  4  5
  permno <chr> time_d <chr> shrout <chr> prc <chr> cfacpr <chr>
1        10026 2020-01-02 0     1.89e+04    181.67999          1.0
2        10028 2020-01-02 0     2.69e+04         1.38          1.0
3        10032 2020-01-02 0     2.92e+04        77.23          1.0
4        10044 2020-01-02 0     6.00e+03         9.05          1.0
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_d

## K_CRSPAcquisitions.py

CRSP Acquisitions data download script - Python equivalent of K_CRSPAcquisitions.do

### 1. m_CRSPAcquisitions.parquet

Size: 0.00 MB
Rows: 8
Columns: 2

All Columns:
   1. permno <int64>         2. SpinoffCo <int64>    

Sample Data:
```
   1  2
  permno <chr> SpinoffCo <chr>
1        35263            1
2        10569            1
3        23588            1
4        13856            1
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: None

## L2_IBES_EPS_Adj.py

IBES EPS Adjusted data download script - Python equivalent of L2_IBES_EPS_Adj.do

### 1. IBES_EPS_Adj.parquet

Size: 139.70 MB
Rows: 14,596,983
Columns: 14

All Columns:
   1. fpi <string>           2. tickerIBES <string>    3. statpers <timestamp[ns]>
   4. fpedats <timestamp[ns]>  5. anndats_act <timestamp[ns]>  6. meanest <double>     
   7. actual <double>        8. medest <double>        9. stdev <double>       
  10. numest <double>       11. prdays <timestamp[ns]> 12. price <double>       
  13. shout <double>        14. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6  7
  fpi <chr> tickerIBES <chr> statpers <chr> fpedats <chr> anndats_act <chr> meanest <chr> ...
1            1         0000 2014-04-17 0 2014-12-31 0 2015-01-30 0         0.52          ...
2            1         0000 2014-05-15 0 2014-12-31 0 2015-01-30 0         0.56          ...
3            1         0000 2014-06-19 0 2014-12-31 0 2015-01-30 0         0.56          ...
4            1         0000 2014-07-17 0 2014-12-31 0 2015-01-30 0         0.56          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: tickerIBES
- time: time_avail_m

## L_IBES_EPS_Unadj.py

IBES EPS Unadjusted data download script - Python equivalent of L_IBES_EPS_Unadj.do

### 1. IBES_EPS_Unadj.parquet

Size: 39.79 MB
Rows: 7,842,868
Columns: 9

All Columns:
   1. tickerIBES <string>    2. statpers <timestamp[ns]>  3. fpi <string>         
   4. numest <double>        5. medest <double>        6. meanest <double>     
   7. stdev <double>         8. fpedats <timestamp[ns]>  9. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6  7
  tickerIBES <chr> statpers <chr> fpi <chr> numest <chr> medest <chr> meanest <chr> ...
1         0000 2014-04-17 0            1          4.0         0.51         0.52          ...
2         0000 2014-05-15 0            1          4.0         0.58         0.56          ...
3         0000 2014-06-19 0            1          4.0         0.58         0.56          ...
4         0000 2014-07-17 0            1          3.0         0.58         0.56          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: tickerIBES
- time: time_avail_m

## M_IBES_Recommendations.py

IBES Recommendations data download script - Python equivalent of M_IBES_Recommendations.do

### 1. IBES_Recommendations.parquet

Size: 10.25 MB
Rows: 864,089
Columns: 11

All Columns:
   1. tickerIBES <string>    2. amaskcd <double>       3. anndats <timestamp[ns]>
   4. time_avail_m <timestamp[ns]>  5. ireccd <double>        6. estimid <string>     
   7. ereccd <string>        8. etext <string>         9. itext <string>       
  10. emaskcd <double>      11. actdats <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6  7
  tickerIBES <chr> amaskcd <chr> anndats <chr> time_avail_m <chr> ireccd <chr> estimid <chr> ...
1         0000     7.12e+04 2014-03-10 0 2014-03-01 0          2.0     RBCDOMIN          ...
2         0000     7.91e+04 2014-03-10 0 2014-03-01 0          2.0     JPMORGAN          ...
3         0000     1.20e+05 2014-03-09 0 2014-03-01 0          2.0        KEEFE          ...
4         0000     8.05e+04 2014-03-10 0 2014-03-01 0          1.0      RAYMOND          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: tickerIBES
- time: time_avail_m

## N_IBES_UnadjustedActuals.py

IBES Unadjusted Actuals data download script - Python equivalent of N_IBES_UnadjustedActuals.do

### 1. IBES_UnadjustedActuals.parquet

Size: 0.03 MB
Rows: 1,018
Columns: 19

All Columns:
   1. time_avail_m <timestamp[ns]>  2. tickerIBES <string>    3. cusip <string>       
   4. oftic <string>         5. cname <string>         6. measure <string>     
   7. fy0a <double>          8. curcode <string>       9. fvyrgro <double>     
  10. fvyrsta <double>      11. usfirm <double>       12. fy0edats <timestamp[ns]>
  13. int0a <double>        14. int0dats <timestamp[ns]> 15. price <double>       
  16. prdays <timestamp[ns]> 17. shoutIBESUnadj <double> 18. iadiv <double>       
  19. curr_price <string>  

Sample Data:
```
   1  2  3  4  5  6  7
  time_avail_m <chr> tickerIBES <chr> cusip <chr> oftic <chr> cname <chr> measure <chr> ...
1 2014-04-01 0         0000     87482X10         TLMR TALMER BANCO          EPS          ...
2 2014-05-01 0         0000     87482X10         TLMR TALMER BANCO          EPS          ...
3 2014-06-01 0         0000     87482X10         TLMR TALMER BANCO          EPS          ...
4 2014-07-01 0         0000     87482X10         TLMR TALMER BANCO          EPS          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: tickerIBES
- time: time_avail_m

## O_Daily_Fama-French.py

Daily Fama-French factors download script - Python equivalent of O_Daily_Fama-French.do

### 1. dailyFF.parquet

Size: 0.02 MB
Rows: 1,000
Columns: 6

All Columns:
   1. time_d <timestamp[ns]>  2. mktrf <double>         3. smb <double>         
   4. hml <double>           5. rf <double>            6. umd <double>         

Sample Data:
```
   1  2  3  4  5  6
  time_d <chr> mktrf <chr> smb <chr> hml <chr> rf <chr> umd <chr>
1 1926-07-01 0       0.0009      -0.0025      -0.0027        9e-05           NA
2 1926-07-02 0       0.0045      -0.0033      -0.0006        9e-05           NA
3 1926-07-06 0       0.0017        0.003      -0.0039        9e-05           NA
4 1926-07-07 0       0.0009      -0.0058       0.0002        9e-05           NA
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: time_d

## P_Monthly_Fama-French.py

Monthly Fama-French factors download script - Python equivalent of P_Monthly_Fama-French.do

### 1. monthlyFF.parquet

Size: 0.03 MB
Rows: 1,000
Columns: 6

All Columns:
   1. mktrf <double>         2. smb <double>           3. hml <double>         
   4. rf <double>            5. umd <double>           6. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6
  mktrf <chr> smb <chr> hml <chr> rf <chr> umd <chr> time_avail_m <chr>
1       0.0289      -0.0255      -0.0239       0.0022           NA 1926-07-01 0
2       0.0264      -0.0114       0.0381       0.0025           NA 1926-08-01 0
3       0.0038      -0.0136       0.0005       0.0023           NA 1926-09-01 0
4      -0.0327      -0.0014       0.0082       0.0032           NA 1926-10-01 0
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: time_avail_m

## Q_MarketReturns.py

Market Returns data download script - Python equivalent of Q_MarketReturns.do

### 1. monthlyMarket.parquet

Size: 0.04 MB
Rows: 1,000
Columns: 4

All Columns:
   1. vwretd <double>        2. ewretd <double>        3. usdval <double>      
   4. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4
  vwretd <chr> ewretd <chr> usdval <chr> time_avail_m <chr>
1           NA           NA           NA 1925-12-01 0
2     0.000561     0.023174     2.74e+07 1926-01-01 0
3    -0.033046     -0.05351     2.76e+07 1926-02-01 0
4    -0.064002    -0.096824     2.67e+07 1926-03-01 0
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: time_avail_m

## R_MonthlyLiquidityFactor.py

Monthly Liquidity Factor download script - Python equivalent of R_MonthlyLiquidityFactor.do

### 1. monthlyLiquidity.parquet

Size: 0.02 MB
Rows: 749
Columns: 2

All Columns:
   1. ps_innov <double>      2. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2
  ps_innov <chr> time_avail_m <chr>
1   0.00426023 1962-08-01 0
2   0.01176268 1962-09-01 0
3  -0.07404113 1962-10-01 0
4   0.02818329 1962-11-01 0
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: time_avail_m

## S_QFactorModel.py

Q Factor Model data download script - Python equivalent of S_QFactorModel.do

### 1. d_qfactor.parquet

Size: 0.05 MB
Rows: 1,000
Columns: 6

All Columns:
   1. r_f_qfac <double>      2. r_mkt_qfac <double>    3. r_me_qfac <double>   
   4. r_ia_qfac <double>     5. r_roe_qfac <double>    6. time_d <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6
  r_f_qfac <chr> r_mkt_qfac <chr> r_me_qfac <chr> r_ia_qfac <chr> r_roe_qfac <chr> time_d <chr>
1 0.0001870000     0.000767     0.004675 0.0015279999    -0.007185 1967-01-03 0
2 0.0001870000     0.001548     -0.00356    -0.000422    -0.002235 1967-01-04 0
3 0.0001870000 0.0128689999     0.004346    -0.005605 0.0006510000 1967-01-05 0
4 0.0001870000     0.007257 0.0065480000     0.008974 0.0035570000 1967-01-06 0
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: time_d

## T_VIX.py

VIX data download script - Python equivalent of T_VIX.do

### 1. d_vix.parquet

Size: 0.02 MB
Rows: 1,000
Columns: 3

All Columns:
   1. time_d <timestamp[ns]>  2. vix <float>            3. dVIX <float>         

Sample Data:
```
   1  2  3
  time_d <chr> vix <chr> dVIX <chr>
1 1986-01-02 0 18.069999694           NA
2 1986-01-03 0 17.959999084 -0.110000610
3 1986-01-06 0 17.049999237 -0.909999847
4 1986-01-07 0 17.389999389 0.3400001525
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: time_d

## U_GNPDeflator.py

GNP Deflator download script - Python equivalent of U_GNPDeflator.do

### 1. GNPdefl.parquet

Size: 0.01 MB
Rows: 939
Columns: 2

All Columns:
   1. time_avail_m <timestamp[ns]>  2. gnpdefl <double>     

Sample Data:
```
   1  2
  time_avail_m <chr> gnpdefl <chr>
1 1947-04-01 0 0.1112700000
2 1947-05-01 0 0.1112700000
3 1947-06-01 0 0.1112700000
4 1947-07-01 0       0.1128
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: time_avail_m

## V_TBill3M.py

3-month T-bill rate download script - Python equivalent of V_TBill3M.do

### 1. TBill3M.parquet

Size: 0.00 MB
Rows: 366
Columns: 3

All Columns:
   1. TbillRate3M <float>    2. qtr <int32>            3. year <int32>         

Sample Data:
```
   1  2  3
  TbillRate3M <chr> qtr <chr> year <chr>
1 0.0052666664          1.0     1.93e+03
2 0.0015333332          2.0     1.93e+03
3 0.0018333332          3.0     1.93e+03
4 0.0025000001          4.0     1.93e+03
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: qtr + year

## W_BrokerDealerLeverage.py

Broker-Dealer Leverage processing - Python equivalent of W_BrokerDealerLeverage.do

### 1. brokerLev.parquet

Size: 0.00 MB
Rows: 229
Columns: 3

All Columns:
   1. qtr <int32>            2. year <int32>           3. levfac <double>      

Sample Data:
```
   1  2  3
  qtr <chr> year <chr> levfac <chr>
1          1.0     1.97e+03           NA
2          2.0     1.97e+03 0.0230650787
3          3.0     1.97e+03 0.0799101497
4          4.0     1.97e+03 -0.029995105
```
... with 1 more rows

IDENTIFIERS:
- stock: None
- time: qtr + year

## X2_CIQCreditRatings.py

CIQ Credit Ratings data download script - Python equivalent of X2_CIQCreditRatings.do

### 1. m_CIQ_creditratings.parquet

Size: 0.03 MB
Rows: 767
Columns: 11

All Columns:
   1. gvkey <int64>          2. ticker <string>        3. ratingdate <timestamp[ns]>
   4. ratingtime <timestamp[ns]>  5. ratingactionword <string>  6. currentratingsymbol <string>
   7. entity_id <string>     8. instrument_id <string>  9. security_id <string> 
  10. source <int64>        11. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6  7
  gvkey <chr> ticker <chr> ratingdate <chr> ratingtime <chr> ratingactionword <chr> currentratingsymbol <chr> ...
1         1004          ARZ 1987-05-28 0 1960-01-01 0   New Rating          BBB          ...
2         1004          ARZ 1989-08-14 0 1960-01-01 0   New Rating   BBB prelim          ...
3         1004          ARZ 1989-10-26 0 1960-01-01 0   New Rating          BBB          ...
4         1004          ARZ 1991-08-27 0 1960-01-01 0   New Rating   BBB prelim          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## X_SPCreditRatings.py

S&P Credit Ratings data download script - Python equivalent of X_SPCreditRatings.do

### 1. m_SP_creditratings.parquet

Size: 0.01 MB
Rows: 1,000
Columns: 3

All Columns:
   1. gvkey <int64>          2. time_avail_m <timestamp[ns]>  3. credrat <int8>       

Sample Data:
```
   1  2  3
  gvkey <chr> time_avail_m <chr> credrat <chr>
1         1003 2004-06-01 0            0
2         1003 2004-07-01 0            0
3         1003 2004-08-01 0            0
4         1003 2004-09-01 0            0
```
... with 1 more rows

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## ZA_IPODates.py

IPO Dates data download script - Python equivalent of ZA_IPODates.do

### 1. IPODates.parquet

Size: 0.02 MB
Rows: 1,000
Columns: 4

All Columns:
   1. permno <double>        2. FoundingYear <double>  3. IPOdate <timestamp[ns]>
   4. __index_level_0__ <int64>

Sample Data:
```
   1  2  3
  permno <chr> FoundingYear <chr> IPOdate <chr>
1     6.79e+04     1.90e+03 1975-01-01 0
2     6.30e+04     1.91e+03 1975-06-01 0
3     5.92e+04     1.90e+03 1975-06-01 0
4     6.20e+04     1.96e+03 1975-07-01 0
```
... with 1 more rows

IDENTIFIERS:
- stock: ticker
- time: None

## ZB_PIN.py

Probability of Informed Trading (PIN) data download script - Python equivalent of ZB_PIN.do

### 1. pin_monthly.parquet

Size: 0.01 MB
Rows: 1,000
Columns: 10

All Columns:
   1. permno <int64>         2. year <double>          3. a <double>           
   4. eb <double>            5. es <double>            6. u <double>           
   7. d <double>             8. month <double>         9. modate <timestamp[ns]>
  10. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4  5  6  7
  permno <chr> year <chr> a <chr> eb <chr> es <chr> u <chr> ...
1        10057     1.99e+03 0.2301274361 5.4697135291 5.7433333972 10.506811190          ...
2        10057     1.99e+03 0.2301274361 5.4697135291 5.7433333972 10.506811190          ...
3        10057     1.99e+03 0.2301274361 5.4697135291 5.7433333972 10.506811190          ...
4        10057     1.99e+03 0.2301274361 5.4697135291 5.7433333972 10.506811190          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZC_GovernanceIndex.py

Governance Index data download script - Python equivalent of ZC_GovernanceIndex.do

### 1. GovIndex.parquet

Size: 0.00 MB
Rows: 1,000
Columns: 3

All Columns:
   1. ticker <string>        2. time_avail_m <timestamp[ns]>  3. G <int8>             

Sample Data:
```
   1  2  3
  ticker <chr> time_avail_m <chr> G <chr>
1          AGE 1990-09-01 0           13
2          AGE 1990-10-01 0           13
3          AGE 1990-11-01 0           13
4          AGE 1990-12-01 0           13
```
... with 1 more rows

IDENTIFIERS:
- stock: ticker
- time: time_avail_m

## ZD_CorwinSchultz.py

Corwin-Schultz bid-ask spread processing - Python equivalent of ZD_CorwinSchultz.do

### 1. BAspreadsCorwin.parquet

Size: 0.02 MB
Rows: 1,000
Columns: 3

All Columns:
   1. permno <int64>         2. BidAskSpread <double>  3. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3
  permno <chr> BidAskSpread <chr> time_avail_m <chr>
1        10001 0.0544740536 1986-09-01 0
2        10001 0.0388545478 1986-10-01 0
3        10001 0.0544403766 1986-11-01 0
4        10001 0.0414199896 1986-12-01 0
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZE_13F.py

Thomson Reuters 13F holdings processing - Python equivalent of ZE_13F.do

### 1. TR_13F.parquet

Size: 0.03 MB
Rows: 1,030
Columns: 7

All Columns:
   1. permno <int64>         2. time_avail_m <timestamp[ns]>  3. numinstown <double>  
   4. dbreadth <double>      5. instown_perc <double>  6. maxinstown_perc <double>
   7. numinstblock <double>

Sample Data:
```
   1  2  3  4  5  6  7
  permno <chr> time_avail_m <chr> numinstown <chr> dbreadth <chr> instown_perc <chr> maxinstown_perc <chr> ...
1        10001 1986-09-01 0          1.0           NA        8.073  8.072653885          ...
2        10001 1986-12-01 0          1.0          0.0        8.073  8.072653885          ...
3        10001 1987-03-01 0          1.0          0.0        8.073  8.072653885          ...
4        10001 1987-06-01 0          1.0          0.0        8.073  8.072653885          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZF_CRSPIBESLink.py

CRSP-IBES Linking data script - Python equivalent of ZF_CRSPIBESLink.do

### 1. IBESCRSPLinkingTable.parquet

Size: 0.01 MB
Rows: 1,000
Columns: 2

All Columns:
   1. tickeribes <string>    2. permno <int64>       

Sample Data:
```
   1  2
  tickeribes <chr> permno <chr>
1         GFGC        10001
2         BTFG        10002
3         GCBK        10003
4         GACO        10008
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: None

## ZG_BidaskTAQ.py

High-frequency bid-ask spread processing - Python equivalent of ZG_BidaskTAQ.do

### 1. hf_spread.parquet

Size: 0.02 MB
Rows: 1,000
Columns: 3

All Columns:
   1. permno <int64>         2. time_avail_m <timestamp[ns]>  3. hf_spread <double>   

Sample Data:
```
   1  2  3
  permno <chr> time_avail_m <chr> hf_spread <chr>
1        10001 1987-01-01 0   3.97470061
2        10001 1987-02-01 0   3.89813271
3        10001 1987-03-01 0   6.37236534
4        10001 1987-06-01 0   8.66166123
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZH_OptionMetrics.py

OptionMetrics data processing - Python equivalent of ZH_OptionMetrics.do

### 1. OptionMetricsVolume.parquet

Size: 0.30 MB
Rows: 1,163,966
Columns: 4

All Columns:
   1. secid <int64>          2. optvolume <double>     3. optinterest <double> 
   4. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3  4
  secid <chr> optvolume <chr> optinterest <chr> time_avail_m <chr>
1         5005           NA           NA 1996-01-01 0
2         5005           NA           NA 1996-02-01 0
3         5005           NA           NA 1996-03-01 0
4         5005           NA           NA 1996-04-01 0
```
... with 1 more rows

IDENTIFIERS:
- stock: secid
- time: time_avail_m
### 2. OptionMetricsVolSurf.parquet

Size: 37.60 MB
Rows: 4,617,772
Columns: 7

All Columns:
   1. secid <int64>          2. days <int64>           3. delta <int64>        
   4. cp_flag <string>       5. time_avail_m <timestamp[ns]>  6. date <string>        
   7. impl_vol <double>    

Sample Data:
```
   1  2  3  4  5  6  7
  secid <chr> days <chr> delta <chr> cp_flag <chr> time_avail_m <chr> date <chr> ...
1         5005           30           50            C 1996-01-01 0   1996-01-31          ...
2         5005           30           50            C 1996-02-01 0   1996-02-29          ...
3         5005           30           50            C 1996-03-01 0   1996-03-29          ...
4         5005           30           50            C 1996-04-01 0   1996-04-30          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: secid
- time: time_avail_m
### 3. OptionMetricsXZZ.parquet

Size: 0.76 MB
Rows: 611,701
Columns: 3

All Columns:
   1. secid <int64>          2. time_avail_m <timestamp[ns]>  3. skew1 <double>       

Sample Data:
```
   1  2  3
  secid <chr> time_avail_m <chr> skew1 <chr>
1         5015 1996-01-01 0           NA
2         5015 1996-03-01 0           NA
3         5015 1996-04-01 0           NA
4         5015 1996-05-01 0           NA
```
... with 1 more rows

IDENTIFIERS:
- stock: secid
- time: time_avail_m
### 4. OptionMetricsBH.parquet

Size: 0.02 MB
Rows: 1,000
Columns: 7

All Columns:
   1. secid <int64>          2. time_avail_m <timestamp[ns]>  3. cp_flag <string>     
   4. mean_imp_vol <double>  5. mean_day <double>      6. nobs <int64>         
   7. ticker <string>      

Sample Data:
```
   1  2  3  4  5  6  7
  secid <chr> time_avail_m <chr> cp_flag <chr> mean_imp_vol <chr> mean_day <chr> nobs <chr> ...
1         5005 1996-01-01 0         BOTH     0.613557         31.0            1          ...
2         5005 1996-01-01 0            P     0.613557         31.0            1          ...
3         5005 1996-02-01 0         BOTH    0.5411796         19.2            5          ...
4         5005 1996-02-01 0            C 0.5790696666 19.666666666            3          ...
```
... with 1 more rows

IDENTIFIERS:
- stock: secid
- time: time_avail_m

## ZI_PatentCitations.py

Patent Citations data script - Python equivalent of ZI_PatentCitations.do

### 1. PatentDataProcessed.parquet

Size: 0.00 MB
Rows: 3
Columns: 4

All Columns:
   1. gvkey <string>         2. year <int64>           3. npat <int64>         
   4. ncitscale <int64>    

Sample Data:
```
   1  2  3  4
  gvkey <chr> year <chr> npat <chr> ncitscale <chr>
1       001001         2020            5           25
2       001002         2021            8           40
3       001003         2022            3           15
```
... with 0 more rows

IDENTIFIERS:
- stock: gvkey
- time: year

## ZJ_InputOutputMomentum.py



### 1. InputOutputMomentumProcessed.parquet

Size: 0.00 MB
Rows: 0
Columns: 6

All Columns:
   1. gvkey <null>           2. time_avail_m <null>    3. retmatchcustomer <null>
   4. portindcustomer <null>  5. retmatchsupplier <null>  6. portindsupplier <null>

Sample Data:
No sample data available

IDENTIFIERS:
- stock: gvkey
- time: time_avail_m

## ZK_CustomerMomentum.py



### 1. customerMom.parquet

Size: 2.24 MB
Rows: 356,462
Columns: 3

All Columns:
   1. permno <int64>         2. custmom <double>       3. time_avail_m <timestamp[ns]>

Sample Data:
```
   1  2  3
  permno <chr> custmom <chr> time_avail_m <chr>
1        76823     0.173333 1976-12-01 0
2        76823    -0.090909 1977-01-01 0
3        76823       0.0025 1977-02-01 0
4        76823     0.113924 1977-03-01 0
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: time_avail_m

## ZL_CRSPOPTIONMETRICS.py

CRSP-OptionMetrics data script - Python equivalent of ZL_CRSPOPTIONMETRICS.do

### 1. OPTIONMETRICSCRSPLinkingTable.parquet

Size: 0.31 MB
Rows: 26,392
Columns: 3

All Columns:
   1. secid <int64>          2. permno <int64>         3. om_score <int64>     

Sample Data:
```
   1  2  3
  secid <chr> permno <chr> om_score <chr>
1       104332        10001            0
2       110326        10002            0
3         6774        10009            0
4         6518        10011            1
```
... with 1 more rows

IDENTIFIERS:
- stock: permno
- time: None
