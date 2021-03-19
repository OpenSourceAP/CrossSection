/**********************************************************
merges select variables from wrdslin/nyse/sasdata/taqms/mast/mastm*.sas* 
into one file
Andrew 2018 07

For running on wrds server, obviously.

first run cp_mastm.sh to avoid authorization errors.

**********************************************************/

proc datasets library=WORK kill; run; quit;
dm "out;clear;log;clear;"; /*clears output and log windows*/

/* USER 

*/

*libname mast "/wrdslin/nyse/sasdata/taqms/mast/";
libname mast "/scratch/frb/ayc_mast/"; * testing;

%let goodyear = 2017;
%let goodmonth = 12;
%let goodday = 29;

%let mergedname = '~/test_output/mastm.csv';
%let samplename = '~/test_output/mastm_sample.csv';


/*
** Push names of files to a dataset
** called 'contents' using proc 
** contents.

This can create authorization errors and cause all following commands to fail.  We don't have 
access to the most recent year of data.

mastm begins in 2009 for some reason
*/
proc contents data = mast._all_ noprint out = contents (keep = memname);
run;


/* Eliminate any duplicate names of the SAS datasets */
proc sort data = contents nodupkey;
  by memname;
run;

/*
** Create 2 macro variables 
** 1. The names of each SAS dataset
** 2. The number of datasets in 'mast'
*/

data _null_;
  set contents end = last;
  by memname;
  i + 1;
 
  /* Each SAS dataset is assigned to macro &&name&i */
  call symputx('name'||trim(left(put(i,8.))),memname);
  /* Number of SAS datasets is assigned to macro count */
  if last then call symputx('count',i);

run;


/*
** Append datasets

WARNING: initializing can be tricky
*/

* initialize dataset by creating an empty one with column names
use as set the name of any good dataset

most of DTAQ uses SYMBOL_ROOT, but this varible is missing
in the 2017 matm files.  Instead we have SYMBOL_15
;
data final; set mast.mastm_&goodyear&goodmonth&goodday
  (keep=DATE CUSIP SYMBOL_15 SEC_DESC); 
  where SYMBOL_15 = "THEREISNOTICKERLIKETHIS";
run;

%macro combine;
  %do i = 1 %to &count;
  proc append base = final data = mast.&&name&i 
    (keep=DATE CUSIP SYMBOL_15 SEC_DESC) force;
    run;
  %end;
%mend combine;

%combine;

/* Aggregate to monthly:
 For each firm, keep last observation in each month */
data final; set final;
  month = month(date);
run;

proc sort data=final; by SYMBOL_15 month Date; run;  

data final; set final;
  by SYMBOL_15 month;
  if last.month; * keep only last obs each month;
run;  

data final; set final (drop = month); run;  

/*
** Export the dataset to csv
*/


proc export data = final
  outfile = &mergedname
  dbms = csv
  replace;
run;


* export sample;
data sample; set final;
	where year(date) = &goodyear & month(date) = &goodmonth;
run;
proc export data = sample
  outfile = &samplename
  dbms = csv
  replace;
run;


