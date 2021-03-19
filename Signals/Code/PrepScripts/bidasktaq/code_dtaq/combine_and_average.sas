/**********************************************************
combine all sas datasets in a given directory into one dataset
Andrew 2018 06

This is for DTAQ code
Instructions:
(1) check the scratch directory with many daily datasets
(2) Find an example date to work off of
(3) Enter example date in User section

**********************************************************/

proc datasets library=WORK kill; run; quit;
dm "out;clear;log;clear;"; /*clears output and log windows*/

/* USER 
go directory with files and use ls to find a good date
*/

libname have "/scratch/frb/ayc_dtaq";

%let goodfilename = dtaq_spreads_20181220;

%let dailyname   = '~/temp_output/dtaq daily.csv';
%let monthlyname = '~/temp_output/dtaq monthly.csv';



/*
** Push names of files to a dataset
** called 'contents' using proc 
** contents.
*/
proc contents data = have._all_ noprint out = contents (keep = memname);
run;

/* Eliminate any duplicate names of the SAS datasets */
proc sort data = contents nodupkey;
  by memname;
run;

/*
** Create 2 macro variables 
** 1. The names of each SAS dataset
** 2. The number of datasets in 'have'
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
;
data final; set have.&goodfilename; 
	where sym_root = "00";
run;

%macro combine;
  %do i = 1 %to &count;
  proc append base = final data = have.&&name&i force;
    run;
  %end;
%mend combine;

%combine;

/*
** Aggregate from daily to monthly
*/



* take monthly averages;
 proc sql noprint; create table monthly 
	as
     select distinct sym_root,
	     year(date)      as year,
	     month(date)     as month,
		 count(effectivespread_percent_ave) as eff_spread_n,
	     avg(effectivespread_percent_ave) as eff_spread_ave,
	     avg(effectivespread_percent_dw) as eff_spread_dw_ave,
	     avg(effectivespread_percent_sw) as eff_spread_sw_ave
     from final
     group by sym_root, year, month;
 quit;


/*
** Export the dataset to csv
*/


proc export data = final
  outfile = &dailyname
  dbms = csv
  replace;
run;


* export to csv;
proc export data = monthly
  outfile = &monthlyname
  dbms = csv
  replace;
run;

/*
summary stats to lst file
*/
proc univariate data = final;
    var effectivespread_percent_ave;
run;    

proc univariate data = monthly;
    var eff_spread_ave;
run;