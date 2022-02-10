/* 
Andrew 2018 08
Adaptation of Holden and Jacobsen's monthly TAQ code to ISSM.

built off issm_spreads_local.sas
this version should be run on the wrds server.

inputs: /wrds/issm/sasdata
outputs: ~/temp_output/

*/

proc datasets library=work kill;run; quit;

/* User and environment */

%let yyyy = %sysget(yyyy); * get year from command line;
%let exchprefix = %sysget(exchprefix); * get nyam or nasd from command line;
libname issm '/wrds/issm/sasdata'; * issm data location on wrds;
libname output '~/temp_output/'; * output path;




* quote delay is in seconds
Lou and Shu 2017 RFS use 2 seconds before 1999. Since
ISSM data is all before 1999, I fix the quote delay at 2.
;
%let quotedelay = 2; 

%let _timer_start = %sysfunc(datetime());

%let sample = date > -99999;



/* STEP 1-2: LOAD AND CLEAN QUOTE DATA */
data quote (
		where = ( &sample and (("9:00:00"t) <= time <= ("16:00:00"t)) )
		);
    set issm.&exchprefix._qt&yyyy;

    /* Quote Filter 1: Abnormal Modes. Quotes with abnormal modes (i.e.,  
	   abnormal quote conditions) are set to extreme values so that they   
	   will not enter the NBBO 
		Andrew - mode is described as "quote condition" in mtaq
				in ISSM mode is "condition code" 

	*/
    if mode in ('C','D','F','G','I','L','N','P','S','V','X','Z') then do; 
        OFR=9999999; 
        BID=0; 
    end;

    /* Quote Filter 2: Crossed Quotes on the Same Exchange. Quotes from a 
	   given exchange with positive values in which the Bid is greater than
	   the Ask (i.e., crossed quotes) are set to extreme values so that they
	   will not enter the NBBO */
    If BID>OFR and BID>0 and OFR>0 then do; 
        OFR=9999999; 
        BID=0; 
    end;

    /* Quote Filter 3: One-Sided Bid Quotes. One-sided bid quotes (i.e., 
	   quotes in which the Bid is a positive value and the Ask is set to '0') 
	   are allowed to enter the NBB; the Ask is set to an extreme value so 
	   that it will not enter the NBO. One-sided ask quotes are also allowed 
	   to enter the NBO (i.e., quotes in which the Ask is a positive value 
	   and the Bid is set to '0'). In these cases, the bid is already the 
	   extreme value 0; as a result, no adjustment is necessary to ensure it 
	   does not enter the NBB. */
    If BID>0 and OFR=0 then OFR=9999999;

    /* Quote Filter 4: Abnormally Large Spreads. Quotes with positive values  
	   and large spreads (i.e., spreads greater than $5.00) are set to 
	   extreme values so that they will not enter the NBBO */
    spr=OFR-BID;
    If spr>5 and BID>0 and OFR>0 and OFR ne 9999999 then do; 
        BID=0; OFR=9999999; end;

    /* Quote Filter 5: Withdrawn Quotes. This is when an exchange temporarily 
		has no quote, as indicated by quotes with price or depth fields 
		containing values less than or equal to 0 or equal to '.'. See 
		discussion in Holden and Jacobsen (2013), page 11. They are set to 
		extreme values so that they will not enter the NBBO. They are NOT 
		deleted, because that would incorrectly allow the prior quote from 
		that exchange to enter the NBBO. NOTE: Quote Filter 5 must come last

		ac: parts of this filter don't work for issm nasdaq data, since
		the bidsize and ofrsize variables are missing
	*/
    if OFR le 0 then OFR=9999999;
    if OFR =. then OFR=9999999;
    if BID le 0 then BID=0;
    if BID =. then BID=0;



    * updated 2018 10 01 to apply everywhere except NASDAQ 1987-1989;
*    if '&exchprefix' = 'nyam' or &yyyy <= 1986 or &yyyy >= 1990 then do;
    if ('&exchprefix' = 'nyam' and &yyyy ~= 1986)  or 
        ('&exchprefix' = 'nasd' and &yyyy >= 1990) then do;
	    if ofrsize le 0 then OFR=9999999;
	    if ofrsize =. then OFR=9999999;
	    if bidsize le 0 then BID=0;
	    if bidsize =. then BID=0;
    end;



    format date date9.;
run;




/* STEP 3: CLEAN TRADE DATA */

