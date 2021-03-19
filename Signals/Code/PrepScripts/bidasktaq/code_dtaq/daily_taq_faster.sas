/* 
faster version of Holden and Jacobsen's Daily TAQ code.  Should be 
about twice as fast.

Based off 2018 03 16 version of HJ's Daily TAQ code.

internal notes:
made from daily_taq_local.sas
Andrew 2018 06

Update 2018 10 15: 
    fixed quote screen to allow 9:00-9:30 am
    removed spreads > 0.40

*/




/* User and environment */
%let yyyymmdd = %sysget(yyyymmdd); * get day from command line;
libname output '/scratch/frb/ayc_dtaq/'; * output path;
%let _timer_start = %sysfunc(datetime());

/* declare stuff */



/* STEP 1: RETRIEVE DAILY TRADE AND QUOTE (DTAQ) FILES 
*/
    
libname nbbo '/wrds/nyse/sasdata/taqms/nbbo';
libname cq '/wrds/nyse/sasdata/taqms/cq';
libname ct '/wrds/nyse/sasdata/taqms/ct';

* formerly DailyTrade 
I put this first since it's fastest.
;
data trade2; 
    set ct.ctm_&yyyymmdd;

	*STEP 6: CLEAN DAILY TRADES DATA - DELETE ABNORMAL TRADES;
    where Tr_Corr eq '00' 
        and price gt 0
        and sym_suffix = '' 
        and (("9:30:00.000000000"t) <= time_m <= ("16:00:00.000000000"t));

	drop Tr_Corr Tr_Source TR_RF Part_Time RRN TRF_Time Tr_SCond 
         Tr_StopInd;

    * define type variable for use when 
    merging with nbbo;
    type='T';
run;    


    
data NBBO2;
    set nbbo.nbbom_&yyyymmdd;

    /* Quote Condition must be normal (i.e., A,B,H,O,R,W) */
    if Qu_Cond not in ('A','B','H','O','R','W') then delete;

	/* If canceled then delete */
    if Qu_Cancel='B' then delete;

	/* if both ask and bid are set to 0 or . then delete */
    if Best_Ask le 0 and Best_Bid le 0 then delete;
    if Best_Asksiz le 0 and Best_Bidsiz le 0 then delete;
    if Best_Ask = . and Best_Bid = . then delete;
    if Best_Asksiz = . and Best_Bidsiz = . then delete;

	/* Create spread and midpoint */
    Spread=Best_Ask-Best_Bid;
    Midpoint=(Best_Ask+Best_Bid)/2;

	/* If size/price = 0 or . then price/size is set to . */
    if Best_Ask le 0 then do;
        Best_Ask=.;
        Best_Asksiz=.;
    end;
    if Best_Ask=. then Best_Asksiz=.;
    if Best_Asksiz le 0 then do;
        Best_Ask=.;
        Best_Asksiz=.;
    end;
    if Best_Asksiz=. then Best_Ask=.;
    if Best_Bid le 0 then do;
        Best_Bid=.;
        Best_Bidsiz=.;
    end;
    if Best_Bid=. then Best_Bidsiz=.;
    if Best_Bidsiz le 0 then do;
        Best_Bid=.;
        Best_Bidsiz=.;
    end;
    if Best_Bidsiz=. then Best_Bid=.;

	/*	Bid/Ask size are in round lots, replace with new shares variable*/
	Best_BidSizeShares = Best_BidSiz * 100;
	Best_AskSizeShares = Best_AskSiz * 100;
run;


