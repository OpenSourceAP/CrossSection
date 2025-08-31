

*! Inspirit of -winsor-(NJ Cox) and -winsorizeJ-(J Caskey)
*! Lian Yujun, arlionn@163.com, 2013-12-25
*! 1.1 2014.12.16

cap program drop winsor2
program def winsor2, sortpreserve 
        version 8
        syntax varlist(min=1) [if] [in] /* 
	*/  [, Suffix(str) REPLACE Trim Cuts(numlist max=2 min=2 >=0 <=100) by(varlist) Label] 

	if "`replace'"!="" & "`suffix'"!=""{
	  dis in w "suffix() " in red "cannot be specified with" in w " replace" 
	  exit 198
	}
	
	if "`suffix'"==""{
	   if "`trim'" == ""{ 
	     local suffix="_w"
	   }
	   else{
	     local suffix="_tr"
	   }
	}

	if "`cuts'"==""{
		local low=1
		local high=99
	}
	else{
		tokenize "`cuts'"
		local low=`1'
		mac shift
		local high=`1'
		if `low'>`high' {
			tempname tmp
			local `tmp'=`low'
			local low=`high'
			local high=`tmp'
		}
		if `low'>0&`low'<1|`high'>0&`high'<1{
		   if "`trim'"!=""{
		      local CUT "trim"
		   }
		   else{
		      local CUT "winsor"
		   }
		    dis in y "Warning: " in g "cuts(1   99) means `CUT' at   1th percentile and 99th percentile,"
			dis in g "         " in g "cuts(0.1 90) means `CUT' at 0.1th percentile and 90th percentile,"
			dis in g "         " in g "make sure cuts(`low' `high') you specified is what you want. "
		}
		if `low'==0&`high'==100{
		    dis in red "option cuts(`cuts') is incorrect, no action taken."
			exit 
		}
	}

	* Validate suffix
	if "`replace'" == ""{
	  foreach k of varlist `varlist' {
		capture confirm variable `k'`suffix', exact
		if _rc == 0 {
		    di as error "variable `k'`suffix' already exist, re-specify option -suffix()-"
			di as error "Suffix `suffix' is invalid for `k'"
			exit 111
		}
	  }
	}
	
	
	* Validate by list
	if "`by'" != "" {
		capture confirm variable `by'
		if _rc != 0 {
			di as error "by() list is invalid"
			exit 111
	    }
	}	
		
 
	* Winsorize or Trimming
	tempname if2
	if "`by'" == "" {   // no by()
		foreach k of varlist `varlist' {
			*qui centile `k' `if' `in', centile(`low' `high')
			if `low'!=0&`high'!=100{
			   qui _pctile `k' `if' `in', p(`low' `high')
			   local qleft = r(r1)
			   local qright= r(r2)
			}
			else if `low'==0{
			   qui _pctile `k' `if' `in', p(`high')
			   local qright = r(r1)
			   qui sum `k'
			   local qleft = r(min)
			}
			else if `high'==100{
			   qui _pctile `k' `if' `in', p(`low')
			   local qleft = r(r1)			
			   qui sum `k'
			   local qright = r(max)
			}
			if "`if'"==""{
			  local `if2' "if ~missing(`k')"
			}
			else{
			  local `if2' "`if' & ~missing(`k')"
			}
			
			local vtype=`"`: type `k''"'
			
			if "`replace'"!=""{  // replace
			  if "`trim'"==""{   //winsorize
			    qui replace `k' = max(min(`qright',`k'),`qleft') ``if2'' `in'
				 local labk : variable label `k'
				 local labk = cond("`labk'"=="","`k'","`labk'")
				 if "`label'"!=""{
				    if `low'<1{
					   local low "0`low'"
					}
			        label var `k' "`labk'-Winsor(p`low',p`high')"	
				 }
				 else{
				    label var `k' "`labk'"	
				 }
			  }
			  else{             //trimming
				qui replace `k' = cond(`k'<`qleft',.,`k') ``if2'' `in'
				qui replace `k' = cond(`k'>`qright',.,`k') ``if2'' `in'
			     local labk : variable label `k'
				 local labk = cond("`labk'"=="","`k'","`labk'")
				 if "`label'"!=""{
				    if `low'<1{
					   local low "0`low'"
					}
			        label var `k' "`labk'-Trim(p`low',p`high')"	
				 }
				 else{
				    label var `k' "`labk'"	
				 }				 			 
			  }
			}
			else{   // noreplace, gen new variable
			  if "`trim'"==""{  //winsorize
			    qui gen `vtype' `k'`suffix'=max(min(`qright',`k'),`qleft') ``if2'' `in'
				 local labk : variable label `k'
				 local labk = cond("`labk'"=="","`k'","`labk'")
				 if "`label'"!=""{
				    if `low'<1{
					   local low "0`low'"
					}
			        label var `k'`suffix' "`labk'-Winsor(p`low',p`high')"	
				 }
				 else{
				    label var `k'`suffix' "`labk'"	
				 }
			  }
			  else{             //Trimming
			    qui gen `vtype' `k'`suffix' = cond(`k'<`qleft',.,`k') ``if2'' `in'
				
				**********Modification 1 by LXC********************
				//qui replace     `k'`suffix' = cond(`k'>r(r2),.,`k') ``if2'' `in'
				qui replace     `k'`suffix' = cond(`k'>`qright',.,`k'`suffix') ``if2'' `in'
				**********Modification 1 ends**********************
			     local labk : variable label `k'
				 local labk = cond("`labk'"=="","`k'","`labk'")
				 if "`label'"!=""{
				    if `low'<1{
					   local low "0`low'"
					}
			        label var `k'`suffix' "`labk'-Trim(p`low',p`high')"	
				 }
				 else{
				    label var `k'`suffix' "`labk'"	
				 }			    
			  }
			}
		}
	}
	
	
	else{   // with by()
		foreach k of varlist `varlist' {
		    tempvar pL pH tL
			
			if "`if'"==""{
			   local `if2' "if ~missing(`k')"
			}
			else{
			   local `if2' "`if' & ~missing(`k')"
			}  
			
			local vtype=`"`:type `k''"'
			
			if `low'!=0&`high'!=100{
			   qui egen `vtype' `pL'=pctile(`k') ``if2'' `in', p(`low')  by(`by')  //lowbound
			   qui egen `vtype' `pH'=pctile(`k') ``if2'' `in', p(`high') by(`by')  //highbound
			}			
			else if `low'==0{
			   qui egen `vtype' `pL'=min(`k')    ``if2'' `in',           by(`by')  //lowbound
			   qui egen `vtype' `pH'=pctile(`k') ``if2'' `in', p(`high') by(`by')  //highbound
			}
			else if `high'==100{
			   qui egen `vtype' `pL'=pctile(`k') ``if2'' `in', p(`low')  by(`by')  //lowbound
			   qui egen `vtype' `pH'=max(`k')    ``if2'' `in',           by(`by')  //highbound
			}

			qui egen `vtype' `tL'=rowmax(`pL' `k') ``if2'' `in'
			
			if "`replace'"!=""{
			   if "`trim'"==""{   //winsorize
			     tempvar kwinsor
			     qui egen `vtype' `kwinsor'=rowmin(`pH' `tL') ``if2'' `in'
			     qui replace `k' = `kwinsor'
				 local labk : variable label `k'
				 local labk = cond("`labk'"=="","`k'","`labk'")
				 if "`label'"!=""{
				    if `low'<1{
					   local low "0`low'"
					}
			        label var `k' "`labk'-Winsor(p`low',p`high')"	
				 }
				 else{
				    label var `k' "`labk'"	
				 }
			     qui drop `kwinsor'
			   }
			   else{              //Trimming
				 qui replace `k' = cond(`k'<`pL',.,`k') ``if2'' `in'
				 qui replace `k' = cond(`k'>`pH',.,`k') ``if2'' `in'
			     local labk : variable label `k'
				 local labk = cond("`labk'"=="","`k'","`labk'")
				 if "`label'"!=""{
				    if `low'<1{
					   local low "0`low'"
					}
			        label var `k' "`labk'-Trim(p`low',p`high')"	
				 }
				 else{
				    label var `k' "`labk'"	
				 }				 
			   }
			}
			
			else{
			   if "`trim'"==""{   //winsorize
			     qui egen `k'`suffix'=rowmin(`pH' `tL') ``if2'' `in'
			     qui drop `pL' `pH' `tL'
			     local labk : variable label `k'
				 local labk = cond("`labk'"=="","`k'","`labk'")
				 if "`label'"!=""{
				    if `low'<1{
					   local low "0`low'"
					}
			        label var `k'`suffix' "`labk'-Winsor(p`low',p`high')"	
				 }
				 else{
				    label var `k'`suffix' "`labk'"	
				 }
			   }
			   else{
			     qui gen `vtype' `k'`suffix' = cond(`k'<`pL',.,`k') ``if2'' `in'
				 
				 **********Modification 2 by LXC********************
				 //qui replace     `k'`suffix' = cond(`k'>`pH',.,`k') ``if2'' `in'
				 qui replace     `k'`suffix' = cond(`k'>`pH',.,`k'`suffix') ``if2'' `in'
				 **********Modification 2 ends**********************
			     local labk : variable label `k'
				 local labk = cond("`labk'"=="","`k'","`labk'")
				 if "`label'"!=""{
				    if `low'<1{
					   local low "0`low'"
					}
			        label var `k'`suffix' "`labk'-Trim(p`low',p`high')"	
				 }
				 else{
				    label var `k'`suffix' "`labk'"	
				 }			     
			   }
			}
		    
		}
	} 
		
	

end
