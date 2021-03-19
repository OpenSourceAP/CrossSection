
/* ********************************************************************************* */
/* ************** W R D S   R E S E A R C H   A P P L I C A T I O N S ************** */
/* ********************************************************************************* */
/* Summary   : Calculate Institutional Ownership, Concentration, and Breadth Ratios  */
/* Date      : May 18, 2009                                                          */
/* Author    : Luis Palacios, Rabih Moussawi, and Denys Glushkov                     */
/* Variables : - INPUT : Thomson-Reuters 13F Data (TR-13F) S34TYPE3 Holdings data    */
/*                       S34TYPE1 data for FDATE and RDATE variables                 */
/*             - OUTPUT: IO_TimeSeries dataset with IO variables for common stocks   */
/* ********************************************************************************* */
 
libname tfn "/wrds/tfn/sasdata/s34";
 
/* Step1. Specifying Options */
/* Select Date Ranges for CRSP and Thomson Data                   */
%let begdate = 01JAN1979;
%let enddate = 31DEC2110;
/* Create a CRSP Subsample with Monthly Stock and Event Variables */
/* Restriction on the type of shares (common stocks only)         */
%let sfilter = (shrcd in (10,11));
/* Selected variables from the CRSP monthly data file (crsp.msf)  */
%let msfvars = prc ret shrout cfacpr cfacshr;
/* Selected variables from the CRSP monthly event file (crsp.mse) */
%let msevars = ncusip exchcd shrcd ;
/* This procedure creates a Monthly CRSP dataset named "CRSP_M"   */
%crspmerge(s=m,start=&begdate,end=&enddate,sfvars=&msfvars,sevars=&msevars,filters=&sfilter);
 

/* Adjust Share and Price in Monthly Data              */
/* and Since Thomson 13-F is Quarterly (FDATE & RDATE) */
/* Align CRSP month-end Dates and keep Quarter Ends    */
data crsp_m; format QDATE date9.;
set crsp_m;
QDATE = INTNX('QTR',date,0,'E');
DATE = INTNX("MONTH",date,0,"E");
P = abs(prc)/cfacpr;
TSO=shrout*cfacshr*1000;
if TSO<=0 then TSO=.;
ME = P*TSO/1000000;
label P = "Price at Period End, Adjusted";
label TSO = "Total Shares Outstanding, Adjusted";
label ME = "Market Capitalization, x$1m";
drop ncusip prc cfacpr shrout exchcd shrcd ret;
format ret percentn8.4 ME P dollar12.3 TSO comma12.;
run;
 
/* Keep Last Monthly Observation for Each quarter */
data crsp_m;
set crsp_m;
by permno qdate date;
if last.qdate;
drop date;
run;
 
/* Step2. Merge TR-13f S34type1 and S34type3 Sets */
/* First, Keep First Vintage with Holdings Data for Each RDATE-MGRNO Combinations */
proc sql;
create table First_Vint
as select distinct rdate, fdate, mgrno, mgrname
from tfn.s34type1
group by mgrno, rdate
having fdate=min(fdate)
order by mgrno, rdate;
quit;
 
/* Marker for First and Last Quarters of Reporting & Reporting Gaps                        */
/* Exercise Helpful Mostly For Clean Time-Series Analysis                                  */
data First_Vint;
set First_Vint;
by mgrno rdate;
length First_Report 3;
First_Report = (first.mgrno or intck("QTR",lag(rdate),rdate)>1);
run;
 
/* Last Report by Institutional Manager, or Missing 13F Reports in the Next Quarter(s) */
proc sort data=First_Vint nodupkey; by mgrno descending rdate; run;
data First_Vint;
set First_Vint;
by mgrno descending rdate;
length Last_Report 3;
Last_Report = (first.mgrno or intck("QTR",rdate,lag(rdate))>1);
if ("&begdate"d <= rdate <="&enddate"d);
run;
 
/* Add Total Number of 13F Filers During Each Quarter       */
/* undo_policy=none is used to suppress the warning message */
proc sql undo_policy=none;
create table First_Vint
as select distinct *, count(mgrno) as NumInst
from First_Vint
group by rdate
order by fdate, mgrno;
quit;
 
/* Step3. Extract Holdings and Adjust Shares Held */
/* FDATE -Vintage Date- is used in Shares' Adjustment */
data Holdings_v1 / view=Holdings_v1;
merge First_Vint(in=a drop=mgrname)
  tfn.s34type3(in=b drop=type sole shared no);
by fdate mgrno;
if a and b and shares>0;
run;
 
/* Map TR-13F's Historical CUSIP to CRSP Unique Identifier PERMNO */
/* Keep Securities in CRSP Common Stock Universe */
proc sql;
create view Holdings_v2 as
select distinct a.rdate, a.fdate, a.mgrno, a.NumInst,
        a.first_report, a.last_report, b.permno, a.shares
from Holdings_v1 as a,
   (select distinct ncusip, permno from crsp.msenames
    where not missing(ncusip)) as b
    where a.cusip=b.ncusip;
quit;
 
/* Step4. Adjust Shares using CRSP Adjustment Factors aligned at Vintage Dates */
proc sql;
create table Holdings as
select distinct a.rdate, a.mgrno, a.NumInst, a.first_report, a.last_report,
      a.permno, a.shares*b.cfacshr as shares_adj label = "Adjusted Shares Held"
