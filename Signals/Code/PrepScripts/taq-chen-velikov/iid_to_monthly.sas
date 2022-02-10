/* 
  reads in wrds iid data and exports csv to ~/temp_output/ 
  andrew chen 2021 04	
  
  even though wrds labels these spreads as "pct" or "percent," it's clear these spreads are straight ratios, hence the 100*
  
  We follow Abdi and Ranaldo for aggregation and additional screens
  	dollar weighted ave of intraday proporational effective spreads to obtain average daily spreads, then average 
  	days to get monthly spread.  They also use a screen like this one:
  	where spread_iid < 4*spreadq_iid
		and spread_iid < 40
		and spreadq_iid < 40;  	
  
  We follow Lou and Shu for quote delays (modified to use DTAQ and iid):
  	before 1999: 1 sec (2 sec is unavailable)
  	1999-2003: 0 sec
  	2003-present: DTAQ 

  We found that the interpolated spreads are pretty badly behaved, so don't use them.
  
  wrds documentation
	https://wrds-www.wharton.upenn.edu/pages/get-data/intraday-indicators-wrds/
	https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/wrds-intraday-indicators/
	https://wrds-www.wharton.upenn.edu/documents/1038/WRDS_DTAQ_IID_Manual_1.0.pdf
	
  updated 2021 08 to add sym_root and sym_suffix
	
*/

proc datasets library=WORK kill; run; quit;
dm "out;clear;log;clear;"; /*clears output and log windows*/

libname s_iid "/wrds/nyse/sasdata/wrds_taqs_iid_v1/";
libname ms_iid "/wrds/nyse/sasdata/wrds_taqms_iid/";
*%let subsamp = month(date) = 1 and year(date) = 2017;
%let subsamp = not missing(date);

* ==== IMPORT MTAQ AND COLLAPSE TO MONTHLY ====;

* MTAQ; 
* see https://wrds-www.wharton.upenn.edu/pages/get-data/nyse-trade-and-quote/trade-and-quote-monthly-product-1993-2014/taq-tools/intraday-indicators-by-wrds/;
* type of spreads chosen here;
data temp0; set s_iid.wrds_iid:;
	where &subsamp;

	if year(date) < 1999 then espread_pct = 100*ESpreadPct_VW1;
	else espread_pct = 100*ESpreadPct_VW0;	
	qspread_pct = 100*QSpreadPct_TW_m; 	* time weighted, market hours;
	
	yearm = year(date)*100 + month(date);	
	
  	keep date symbol espread_pct qspread_pct yearm;
run;

* clean and save last obs of month;
proc sort data=temp0; by symbol yearm date; run;
data temp1; set temp0;
  	where espread_pct < 4*qspread_pct
		and espread_pct < 40
		and qspread_pct < 40
		and not missing(espread_pct);  		
  	by symbol yearm;
  	if last.yearm then do;
  		espread_pct_month_end = espread_pct;
	end;		
run;	

* collapse to monthly;
proc means data=temp1 noprint;
	var espread_pct espread_pct_month_end;
	by symbol yearm;
	output out = temp2 mean= /autoname;
run;		

* clean up and save;
data monthly_mtaq; set temp2;	
	espread_n = _freq_;
	source = 'mtaq';
	rename espread_pct_month_end_Mean = espread_pct_month_end;
	keep symbol yearm espread: source;
run;	

* ==== IMPORT DTAQ AND COLLAPSE TO MONTHLY ====;

* DTAQ;
* see https://wrds-www.wharton.upenn.edu/pages/get-data/nyse-trade-and-quote/millisecond-trade-and-quote-daily-product-2003-present-updated-daily/taq-millisecond-tools/millisecond-intraday-indicators-by-wrds/;
data temp0; set ms_iid.wrds_iid_:;
	where &subsamp;
	
	espread_pct = 100*EffectiveSpread_Percent_DW;
	qspread_pct = 100*QuotedSpread_Percent_tw; 	* time weighted, market hours (only one available);	
	yearm = year(date)*100 + month(date);		
	
  	keep date symbol sym_root sym_suffix espread_pct qspread_pct year yearm;  	
run;

* clean and save last obs of month;
proc sort data=temp0; by symbol yearm date; run;
data temp1; set temp0;
  	where espread_pct < 4*qspread_pct
		and espread_pct < 40
		and qspread_pct < 40
		and not missing(espread_pct);  		
  	by symbol yearm;
  	if last.yearm then do;
  		espread_pct_month_end = espread_pct;
	end;		
run;	

* collapse to monthly;
proc sort data=temp1; by symbol sym_root sym_suffix yearm; run;
proc means data=temp1 noprint;
	var espread_pct espread_pct_month_end;
	by symbol sym_root sym_suffix yearm;
	output out = temp2 mean= /autoname;
run;		

* clean up and save;
data monthly_dtaq; set temp2;	
	espread_n = _freq_;
	source = 'dtaq';
	rename espread_pct_month_end_Mean = espread_pct_month_end;
	keep symbol sym_root sym_suffix yearm espread: source;
run;	

* ==== FULL JOIN MTAQ AND DTAQ ==== ;

* append datasets and clean up a few whitespaces in mtaq;
data temp0; set monthly_mtaq monthly_dtaq; 
  symbol = compress(symbol); * clean up a few whitespaces in mtaq;
run;

* drop mtaq duplicates;
proc sort data=temp0; by symbol yearm source; run;
data monthly_iid; set temp0;
	by symbol yearm;
	if first.yearm then output;
run;	


* ==== SAVE ==== ;
proc print data=monthly_iid (obs=20); run;

proc export data = monthly_iid
  outfile = "~/temp_output/wrds_iid_monthly.csv"
  dbms = csv
  replace;
run;

