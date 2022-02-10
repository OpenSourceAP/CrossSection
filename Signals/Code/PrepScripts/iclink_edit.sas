/* ********************************************************************************* */
/* ******************** W R D S   R E S E A R C H   M A C R O S ******************** */
/* ********************************************************************************* */
/* WRDS Macro: ICLINK                                                                */
/* Summary   : Create IBES-CRSP Link Table                                           */
/* Date      : September 25, 2006                                                    */ 
/* Author    : Rabih Moussawi, WRDS                                                  */
/* Variables : - IBESID and CRSPID are IBES and CRSP Names Datasets                  */
/*             - OUTSET: IBES-CRSP link table output dataset                         */
/* ********************************************************************************* */
 
%MACRO ICLINK (IBESID=IBES.ID,CRSPID=CRSP.STOCKNAMES,OUTSET=WORK.ICLINK);
 
/* ********************************************************************************* */
/* FUNCTION: - Creates a link table between IBES TICKER and CRSP PERMNO              */
/*           - Scores links from 0 (best link) to 6                                  */
/* Possible IBES ID (names) file to use:                                             */
/*    Detail History: ID File                                                        */
/*    Summary History: IDSUM File                                                    */
/*    Recommendation Detail and Summary Statistics: RECDID and RECDIDSUM Files       */
/*                                                                                   */
/* INPUT: IBES and CRSP ID (or NAMES) Datasets, with historical identifiers list     */
/*       - IBES: IBES.ID, IBES.IDSUM, IBES.RECID, or IBES.RECIDSUM files             */
/*       - CRSP: CRSP.MSENAMES, CRSP.DSENAMES, or CRSP.STOCKNAMES files              */
/*                                                                                   */
/* OUTPUT: ICLINK set stored in prespecified directory                               */
/*       - SCORE variable: lower scores are better and high scores may need further  */
/*               checking before using them to link CRSP & IBES data.                */
/*               In computing the score, a CUSIP match is considered better than a   */
/*               TICKER match.  The score also includes a penalty for differences in */
/*               company names-- CNAME in IBES and COMNAM in CRSP. Name penalty is   */
/*               based upon SPEDIS, which is the spelling distance function in SAS.  */
/*               SPEDIS=0 is a perfect score and SPEDIS<30 is usually good           */
/*               enough to be considered a name match.                               */
/*               Note here that Exchange Ticker can also be used as Flag             */
/*          "SCORE" levels:                                                          */
/*               - 0: BEST match: using (cusip, cusip dates and company names)       */
/*                         or (exchange ticker, company names and 6-digit cusip)     */
/*               - 1: Cusips and cusip dates match but company names do not match    */
/*               - 2: Cusips and company names match but cusip dates do not match    */
/*               - 3: Cusips match but cusip dates and company names do not match    */
/*               - 4: tickers and 6-digit cusips match but comp names do not match   */
/*               - 5: tickers and names match but 6-digit cusips do not match        */
/*               - 6: tickers match but names and 6-digit cusips do not match        */
/* ********************************************************************************* */
 
options nonotes;
/* Check Validity of Library Assignments */
%if (%sysfunc(libref(crsp))) %then %do;
  %let cs=/wrds/crsp/sasdata/;
  libname crsp ("&cs/m_stock","&cs/q_stock","&cs/a_stock");
%end;
%if (%sysfunc(libref(ibes))) %then %do; libname ibes "/wrds/ibes/sasdata"; %end;
 
/* Name End Dates variable in MSENAMES and DSENAMES is different than STOCKNAMES */
%if %sysfunc(upcase(&CRSPID)) ne CRSP.STOCKNAMES %then %let condition = %str(RENAME=(nameendt=nameenddt));
%else %let condition = ;
 
%put ;
%put ### START. Creating IBES-CRSP Link Table: ICLINK ;
%put ## IBES NAMES (ID) Dataset Used:  &IBESID;
%put ## CRSP NAMES (ID) Dataset Used:  &CRSPID;
%put ## Step1: Linking using CUSIPs... ;
 
