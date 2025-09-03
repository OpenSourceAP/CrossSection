{smcl}
{right:version:  4.8}
{cmd:help asreg} {right:Dec 23, 2022}
{hline}
{viewerjumpto "Options" "asreg##options"}{...}
{viewerjumpto "fmb" "asreg##fmb"}{...}
{viewerjumpto "newey" "asreg##newey"}{...}
{viewerjumpto "first" "asreg##first"}{...}
{viewerjumpto "save" "asreg##save"}{...}
{viewerjumpto "examples" "asreg##examples"}{...}

{title:Title}

{p 4 8}{cmd:asreg}  -  Rolling window regressions and by(group) regressions {p_end}


{title:Syntax}

{p 8 15 2}
[bysort varlist:] {cmd:asreg}
{depvar} {indepvars} {ifin} 
[, {cmdab:w:indow(}{it:{help asreg##window:rangevar range_low range_high}}{cmd:)}
{cmdab:noc:onstant:}{cmd:}
{cmdab:rec:ursive:}{cmd:}
{cmdab:min:imum:(}{it:#}{cmd:)}
{cmdab:by:(}{it:varlist}{cmd:)}
{help asreg##Options:{statistics_options} }
{help asreg##newey:newey(#)}
{help asreg##fmb:fmb}
{help asreg##save:save(file name)}
{help asreg##first:first}
{cmdab:exclude:(}{it:{help asreg##xf:rangevar range_low range_high}}{cmd:)}]


{title:Description}

{p 4 4 2} {cmd: asreg} fits a model of depvar on indepvars using linear regression
 in a user's defined rolling window or by a grouping variable. asreg is order of
 magnitude faster than estimating rolling window regressions through conventional
methods such as Stata loops or using the Stata's official {help rolling} command.
 {help asreg} has the same speed efficiency as {help asrol}. All the rolling 
 window calculations, estimation of regression parameters, and writing the 
 results to Stata variables are done in the Mata language.
 
 {p 4 4 2} Rolling window calculations require lots of looping over observations.
 The problem is compounded by different data structures such as unbalanced panel data,
 data with many duplicates, and data with many missing values. Yet, there might 
 be data sets that have both time series gaps as well as many duplicate observations
 across groups. {help asreg} does not use a static code for all types of data 
 structures. Instead, {help asreg} intelligently identifies data structures and matches
one of its rolling window routines with the data characteristics. Therefore, 
the rolling window regressions are fast even in larger data sets. {p_end}

{title:What's New in Version 4.0}

{p 4 4 2}
{hi: 1. Changes made to the window() option}  {break}
Version 4.0 of asreg introduces a more flexible window to identify observation
in a given range. Previously, the {help asreg##window:window()} option of asreg
 would take two inputs: the first one as the range variable (such as date) 
 and the second one as the length of the rolling window. In the older versions, the window
would always look backward. This has changed in version 4.0.

{p 4 4 2} The window argument can now take up to three arguments. The window can now look
backward, forward, and both back and forward. More details can be read in the following section
 under the {help asreg##window: option  window()}

{p 4 4 2} {hi:2. Improved algorithm for rolling window indices} {break}
This version of {cmd: asreg} (version 4.0) significantly improves the 
calculation speed of the required statistics,
thanks to the development of a more efficient algorithm for extracting rolling 
window indices. This has resulted in a significant speed advantage for asreg compared
to its previous versions or other available programs. The speed efficiency matters 
more in larger datasets. 

{title:Web Page}

{p 4 4 2} There is a dedicated 
{browse "https://fintechprofessor.com/stata-programs/asreg-a-powerful-package-for-regressions-in-stata/":web page}
of asreg on my website 
{browse "https://fintechprofessor.com/": www.FinTechProfessor.com}. 
The webpage lists different helping material related to asreg. These materials
 include YouTube videos, blog posts on different situations where asreg
can be used, and some questions and answers. Further, I aslo maintain 
{browse "https://fintechprofessor.com/forums/topic-tag/asreg/":a users' community forum} where questions related to asreg can be answered.{p_end} 

{title:Regression statistics and their names}
{p 4 4 2} {cmd: asreg} writes all regression outputs to the data in memory as 
separate variables. This eliminates the need for
writing the results to a separate file, and then merging them back to the data 
for any further calculations. New variables
from the regression results follow the following naming conventions: {p_end}


{dlgtab:Regression statistics and their names}
 
 {p2colset 8 29 29 2}{...}
{p2col :{opt observations}}variable containing number of observation is named as {cmd:_N}{p_end}
{p2col :{opt regression slopes}}a prefix of {cmd: _b_} is added to the name of each independent variables{p_end}
{p2col :{opt constant}}variable containing constant of the regression is names as {cmd: _b_cons}{p_end}
{p2col :{opt r-squared}}r-squared and adj. r-squared are named as {cmd:R2} and {cmd:AdjR2} , respectively{p_end}
{p2col :{opt RMSE}}root-mean-square error. This variable is named as {cmd:_rmse}.{p_end}
{p2col :{opt standard errors}}a prefix of {cmd: _se_} is added to the name of each independent variables. asreg can estimate three types of coefficient errors: See {help asreg##errors:Section 6 below} {p_end}
{p2col :{opt residuals}}variable containing residuals is named as {cmd:_residuals} {p_end}
{p2col :{opt fitted}}variable containing fitted values is named as {cmd:_fitted}.{p_end}

{marker asreg_options}{...}
{dlgtab:Options}

{p 4 4 2} 
{cmd:asreg} has the following options. {p_end}

{marker window}
{p 4 4 2} 1.  The {opt w:indow()}:{break} 
The latest version of asreg accepts up to three
 arguments and is written like this: {p_end}

{p 4 4 2} {opt window(rangevar #from #upto)}

{p 4 4 2}The {it:rangevar} is usually a time variable such as date, monthly date,
 or yearly date. However, it can also be any other numeric variable, such as age,
 income, industry indicator, etc.
Both {it:{hi:#from}} and {it:{hi:#upto}} are numeric values that set the lower and upper
bounds on the rolling window, using the current value of the {it:rangevar} as a benchmark. 
Negative values of these inputs mean going back # periods from the current 
value of the {it:rangevar}. Similarly, positive values of these imply going ahead # periods 
of the current value of the {it:rangevar}. {p_end}

{p 4 8 2}{hi: Please note}: {break}
1. asreg considers the focal observation as part of the past. {break}
2. Given the legacy of asreg, a window() with two inputs is still supported. 
However, the following rule should be noted: {p_end}

{p 12 12 2}If option {help asreg##window:window()} has two arguments, it shall always look back. 
In other words, if option window() has two arguments, then the second argument
will always be counted as a negative number. Therefore, the following
{help asreg##window:window()} options mean the same: {p_end}

{p 12 12 2} {opt w:indow(year 50)} {p_end}

{p 12 12 2} {opt w:indow(year -50 0)} {p_end}

{p 12 12 2} {opt w:indow(year -50)} {p_end}

{p 4 4 2}In the following paragraphs, I present some examples to make it easier to understand 
option {help asreg##window:window()}.


{p 4 4 2}{hi:Window examples and interpretations}

{p 4 4 2} The following table presents examples of the {opt w:indow()} option and its interpretations.


{dlgtab:window examples}
{p2colset 4 25 26 2}{...}

{p2col : {opt w:indow(year -5 0)}}	A rolling window of past 5 observations. 
Therefore, if the focal year is 2006, the window will include these years in the 
calculations: {hi:2006, 2005, 2004, 2003, 2002}. 
The window can also be written as {opt w:indow(year 5)} {p_end}

{p2col : {opt w:indow(year 1 5)}}	A rolling window of 5 lead-observations. 
Therefore, if the focal year is 2006, the window will include these years in the 
calculations: {hi:2007, 2008, 2009, 2010, 2011}.  {p_end}

{p2col : {opt w:indow(year -13 -2)}}	A rolling window of past 11 observations 
from t-12 up to t-2. Therefore, if the focal year is 2006, 
the window will include these years in the calculations: {hi: 1994, 1995, 1996, 
1997 , 1998, 1999, 2000, 2001, 2002, 2003, 2004}. 
The window can also be written as {opt w:indow(year 5)} {p_end}

{p2col : {opt w:indow(year -5 5)}}	A rolling window of 10 observations. Therefore, 
if the focal year is 2006, the window will include these years in the calculations:
 {hi:2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011}. The window 
 can also be written as {opt w:indow(year 5)} {p_end}

{p2col : {opt  Note on missing values in the rangevar}} Some posts on the Statalist 
show confusion concerning the interpretation of the option {opt w:indow()}.
 For example, using {opt window(year -5)}, a user might incorrectly assume that 
 the observation in this range will always be 5. This might not be true in a 
 case where the {it:rangevar} has gaps.  So if the current value of the {it:rangevar}
 (in our case year) is 2006 and its previous values are 2000, 2001, 2003, 2005. 
 Though the window asks for 5 observations within the range of 2006, the available
 values of the {it:rangevar} are only {hi:2006, 2005, 2003}, which are only 3 observations. The window
range ends at 2002, other values of the year are outside the window bounds. {p_end}
{hline}

{p 4 4 2}For more discussion and examples on the option window, {browse "https://fintechprofessor.com/asrol-fastest-rolling-window-and-groups-statistics-in-stata/asrol-option-window/" :see this web page.}

{p 4 4 2} {opt 2.  Cross-sectional regressions:}({opt When option window() is not used)}

{p 4 4 2} NOTE: Option window is an optional option, and hence it can be dropped 
altogether. This is useful when we are interested in by-group or cross-sectional regressions without 
using a rolling window. For example, if we have a large cross-section of industries
 or firms and we wish to estimate a separate regression for each of the cross-sections,
 we shall drop option window. See Example 6 below. {p_end}

{p 4 4 2} 3. {opt rec:ursive}: The option recursive specifies that a recursive 
window be used. In time series analysis, a recursive window refers to 
a window where the starting period is held fixed, the ending period advances, 
and the window size grows (see, for example, {help rolling}). {help asreg}
allows a recursive window either by invoking the option {opt rec:ursive} or 
setting the length of the window greater than or equal to the sample size per group. 
For example, if the sample size of our data set is 1000 observation per group, we 
can use a {opt rec:ursive} analysis by setting the window length equal to 1000 
or greater than 1000 {p_end}
		
{p 4 4 2} 4. {opt by}: {cmd: asreg} is {help byable}. Hence, it can be run on
 groups as specified by option {help by}({it:varlist}) or the {help bysort} 
 {it: varlist}: prefix.
An example of such regression might be 
{browse "https://en.wikipedia.org/wiki/Fama%E2%80%93MacBeth_regression": Fama and MacBeth (1973)} first stage regression, which is estimated 
cross-sectionally in each time period. Therefore, the grouping {help variable}
 in this case would be 
the time variable. Assume that we have our dependent variable named 
as{it: stock_returns}, independent variable as  {it: stock_betas}, and time variable as 
{it:month_id}, then to estimate the cross-sectional
regression for each month, {help asreg} command will look like this:

 {p 4 4 2}{stata "bys month_id: asreg stock_returns  stock_betas" :. bys month_id: asreg stock_return  stock_betas} {p_end}
 
 {p 4 4 2} 5. {opt  min:imum(#)}: {help asreg} estimates regressions where the number of observations is greater than the number of regressors.
 However, the option {opt min:imum(#)} can be used to specify the minimum number of observations for a given regression, where {opt #:} is an integer.
If option {opt min(#)} is used, {help asreg} then finds the required number of observation for the regression estimated such that : {p_end}
 {p 4 8 2} obs = max(number of regressors (including the intercept), minimum observation as specified by the option {opt min}). {p_end}
 {p 4 4 2} For example, if we have 4 explanatory variables, then the number of regressors will be equal to 4 plus 1 i.e. 5. 
 Therefore, if option {opt min:(8)} is used, the required number of observations will be : max(5,8) = 8. If a specific
 rolling window does not have that many observations, the values of the new variable will be replaced with missing values. {p_end}
{marker Options}
 {dlgtab:Statistics_Options}

{p2colset 8 21 21 2}{...}
{p2col :{opt fit:ted}}reports {stata help regress postestimation##predict:residuals} and fitted values for the last observation in the rolling window. 
If option window is not specified, then the residuals are calculated within each group as specified by the option {help by}({it:varlist}) or the {help bysort} {it: varlist}: {p_end}
{p2col :{opt se:rror}}reports standard errors for each explanatory variable{p_end}
{p2col :{opt rmse}}reports root-mean-squared error of OLS regression{p_end}
{p2col :{opt noc:onstant}}suppresses the constant term (intercept) in the model (this option is not available in the Fama-MacBeth regression i.e., when using option {opt fmb}{p_end}
{p2col :{opt other}}Most commonly used regression statistics such as number of observations, slope coefficients, r-squared, and adjusted r-squared are
written to new variables by default. Therefore, if these statistics are not needed, they can be dropped once asreg is estimated.{p_end}

{marker errors}
 {p 4 4 2} 6. {opt  Coefficient errors}: {help asreg} can estimate three types 
 of coefficient errors. The first type is the standard errors. Standard errors are
 the default option in asreg. They are reported only when option {opt se} is used.
 The second type is the 
 {browse "https://www.stata.com/support/faqs/statistics/robust-standard-errors/": robust standard errors}
 which are reported when option {opt r:obust} is used (this option is not 
 available in the Fama-MacBeth regression i.e., when using option {opt fmb}. 
 The third type is the {help newey:Newey-West} standard errors which are 
 reported when option {opt newey(#)} is used, see
 further details {help asreg##newey:here}.
 
{marker xf}
 {p 4 4 2} 7. {opt  exclude(rangevar #low #high)}: Option exclude() is 
 used to exclude specific observations from regressions. This option requires
 three arguments, with or without using the comma character. The first is the range variable
such as daily, weekly, monthly or yearly date; the second and third arguments
 are the lower and upper bounds of th range variable. The definitions and working
 of option {opt  exclude(rangevar #low #high)} are similar to that of the option 
 {help asreg##window:{opt window(rangevar #from #upto)}}. 
 
{dlgtab:exclude examples}
{p2colset 4 25 26 2}{...}

{p2col : {opt exclude(year 0 0)}}	Exclude focal observation. Therefore, if 
the focal year is 2006, it will be excluded from the regression.
Also note if the focal year has duplicates, they shall also be excluded.{p_end}

{p2col : {opt exclude(year 2 2)}}	Exclude 5 observations. Assume that the 
focal year is 2020. Observations pertaining to 
the years 2018, 2019, 2020, 2021, and 2022 will be excluded. {p_end}

{p2col : {opt exclude(year -5 0)}}	Exclude 6 observations. Assume that the 
focal year is 1940. Observations pertaining to the 
year 1935, 1936, 1937, 1938, 1939, and 1940 will be excluded. {p_end}

{p2col : {opt exclude(year 0 5)}}	Exclude 6 observations. Assume that the 
focal year is 1940. Observations pertaining to the 
years 1940, 1941, 1942, 1943, 1944, 1945, and 1945 will be excluded. {p_end}
{hline}


{marker fmb}
{title:FMB: Fama and McBeth(1973) regression}

{p 4 4 2} Option {cmd: fmb} applies a two-step Fama-McBeth procedure.{break} 
• The first step involves estimating {bf:N} cross-sectional regressions. {break}
• The second step involves taking {bf:T} time-series averages of the coefficients from the {bf:N} cross-sectional regressions.{break}
The standard errors are adjusted for cross-sectional dependence. This is generally an acceptable solution when there is a large number of cross-sectional units and a relatively small time series for each cross-sectional unit. However, if both cross-sectional and time-series dependence are suspected in the data set, then Newey-West consistent standard errors can be used. {help asreg} uses the first method as a default.
 {p_end}

{p 4 4 2} {cmd:asreg} with option {cmd: fmb} is very similar to {stata "ssc des xtfmb":xtfmb} program written by Daniel Hoechle. However, there are
 three major differences: {p_end}

{p 8 8 2} 1. {cmd:asreg} estimates the cross-sectional regressions using Mata language, while {cmd:xtfmb} does that using the {help statsby} command. This difference in implementation can have a significant impact on the run time of the two programs, with {help asreg} typically being much faster for large datasets.{break}
2. {help asreg} allows estimation of Newey-West standard errors even if the data set has time-series gaps. xtfmb, on the other hand, will exit with an error message if the data has time-series gaps. {break}
3. {help asreg}  allows saving the coefficients of the first stage regression to a file using the {opt save(filename)} option. This can be useful for debugging or for further analysis.

{marker save}
{p 4 4 2} {opt  6. save(filename)}: Option {opt save} is used only when option {opt fmb} is used. Option {opt save} saves the first stage regression coefficients of the Fama-McBeth 
regression to a file. 

{marker newey}
{p 4 4 2} {opt  7. newey(integer)}: {opt newey} specifies the number of lags for estimation of Newey-West consistent standard errors. {cmd: asreg} allows option {opt newey} to be used in both the rolling
regressions and Fama-McBeth regressions. In the rolling regressions, {opt newey} will work only when option {opt se} is used. Also, please note that without using option {opt newey},
 option {opt se} estimates normal standard errors of OLS. This option accepts only integers, for example {opt newey(1)} or {opt newey(4)} are acceptable, but {opt newey(1.5)} 
 or {opt newey(2.3)} are not.

 {marker first}
{p 4 4 2} {opt  8. first}: This option will work only when option {opt fmb} is invoked. Option {opt first} displays on the screen the first-stage regression coefficients of the Fama-McBeth regressions.

{marker examples}
 {dlgtab:Examples}

 
 {title:Example 1: Regression for each company in a rolling window of last 10 years}
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 10)" :. bys company: asreg invest mvalue kstock, wind(year 10)} {p_end}
 {p 4 8 2}OR{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year -10 0)" :. bys company: asreg invest mvalue kstock, wind(year -10 0)} {p_end}

 
 {title:Example 2: Regression for each company in a rolling window of 10 years; 5 past and 5 forward}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year -5 5)" :. bys company: asreg invest mvalue kstock, wind(year -5 5)} {p_end}

 
 {title:Example 3: Regression for each company in a rolling window of 10 leading years}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 0 10)" :. bys company: asreg invest mvalue kstock, wind(year 0 10)} {p_end}

 {title:Example 4: Regression for each company in a recursive window}
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 10) rec" :. bys company: asreg invest mvalue kstock, wind(year 10) rec} {p_end}
 {p 4 8 2} OR {p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 1000)" :. bys company: asreg invest mvalue kstock, wind(year 1000)} {p_end}

 
 {title:Example 5: Using option minimum - Limit regression to a minimum of 5 observations}
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 10) min(5)" :. bys company: asreg invest mvalue kstock, wind(year 10) min(5)} {p_end}

 
 
 {title:Example 6: Reporting standard errors} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 10) se" :. bys company: asreg invest mvalue kstock, wind(year 10) se} {p_end}
 
 
 {title:Example 7: Newey-West standard errors, lag(1)} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 10) se newey(1)" :. bys company: asreg invest mvalue kstock, wind(year 10) se newey(1)} {p_end}

 
 {title:Example 8: Robust standard errors} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 10) robust" :. bys company: asreg invest mvalue kstock, wind(year 10) robust} {p_end}

 
 
 {title:Example 9: Reporting standard errors, fitted values and residuals} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 10) se fit" :. bys company: asreg invest mvalue kstock, wind(year 10) se fit} {p_end}

 
  {title:Example 10: Regressions without constant} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, wind(year 10) noc" :. bys company: asreg invest mvalue kstock, wind(year 10) noc} {p_end}


 
 {title:Example 11: No window - by groups regressions} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock" :. bys company: asreg invest mvalue kstock} {p_end}

 
 
 {title:Example 12: Yearly cross-sectional regressions} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys year: asreg invest mvalue kstock" :. bys year: asreg invest mvalue kstock} {p_end}
 

 {title:Example 13: Rolling regression - reporting RMSE} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, w(year 10) rmse" :. bys company: asreg invest mvalue kstock, w(year 10) rmse} {p_end}
 
 
 {title:Example 14: Fama and McBeth Regression} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "asreg invest mvalue kstock, fmb" :. asreg invest mvalue kstock, fmb} {p_end}
 
 
 {title:Example 15: Fama and McBeth Regression - using Newey-West errors} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "asreg invest mvalue kstock, fmb newey(1)" :. asreg invest mvalue kstock, fmb newey(1)} {p_end}


 {title:Example 16: Fama and McBeth Regression - report first stage regression} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "asreg invest mvalue kstock, fmb first" :. asreg invest mvalue kstock, fmb first} {p_end}
 
 
 {title:Example 17: Fama and McBeth Regression - save first stage results} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "asreg invest mvalue kstock, fmb save(FirstStage)" :. asreg invest mvalue kstock, fmb save(FirstStage)} {p_end}

 
  {title:Example 18: Exclude focal observation in cross-sectional regressions} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, exclude(year 0 0 )" :. bys company: asreg invest mvalue kstock, exclude(year 0 0)} {p_end}

  {title:Example 19: Exclude 5 most recent observations (the focal observation and 4 others from the recent past)} 
 {p 4 8 2}{stata "webuse grunfeld, clear" :. webuse grunfeld, clear}{p_end}
 {p 4 8 2}{stata "bys company: asreg invest mvalue kstock, exclude(year -4 0 )" :. bys company: asreg invest mvalue kstock, exclude(year -4 0)} {p_end}


 
 {title:Stored Results from option FMB}
  {p 4 8 2} {cmd: asreg} returns the following scalars, macros and matrices in eclass for Fama-McBeth regressions.
  
  
 scalars:
                  e(N) =  number of observation
                e(N_g) =  number of groups
               e(df_r) =  degrees of freedom
                  e(F) =  F-test value
                e(r2_a) =  average r-squared

macros:
              e(avgr2) : "average r-squared"
               e(cof1) : "coefficient of the first independent variable"
                e(cmd) : "command name"
             e(method) : "Fama-MacBeth Two-Step procedure"
             e(depvar) : "invest"
            e(vcetype) : "Fama-MacBeth"
         e(properties) : "b V"

matrices:
                  e(b) :  vector of slopes
                  e(V) :  variance-covariance matrix



{title:Author}

::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::: *
*                                                                   *
*            Dr. Attaullah Shah                                     *
*            Institute of Management Sciences, Peshawar, Pakistan   *
*            Email: attaullah.shah@imsciences.edu.pk                *
*           {browse "www.OpenDoors.Pk": www.OpenDoors.Pk}                                       *
*           {browse "www.StataProfessor.com": www.StataProfessor.com}                                 *
*:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::*


{marker also}{...}
{title:Also see}

{marker sub_opt}{...}
{synoptset 15}{...}
{synopthdr:Program}
{synoptline}
{synopt :{browse "https://fintechprofessor.com/asdocx/" :asdocx }}Flexible, yet extremely powerful package for publication quality tables {p_end}
{synopt :{browse "https://fintechprofessor.com/stata-programs/asm-stata-program-to-construct-j-k-momentum-portfolios/":asm}}for momentum portfolios{p_end}
{synopt :{stata "ssc desc asdoc":asdoc}}f creating high-quality tables in MS Word from Stata output {p_end}
{synopt :{stata "ssc desc asreg":asgen}}for weighted average mean {p_end}
{synopt :{stata "ssc desc asrol":asrol}}for rolling window statistics {p_end}
{synopt :{stata "ssc desc ascol":ascol}}for coverting share prices and returns from daily to weekly or monthly frequency {p_end}
{synopt :{stata "ssc desc searchfor":searchfor}}for searching text in data sets {p_end}
{synopt :{stata "ssc desc fillmissing":fillmissing}}Fills missing values in a variable based on a given criterion {p_end}
{synoptline}




