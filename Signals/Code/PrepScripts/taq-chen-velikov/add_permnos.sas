/*

adds permnos to high freq data

andrew chen 2021 08


*/

* ==== import issm, iid, and msenames ====;

%include '/wrds/lib/utility/wrdslib.sas' ;

proc import datafile = '~/temp_output/issm_monthly.csv' out=issm 
	dbms=csv replace;
	guessingrows=6000;
run;	

proc import datafile = '~/temp_output/wrds_iid_monthly.csv' out=iid 
	dbms=csv replace;
	guessingrows=6000;
run;	

data msenames; set crsp.msenames; 	
	* round to nearest month to ensure distinct;
	* note this means we should use < for end dates;
	linkstart = namedt; linkend = nameendt;
	if day(linkstart) > 15 then linkstart = intnx('month', linkstart, 1);
	if day(linkend) > 15 then linkend = intnx('month', linkend, 1);
	
	linkyearmstart = year(linkstart)*100 + month(linkstart);
	linkyearmend = year(linkend)*100 + month(linkend);	
	
	keep permno namedt nameendt ticker shrcls link: name:;
run;

* ==== append into dataset hf0 ==== ;
* clean issm
separate symbol into root and suffix
select dw spreads to match iid data
;
data temp; set issm; 
	sym_root = scan(symbol,1,'.');
	suffix_1 = scan(symbol,2,'.');	
	suffix_2 = scan(symbol,3,'.');		
	sym_suffix = cats(suffix_1,suffix_2); * ISSM has double suffixes, like .A.WI.  We turn this into .AWI;
	
	espread_pct_mean = eff_spread_dw_ave*100;
	yearm = year*100 + month;
	espread_n = eff_spread_n;
	espread_pct_month_end = .;
	
	keep sym_root sym_suffix espread: symbol yearm;
run;


data hf0;
	set temp iid;
run;	


* ==== add permnos using ticker + shrcls as hf1 ==== ;
*
	according to wrds, this is sufficient for dtaq
	but we also use this for issm due to lack of other options	
	since sym_root is missing for all mtaq data, this step does not add permnos for mtaq
	creates a tiny amount of duplicates, not sure why.
;

proc sql; create table hf1 as select
	a.*, b.permno
	from hf0 as a
	left join msenames as b
	on a.sym_root = b.ticker and a.sym_suffix = b.shrcls
	and a.yearm >= b.linkyearmstart and a.yearm < b.linkyearmend
	and not missing(a.sym_root);
quit;

data hf1; format permno yearm _all_;  set hf1; run;

* ==== add permnos using WRDS tclink algo as hf2 ==== ;

* create link table using WRDS code;
%include '~/hf-spreads-all/macro_tclink.sas';
%TCLINK (BEGDATE=199301,ENDDATE=201012,OUTSET=WORK.mtaq_link);

* remove duplicates from mtaq_link by keeping first symbol (also shortest symbol);
proc sort data = mtaq_link; by permno date symbol; run;
data mtaq_link2; set mtaq_link; 
	by permno date;
	if first.date then output;
run;	

proc sql; create table hf2 as select
	a.*, b.permno as permno_wrds
	from hf1 as a 
	left join mtaq_link2 as b
	on a.symbol = b.symbol and a.yearm = year(b.date)*100+month(b.date);
run;

* clean up;	
data hf2; format permno permno_wrds yearm espread_pct_mean espread_n espread_pct_month_end symbol sym_root sym_suffix;
	set hf2;
	permno2 = coalesce(permno, permno_wrds);
	drop permno;
run;	
data hf2; set hf2;
	rename permno2 = permno;
run;	
proc sort data=hf2; by permno yearm; run;

* ==== clean up a tiny amount of dups ==== ;
* 1,500 out of 3 million obs are dups;

* split data into unique and nonuinque;
proc sort data=hf2 out=temp_nonunique uniqueout=temp_unique nouniquekey;
	by permno yearm;
	where not missing(permno);
run;

* intuitive cleaning removes 1200 dups;
data temp_nonunique1; set temp_nonunique;
	if source = 'mtaq' then delete; * delete if from mtaq; 
	if source = 'dtaq' and not missing(permno_wrds) then delete; * else keep only msenames link;
run;	

* for remaining 300 dups, keep if more observations;
* there seem to be some weird alternative shares situations (VALE and VALEP get assigned to same permno) 
  but these all have a tiny number of daily obs in the month;
proc sort data=temp_nonunique1; by permno yearm descending espread_n; run;
data temp_nonunique1; set temp_nonunique1;
	by permno yearm;
	if first.yearm then output;
run;	

* append back together;
data hf3; set temp_unique temp_nonunique1; run;


* ==== export ==== ;
proc export data = hf3
  outfile = "~/temp_output/hf_monthly.csv"
  dbms = csv
  replace;
run;
