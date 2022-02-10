* modified to work on DTAQ data
Andrew Chen 2018 07

taq changed to taqmsec
yymm6 changed to yymmdd8
;

/* ********************************************************************************* */
/* ******************** W R D S   R E S E A R C H   M A C R O S ******************** */
/* ********************************************************************************* */
/* WRDS Macro: TCLINK                                                                */
/* Summary   : Create TAQ-CRSP Link Table                                            */
/* Date      : September 20, 2010                                                    */
/* Author    : Rabih Moussawi, WRDS                                                  */
/* Variables : - BEGDATE and ENDDATE are Start and End Dates in YYYYMMDD format        */
/*             - OUTSET: TAQ-CRSP link table output dataset                          */
/* ********************************************************************************* */
 
%MACRO TCLINK (BEGDATE=20150101,ENDDATE=20200101,OUTSET=WORK.TCLINK);
 
/* Check Validity of TAQ Library Assignment */
* updated to use taqmsec - AC 2018 07;
%if (%sysfunc(libref(taqmsec))) %then %do; libname taq "/wrds/nyse/sasdata/"; %end;
%put; %put ### START . ; %put ;
/* IDEA: Use VINTAGE-SYMBOL as TAQ Primary Key */
/*       Then Link it to PERMNO using CUSIP and Ticker Info */
options nonotes;
%let date1= %sysfunc(inputn(&begdate,YYMMDD8.));
%let date2= %sysfunc(inputn(&enddate,YYMMDD8.));
 %if &date1<&date2 %then %let NMONTHS=%sysfunc(intck(MONTH,&date1,&date2));
  %else %let NMONTHS=0;
data _mast1; set _null_; run;
/* Begin Loop To Construct a 'Master' TAQ Master Dataset */
%do m=0 %to &NMONTHS;
%let date = %sysfunc(intnx(MONTH,&date1,&m,E));
%let yymmdd = %sysfunc(putn(&date,YYMMDD8));
/* Make Sure that dataset Exist */
* updated to use taqmsec, also note the date format change - AC 2018 07;
%if %sysfunc(exist(taqmsec.mast_&yymmdd))=1 %then
%do;
 %put ### Processing Master Dataset for &yymmdd ### ;

  * xxx debug;
  proc contents data = taqmsec.mast_&yymmdd; run;

 * read temporarily into _mastm and make some edits; 
 data _mastm; format DATE date9.;
 * updated to use taqmsec - AC 2018 07;
  set taqmsec.mast_&yymmdd; 
  date=&date;
  %if (&yymmdd>=199601 and &yymmdd<=199612) or (&yymmdd>=200407 and &yymmdd<=200412) %then
   %do;
    rename DATEF=FDATE;
    drop CUSIP8;
   %end;
 run;

 * add day of data to _mastm;
 %if &m=0 %then %do; data _mast1; set _mastm; run; %end;
  %else %do; proc append base=_mast1 data=_mastm force; run; %end;
 proc sql; drop table _mastm; quit;
%end;
/* End Loop */
%end;
 
/* Clean TAQ Master Dataset Information */
    * xxx debug;
    proc contents data = _mastm; run;
    proc contents data = _mast1; run;

data _mast2; format CUSIP8 $8.;
set _mast1 (keep=DATE FDATE CUSIP SYMBOL NAME SHROUT TYPE); * errors here;
CUSIP = strip(compress(CUSIP," ."));
if missing(FDATE) then fdate=date;
if not missing(CUSIP)  then CUSIP8=substr(CUSIP,1,8);
if missing(CUSIP) and missing(NAME) then delete;
run;
 
/* Sort Data using DATE-SYMBOL Key */
proc sort data=_mast2 nodupkey; by date symbol fdate cusip; run;
 
/* Step 1: Link by CUSIP */
/* CRSP: Get all PERMNO-NCUSIP combinations */
proc sql;
create table _msenames
as select distinct permno, ncusip, upcase(compbl(comnam)) as comnam
 from crsp.msenames where not missing(ncusip)
group by permno, ncusip
having nameendt=max(nameendt);
quit;
proc sort data=_msenames nodupkey; by permno ncusip; run;
 
/* Map TAQ and CRSP using 8-digit CUSIP */
proc sql;
create table _mast3
as select b.permno, a.*, b.comnam
from _mast2 as a left join _msenames as b
on a.cusip8=b.ncusip;
quit;
 
