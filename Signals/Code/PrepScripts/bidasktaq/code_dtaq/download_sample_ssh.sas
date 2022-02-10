/*
download a sample of millisecond taq data for testing code
Andrew 2018 06

made to test updates to daily_taq_chen.sas

seems like this is a no go.  Even one day of data is more than 50 gigs.
The quote data for one day is 55 gigs.  nbbo data is 16 gigs.
*/

libname project '/scratch/frb/ayc';


/* declare stuff */

	* small;
	*%let sample = sym_root in ('AAPL','IBM','BRK') and sym_suffix = ''
		and (("9:30:00.000000000"t) <= time_m <= ("16:00:00.000000000"t)); 

	* small sample in terms of time;
	%let sample = sym_suffix = ''
		and (("15:30:00.000000000"t) <= time_m <= ("15:31:00.000000000"t)); 

	* testing;
	*%let sample = sym_suffix = ''
		and (("9:00:00.000000000"t) <= time_m <= ("16:00:00.000000000"t)); 
	*%let sample = substrn(sym_root,1,4) = ('AAPL') and sym_suffix = ''
		and (("9:30:00.000000000"t) <= time_m <= ("16:00:00.000000000"t)); 


%let yyyymmdd = 20161207; * user: select day to download;
libname nbbo '/wrds/nyse/sasdata/taqms/nbbo';
libname cq '/wrds/nyse/sasdata/taqms/cq';
libname ct '/wrds/nyse/sasdata/taqms/ct';

/* testing
proc contents data = nbbo.nbbom_&yyyymmdd; run;
proc print data=nbbo.nbbom_&yyyymmdd (obs=200); 
	var sym_root time_m; 
	where (("15:59:59.999900000"t) <= time_m <= ("16:00:00.000000000"t)); 
run;

	* testing;
	endrsubmit;
*/


/* subset the data */
/* Retrieve NBBO data */
/* about 4 minutes for 1 day! */
data project.DailyNBBO (where = (&sample));

    * Enter NBBO file names in YYYYMMDD format for the dates you want;
    set nbbo.nbbom_&yyyymmdd;

    format date date9.;
    format time_m part_time trf_time TIME20.9;
run;

* Retrieve Quote data;
data project.DailyQuote (where = (&sample));
    set cq.cqm_&yyyymmdd;
    format date date9.;
    format time_m part_time trf_time TIME20.9;
run;

* Retrieve Trade data;
data project.DailyTrade (where = (&sample));
    set ct.ctm_&yyyymmdd;
    type='T';
    format date date9.;
    format time_m part_time trf_time TIME20.9;
run;