* formerly called DailyQuote;
data quoteAB2;
    set cq.cqm_&yyyymmdd;

	*STEP 5: CLEAN DTAQ QUOTES DATA;

    /* Create spread and midpoint*/;
    Spread=Ask-Bid;

	/* Delete if abnormal quote conditions */
    if Qu_Cond not in ('A','B','H','O','R','W')then delete; 

	/* Delete if abnormal crossed markets */
    if Bid>Ask then delete;

	/* Delete abnormal spreads*/
    if Spread>5 then delete;

	/* Delete withdrawn Quotes. This is 
	   when an exchange temporarily has no quote, as indicated by quotes 
	   with price or depth fields containing values less than or equal to 0 
	   or equal to '.'. See discussion in Holden and Jacobsen (2014), 
	   page 11. */
    if Ask le 0 or Ask =. then delete;
    if Asksiz le 0 or Asksiz =. then delete;
    if Bid le 0 or Bid =. then delete;
    if Bidsiz le 0 or Bidsiz =. then delete;
	drop Bidex Askex Qu_Cancel RPI SSR LULD_BBO_CQS 
         LULD_BBO_UTP FINRA_ADF_MPID SIP_Message_ID Part_Time RRN TRF_Time 
         Spread NATL_BBO_LULD;

	
	* prepare for matching with nbbo;
	rename Ask=Best_Ask; 
	rename Bid=Best_Bid;
    
    where ((Qu_Source = "C" and NatBBO_Ind='1') or (Qu_Source = "N" and NatBBO_Ind='4'))
       and sym_suffix = ''
       and (("9:00:00.000000000"t) <= time_m <= ("16:00:00.000000000"t));
    keep date time_m sym_root sym_suffix Qu_SeqNum Bid Best_BidSizeShares Ask 
         Best_AskSizeShares;

	/*	Bid/Ask size are in round lots, replace with new shares variable
	and rename Best_BidSizeShares and Best_AskSizeShares*/
	Best_BidSizeShares = Bidsiz * 100;
	Best_AskSizeShares = Asksiz * 100;
run;


/* STEP 3: GET PREVIOUS MIDPOINT */

proc sort 
    data=NBBO2 (drop = Best_BidSiz Best_AskSiz);
    by sym_root date;
run; 

data NBBO2;

	* find lagged midpoints?;
    set NBBO2;
    by sym_root date;
    lmid=lag(Midpoint);
    if first.sym_root or first.date then lmid=.;
    lm25=lmid-2.5;
    lp25=lmid+2.5;

 	*If the quoted spread is greater than $5.00 and the bid (ask) price is less
   (greater) than the previous midpoint - $2.50 (previous midpoint + $2.50), 
   then the bid (ask) is not considered. ;
    if Spread gt 5 and Best_Bid lt lm25 then do;
        Best_Bid=.;
        Best_BidSizeShares=.;
    end;
    if Spread gt 5 and Best_Ask gt lp25 then do;
        Best_Ask=.;
        Best_AskSizeShares=.;
    end;
	keep date time_m sym_root Best_Bidex Best_Bid Best_BidSizeShares 
         Best_Askex Best_Ask Best_AskSizeShares Qu_SeqNum;

	*STEP 4: OUTPUT NEW NBBO RECORDS - IDENTIFY CHANGES IN NBBO RECORDS 
   (CHANGES IN PRICE AND/OR DEPTH);
    if sym_root ne lag(sym_root) 
       or date ne lag(date) 
       or Best_Ask ne lag(Best_Ask) 
       or Best_Bid ne lag(Best_Bid) 
       or Best_AskSizeShares ne lag(Best_AskSizeShares) 
       or Best_BidSizeShares ne lag(Best_BidSizeShares); 
run;




/* STEP 7: THE NBBO FILE IS INCOMPLETE BY ITSELF (IF A SINGLE EXCHANGE 
   HAS THE BEST BID AND OFFER, THE QUOTE IS INCLUDED IN THE QUOTES FILE, BUT 
   NOT THE NBBO FILE). TO CREATE THE COMPLETE OFFICIAL NBBO, WE NEED TO 
   MERGE WITH THE QUOTES FILE (SEE FOOTNOTE 6 AND 24 IN OUR PAPER) */

/*
This seems to be the most tricky step.  Probably the most time consuming too.
*/

proc sort data=NBBO2;
    by sym_root date Qu_SeqNum;
run;

proc sort data=quoteAB2;
    by sym_root date Qu_SeqNum;
run;

* XXX QUOTE DATA GETS MERGED FOR FIRST TIME HERE
this could be a bottleneck, as it takes a long ass time
to read in the quote file.
Is there a way to loop this more efficiently?  
;
data OfficialCompleteNBBO (drop=Best_Askex Best_Bidex);
    set NBBO2 quoteAB2; 
    by sym_root date Qu_SeqNum;
