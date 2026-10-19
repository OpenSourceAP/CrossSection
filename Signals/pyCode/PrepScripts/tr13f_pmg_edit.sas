/* Minor edit of Palacios, Moussawi, and Glushkov code to output to CSV.
Andrew Chen 2022; CRSP inputs migrated to native CIZ in 2026.
Ownership uses one explicit vintage/report split-factor ratio per manager.

Run on WRDS from the prep directory, with data_for_dl/ and log/ present:
    sas tr13f_pmg_edit.sas -log log/tr13f_pmg_edit.log
Inputs: crsp.msf_v2, crsp.stksecurityinfohist, tfn.s34type1, tfn.s34type3.
Output: ./data_for_dl/tr_13f.csv, quarterly institutional ownership measures.
*/

* paths;
%include '/wrds/lib/utility/wrdslib.sas' ;
options sasautos=('/wrds/wrdsmacros/', SASAUTOS) MAUTOSOURCE;
%let path_dl_me = ./data_for_dl/;


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

/* First vintage for each manager/report, also supplying the needed date pairs. */
proc sql;
create table First_Vint
as select distinct rdate, fdate, mgrno, mgrname
from tfn.s34type1
group by mgrno, rdate
having fdate=min(fdate)
order by mgrno, rdate;
quit;

/* ===== Cumulative-factor inputs and conversion to split adjustments ===== */
/* CIZ classifications corresponding to legacy shrcd in (10,11). */
/* Align monthly dates to calendar quarter ends; raw shrout is in thousands. */
data crsp_m;
set crsp.msf_v2 (keep=permno mthcaldt shrout mthcumfacshr
    sharetype securitytype securitysubtype usincflg issuertype);
where "&begdate"d <= mthcaldt <= "&enddate"d
    and sharetype='NS' and securitytype='EQTY' and securitysubtype='COM'
    and usincflg='Y' and issuertype in ('ACOR','CORP');
DATE = INTNX('MONTH',mthcaldt,0,'E');
QDATE = INTNX('QTR',date,0,'E');
stock_eligible = (shrout>0);
keep permno date qdate shrout stock_eligible mthcumfacshr;
format DATE QDATE date9.;
run;
 
/* Sort explicitly; reject duplicate months before selecting one row per quarter. */
proc sort data=crsp_m; by permno qdate date; run;
data crsp_m;
set crsp_m;
by permno qdate date;
if not (first.date and last.date) then do;
    put 'ERROR: Duplicate CRSP security-month key.' permno= date=date9.;
    abort abend;
end;
/* Keep the last eligible month, including securities that end before quarter end. */
if last.qdate;
drop date;
run;
 
/* Only actual report/vintage date pairs are needed, not every quarter pair. */
proc sql;
create table split_adjustments as
select vintage.permno, dates.rdate, dates.fdate, report.shrout,
       vintage.mthcumfacshr as vintage_cfacshr,
       report.mthcumfacshr as report_cfacshr
from (select distinct rdate, fdate from First_Vint
      where "&begdate"d <= rdate <= "&enddate"d) as dates
inner join crsp_m as vintage on dates.fdate=vintage.qdate
left join crsp_m as report
  on vintage.permno=report.permno and dates.rdate=report.qdate;
quit;

data split_adjustments;
set split_adjustments;
/* Positive vintage holdings remain breadth-eligible even without a denominator.
   Positivity is unchanged by any common positive future normalization. */
breadth_eligible = (vintage_cfacshr>0);
split_adj = .;
/* A common positive future normalization cancels in this factor ratio. */
if report_cfacshr then
    split_adj = vintage_cfacshr / report_cfacshr;
keep permno rdate fdate shrout split_adj breadth_eligible;
run;

/* No cumulative factors are carried into the holdings or ownership calculations. */
data crsp_m;
set crsp_m(keep=permno qdate shrout stock_eligible);
run;
/* ===== End cumulative-factor block ===== */

/* Step2. Mark First/Last Reports and Reporting Gaps */
 
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
 
/* Step3. Extract Holdings and Map Securities */
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
   (select distinct cusip, permno from crsp.stksecurityinfohist
    where not missing(cusip)) as b
    where a.cusip=b.cusip;
