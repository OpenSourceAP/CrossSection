// PREP DISTRIBUTIONS DATA
use permno cd* divamt exdt using "$pathDataIntermediate/CRSPdistributions", clear

* CHECKPOINT 1: Check initial data for problematic permnos
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 1: Initial data for permno `pn' ==="
        count if permno == `pn'
        list permno cd1 cd2 cd3 divamt exdt if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987, clean noobs
    }
}

keep if cd1 == 1 & cd2 == 2

* CHECKPOINT 2: Check after filtering cd1==1 & cd2==2 for problematic permnos
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 2: After cd1==1 & cd2==2 filter for permno `pn' ==="
        count if permno == `pn'
        list permno cd1 cd2 cd3 divamt exdt if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987, clean noobs
    }
}

* select timing variable and convert to monthly
* (p5 says exdt is used)
gen time_avail_m = mofd(exdt)
format time_avail_m %tm

* CHECKPOINT 3: Check before dropping missing time_avail_m/divamt
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 3: Before dropping missing values for permno `pn' ==="
        count if permno == `pn'
        list permno cd3 divamt exdt time_avail_m if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987, clean noobs
    }
}

drop if time_avail_m == . | divamt == .

* CHECKPOINT 4: Check after dropping missing time_avail_m/divamt
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 4: After dropping missing values for permno `pn' ==="
        count if permno == `pn'
        list permno cd3 divamt exdt time_avail_m if permno == `pn' & year(exdt) >= 1986 & year(exdt) <= 1987, clean noobs
    }
}

* sum across all frequency codes
gcollapse (sum) divamt, by(permno cd3 time_avail_m)

* CHECKPOINT 5: Check after gcollapse
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 5: After gcollapse for permno `pn' ==="
        count if permno == `pn'
        list permno cd3 divamt time_avail_m if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}

* clean up a handful of odd two-frequency permno-months
* by keeping the quarterly code
sort permno time_avail_m cd3
by permno time_avail_m: keep if _n == 1

* CHECKPOINT 6: Check after keeping first frequency code
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 6: After keeping first frequency code for permno `pn' ==="
        count if permno == `pn'
        list permno cd3 divamt time_avail_m if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}

save "$pathtemp/tempdivamt", replace

// DATA LOAD
use permno time_avail_m using "$pathDataIntermediate/SignalMasterTable", clear

* CHECKPOINT 7: Check SignalMasterTable for our target observations
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 7: SignalMasterTable for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}

merge 1:1 permno time_avail_m using "$pathtemp/tempdivamt", keep(master match) nogenerate keepusing(cd3 divamt)

* CHECKPOINT 8: Check after merge
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 8: After merge for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m cd3 divamt if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
} 

replace cd3 = l1.cd3 if cd3 == .
replace divamt = 0 if divamt == .
gen divpaid = divamt > 0

* CHECKPOINT 9: Check after filling missing values and creating divpaid
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 9: After creating divpaid for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m cd3 divamt divpaid if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}

drop if cd3 == 2 // OP drops monly div unless otherwise noted (p5)

* CHECKPOINT 10: Check after dropping monthly dividends (cd3==2)
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 10: After dropping monthly dividends for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m cd3 divamt divpaid if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}

keep if cd3 < 6 // Tab 2 note

* CHECKPOINT 11: Check after keeping only cd3 < 6
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 11: After keeping cd3 < 6 for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m cd3 divamt divpaid if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}


* short all other with a div in last 12 months
bys permno: asrol divpaid, window(time_avail_m 12) stat(sum) gen(div12)

* CHECKPOINT 12: Check div12 rolling sum calculation
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 12: After div12 calculation for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m cd3 divpaid div12 if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}

gen DivSeason = 0 if div12 > 0

* CHECKPOINT 13: Check initial DivSeason assignment
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 13: Initial DivSeason for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m cd3 divpaid div12 DivSeason if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
} 

* long if div month is predicted
* OP page 5: "unkown and missing frequency are assumed quarterly"
gen temp3 = (cd3 == 3 | cd3 == 0 | cd3 == 1) ///
	& (l2.divpaid | l5.divpaid | l8.divpaid | l11.divpaid ) 
gen temp4 = cd3 == 4 & (l5.divpaid | l11.divpaid )
gen temp5 = cd3 == 5 & (l11.divpaid )

* CHECKPOINT 14: Check temp variables for prediction logic
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 14: Temp variables for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m cd3 l2.divpaid l5.divpaid l8.divpaid l11.divpaid temp3 temp4 temp5 if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}

replace DivSeason = 1 if temp3 | temp4 | temp5

* CHECKPOINT 15: Check final DivSeason values
foreach pn in 10001 10006 11406 12473 {
    if permno == `pn' {
        display "=== CHECKPOINT 15: Final DivSeason for permno `pn' ==="
        count if permno == `pn'
        list permno time_avail_m cd3 div12 temp3 temp4 temp5 DivSeason if permno == `pn' & time_avail_m >= tm(1986m1) & time_avail_m <= tm(1987m12), clean noobs
    }
}

* CHECKPOINT 16: Show data drops at critical points
display "=== CHECKPOINT 16: Data drop summary ==="
display "Total observations in final dataset:"
count
display "Observations by year:"
bys year(dofm(time_avail_m)): gen count_year = _n == 1
count if count_year == 1
tab year(dofm(time_avail_m)) if _n <= 100


label var DivSeason "Predicted Dividend Month"

// SAVE
do "$pathCode/savepredictor" DivSeason