run;

/* If the NBBO Contains two quotes in the exact same microseond, assume 
   last quotes (based on sequence number) is active one */
proc sort data=OfficialCompleteNBBO;
    by sym_root date time_m descending Qu_SeqNum;
run;

proc sort data=OfficialCompleteNBBO nodupkey;
    by sym_root date time_m;
run;

/* STEP 8: INTERLEAVE TRADES WITH NBBO QUOTES. DTAQ TRADES AT NANOSECOND 
   TMMMMMMMMM ARE MATCHED WITH THE DTAQ NBBO QUOTES STILL IN FORCE AT THE 
   NANOSECOND TMMMMMMMM(M-1) */;

data OfficialCompleteNBBO;
    set OfficialCompleteNBBO;type='Q';
    time_m=time_m+.000000001;
	drop Qu_SeqNum;
run;

proc sort data=OfficialCompleteNBBO;
    by sym_root date time_m;
run;

proc sort data=trade2;
    by sym_root date time_m Tr_SeqNum;
run;

data TradesandCorrespondingNBBO;
    set OfficialCompleteNBBO trade2;
    by sym_root date time_m type;
run;

data TradesandCorrespondingNBBO 
    (drop=Best_Ask Best_Bid Best_AskSizeShares Best_BidSizeShares);
    set TradesandCorrespondingNBBO;
    by sym_root date;
    retain QTime NBO NBB NBOqty NBBqty;
    if first.sym_root or first.date and type='T' then do;
		QTime=.;
        NBO=.;
        NBB=.;
        NBOqty=.;
        NBBqty=.;
    end;
    if type='Q' then Qtime=time_m;
        else Qtime=Qtime;
    if type='Q' then NBO=Best_Ask;
        else NBO=NBO;
    if type='Q' then NBB=Best_Bid;
        else NBB=NBB;
    if type='Q' then NBOqty=Best_AskSizeShares;
        else NBOqty=NBOqty;
    if type='Q' then NBBqty=Best_BidSizeShares;
        else NBBqty=NBBqty;
	format Qtime TIME20.9;
run;

/* STEP 9: CLASSIFY TRADES AS "BUYS" OR "SELLS" USING THREE CONVENTIONS:
   LR = LEE AND READY (1991), EMO = ELLIS, MICHAELY, AND O'HARA (2000)
   AND CLNV = CHAKRABARTY, LI, NGUYEN, AND VAN NESS (2006); DETERMINE NBBO 
   MIDPOINT AND LOCKED AND CROSSED NBBOs */

data BuySellIndicators;
    set TradesandCorrespondingNBBO;
	by sym_root date;

    where type='T';
    midpoint=(NBO+NBB)/2;
    if NBO=NBB then lock=1;else lock=0;
    if NBO<NBB then cross=1;else cross=0;

	*Determine Whether Trade Price is Higher or Lower than Previous Trade 
   Price, or "Trade Direction";

	retain direction2;
    direction=dif(price);
    if first.sym_root or first.date then direction=.;
    if direction ne 0 then direction2=direction; 
    else direction2=direction2;
	drop direction;
run;

