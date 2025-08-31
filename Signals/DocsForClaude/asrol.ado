*! Attaullah Shah; Email: attaullah.shah@imsciences.edu.pk; Support website: www.FinTechProfessor.com
* Version 5.9: Feb 29, 2024: Fixed the selectindex() not found error.

* Version 5.8: May 5, 2022: bug fixed in max2, max2, max4, and max5
* Version 5.7: Arpil 5, 2022: bug fixed when option window(var 0 1) was used 
* Version 5.6: Mar 1, 2022 : New statistic - kurtosis - added
* Version 5.5: Nov 6, 2021 : Added max2, max3, max4, and max5 for finding second, third, fourth and fifth largest values.
* Version 5.4: July 13, 2021 : The error 'PRODUCT():  3201  vector required' fixed. This error would occur in the calculation of product if extended missing values were present
* Version 5.3: June 14, 2021 : Bug fixed related to missing value in the rangeevar
* Version 5.2: Nov 29, 2020 : Bug fix when 0 was used in the back window
* Version 5.1: Sep 4, 2020 : Mutilple statistics / variables can used used now in the flexible window
* Version 5.0: Adding forward window : May 22, 2020
* Version 4.6 Improves the calculation of gmean for large numbers
* Version 4.5 Gmean improvement
* Version 4.4 10May2018: product fuction improvement
* This version supports multiple variables and multiple statistics