/* Step 1: Link by CUSIP */
/* IBES: Get the list of IBES TICKERS for US firms in IBES */
proc sort data=&IBESID out=_IBES1 (keep=ticker cusip CNAME sdates);
  where USFIRM=1 and not(missing(cusip));
  by ticker cusip sdates;
run;
 
/* Create first and last 'start dates' for CUSIP link */
proc sql;
  create table _IBES2
  as select *, min(sdates) as fdate, max(sdates) as ldate
  from _IBES1
  group by ticker, cusip
  order by ticker, cusip, sdates;
quit;
 
/* Label date range variables and keep only most recent company name for CUSIP link */
data _IBES2;
  set _IBES2;
  by ticker cusip;
  if last.cusip;
  label fdate="First Start date of CUSIP record";
  label ldate="Last Start date of CUSIP record";
  format fdate ldate date9.;
  drop sdates;
run;
 
/* CRSP: Get all PERMNO-NCUSIP combinations */
proc sort data=&CRSPID out=_CRSP1 (keep=PERMNO NCUSIP comnam name: &condition);
  where not missing(NCUSIP);
  by PERMNO NCUSIP namedt;
run;
 
/* Arrange effective dates for CUSIP link */
proc sql;
  create table _CRSP2
  as select PERMNO,NCUSIP,comnam,min(namedt)as namedt,max(nameenddt) as nameenddt
  from _CRSP1
  group by PERMNO, NCUSIP
  order by PERMNO, NCUSIP, NAMEDT;
quit;
 
/* Label date range variables and keep only most recent company name */
data _CRSP2;
  set _CRSP2;
  by permno ncusip;
  if last.ncusip;
  label namedt="Start date of CUSIP record";
  label nameenddt="End date of CUSIP record";
  format namedt nameenddt date9.;
run;
 
/* Create CUSIP Link Table */
/* CUSIP date ranges are only used in scoring as CUSIPs are not reused for
    different companies overtime */
proc sql;
  create table _LINK1_1
  as select *
  from _IBES2 as a, _CRSP2 as b
  where a.CUSIP = b.NCUSIP
  order by TICKER, PERMNO, ldate;
quit;
 
/* Score links using CUSIP date range and company name spelling distance */
/* Idea: date ranges the same cusip was used in CRSP and IBES should intersect */
data _LINK1_2;
  set _LINK1_1;
  by TICKER PERMNO;
  if last.permno; /* Keep link with most recent company name */
  name_dist = min(spedis(cname,comnam),spedis(comnam,cname));
  if (not ((ldate < namedt) or (fdate > nameenddt))) and name_dist < 30 then SCORE = 0;
    else if (not ((ldate < namedt) or (fdate > nameenddt))) then score = 1;
        else if name_dist < 30 then SCORE = 2;
      else SCORE = 3;
  keep TICKER PERMNO cname comnam score;
run;
 
%put ## Step2: Linking using TICKERs... ;
/* Step 2: Find links for the remaining unmatched cases using Exchange Ticker */
/* Identify remaining unmatched cases */
proc sql;
  create table _NOMATCH1
  as select distinct a.*
  from _IBES1 (keep=ticker) as a
  where a.ticker NOT in (select ticker from _LINK1_2)
  order by a.ticker;
quit;
 
/* Drop Step1 Tables*/
proc sql; drop table _IBES1,_IBES2,_CRSP1,_CRSP2; quit;
 
/* Add IBES identifying information */
proc sql;
  create table _NOMATCH2
  as select b.ticker, b.CNAME, b.OFTIC, b.sdates, b.cusip
  from _NOMATCH1 as a, &IBESID as b
  where a.ticker = b.ticker and not (missing(b.OFTIC))
  order by ticker, oftic, sdates;
quit; 
 
/* Create first and last 'start dates' for Exchange Tickers */
proc sql;
  create table _NOMATCH3
  as select *, min(sdates) as fdate, max(sdates) as ldate
  from _NOMATCH2
  group by ticker, oftic
  order by ticker, oftic, sdates;
