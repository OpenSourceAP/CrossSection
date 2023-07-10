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
* %OCLINK (IBESID=IBES.ID,CRSPID=CRSP.STOCKNAMES,OUTSET=WORK.OCLINK);
%OCLINK (OPTIONMID=OPTIONM.SECNMD,CRSPID=CRSP.MSENAMES,OUTSET=WORK.OCLINK);

* export to csv;
proc export data=OCLINK outfile="&path_dl_me.oclink.csv"
	dbms=csv replace;
run;