/* Step 2: Find links for the remaining unmatched cases using Exchange Ticker */
/* Identify Unmatched Cases by Splitting the Sample into Match1 and NoMap1 */
proc sort data=_mast3 nodupkey; by date symbol permno fdate; run;
data _Match1 _NoMap1;
set _mast3;
by date symbol permno fdate;
if last.symbol;
SCORE=(missing(permno));
NAMEDIS=min(spedis(name,comnam),spedis(comnam,name));
if not missing(permno) then output _match1;
else output _NoMap1;
run;
 
/* Add the Matches by Ticker */
data _NoMap2;
set _NoMap1;
where not missing(name);
symbol=strip(symbol);
name = upcase(compbl(name));
drop permno comnam score namedis;
run;
 
/* Get entire list of CRSP stocks with Exchange Ticker information */
/* Arrange effective dates for link by Exchange 'Trading' Ticker */
/* Use CRSP Ticker if Trading Ticker is missing */
data _CRSP1;
set crsp.msenames;
if not missing(tsymbol) then SMBL = tsymbol;
else SMBL=ticker;
smbl=strip(smbl);
if not missing(smbl);
COMNAM=upcase(compbl(comnam));
run;
 
/* Get date ranges for every permno-ticker combination */
proc sql;
  create table _CRSP2
  as select permno, smbl, comnam, 
              min(namedt)as namedt,max(nameendt) as nameenddt
  from _CRSP1
  where not missing (smbl)
  group by permno, smbl
  order by permno, smbl, namedt;
quit;
 
/* Label date range variables and keep only most recent company name */
data _CRSP3;
  set _CRSP2;
  by permno smbl;
  if  last.smbl;
  label namedt="Start date of exch. ticker record";
  label nameenddt="End date of exch. ticker record";
  format namedt nameenddt date9.;
run;
 
/* Get PERMNO for Unmatched Stocks using Ticker-DATE Match*/
proc sql;
create table _NoMap3
as select a.*, b.permno,comnam,
 min(spedis(a.name,b.comnam),spedis(b.comnam,a.name)) as NAMEDIS
from _NoMap2 as a, _CRSP3 as b
where strip(a.symbol)=strip(b.smbl) and a.date between namedt and nameenddt
order by date,symbol,namedis;
quit;
 
/* Assign all Ticker Matches a Lower Score than CUSIP Matches */
data _NoMap4;
set _NoMap3;
by date symbol;
if first.symbol;
SCORE=2;
run;
 
/* Score links using company name spelling distance: 0 is Best */
/* Consolidate Link Table */
data _TAQLINK1;
set _match1 _NoMap4(in=b);
SCORE=SCORE+(NAMEDIS>30);
label SCORE="0.CUSIP+Names, 1.CUSIP, 2.Ticker+Names, 3.Ticker Only";
label NAMEDIS="Spelling Distance between TAQ and CRSP Company Names";
label DATE="TAQ Vintage Date";
label CUSIP8='8-digit CUSIP';
label CUSIP ='Full CUSIP Number: 9-digit CUSIP + 3-digit NSCC Exchange ID';
rename CUSIP=CUSIP_FULL CUSIP8=CUSIP;
label SYMBOL="Stock Symbol in TAQ";
label NAME = "Company Name in TAQ";
label COMNAM = "Company Name in CRSP";
label FDATE = "Effective Date of Current TAQ Name Record";
run;
 
/* Some companies may have more than one TICKER-PERMNO link,         */
/* Can Clean the link additionally for one observation per permno-date */
/* Final Sort */
proc sort data=_TAQLINK1 out=&outset nodupkey; by date symbol; run;
 
/* House Cleaning */
proc sql;
 drop table _Mast1,_Mast2,_Mast3,_MSENames,_CRSP1,_CRSP2,_CRSP3,
  _Match1,_NoMap1,_NoMap2,_NoMap3,_NoMap4,_TAQLINK1;
quit;
 
%put; %put ### DONE . ; %put ;
options notes;
 
%MEND TCLINK;
 
/* ********************************************************************************* */
/* *************  Material Copyright Wharton Research Data Services  *************** */
/* ****************************** All Rights Reserved ****************************** */
/* ********************************************************************************* */


/* run macro to create tclink sas dataset 
  though the macro calls for up to 2017 12, the data is only available
  for up to 2014 12 (as of 2018 06)
*/

%TCLINK(BEGDATE=20150101,ENDDATE=20200101,OUTSET=tclink);

proc export data = tclink
  outfile = '~/test_output/tclink.csv'
  dbms = csv
  replace;
run;