quit;
 
/* Label date range variables and keep only most recent company name */
data _NOMATCH3;
  set _NOMATCH3;
  by ticker oftic;
  if last.oftic;
  label fdate="First Start date of OFTIC record";
  label ldate="Last Start date of OFTIC record";
  format fdate ldate date9.;
  drop sdates;
run;
 
/* Get entire list of CRSP stocks with Exchange Ticker information */
proc sort data=&CRSPID out=_CRSP1 (keep=ticker comnam permno ncusip name: &condition);
  where not missing(ticker);
  by permno ticker namedt;
run;
 
/* Arrange effective dates for link by Exchange Ticker */
proc sql;
  create table _CRSP2
  as select permno,comnam,ticker as crsp_ticker,ncusip,
              min(namedt)as namedt,max(nameenddt) as nameenddt
  from _CRSP1
  group by permno, ticker
  order by permno, crsp_ticker, namedt;
quit;
/* CRSP exchange ticker renamed to crsp_ticker to avoid confusion with IBES TICKER */
 
/* Label date range variables and keep only most recent company name */
data _CRSP2;
  set _CRSP2;
  by permno crsp_ticker;
  if  last.crsp_ticker;
  label namedt="Start date of exch. ticker record";
  label nameenddt="End date of exch. ticker record";
  format namedt nameenddt date9.;
run;
 
/* Merge remaining unmatched cases using Exchange Ticker */
/* Note: Use ticker date ranges as exchange tickers are reused overtime */
proc sql;
  create table _LINK2_1
  as select a.ticker,a.oftic, b.permno, a.cname, b.comnam, a.cusip, b.ncusip, a.ldate
  from _NOMATCH3 as a, _CRSP2 as b
  where a.oftic = b.crsp_ticker and
     (ldate>=namedt) and (fdate<=nameenddt)
  order by ticker, oftic, ldate;
quit;
 
/* Score using company name using 6-digit CUSIP and company name spelling distance */
data _LINK2_2;
  set _LINK2_1;
  name_dist = min(spedis(cname,comnam),spedis(comnam,cname));
  if substr(cusip,1,6)=substr(ncusip,1,6) and name_dist < 30 then SCORE=0;
  else if substr(cusip,1,6)=substr(ncusip,1,6) then score = 4;
  else if name_dist < 30 then SCORE = 5;
      else SCORE = 6;
run;
 
/* Some companies may have more than one TICKER-PERMNO link,         */
/* so re-sort and keep the case (PERMNO & Company name from CRSP)    */
/* that gives the lowest score for each IBES TICKER (first.ticker=1) */
proc sort data=_LINK2_2; by ticker score; run;
data _LINK2_3;
  set _LINK2_2;
  by ticker score;
  if first.ticker;
  keep ticker permno cname comnam permno score;
run;
 
%put ## Step3: Finalizing Links and Scores... ;
/* Step 3: Add Exchange Ticker links to CUSIP links      */
/* Create Labels for ICLINK dataset and variables        */
/* Create final link table and save it in prespecified directory */
data &OUTSET (label="IBES-CRSP Link Table");
  set _LINK1_2 _LINK2_3;
label CNAME = "Company Name in IBES";
label COMNAM= "Company Name in CRSP";
label SCORE= "Link Score: 0(best) - 6";
run;
 
/* Final Sort */
proc sort data=&OUTSET; by TICKER SCORE PERMNO; run;
 
%put ## Step4: Link Table &OUTSET Ready... ;
/* House Cleaning */
proc sql;
drop table _CRSP1,_CRSP2,
           _LINK1_1,_LINK1_2,_LINK2_1,_LINK2_2,_LINK2_3,
           _NOMATCH1,_NOMATCH2,_NOMATCH3;
quit;
%put ### DONE . ; %put ;
options notes;
%MEND ICLINK;
 
/* ********************************************************************************* */
/* *************  Material Copyright Wharton Research Data Services  *************** */
/* ****************************** All Rights Reserved ****************************** */
/* ********************************************************************************* */

