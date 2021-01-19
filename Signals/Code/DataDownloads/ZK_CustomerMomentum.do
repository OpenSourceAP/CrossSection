* R 4. Customer Segments -------------------------------------------------------
if "`c(os)'" != "Unix" {
	rscript using "$pathProject/Signals/Code/DataDownloads/ZKR_CustomerSegments.R", args("$pathProject")
} 
else {
	shell Rscript $pathProject/Signals/Code/DataDownloads/ZKR_CustomerSegments.R $pathProject
}

import delimited using "$pathDataIntermediate/customerMom.csv", clear
gen temp = mofd(date(time_avail_m, "YMD"))
drop time_avail_m
rename temp time_avail_m
format time_avail_m %tm

save "$pathDataIntermediate/customerMom", replace
