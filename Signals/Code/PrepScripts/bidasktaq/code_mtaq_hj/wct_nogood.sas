/*
Andrew Chen 2018 10
Shows how WRDS consolidated trade data is no good in 1993-199403 using 
data that is manually downloaded and somewhat processeed

*/

libname test 'b:/costzoo/data/test_data/';

%let filename = wct_19940307;


* WCT 03 07;
data symbol; set test.wct_19940307; 
	by symbol;
	if last.symbol;
run;

proc means data=symbol; 
	var price midpoint2 qspread0;
	title 'WCT 19940307';
run;

* WCT 03 08;
data symbol; set test.wct_19940308; 
	by symbol;
	if last.symbol;
run;

proc means data=symbol; 
	var price midpoint2 qspread0;
	title 'WCT 19940308';
run;

* HJ code 03 07;
data symbol; set test.effspread19940307; 
	spreadclean = effectivespread_percent_ave;
	if effectivespread_percent_ave = 0 then spreadclean = .;
	if effectivespread_percent_ave > 0.20 then spreadclean = .;
run;

proc means data=symbol;
	var effectivespread_percent_ave spreadclean;
	title 'HJ 19940307';
run;

* HJ code 03 08;
data symbol; set test.effspread19940308; 
	spreadclean = effectivespread_percent_ave;
	if effectivespread_percent_ave = 0 then spreadclean = .;
	if effectivespread_percent_ave > 0.20 then spreadclean = .;
run;

proc means data=symbol;
	var effectivespread_percent_ave spreadclean;
	title 'HJ 19940308';
run;
