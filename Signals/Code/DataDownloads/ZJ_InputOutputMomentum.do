* R 3. Input-Output Momentum ---------------------------------------------------
if "`c(os)'" != "Unix" {
	rscript using "$pathProject/Signals/Code/DataDownloads/ZJR_InputOutputMomentum.R", args("$pathProject")
} 
else {
	shell Rscript $pathProject/Signals/Code/DataDownloads/ZJR_InputOutputMomentum.R $pathProject
}


use "$pathDataIntermediate/InputOutputMomentum", clear

gen time_avail_m = ym(year_avail, month_avail)
format time_avail_m %tm

gcollapse (mean) iomom*, by(gvkey time_avail_m)  // A few observations are duplicates

save "$pathDataIntermediate/InputOutputMomentumProcessed", replace
