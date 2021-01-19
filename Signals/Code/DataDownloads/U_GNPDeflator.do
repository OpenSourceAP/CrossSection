* 21. GNP Deflator---------------------------------------------------------------
import fred GNPCTPI, clear

gen temp_time_m = mofd(daten)
* Expand to monthly
expand 3
bys temp: gen time_avail_m = temp + _n - 1
format time_avail_m %tm
drop daten datestr temp
replace time_avail_m = time_avail_m + 3  // Assume that data available with a 3 month lag
gen gnpdefl = GNPCTPI/100
keep time gnpdefl

compress
save "$pathDataIntermediate/GNPdefl", replace