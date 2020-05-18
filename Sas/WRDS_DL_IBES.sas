/*
Downloads IBES data from wrds into csv format.

-Andrew 2017 06


*/

dm "out;clear;log;clear;"; /*clears output and log windows*/
proc datasets lib=work nolist kill; quit; run;

********************************

	log on to wrds to get data

********************************;

%let wrds = wrds.wharton.upenn.edu 4016;
signon wrds username = _prompt_;

***;
%let wrds=wrds.wharton.upenn.edu 4016;options comamid=TCP remote=WRDS;
	signon username=_prompt_; 


rsubmit;
%ICLINK (IBESID=IBES.ID,CRSPID=CRSP.STOCKNAMES,OUTSET=WORK.ICLINK);
proc download data=ICLINK out=ICLINK; run;
endrsubmit;



proc export data=ICLINK outfile="b:\anomalies.com\rawdata_fed\iclink.csv"
	dbms=csv;
run;