data TSpread2;
    set BuySellIndicators;

	*First Classification Step: Classify Trades Using Tick Test;
    if direction2>0 then BuySellLR=1;
    if direction2<0 then BuySellLR=-1;
    if direction2=. then BuySellLR=.;
    if direction2>0 then BuySellEMO=1;
    if direction2<0 then BuySellEMO=-1;
    if direction2=. then BuySellEMO=.;
    if direction2>0 then BuySellCLNV=1;
    if direction2<0 then BuySellCLNV=-1;
    if direction2=. then BuySellCLNV=.;

	*Second Classification Step: Update Trade Classification When 
   	Conditions are Met as Specified by LR, EMO, and CLNV;
    if lock=0 and cross=0 and price gt midpoint then BuySellLR=1;
    if lock=0 and cross=0 and price lt midpoint then BuySellLR=-1;
    if lock=0 and cross=0 and price=NBO then BuySellEMO=1;
    if lock=0 and cross=0 and price=NBB then BuySellEMO=-1;
    ofr30=NBO-.3*(NBO-NBB);
    bid30=NBB+.3*(NBO-NBB);
    if lock=0 and cross=0 and price le NBO and price ge ofr30
        then BuySellCLNV=1;
    if lock=0 and cross=0 and price le bid30 and price ge NBB 
        then BuySellCLNV=-1;


	*skip STEP 10: CALCULATE QUOTED SRPEADS AND DEPTHS;
 
	*STEP 11: CALCULATE EFFECTIVE SPREADS. AGGREGATE BASED ON 3 CONVENTIONS:
   Ave = SIMPLE AVERAGE, DW = DOLLAR-WEIGHTED, SW = SHARE-WEIGHTED;
    wEffectiveSpread_Dollar=(abs(price-midpoint))*2;
    wEffectiveSpread_Percent=abs(log(price)-log(midpoint))*2;

	* ANDREW EDIT: REMOVE OUTLIERS;
	if wEffectiveSpread_Percent > 0.40 then delete;    

    dollar=price*size;
    wEffectiveSpread_Dollar_DW=wEffectiveSpread_Dollar*dollar;
    wEffectiveSpread_Dollar_SW=wEffectiveSpread_Dollar*size;
    wEffectiveSpread_Percent_DW=wEffectiveSpread_Percent*dollar;
    wEffectiveSpread_Percent_SW=wEffectiveSpread_Percent*size;


	*Delete Trades Associated with Locked or Crossed Best Bids or Best 
   Offers;
    if lock=1 or cross=1 then delete;
run;

/* Find average across firm-day */
proc sql;
    create table EffectiveSpreads 
    as select sym_root,date,
    sum(dollar) as sumdollar,
    sum(size) as sumsize,
    mean(wEffectiveSpread_Dollar) as EffectiveSpread_Dollar_Ave,
    mean(wEffectiveSpread_Percent) as EffectiveSpread_Percent_Ave,
    sum(wEffectiveSpread_Dollar_DW) as waEffectiveSpread_Dollar_DW,
    sum(wEffectiveSpread_Dollar_SW) as waEffectiveSpread_Dollar_SW,
    sum(wEffectiveSpread_Percent_DW) as waEffectiveSpread_Percent_DW,
    sum(wEffectiveSpread_Percent_SW) as waEffectiveSpread_Percent_SW 
    from TSpread2 
    group by sym_root,date 
    order by sym_root,date;
quit;

/* Calculate Dollar-Weighted (DW) and Share-Weighted (SW) Dollar Effective 
   Spreads and Percent Effective Spreads */
data EffectiveSpreads;
    set EffectiveSpreads;
    EffectiveSpread_Dollar_DW=waEffectiveSpread_Dollar_DW/sumdollar;
    EffectiveSpread_Dollar_SW=waEffectiveSpread_Dollar_SW/sumsize;
    EffectiveSpread_Percent_DW=waEffectiveSpread_Percent_DW/sumdollar;
    EffectiveSpread_Percent_SW=waEffectiveSpread_Percent_SW/sumsize;
	drop waEffectiveSpread_Dollar_DW waEffectiveSpread_Dollar_SW
         waEffectiveSpread_Percent_DW waEffectiveSpread_Percent_SW;
run;

/* skip STEP 12: CALCULATE REALIZED SPREADS AND PRICE IMPACTS BASED ON THREE:
   CONVENTIONS: LR = LEE AND READY (1991), EMO = ELLIS, MICHAELY, AND O'HARA 
   (2000) AND CLNV = CHAKRABARTY, LI, NGUYEN, AND VAN NESS (2006);  
   FIND THE NBBO MIDPOINT 5 MINUTES SUBSEQUENT TO THE TRADE */


/* STEP 13: DOWNLOAD THE FILES YOU WANT TO YOUR output FOLDER

*/

data output.dtaq_spreads_&yyyymmdd; set EffectiveSpreads; run;




/* Stop timer */
data _null_;
  dur = datetime() - &_timer_start;
  put 30*'-' / ' TOTAL DURATION:' dur time13.2 / 30*'-';
run;