from Holdings_v2 as a, crsp_m as b
where a.permno=b.permno and a.fdate = b.qdate;
quit;
 
/* Sanity Checks for Duplicates - Ultimately, Should be 0 Duplicates */
/* If No Errors, then Duplicates can be due to 2 historical CUSIPs   */
/*    (Separate Holdings by Same Manager) mapping to the same permno */
proc sort data=Holdings nodupkey; by permno rdate mgrno; run;
proc sort data=crsp_m   nodupkey; by permno qdate;       run;
 
/* Step5. Calculate Institutional Measures at the Security Level */
proc means data=Holdings noprint;
where shares_adj>0;
by permno rdate;
var shares_adj first_report;
output out=IO_Metrics (drop=_freq_ _type_)
       n=NumOwners max(NumInst)=NumInst
       sum(first_report)=NewInst sum(last_report)=OldInst
       sum(shares_adj)=IO_TOTAL USS(shares_adj)=IO_SS;
run;
 
/* Changes in Institutional Breadth: Lehavy and Sloan (2008) Calculation               */
/* DBREADTH Condition: institutions should exist in Q(t) & Q(t-1)                      */
/* Objective: Mitigate Bias due to Universe Changes - $100M AUM Filing Threshold       */
/* DBREADTH=((NumInst(t)-NewInst(t))-(Numinst(t-1)-OldInst(t-1)) divided by            */
/*                  Total Number of 13F filers in quarter (t-1))                       */
/*  where,                                                                             */
/*  . NewInst(t): Number of 13F filers that reported in t, but did not report in (t-1) */
/*  . OldInst(t): Number of 13F filers that reported in (t-1), but did not report in t */
/*  . (NumOwners(t)-NewInst(t)): Number of 13F filers holding security in quarter t,   */
/*                  that have reported in both quarters t and t-1                      */
/*  . (NumOwners(t-1)-OldInst(t-1)): number of 13F filers that held the security       */
/*                  in quarter (t-1), and have reported in both quarters t and t-1     */
/*                                                                                     */
/* Calculate IO DBreadth and Concentration Metrics                                     */
data IO_Metrics;
set IO_Metrics;
by permno rdate;
IOC_HHI = IO_SS/(IO_TOTAL**2);
DBREADTH = ( (NumOwners - NewInst) - lag(NumOwners-OldInst) ) / lag(NumInst);
if first.permno then DBREADTH=.;
label NumOwners  = "Breadth - # of 13-F Institutional Owners";
label IO_TOTAL = "Institutional Ownership, Total - Adjusted";
label IOC_HHI   = "IO Concentration - Herfindahl- Hirschman Index";
label DBREADTH = "Change in IO Breadth, Percent";
drop NumInst IO_SS NewInst OldInst;
run;
 
/* Step6. Add CRSP Market Data to Holdings at Calendar Quarter Ends */
/* Note: a Right Join is Necessary to Identify Common Stock with no 13F Data */
data IO_TimeSeries;
merge IO_Metrics(in=a) crsp_m (in=b rename=(qdate=rdate));
by permno rdate;
if b and TSO>0;
IOR = IO_TOTAL/TSO;
if missing(IOR) then IOR=0;
IO_MISSING = (not a);
IO_G1      = (IOR>1);
label IOR = "Institutional Ownership Ratio";
label IO_MISSING = "Missing (or NA) 13-F Data";
label IO_G1 = "IOR % > 1";
drop CFACSHR;
format IO_TOTAL NumOwners comma16. IOR DBREADTH IOC_HHI percentn8.2;
run;
 

/* ========== END STUFF FROM PALACIOS ET AL =========== */





/* ac1: create instbasic: select data we need and reformat*/


data instbasic; set IO_Timeseries;
	keep permno rdate ior numowners dbreadth;
	ior = ior*100;
	dbreadth = dbreadth*100;
	label ior = "Inst Shares / Total Shares (%)";
	label NumOwners  = "# of Institutional Owners (Breadth)";
	format dbreadth ior 6.3;
	rename 	ior = instown_perc
			numowners = numinstown;
run;




/* ac2: create activism: shareholder activism stuff */


* find mgr_pct;
proc sql;
create table temphold as
select a.permno, a.mgrno, a.rdate, a.shares_adj, b.tso
	,a.shares_adj/b.tso*100 as mgr_pct
from holdings as a left join crsp_m as b
on a.permno=b.permno and a.rdate = b.qdate;
quit;

data temphold; set temphold;
	blockholder = 0;
	if mgr_pct > 5 then blockholder = 1;
run;

* average across mgrs to find maxinstown_perc and numinstblock;
proc means data=temphold noprint;
by permno rdate;
var mgr_pct blockholder;
output out=activism (drop=_freq_ _type_)
       max(mgr_pct)=maxinstown_perc
       sum(blockholder)=numinstblock;
run;


/* ac3: merge activism and instbasic and download*/

proc sql; create table tr_13f_stock as
	select a.*, b.*
	from instbasic as a full outer join activism as b
	on a.permno = b.permno and a.rdate = b.rdate;
quit;
proc download data=tr_13f_stock out=tr_13f_stock; run;



/* ac4: clean up and export as csv */
data tr_13f_stock2;
	set tr_13f_stock;
	if missing(numinstown) then delete;
run;
proc sort data = tr_13f_stock2; by permno rdate; run;



