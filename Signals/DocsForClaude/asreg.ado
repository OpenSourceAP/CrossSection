*! Attaullah Shah ;  Email: attaullah.shah@imsciences.edu.pk ; * Support website: www.FinTechProfessor.com

*!Version 4.8 : Jul 02, 2023 : Time labels were incorrectly displayed with fmb first options. Fixed now.

* Version 4.7: Jan 07, 2022 : When data had duplicates, the fitted and residual were not calculated for each obs. This has been fixed.
* Version 4.6 : Oct 13, 2021 : Added [aweights] and noconstant to fmb
* Version 4.5 : Feb 17, 2021 : Shanken license updated
* Version 4.4 : Feb 09, 2021 : Issue with by groups regressions solved : Also, removed the select index pointer
* Version 4.3 : Feb 05, 2021 : label issue with the fmb, first regression is fixed. 
* Version 4.2 : Jan 31, 2021 : Option exclude(keyvar low high) added
* Version 4.1 : Nov 02, 2020 : New system for shanken correction license
* Version 4.0 : Oct 29, 2020 : Added flexible window : window(year -40 10) etc.
* Version 3.4 : Jul 09, 2019 : Added adjusted r-squared to fmb
* Version 3.3 : Dec 19, 2018 : Fixed a bug in  function ASREG4s1f1()
* Version 3.2 : Jul 01, 2018 : Fixed bugs in newey()
* Added noConstant and Robust options
* Added Fama and MacBeth regressions and newey SE
* Multiple functions for se and fitted values


