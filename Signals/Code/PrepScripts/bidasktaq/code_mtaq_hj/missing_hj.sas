/*
2018 10 Andrew

Trying to understand why Pre 1993 04 06 MTAQ spreads are missing
*/

libname test 'b:/costzoo/data/mtaq_missing/';


* 04 02;
%let date = 19930402;

data symbol; set test.cq_&date; 
	by symbol;
	if last.symbol;
run;

data symbol; set test.cq_&date; 
	by symbol;
	where bidsiz > 0 or ofrsiz > 0;
	if last.symbol;
run;


data symbol; set test.ct_&date; 
	by symbol;
	if last.symbol;
run;

* 04 05;
%let date = 19930405;

data symbol; set test.cq_&date; 
	by symbol;
	if last.symbol;
run;

data symbol; set test.cq_&date; 
	by symbol;
	where bidsiz > 0 or ofrsiz > 0;
	if last.symbol;
run;


data symbol; set test.ct_&date; 
	by symbol;
	if last.symbol;
run;

* bad data above, good below =============================================;


* 04 06;
%let date = 19930406;

data symbol; set test.cq_&date; 
	by symbol;
	if last.symbol;
run;

data symbol; set test.cq_&date; 
	by symbol;
	where bidsiz > 0 or ofrsiz > 0;
	if last.symbol;
run;


data symbol; set test.ct_&date; 
	by symbol;
	if last.symbol;
run;

* 04 07;
%let date = 19930407;

data symbol; set test.cq_&date; 
	by symbol;
	if last.symbol;
run;

data symbol; set test.cq_&date; 
	by symbol;
	where bidsiz > 0 or ofrsiz > 0;
	if last.symbol;
run;


data symbol; set test.ct_&date; 
	by symbol;
	if last.symbol;
run;


* Closer look ==============================================;

* bad: 04 05;
data cq; set test.cq_19930405; run;
proc means data = cq noprint;
	var bidsiz;
	by symbol; 
	output out = sizmax max = sizmax;
	label sizmax = 'sizmax';
run;
proc sort data = sizmax; by sizmax; run;
data sizmax; set sizmax;
	zerosiz = 0;
	if sizmax = 0 then zerosiz = 1;
run;
proc means data= sizmax;
	var zerosiz sizmax;
	title "1993 04 05";
run;

* good: 04 06;
data cq; set test.cq_19930406; run;
proc means data = cq noprint;
	var bidsiz;
	by symbol; 
	output out = sizmax max = sizmax;
	label sizmax = 'sizmax';
run;
proc sort data = sizmax; by sizmax; run;
data sizmax; set sizmax;
	zerosiz = 0;
	if sizmax = 0 then zerosiz = 1;
run;

proc means data= sizmax;
	var zerosiz sizmax;
	title "1993 04 06";
run;
