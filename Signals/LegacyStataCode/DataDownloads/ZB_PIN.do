* 27. Probability of informed trading ------------------------------------------

/*
local webloc "https://www.dropbox.com/s/45b42e89gaafg0n/cpie_data.zip?dl=1"
shell wget "`webloc'" -O $pathDataIntermediate/cpie_data.zip
*shell wget "https://www.dropbox.com/s/45b42e89gaafg0n/cpie_data.zip?dl=1" -O $pathDataIntermediate/cpie_data.zip
shell unzip -o $pathDataIntermediate/cpie_data.zip -d $pathDataIntermediate
import delimited "$pathDataIntermediate/pin_yearly.csv", clear
shell rm $pathDataIntermediate/cpie_data.zip -f

rm $pathDataIntermediate/owr_yearly.csv
rm $pathDataIntermediate/cpie_daily.csv
rm $pathDataIntermediate/gpin_yearly.csv
rm $pathDataIntermediate/dy_yearly.csv

*/

* Load Edwin Hus data
copy "https://www.dropbox.com/s/45b42e89gaafg0n/cpie_data.zip?dl=1" ///
     "$pathDataIntermediate/temp.zip", replace

cd $pathDataIntermediate
unzipfile "temp.zip", replace ifilter("pin_yearly.csv")

import delimited "$pathDataIntermediate/pin_yearly.csv", clear

* convert to monthly
tset (year permno)
expand 12
sort permno year
by permno year: generate month = _n
gen modate = ym(year, month)
format modate %tm
gen time_avail_m = modate + 12
format time_avail_m %tm

compress
save "$pathDataIntermediate/pin_monthly_Hu", replace


* Load Soren Hvidkjaers data
copy "https://web.archive.org/web/20110219024112/http://sites.google.com/site/hvidkjaer/data/data-files/pin1983-2001.zip?attredirects=0" ///
     "$pathDataIntermediate/temp.zip", replace

unzipfile "temp.zip", replace ifilter("pin1983-2001.dat")

import delimited pin1983-2001.dat, clear varnames(1) delimiter(whitespace, collapse)
rename permn permno
replace year = year +1  // To trade on information from previous year

tset (year permno)
expand 12
sort permno year
by permno year: generate month = _n
gen time_avail_m = ym(year, month)
format time_avail_m %tm

rename pin pinHvidkjaer
compress
save "$pathDataIntermediate/pin_monthly_Hvidkjaer", replace

** Join the two files
use $pathDataIntermediate/pin_monthly_Hu, clear
merge 1:1 permno time_avail_m using "$pathDataIntermediate/pin_monthly_Hvidkjaer", nogen

gen flag = "Hvidkjaer" if !mi(pin)
replace flag = "Hu" if mi(flag)

compress
save "$pathDataIntermediate/pin_monthly", replace