data trade (
		where = ( &sample and (("9:30:00"t) <= time <= ("16:00:00"t)) )
		);
    set issm.&exchprefix._tr&yyyy;

    /* Trade Filter: Keep only trades in which the Correction field 
       contains '00' and the Price field contains a value greater than 
       zero 

		Andrew - ISSM does not have a correction field
				It does have a "quote condition" field.

                I think I will follow Lou and Shu for cleaning
                the quote condition (they call it special sale condition)

	*/
    *where corr eq 0 and price gt 0;

    where cond not in ('C','L','N','R','O','Z')
         and price > 0 and size > 0;    

    type='T';
    format date date9.;	
run;



/* STEP 4: CREATE INTERPOLATED TIME VARIABLES 
   Based on: Holden and Jacobsen (2013), pages 22-24 */
* ac: skip!;

/* STEP 5: NATIONAL BEST BID AND OFFER (NBB0) CALCULATION */

* Assign ID to Each Unique Exchange or Market Maker and Find 
   The Maximum Number of Exchanges
Andrew - in mtaq
	ex = exchange on which quote occurred
	mmid = Indentifies NASDAQ market maker

	ISSM instead has
	oexch = originating exchange
	pexch = ? No description.

	So I'm going to just sort by oexch since this is 
	using the NYSE file for now
	
;
proc sort data=quote; 
    *by ex mmid; * old;
	by oexch; * new;
run;

data quote;
    set quote;
    retain ExchangeID;
    if _N_=1 then ExchangeID=0;
    if first.oexch then ExchangeID=ExchangeID+1;
    by oexch;
run;

data _null_;
 	set quote end=eof;
 	retain MaxExchangeID;
 	if ExchangeID gt MaxExchangeID then MaxExchangeID=ExchangeID;
 	if eof then call symput('MaxExchangeID',MaxExchangeID);
run;

%put &MaxExchangeID;
proc sort data=quote; 
	by symbol date time;
run;
	
%macro BBO;
/* Create Dataset that has a Column for Each Exchange ID's Bid and Offer
   Quote for All Interpolated Times and Multiply Bid Size and Offer Size
   By 100 to convert Round Lots to Shares*/
data quote;
    set quote;
	by symbol date;
	array exbid(&MaxExchangeID);exbid(ExchangeID)=bid;
	array exofr(&MaxExchangeID);exofr(ExchangeID)=ofr;
	array exbidsz(&MaxExchangeID);exbidsz(ExchangeID)=bidsize*100;
	array exofrsz(&MaxExchangeID);exofrsz(ExchangeID)=ofrsize*100;
/* For Interpolated Times with No Quote Update, Retain Previous Quote 
   Outstanding*/
%do i=1 %to &MaxExchangeID;
	retain exbidR&i exofrR&i exbidszR&i exofrszR&i;
	if first.symbol or first.date then exbidR&i=exbid&i;
    if exbid&i ge 0 then exbidR&i=exbid&i; 
        else exbidR&i=exbidR&i+0;
	if first.symbol or first.date then exofrR&i=exofr&i;
    if exofr&i ge 0 then exofrR&i=exofr&i; 
        else exofrR&i=exofrR&i+0;
	if first.symbol or first.date then exbidszR&i=exbidsz&i;
    if exbidsz&i ge 0 then exbidszR&i=exbidsz&i; 
        else exbidszR&i=exbidszR&i+0;
	if first.symbol or first.date then exofrszR&i=exofrsz&i;
    if exofrsz&i ge 0 then exofrszR&i=exofrsz&i; 
        else exofrszR&i=exofrszR&i+0;
%end;
/* Find Best Bid and Offer Across All Exchanges and Market Makers*/
%do i=&MaxExchangeID %to &MaxExchangeID;
	BestBid = max(of exbidR1-exbidR&i);
	BestOfr = min(of exofrR1-exofrR&i);
%end;
/* Find Best and Total Depth Across All Exchanges and Market Makers that
   are at the NBBO*/
%do i=1 %to &MaxExchangeID;
	if exbidR&i=BestBid then MaxBidDepth=max(MaxBidDepth,exbidszR&i);
	if exofrR&i=BestOfr then MaxOfrDepth=max(MaxOfrDepth,exofrszR&i);
	if exbidR&i=BestBid then TotalBidDepth=sum(TotalBidDepth,exbidszR&i);
	if exofrR&i=BestOfr then TotalOfrDepth=sum(TotalOfrDepth,exofrszR&i);
%end;
run;
%mend BBO;
%BBO;


data CompleteNBBO (keep=symbol date time  
    BestBid BestOfr MaxBidDepth MaxOfrDepth TotalBidDepth TotalOfrDepth);
    set quote;
