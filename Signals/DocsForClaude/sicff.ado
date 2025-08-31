
// Program for turning SIC codes into Fama French 12 industries

// Takes a single input: the (numeric) variable identifying the SIC code

program sicff
	// Version
	version 10.0

	// Syntax
	syntax varname(numeric), INDustry(integer) [ GENerate(name local) Longlabels]

	// If user does not specify a name for newvar, then set newvar to "ff_`industry'"
	if "`generate'" == "" {
		local generate = "ff_`industry'"
	}

	// Create the variable
	qui gen byte `generate' = .

	// Fama French 5 industry
	if `industry' == 5 {

		// define label
		if "`longlabels'" != "" {
			// the long label
			label define lbl_ff_5 1 "(1) Consumer Durables, Nondurables, Wholesale, Retail, and Some Services (Laundries, Repair Shops)"
			label define lbl_ff_5 2 "(2) Manufacturing, Energy, and Utilities", add
			label define lbl_ff_5 3 "(3) Business Equipment, Telephone and Television Transmission", add
			label define lbl_ff_5 4 "(4) Healthcare, Medical Equipment, and Drugs", add
			label define lbl_ff_5 5 "(5) Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment, Finance", add
		}
		else {
			// the short label
			label define lbl_ff_5 1 "(1) Cnsmr" 2 "(2) Manuf" 3 "(3) HiTec" 4 "(4) Hlth" 5 "(5) Other"
		}
		label values `generate' lbl_ff_5

		// the actual assignment
		qui replace `generate' = 1 if inrange(`varlist', 0100, 0999) | inrange(`varlist', 2000, 2399) | inrange(`varlist', 2700, 2749) | inrange(`varlist', 2770, 2799) | inrange(`varlist', 3100, 3199) | inrange(`varlist', 3940, 3989) | inrange(`varlist', 2500, 2519) | inrange(`varlist', 2590, 2599) | inrange(`varlist', 3630, 3659) | inrange(`varlist', 3710, 3711) | inrange(`varlist', 3714, 3714) | inrange(`varlist', 3716, 3716) | inrange(`varlist', 3750, 3751) | inrange(`varlist', 3792, 3792) | inrange(`varlist', 3900, 3939) | inrange(`varlist', 3990, 3999) | inrange(`varlist', 5000, 5999) | inrange(`varlist', 7200, 7299) | inrange(`varlist', 7600, 7699)
		
		qui replace `generate' = 2 if inrange(`varlist', 2520, 2589) | inrange(`varlist', 2600, 2699) | inrange(`varlist', 2750, 2769) | inrange(`varlist', 2800, 2829) | inrange(`varlist', 2840, 2899) | inrange(`varlist', 3000, 3099) | inrange(`varlist', 3200, 3569) | inrange(`varlist', 3580, 3621) | inrange(`varlist', 3623, 3629) | inrange(`varlist', 3700, 3709) | inrange(`varlist', 3712, 3713) | inrange(`varlist', 3715, 3715) | inrange(`varlist', 3717, 3749) | inrange(`varlist', 3752, 3791) | inrange(`varlist', 3793, 3799) | inrange(`varlist', 3860, 3899) | inrange(`varlist', 1200, 1399) | inrange(`varlist', 2900, 2999) | inrange(`varlist', 4900, 4949)
		
		qui replace `generate' = 3 if inrange(`varlist', 3570, 3579) | inrange(`varlist', 3622, 3622) | inrange(`varlist', 3660, 3692) | inrange(`varlist', 3694, 3699) | inrange(`varlist', 3810, 3839) | inrange(`varlist', 7370, 7372) | inrange(`varlist', 7373, 7373) | inrange(`varlist', 7374, 7374) | inrange(`varlist', 7375, 7375) | inrange(`varlist', 7376, 7376) | inrange(`varlist', 7377, 7377) | inrange(`varlist', 7378, 7378) | inrange(`varlist', 7379, 7379) | inrange(`varlist', 7391, 7391) | inrange(`varlist', 8730, 8734) | inrange(`varlist', 4800, 4899)
		
		qui replace `generate' = 4 if inrange(`varlist', 2830, 2839) | inrange(`varlist', 3693, 3693) | inrange(`varlist', 3840, 3859) | inrange(`varlist', 8000, 8099)
		
		qui replace `generate' = 5 if `generate' == . & inrange(`varlist', 100, 9999)
	}



	// Fama French 10 industry
	else if `industry' == 10 {

		// define label
		if "`longlabels'" != "" {
			// the long label
			label define lbl_ff_10 1 "(1) Consumer Nondurables -- Food, Tobacco, Textiles, Apparel, Leather, Toys"
			label define lbl_ff_10 2 "(2) Consumer Durables -- Cars, TVs, Furniture, Household Appliances", add
			label define lbl_ff_10 3 "(3) Manufacturing -- Machinery, Trucks, Planes, Chemicals, Off Furn, Paper, Com Printing", add
			label define lbl_ff_10 4 "(4) Oil, Gas, and Coal Extraction and Products", add
			label define lbl_ff_10 5 "(5) Business Equipment -- Computers, Software, and Electronic Equipment", add
			label define lbl_ff_10 6 "(6) Telephone and Television Transmission", add
			label define lbl_ff_10 7 "(7) Wholesale, Retail, and Some Services (Laundries, Repair Shops)", add
			label define lbl_ff_10 8 "(8) Healthcare, Medical Equipment, and Drugs", add
			label define lbl_ff_10 9 "(9) Utilities", add
			label define lbl_ff_10 10 "(10) Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment, Finance", add
		}
		else {
			// the short label
			label define lbl_ff_10 1 "(1) NoDur" 2 "(2) Durbl" 3 "(3) Manuf" 4 "(4) Enrgy" 5 "(5) HiTec" 6 "(6) Telcm" 7 "(7) Shops" 8 "(8) Hlth" 9 "(9) Utils" 10 "(10) Other"
		}
		label values `generate' lbl_ff_10

		// the actual assignment
		qui replace `generate' = 1 if inrange(`varlist', 0100, 0999) | inrange(`varlist', 2000, 2399) | inrange(`varlist', 2700, 2749) | inrange(`varlist', 2770, 2799) | inrange(`varlist', 3100, 3199) | inrange(`varlist', 3940, 3989)
		
		qui replace `generate' = 2 if inrange(`varlist', 2500, 2519) | inrange(`varlist', 2590, 2599) | inrange(`varlist', 3630, 3659) | inrange(`varlist', 3710, 3711) | inrange(`varlist', 3714, 3714) | inrange(`varlist', 3716, 3716) | inrange(`varlist', 3750, 3751) | inrange(`varlist', 3792, 3792) | inrange(`varlist', 3900, 3939) | inrange(`varlist', 3990, 3999)
		
		qui replace `generate' = 3 if inrange(`varlist', 2520, 2589) | inrange(`varlist', 2600, 2699) | inrange(`varlist', 2750, 2769) | inrange(`varlist', 2800, 2829) | inrange(`varlist', 2840, 2899) | inrange(`varlist', 3000, 3099) | inrange(`varlist', 3200, 3569) | inrange(`varlist', 3580, 3621) | inrange(`varlist', 3623, 3629) | inrange(`varlist', 3700, 3709) | inrange(`varlist', 3712, 3713) | inrange(`varlist', 3715, 3715) | inrange(`varlist', 3717, 3749) | inrange(`varlist', 3752, 3791) | inrange(`varlist', 3793, 3799) | inrange(`varlist', 3860, 3899)
		
		qui replace `generate' = 4 if inrange(`varlist', 1200, 1399) | inrange(`varlist', 2900, 2999)
		
		qui replace `generate' = 5 if inrange(`varlist', 3570, 3579) | inrange(`varlist', 3622, 3622) | inrange(`varlist', 3660, 3692) | inrange(`varlist', 3694, 3699) | inrange(`varlist', 3810, 3839) | inrange(`varlist', 7370, 7372) | inrange(`varlist', 7373, 7373) | inrange(`varlist', 7374, 7374) | inrange(`varlist', 7375, 7375) | inrange(`varlist', 7376, 7376) | inrange(`varlist', 7377, 7377) | inrange(`varlist', 7378, 7378) | inrange(`varlist', 7379, 7379) | inrange(`varlist', 7391, 7391) | inrange(`varlist', 8730, 8734)
		
		qui replace `generate' = 6 if inrange(`varlist', 4800, 4899)
		
		qui replace `generate' = 7 if inrange(`varlist', 5000, 5999) | inrange(`varlist', 7200, 7299) | inrange(`varlist', 7600, 7699)
		
		qui replace `generate' = 8 if inrange(`varlist', 2830, 2839) | inrange(`varlist', 3693, 3693) | inrange(`varlist', 3840, 3859) | inrange(`varlist', 8000, 8099)
		
		qui replace `generate' = 9 if inrange(`varlist', 4900, 4949)
		
		qui replace `generate' = 10 if `generate' == . & inrange(`varlist', 100, 9999)
	}



	// Fama French 12 industry
	else if `industry' == 12 {

		// define label
		if "`longlabels'" != "" {
			// the long label
			label define lbl_ff_12 1 "(1) Consumer Nondurables -- Food, Tobacco, Textiles, Apparel, Leather, Toys"
			label define lbl_ff_12 2 "(2) Consumer Durables -- Cars, TVs, Furniture, Household Appliances", add
			label define lbl_ff_12 3 "(3) Manufacturing -- Machinery, Trucks, Planes, Off Furn, Paper, Com Printing", add
			label define lbl_ff_12 4 "(4) Oil, Gas, and Coal Extraction and Products", add
			label define lbl_ff_12 5 "(5) Chemicals and Allied Products", add
			label define lbl_ff_12 6 "(6) Business Equipment -- Computers, Software, and Electronic Equipment", add
			label define lbl_ff_12 7 "(7) Telephone and Television Transmission", add
			label define lbl_ff_12 8 "(8) Utilities", add
			label define lbl_ff_12 9 "(9) Wholesale, Retail, and Some Services (Laundries, Repair Shops)", add
			label define lbl_ff_12 10 "(10)  Healthcare, Medical Equipment, and Drugs", add
			label define lbl_ff_12 11 "(11) Finance", add
			label define lbl_ff_12 12 "(12) Other -- Mines, Constr, BldMt, Trans, Hotels, Bus Serv, Entertainment", add
		}
		else {
			// the short label
			label define lbl_ff_12 1 "(1) NoDur" 2 "(2) Durbl" 3 "(3) Manuf" 4 "(4) Enrgy" 5 "(5) Chems" 6 "(6) BusEq" 7 "(7) Telcm" 8 "(8) Utils" 9 "(9) Shops" 10 "(10) Hlth" 11 "(11) Money" 12 "(12) Other"
		}
		label values `generate' lbl_ff_12

		// the actual assignment
		qui replace `generate' = 1 if inrange(`varlist', 0100, 0999) | inrange(`varlist', 2000, 2399) | inrange(`varlist', 2700, 2749) | inrange(`varlist', 2770, 2799) | inrange(`varlist', 3100, 3199) | inrange(`varlist', 3940, 3989)
		
		qui replace `generate' = 2 if inrange(`varlist', 2500, 2519) | inrange(`varlist', 2590, 2599) | inrange(`varlist', 3630, 3659) | inrange(`varlist', 3710, 3711) | inrange(`varlist', 3714, 3714) | inrange(`varlist', 3716, 3716) | inrange(`varlist', 3750, 3751) | inrange(`varlist', 3792, 3792) | inrange(`varlist', 3900, 3939) | inrange(`varlist', 3990, 3999)
		
		qui replace `generate' = 3 if inrange(`varlist', 2520, 2589) | inrange(`varlist', 2600, 2699) | inrange(`varlist', 2750, 2769) | inrange(`varlist', 3000, 3099) | inrange(`varlist', 3200, 3569) | inrange(`varlist', 3580, 3629) | inrange(`varlist', 3700, 3709) | inrange(`varlist', 3712, 3713) | inrange(`varlist', 3715, 3715) | inrange(`varlist', 3717, 3749) | inrange(`varlist', 3752, 3791) | inrange(`varlist', 3793, 3799) | inrange(`varlist', 3830, 3839) | inrange(`varlist', 3860, 3899)
		
		qui replace `generate' = 4 if inrange(`varlist', 1200, 1399) | inrange(`varlist', 2900, 2999)
		
		qui replace `generate' = 5 if inrange(`varlist', 2800, 2829) | inrange(`varlist', 2840, 2899)
		
		qui replace `generate' = 6 if inrange(`varlist', 3570, 3579) | inrange(`varlist', 3660, 3692) | inrange(`varlist', 3694, 3699) | inrange(`varlist', 3810, 3829) | inrange(`varlist', 7370, 7379)
		
		qui replace `generate' = 7 if inrange(`varlist', 4800, 4899)
		
		qui replace `generate' = 8 if inrange(`varlist', 4900, 4949)
		
		qui replace `generate' = 9 if inrange(`varlist', 5000, 5999) | inrange(`varlist', 7200, 7299) | inrange(`varlist', 7600, 7699)
		
		qui replace `generate' = 10 if inrange(`varlist', 2830, 2839) | inrange(`varlist', 3693, 3693) | inrange(`varlist', 3840, 3859) | inrange(`varlist', 8000, 8099)
		
		qui replace `generate' = 11 if inrange(`varlist', 6000, 6999)
		
		qui replace `generate' = 12 if `generate' == . & inrange(`varlist', 100, 9999)
	}



	// Fama French 17 industry
	else if `industry' == 17 {

		// define label
		if "`longlabels'" != "" {
			// the long label
			label define lbl_ff_17 1 "(1) Food"
			label define lbl_ff_17 2 "(2) Mining and Minerals", add
			label define lbl_ff_17 3 "(3) Oil and Petroleum Products", add
			label define lbl_ff_17 4 "(4) Textiles, Apparel & Footwear", add
			label define lbl_ff_17 5 "(5) Consumer Durables", add
			label define lbl_ff_17 6 "(6) Chemicals", add
			label define lbl_ff_17 7 "(7) Drugs, Soap, Perfumes, Tobacco", add
			label define lbl_ff_17 8 "(8) Construction and Construction Materials", add
			label define lbl_ff_17 9 "(9) Steel Works Etc", add
			label define lbl_ff_17 10 "(10) Fabricated Products", add
			label define lbl_ff_17 11 "(11) Machinery and Business Equipment", add
			label define lbl_ff_17 12 "(12) Automobiles", add
			label define lbl_ff_17 13 "(13) Transportation", add
			label define lbl_ff_17 14 "(14) Utilities", add
			label define lbl_ff_17 15 "(15) Retail Stores", add
			label define lbl_ff_17 16 "(16) Banks, Insurance Companies, and Other Financials", add
			label define lbl_ff_17 17 "(17) Other", add
		}
		else {
			// the short label
			label define lbl_ff_17 1 "(1) Food" 2 "(2) Mines" 3 "(3) Oil" 4 "(4) Clths" 5 "(5) Durbl" 6 "(6) Chems" 7 "(7) Cnsum" 8 "(8) Cnstr" 9 "(9) Steel" 10 "(10) FabPr" 11 "(11) Machn" 12 "(12) Cars" 13 "(13) Trans" 14 "(14) Utils" 15 "(15) Rtail" 16 "(16) Finan" 17 "(17) Other"
		}
		label values `generate' lbl_ff_17

		// the actual assignment
		qui replace `generate' = 1 if inrange(`varlist', 0100, 0199) | inrange(`varlist', 0200, 0299) | inrange(`varlist', 0700, 0799) | inrange(`varlist', 0900, 0999) | inrange(`varlist', 2000, 2009) | inrange(`varlist', 2010, 2019) | inrange(`varlist', 2020, 2029) | inrange(`varlist', 2030, 2039) | inrange(`varlist', 2040, 2046) | inrange(`varlist', 2047, 2047) | inrange(`varlist', 2048, 2048) | inrange(`varlist', 2050, 2059) | inrange(`varlist', 2060, 2063) | inrange(`varlist', 2064, 2068) | inrange(`varlist', 2070, 2079) | inrange(`varlist', 2080, 2080) | inrange(`varlist', 2082, 2082) | inrange(`varlist', 2083, 2083) | inrange(`varlist', 2084, 2084) | inrange(`varlist', 2085, 2085) | inrange(`varlist', 2086, 2086) | inrange(`varlist', 2087, 2087) | inrange(`varlist', 2090, 2092) | inrange(`varlist', 2095, 2095) | inrange(`varlist', 2096, 2096) | inrange(`varlist', 2097, 2097) | inrange(`varlist', 2098, 2099) | inrange(`varlist', 5140, 5149) | inrange(`varlist', 5150, 5159) | inrange(`varlist', 5180, 5182) | inrange(`varlist', 5191, 5191)
		
		qui replace `generate' = 2 if inrange(`varlist', 1000, 1009) | inrange(`varlist', 1010, 1019) | inrange(`varlist', 1020, 1029) | inrange(`varlist', 1030, 1039) | inrange(`varlist', 1040, 1049) | inrange(`varlist', 1060, 1069) | inrange(`varlist', 1080, 1089) | inrange(`varlist', 1090, 1099) | inrange(`varlist', 1200, 1299) | inrange(`varlist', 1400, 1499) | inrange(`varlist', 5050, 5052)
		
		qui replace `generate' = 3 if inrange(`varlist', 1300, 1300) | inrange(`varlist', 1310, 1319) | inrange(`varlist', 1320, 1329) | inrange(`varlist', 1380, 1380) | inrange(`varlist', 1381, 1381) | inrange(`varlist', 1382, 1382) | inrange(`varlist', 1389, 1389) | inrange(`varlist', 2900, 2912) | inrange(`varlist', 5170, 5172)
		
		qui replace `generate' = 4 if inrange(`varlist', 2200, 2269) | inrange(`varlist', 2270, 2279) | inrange(`varlist', 2280, 2284) | inrange(`varlist', 2290, 2295) | inrange(`varlist', 2296, 2296) | inrange(`varlist', 2297, 2297) | inrange(`varlist', 2298, 2298) | inrange(`varlist', 2299, 2299) | inrange(`varlist', 2300, 2390) | inrange(`varlist', 2391, 2392) | inrange(`varlist', 2393, 2395) | inrange(`varlist', 2396, 2396) | inrange(`varlist', 2397, 2399) | inrange(`varlist', 3020, 3021) | inrange(`varlist', 3100, 3111) | inrange(`varlist', 3130, 3131) | inrange(`varlist', 3140, 3149) | inrange(`varlist', 3150, 3151) | inrange(`varlist', 3963, 3965) | inrange(`varlist', 5130, 5139)
		
		qui replace `generate' = 5 if inrange(`varlist', 2510, 2519) | inrange(`varlist', 2590, 2599) | inrange(`varlist', 3060, 3069) | inrange(`varlist', 3070, 3079) | inrange(`varlist', 3080, 3089) | inrange(`varlist', 3090, 3099) | inrange(`varlist', 3630, 3639) | inrange(`varlist', 3650, 3651) | inrange(`varlist', 3652, 3652) | inrange(`varlist', 3860, 3861) | inrange(`varlist', 3870, 3873) | inrange(`varlist', 3910, 3911) | inrange(`varlist', 3914, 3914) | inrange(`varlist', 3915, 3915) | inrange(`varlist', 3930, 3931) | inrange(`varlist', 3940, 3949) | inrange(`varlist', 3960, 3962) | inrange(`varlist', 5020, 5023) | inrange(`varlist', 5064, 5064) | inrange(`varlist', 5094, 5094) | inrange(`varlist', 5099, 5099)
		
		qui replace `generate' = 6 if inrange(`varlist', 2800, 2809) | inrange(`varlist', 2810, 2819) | inrange(`varlist', 2820, 2829) | inrange(`varlist', 2860, 2869) | inrange(`varlist', 2870, 2879) | inrange(`varlist', 2890, 2899) | inrange(`varlist', 5160, 5169)
		
		qui replace `generate' = 7 if inrange(`varlist', 2100, 2199) | inrange(`varlist', 2830, 2830) | inrange(`varlist', 2831, 2831) | inrange(`varlist', 2833, 2833) | inrange(`varlist', 2834, 2834) | inrange(`varlist', 2840, 2843) | inrange(`varlist', 2844, 2844) | inrange(`varlist', 5120, 5122) | inrange(`varlist', 5194, 5194)
		
		qui replace `generate' = 8 if inrange(`varlist', 0800, 0899) | inrange(`varlist', 1500, 1511) | inrange(`varlist', 1520, 1529) | inrange(`varlist', 1530, 1539) | inrange(`varlist', 1540, 1549) | inrange(`varlist', 1600, 1699) | inrange(`varlist', 1700, 1799) | inrange(`varlist', 2400, 2439) | inrange(`varlist', 2440, 2449) | inrange(`varlist', 2450, 2459) | inrange(`varlist', 2490, 2499) | inrange(`varlist', 2850, 2859) | inrange(`varlist', 2950, 2952) | inrange(`varlist', 3200, 3200) | inrange(`varlist', 3210, 3211) | inrange(`varlist', 3240, 3241) | inrange(`varlist', 3250, 3259) | inrange(`varlist', 3261, 3261) | inrange(`varlist', 3264, 3264) | inrange(`varlist', 3270, 3275) | inrange(`varlist', 3280, 3281) | inrange(`varlist', 3290, 3293) | inrange(`varlist', 3420, 3429) | inrange(`varlist', 3430, 3433) | inrange(`varlist', 3440, 3441) | inrange(`varlist', 3442, 3442) | inrange(`varlist', 3446, 3446) | inrange(`varlist', 3448, 3448) | inrange(`varlist', 3449, 3449) | inrange(`varlist', 3450, 3451) | inrange(`varlist', 3452, 3452) | inrange(`varlist', 5030, 5039) | inrange(`varlist', 5070, 5078) | inrange(`varlist', 5198, 5198) | inrange(`varlist', 5210, 5211) | inrange(`varlist', 5230, 5231) | inrange(`varlist', 5250, 5251)
		
		qui replace `generate' = 9 if inrange(`varlist', 3300, 3300) | inrange(`varlist', 3310, 3317) | inrange(`varlist', 3320, 3325) | inrange(`varlist', 3330, 3339) | inrange(`varlist', 3340, 3341) | inrange(`varlist', 3350, 3357) | inrange(`varlist', 3360, 3369) | inrange(`varlist', 3390, 3399)
		
		qui replace `generate' = 10 if inrange(`varlist', 3410, 3412) | inrange(`varlist', 3443, 3443) | inrange(`varlist', 3444, 3444) | inrange(`varlist', 3460, 3469) | inrange(`varlist', 3470, 3479) | inrange(`varlist', 3480, 3489) | inrange(`varlist', 3490, 3499)
		
		qui replace `generate' = 11 if inrange(`varlist', 3510, 3519) | inrange(`varlist', 3520, 3529) | inrange(`varlist', 3530, 3530) | inrange(`varlist', 3531, 3531) | inrange(`varlist', 3532, 3532) | inrange(`varlist', 3533, 3533) | inrange(`varlist', 3534, 3534) | inrange(`varlist', 3535, 3535) | inrange(`varlist', 3536, 3536) | inrange(`varlist', 3540, 3549) | inrange(`varlist', 3550, 3559) | inrange(`varlist', 3560, 3569) | inrange(`varlist', 3570, 3579) | inrange(`varlist', 3580, 3580) | inrange(`varlist', 3581, 3581) | inrange(`varlist', 3582, 3582) | inrange(`varlist', 3585, 3585) | inrange(`varlist', 3586, 3586) | inrange(`varlist', 3589, 3589) | inrange(`varlist', 3590, 3599) | inrange(`varlist', 3600, 3600) | inrange(`varlist', 3610, 3613) | inrange(`varlist', 3620, 3621) | inrange(`varlist', 3622, 3622) | inrange(`varlist', 3623, 3629) | inrange(`varlist', 3670, 3679) | inrange(`varlist', 3680, 3680) | inrange(`varlist', 3681, 3681) | inrange(`varlist', 3682, 3682) | inrange(`varlist', 3683, 3683) | inrange(`varlist', 3684, 3684) | inrange(`varlist', 3685, 3685) | inrange(`varlist', 3686, 3686) | inrange(`varlist', 3687, 3687) | inrange(`varlist', 3688, 3688) | inrange(`varlist', 3689, 3689) | inrange(`varlist', 3690, 3690) | inrange(`varlist', 3691, 3692) | inrange(`varlist', 3693, 3693) | inrange(`varlist', 3694, 3694) | inrange(`varlist', 3695, 3695) | inrange(`varlist', 3699, 3699) | inrange(`varlist', 3810, 3810) | inrange(`varlist', 3811, 3811) | inrange(`varlist', 3812, 3812) | inrange(`varlist', 3820, 3820) | inrange(`varlist', 3821, 3821) | inrange(`varlist', 3822, 3822) | inrange(`varlist', 3823, 3823) | inrange(`varlist', 3824, 3824) | inrange(`varlist', 3825, 3825) | inrange(`varlist', 3826, 3826) | inrange(`varlist', 3827, 3827) | inrange(`varlist', 3829, 3829) | inrange(`varlist', 3830, 3839) | inrange(`varlist', 3950, 3955) | inrange(`varlist', 5060, 5060) | inrange(`varlist', 5063, 5063) | inrange(`varlist', 5065, 5065) | inrange(`varlist', 5080, 5080) | inrange(`varlist', 5081, 5081)
		
		qui replace `generate' = 12 if inrange(`varlist', 3710, 3710) | inrange(`varlist', 3711, 3711) | inrange(`varlist', 3714, 3714) | inrange(`varlist', 3716, 3716) | inrange(`varlist', 3750, 3751) | inrange(`varlist', 3792, 3792) | inrange(`varlist', 5010, 5015) | inrange(`varlist', 5510, 5521) | inrange(`varlist', 5530, 5531) | inrange(`varlist', 5560, 5561) | inrange(`varlist', 5570, 5571) | inrange(`varlist', 5590, 5599)
		
		qui replace `generate' = 13 if inrange(`varlist', 3713, 3713) | inrange(`varlist', 3715, 3715) | inrange(`varlist', 3720, 3720) | inrange(`varlist', 3721, 3721) | inrange(`varlist', 3724, 3724) | inrange(`varlist', 3725, 3725) | inrange(`varlist', 3728, 3728) | inrange(`varlist', 3730, 3731) | inrange(`varlist', 3732, 3732) | inrange(`varlist', 3740, 3743) | inrange(`varlist', 3760, 3769) | inrange(`varlist', 3790, 3790) | inrange(`varlist', 3795, 3795) | inrange(`varlist', 3799, 3799) | inrange(`varlist', 4000, 4013) | inrange(`varlist', 4100, 4100) | inrange(`varlist', 4110, 4119) | inrange(`varlist', 4120, 4121) | inrange(`varlist', 4130, 4131) | inrange(`varlist', 4140, 4142) | inrange(`varlist', 4150, 4151) | inrange(`varlist', 4170, 4173) | inrange(`varlist', 4190, 4199) | inrange(`varlist', 4200, 4200) | inrange(`varlist', 4210, 4219) | inrange(`varlist', 4220, 4229) | inrange(`varlist', 4230, 4231) | inrange(`varlist', 4400, 4499) | inrange(`varlist', 4500, 4599) | inrange(`varlist', 4600, 4699) | inrange(`varlist', 4700, 4700) | inrange(`varlist', 4710, 4712) | inrange(`varlist', 4720, 4729) | inrange(`varlist', 4730, 4739) | inrange(`varlist', 4740, 4742) | inrange(`varlist', 4780, 4780) | inrange(`varlist', 4783, 4783) | inrange(`varlist', 4785, 4785) | inrange(`varlist', 4789, 4789)
		
		qui replace `generate' = 14 if inrange(`varlist', 4900, 4900) | inrange(`varlist', 4910, 4911) | inrange(`varlist', 4920, 4922) | inrange(`varlist', 4923, 4923) | inrange(`varlist', 4924, 4925) | inrange(`varlist', 4930, 4931) | inrange(`varlist', 4932, 4932) | inrange(`varlist', 4939, 4939) | inrange(`varlist', 4940, 4942)
		
		qui replace `generate' = 15 if inrange(`varlist', 5260, 5261) | inrange(`varlist', 5270, 5271) | inrange(`varlist', 5300, 5300) | inrange(`varlist', 5310, 5311) | inrange(`varlist', 5320, 5320) | inrange(`varlist', 5330, 5331) | inrange(`varlist', 5334, 5334) | inrange(`varlist', 5390, 5399) | inrange(`varlist', 5400, 5400) | inrange(`varlist', 5410, 5411) | inrange(`varlist', 5412, 5412) | inrange(`varlist', 5420, 5421) | inrange(`varlist', 5430, 5431) | inrange(`varlist', 5440, 5441) | inrange(`varlist', 5450, 5451) | inrange(`varlist', 5460, 5461) | inrange(`varlist', 5490, 5499) | inrange(`varlist', 5540, 5541) | inrange(`varlist', 5550, 5551) | inrange(`varlist', 5600, 5699) | inrange(`varlist', 5700, 5700) | inrange(`varlist', 5710, 5719) | inrange(`varlist', 5720, 5722) | inrange(`varlist', 5730, 5733) | inrange(`varlist', 5734, 5734) | inrange(`varlist', 5735, 5735) | inrange(`varlist', 5736, 5736) | inrange(`varlist', 5750, 5750) | inrange(`varlist', 5800, 5813) | inrange(`varlist', 5890, 5890) | inrange(`varlist', 5900, 5900) | inrange(`varlist', 5910, 5912) | inrange(`varlist', 5920, 5921) | inrange(`varlist', 5930, 5932) | inrange(`varlist', 5940, 5940) | inrange(`varlist', 5941, 5941) | inrange(`varlist', 5942, 5942) | inrange(`varlist', 5943, 5943) | inrange(`varlist', 5944, 5944) | inrange(`varlist', 5945, 5945) | inrange(`varlist', 5946, 5946) | inrange(`varlist', 5947, 5947) | inrange(`varlist', 5948, 5948) | inrange(`varlist', 5949, 5949) | inrange(`varlist', 5960, 5963) | inrange(`varlist', 5980, 5989) | inrange(`varlist', 5990, 5990) | inrange(`varlist', 5992, 5992) | inrange(`varlist', 5993, 5993) | inrange(`varlist', 5994, 5994) | inrange(`varlist', 5995, 5995) | inrange(`varlist', 5999, 5999)
		
		qui replace `generate' = 16 if inrange(`varlist', 6010, 6019) | inrange(`varlist', 6020, 6020) | inrange(`varlist', 6021, 6021) | inrange(`varlist', 6022, 6022) | inrange(`varlist', 6023, 6023) | inrange(`varlist', 6025, 6025) | inrange(`varlist', 6026, 6026) | inrange(`varlist', 6028, 6029) | inrange(`varlist', 6030, 6036) | inrange(`varlist', 6040, 6049) | inrange(`varlist', 6050, 6059) | inrange(`varlist', 6060, 6062) | inrange(`varlist', 6080, 6082) | inrange(`varlist', 6090, 6099) | inrange(`varlist', 6100, 6100) | inrange(`varlist', 6110, 6111) | inrange(`varlist', 6112, 6112) | inrange(`varlist', 6120, 6129) | inrange(`varlist', 6140, 6149) | inrange(`varlist', 6150, 6159) | inrange(`varlist', 6160, 6163) | inrange(`varlist', 6172, 6172) | inrange(`varlist', 6199, 6199) | inrange(`varlist', 6200, 6299) | inrange(`varlist', 6300, 6300) | inrange(`varlist', 6310, 6312) | inrange(`varlist', 6320, 6324) | inrange(`varlist', 6330, 6331) | inrange(`varlist', 6350, 6351) | inrange(`varlist', 6360, 6361) | inrange(`varlist', 6370, 6371) | inrange(`varlist', 6390, 6399) | inrange(`varlist', 6400, 6411) | inrange(`varlist', 6500, 6500) | inrange(`varlist', 6510, 6510) | inrange(`varlist', 6512, 6512) | inrange(`varlist', 6513, 6513) | inrange(`varlist', 6514, 6514) | inrange(`varlist', 6515, 6515) | inrange(`varlist', 6517, 6519) | inrange(`varlist', 6530, 6531) | inrange(`varlist', 6532, 6532) | inrange(`varlist', 6540, 6541) | inrange(`varlist', 6550, 6553) | inrange(`varlist', 6611, 6611) | inrange(`varlist', 6700, 6700) | inrange(`varlist', 6710, 6719) | inrange(`varlist', 6720, 6722) | inrange(`varlist', 6723, 6723) | inrange(`varlist', 6724, 6724) | inrange(`varlist', 6725, 6725) | inrange(`varlist', 6726, 6726) | inrange(`varlist', 6730, 6733) | inrange(`varlist', 6790, 6790) | inrange(`varlist', 6792, 6792) | inrange(`varlist', 6794, 6794) | inrange(`varlist', 6795, 6795) | inrange(`varlist', 6798, 6798) | inrange(`varlist', 6799, 6799)
		
		qui replace `generate' = 17 if inrange(`varlist', 2520, 2549) | inrange(`varlist', 2600, 2639) | inrange(`varlist', 2640, 2659) | inrange(`varlist', 2661, 2661) | inrange(`varlist', 2670, 2699) | inrange(`varlist', 2700, 2709) | inrange(`varlist', 2710, 2719) | inrange(`varlist', 2720, 2729) | inrange(`varlist', 2730, 2739) | inrange(`varlist', 2740, 2749) | inrange(`varlist', 2750, 2759) | inrange(`varlist', 2760, 2761) | inrange(`varlist', 2770, 2771) | inrange(`varlist', 2780, 2789) | inrange(`varlist', 2790, 2799) | inrange(`varlist', 2835, 2835) | inrange(`varlist', 2836, 2836) | inrange(`varlist', 2990, 2999) | inrange(`varlist', 3000, 3000) | inrange(`varlist', 3010, 3011) | inrange(`varlist', 3041, 3041) | inrange(`varlist', 3050, 3053) | inrange(`varlist', 3160, 3161) | inrange(`varlist', 3170, 3171) | inrange(`varlist', 3172, 3172) | inrange(`varlist', 3190, 3199) | inrange(`varlist', 3220, 3221) | inrange(`varlist', 3229, 3229) | inrange(`varlist', 3230, 3231) | inrange(`varlist', 3260, 3260) | inrange(`varlist', 3262, 3263) | inrange(`varlist', 3269, 3269) | inrange(`varlist', 3295, 3299) | inrange(`varlist', 3537, 3537) | inrange(`varlist', 3640, 3644) | inrange(`varlist', 3645, 3645) | inrange(`varlist', 3646, 3646) | inrange(`varlist', 3647, 3647) | inrange(`varlist', 3648, 3649) | inrange(`varlist', 3660, 3660) | inrange(`varlist', 3661, 3661) | inrange(`varlist', 3662, 3662) | inrange(`varlist', 3663, 3663) | inrange(`varlist', 3664, 3664) | inrange(`varlist', 3665, 3665) | inrange(`varlist', 3666, 3666) | inrange(`varlist', 3669, 3669) | inrange(`varlist', 3840, 3849) | inrange(`varlist', 3850, 3851) | inrange(`varlist', 3991, 3991) | inrange(`varlist', 3993, 3993) | inrange(`varlist', 3995, 3995) | inrange(`varlist', 3996, 3996) | inrange(`varlist', 4810, 4813) | inrange(`varlist', 4820, 4822) | inrange(`varlist', 4830, 4839) | inrange(`varlist', 4840, 4841) | inrange(`varlist', 4890, 4890) | inrange(`varlist', 4891, 4891) | inrange(`varlist', 4892, 4892) | inrange(`varlist', 4899, 4899) | inrange(`varlist', 4950, 4959) | inrange(`varlist', 4960, 4961) | inrange(`varlist', 4970, 4971) | inrange(`varlist', 4991, 4991) | inrange(`varlist', 5040, 5042) | inrange(`varlist', 5043, 5043) | inrange(`varlist', 5044, 5044) | inrange(`varlist', 5045, 5045) | inrange(`varlist', 5046, 5046) | inrange(`varlist', 5047, 5047) | inrange(`varlist', 5048, 5048) | inrange(`varlist', 5049, 5049) | inrange(`varlist', 5082, 5082) | inrange(`varlist', 5083, 5083) | inrange(`varlist', 5084, 5084) | inrange(`varlist', 5085, 5085) | inrange(`varlist', 5086, 5087) | inrange(`varlist', 5088, 5088) | inrange(`varlist', 5090, 5090) | inrange(`varlist', 5091, 5092) | inrange(`varlist', 5093, 5093) | inrange(`varlist', 5100, 5100) | inrange(`varlist', 5110, 5113) | inrange(`varlist', 5199, 5199) | inrange(`varlist', 7000, 7000) | inrange(`varlist', 7010, 7011) | inrange(`varlist', 7020, 7021) | inrange(`varlist', 7030, 7033) | inrange(`varlist', 7040, 7041) | inrange(`varlist', 7200, 7200) | inrange(`varlist', 7210, 7212) | inrange(`varlist', 7213, 7213) | inrange(`varlist', 7215, 7216) | inrange(`varlist', 7217, 7217) | inrange(`varlist', 7218, 7218) | inrange(`varlist', 7219, 7219) | inrange(`varlist', 7220, 7221) | inrange(`varlist', 7230, 7231) | inrange(`varlist', 7240, 7241) | inrange(`varlist', 7250, 7251) | inrange(`varlist', 7260, 7269) | inrange(`varlist', 7290, 7290) | inrange(`varlist', 7291, 7291) | inrange(`varlist', 7299, 7299) | inrange(`varlist', 7300, 7300) | inrange(`varlist', 7310, 7319) | inrange(`varlist', 7320, 7323) | inrange(`varlist', 7330, 7338) | inrange(`varlist', 7340, 7342) | inrange(`varlist', 7349, 7349) | inrange(`varlist', 7350, 7351) | inrange(`varlist', 7352, 7352) | inrange(`varlist', 7353, 7353) | inrange(`varlist', 7359, 7359) | inrange(`varlist', 7360, 7369) | inrange(`varlist', 7370, 7372) | inrange(`varlist', 7373, 7373) | inrange(`varlist', 7374, 7374) | inrange(`varlist', 7375, 7375) | inrange(`varlist', 7376, 7376) | inrange(`varlist', 7377, 7377) | inrange(`varlist', 7378, 7378) | inrange(`varlist', 7379, 7379) | inrange(`varlist', 7380, 7380) | inrange(`varlist', 7381, 7382) | inrange(`varlist', 7383, 7383) | inrange(`varlist', 7384, 7384) | inrange(`varlist', 7385, 7385) | inrange(`varlist', 7389, 7390) | inrange(`varlist', 7391, 7391) | inrange(`varlist', 7392, 7392) | inrange(`varlist', 7393, 7393) | inrange(`varlist', 7394, 7394) | inrange(`varlist', 7395, 7395) | inrange(`varlist', 7397, 7397) | inrange(`varlist', 7399, 7399) | inrange(`varlist', 7500, 7500) | inrange(`varlist', 7510, 7519) | inrange(`varlist', 7520, 7523) | inrange(`varlist', 7530, 7539) | inrange(`varlist', 7540, 7549) | inrange(`varlist', 7600, 7600) | inrange(`varlist', 7620, 7620) | inrange(`varlist', 7622, 7622) | inrange(`varlist', 7623, 7623) | inrange(`varlist', 7629, 7629) | inrange(`varlist', 7630, 7631) | inrange(`varlist', 7640, 7641) | inrange(`varlist', 7690, 7699) | inrange(`varlist', 7800, 7829) | inrange(`varlist', 7830, 7833) | inrange(`varlist', 7840, 7841) | inrange(`varlist', 7900, 7900) | inrange(`varlist', 7910, 7911) | inrange(`varlist', 7920, 7929) | inrange(`varlist', 7930, 7933) | inrange(`varlist', 7940, 7949) | inrange(`varlist', 7980, 7980) | inrange(`varlist', 7990, 7999) | inrange(`varlist', 8000, 8099) | inrange(`varlist', 8100, 8199) | inrange(`varlist', 8200, 8299) | inrange(`varlist', 8300, 8399) | inrange(`varlist', 8400, 8499) | inrange(`varlist', 8600, 8699) | inrange(`varlist', 8700, 8700) | inrange(`varlist', 8710, 8713) | inrange(`varlist', 8720, 8721) | inrange(`varlist', 8730, 8734) | inrange(`varlist', 8740, 8748) | inrange(`varlist', 8800, 8899) | inrange(`varlist', 8900, 8910) | inrange(`varlist', 8911, 8911) | inrange(`varlist', 8920, 8999)
	}



	// Fama French 30 industry
	else if `industry' == 30 {

		// define label
		if "`longlabels'" != "" {
			// the long label
			label define lbl_ff_30 1 "(1) Food Products"
			label define lbl_ff_30 2 "(2) Beer & Liquor", add
			label define lbl_ff_30 3 "(3) Tobacco Products", add
			label define lbl_ff_30 4 "(4) Recreation", add
			label define lbl_ff_30 5 "(5) Printing and Publishing", add
			label define lbl_ff_30 6 "(6) Consumer Goods", add
			label define lbl_ff_30 7 "(7) Apparel", add
			label define lbl_ff_30 8 "(8) Healthcare, Medical Equipment, Pharmaceutical Products", add
			label define lbl_ff_30 9 "(9) Chemicals", add
			label define lbl_ff_30 10 "(10) Textiles", add
			label define lbl_ff_30 11 "(11) Construction and Construction Materials", add
			label define lbl_ff_30 12 "(12) Steel Works Etc", add
			label define lbl_ff_30 13 "(13) Fabricated Products and Machinery", add
			label define lbl_ff_30 14 "(14) Electrical Equipment", add
			label define lbl_ff_30 15 "(15) Automobiles and Trucks", add
			label define lbl_ff_30 16 "(16) Aircraft, ships, and railroad equipment", add
			label define lbl_ff_30 17 "(17) Precious Metals, Non-Metallic, and Industrial Metal Mining", add
			label define lbl_ff_30 18 "(18) Coal", add
			label define lbl_ff_30 19 "(19) Petroleum and Natural Gas", add
			label define lbl_ff_30 20 "(20) Utilities", add
			label define lbl_ff_30 21 "(21) Communication", add
			label define lbl_ff_30 22 "(22) Personal and Business Services", add
			label define lbl_ff_30 23 "(23) Business Equipment", add
			label define lbl_ff_30 24 "(24) Business Supplies and Shipping Containers", add
			label define lbl_ff_30 25 "(25) Transportation", add
			label define lbl_ff_30 26 "(26) Wholesale", add
			label define lbl_ff_30 27 "(27) Retail ", add
			label define lbl_ff_30 28 "(28) Restaurants, Hotels, Motels", add
			label define lbl_ff_30 29 "(29) Banking, Insurance, Real Estate, Trading", add
			label define lbl_ff_30 30 "(30) Everything Else", add
		}
		else {
			// the short label
			label define lbl_ff_30 1 "(1) Food" 2 "(2) Beer" 3 "(3) Smoke" 4 "(4) Games" 5 "(5) Books" 6 "(6) Hshld" 7 "(7) Clths" 8 "(8) Hlth" 9 "(9) Chems" 10 "(10) Txtls" 11 "(11) Cnstr" 12 "(12) Steel" 13 "(13) FabPr" 14 "(14) ElcEq" 15 "(15) Autos" 16 "(16) Carry" 17 "(17) Mines" 18 "(18) Coal" 19 "(19) Oil" 20 "(20) Util" 21 "(21) Telcm" 22 "(22) Servs" 23 "(23) BusEq" 24 "(24) Paper" 25 "(25) Trans" 26 "(26) Whlsl" 27 "(27) Rtail" 28 "(28) Meals" 29 "(29) Fin" 30 "(30) Other"
		}
		label values `generate' lbl_ff_30

		// the actual assignment
		qui replace `generate' = 1 if inrange(`varlist', 0100, 0199) | inrange(`varlist', 0200, 0299) | inrange(`varlist', 0700, 0799) | inrange(`varlist', 0910, 0919) | inrange(`varlist', 2000, 2009) | inrange(`varlist', 2010, 2019) | inrange(`varlist', 2020, 2029) | inrange(`varlist', 2030, 2039) | inrange(`varlist', 2040, 2046) | inrange(`varlist', 2048, 2048) | inrange(`varlist', 2050, 2059) | inrange(`varlist', 2060, 2063) | inrange(`varlist', 2064, 2068) | inrange(`varlist', 2070, 2079) | inrange(`varlist', 2086, 2086) | inrange(`varlist', 2087, 2087) | inrange(`varlist', 2090, 2092) | inrange(`varlist', 2095, 2095) | inrange(`varlist', 2096, 2096) | inrange(`varlist', 2097, 2097) | inrange(`varlist', 2098, 2099)
		
		qui replace `generate' = 2 if inrange(`varlist', 2080, 2080) | inrange(`varlist', 2082, 2082) | inrange(`varlist', 2083, 2083) | inrange(`varlist', 2084, 2084) | inrange(`varlist', 2085, 2085)
		
		qui replace `generate' = 3 if inrange(`varlist', 2100, 2199)
		
		qui replace `generate' = 4 if inrange(`varlist', 0920, 0999) | inrange(`varlist', 3650, 3651) | inrange(`varlist', 3652, 3652) | inrange(`varlist', 3732, 3732) | inrange(`varlist', 3930, 3931) | inrange(`varlist', 3940, 3949) | inrange(`varlist', 7800, 7829) | inrange(`varlist', 7830, 7833) | inrange(`varlist', 7840, 7841) | inrange(`varlist', 7900, 7900) | inrange(`varlist', 7910, 7911) | inrange(`varlist', 7920, 7929) | inrange(`varlist', 7930, 7933) | inrange(`varlist', 7940, 7949) | inrange(`varlist', 7980, 7980) | inrange(`varlist', 7990, 7999)
		
		qui replace `generate' = 5 if inrange(`varlist', 2700, 2709) | inrange(`varlist', 2710, 2719) | inrange(`varlist', 2720, 2729) | inrange(`varlist', 2730, 2739) | inrange(`varlist', 2740, 2749) | inrange(`varlist', 2750, 2759) | inrange(`varlist', 2770, 2771) | inrange(`varlist', 2780, 2789) | inrange(`varlist', 2790, 2799) | inrange(`varlist', 3993, 3993)
		
		qui replace `generate' = 6 if inrange(`varlist', 2047, 2047) | inrange(`varlist', 2391, 2392) | inrange(`varlist', 2510, 2519) | inrange(`varlist', 2590, 2599) | inrange(`varlist', 2840, 2843) | inrange(`varlist', 2844, 2844) | inrange(`varlist', 3160, 3161) | inrange(`varlist', 3170, 3171) | inrange(`varlist', 3172, 3172) | inrange(`varlist', 3190, 3199) | inrange(`varlist', 3229, 3229) | inrange(`varlist', 3260, 3260) | inrange(`varlist', 3262, 3263) | inrange(`varlist', 3269, 3269) | inrange(`varlist', 3230, 3231) | inrange(`varlist', 3630, 3639) | inrange(`varlist', 3750, 3751) | inrange(`varlist', 3800, 3800) | inrange(`varlist', 3860, 3861) | inrange(`varlist', 3870, 3873) | inrange(`varlist', 3910, 3911) | inrange(`varlist', 3914, 3914) | inrange(`varlist', 3915, 3915) | inrange(`varlist', 3960, 3962) | inrange(`varlist', 3991, 3991) | inrange(`varlist', 3995, 3995)
		
		qui replace `generate' = 7 if inrange(`varlist', 2300, 2390) | inrange(`varlist', 3020, 3021) | inrange(`varlist', 3100, 3111) | inrange(`varlist', 3130, 3131) | inrange(`varlist', 3140, 3149) | inrange(`varlist', 3150, 3151) | inrange(`varlist', 3963, 3965)
		
		qui replace `generate' = 8 if inrange(`varlist', 2830, 2830) | inrange(`varlist', 2831, 2831) | inrange(`varlist', 2833, 2833) | inrange(`varlist', 2834, 2834) | inrange(`varlist', 2835, 2835) | inrange(`varlist', 2836, 2836) | inrange(`varlist', 3693, 3693) | inrange(`varlist', 3840, 3849) | inrange(`varlist', 3850, 3851) | inrange(`varlist', 8000, 8099)
		
		qui replace `generate' = 9 if inrange(`varlist', 2800, 2809) | inrange(`varlist', 2810, 2819) | inrange(`varlist', 2820, 2829) | inrange(`varlist', 2850, 2859) | inrange(`varlist', 2860, 2869) | inrange(`varlist', 2870, 2879) | inrange(`varlist', 2890, 2899)
		
		qui replace `generate' = 10 if inrange(`varlist', 2200, 2269) | inrange(`varlist', 2270, 2279) | inrange(`varlist', 2280, 2284) | inrange(`varlist', 2290, 2295) | inrange(`varlist', 2297, 2297) | inrange(`varlist', 2298, 2298) | inrange(`varlist', 2299, 2299) | inrange(`varlist', 2393, 2395) | inrange(`varlist', 2397, 2399)
		
		qui replace `generate' = 11 if inrange(`varlist', 0800, 0899) | inrange(`varlist', 1500, 1511) | inrange(`varlist', 1520, 1529) | inrange(`varlist', 1530, 1539) | inrange(`varlist', 1540, 1549) | inrange(`varlist', 1600, 1699) | inrange(`varlist', 1700, 1799) | inrange(`varlist', 2400, 2439) | inrange(`varlist', 2450, 2459) | inrange(`varlist', 2490, 2499) | inrange(`varlist', 2660, 2661) | inrange(`varlist', 2950, 2952) | inrange(`varlist', 3200, 3200) | inrange(`varlist', 3210, 3211) | inrange(`varlist', 3240, 3241) | inrange(`varlist', 3250, 3259) | inrange(`varlist', 3261, 3261) | inrange(`varlist', 3264, 3264) | inrange(`varlist', 3270, 3275) | inrange(`varlist', 3280, 3281) | inrange(`varlist', 3290, 3293) | inrange(`varlist', 3295, 3299) | inrange(`varlist', 3420, 3429) | inrange(`varlist', 3430, 3433) | inrange(`varlist', 3440, 3441) | inrange(`varlist', 3442, 3442) | inrange(`varlist', 3446, 3446) | inrange(`varlist', 3448, 3448) | inrange(`varlist', 3449, 3449) | inrange(`varlist', 3450, 3451) | inrange(`varlist', 3452, 3452) | inrange(`varlist', 3490, 3499) | inrange(`varlist', 3996, 3996)
		
		qui replace `generate' = 12 if inrange(`varlist', 3300, 3300) | inrange(`varlist', 3310, 3317) | inrange(`varlist', 3320, 3325) | inrange(`varlist', 3330, 3339) | inrange(`varlist', 3340, 3341) | inrange(`varlist', 3350, 3357) | inrange(`varlist', 3360, 3369) | inrange(`varlist', 3370, 3379) | inrange(`varlist', 3390, 3399)
		
		qui replace `generate' = 13 if inrange(`varlist', 3400, 3400) | inrange(`varlist', 3443, 3443) | inrange(`varlist', 3444, 3444) | inrange(`varlist', 3460, 3469) | inrange(`varlist', 3470, 3479) | inrange(`varlist', 3510, 3519) | inrange(`varlist', 3520, 3529) | inrange(`varlist', 3530, 3530) | inrange(`varlist', 3531, 3531) | inrange(`varlist', 3532, 3532) | inrange(`varlist', 3533, 3533) | inrange(`varlist', 3534, 3534) | inrange(`varlist', 3535, 3535) | inrange(`varlist', 3536, 3536) | inrange(`varlist', 3538, 3538) | inrange(`varlist', 3540, 3549) | inrange(`varlist', 3550, 3559) | inrange(`varlist', 3560, 3569) | inrange(`varlist', 3580, 3580) | inrange(`varlist', 3581, 3581) | inrange(`varlist', 3582, 3582) | inrange(`varlist', 3585, 3585) | inrange(`varlist', 3586, 3586) | inrange(`varlist', 3589, 3589) | inrange(`varlist', 3590, 3599)
		
		qui replace `generate' = 14 if inrange(`varlist', 3600, 3600) | inrange(`varlist', 3610, 3613) | inrange(`varlist', 3620, 3621) | inrange(`varlist', 3623, 3629) | inrange(`varlist', 3640, 3644) | inrange(`varlist', 3645, 3645) | inrange(`varlist', 3646, 3646) | inrange(`varlist', 3648, 3649) | inrange(`varlist', 3660, 3660) | inrange(`varlist', 3690, 3690) | inrange(`varlist', 3691, 3692) | inrange(`varlist', 3699, 3699)
		
		qui replace `generate' = 15 if inrange(`varlist', 2296, 2296) | inrange(`varlist', 2396, 2396) | inrange(`varlist', 3010, 3011) | inrange(`varlist', 3537, 3537) | inrange(`varlist', 3647, 3647) | inrange(`varlist', 3694, 3694) | inrange(`varlist', 3700, 3700) | inrange(`varlist', 3710, 3710) | inrange(`varlist', 3711, 3711) | inrange(`varlist', 3713, 3713) | inrange(`varlist', 3714, 3714) | inrange(`varlist', 3715, 3715) | inrange(`varlist', 3716, 3716) | inrange(`varlist', 3792, 3792) | inrange(`varlist', 3790, 3791) | inrange(`varlist', 3799, 3799)
		
		qui replace `generate' = 16 if inrange(`varlist', 3720, 3720) | inrange(`varlist', 3721, 3721) | inrange(`varlist', 3723, 3724) | inrange(`varlist', 3725, 3725) | inrange(`varlist', 3728, 3729) | inrange(`varlist', 3730, 3731) | inrange(`varlist', 3740, 3743)
		
		qui replace `generate' = 17 if inrange(`varlist', 1000, 1009) | inrange(`varlist', 1010, 1019) | inrange(`varlist', 1020, 1029) | inrange(`varlist', 1030, 1039) | inrange(`varlist', 1040, 1049) | inrange(`varlist', 1050, 1059) | inrange(`varlist', 1060, 1069) | inrange(`varlist', 1070, 1079) | inrange(`varlist', 1080, 1089) | inrange(`varlist', 1090, 1099) | inrange(`varlist', 1100, 1119) | inrange(`varlist', 1400, 1499)
		
		qui replace `generate' = 18 if inrange(`varlist', 1200, 1299)
		
		qui replace `generate' = 19 if inrange(`varlist', 1300, 1300) | inrange(`varlist', 1310, 1319) | inrange(`varlist', 1320, 1329) | inrange(`varlist', 1330, 1339) | inrange(`varlist', 1370, 1379) | inrange(`varlist', 1380, 1380) | inrange(`varlist', 1381, 1381) | inrange(`varlist', 1382, 1382) | inrange(`varlist', 1389, 1389) | inrange(`varlist', 2900, 2912) | inrange(`varlist', 2990, 2999)
		
		qui replace `generate' = 20 if inrange(`varlist', 4900, 4900) | inrange(`varlist', 4910, 4911) | inrange(`varlist', 4920, 4922) | inrange(`varlist', 4923, 4923) | inrange(`varlist', 4924, 4925) | inrange(`varlist', 4930, 4931) | inrange(`varlist', 4932, 4932) | inrange(`varlist', 4939, 4939) | inrange(`varlist', 4940, 4942)
		
		qui replace `generate' = 21 if inrange(`varlist', 4800, 4800) | inrange(`varlist', 4810, 4813) | inrange(`varlist', 4820, 4822) | inrange(`varlist', 4830, 4839) | inrange(`varlist', 4840, 4841) | inrange(`varlist', 4880, 4889) | inrange(`varlist', 4890, 4890) | inrange(`varlist', 4891, 4891) | inrange(`varlist', 4892, 4892) | inrange(`varlist', 4899, 4899)
		
		qui replace `generate' = 22 if inrange(`varlist', 7020, 7021) | inrange(`varlist', 7030, 7033) | inrange(`varlist', 7200, 7200) | inrange(`varlist', 7210, 7212) | inrange(`varlist', 7214, 7214) | inrange(`varlist', 7215, 7216) | inrange(`varlist', 7217, 7217) | inrange(`varlist', 7218, 7218) | inrange(`varlist', 7219, 7219) | inrange(`varlist', 7220, 7221) | inrange(`varlist', 7230, 7231) | inrange(`varlist', 7240, 7241) | inrange(`varlist', 7250, 7251) | inrange(`varlist', 7260, 7269) | inrange(`varlist', 7270, 7290) | inrange(`varlist', 7291, 7291) | inrange(`varlist', 7292, 7299) | inrange(`varlist', 7300, 7300) | inrange(`varlist', 7310, 7319) | inrange(`varlist', 7320, 7329) | inrange(`varlist', 7330, 7339) | inrange(`varlist', 7340, 7342) | inrange(`varlist', 7349, 7349) | inrange(`varlist', 7350, 7351) | inrange(`varlist', 7352, 7352) | inrange(`varlist', 7353, 7353) | inrange(`varlist', 7359, 7359) | inrange(`varlist', 7360, 7369) | inrange(`varlist', 7370, 7372) | inrange(`varlist', 7374, 7374) | inrange(`varlist', 7375, 7375) | inrange(`varlist', 7376, 7376) | inrange(`varlist', 7377, 7377) | inrange(`varlist', 7378, 7378) | inrange(`varlist', 7379, 7379) | inrange(`varlist', 7380, 7380) | inrange(`varlist', 7381, 7382) | inrange(`varlist', 7383, 7383) | inrange(`varlist', 7384, 7384) | inrange(`varlist', 7385, 7385) | inrange(`varlist', 7389, 7390) | inrange(`varlist', 7391, 7391) | inrange(`varlist', 7392, 7392) | inrange(`varlist', 7393, 7393) | inrange(`varlist', 7394, 7394) | inrange(`varlist', 7395, 7395) | inrange(`varlist', 7396, 7396) | inrange(`varlist', 7397, 7397) | inrange(`varlist', 7399, 7399) | inrange(`varlist', 7500, 7500) | inrange(`varlist', 7510, 7519) | inrange(`varlist', 7520, 7529) | inrange(`varlist', 7530, 7539) | inrange(`varlist', 7540, 7549) | inrange(`varlist', 7600, 7600) | inrange(`varlist', 7620, 7620) | inrange(`varlist', 7622, 7622) | inrange(`varlist', 7623, 7623) | inrange(`varlist', 7629, 7629) | inrange(`varlist', 7630, 7631) | inrange(`varlist', 7640, 7641) | inrange(`varlist', 7690, 7699) | inrange(`varlist', 8100, 8199) | inrange(`varlist', 8200, 8299) | inrange(`varlist', 8300, 8399) | inrange(`varlist', 8400, 8499) | inrange(`varlist', 8600, 8699) | inrange(`varlist', 8700, 8700) | inrange(`varlist', 8710, 8713) | inrange(`varlist', 8720, 8721) | inrange(`varlist', 8730, 8734) | inrange(`varlist', 8740, 8748) | inrange(`varlist', 8800, 8899) | inrange(`varlist', 8900, 8910) | inrange(`varlist', 8911, 8911) | inrange(`varlist', 8920, 8999)
		
		qui replace `generate' = 23 if inrange(`varlist', 3570, 3579) | inrange(`varlist', 3622, 3622) | inrange(`varlist', 3661, 3661) | inrange(`varlist', 3662, 3662) | inrange(`varlist', 3663, 3663) | inrange(`varlist', 3664, 3664) | inrange(`varlist', 3665, 3665) | inrange(`varlist', 3666, 3666) | inrange(`varlist', 3669, 3669) | inrange(`varlist', 3670, 3679) | inrange(`varlist', 3680, 3680) | inrange(`varlist', 3681, 3681) | inrange(`varlist', 3682, 3682) | inrange(`varlist', 3683, 3683) | inrange(`varlist', 3684, 3684) | inrange(`varlist', 3685, 3685) | inrange(`varlist', 3686, 3686) | inrange(`varlist', 3687, 3687) | inrange(`varlist', 3688, 3688) | inrange(`varlist', 3689, 3689) | inrange(`varlist', 3695, 3695) | inrange(`varlist', 3810, 3810) | inrange(`varlist', 3811, 3811) | inrange(`varlist', 3812, 3812) | inrange(`varlist', 3820, 3820) | inrange(`varlist', 3821, 3821) | inrange(`varlist', 3822, 3822) | inrange(`varlist', 3823, 3823) | inrange(`varlist', 3824, 3824) | inrange(`varlist', 3825, 3825) | inrange(`varlist', 3826, 3826) | inrange(`varlist', 3827, 3827) | inrange(`varlist', 3829, 3829) | inrange(`varlist', 3830, 3839) | inrange(`varlist', 7373, 7373)
		
		qui replace `generate' = 24 if inrange(`varlist', 2440, 2449) | inrange(`varlist', 2520, 2549) | inrange(`varlist', 2600, 2639) | inrange(`varlist', 2640, 2659) | inrange(`varlist', 2670, 2699) | inrange(`varlist', 2760, 2761) | inrange(`varlist', 3220, 3221) | inrange(`varlist', 3410, 3412) | inrange(`varlist', 3950, 3955)
		
		qui replace `generate' = 25 if inrange(`varlist', 4000, 4013) | inrange(`varlist', 4040, 4049) | inrange(`varlist', 4100, 4100) | inrange(`varlist', 4110, 4119) | inrange(`varlist', 4120, 4121) | inrange(`varlist', 4130, 4131) | inrange(`varlist', 4140, 4142) | inrange(`varlist', 4150, 4151) | inrange(`varlist', 4170, 4173) | inrange(`varlist', 4190, 4199) | inrange(`varlist', 4200, 4200) | inrange(`varlist', 4210, 4219) | inrange(`varlist', 4220, 4229) | inrange(`varlist', 4230, 4231) | inrange(`varlist', 4240, 4249) | inrange(`varlist', 4400, 4499) | inrange(`varlist', 4500, 4599) | inrange(`varlist', 4600, 4699) | inrange(`varlist', 4700, 4700) | inrange(`varlist', 4710, 4712) | inrange(`varlist', 4720, 4729) | inrange(`varlist', 4730, 4739) | inrange(`varlist', 4740, 4749) | inrange(`varlist', 4780, 4780) | inrange(`varlist', 4782, 4782) | inrange(`varlist', 4783, 4783) | inrange(`varlist', 4784, 4784) | inrange(`varlist', 4785, 4785) | inrange(`varlist', 4789, 4789)
		
		qui replace `generate' = 26 if inrange(`varlist', 5000, 5000) | inrange(`varlist', 5010, 5015) | inrange(`varlist', 5020, 5023) | inrange(`varlist', 5030, 5039) | inrange(`varlist', 5040, 5042) | inrange(`varlist', 5043, 5043) | inrange(`varlist', 5044, 5044) | inrange(`varlist', 5045, 5045) | inrange(`varlist', 5046, 5046) | inrange(`varlist', 5047, 5047) | inrange(`varlist', 5048, 5048) | inrange(`varlist', 5049, 5049) | inrange(`varlist', 5050, 5059) | inrange(`varlist', 5060, 5060) | inrange(`varlist', 5063, 5063) | inrange(`varlist', 5064, 5064) | inrange(`varlist', 5065, 5065) | inrange(`varlist', 5070, 5078) | inrange(`varlist', 5080, 5080) | inrange(`varlist', 5081, 5081) | inrange(`varlist', 5082, 5082) | inrange(`varlist', 5083, 5083) | inrange(`varlist', 5084, 5084) | inrange(`varlist', 5085, 5085) | inrange(`varlist', 5086, 5087) | inrange(`varlist', 5088, 5088) | inrange(`varlist', 5090, 5090) | inrange(`varlist', 5091, 5092) | inrange(`varlist', 5093, 5093) | inrange(`varlist', 5094, 5094) | inrange(`varlist', 5099, 5099) | inrange(`varlist', 5100, 5100) | inrange(`varlist', 5110, 5113) | inrange(`varlist', 5120, 5122) | inrange(`varlist', 5130, 5139) | inrange(`varlist', 5140, 5149) | inrange(`varlist', 5150, 5159) | inrange(`varlist', 5160, 5169) | inrange(`varlist', 5170, 5172) | inrange(`varlist', 5180, 5182) | inrange(`varlist', 5190, 5199)
		
		qui replace `generate' = 27 if inrange(`varlist', 5200, 5200) | inrange(`varlist', 5210, 5219) | inrange(`varlist', 5220, 5229) | inrange(`varlist', 5230, 5231) | inrange(`varlist', 5250, 5251) | inrange(`varlist', 5260, 5261) | inrange(`varlist', 5270, 5271) | inrange(`varlist', 5300, 5300) | inrange(`varlist', 5310, 5311) | inrange(`varlist', 5320, 5320) | inrange(`varlist', 5330, 5331) | inrange(`varlist', 5334, 5334) | inrange(`varlist', 5340, 5349) | inrange(`varlist', 5390, 5399) | inrange(`varlist', 5400, 5400) | inrange(`varlist', 5410, 5411) | inrange(`varlist', 5412, 5412) | inrange(`varlist', 5420, 5429) | inrange(`varlist', 5430, 5439) | inrange(`varlist', 5440, 5449) | inrange(`varlist', 5450, 5459) | inrange(`varlist', 5460, 5469) | inrange(`varlist', 5490, 5499) | inrange(`varlist', 5500, 5500) | inrange(`varlist', 5510, 5529) | inrange(`varlist', 5530, 5539) | inrange(`varlist', 5540, 5549) | inrange(`varlist', 5550, 5559) | inrange(`varlist', 5560, 5569) | inrange(`varlist', 5570, 5579) | inrange(`varlist', 5590, 5599) | inrange(`varlist', 5600, 5699) | inrange(`varlist', 5700, 5700) | inrange(`varlist', 5710, 5719) | inrange(`varlist', 5720, 5722) | inrange(`varlist', 5730, 5733) | inrange(`varlist', 5734, 5734) | inrange(`varlist', 5735, 5735) | inrange(`varlist', 5736, 5736) | inrange(`varlist', 5750, 5799) | inrange(`varlist', 5900, 5900) | inrange(`varlist', 5910, 5912) | inrange(`varlist', 5920, 5929) | inrange(`varlist', 5930, 5932) | inrange(`varlist', 5940, 5940) | inrange(`varlist', 5941, 5941) | inrange(`varlist', 5942, 5942) | inrange(`varlist', 5943, 5943) | inrange(`varlist', 5944, 5944) | inrange(`varlist', 5945, 5945) | inrange(`varlist', 5946, 5946) | inrange(`varlist', 5947, 5947) | inrange(`varlist', 5948, 5948) | inrange(`varlist', 5949, 5949) | inrange(`varlist', 5950, 5959) | inrange(`varlist', 5960, 5969) | inrange(`varlist', 5970, 5979) | inrange(`varlist', 5980, 5989) | inrange(`varlist', 5990, 5990) | inrange(`varlist', 5992, 5992) | inrange(`varlist', 5993, 5993) | inrange(`varlist', 5994, 5994) | inrange(`varlist', 5995, 5995) | inrange(`varlist', 5999, 5999)
		
		qui replace `generate' = 28 if inrange(`varlist', 5800, 5819) | inrange(`varlist', 5820, 5829) | inrange(`varlist', 5890, 5899) | inrange(`varlist', 7000, 7000) | inrange(`varlist', 7010, 7019) | inrange(`varlist', 7040, 7049) | inrange(`varlist', 7213, 7213)
		
		qui replace `generate' = 29 if inrange(`varlist', 6000, 6000) | inrange(`varlist', 6010, 6019) | inrange(`varlist', 6020, 6020) | inrange(`varlist', 6021, 6021) | inrange(`varlist', 6022, 6022) | inrange(`varlist', 6023, 6024) | inrange(`varlist', 6025, 6025) | inrange(`varlist', 6026, 6026) | inrange(`varlist', 6027, 6027) | inrange(`varlist', 6028, 6029) | inrange(`varlist', 6030, 6036) | inrange(`varlist', 6040, 6059) | inrange(`varlist', 6060, 6062) | inrange(`varlist', 6080, 6082) | inrange(`varlist', 6090, 6099) | inrange(`varlist', 6100, 6100) | inrange(`varlist', 6110, 6111) | inrange(`varlist', 6112, 6113) | inrange(`varlist', 6120, 6129) | inrange(`varlist', 6130, 6139) | inrange(`varlist', 6140, 6149) | inrange(`varlist', 6150, 6159) | inrange(`varlist', 6160, 6169) | inrange(`varlist', 6170, 6179) | inrange(`varlist', 6190, 6199) | inrange(`varlist', 6200, 6299) | inrange(`varlist', 6300, 6300) | inrange(`varlist', 6310, 6319) | inrange(`varlist', 6320, 6329) | inrange(`varlist', 6330, 6331) | inrange(`varlist', 6350, 6351) | inrange(`varlist', 6360, 6361) | inrange(`varlist', 6370, 6379) | inrange(`varlist', 6390, 6399) | inrange(`varlist', 6400, 6411) | inrange(`varlist', 6500, 6500) | inrange(`varlist', 6510, 6510) | inrange(`varlist', 6512, 6512) | inrange(`varlist', 6513, 6513) | inrange(`varlist', 6514, 6514) | inrange(`varlist', 6515, 6515) | inrange(`varlist', 6517, 6519) | inrange(`varlist', 6520, 6529) | inrange(`varlist', 6530, 6531) | inrange(`varlist', 6532, 6532) | inrange(`varlist', 6540, 6541) | inrange(`varlist', 6550, 6553) | inrange(`varlist', 6590, 6599) | inrange(`varlist', 6610, 6611) | inrange(`varlist', 6700, 6700) | inrange(`varlist', 6710, 6719) | inrange(`varlist', 6720, 6722) | inrange(`varlist', 6723, 6723) | inrange(`varlist', 6724, 6724) | inrange(`varlist', 6725, 6725) | inrange(`varlist', 6726, 6726) | inrange(`varlist', 6730, 6733) | inrange(`varlist', 6740, 6779) | inrange(`varlist', 6790, 6791) | inrange(`varlist', 6792, 6792) | inrange(`varlist', 6793, 6793) | inrange(`varlist', 6794, 6794) | inrange(`varlist', 6795, 6795) | inrange(`varlist', 6798, 6798) | inrange(`varlist', 6799, 6799)
		
		qui replace `generate' = 30 if inrange(`varlist', 4950, 4959) | inrange(`varlist', 4960, 4961) | inrange(`varlist', 4970, 4971) | inrange(`varlist', 4990, 4991)
	}



	// Fama French 38 industry
	else if `industry' == 38 {

		// define label
		if "`longlabels'" != "" {
			// the long label
			label define lbl_ff_38 1 "(1) Agriculture, forestry, and fishing"
			label define lbl_ff_38 2 "(2) Mining", add
			label define lbl_ff_38 3 "(3) Oil and Gas Extraction", add
			label define lbl_ff_38 4 "(4) Nonmetallic Minerals Except Fuels", add
			label define lbl_ff_38 5 "(5) Construction", add
			label define lbl_ff_38 6 "(6) Food and Kindred Products", add
			label define lbl_ff_38 7 "(7) Tobacco Products", add
			label define lbl_ff_38 8 "(8) Textile Mill Products", add
			label define lbl_ff_38 9 "(9) Apparel and other Textile Products", add
			label define lbl_ff_38 10 "(10) Lumber and Wood Products", add
			label define lbl_ff_38 11 "(11) Furniture and Fixtures", add
			label define lbl_ff_38 12 "(12) Paper and Allied Products", add
			label define lbl_ff_38 13 "(13) Printing and Publishing", add
			label define lbl_ff_38 14 "(14) Chemicals and Allied Products", add
			label define lbl_ff_38 15 "(15) Petroleum and Coal Products", add
			label define lbl_ff_38 16 "(16) Rubber and Miscellaneous Plastics Products", add
			label define lbl_ff_38 17 "(17) Leather and Leather Products", add
			label define lbl_ff_38 18 "(18) Stone, Clay and Glass Products", add
			label define lbl_ff_38 19 "(19) Primary Metal Industries", add
			label define lbl_ff_38 20 "(20) Fabricated Metal Products", add
			label define lbl_ff_38 21 "(21) Machinery, Except Electrical", add
			label define lbl_ff_38 22 "(22) Electrical and Electronic Equipment", add
			label define lbl_ff_38 23 "(23) Transportation Equipment", add
			label define lbl_ff_38 24 "(24) Instruments and Related Products", add
			label define lbl_ff_38 25 "(25) Miscellaneous Manufacturing Industries", add
			label define lbl_ff_38 26 "(26) Transportation", add
			label define lbl_ff_38 27 "(27) Telephone and Telegraph Communication", add
			label define lbl_ff_38 28 "(28) Radio and Television Broadcasting", add
			label define lbl_ff_38 29 "(29) Electric, Gas, and Water Supply", add
			label define lbl_ff_38 30 "(30) Sanitary Services", add
			label define lbl_ff_38 31 "(31) Steam Supply", add
			label define lbl_ff_38 32 "(32) Irrigation Systems", add
			label define lbl_ff_38 33 "(33) Wholesale", add
			label define lbl_ff_38 34 "(34) Retail Stores", add
			label define lbl_ff_38 35 "(35) Finance, Insurance, and Real Estate", add
			label define lbl_ff_38 36 "(36) Services", add
			label define lbl_ff_38 37 "(37) Public Administration", add
			label define lbl_ff_38 38 "(38) Almost Nothing", add
		}
		else {
			// the short label
			label define lbl_ff_38 1 "(1) Agric" 2 "(2) Mines" 3 "(3) Oil" 4 "(4) Stone" 5 "(5) Cnstr" 6 "(6) Food" 7 "(7) Smoke" 8 "(8) Txtls" 9 "(9) Apprl" 10 "(10) Wood" 11 "(11) Chair" 12 "(12) Paper" 13 "(13) Print" 14 "(14) Chems" 15 "(15) Ptrlm" 16 "(16) Rubbr" 17 "(17) Lethr" 18 "(18) Glass" 19 "(19) Metal" 20 "(20) MtlPr" 21 "(21) Machn" 22 "(22) Elctr" 23 "(23) Cars" 24 "(24) Instr" 25 "(25) Manuf" 26 "(26) Trans" 27 "(27) Phone" 28 "(28) TV" 29 "(29) Utils" 30 "(30) Garbg" 31 "(31) Steam" 32 "(32) Water" 33 "(33) Whlsl" 34 "(34) Rtail" 35 "(35) Money" 36 "(36) Srvc" 37 "(37) Govt" 38 "(38) Other"
		}
		label values `generate' lbl_ff_38

		// the actual assignment
		qui replace `generate' = 1 if inrange(`varlist', 0100, 0999)
		
		qui replace `generate' = 2 if inrange(`varlist', 1000, 1299)
		
		qui replace `generate' = 3 if inrange(`varlist', 1300, 1399)
		
		qui replace `generate' = 4 if inrange(`varlist', 1400, 1499)
		
		qui replace `generate' = 5 if inrange(`varlist', 1500, 1799)
		
		qui replace `generate' = 6 if inrange(`varlist', 2000, 2099)
		
		qui replace `generate' = 7 if inrange(`varlist', 2100, 2199)
		
		qui replace `generate' = 8 if inrange(`varlist', 2200, 2299)
		
		qui replace `generate' = 9 if inrange(`varlist', 2300, 2399)
		
		qui replace `generate' = 10 if inrange(`varlist', 2400, 2499)
		
		qui replace `generate' = 11 if inrange(`varlist', 2500, 2599)
		
		qui replace `generate' = 12 if inrange(`varlist', 2600, 2661)
		
		qui replace `generate' = 13 if inrange(`varlist', 2700, 2799)
		
		qui replace `generate' = 14 if inrange(`varlist', 2800, 2899)
		
		qui replace `generate' = 15 if inrange(`varlist', 2900, 2999)
		
		qui replace `generate' = 16 if inrange(`varlist', 3000, 3099)
		
		qui replace `generate' = 17 if inrange(`varlist', 3100, 3199)
		
		qui replace `generate' = 18 if inrange(`varlist', 3200, 3299)
		
		qui replace `generate' = 19 if inrange(`varlist', 3300, 3399)
		
		qui replace `generate' = 20 if inrange(`varlist', 3400, 3499)
		
		qui replace `generate' = 21 if inrange(`varlist', 3500, 3599)
		
		qui replace `generate' = 22 if inrange(`varlist', 3600, 3699)
		
		qui replace `generate' = 23 if inrange(`varlist', 3700, 3799)
		
		qui replace `generate' = 24 if inrange(`varlist', 3800, 3879)
		
		qui replace `generate' = 25 if inrange(`varlist', 3900, 3999)
		
		qui replace `generate' = 26 if inrange(`varlist', 4000, 4799)
		
		qui replace `generate' = 27 if inrange(`varlist', 4800, 4829)
		
		qui replace `generate' = 28 if inrange(`varlist', 4830, 4899)
		
		qui replace `generate' = 29 if inrange(`varlist', 4900, 4949)
		
		qui replace `generate' = 30 if inrange(`varlist', 4950, 4959)
		
		qui replace `generate' = 31 if inrange(`varlist', 4960, 4969)
		
		qui replace `generate' = 32 if inrange(`varlist', 4970, 4979)
		
		qui replace `generate' = 33 if inrange(`varlist', 5000, 5199)
		
		qui replace `generate' = 34 if inrange(`varlist', 5200, 5999)
		
		qui replace `generate' = 35 if inrange(`varlist', 6000, 6999)
		
		qui replace `generate' = 36 if inrange(`varlist', 7000, 8999)
		
		qui replace `generate' = 37 if inrange(`varlist', 9000, 9999)

		qui replace `generate' = 38 if `generate' == . & inrange(`varlist', 100, 9999)
	}



	// Fama French 48 industry
	else if `industry' == 48 {

		// define label
		if "`longlabels'" != "" {
			// the long label
			label define lbl_ff_48 1 "(1) Agriculture"
			label define lbl_ff_48 2 "(2) Food Products", add
			label define lbl_ff_48 3 "(3) Candy & Soda", add
			label define lbl_ff_48 4 "(4) Beer & Liquor", add
			label define lbl_ff_48 5 "(5) Tobacco Products", add
			label define lbl_ff_48 6 "(6) Recreation", add
			label define lbl_ff_48 7 "(7) Entertainment", add
			label define lbl_ff_48 8 "(8) Printing and Publishing", add
			label define lbl_ff_48 9 "(9) Consumer Goods", add
			label define lbl_ff_48 10 "(10) Apparel", add
			label define lbl_ff_48 11 "(11) Healthcare", add
			label define lbl_ff_48 12 "(12) Medical Equipment", add
			label define lbl_ff_48 13 "(13) Pharmaceutical Products", add
			label define lbl_ff_48 14 "(14) Chemicals", add
			label define lbl_ff_48 15 "(15) Rubber and Plastic Products", add
			label define lbl_ff_48 16 "(16) Textiles", add
			label define lbl_ff_48 17 "(17) Construction Materials", add
			label define lbl_ff_48 18 "(18) Construction", add
			label define lbl_ff_48 19 "(19) Steel Works Etc", add
			label define lbl_ff_48 20 "(20) Fabricated Products", add
			label define lbl_ff_48 21 "(21) Machinery", add
			label define lbl_ff_48 22 "(22) Electrical Equipment", add
			label define lbl_ff_48 23 "(23) Automobiles and Trucks", add
			label define lbl_ff_48 24 "(24) Aircraft", add
			label define lbl_ff_48 25 "(25) Shipbuilding, Railroad Equipment", add
			label define lbl_ff_48 26 "(26) Defense", add
			label define lbl_ff_48 27 "(27) Precious Metals", add
			label define lbl_ff_48 28 "(28) Non-Metallic and Industrial Metal Mining", add
			label define lbl_ff_48 29 "(29) Coal", add
			label define lbl_ff_48 30 "(30) Petroleum and Natural Gas", add
			label define lbl_ff_48 31 "(31) Utilities", add
			label define lbl_ff_48 32 "(32) Communication", add
			label define lbl_ff_48 33 "(33) Personal Services", add
			label define lbl_ff_48 34 "(34) Business Services", add
			label define lbl_ff_48 35 "(35) Computers", add
			label define lbl_ff_48 36 "(36) Electronic Equipment", add
			label define lbl_ff_48 37 "(37) Measuring and Control Equipment", add
			label define lbl_ff_48 38 "(38) Business Supplies", add
			label define lbl_ff_48 39 "(39) Shipping Containers", add
			label define lbl_ff_48 40 "(40) Transportation", add
			label define lbl_ff_48 41 "(41) Wholesale", add
			label define lbl_ff_48 42 "(42) Retail ", add
			label define lbl_ff_48 43 "(43) Restaurants, Hotels, Motels", add
			label define lbl_ff_48 44 "(44) Banking", add
			label define lbl_ff_48 45 "(45) Insurance", add
			label define lbl_ff_48 46 "(46) Real Estate", add
			label define lbl_ff_48 47 "(47) Trading", add
			label define lbl_ff_48 48 "(48) Almost Nothing", add
		}
		else {
			// the short label
			label define lbl_ff_48 1 "(1) Agric" 2 "(2) Food" 3 "(3) Soda" 4 "(4) Beer" 5 "(5) Smoke" 6 "(6) Toys" 7 "(7) Fun" 8 "(8) Books" 9 "(9) Hshld" 10 "(10) Clths" 11 "(11) Hlth" 12 "(12) MedEq" 13 "(13) Drugs" 14 "(14) Chems" 15 "(15) Rubbr" 16 "(16) Txtls" 17 "(17) BldMt" 18 "(18) Cnstr" 19 "(19) Steel" 20 "(20) FabPr" 21 "(21) Mach" 22 "(22) ElcEq" 23 "(23) Autos" 24 "(24) Aero" 25 "(25) Ships" 26 "(26) Guns" 27 "(27) Gold" 28 "(28) Mines" 29 "(29) Coal" 30 "(30) Oil" 31 "(31) Util" 32 "(32) Telcm" 33 "(33) PerSv" 34 "(34) BusSv" 35 "(35) Comps" 36 "(36) Chips" 37 "(37) LabEq" 38 "(38) Paper" 39 "(39) Boxes" 40 "(40) Trans" 41 "(41) Whlsl" 42 "(42) Rtail" 43 "(43) Meals" 44 "(44) Banks" 45 "(45) Insur" 46 "(46) RlEst" 47 "(47) Fin" 48 "(48) Other"
		}
		label values `generate' lbl_ff_48

		// the actual assignment
		qui replace `generate' = 1 if inrange(`varlist', 0100, 0199) | inrange(`varlist', 0200, 0299) | inrange(`varlist', 0700, 0799) | inrange(`varlist', 0910, 0919) | inrange(`varlist', 2048, 2048)
		
		qui replace `generate' = 2 if inrange(`varlist', 2000, 2009) | inrange(`varlist', 2010, 2019) | inrange(`varlist', 2020, 2029) | inrange(`varlist', 2030, 2039) | inrange(`varlist', 2040, 2046) | inrange(`varlist', 2050, 2059) | inrange(`varlist', 2060, 2063) | inrange(`varlist', 2070, 2079) | inrange(`varlist', 2090, 2092) | inrange(`varlist', 2095, 2095) | inrange(`varlist', 2098, 2099)
		
		qui replace `generate' = 3 if inrange(`varlist', 2064, 2068) | inrange(`varlist', 2086, 2086) | inrange(`varlist', 2087, 2087) | inrange(`varlist', 2096, 2096) | inrange(`varlist', 2097, 2097)
		
		qui replace `generate' = 4 if inrange(`varlist', 2080, 2080) | inrange(`varlist', 2082, 2082) | inrange(`varlist', 2083, 2083) | inrange(`varlist', 2084, 2084) | inrange(`varlist', 2085, 2085)
		
		qui replace `generate' = 5 if inrange(`varlist', 2100, 2199)
		
		qui replace `generate' = 6 if inrange(`varlist', 0920, 0999) | inrange(`varlist', 3650, 3651) | inrange(`varlist', 3652, 3652) | inrange(`varlist', 3732, 3732) | inrange(`varlist', 3930, 3931) | inrange(`varlist', 3940, 3949)
		
		qui replace `generate' = 7 if inrange(`varlist', 7800, 7829) | inrange(`varlist', 7830, 7833) | inrange(`varlist', 7840, 7841) | inrange(`varlist', 7900, 7900) | inrange(`varlist', 7910, 7911) | inrange(`varlist', 7920, 7929) | inrange(`varlist', 7930, 7933) | inrange(`varlist', 7940, 7949) | inrange(`varlist', 7980, 7980) | inrange(`varlist', 7990, 7999)
		
		qui replace `generate' = 8 if inrange(`varlist', 2700, 2709) | inrange(`varlist', 2710, 2719) | inrange(`varlist', 2720, 2729) | inrange(`varlist', 2730, 2739) | inrange(`varlist', 2740, 2749) | inrange(`varlist', 2770, 2771) | inrange(`varlist', 2780, 2789) | inrange(`varlist', 2790, 2799)
		
		qui replace `generate' = 9 if inrange(`varlist', 2047, 2047) | inrange(`varlist', 2391, 2392) | inrange(`varlist', 2510, 2519) | inrange(`varlist', 2590, 2599) | inrange(`varlist', 2840, 2843) | inrange(`varlist', 2844, 2844) | inrange(`varlist', 3160, 3161) | inrange(`varlist', 3170, 3171) | inrange(`varlist', 3172, 3172) | inrange(`varlist', 3190, 3199) | inrange(`varlist', 3229, 3229) | inrange(`varlist', 3260, 3260) | inrange(`varlist', 3262, 3263) | inrange(`varlist', 3269, 3269) | inrange(`varlist', 3230, 3231) | inrange(`varlist', 3630, 3639) | inrange(`varlist', 3750, 3751) | inrange(`varlist', 3800, 3800) | inrange(`varlist', 3860, 3861) | inrange(`varlist', 3870, 3873) | inrange(`varlist', 3910, 3911) | inrange(`varlist', 3914, 3914) | inrange(`varlist', 3915, 3915) | inrange(`varlist', 3960, 3962) | inrange(`varlist', 3991, 3991) | inrange(`varlist', 3995, 3995)
		
		qui replace `generate' = 10 if inrange(`varlist', 2300, 2390) | inrange(`varlist', 3020, 3021) | inrange(`varlist', 3100, 3111) | inrange(`varlist', 3130, 3131) | inrange(`varlist', 3140, 3149) | inrange(`varlist', 3150, 3151) | inrange(`varlist', 3963, 3965)
		
		qui replace `generate' = 11 if inrange(`varlist', 8000, 8099)
		
		qui replace `generate' = 12 if inrange(`varlist', 3693, 3693) | inrange(`varlist', 3840, 3849) | inrange(`varlist', 3850, 3851)
		
		qui replace `generate' = 13 if inrange(`varlist', 2830, 2830) | inrange(`varlist', 2831, 2831) | inrange(`varlist', 2833, 2833) | inrange(`varlist', 2834, 2834) | inrange(`varlist', 2835, 2835) | inrange(`varlist', 2836, 2836)
		
		qui replace `generate' = 14 if inrange(`varlist', 2800, 2809) | inrange(`varlist', 2810, 2819) | inrange(`varlist', 2820, 2829) | inrange(`varlist', 2850, 2859) | inrange(`varlist', 2860, 2869) | inrange(`varlist', 2870, 2879) | inrange(`varlist', 2890, 2899)
		
		qui replace `generate' = 15 if inrange(`varlist', 3031, 3031) | inrange(`varlist', 3041, 3041) | inrange(`varlist', 3050, 3053) | inrange(`varlist', 3060, 3069) | inrange(`varlist', 3070, 3079) | inrange(`varlist', 3080, 3089) | inrange(`varlist', 3090, 3099)
		
		qui replace `generate' = 16 if inrange(`varlist', 2200, 2269) | inrange(`varlist', 2270, 2279) | inrange(`varlist', 2280, 2284) | inrange(`varlist', 2290, 2295) | inrange(`varlist', 2297, 2297) | inrange(`varlist', 2298, 2298) | inrange(`varlist', 2299, 2299) | inrange(`varlist', 2393, 2395) | inrange(`varlist', 2397, 2399)
		
		qui replace `generate' = 17 if inrange(`varlist', 0800, 0899) | inrange(`varlist', 2400, 2439) | inrange(`varlist', 2450, 2459) | inrange(`varlist', 2490, 2499) | inrange(`varlist', 2660, 2661) | inrange(`varlist', 2950, 2952) | inrange(`varlist', 3200, 3200) | inrange(`varlist', 3210, 3211) | inrange(`varlist', 3240, 3241) | inrange(`varlist', 3250, 3259) | inrange(`varlist', 3261, 3261) | inrange(`varlist', 3264, 3264) | inrange(`varlist', 3270, 3275) | inrange(`varlist', 3280, 3281) | inrange(`varlist', 3290, 3293) | inrange(`varlist', 3295, 3299) | inrange(`varlist', 3420, 3429) | inrange(`varlist', 3430, 3433) | inrange(`varlist', 3440, 3441) | inrange(`varlist', 3442, 3442) | inrange(`varlist', 3446, 3446) | inrange(`varlist', 3448, 3448) | inrange(`varlist', 3449, 3449) | inrange(`varlist', 3450, 3451) | inrange(`varlist', 3452, 3452) | inrange(`varlist', 3490, 3499) | inrange(`varlist', 3996, 3996)
		
		qui replace `generate' = 18 if inrange(`varlist', 1500, 1511) | inrange(`varlist', 1520, 1529) | inrange(`varlist', 1530, 1539) | inrange(`varlist', 1540, 1549) | inrange(`varlist', 1600, 1699) | inrange(`varlist', 1700, 1799)
		
		qui replace `generate' = 19 if inrange(`varlist', 3300, 3300) | inrange(`varlist', 3310, 3317) | inrange(`varlist', 3320, 3325) | inrange(`varlist', 3330, 3339) | inrange(`varlist', 3340, 3341) | inrange(`varlist', 3350, 3357) | inrange(`varlist', 3360, 3369) | inrange(`varlist', 3370, 3379) | inrange(`varlist', 3390, 3399)
		
		qui replace `generate' = 20 if inrange(`varlist', 3400, 3400) | inrange(`varlist', 3443, 3443) | inrange(`varlist', 3444, 3444) | inrange(`varlist', 3460, 3469) | inrange(`varlist', 3470, 3479)
		
		qui replace `generate' = 21 if inrange(`varlist', 3510, 3519) | inrange(`varlist', 3520, 3529) | inrange(`varlist', 3530, 3530) | inrange(`varlist', 3531, 3531) | inrange(`varlist', 3532, 3532) | inrange(`varlist', 3533, 3533) | inrange(`varlist', 3534, 3534) | inrange(`varlist', 3535, 3535) | inrange(`varlist', 3536, 3536) | inrange(`varlist', 3538, 3538) | inrange(`varlist', 3540, 3549) | inrange(`varlist', 3550, 3559) | inrange(`varlist', 3560, 3569) | inrange(`varlist', 3580, 3580) | inrange(`varlist', 3581, 3581) | inrange(`varlist', 3582, 3582) | inrange(`varlist', 3585, 3585) | inrange(`varlist', 3586, 3586) | inrange(`varlist', 3589, 3589) | inrange(`varlist', 3590, 3599)
		
		qui replace `generate' = 22 if inrange(`varlist', 3600, 3600) | inrange(`varlist', 3610, 3613) | inrange(`varlist', 3620, 3621) | inrange(`varlist', 3623, 3629) | inrange(`varlist', 3640, 3644) | inrange(`varlist', 3645, 3645) | inrange(`varlist', 3646, 3646) | inrange(`varlist', 3648, 3649) | inrange(`varlist', 3660, 3660) | inrange(`varlist', 3690, 3690) | inrange(`varlist', 3691, 3692) | inrange(`varlist', 3699, 3699)
		
		qui replace `generate' = 23 if inrange(`varlist', 2296, 2296) | inrange(`varlist', 2396, 2396) | inrange(`varlist', 3010, 3011) | inrange(`varlist', 3537, 3537) | inrange(`varlist', 3647, 3647) | inrange(`varlist', 3694, 3694) | inrange(`varlist', 3700, 3700) | inrange(`varlist', 3710, 3710) | inrange(`varlist', 3711, 3711) | inrange(`varlist', 3713, 3713) | inrange(`varlist', 3714, 3714) | inrange(`varlist', 3715, 3715) | inrange(`varlist', 3716, 3716) | inrange(`varlist', 3792, 3792) | inrange(`varlist', 3790, 3791) | inrange(`varlist', 3799, 3799)
		
		qui replace `generate' = 24 if inrange(`varlist', 3720, 3720) | inrange(`varlist', 3721, 3721) | inrange(`varlist', 3723, 3724) | inrange(`varlist', 3725, 3725) | inrange(`varlist', 3728, 3729)
		
		qui replace `generate' = 25 if inrange(`varlist', 3730, 3731) | inrange(`varlist', 3740, 3743)
		
		qui replace `generate' = 26 if inrange(`varlist', 3760, 3769) | inrange(`varlist', 3795, 3795) | inrange(`varlist', 3480, 3489)
		
		qui replace `generate' = 27 if inrange(`varlist', 1040, 1049)
		
		qui replace `generate' = 28 if inrange(`varlist', 1000, 1009) | inrange(`varlist', 1010, 1019) | inrange(`varlist', 1020, 1029) | inrange(`varlist', 1030, 1039) | inrange(`varlist', 1050, 1059) | inrange(`varlist', 1060, 1069) | inrange(`varlist', 1070, 1079) | inrange(`varlist', 1080, 1089) | inrange(`varlist', 1090, 1099) | inrange(`varlist', 1100, 1119) | inrange(`varlist', 1400, 1499)
		
		qui replace `generate' = 29 if inrange(`varlist', 1200, 1299)
		
		qui replace `generate' = 30 if inrange(`varlist', 1300, 1300) | inrange(`varlist', 1310, 1319) | inrange(`varlist', 1320, 1329) | inrange(`varlist', 1330, 1339) | inrange(`varlist', 1370, 1379) | inrange(`varlist', 1380, 1380) | inrange(`varlist', 1381, 1381) | inrange(`varlist', 1382, 1382) | inrange(`varlist', 1389, 1389) | inrange(`varlist', 2900, 2912) | inrange(`varlist', 2990, 2999)
		
		qui replace `generate' = 31 if inrange(`varlist', 4900, 4900) | inrange(`varlist', 4910, 4911) | inrange(`varlist', 4920, 4922) | inrange(`varlist', 4923, 4923) | inrange(`varlist', 4924, 4925) | inrange(`varlist', 4930, 4931) | inrange(`varlist', 4932, 4932) | inrange(`varlist', 4939, 4939) | inrange(`varlist', 4940, 4942)
		
		qui replace `generate' = 32 if inrange(`varlist', 4800, 4800) | inrange(`varlist', 4810, 4813) | inrange(`varlist', 4820, 4822) | inrange(`varlist', 4830, 4839) | inrange(`varlist', 4840, 4841) | inrange(`varlist', 4880, 4889) | inrange(`varlist', 4890, 4890) | inrange(`varlist', 4891, 4891) | inrange(`varlist', 4892, 4892) | inrange(`varlist', 4899, 4899)
		
		qui replace `generate' = 33 if inrange(`varlist', 7020, 7021) | inrange(`varlist', 7030, 7033) | inrange(`varlist', 7200, 7200) | inrange(`varlist', 7210, 7212) | inrange(`varlist', 7214, 7214) | inrange(`varlist', 7215, 7216) | inrange(`varlist', 7217, 7217) | inrange(`varlist', 7219, 7219) | inrange(`varlist', 7220, 7221) | inrange(`varlist', 7230, 7231) | inrange(`varlist', 7240, 7241) | inrange(`varlist', 7250, 7251) | inrange(`varlist', 7260, 7269) | inrange(`varlist', 7270, 7290) | inrange(`varlist', 7291, 7291) | inrange(`varlist', 7292, 7299) | inrange(`varlist', 7395, 7395) | inrange(`varlist', 7500, 7500) | inrange(`varlist', 7520, 7529) | inrange(`varlist', 7530, 7539) | inrange(`varlist', 7540, 7549) | inrange(`varlist', 7600, 7600) | inrange(`varlist', 7620, 7620) | inrange(`varlist', 7622, 7622) | inrange(`varlist', 7623, 7623) | inrange(`varlist', 7629, 7629) | inrange(`varlist', 7630, 7631) | inrange(`varlist', 7640, 7641) | inrange(`varlist', 7690, 7699) | inrange(`varlist', 8100, 8199) | inrange(`varlist', 8200, 8299) | inrange(`varlist', 8300, 8399) | inrange(`varlist', 8400, 8499) | inrange(`varlist', 8600, 8699) | inrange(`varlist', 8800, 8899) | inrange(`varlist', 7510, 7515)
		
		qui replace `generate' = 34 if inrange(`varlist', 2750, 2759) | inrange(`varlist', 3993, 3993) | inrange(`varlist', 7218, 7218) | inrange(`varlist', 7300, 7300) | inrange(`varlist', 7310, 7319) | inrange(`varlist', 7320, 7329) | inrange(`varlist', 7330, 7339) | inrange(`varlist', 7340, 7342) | inrange(`varlist', 7349, 7349) | inrange(`varlist', 7350, 7351) | inrange(`varlist', 7352, 7352) | inrange(`varlist', 7353, 7353) | inrange(`varlist', 7359, 7359) | inrange(`varlist', 7360, 7369) | inrange(`varlist', 7370, 7372) | inrange(`varlist', 7374, 7374) | inrange(`varlist', 7375, 7375) | inrange(`varlist', 7376, 7376) | inrange(`varlist', 7377, 7377) | inrange(`varlist', 7378, 7378) | inrange(`varlist', 7379, 7379) | inrange(`varlist', 7380, 7380) | inrange(`varlist', 7381, 7382) | inrange(`varlist', 7383, 7383) | inrange(`varlist', 7384, 7384) | inrange(`varlist', 7385, 7385) | inrange(`varlist', 7389, 7390) | inrange(`varlist', 7391, 7391) | inrange(`varlist', 7392, 7392) | inrange(`varlist', 7393, 7393) | inrange(`varlist', 7394, 7394) | inrange(`varlist', 7396, 7396) | inrange(`varlist', 7397, 7397) | inrange(`varlist', 7399, 7399) | inrange(`varlist', 7519, 7519) | inrange(`varlist', 8700, 8700) | inrange(`varlist', 8710, 8713) | inrange(`varlist', 8720, 8721) | inrange(`varlist', 8730, 8734) | inrange(`varlist', 8740, 8748) | inrange(`varlist', 8900, 8910) | inrange(`varlist', 8911, 8911) | inrange(`varlist', 8920, 8999) | inrange(`varlist', 4220, 4229)
		
		qui replace `generate' = 35 if inrange(`varlist', 3570, 3579) | inrange(`varlist', 3680, 3680) | inrange(`varlist', 3681, 3681) | inrange(`varlist', 3682, 3682) | inrange(`varlist', 3683, 3683) | inrange(`varlist', 3684, 3684) | inrange(`varlist', 3685, 3685) | inrange(`varlist', 3686, 3686) | inrange(`varlist', 3687, 3687) | inrange(`varlist', 3688, 3688) | inrange(`varlist', 3689, 3689) | inrange(`varlist', 3695, 3695) | inrange(`varlist', 7373, 7373)
		
		qui replace `generate' = 36 if inrange(`varlist', 3622, 3622) | inrange(`varlist', 3661, 3661) | inrange(`varlist', 3662, 3662) | inrange(`varlist', 3663, 3663) | inrange(`varlist', 3664, 3664) | inrange(`varlist', 3665, 3665) | inrange(`varlist', 3666, 3666) | inrange(`varlist', 3669, 3669) | inrange(`varlist', 3670, 3679) | inrange(`varlist', 3810, 3810) | inrange(`varlist', 3812, 3812)
		
		qui replace `generate' = 37 if inrange(`varlist', 3811, 3811) | inrange(`varlist', 3820, 3820) | inrange(`varlist', 3821, 3821) | inrange(`varlist', 3822, 3822) | inrange(`varlist', 3823, 3823) | inrange(`varlist', 3824, 3824) | inrange(`varlist', 3825, 3825) | inrange(`varlist', 3826, 3826) | inrange(`varlist', 3827, 3827) | inrange(`varlist', 3829, 3829) | inrange(`varlist', 3830, 3839)
		
		qui replace `generate' = 38 if inrange(`varlist', 2520, 2549) | inrange(`varlist', 2600, 2639) | inrange(`varlist', 2670, 2699) | inrange(`varlist', 2760, 2761) | inrange(`varlist', 3950, 3955)
		
		qui replace `generate' = 39 if inrange(`varlist', 2440, 2449) | inrange(`varlist', 2640, 2659) | inrange(`varlist', 3220, 3221) | inrange(`varlist', 3410, 3412)
		
		qui replace `generate' = 40 if inrange(`varlist', 4000, 4013) | inrange(`varlist', 4040, 4049) | inrange(`varlist', 4100, 4100) | inrange(`varlist', 4110, 4119) | inrange(`varlist', 4120, 4121) | inrange(`varlist', 4130, 4131) | inrange(`varlist', 4140, 4142) | inrange(`varlist', 4150, 4151) | inrange(`varlist', 4170, 4173) | inrange(`varlist', 4190, 4199) | inrange(`varlist', 4200, 4200) | inrange(`varlist', 4210, 4219) | inrange(`varlist', 4230, 4231) | inrange(`varlist', 4240, 4249) | inrange(`varlist', 4400, 4499) | inrange(`varlist', 4500, 4599) | inrange(`varlist', 4600, 4699) | inrange(`varlist', 4700, 4700) | inrange(`varlist', 4710, 4712) | inrange(`varlist', 4720, 4729) | inrange(`varlist', 4730, 4739) | inrange(`varlist', 4740, 4749) | inrange(`varlist', 4780, 4780) | inrange(`varlist', 4782, 4782) | inrange(`varlist', 4783, 4783) | inrange(`varlist', 4784, 4784) | inrange(`varlist', 4785, 4785) | inrange(`varlist', 4789, 4789)
		
		qui replace `generate' = 41 if inrange(`varlist', 5000, 5000) | inrange(`varlist', 5010, 5015) | inrange(`varlist', 5020, 5023) | inrange(`varlist', 5030, 5039) | inrange(`varlist', 5040, 5042) | inrange(`varlist', 5043, 5043) | inrange(`varlist', 5044, 5044) | inrange(`varlist', 5045, 5045) | inrange(`varlist', 5046, 5046) | inrange(`varlist', 5047, 5047) | inrange(`varlist', 5048, 5048) | inrange(`varlist', 5049, 5049) | inrange(`varlist', 5050, 5059) | inrange(`varlist', 5060, 5060) | inrange(`varlist', 5063, 5063) | inrange(`varlist', 5064, 5064) | inrange(`varlist', 5065, 5065) | inrange(`varlist', 5070, 5078) | inrange(`varlist', 5080, 5080) | inrange(`varlist', 5081, 5081) | inrange(`varlist', 5082, 5082) | inrange(`varlist', 5083, 5083) | inrange(`varlist', 5084, 5084) | inrange(`varlist', 5085, 5085) | inrange(`varlist', 5086, 5087) | inrange(`varlist', 5088, 5088) | inrange(`varlist', 5090, 5090) | inrange(`varlist', 5091, 5092) | inrange(`varlist', 5093, 5093) | inrange(`varlist', 5094, 5094) | inrange(`varlist', 5099, 5099) | inrange(`varlist', 5100, 5100) | inrange(`varlist', 5110, 5113) | inrange(`varlist', 5120, 5122) | inrange(`varlist', 5130, 5139) | inrange(`varlist', 5140, 5149) | inrange(`varlist', 5150, 5159) | inrange(`varlist', 5160, 5169) | inrange(`varlist', 5170, 5172) | inrange(`varlist', 5180, 5182) | inrange(`varlist', 5190, 5199)
		
		qui replace `generate' = 42 if inrange(`varlist', 5200, 5200) | inrange(`varlist', 5210, 5219) | inrange(`varlist', 5220, 5229) | inrange(`varlist', 5230, 5231) | inrange(`varlist', 5250, 5251) | inrange(`varlist', 5260, 5261) | inrange(`varlist', 5270, 5271) | inrange(`varlist', 5300, 5300) | inrange(`varlist', 5310, 5311) | inrange(`varlist', 5320, 5320) | inrange(`varlist', 5330, 5331) | inrange(`varlist', 5334, 5334) | inrange(`varlist', 5340, 5349) | inrange(`varlist', 5390, 5399) | inrange(`varlist', 5400, 5400) | inrange(`varlist', 5410, 5411) | inrange(`varlist', 5412, 5412) | inrange(`varlist', 5420, 5429) | inrange(`varlist', 5430, 5439) | inrange(`varlist', 5440, 5449) | inrange(`varlist', 5450, 5459) | inrange(`varlist', 5460, 5469) | inrange(`varlist', 5490, 5499) | inrange(`varlist', 5500, 5500) | inrange(`varlist', 5510, 5529) | inrange(`varlist', 5530, 5539) | inrange(`varlist', 5540, 5549) | inrange(`varlist', 5550, 5559) | inrange(`varlist', 5560, 5569) | inrange(`varlist', 5570, 5579) | inrange(`varlist', 5590, 5599) | inrange(`varlist', 5600, 5699) | inrange(`varlist', 5700, 5700) | inrange(`varlist', 5710, 5719) | inrange(`varlist', 5720, 5722) | inrange(`varlist', 5730, 5733) | inrange(`varlist', 5734, 5734) | inrange(`varlist', 5735, 5735) | inrange(`varlist', 5736, 5736) | inrange(`varlist', 5750, 5799) | inrange(`varlist', 5900, 5900) | inrange(`varlist', 5910, 5912) | inrange(`varlist', 5920, 5929) | inrange(`varlist', 5930, 5932) | inrange(`varlist', 5940, 5940) | inrange(`varlist', 5941, 5941) | inrange(`varlist', 5942, 5942) | inrange(`varlist', 5943, 5943) | inrange(`varlist', 5944, 5944) | inrange(`varlist', 5945, 5945) | inrange(`varlist', 5946, 5946) | inrange(`varlist', 5947, 5947) | inrange(`varlist', 5948, 5948) | inrange(`varlist', 5949, 5949) | inrange(`varlist', 5950, 5959) | inrange(`varlist', 5960, 5969) | inrange(`varlist', 5970, 5979) | inrange(`varlist', 5980, 5989) | inrange(`varlist', 5990, 5990) | inrange(`varlist', 5992, 5992) | inrange(`varlist', 5993, 5993) | inrange(`varlist', 5994, 5994) | inrange(`varlist', 5995, 5995) | inrange(`varlist', 5999, 5999)
		
		qui replace `generate' = 43 if inrange(`varlist', 5800, 5819) | inrange(`varlist', 5820, 5829) | inrange(`varlist', 5890, 5899) | inrange(`varlist', 7000, 7000) | inrange(`varlist', 7010, 7019) | inrange(`varlist', 7040, 7049) | inrange(`varlist', 7213, 7213)
		
		qui replace `generate' = 44 if inrange(`varlist', 6000, 6000) | inrange(`varlist', 6010, 6019) | inrange(`varlist', 6020, 6020) | inrange(`varlist', 6021, 6021) | inrange(`varlist', 6022, 6022) | inrange(`varlist', 6023, 6024) | inrange(`varlist', 6025, 6025) | inrange(`varlist', 6026, 6026) | inrange(`varlist', 6027, 6027) | inrange(`varlist', 6028, 6029) | inrange(`varlist', 6030, 6036) | inrange(`varlist', 6040, 6059) | inrange(`varlist', 6060, 6062) | inrange(`varlist', 6080, 6082) | inrange(`varlist', 6090, 6099) | inrange(`varlist', 6100, 6100) | inrange(`varlist', 6110, 6111) | inrange(`varlist', 6112, 6113) | inrange(`varlist', 6120, 6129) | inrange(`varlist', 6130, 6139) | inrange(`varlist', 6140, 6149) | inrange(`varlist', 6150, 6159) | inrange(`varlist', 6160, 6169) | inrange(`varlist', 6170, 6179) | inrange(`varlist', 6190, 6199)
		
		qui replace `generate' = 45 if inrange(`varlist', 6300, 6300) | inrange(`varlist', 6310, 6319) | inrange(`varlist', 6320, 6329) | inrange(`varlist', 6330, 6331) | inrange(`varlist', 6350, 6351) | inrange(`varlist', 6360, 6361) | inrange(`varlist', 6370, 6379) | inrange(`varlist', 6390, 6399) | inrange(`varlist', 6400, 6411)
		
		qui replace `generate' = 46 if inrange(`varlist', 6500, 6500) | inrange(`varlist', 6510, 6510) | inrange(`varlist', 6512, 6512) | inrange(`varlist', 6513, 6513) | inrange(`varlist', 6514, 6514) | inrange(`varlist', 6515, 6515) | inrange(`varlist', 6517, 6519) | inrange(`varlist', 6520, 6529) | inrange(`varlist', 6530, 6531) | inrange(`varlist', 6532, 6532) | inrange(`varlist', 6540, 6541) | inrange(`varlist', 6550, 6553) | inrange(`varlist', 6590, 6599) | inrange(`varlist', 6610, 6611)
		
		qui replace `generate' = 47 if inrange(`varlist', 6200, 6299) | inrange(`varlist', 6700, 6700) | inrange(`varlist', 6710, 6719) | inrange(`varlist', 6720, 6722) | inrange(`varlist', 6723, 6723) | inrange(`varlist', 6724, 6724) | inrange(`varlist', 6725, 6725) | inrange(`varlist', 6726, 6726) | inrange(`varlist', 6730, 6733) | inrange(`varlist', 6740, 6779) | inrange(`varlist', 6790, 6791) | inrange(`varlist', 6792, 6792) | inrange(`varlist', 6793, 6793) | inrange(`varlist', 6794, 6794) | inrange(`varlist', 6795, 6795) | inrange(`varlist', 6798, 6798) | inrange(`varlist', 6799, 6799)
		
		qui replace `generate' = 48 if inrange(`varlist', 4950, 4959) | inrange(`varlist', 4960, 4961) | inrange(`varlist', 4970, 4971) | inrange(`varlist', 4990, 4991)
	}



	// Fama French 49 industry
	else if `industry' == 49 {

		// define label
		if "`longlabels'" != "" {
			// the long label
			label define lbl_ff_49 1 "(1) Agriculture"
			label define lbl_ff_49 2 "(2) Food Products", add
			label define lbl_ff_49 3 "(3) Candy & Soda", add
			label define lbl_ff_49 4 "(4) Beer & Liquor", add
			label define lbl_ff_49 5 "(5) Tobacco Products", add
			label define lbl_ff_49 6 "(6) Recreation", add
			label define lbl_ff_49 7 "(7) Entertainment", add
			label define lbl_ff_49 8 "(8) Printing and Publishing", add
			label define lbl_ff_49 9 "(9) Consumer Goods", add
			label define lbl_ff_49 10 "(10) Apparel", add
			label define lbl_ff_49 11 "(11) Healthcare", add
			label define lbl_ff_49 12 "(12) Medical Equipment", add
			label define lbl_ff_49 13 "(13) Pharmaceutical Products", add
			label define lbl_ff_49 14 "(14) Chemicals", add
			label define lbl_ff_49 15 "(15) Rubber and Plastic Products", add
			label define lbl_ff_49 16 "(16) Textiles", add
			label define lbl_ff_49 17 "(17) Construction Materials", add
			label define lbl_ff_49 18 "(18) Construction", add
			label define lbl_ff_49 19 "(19) Steel Works Etc", add
			label define lbl_ff_49 20 "(20) Fabricated Products", add
			label define lbl_ff_49 21 "(21) Machinery", add
			label define lbl_ff_49 22 "(22) Electrical Equipment", add
			label define lbl_ff_49 23 "(23) Automobiles and Trucks", add
			label define lbl_ff_49 24 "(24) Aircraft", add
			label define lbl_ff_49 25 "(25) Shipbuilding, Railroad Equipment", add
			label define lbl_ff_49 26 "(26) Defense", add
			label define lbl_ff_49 27 "(27) Precious Metals", add
			label define lbl_ff_49 28 "(28) Non-Metallic and Industrial Metal Mining", add
			label define lbl_ff_49 29 "(29) Coal", add
			label define lbl_ff_49 30 "(30) Petroleum and Natural Gas", add
			label define lbl_ff_49 31 "(31) Utilities", add
			label define lbl_ff_49 32 "(32) Communication", add
			label define lbl_ff_49 33 "(33) Personal Services", add
			label define lbl_ff_49 34 "(34) Business Services", add
			label define lbl_ff_49 35 "(35) Computers", add
			label define lbl_ff_49 36 "(36) Computer Software ", add
			label define lbl_ff_49 37 "(37) Electronic Equipment", add
			label define lbl_ff_49 38 "(38) Measuring and Control Equipment", add
			label define lbl_ff_49 39 "(39) Business Supplies", add
			label define lbl_ff_49 40 "(40) Shipping Containers", add
			label define lbl_ff_49 41 "(41) Transportation", add
			label define lbl_ff_49 42 "(42) Wholesale", add
			label define lbl_ff_49 43 "(43) Retail ", add
			label define lbl_ff_49 44 "(44) Restaurants, Hotels, Motels", add
			label define lbl_ff_49 45 "(45) Banking", add
			label define lbl_ff_49 46 "(46) Insurance", add
			label define lbl_ff_49 47 "(47) Real Estate", add
			label define lbl_ff_49 48 "(48) Trading", add
			label define lbl_ff_49 49 "(49) Almost Nothing", add
		}
		else {
			// the short label
			label define lbl_ff_49 1 "(1) Agric" 2 "(2) Food" 3 "(3) Soda" 4 "(4) Beer" 5 "(5) Smoke" 6 "(6) Toys" 7 "(7) Fun" 8 "(8) Books" 9 "(9) Hshld" 10 "(10) Clths" 11 "(11) Hlth" 12 "(12) MedEq" 13 "(13) Drugs" 14 "(14) Chems" 15 "(15) Rubbr" 16 "(16) Txtls" 17 "(17) BldMt" 18 "(18) Cnstr" 19 "(19) Steel" 20 "(20) FabPr" 21 "(21) Mach" 22 "(22) ElcEq" 23 "(23) Autos" 24 "(24) Aero" 25 "(25) Ships" 26 "(26) Guns" 27 "(27) Gold" 28 "(28) Mines" 29 "(29) Coal" 30 "(30) Oil" 31 "(31) Util" 32 "(32) Telcm" 33 "(33) PerSv" 34 "(34) BusSv" 35 "(35) Hardw" 36 "(36) Softw" 37 "(37) Chips" 38 "(38) LabEq" 39 "(39) Paper" 40 "(40) Boxes" 41 "(41) Trans" 42 "(42) Whlsl" 43 "(43) Rtail" 44 "(44) Meals" 45 "(45) Banks" 46 "(46) Insur" 47 "(47) RlEst" 48 "(48) Fin" 49 "(49) Other"
		}
		label values `generate' lbl_ff_49

		// the actual assignment
		qui replace `generate' = 1 if inrange(`varlist', 0100, 0199) | inrange(`varlist', 0200, 0299) | inrange(`varlist', 0700, 0799) | inrange(`varlist', 0910, 0919) | inrange(`varlist', 2048, 2048)
		
		qui replace `generate' = 2 if inrange(`varlist', 2000, 2009) | inrange(`varlist', 2010, 2019) | inrange(`varlist', 2020, 2029) | inrange(`varlist', 2030, 2039) | inrange(`varlist', 2040, 2046) | inrange(`varlist', 2050, 2059) | inrange(`varlist', 2060, 2063) | inrange(`varlist', 2070, 2079) | inrange(`varlist', 2090, 2092) | inrange(`varlist', 2095, 2095) | inrange(`varlist', 2098, 2099)
		
		qui replace `generate' = 3 if inrange(`varlist', 2064, 2068) | inrange(`varlist', 2086, 2086) | inrange(`varlist', 2087, 2087) | inrange(`varlist', 2096, 2096) | inrange(`varlist', 2097, 2097)
		
		qui replace `generate' = 4 if inrange(`varlist', 2080, 2080) | inrange(`varlist', 2082, 2082) | inrange(`varlist', 2083, 2083) | inrange(`varlist', 2084, 2084) | inrange(`varlist', 2085, 2085)
		
		qui replace `generate' = 5 if inrange(`varlist', 2100, 2199)
		
		qui replace `generate' = 6 if inrange(`varlist', 0920, 0999) | inrange(`varlist', 3650, 3651) | inrange(`varlist', 3652, 3652) | inrange(`varlist', 3732, 3732) | inrange(`varlist', 3930, 3931) | inrange(`varlist', 3940, 3949)
		
		qui replace `generate' = 7 if inrange(`varlist', 7800, 7829) | inrange(`varlist', 7830, 7833) | inrange(`varlist', 7840, 7841) | inrange(`varlist', 7900, 7900) | inrange(`varlist', 7910, 7911) | inrange(`varlist', 7920, 7929) | inrange(`varlist', 7930, 7933) | inrange(`varlist', 7940, 7949) | inrange(`varlist', 7980, 7980) | inrange(`varlist', 7990, 7999)
		
		qui replace `generate' = 8 if inrange(`varlist', 2700, 2709) | inrange(`varlist', 2710, 2719) | inrange(`varlist', 2720, 2729) | inrange(`varlist', 2730, 2739) | inrange(`varlist', 2740, 2749) | inrange(`varlist', 2770, 2771) | inrange(`varlist', 2780, 2789) | inrange(`varlist', 2790, 2799)
		
		qui replace `generate' = 9 if inrange(`varlist', 2047, 2047) | inrange(`varlist', 2391, 2392) | inrange(`varlist', 2510, 2519) | inrange(`varlist', 2590, 2599) | inrange(`varlist', 2840, 2843) | inrange(`varlist', 2844, 2844) | inrange(`varlist', 3160, 3161) | inrange(`varlist', 3170, 3171) | inrange(`varlist', 3172, 3172) | inrange(`varlist', 3190, 3199) | inrange(`varlist', 3229, 3229) | inrange(`varlist', 3260, 3260) | inrange(`varlist', 3262, 3263) | inrange(`varlist', 3269, 3269) | inrange(`varlist', 3230, 3231) | inrange(`varlist', 3630, 3639) | inrange(`varlist', 3750, 3751) | inrange(`varlist', 3800, 3800) | inrange(`varlist', 3860, 3861) | inrange(`varlist', 3870, 3873) | inrange(`varlist', 3910, 3911) | inrange(`varlist', 3914, 3914) | inrange(`varlist', 3915, 3915) | inrange(`varlist', 3960, 3962) | inrange(`varlist', 3991, 3991) | inrange(`varlist', 3995, 3995)
		
		qui replace `generate' = 10 if inrange(`varlist', 2300, 2390) | inrange(`varlist', 3020, 3021) | inrange(`varlist', 3100, 3111) | inrange(`varlist', 3130, 3131) | inrange(`varlist', 3140, 3149) | inrange(`varlist', 3150, 3151) | inrange(`varlist', 3963, 3965)
		
		qui replace `generate' = 11 if inrange(`varlist', 8000, 8099)
		
		qui replace `generate' = 12 if inrange(`varlist', 3693, 3693) | inrange(`varlist', 3840, 3849) | inrange(`varlist', 3850, 3851)
		
		qui replace `generate' = 13 if inrange(`varlist', 2830, 2830) | inrange(`varlist', 2831, 2831) | inrange(`varlist', 2833, 2833) | inrange(`varlist', 2834, 2834) | inrange(`varlist', 2835, 2835) | inrange(`varlist', 2836, 2836)
		
		qui replace `generate' = 14 if inrange(`varlist', 2800, 2809) | inrange(`varlist', 2810, 2819) | inrange(`varlist', 2820, 2829) | inrange(`varlist', 2850, 2859) | inrange(`varlist', 2860, 2869) | inrange(`varlist', 2870, 2879) | inrange(`varlist', 2890, 2899)
		
		qui replace `generate' = 15 if inrange(`varlist', 3031, 3031) | inrange(`varlist', 3041, 3041) | inrange(`varlist', 3050, 3053) | inrange(`varlist', 3060, 3069) | inrange(`varlist', 3070, 3079) | inrange(`varlist', 3080, 3089) | inrange(`varlist', 3090, 3099)
		
		qui replace `generate' = 16 if inrange(`varlist', 2200, 2269) | inrange(`varlist', 2270, 2279) | inrange(`varlist', 2280, 2284) | inrange(`varlist', 2290, 2295) | inrange(`varlist', 2297, 2297) | inrange(`varlist', 2298, 2298) | inrange(`varlist', 2299, 2299) | inrange(`varlist', 2393, 2395) | inrange(`varlist', 2397, 2399)
		
		qui replace `generate' = 17 if inrange(`varlist', 0800, 0899) | inrange(`varlist', 2400, 2439) | inrange(`varlist', 2450, 2459) | inrange(`varlist', 2490, 2499) | inrange(`varlist', 2660, 2661) | inrange(`varlist', 2950, 2952) | inrange(`varlist', 3200, 3200) | inrange(`varlist', 3210, 3211) | inrange(`varlist', 3240, 3241) | inrange(`varlist', 3250, 3259) | inrange(`varlist', 3261, 3261) | inrange(`varlist', 3264, 3264) | inrange(`varlist', 3270, 3275) | inrange(`varlist', 3280, 3281) | inrange(`varlist', 3290, 3293) | inrange(`varlist', 3295, 3299) | inrange(`varlist', 3420, 3429) | inrange(`varlist', 3430, 3433) | inrange(`varlist', 3440, 3441) | inrange(`varlist', 3442, 3442) | inrange(`varlist', 3446, 3446) | inrange(`varlist', 3448, 3448) | inrange(`varlist', 3449, 3449) | inrange(`varlist', 3450, 3451) | inrange(`varlist', 3452, 3452) | inrange(`varlist', 3490, 3499) | inrange(`varlist', 3996, 3996)
		
		qui replace `generate' = 18 if inrange(`varlist', 1500, 1511) | inrange(`varlist', 1520, 1529) | inrange(`varlist', 1530, 1539) | inrange(`varlist', 1540, 1549) | inrange(`varlist', 1600, 1699) | inrange(`varlist', 1700, 1799)
		
		qui replace `generate' = 19 if inrange(`varlist', 3300, 3300) | inrange(`varlist', 3310, 3317) | inrange(`varlist', 3320, 3325) | inrange(`varlist', 3330, 3339) | inrange(`varlist', 3340, 3341) | inrange(`varlist', 3350, 3357) | inrange(`varlist', 3360, 3369) | inrange(`varlist', 3370, 3379) | inrange(`varlist', 3390, 3399)
		
		qui replace `generate' = 20 if inrange(`varlist', 3400, 3400) | inrange(`varlist', 3443, 3443) | inrange(`varlist', 3444, 3444) | inrange(`varlist', 3460, 3469) | inrange(`varlist', 3470, 3479)
		
		qui replace `generate' = 21 if inrange(`varlist', 3510, 3519) | inrange(`varlist', 3520, 3529) | inrange(`varlist', 3530, 3530) | inrange(`varlist', 3531, 3531) | inrange(`varlist', 3532, 3532) | inrange(`varlist', 3533, 3533) | inrange(`varlist', 3534, 3534) | inrange(`varlist', 3535, 3535) | inrange(`varlist', 3536, 3536) | inrange(`varlist', 3538, 3538) | inrange(`varlist', 3540, 3549) | inrange(`varlist', 3550, 3559) | inrange(`varlist', 3560, 3569) | inrange(`varlist', 3580, 3580) | inrange(`varlist', 3581, 3581) | inrange(`varlist', 3582, 3582) | inrange(`varlist', 3585, 3585) | inrange(`varlist', 3586, 3586) | inrange(`varlist', 3589, 3589) | inrange(`varlist', 3590, 3599)
		
		qui replace `generate' = 22 if inrange(`varlist', 3600, 3600) | inrange(`varlist', 3610, 3613) | inrange(`varlist', 3620, 3621) | inrange(`varlist', 3623, 3629) | inrange(`varlist', 3640, 3644) | inrange(`varlist', 3645, 3645) | inrange(`varlist', 3646, 3646) | inrange(`varlist', 3648, 3649) | inrange(`varlist', 3660, 3660) | inrange(`varlist', 3690, 3690) | inrange(`varlist', 3691, 3692) | inrange(`varlist', 3699, 3699)
		
		qui replace `generate' = 23 if inrange(`varlist', 2296, 2296) | inrange(`varlist', 2396, 2396) | inrange(`varlist', 3010, 3011) | inrange(`varlist', 3537, 3537) | inrange(`varlist', 3647, 3647) | inrange(`varlist', 3694, 3694) | inrange(`varlist', 3700, 3700) | inrange(`varlist', 3710, 3710) | inrange(`varlist', 3711, 3711) | inrange(`varlist', 3713, 3713) | inrange(`varlist', 3714, 3714) | inrange(`varlist', 3715, 3715) | inrange(`varlist', 3716, 3716) | inrange(`varlist', 3792, 3792) | inrange(`varlist', 3790, 3791) | inrange(`varlist', 3799, 3799)
		
		qui replace `generate' = 24 if inrange(`varlist', 3720, 3720) | inrange(`varlist', 3721, 3721) | inrange(`varlist', 3723, 3724) | inrange(`varlist', 3725, 3725) | inrange(`varlist', 3728, 3729)
		
		qui replace `generate' = 25 if inrange(`varlist', 3730, 3731) | inrange(`varlist', 3740, 3743)
		
		qui replace `generate' = 26 if inrange(`varlist', 3760, 3769) | inrange(`varlist', 3795, 3795) | inrange(`varlist', 3480, 3489)
		
		qui replace `generate' = 27 if inrange(`varlist', 1040, 1049)
		
		qui replace `generate' = 28 if inrange(`varlist', 1000, 1009) | inrange(`varlist', 1010, 1019) | inrange(`varlist', 1020, 1029) | inrange(`varlist', 1030, 1039) | inrange(`varlist', 1050, 1059) | inrange(`varlist', 1060, 1069) | inrange(`varlist', 1070, 1079) | inrange(`varlist', 1080, 1089) | inrange(`varlist', 1090, 1099) | inrange(`varlist', 1100, 1119) | inrange(`varlist', 1400, 1499)
		
		qui replace `generate' = 29 if inrange(`varlist', 1200, 1299)
		
		qui replace `generate' = 30 if inrange(`varlist', 1300, 1300) | inrange(`varlist', 1310, 1319) | inrange(`varlist', 1320, 1329) | inrange(`varlist', 1330, 1339) | inrange(`varlist', 1370, 1379) | inrange(`varlist', 1380, 1380) | inrange(`varlist', 1381, 1381) | inrange(`varlist', 1382, 1382) | inrange(`varlist', 1389, 1389) | inrange(`varlist', 2900, 2912) | inrange(`varlist', 2990, 2999)
		
		qui replace `generate' = 31 if inrange(`varlist', 4900, 4900) | inrange(`varlist', 4910, 4911) | inrange(`varlist', 4920, 4922) | inrange(`varlist', 4923, 4923) | inrange(`varlist', 4924, 4925) | inrange(`varlist', 4930, 4931) | inrange(`varlist', 4932, 4932) | inrange(`varlist', 4939, 4939) | inrange(`varlist', 4940, 4942)
		
		qui replace `generate' = 32 if inrange(`varlist', 4800, 4800) | inrange(`varlist', 4810, 4813) | inrange(`varlist', 4820, 4822) | inrange(`varlist', 4830, 4839) | inrange(`varlist', 4840, 4841) | inrange(`varlist', 4880, 4889) | inrange(`varlist', 4890, 4890) | inrange(`varlist', 4891, 4891) | inrange(`varlist', 4892, 4892) | inrange(`varlist', 4899, 4899)
		
		qui replace `generate' = 33 if inrange(`varlist', 7020, 7021) | inrange(`varlist', 7030, 7033) | inrange(`varlist', 7200, 7200) | inrange(`varlist', 7210, 7212) | inrange(`varlist', 7214, 7214) | inrange(`varlist', 7215, 7216) | inrange(`varlist', 7217, 7217) | inrange(`varlist', 7219, 7219) | inrange(`varlist', 7220, 7221) | inrange(`varlist', 7230, 7231) | inrange(`varlist', 7240, 7241) | inrange(`varlist', 7250, 7251) | inrange(`varlist', 7260, 7269) | inrange(`varlist', 7270, 7290) | inrange(`varlist', 7291, 7291) | inrange(`varlist', 7292, 7299) | inrange(`varlist', 7395, 7395) | inrange(`varlist', 7500, 7500) | inrange(`varlist', 7520, 7529) | inrange(`varlist', 7530, 7539) | inrange(`varlist', 7540, 7549) | inrange(`varlist', 7600, 7600) | inrange(`varlist', 7620, 7620) | inrange(`varlist', 7622, 7622) | inrange(`varlist', 7623, 7623) | inrange(`varlist', 7629, 7629) | inrange(`varlist', 7630, 7631) | inrange(`varlist', 7640, 7641) | inrange(`varlist', 7690, 7699) | inrange(`varlist', 8100, 8199) | inrange(`varlist', 8200, 8299) | inrange(`varlist', 8300, 8399) | inrange(`varlist', 8400, 8499) | inrange(`varlist', 8600, 8699) | inrange(`varlist', 8800, 8899) | inrange(`varlist', 7510, 7515)
		
		qui replace `generate' = 34 if inrange(`varlist', 2750, 2759) | inrange(`varlist', 3993, 3993) | inrange(`varlist', 7218, 7218) | inrange(`varlist', 7300, 7300) | inrange(`varlist', 7310, 7319) | inrange(`varlist', 7320, 7329) | inrange(`varlist', 7330, 7339) | inrange(`varlist', 7340, 7342) | inrange(`varlist', 7349, 7349) | inrange(`varlist', 7350, 7351) | inrange(`varlist', 7352, 7352) | inrange(`varlist', 7353, 7353) | inrange(`varlist', 7359, 7359) | inrange(`varlist', 7360, 7369) | inrange(`varlist', 7374, 7374) | inrange(`varlist', 7376, 7376) | inrange(`varlist', 7377, 7377) | inrange(`varlist', 7378, 7378) | inrange(`varlist', 7379, 7379) | inrange(`varlist', 7380, 7380) | inrange(`varlist', 7381, 7382) | inrange(`varlist', 7383, 7383) | inrange(`varlist', 7384, 7384) | inrange(`varlist', 7385, 7385) | inrange(`varlist', 7389, 7390) | inrange(`varlist', 7391, 7391) | inrange(`varlist', 7392, 7392) | inrange(`varlist', 7393, 7393) | inrange(`varlist', 7394, 7394) | inrange(`varlist', 7396, 7396) | inrange(`varlist', 7397, 7397) | inrange(`varlist', 7399, 7399) | inrange(`varlist', 7519, 7519) | inrange(`varlist', 8700, 8700) | inrange(`varlist', 8710, 8713) | inrange(`varlist', 8720, 8721) | inrange(`varlist', 8730, 8734) | inrange(`varlist', 8740, 8748) | inrange(`varlist', 8900, 8910) | inrange(`varlist', 8911, 8911) | inrange(`varlist', 8920, 8999) | inrange(`varlist', 4220, 4229)
		
		qui replace `generate' = 35 if inrange(`varlist', 3570, 3579) | inrange(`varlist', 3680, 3680) | inrange(`varlist', 3681, 3681) | inrange(`varlist', 3682, 3682) | inrange(`varlist', 3683, 3683) | inrange(`varlist', 3684, 3684) | inrange(`varlist', 3685, 3685) | inrange(`varlist', 3686, 3686) | inrange(`varlist', 3687, 3687) | inrange(`varlist', 3688, 3688) | inrange(`varlist', 3689, 3689) | inrange(`varlist', 3695, 3695)
		
		qui replace `generate' = 36 if inrange(`varlist', 7370, 7372) | inrange(`varlist', 7375, 7375) | inrange(`varlist', 7373, 7373)
		
		qui replace `generate' = 37 if inrange(`varlist', 3622, 3622) | inrange(`varlist', 3661, 3661) | inrange(`varlist', 3662, 3662) | inrange(`varlist', 3663, 3663) | inrange(`varlist', 3664, 3664) | inrange(`varlist', 3665, 3665) | inrange(`varlist', 3666, 3666) | inrange(`varlist', 3669, 3669) | inrange(`varlist', 3670, 3679) | inrange(`varlist', 3810, 3810) | inrange(`varlist', 3812, 3812)
		
		qui replace `generate' = 38 if inrange(`varlist', 3811, 3811) | inrange(`varlist', 3820, 3820) | inrange(`varlist', 3821, 3821) | inrange(`varlist', 3822, 3822) | inrange(`varlist', 3823, 3823) | inrange(`varlist', 3824, 3824) | inrange(`varlist', 3825, 3825) | inrange(`varlist', 3826, 3826) | inrange(`varlist', 3827, 3827) | inrange(`varlist', 3829, 3829) | inrange(`varlist', 3830, 3839)
		
		qui replace `generate' = 39 if inrange(`varlist', 2520, 2549) | inrange(`varlist', 2600, 2639) | inrange(`varlist', 2670, 2699) | inrange(`varlist', 2760, 2761) | inrange(`varlist', 3950, 3955)
		
		qui replace `generate' = 40 if inrange(`varlist', 2440, 2449) | inrange(`varlist', 2640, 2659) | inrange(`varlist', 3220, 3221) | inrange(`varlist', 3410, 3412)
		
		qui replace `generate' = 41 if inrange(`varlist', 4000, 4013) | inrange(`varlist', 4040, 4049) | inrange(`varlist', 4100, 4100) | inrange(`varlist', 4110, 4119) | inrange(`varlist', 4120, 4121) | inrange(`varlist', 4130, 4131) | inrange(`varlist', 4140, 4142) | inrange(`varlist', 4150, 4151) | inrange(`varlist', 4170, 4173) | inrange(`varlist', 4190, 4199) | inrange(`varlist', 4200, 4200) | inrange(`varlist', 4210, 4219) | inrange(`varlist', 4230, 4231) | inrange(`varlist', 4240, 4249) | inrange(`varlist', 4400, 4499) | inrange(`varlist', 4500, 4599) | inrange(`varlist', 4600, 4699) | inrange(`varlist', 4700, 4700) | inrange(`varlist', 4710, 4712) | inrange(`varlist', 4720, 4729) | inrange(`varlist', 4730, 4739) | inrange(`varlist', 4740, 4749) | inrange(`varlist', 4780, 4780) | inrange(`varlist', 4782, 4782) | inrange(`varlist', 4783, 4783) | inrange(`varlist', 4784, 4784) | inrange(`varlist', 4785, 4785) | inrange(`varlist', 4789, 4789)
		
		qui replace `generate' = 42 if inrange(`varlist', 5000, 5000) | inrange(`varlist', 5010, 5015) | inrange(`varlist', 5020, 5023) | inrange(`varlist', 5030, 5039) | inrange(`varlist', 5040, 5042) | inrange(`varlist', 5043, 5043) | inrange(`varlist', 5044, 5044) | inrange(`varlist', 5045, 5045) | inrange(`varlist', 5046, 5046) | inrange(`varlist', 5047, 5047) | inrange(`varlist', 5048, 5048) | inrange(`varlist', 5049, 5049) | inrange(`varlist', 5050, 5059) | inrange(`varlist', 5060, 5060) | inrange(`varlist', 5063, 5063) | inrange(`varlist', 5064, 5064) | inrange(`varlist', 5065, 5065) | inrange(`varlist', 5070, 5078) | inrange(`varlist', 5080, 5080) | inrange(`varlist', 5081, 5081) | inrange(`varlist', 5082, 5082) | inrange(`varlist', 5083, 5083) | inrange(`varlist', 5084, 5084) | inrange(`varlist', 5085, 5085) | inrange(`varlist', 5086, 5087) | inrange(`varlist', 5088, 5088) | inrange(`varlist', 5090, 5090) | inrange(`varlist', 5091, 5092) | inrange(`varlist', 5093, 5093) | inrange(`varlist', 5094, 5094) | inrange(`varlist', 5099, 5099) | inrange(`varlist', 5100, 5100) | inrange(`varlist', 5110, 5113) | inrange(`varlist', 5120, 5122) | inrange(`varlist', 5130, 5139) | inrange(`varlist', 5140, 5149) | inrange(`varlist', 5150, 5159) | inrange(`varlist', 5160, 5169) | inrange(`varlist', 5170, 5172) | inrange(`varlist', 5180, 5182) | inrange(`varlist', 5190, 5199)
		
		qui replace `generate' = 43 if inrange(`varlist', 5200, 5200) | inrange(`varlist', 5210, 5219) | inrange(`varlist', 5220, 5229) | inrange(`varlist', 5230, 5231) | inrange(`varlist', 5250, 5251) | inrange(`varlist', 5260, 5261) | inrange(`varlist', 5270, 5271) | inrange(`varlist', 5300, 5300) | inrange(`varlist', 5310, 5311) | inrange(`varlist', 5320, 5320) | inrange(`varlist', 5330, 5331) | inrange(`varlist', 5334, 5334) | inrange(`varlist', 5340, 5349) | inrange(`varlist', 5390, 5399) | inrange(`varlist', 5400, 5400) | inrange(`varlist', 5410, 5411) | inrange(`varlist', 5412, 5412) | inrange(`varlist', 5420, 5429) | inrange(`varlist', 5430, 5439) | inrange(`varlist', 5440, 5449) | inrange(`varlist', 5450, 5459) | inrange(`varlist', 5460, 5469) | inrange(`varlist', 5490, 5499) | inrange(`varlist', 5500, 5500) | inrange(`varlist', 5510, 5529) | inrange(`varlist', 5530, 5539) | inrange(`varlist', 5540, 5549) | inrange(`varlist', 5550, 5559) | inrange(`varlist', 5560, 5569) | inrange(`varlist', 5570, 5579) | inrange(`varlist', 5590, 5599) | inrange(`varlist', 5600, 5699) | inrange(`varlist', 5700, 5700) | inrange(`varlist', 5710, 5719) | inrange(`varlist', 5720, 5722) | inrange(`varlist', 5730, 5733) | inrange(`varlist', 5734, 5734) | inrange(`varlist', 5735, 5735) | inrange(`varlist', 5736, 5736) | inrange(`varlist', 5750, 5799) | inrange(`varlist', 5900, 5900) | inrange(`varlist', 5910, 5912) | inrange(`varlist', 5920, 5929) | inrange(`varlist', 5930, 5932) | inrange(`varlist', 5940, 5940) | inrange(`varlist', 5941, 5941) | inrange(`varlist', 5942, 5942) | inrange(`varlist', 5943, 5943) | inrange(`varlist', 5944, 5944) | inrange(`varlist', 5945, 5945) | inrange(`varlist', 5946, 5946) | inrange(`varlist', 5947, 5947) | inrange(`varlist', 5948, 5948) | inrange(`varlist', 5949, 5949) | inrange(`varlist', 5950, 5959) | inrange(`varlist', 5960, 5969) | inrange(`varlist', 5970, 5979) | inrange(`varlist', 5980, 5989) | inrange(`varlist', 5990, 5990) | inrange(`varlist', 5992, 5992) | inrange(`varlist', 5993, 5993) | inrange(`varlist', 5994, 5994) | inrange(`varlist', 5995, 5995) | inrange(`varlist', 5999, 5999)
		
		qui replace `generate' = 44 if inrange(`varlist', 5800, 5819) | inrange(`varlist', 5820, 5829) | inrange(`varlist', 5890, 5899) | inrange(`varlist', 7000, 7000) | inrange(`varlist', 7010, 7019) | inrange(`varlist', 7040, 7049) | inrange(`varlist', 7213, 7213)
		
		qui replace `generate' = 45 if inrange(`varlist', 6000, 6000) | inrange(`varlist', 6010, 6019) | inrange(`varlist', 6020, 6020) | inrange(`varlist', 6021, 6021) | inrange(`varlist', 6022, 6022) | inrange(`varlist', 6023, 6024) | inrange(`varlist', 6025, 6025) | inrange(`varlist', 6026, 6026) | inrange(`varlist', 6027, 6027) | inrange(`varlist', 6028, 6029) | inrange(`varlist', 6030, 6036) | inrange(`varlist', 6040, 6059) | inrange(`varlist', 6060, 6062) | inrange(`varlist', 6080, 6082) | inrange(`varlist', 6090, 6099) | inrange(`varlist', 6100, 6100) | inrange(`varlist', 6110, 6111) | inrange(`varlist', 6112, 6113) | inrange(`varlist', 6120, 6129) | inrange(`varlist', 6130, 6139) | inrange(`varlist', 6140, 6149) | inrange(`varlist', 6150, 6159) | inrange(`varlist', 6160, 6169) | inrange(`varlist', 6170, 6179) | inrange(`varlist', 6190, 6199)
		
		qui replace `generate' = 46 if inrange(`varlist', 6300, 6300) | inrange(`varlist', 6310, 6319) | inrange(`varlist', 6320, 6329) | inrange(`varlist', 6330, 6331) | inrange(`varlist', 6350, 6351) | inrange(`varlist', 6360, 6361) | inrange(`varlist', 6370, 6379) | inrange(`varlist', 6390, 6399) | inrange(`varlist', 6400, 6411)

		qui replace `generate' = 47 if inrange(`varlist', 6500, 6500) | inrange(`varlist', 6510, 6510) | inrange(`varlist', 6512, 6512) | inrange(`varlist', 6513, 6513) | inrange(`varlist', 6514, 6514) | inrange(`varlist', 6515, 6515) | inrange(`varlist', 6517, 6519) | inrange(`varlist', 6520, 6529) | inrange(`varlist', 6530, 6531) | inrange(`varlist', 6532, 6532) | inrange(`varlist', 6540, 6541) | inrange(`varlist', 6550, 6553) | inrange(`varlist', 6590, 6599) | inrange(`varlist', 6610, 6611)
		
		qui replace `generate' = 48 if inrange(`varlist', 6200, 6299) | inrange(`varlist', 6700, 6700) | inrange(`varlist', 6710, 6719) | inrange(`varlist', 6720, 6722) | inrange(`varlist', 6723, 6723) | inrange(`varlist', 6724, 6724) | inrange(`varlist', 6725, 6725) | inrange(`varlist', 6726, 6726) | inrange(`varlist', 6730, 6733) | inrange(`varlist', 6740, 6779) | inrange(`varlist', 6790, 6791) | inrange(`varlist', 6792, 6792) | inrange(`varlist', 6793, 6793) | inrange(`varlist', 6794, 6794) | inrange(`varlist', 6795, 6795) | inrange(`varlist', 6798, 6798) | inrange(`varlist', 6799, 6799)
		
		qui replace `generate' = 49 if inrange(`varlist', 4950, 4959) | inrange(`varlist', 4960, 4961) | inrange(`varlist', 4970, 4971) | inrange(`varlist', 4990, 4991)
	}



	// Throw an error if industry is not in the list
	else {
		drop `generate'
		display as error "Industry option can only be 5, 10, 12, 17, 30, 38, 48, or 49."
		exit 175
	}
end
