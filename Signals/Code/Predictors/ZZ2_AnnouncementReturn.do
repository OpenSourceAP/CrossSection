* AnnouncementReturn
* --------------

// DATA LOAD

* Prepare crosswalk CRSP-CS
use gvkey permno timeLink* using "$pathDataIntermediate/CCMLinkingTable", clear
save "$pathtemp/tempCW", replace

* Prepare earnings announcement dates
use gvkey rdq using "$pathDataIntermediate/m_QCompustat", clear
drop if mi(rdq)
rename rdq time_ann_d
duplicates drop

save "$pathtemp/tempAnnDats", replace

*
use permno time_d ret using "$pathDataIntermediate/dailyCRSP", clear

* Match announcement dates
// Add identifiers for merging
joinby permno using "$pathtemp/tempCW"

* Use only if data date is within the validity period of the link
gen temp = (timeLinkStart_d <= time_d  & time_d <= timeLinkEnd_d)
tab temp
keep if temp == 1
drop temp timeLink*

rename time_d time_ann_d
destring gvkey, replace
merge m:1 gvkey time_ann_d using "$pathtemp/tempAnnDats", keep(master match)
gen anndat = (_merge == 3)
drop _merge gvkey

* Merge market return
rename time_ann_d time_d
merge m:1 time_d using "$pathDataIntermediate/dailyFF", nogenerate keep(match) keepusing(mktrf rf)

// SIGNAL CONSTRUCTION
gen AnnouncementReturn = ret - (mktrf + rf)
bys permno (time_d): gen time_temp = _n  // To deal with weekends
xtset permno time_temp

* time_temp indexes the business days for a particular permno (1,2,3,..,)
* time_ann_d creates a window that starts two biz days before anndat
* 	and ends 1 day after anndat. The value of time_ann_d is the biz day
* 	of the anndat (unique for each announcement) but is na if outside the window.
gen time_ann_d = time_temp if anndat == 1 
replace time_ann_d = time_temp + 1 if f1.anndat == 1
replace time_ann_d = time_temp + 2 if f2.anndat == 1
replace time_ann_d = time_temp - 1 if l1.anndat == 1
drop if mi(time_ann_d)
format time_ann_d %td

* this is key:sum up daily returns over the window, but then assign
* the daily date as the maximum of these dates in the window. So if the window
* ends Jan 2, AnnouncementReturn is assigned to Jan 2
gcollapse (sum) AnnouncementReturn (max) time_d, by(permno time_ann_d) 

* convert the daily date to monthly date
gen time_avail_m = mofd(time_d)
format time_avail_m %tm

* Fill in months with no earnings announcements with most recent announcement return at most six months ago
keep permno time_avail_m AnnouncementReturn
drop if mi(time_avail_m)
bys permno time_a: keep if _n == _N
compress

xtset permno time_avail
tsfill
sort permno time_avail_m
gen temp = AnnouncementReturn  // Necesssary because Stata fills sequentially

by permno: replace AnnouncementReturn = temp[_n-1] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-2] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-3] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-4] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-5] if mi(AnnouncementReturn)
by permno: replace AnnouncementReturn = temp[_n-6] if mi(AnnouncementReturn)

drop if mi(AnnouncementReturn)
drop temp

label var AnnouncementReturn "Earnings announcement return"

// SAVE 
do "$pathCode/savepredictor" AnnouncementReturn
