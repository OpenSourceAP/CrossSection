* --------------
// DATA LOAD
use permno gvkey time_avail_m mve_c using "$pathDataIntermediate/SignalMasterTable", clear
drop if mi(gvkey)
merge 1:1 gvkey time_avail_m using "$pathDataIntermediate/m_aCompustat", keepusing(revt cogs xsga xint ceq) nogenerate keep(match)
// SIGNAL CONSTRUCTION
// dirty simulation of NYSE size breakpoints:
// Fama and French use NYSE market cap median to form size groups,
// independently sort on OperProf, and then equally weight the two
// size groups with high OperProf in the long portfolio 
// (see RFS paper footnote to Table 1)
// This effectively overweights large cap stocks.  We can do
// that by simply excluding small cap here.
// Hou Xue Zhang do something similar

      * more complicated denominator (ceq-pstk+min(txdi,0)) does not help

      * removing xsga helps a _lot_, and is pretty much the Novy Marx signal
gen tempprof = (revt - cogs - xsga - xint)/ceq
egen tempsizeq = fastxtile(mve_c), by(time_avail_m) n(3)
replace tempprof = . if tempsizeq == 1
gen OperProf = tempprof
label var OperProf "Operating Profitability"
// SAVE
do "$pathCode/savepredictor" OperProf