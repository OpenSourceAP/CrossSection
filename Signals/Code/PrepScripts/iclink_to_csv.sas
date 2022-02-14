/* 
	wrapper script for wrds iclink macro
	Andrew Chen 2022 02
	
	created reorg from masterSAS.sas to master.sh

*/

* paths;
%include '/wrds/lib/utility/wrdslib.sas' ;
options sasautos=('/wrds/wrdsmacros/', SASAUTOS) MAUTOSOURCE;
%let path_dl_me = ~/data_prep/;

* run wrds macro;
%ICLINK (IBESID=IBES.ID,CRSPID=CRSP.STOCKNAMES,OUTSET=WORK.ICLINK);

* export to csv;
proc export data=ICLINK outfile="&path_dl_me.iclink.csv"
	dbms=csv replace;
run;