cap prog drop asreg
prog asreg, byable(onecall) sortpreserve eclass
	version 11

	syntax       	    ///
		varlist(min=1)  ///
		[aw/]            /// works only with fmb
		[in] [if],      ///
		[Window(string) ///
		MINimum(real 0) ///
		by(varlist)     ///
		FITted          ///
		SE            	///
		RMSE			///
		RECursive		///
		FMB				///
		newey(int 0)    ///
		first    		///
		save(string)	///
		KEEP(string)	///
		NOConstant      ///
		Robust			///
		shanken(str)	///
		EXclude(str)	///
		] 

	if "`shanken'" != "" {
		if "`fmb'" == "" {
			dis as error "Option Shanken() can be used only with option fmb"
			exit
		}
		else {
			cap confirm matrix `shanken'
			if _rc {
				dis as error "Option Shanken needs a matrix of covariances among the right-hand side variables"
				dis as text "asreg could not find such a matrix"
				exit
			}
			else {
				loc colS = colsof(`shanken')
				dis "`varlist'"
				loc nRHS : word count `varlist'


				if `colS' != `=`nRHS'-1' {
					dis as error "The covariance matrix `shanken' has `colS' columns"
					dis as error "whereas you have entered `=`nRHS'-1' right hand-side variables"
					dis as error "Columns of matrix `shanken' and the right hand-side variables should be equal in number"
					exit
				}

			}
		}

	}
	marksample touse
	if "`fmb'" == "" {
		if "`window'"!=""{
		    loc window = subinstr("`window'", ",", " ", .)
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



			if "`recursive'"~=""{
				local recursive = 1000000
			}
			else{
				local recursive = 0 
			}

			local bw = `bw' + `recursive'

		}

		if "`exclude'" != "" {
		    loc exclude = subinstr("`exclude'", ",", " ", .)
			local nexclude : word count `exclude'
			if !inlist(`nexclude', 3) {
				dis as error "Error in the option exclude()!"
				display as text "Option exclude must have three arguments : keyvar, low and high range., {opt exclude(year -2 2)}"
				exit
			}
			local keyvar : word 1 of `exclude'
			cap confirm numeric variable `keyvar'
			if _rc {
				di as error "Error in the option exclude!"
				di as text "The first argument must be a numeric variable"
				exit
			}
			local xlow : word 2 of `exclude'
			local xhigh : word 3 of `exclude'
			confirm number `xlow'
			confirm number `xhigh'
			if `xlow' > `xhigh' {
				dis as error "Invalide exclude range!"
				dis as text "The second argument of exclude should be lower than the third argument"
				exit
			}


		}

		gettoken lhsvar rhs : varlist
		loc varlist "`lhsvar' `rhs'"
		qui {
			if "`rmse'"!="" {
				qui gen double _rmse = .
				label var _rmse "Root-mean-squared error"
				local _b_rmse _rmse
			}

			gen  _Nobs 	= .
			label var _Nobs "No of observatons"
			gen double _R2 	= .
			label var _R2 "R-squared"
			gen double _adjR2	= .
			label var _adjR2 "Adjusted R-squared"

			if "`rhs'" != "" {

				foreach var of varlist `rhs'{
					gen double _b_`var'=.
					label var _b_`var' "Coefficient of `var'"
					local b_rvsvars "`b_rvsvars' _b_`var'"

				}
			}
			if `newey' != 0 {
				loc mindif = `newey' - `minimum' +1
				loc minimum = `mindif'
			}

			if "`noconstant'" == "" {
				tempvar _CONS
				qui gen `_CONS' = 1
				gen double _b_cons = .
				label var _b_cons "Constant of the regression"
				loc _b_cons _b_cons
			}

			if "`newey'" ! = "0" | "`robust'" ! = "" loc se se

			if "`se'"!=""{
				if `newey' != 0 & "`robust'" != "" {
					dis as error "Option newey() and robust cannot be combined"
					exit
				}
				if `newey' != 0 local se_text "Newey adj. Std. errors of "
				else if "`robust'" != "" local se_text "Robust Std. errors of "
				else local se_text "Standard Std. errors of "

				if "`rhs'" != "" {
					foreach var of varlist `rhs'{
						gen _se_`var'=.
						label var _se_`var' "`se_text'`var'"
						local _se_rvsvars "`_se_rvsvars' _se_`var'"
					}
				}

				if "`noconstant'" == "" { 
					gen _se_cons = .
					label var _se_cons "`se_text'constant"
					loc _se_cons _se_cons
				}
				local _se_rvsvars "`_se_rvsvars' `_se_cons'"
			}
			if ("`fitted'" != "") {
				gen double  _fitted =.
				gen double  _residuals =.
				local fitres "_fitted _residuals"
			}

			local ResultsVars "_Nobs _R2 _adjR2   `b_rvsvars' `_b_cons' `_se_rvsvars'  `fitres' `_b_rmse'"
		}

		if "`timevar'" != "" {
			local by "`timevar'"
		}
		
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

				if "`fw'" == "" qui bysort `__GByVars' `rangevar' : gen `touse2' = _n == _N
				else            qui bysort `__GByVars' `rangevar' : gen `touse2' = _n == 1
			} 
		}




		if "`bw'" != "" {

			if "`fw'" == "" {
				mata: ASREGW(				///
					"`varlist' `_CONS'",  	///
					"`__GByVars'" ,		   	///
					"`ResultsVars'" , 	 	///
					`bw',		  			/// 
					`minimum', 	       		///
					`newey' ,			  	///
					"`rangevar'",	      	///
					"`__0dIf'"	,			///
					"`se'",           		///
					"`fitted'",      		/// 
					`c(version)' ,  		///
					"`rmse'",				///
					"`robust'",     		///
					"`noconstant'",  		///
					"`touse'",	    		///
					"`touse2'",				///
					"`exclude'"				///
					)

				if "`dt'" == "3" {

					if "`fitted'" != "" {
						loc removeFitted _fitted
						loc removeResiduals _residuals

						local  ResultsVars : list ResultsVars - removeFitted
						local  ResultsVars : list ResultsVars - removeResiduals
					}
					
					foreach v of varlist `ResultsVars' {
						qui bys `__GByVars' `rangevar': replace `v' =`v'[_N]
					}
					
					if "`fitted'" != "" gen_residual_fitted `rhs', depvar(`lhsvar') constant(`_b_cons')

				}


			}
			else  {
				mata: ASREGFW(				///
					"`varlist' `_CONS'",  	///
					"`__GByVars'" ,		   	///
					"`ResultsVars'" , 	 	///
					`bw',		   			/// 
					`fw', 					///
					`minimum', 	       		///
					`newey' ,			  	///
					"`rangevar'",	      	///
					"`dt'"	,				///
					"`se'",           		///
					"`fitted'",      		/// 
					`c(version)' ,  		///
					"`rmse'",				///
					"`robust'",     		///
					"`noconstant'",  		///
					"`touse'",	    		///
					"`touse2'",				///
					"`exclude'"				///
					)
				if "`dt'" == "3" {
					foreach v of varlist `ResultsVars' {
						qui bys `__GByVars' `rangevar': replace `v' =`v'[1]
					}
				}
			}


		}

		else{

			mata: ASREGNW(         		///
				"`varlist' `_CONS'",    ///
				"`__GByVars'" ,			///
				"`ResultsVars'" , 		///
				"`se'", 				///
				"`fitted'",				///
				`minimum',				///
				`newey' , 				///
				"`rmse'",				///
				"`robust'",		    	///
				"`noconstant'",  		///
				"`touse'",	         	///
				"`exclude'"				///
				)
		}
		cap qui label variable `generate' "`stat' of `varlist' in a rol. window"
		if "`keep'"!="" {
			local keep _fitted
			qui cap unab v : _se_*
			cap confirm var _fitted 
			if _rc==0 local var `var' _fitted _residuals
			cap noi unab b : _b_*
			local all `b' `var' _R2 _adjR2 _Nobs
			local drop : list all - keep
			drop `drop'
		}
	} 

	else { 
		marksample touse
		preserve
		qui _xt
		local timevar `r(tvar)'
		sort `timevar'
		local nvars : word count `varlist'

		if `newey'< 0 { 
			di in red `"newey(`newey') invalid lag selected"'
			exit 198
		}

		gettoken lhsvar rhs : varlist

		tsrevar `lhsvar'
		loc lhsvar  `r(varlist)'

		// tsrevar, list

		if (strmatch("`rhs'", "*.*")) {
			tsrevar `rhs'
			loc rhsvars  `r(varlist)'
			tsrevar `rhs', list
			loc rhs  `r(varlist)'
		}
		else loc rhsvars `rhs'

		loc varlist "`lhsvar' `rhsvars'"

		qui count if `touse'
		local observations = r(N)

		loc IFaweightExists 0

		if ("`weight'" == "aweight") {
		    loc aweight `exp'
			loc IFaweightExists 1
			loc __aweight __aweight
		    asreg_aweights `varlist', aweight(`aweight') `noconstant'

		}

		qui {	
			foreach i of varlist `rhs'{

				gen double _b_`i'=.

				local b_rvsvars "`b_rvsvars' _b_`i'"
			}

			cap drop _TimeVar obs R2 cons 

			gen _R2      = .
			gen _adjR2   = .
			gen _TimeVar = .
			gen _obs     = .

			if "`noconstant'" == "" {
				gen _Cons = .
				loc _constant _Cons
				loc cons ":cons"
			}

			local ResultsVars "_TimeVar _obs _R2 _adjR2  `b_rvsvars' `_constant'"

		}

		if `IFaweightExists' {

		    mata: fmb_first_stage_aw("`varlist' `__aweight'",   /// 
				"`timevar'" , "`ResultsVars'", "`aweight'" ,        ///
				"`noconstant'", "`touse'")
		}

		else mata: fmb_first_stage("`varlist'", "`timevar'" , "`ResultsVars'" ,  ///
			"`noconstant'", "`newey'", "`touse'")

		qui count if _obs != .

		loc periods = r(N)

		if ("`save'" != "") {

			keep if _obs != .

			qui save "`save'", replace
		}

		if ("`first'" != "") report_first_stage_fmb `ResultsVars', timevar(`timevar')
		
		if (`newey' == 0) 	mata: fmb_with_se("`b_rvsvars'", "`noconstant'")

		else mata: fmb_with_newey("`b_rvsvars' `_constant'", `newey')

		foreach var of local rhsvars {

			local Labels "`Labels' :`var'"
		}

		qui sum _R2
		ereturn local avgr2 = r(mean)
		qui sum _adjR2, meanonly
		
		ereturn local r2_a = r(mean)
		restore		

		if "`shanken'" != "" {

			mata: shanken_se("v", "b", "`shanken'", `periods',  "`c(os)'")
		}
		matrix rownames b = `lhsvar'
		matrix colnames b = `Labels' `cons'
		matrix rownames v = `Labels' `cons'
		matrix colnames v = `Labels' `cons'

		ereturn clear
		ereturn post b v, esample(`touse') depname("`lhsvar'")

		ereturn scalar N = `observations'
		ereturn scalar N_g = `periods'
		ereturn scalar df_m = wordcount("`rhsvars'")
		ereturn scalar df_r = `periods' - (wordcount("`rhsvars'")+1)
		local df_r = `periods' - (wordcount("`rhsvars'")+1)

		cast_e_here df_r `df_r'


		qui if "`rhsvars'"!=""  test `rhsvars', min  
		ereturn scalar F = r(F)

		ereturn scalar r2 = `avgR2'
		ereturn scalar r2_a = `adjR2'

		if `newey' == 0 {
			if "`shanken'" == "" {
				ereturn local vcetype "Fama-MacBeth"
				local title "Fama-MacBeth (1973) Two-Step procedure"
			}
			else {
				ereturn local vcetype "Shanken"
				local title "Fama-MacBeth procedure with Shanken Correction"
			}

		} 
		else {
			ereturn local vcetype "Newey-FMB"
			ereturn local title "Fama-MacBeth Two-Step procedure (Newey SE)"
			local title "Fama-MacBeth Two-Step procedure (Newey SE)"
			local Newey_Text "(Newey-West adj. Std. Err. using lags(`newey'))"

		}

		ereturn local depvar "`lhsvar'"
		ereturn local method "Fama-MacBeth Two-Step procedure"
		ereturn local cmd "asreg"
		local R2text "avg. R-squared    =    "
		local adjR2text "Adj. R-squared    =    "
		#delimit ;
		disp _n
		in green `"`title'"'
		_col(50) in green `"Number of obs     ="' in yellow %10.0f `observations' _n
		in green "`Newey_Text'"
		_col(50) in green `"Num. time periods ="' in yellow %10.0f e(N_g) _n
		_col(50) in green `"F("' in yellow %3.0f e(df_m) in green `","' in yellow %6.0f e(df_r)
		in green `")"' _col(68) `"="' in yellow %10.2f e(F) _n
		_col(50) in green `"Prob > F          =    "' 
		in yellow %6.4f fprob(e(df_m),e(df_r),e(F)) _n 
		_col(1) in green `"`SE_Text'"'
		_col(50) in green `"`R2text'"' in yellow %5.4f `avgR2' _n
		_col(50) in green `"`adjR2text'"' in yellow %5.4f `adjR2'
		;
		#delimit cr
		ereturn display, level(95)


		if "`save'" != "" {

			preserve

			use "`save'", clear
			qui keep `ResultsVars'
			capture qui rename _TimeVar `timevar'
			qui save "`save'", replace
			di as smcl `"First stage regression results saved in {browse "`save'.dta"}"'
		}
	}
