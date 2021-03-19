* 20. VIX data ------------------------------------------------------------------
import fred VXOCLS, clear

rename VXOCLS vix
drop datestr
gen time_temp = _n
tsset time_temp
gen dVIX = vix - l.vix
drop time_temp

rename daten time_d

compress
save "$pathDataIntermediate/d_vix", replace
