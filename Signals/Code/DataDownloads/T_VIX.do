* 20. VIX data ------------------------------------------------------------------
import fred VIXCLS VXOCLS, clear  // OP uses VXOXLS but the series was discontinued in 2021

gen vix = VXOCLS
replace vix = VIXCLS if mi(VXOCLS) & daten >= dmy(23, 9, 2021)

drop datestr VIXCLS VXOCLS
gen time_temp = _n
tsset time_temp
gen dVIX = vix - l.vix
drop time_temp

rename daten time_d

compress
save "$pathDataIntermediate/d_vix", replace