cap prog drop asrol
prog asrol, byable(onecall) sortpreserve
	version 11
	syntax                    	    ///
	    varlist(numeric)    	   ///
		[in] [if],          	  ///
		Stat(str) 		   		 ///
		[Generate(str)    	    ///
		Window(string)   	   ///
		Perc(str)			  ///
		MINimum(real 0) 	 ///
		by(varlist)    	    ///
		XFocal(string) 	   ///
		ADD (real 0)      ///
		IGnorezero       ///
		TYPE(str)		///
		] 
	preserve
	marksample touse, nov
	local Z : word count `stat'
	local V : word count `varlist'
	loc mult = `Z' * `V'
	if "`generate'"! = "" & `mult'> 1 {
		display as error "Option {opt g:en} is not allowed with multiple variables or statistics"
		exit
	}

	foreach  z of local stat {
		if "`z'" != "mean" 		& "`z'" != "gmean" 		& "`z'" 	!= "sd"        ///
			& "`z'" != "sum" 	& "`z'" != "product" 	& "`z'" 	!= "median"   ///
			& "`z'" != "count" 	& "`z'" != "min" 		& "`z'" 	!= "max"      ///
			& "`z'" != "first" 	& "`z'" != "last" 		& "`z'" 	!= "missing" ///
			& "`z'" != "skewness" & "`z'" != "max2" 	& "`z'" 	!= "max3"  ///
			& "`z'" != "max4" 	& "`z'" != "max5" 		& "`z'"		!= "kurtosis" { 
			display as error " Incorrect statistics specified!"
			display as text "You have entered {cmd: `z'} in the {cmd: stat option}. However, only the following staticts are allowed with {help asrol}"
			dis as res "mean, gmean, sd, sum, product, median, count, min, max, first, last, missing"
			exit
		}
		if "`z'" != "median" & "`perc'"!="" dis as error "option {cmd: perc()} is used only when finding {cmd: percentiles with option median}, see help file {help asrol}"
		if "`z'" == "median" {
			if "`perc'" == ""{
				global Q = .5
			}
			else {
				confirm number `perc'
				global Q = `perc'
			}
		}
	}
	if "`xfocal'"=="" {
		local XF = 1
	}
	else{ 
		cap confirm numeric variable `xfocal'
		if _rc==0 {
			local varfocal "yes"
		}
		if "`xfocal'" != "focal" & "`varfocal'"!="yes"{
			display as error " Option xfocal either accepts the word focal or name of an existing numeric variable"
			display as text "For example, you can specify xfocal option as {cmd: xfocal(focal)} or {cmd: xfocal(year)}"
			exit
		}
		if "`xfocal'"=="focal" { 
			local XF = 2
		}
		else{ 
			local XF = 3
		}
	}
	if "`type'" != "" {
		if !inlist("`type'", "s", "sample", "p", "population") {
			display as error "Option type accepts sample or population only"
			display as error "The default of population is used in the calculation"
		}
		else global type "`type'"
	}
	global addtofunc = `add'
	global ignorezero `ignorezero'
	if "`XF'" != "1" global XF 1
	else global XF 0

	if "`window'"!=""{
		local nwindow : word count `window'
		if !inrange(`nwindow', 2, 3) {
			dis ""
			display as error "Option window must have either two arguments: rangevar and length of the rolling window, e.g., {opt window(year 10)}"
			dis as error " Or three arguments : rangeevar, length of the backward, and the forward windows e.g., {opt window(year -10 20)}"
			exit
		}
		else if `nwindow'==2 {
			tokenize `window'
			gettoken    rangevar window : window
			gettoken  bw window : window
			confirm number `bw'
			confirm numeric variable `rangevar'
		}
		else if `nwindow' == 3 {
		    local rangevar : word 1 of `window'
			local bw : word 2 of `window'
			local fw : word 3 of `window'
			confirm number `bw'
			confirm number `fw'
			confirm numeric variable `rangevar'



			if (`bw' >= `fw') {
			    display as error "The lower bound of the window is either equal to or less than the upper bound."
				display as error "Rolling window calculations are not possible when this is the case!"
				exit
			}

			if `fw' == 0 {
			    loc fw
				loc bw = abs(`bw')
			}
		}

		markout `touse' `rangevar'

		if "`_byvars'"!="" {
			local by "`_byvars'"
		}
		if "`by'"=="" {
			tempvar by
			qui gen `by' = 1
		}
		local cversion =`c(version)'
		tempvar __GByVars __000first __0dIf
		qui bysort `by' (`rangevar'): gen  `__000first' = _n == 1
		qui gen `__GByVars'=sum(`__000first')
		qui drop `__000first' 

		qui by `by' : gen `__0dIf' = `rangevar' - `rangevar'[_n-1]


		loc dt = 2
		cap qui assert `__0dIf' == 1 | `__0dIf' == .
		if _rc == 0 loc dt = 1
		else {
		    cap assert `__0dIf' == 0  if `__0dIf' < 1, fast null
			if _rc != 8 & _rc != 9 {
				loc dt = 3
				tempvar touse2
				qui bysort `__GByVars' `rangevar' : gen `touse2' = _n == 1
			} 
		}


		if "`fw'" == "" {
			loc bw = abs(`bw')

			if  `mult'<=1 {
				if "`stat'"=="median" {
					if "`perc'"==""{
						global Q = .5
					}
					else {
						confirm number `perc'
						global Q = `perc'
					}
				}

				if "`generate'" == "" local generate "`varlist'_`stat'`bw'"
				loc generate = subinstr("`generate'", "-", "_", .)
				loc generate = subinstr("`generate'", " ", "", .)

				mata: asrolw(				      ///
					"`varlist'", 		         ///
					"`__GByVars'" ,	    		///
					"`generate'" , 	  		   ///
					`bw',			          /// 
					"`stat'", 	    		 ///
					"`minimum'", 	   		///
					"`rangevar'",	  	   /// 
					`XF' ,    			  ///
					"`__0dIf'" ,		 ///
					`cversion',	        ///
					"`touse'" 		      )
				cap qui label var `generate' "`stat' of `varlist' in a `bw' `fw' periods rol. wind."
			}
			else {
				loc windname = abs(`bw')
				foreach v of varlist `varlist'  {
					foreach z  of  local    stat    {

						local generate "`v'_`z'`bw'"
						loc generate = subinstr("`generate'", "-", "_", .)
						loc generate = subinstr("`generate'", " ", "", .)

						mata: asrolw(				      ///
							"`v'", 		                 ///
							"`__GByVars'" ,	    		///
							"`generate'" , 	  		   ///
							`bw',			          /// 
							"`z'", 	    		     ///
							"`minimum'", 	   		///
							"`rangevar'",	  	   /// 
							`XF' ,    			  ///
							"`__0dIf'" ,		 ///
							`cversion',	        ///
							"`touse'" 		      )
						cap qui label variable `generate' "`z' of `v' in a `bw' `fw' periods rol. wind."
					}
				}
			}

		}




		// If forward window
		else {
			if  `mult'<=1 {
				if "`stat'"=="median" {
					if "`perc'"==""{
						global Q = .5
					}
					else {
						confirm number `perc'
						global Q = `perc'
					}
				}

				if "`generate'" == "" local generate "`stat'`bw'_`varlist'"
				loc generate = subinstr("`generate'", "-", "_", .)
				loc generate = subinstr("`generate'", " ", "", .)

				mata: asrolfw(				      ///
					"`varlist'", 		         ///
					"`__GByVars'" ,	    		///
					"`generate'" , 	  		   ///
					`bw',			  		  /// 
					`fw',				     ///
					"`stat'", 	    		///
					"`minimum'", 	   	   ///
					"`rangevar'",	  	  /// 
					`XF' ,    			 ///
					"`dt'" ,			///
					"`touse2'", 	   ///
					`cversion',	       ///
					"`touse'" 		      )
				cap qui label var `generate' "`stat' of `varlist' in a `bw' `fw' periods rol. wind."
			}

			// if forward window and multi
			else {

				foreach v of varlist `varlist'  {
					foreach z  of  local    stat    {

						local generate "`v'_`z'`bw'_`fw'"
						loc generate = subinstr("`generate'", "-", "_", .)
						loc generate = subinstr("`generate'", " ", "", .)

						mata: asrolfw(				      ///
							"`v'", 		         		 ///
							"`__GByVars'" ,	    		///
							"`generate'" , 	  		   ///
							`bw',			  		  /// 
							`fw',				     ///
							"`z'", 	    			///
							"`minimum'", 	   	   ///
							"`rangevar'",	  	  /// 
							`XF' ,    			 ///
							"`dt'" ,			///
							"`touse2'", 	   ///
							`cversion',	       ///
							"`touse'" 		      )
						cap qui label variable `generate' "`z' of `v' in a `bw' `fw' periods rol. wind."
					}
				}
			}
		}
	} 

	// End window

	else { 
		local bw = 0
		tempvar GByVars dup first n  dif
		if "`_byvars'"!="" {
			local by "`_byvars'"
		}
		if "`by'"!="" {
			if `XF'==3 { 
				local rangevar "`xfocal'"
			}

			gen `n'=_n
			bysort `by' (`rangevar' `n'): gen  `first' = _n == 1
			qui gen `GByVars' = sum(`first')
			drop `first' `n'
		}
		if "`by'"=="" {
			tempvar GByVars
			qui gen `GByVars' = 1
			if `XF'==3 {
				local rangevar "`xfocal'"
				sort `GByVars' `rangevar'
			}
		}

		if  `mult' <= 1 {
			if   "`generate'" == ""  local    generate   "`varlist'_`stat'"
			mata: asrolnw(		 		     ///
				"`varlist'", 	   	 	    ///
				"`GByVars'" ,	           ///
				"`generate'" ,       	  ///
				"`stat'", 	    		 ///
				`minimum',        		///
				"`rangevar'", 		   /// 
				`XF' ,   	 	      ///
				"`touse'"   	     ///
				)
			capture    quietly       label    variable  `generate' "`stat' of `varlist'"

		}
	    else{
			foreach v of varlist `varlist' {
				foreach z of local stat       {
					local generate "`z'_`v'"
					mata: asrolnw(		 		   ///
						"`v'", 	  	    	 	  ///
						"`GByVars'" ,	         ///
						"`generate'" ,          ///
						"`z'", 	       		   ///
						`minimum',            ///
						"`rangevar'", 	     /// 
						`XF' ,   	 		///
						"`touse'"          ///
						)
					capture  quietly  label  variable  `generate'   "`z' of `v'"
				}
			}
		}
	}
	restore, not

	if `mult' <= 1 {
		if "`dt'" == "3" & `XF' != 2 {
			qui bys `__GByVars' `rangevar': replace `generate' =`generate'[1]
		}
	}
	else  {
		foreach v of varlist `varlist' {
			foreach z of local stat {
				loc generate "`v'_`z'`bw'"
				loc generate = subinstr("`generate'", "-", "_", .)
				loc generate = subinstr("`generate'", " ", "", .)
				qui bys `__GByVars' `rangevar': replace `generate' =`generate'[1]

			}
		}
	}

	global type
	end
	
