* --------------
// DATA LOAD
use permno time_avail_m ret using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 1: After data load
list permno time_avail_m ret if permno == 13755 & time_avail_m >= tm(2021m3) & time_avail_m <= tm(2021m5)
list permno time_avail_m ret if permno == 89169 & time_avail_m >= tm(2020m9) & time_avail_m <= tm(2020m11)
list permno time_avail_m ret if permno == 91201 & time_avail_m >= tm(2019m7) & time_avail_m <= tm(2019m9)

// SIGNAL CONSTRUCTION
replace ret = 0 if mi(ret)

* CHECKPOINT 2: After replacing missing returns with 0
list permno time_avail_m ret if permno == 13755 & time_avail_m >= tm(2021m3) & time_avail_m <= tm(2021m5)
list permno time_avail_m ret if permno == 89169 & time_avail_m >= tm(2020m9) & time_avail_m <= tm(2020m11)
list permno time_avail_m ret if permno == 91201 & time_avail_m >= tm(2019m7) & time_avail_m <= tm(2019m9)

asrol ret, by(permno) window(time_avail_m 10) stat(mean) minimum(6) gen(Mom12mOffSeason) xf(focal)  // xf(focal) excludes STR, the most recent return

* CHECKPOINT 3: After Mom12mOffSeason calculation
list permno time_avail_m ret Mom12mOffSeason if permno == 13755 & time_avail_m >= tm(2021m3) & time_avail_m <= tm(2021m5)
list permno time_avail_m ret Mom12mOffSeason if permno == 89169 & time_avail_m >= tm(2020m9) & time_avail_m <= tm(2020m11)
list permno time_avail_m ret Mom12mOffSeason if permno == 91201 & time_avail_m >= tm(2019m7) & time_avail_m <= tm(2019m9)

label var Mom12mOffSeason "Momentum without Seasonal Part"

* CHECKPOINT 4: Before save
list permno time_avail_m Mom12mOffSeason if permno == 13755 & time_avail_m == tm(2021m5)
list permno time_avail_m Mom12mOffSeason if permno == 89169 & time_avail_m == tm(2020m11)
list permno time_avail_m Mom12mOffSeason if permno == 91201 & time_avail_m == tm(2019m9)

// SAVE
do "$pathCode/savepredictor" Mom12mOffSeason
