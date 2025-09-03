// ---- Debug: run only selected predictors ----

// Hard-coded list of predictor names
local predictors Recomm_ShortInterest PatentsRD Mom6mJunk

// Folder where predictor do-files are located
local dofolder "$pathPredictors"

// Loop through each predictor and run its do-file
foreach pred of local predictors {
    local dofile "`dofolder'/`pred'.do"
    di as txt "▶ Running: `dofile'"
    capture noisily do `"`dofile'"'
    if (_rc) {
        di as error "✖ Error running: `pred' (return code = " %9.0g _rc ")"
    }
    di as txt "— done: `pred'"
}
