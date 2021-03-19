*
runs all sas predictor files.  Created 2020 11, Andrew Chen 
You might want to comment out everthing except for the IBES CRSP link,
since the 13F and Corwin Schultz code only applies to a few signals
but they're time consuming.

Thanks to Luis Palacios, Rabih Moussawi, and Denys Glushkov for the 13F code
and thanks to Shane Corwin and Paul Schultz for their code.

Instructions: 
	- ssh into wrds
	- create folders ~/SAS/ and ~/data_sas/
	- upload sas files to masterSAS.sas
	- run "qsas masterSAS.sas"
	- download ~/data_sas/ to $pathProject/Signals/Data/Prep/ using, say, WinSCP
;

* clear output and windows;
dm "out;clear;log;clear;"; 
proc datasets lib=work nolist kill; quit; run;

* PATHS;
%let path_dl_me = ~/data_sas/;
libname dl_me "~/data_sas/";

* (1) DOWNLOAD IBES CRSP LINK (this is fast.  ICLINK is kept on WRDS server);
%let iclink_name = &path_dl_me.iclink.csv;
%ICLINK (IBESID=IBES.ID,CRSPID=CRSP.STOCKNAMES,OUTSET=WORK.ICLINK);
proc export data=ICLINK outfile="&iclink_name"
	dbms=csv replace;
run;

* (2) DOWNLOAD 13F (takes maybe 2-3 minutes) ;
%let _13f_name = &path_dl_me.tr_13f.csv;
%include "tr13f_pmg_edit.sas";
proc export data=tr_13f_stock2 outfile="&_13f_name"
	dbms=csv replace; 
run;


* (3) DOWNLOAD Corwin Schultz Spread (maybe 10 minutes);
%let cs_name = &path_dl_me.corwin_schultz_spread.csv;
%include "Corwin_Schultz_Edit.sas";
proc export data=hlfinal outfile="&cs_name"
	dbms=csv replace; 
run;

*/