quit;
 
/* Step4. Apply the Precomputed Split Adjustment to Manager Ownership */
proc sql;
create table Holdings as
select distinct a.rdate, a.mgrno, a.NumInst, a.first_report, a.last_report,
      a.permno, a.shares*adj.split_adj as _dedup_order,
      a.fdate, a.shares, adj.shrout, adj.split_adj, adj.breadth_eligible
from Holdings_v2 as a inner join split_adjustments as adj
  on a.permno=adj.permno and a.rdate=adj.rdate and a.fdate=adj.fdate
/* With a positive report factor, the ratio preserves adjusted-share ordering.
   Sort ineligible holdings first even when the report denominator is missing. */
order by a.rdate, a.mgrno, a.NumInst, a.first_report, a.last_report,
         a.permno, adj.breadth_eligible, _dedup_order;
quit;
 
/* Sanity Checks for Duplicates - Ultimately, Should be 0 Duplicates */
/* If No Errors, then Duplicates can be due to 2 historical CUSIPs   */
/*    (Separate Holdings by Same Manager) mapping to the same permno */
proc sort data=Holdings nodupkey; by permno rdate mgrno; run;
/* crsp_m is already sorted and has one row per permno/qdate. */

data Holdings;
set Holdings;
mgr_pct = .;
if shrout>0 then
    mgr_pct = 100 * shares / (1000 * shrout) * split_adj;
/* Retain raw holdings and the split adjustment for diagnostics. */
drop _dedup_order shrout;
run;
 
/* Step5. Calculate Institutional Measures at the Security Level */
proc means data=Holdings noprint;
where breadth_eligible;
by permno rdate;
var mgr_pct first_report;
output out=IO_Metrics (drop=_freq_ _type_)
       n(first_report)=NumOwners max(NumInst)=NumInst
       sum(first_report)=NewInst sum(last_report)=OldInst
       sum(mgr_pct)=instown_perc;
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
/* Calculate the change in institutional breadth. */
data IO_Metrics;
set IO_Metrics;
by permno rdate;
DBREADTH = ( (NumOwners - NewInst) - lag(NumOwners-OldInst) ) / lag(NumInst);
if first.permno then DBREADTH=.;
label NumOwners  = "Breadth - # of 13-F Institutional Owners";
label DBREADTH = "Change in IO Breadth, Percent";
drop NumInst NewInst OldInst;
run;
 
/* Step6. Add CRSP Market Data to Holdings at Calendar Quarter Ends */
/* Note: a Right Join is Necessary to Identify Common Stock with no 13F Data */
data IO_TimeSeries;
merge IO_Metrics(in=a) crsp_m (in=b rename=(qdate=rdate));
by permno rdate;
if b and stock_eligible;
if missing(instown_perc) then instown_perc=0;
drop shrout stock_eligible;
format NumOwners comma16. DBREADTH percentn8.2;
run;
 

/* ========== END STUFF FROM PALACIOS ET AL =========== */





/* ac1: create instbasic: select data we need and reformat*/


data instbasic;
    /* Preserve the seven-column CSV order and original identifier case. */
    retain PERMNO rdate NumOwners DBREADTH instown_perc;
    set IO_Timeseries;
	keep permno rdate instown_perc numowners dbreadth;
	dbreadth = dbreadth*100;
	label instown_perc = "Inst Shares / Total Shares (%)";
	label NumOwners  = "# of Institutional Owners (Breadth)";
	format dbreadth instown_perc 6.3;
	rename numowners = numinstown;
run;




/* ac2: create activism: shareholder activism stuff */


/* Activism uses every retained holding, including zero/missing percentages. */
data temphold;
    set Holdings(keep=permno mgrno rdate mgr_pct);
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
	/* Match the date parser in InstitutionalHoldings13F.py. */
	format rdate date9.;
run;
proc sort data = tr_13f_stock2; by permno rdate; run;




/* export as csv */
proc export data=tr_13f_stock2 outfile="&path_dl_me.tr_13f.csv"
	dbms=csv replace; 
run;

