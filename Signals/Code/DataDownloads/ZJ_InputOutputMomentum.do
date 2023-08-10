* Menzly Ozbas. Input-Output Momentum ---------------------------------------------------
if "`c(os)'" != "Unix" {
	rscript using "$pathProject/Signals/Code/DataDownloads/ZJR_InputOutputMomentum.R", args("$pathProject")
} 
else {
	shell Rscript $pathProject/Signals/Code/DataDownloads/ZJR_InputOutputMomentum.R $pathProject
}


use "$pathDataIntermediate/InputOutputMomentum", clear

gen time_avail_m = ym(year_avail, month_avail)
format time_avail_m %tm

gcollapse (mean) retmatch portind, by(gvkey time_avail_m type)  // A few observations are duplicates

// keep gvkey time_avail_m type retmatch
reshape wide retmatch portind, i(gvkey time_avail_m) j(type) string

save "$pathDataIntermediate/InputOutputMomentumProcessed", replace