/* Only Output Changes in NBBO Records (e.g., changes in quotes or depth)*/
    if symbol eq lag(symbol) 
        and date eq lag(date) 
        and BestOfr eq lag(BestOfr) 
        and BestBid eq lag(BestBid) 
        and MaxOfrDepth eq lag(MaxOfrDepth) 
        and MaxBidDepth eq lag(MaxBidDepth)
        and TotalOfrDepth eq lag(TotalOfrDepth) 
        and TotalBidDepth eq lag(TotalBidDepth) then delete;
/* If Abnormal Quotes Enter the NBBO Then Set To ".". There Will Be 
   NO NBBO */
    if BestBid < .00001 then 
        do;
        BestBid=.;
        BestOfr=.;
        MaxOfrDepth=.;
        MaxBidDepth=.;
        TotalOfrDepth=.;
        TotalBidDepth=.;
        end;
    else if BestOfr > 9999998 then 
        do;
        BestBid=.; 
        BestOfr=.;
        MaxOfrDepth=.;
        MaxBidDepth=.;
        TotalOfrDepth=.;
        TotalBidDepth=.;
        end;
run;

/* STEP 6: INTERWEAVE TRADES WITH QUOTES: TRADES AT INTERPOLATED TIME TMMM
   ARE MATCHED WITH QUOTES IN FORCE AT INTERPOLATED TIME TMM(M-1)
   To Do This, Increase Interpolated Quote Time in Quotes Dataset by One
   Millisecond = .001*/
* ac: skip interpolation.  We found issues with it in WRDS iid data;
* also, quote delay is set using macro &quotedelay;


data CompleteNBBOinforce;
    set CompleteNBBO;
    type='Q';
	time + &quotedelay;
run;

/* Stack Quotes and Trades Datasets */
data TradesandCorrespondingNBBO;
    set trade CompleteNBBOinforce;
	by symbol date time type; * sort alternatively by interpolated time;
run;

/* For Each Trade, Identify the Outstanding NBBO, Best Depth and Total 
   Depth
*/
* ac: make sure datasets are lagged and sorted correctly here;
data TradesandCorrespondingNBBOv2 (drop=time BestOfr BestBid 
     MaxOfrDepth MaxBidDepth TotalOfrDepth TotalBidDepth);
    set TradesandCorrespondingNBBO;
    by symbol date;
    retain quotetime BestOfr2 BestBid2 MaxOfrDepth2 MaxBidDepth2 
        TotalOfrDepth2 TotalBidDepth2;
	if first.symbol or first.date and type='T' then quotetime=.;
	if first.symbol or first.date and type='T' then BestOfr2=.;
	if first.symbol or first.date and type='T' then BestBid2=.;
	if first.symbol or first.date and type='T' then MaxOfrDepth2=.;
	if first.symbol or first.date and type='T' then MaxBidDepth2=.;
	if first.symbol or first.date and type='T' then TotalOfrDepth2=.;
	if first.symbol or first.date and type='T' then TotalBidDepth2=.;
    if type='Q' then quotetime=time;else quotetime=quotetime;
    if type='Q' then BestOfr2=BestOfr;else BestOfr2=BestOfr2;
    if type='Q' then BestBid2=BestBid;else BestBid2=BestBid2;
    if type='Q' then MaxOfrDepth2=MaxOfrDepth;else MaxOfrDepth2=MaxOfrDepth2;
    if type='Q' then MaxBidDepth2=MaxBidDepth;else MaxBidDepth2=MaxBidDepth2;
    if type='Q' then TotalOfrDepth2=TotalOfrDepth;
        else TotalOfrDepth2=TotalOfrDepth2;
    if type='Q' then TotalBidDepth2=TotalBidDepth;
        else TotalBidDepth2=TotalBidDepth2;
    format quotetime time.;
run;

/* STEP 7: Classify Trades as "Buys" or "Sells" Using Three Conventions: 
   LR = Lee and Ready (1991), EMO = Ellis, Michaely and O?Hara (2000)
   and CLNV = Chakrabarty, Li, Nguyen, and Van Ness (2006); Determine NBBO 
   Midpoint and Locked and Crossed NBBOs */

data BuySellIndicators;
    set TradesandCorrespondingNBBOv2;
    where type='T';
    midpoint=(BestOfr2+BestBid2)/2;
    if BestOfr2=BestBid2 then lock=1;else lock=0;
    if BestOfr2<BestBid2 then cross=1;else cross=0;
run;

*
ac: we probably don't need all these buy sell indicators below
;

/* Determine Whether Trade Price is Higher or Lower than Previous Trade 
   Price, or "Trade Direction" */
