* R 2. Patent citation data ----------------------------------------------------
if "`c(os)'" != "Unix" {
	rscript using "$pathProject/Signals/Code/DataDownloads/ZIR_Patents.R", args("$pathProject")
} 
else {
	shell Rscript $pathProject/Signals/Code/DataDownloads/ZIR_Patents.R $pathProject
}

confirm file "$pathDataIntermediate/PatentDataProcessed.dta"