end

program define cast_e_here, eclass
	ereturn scalar `1' = `2'
end

* gen_residual_fitted: Version 1.0 Jan 7, 2021
program define gen_residual_fitted

	syntax varlist, depvar(str) [constant(str) ] 
	if "`constant'" == "" local constant 0


	local sum_notation `constant'

	foreach v of local varlist {
		local sum_notation `sum_notation' + (`v' * _b_`v')
	}
	qui cap replace _fitted    = `sum_notation'     if _fitted       == .
	qui cap replace _residuals = `depvar' - _fitted if _residuals    == .
end

* asreg_aweights: Version 1.0 Oct 13, 2021 
program define asreg_aweights

	syntax varlist [if] [in], AWeight(str) [NOConstant]

	if ("`noconstant'" == "") loc __aweight __aweight

	quietly gen __aweight = sqrt(`aweight')

	foreach v of varlist `varlist' {

		qui replace `v' = `v' * __aweight

	}			

end


* report first stage fmb regressions: Version 1.0 July 2, 2023
program define report_first_stage_fmb

	syntax varlist, TIMEvar(varlist)
	preserve
	qui keep `varlist'
	qui drop if _obs == .
	foreach v of varlist `varlist' {
		qui format %8.0g `v'
	}
	
	display "{title:First stage Fama-McBeth regression results}"
	capture qui rename _TimeVar `timevar'
	capture qui rename _Cons constant
	capture qui rename _R2 R²
	capture qui rename _adjR2 adjR²
	capture qui rename _obs N
	
	qui ds _b_*
	loc betas `r(varlist)'
	
	foreach var of varlist `betas' {
		loc newName = subinstr("`var'", "_b_", "β_", 1)
		qui rename `var' `newName'
		loc varlist = subinstr("`varlist'", "`var'", "`newName'", 1)
		dis "`newName'"
		
	}
	
	loc varlist = subinstr("`varlist'", "_TimeVar", "`timevar'", 1)
	loc varlist = subinstr("`varlist'", "_Cons", "constant", 1)
	loc varlist = subinstr("`varlist'", "_R2", "R²", 1)
	loc varlist = subinstr("`varlist'", "_adjR2", "adjR²", 1)
	loc varlist = subinstr("`varlist'", "_obs", "N", 1)
	

	list `varlist'  , noobs mean separator(0)
	restore
end
