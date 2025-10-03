* --------------
// DATA LOAD
use permno time_avail_m vol using "$pathDataIntermediate/monthlyCRSP", clear
// SIGNAL CONSTRUCTION
asreg vol time_avail_m, window(time_av 60) min(30) by(permno)
rename _b_time betaVolTrend
drop _*
bys permno: asrol vol, gen(meanX) stat(mean) window(time_avail_m 60) min(30)  
gen VolumeTrend = betaVolTrend/meanX
winsor2 VolumeTrend, cut(1 99) replace trim  // ADD ON SINCE SOME VALUES LOOKED OUT OF LINE (e^14)
label var VolumeTrend "Volume Trend"

// SAVE
do "$pathCode/savepredictor" VolumeTrend