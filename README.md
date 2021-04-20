# Open source cross sectional asset pricing

This repo accompanies our paper:
[Chen and Zimmermann (2021), "Open source cross-sectional asset pricing"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626)

If you use data or code based on our work, please cite the paper: 

~~~
@unpublished{ChenZimmermann2021,
author = "Chen, Andrew Y. and Tom Zimmermann",
title = "Open Source Cross Sectional Asset Pricing",
note = "available at https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626",
year = 2021
}
~~~


----

## Data

If you are mostly interested in working with the data, we provide signal and portfolio returns in separate files for direct download [here].

----

## Code 

The code is separated into two parts:

1. **Signals**: Contains code to produce stock-level signals
2. **Portfolios** Contains code to produce portfolio returns

You can download the individual signals that are outputs of the **Signals** part of the code from the data repository above and start from the **Portfolios** part if you like.

### 1. Signals

The **Signals code** provides scripts for `DataDownloads`, `Predictors` and `Placebos`. The `master.do` file runs all files but you will need to set paths pointing to your project folder, your R installation and your WRDS connection (see below).

*Optional (i.e. code is modular and will work even if you do not do that)*: To construct signals that rely on IBES, 13F, TAQ or OptionMetrics data run the SAS scripts in `PrepScripts` on the WRDS server. See the [WRDS instructions](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-sas/) for different ways to run these scripts on the WRDS server. Copy the output of those scripts to `Signals/Data/Prep`. Code to construct trading costs from TAQ data is provided separately and can be downloaded [here](https://drive.google.com/open?id=1W256-g-RxqOZBjNtkSJuuWXUqHZEYHsM).

*See **Data access** part of the readme below for some data access steps that you need to complete before you can run the code.*


### 2. Portfolios

The _Portfolios_ code constructs portfolio returns from the signal files. The `master.R` can serve as a reference as to the order in which files should run. You need to set the project folder (same as for the Stata code) in `00_SettingsAndTools.R` for everything to work.

---- 
## Data access

### 1. Connecting to Wharton Research Data Services (WRDS)

To download raw data from the original sources, you will need access to WRDS via Stata / ODBC. At a minimum, you will need access to CRSP and Compustat, but the code is modular and should be able to deal with lack of access to other datasets.

#### Setting up Stata / ODBC access to WRDS

WRDS provides instructions for Windows users [here.](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-stata/stata-from-your-computer/)  

For Linux users, we recommend the following (This is similar to how it works on the WRDS server):

Step 1 - Create a text file ~/.odbc.ini, and put the following text in there:

    [ODBC Data Sources]
    wrds-postgres = PostgreSQL

    [wrds-postgres]
    Driver           = PostgreSQL
    Description      = Connect to WRDS on the WRDS Cloud
    Database         = wrds
    Username         = mcgregor_should_retire
    Password         = and_teach_classes_on_shorts_grabbing
    Servername       = wrds-pgdata.wharton.upenn.edu
    Port             = 9737
    SSLmode          = require

Step 2 - Check that odbc.ini is working.  Open Stata and run the following:

    set odbcmgr unixodbc
    odbc load, exec("select * from crsp.dsf limit 10") dsn("wrds-postgres")
    list

You should see some cusips and other stuff.  If that looks good, then you should be able to run master.do

#### Setting up Rstudio to access to WRDS

For a handful of predictors, we use R scripts to download CRSP data directly. WRDS provides [instructions for setting up WRDS to work via RStudio on your computer](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-r/r-from-your-computer/).  These predictors are optional though, so you can skip this step if you don't need the full dataset.


### 2. FRED

To download macroeconomic data required for some signals, you will need to [request an API key from FRED](https://research.stlouisfed.org/docs/api/api_key.html). Before you run the download scripts, you need to save your API key in Stata (either via the context menu or via `set fredkey`).  See [this Stata blog entry](
https://blog.stata.com/2017/08/08/importing-data-with-import-fred/) for more details.

----

## Contribute

Please let us know if you find typos in the code or think that we should add additional signals. You can let us know about any suggested changes via pull requests for this repo. We will keep the code up to date for other researchers to use it.

*Git Integration* 

If you use RStudio, take a look at [Hendrik Bruns' guide](https://www.hendrikbruns.tk/post/using-rstudio-and-git-version-control/) to set up version control.

As a stand-alone client for Windows, we recommend [Sourcetree](https://www.sourcetreeapp.com/).
