* 22. 3-month T-bill rate (quarterly) ------------------------------------------
import fred TB3MS, clear aggregate(q, avg)

gen TbillRate3M = TB3MS/100
gen qtr = quarter(daten)
gen year = yofd(daten)

keep year qtr TbillRate3M

compress
save "$pathDataIntermediate/TBill3M", replace