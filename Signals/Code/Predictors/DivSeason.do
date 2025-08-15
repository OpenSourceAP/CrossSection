// PREP DISTRIBUTIONS DATA
use permno cd* divamt exdt using "$pathDataIntermediate/CRSPdistributions", clear

* CHECKPOINT 1: Check initial data for problematic permnos
display "=== CHECKPOINT 1: Check initial data for problematic permnos ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn': " r(N)
	
	count if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987
	if r(N) > 0 {
		display "permno `pn' data (1986-1987):"
		list permno cd1 cd2 cd3 divamt exdt if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987, clean noobs
	}
	else {
		display "No data found for permno `pn' in 1986-1987"
	}
}

keep if cd1 == 1 & cd2 == 2

* CHECKPOINT 2: Check after filtering cd1==1 & cd2==2 for problematic permnos
display ""
display "=== CHECKPOINT 2: Check after filtering cd1==1 & cd2==2 for problematic permnos ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after filter: " r(N)
	
	count if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987
	if r(N) > 0 {
		display "permno `pn' data after cd1==1 & cd2==2 filter:"
		list permno cd1 cd2 cd3 divamt exdt if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987, clean noobs
	}
	else {
		display "No data found for permno `pn' after filter"
	}
}

* select timing variable and convert to monthly
* (p5 says exdt is used)
gen time_avail_m = mofd(exdt)
format time_avail_m %tm

* CHECKPOINT 3: Check before dropping missing time_avail_m/divamt
display ""
display "=== CHECKPOINT 3: Check before dropping missing time_avail_m/divamt ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' before dropping missing: " r(N)
	
	count if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987
	if r(N) > 0 {
		display "permno `pn' data before dropping missing values:"
		list permno cd3 divamt exdt time_avail_m if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987, clean noobs
	}
	else {
		display "No data found for permno `pn'"
	}
}

drop if time_avail_m == . | divamt == .

* CHECKPOINT 4: Check after dropping missing time_avail_m/divamt
display ""
display "=== CHECKPOINT 4: Check after dropping missing time_avail_m/divamt ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after dropping missing: " r(N)
	
	count if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987
	if r(N) > 0 {
		display "permno `pn' data after dropping missing values:"
		list permno cd3 divamt exdt time_avail_m if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987, clean noobs
	}
	else {
		display "No data found for permno `pn' after dropping missing values"
	}
}

* sum across all frequency codes
gcollapse (sum) divamt, by(permno cd3 time_avail_m)

* CHECKPOINT 5: Check after gcollapse
display ""
display "=== CHECKPOINT 5: Check after gcollapse ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after gcollapse: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data after gcollapse:"
		list permno cd3 divamt time_avail_m if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn' after gcollapse"
	}
}

* clean up a handful of odd two-frequency permno-months
* by keeping the quarterly code
sort permno time_avail_m cd3
by permno time_avail_m: keep if _n == 1

* CHECKPOINT 6: Check after keeping first frequency code
display ""
display "=== CHECKPOINT 6: Check after keeping first frequency code ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after frequency cleanup: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data after keeping first frequency code:"
		list permno cd3 divamt time_avail_m if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn' after frequency cleanup"
	}
}

save "$pathtemp/tempdivamt", replace

// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 7: Check SignalMasterTable for our target observations
display ""
display "=== CHECKPOINT 7: Check SignalMasterTable for our target observations ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' in SignalMasterTable: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data in SignalMasterTable:"
		list permno time_avail_m if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn' in SignalMasterTable"
	}
}

merge 1:1 permno time_avail_m using "$pathtemp/tempdivamt", keep(master match) nogenerate keepusing(cd3 divamt)

* CHECKPOINT 8: Check after merge
display ""
display "=== CHECKPOINT 8: Check after merge ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after merge: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data after merge:"
		list permno time_avail_m cd3 divamt if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn' after merge"
	}
} 

replace cd3 = l1.cd3 if cd3 == .
replace divamt = 0 if divamt == .
gen divpaid = divamt > 0

* CHECKPOINT 9: Check after filling missing values and creating divpaid
display ""
display "=== CHECKPOINT 9: Check after filling missing values and creating divpaid ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after creating divpaid: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data after creating divpaid:"
		list permno time_avail_m cd3 divamt divpaid if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn'"
	}
}

drop if cd3 == 2 // OP drops monly div unless otherwise noted (p5)

* CHECKPOINT 10: Check after dropping monthly dividends (cd3==2)
display ""
display "=== CHECKPOINT 10: Check after dropping monthly dividends (cd3==2) ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after dropping monthly dividends: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data after dropping monthly dividends:"
		list permno time_avail_m cd3 divamt divpaid if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn' after dropping monthly dividends"
	}
}

keep if cd3 < 6 // Tab 2 note

* CHECKPOINT 11: Check after keeping only cd3 < 6
display ""
display "=== CHECKPOINT 11: Check after keeping only cd3 < 6 ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after filtering: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data after filtering:"
		list permno time_avail_m cd3 divamt divpaid if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn' after filtering"
	}
}


* short all other with a div in last 12 months
bys permno: asrol divpaid, window(time_avail_m 12) stat(sum) gen(div12)

* CHECKPOINT 12: Check div12 rolling sum calculation
display ""
display "=== CHECKPOINT 12: Check div12 rolling sum calculation ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' after div12 calculation: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data with div12:"
		list permno time_avail_m cd3 divpaid div12 if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn'"
	}
}

gen DivSeason = 0 if div12 > 0

* CHECKPOINT 13: Check initial DivSeason assignment
display ""
display "=== CHECKPOINT 13: Check initial DivSeason assignment ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' with initial DivSeason: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data with initial DivSeason:"
		list permno time_avail_m cd3 divpaid div12 DivSeason if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn'"
	}
} 

* long if div month is predicted
* OP page 5: "unkown and missing frequency are assumed quarterly"
gen temp3 = (cd3 == 3 | cd3 == 0 | cd3 == 1) ///
	& (l2.divpaid | l5.divpaid | l8.divpaid | l11.divpaid ) 
gen temp4 = cd3 == 4 & (l5.divpaid | l11.divpaid )
gen temp5 = cd3 == 5 & (l11.divpaid )

* CHECKPOINT 14: Check temp variables for prediction logic
display ""
display "=== CHECKPOINT 14: Check temp variables for prediction logic ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' with temp variables: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data with temp variables:"
		list permno time_avail_m cd3 l2.divpaid l5.divpaid l8.divpaid l11.divpaid temp3 temp4 temp5 if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn'"
	}
}

replace DivSeason = 1 if temp3 | temp4 | temp5

* CHECKPOINT 15: Check final DivSeason values
display ""
display "=== CHECKPOINT 15: Check final DivSeason values ==="
foreach pn in 10001 10006 11406 12473 {
	display "--- Permno `pn' ---"
	count if permno == `pn'
	display "Total observations for permno `pn' with final DivSeason: " r(N)
	
	count if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12)
	if r(N) > 0 {
		display "permno `pn' data with final DivSeason:"
		list permno time_avail_m cd3 div12 temp3 temp4 temp5 DivSeason if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
	}
	else {
		display "No data found for permno `pn'"
	}
}


label var DivSeason "Predicted Dividend Month"

* CHECKPOINT 16: Show data drops at critical points
display ""
display "=== CHECKPOINT 16: Data drop summary ==="
count
display "Total observations in final dataset: " r(N)
display "Observations by year:"
tab year(dofm(time_avail_m)), matcell(year_counts) matrow(years)

// SAVE
do "$pathCode/savepredictor" DivSeason
