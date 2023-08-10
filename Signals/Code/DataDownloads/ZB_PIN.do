* 27. Probability of informed trading ------------------------------------------
local webloc "https://www.dropbox.com/s/45b42e89gaafg0n/cpie_data.zip?dl=1"
shell wget "`webloc'" -O $pathDataIntermediate/cpie_data.zip
*shell wget "https://www.dropbox.com/s/45b42e89gaafg0n/cpie_data.zip?dl=1" -O $pathDataIntermediate/cpie_data.zip
shell unzip -o $pathDataIntermediate/cpie_data.zip -d $pathDataIntermediate
import delimited "$pathDataIntermediate/pin_yearly.csv", clear
shell rm $pathDataIntermediate/cpie_data.zip -f
rm $pathDataIntermediate/owr_yearly.csv
rm $pathDataIntermediate/pin_yearly.csv
rm $pathDataIntermediate/cpie_daily.csv
rm $pathDataIntermediate/gpin_yearly.csv
rm $pathDataIntermediate/dy_yearly.csv


* generate yearly PIN measure from Easley et al


* conver to monthly
tset (year permno)
expand 12
sort permno year
by permno year: generate month = _n
gen modate = ym(year, month)
format modate %tm
gen time_avail_m = modate + 11
format time_avail_m %tm




compress
save "$pathDataIntermediate/pin_monthly", replace