data BuySellIndicators;
    set BuySellIndicators;
    by symbol date;
    direction=dif(price);
    if first.symbol then direction=.;
    if first.date then direction=.;
run;

data BuySellIndicators;
    set BuySellIndicators;
    retain direction2;
    if direction ne 0 then direction2=direction; 
    else direction2=direction2;
run;

/* First Classification Step: Classify Trades Using Tick Test */
data BuySellIndicators (drop=direction);
    set BuySellIndicators;
	length BuySellLR BuySellEMO BuySellCLNV $4.;
    if direction2>0 then BuySellLR=1;
    if direction2<0 then BuySellLR=-1;
    if direction2=. then BuySellLR=.;
    if direction2>0 then BuySellEMO=1;
    if direction2<0 then BuySellEMO=-1;
    if direction2=. then BuySellEMO=.;
    if direction2>0 then BuySellCLNV=1;
    if direction2<0 then BuySellCLNV=-1;
    if direction2=. then BuySellCLNV=.;
run;

/* Second Classification Step: Update Trade Classification When 
   Conditions are Met as Specified by LR, EMO, and CLNV */
data BuySellIndicators;
    set BuySellIndicators;
    if lock=0 and cross=0 and price gt midpoint then BuySellLR=1;
    if lock=0 and cross=0 and price lt midpoint then BuySellLR=-1;
    if lock=0 and cross=0 and price=BestOfr2 then BuySellEMO=1;
    if lock=0 and cross=0 and price=BestBid2 then BuySellEMO=-1;
    ofr30=BestOfr2-.3*(BestOfr2-BestBid2);
    bid30=BestBid2+.3*(BestOfr2-BestBid2);
    if lock=0 and cross=0 and price le BestOfr2 and price ge ofr30
        then BuySellCLNV=1;
    if lock=0 and cross=0 and price le bid30 and price ge BestBid2 
        then BuySellCLNV=-1;
run;

/* STEP 8: CALCULATE QUOTED SRPEADS AND DEPTHS */
* ac: skip;

/* STEP 9: CALCULATE EFFECTIVE SPREADS; AGGREGATE BASED ON 3 CONVENTIONS:
   Ave = SIMPLE AVERAGE, DW = DOLLAR-WEIGHTED, SW = SHARE-WEIGHTED */

data BuySellIndicators;
    set BuySellIndicators;
    wEffectiveSpread_Dollar=(abs(price-midpoint))*2;
    wEffectiveSpread_Percent=abs(log(price)-log(midpoint))*2;

	* ANDREW EDIT: REMOVE OUTLIERS;
	if weffectivespread_percent > 0.40 then delete;

    dollar=price*size;
    wEffectiveSpread_Dollar_DW=wEffectiveSpread_Dollar*dollar;
    wEffectiveSpread_Dollar_SW=wEffectiveSpread_Dollar*size;
    wEffectiveSpread_Percent_DW=wEffectiveSpread_Percent*dollar;
    wEffectiveSpread_Percent_SW=wEffectiveSpread_Percent*size;
run;

/* Delete Trades Associated with Locked or Crossed Best Bids or Best 
   Offers */
data TSpread2;
    set BuySellIndicators;
    if lock=1 or cross=1 then delete;
run;


/* Find average across firm-day */
proc sql;
    create table EffectiveSpreads 
    as select symbol,date,
    sum(dollar) as sumdollar,
    sum(size) as sumsize,
    mean(wEffectiveSpread_Dollar) as EffectiveSpread_Dollar_Ave,
    mean(wEffectiveSpread_Percent) as EffectiveSpread_Percent_Ave,
    sum(wEffectiveSpread_Dollar_DW) as waEffectiveSpread_Dollar_DW,
    sum(wEffectiveSpread_Dollar_SW) as waEffectiveSpread_Dollar_SW,
    sum(wEffectiveSpread_Percent_DW) as waEffectiveSpread_Percent_DW,
    sum(wEffectiveSpread_Percent_SW) as waEffectiveSpread_Percent_SW 
    from TSpread2 
    group by symbol,date 
    order by symbol,date;
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

proc sort data=effectivespreads; by effectivespread_percent_ave; run;



/* STEP 13: DOWNLOAD THE FILES YOU WANT TO YOUR output FOLDER

*/
data output.spread_issm_&exchprefix.&yyyy; set EffectiveSpreads; run;



/* Stop timer */
data _null_;
  dur = datetime() - &_timer_start;
  put 30*'-' / ' TOTAL DURATION:' dur time13.2 / 30*'-';
run;
