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

If you are mostly interested in working with the data, we provide signal and portfolio returns in separate files for direct download at the dedicated data page [here](https://sites.google.com/site/chenandrewy/open-source-ap).

----

## Code 

The code is separated into three parts:

1. **Signals**: Contains code to produce stock-level signals (characteristics)
2. **Portfolios**: Contains code to produce portfolio returns
3. **Shipping**: You shouldn't need this, this is used by us for replicable data sharing and data checking

### 1. Signals

The **Signals code** provides scripts for downloading data from WRDS and elsewhere (`DataDownloads`), creating stock-level predictors (`Predictors`), and creating stock-level signals that were not shown to predict (`Placebos`). `master.do` runs all of the files.

Setup: (tbc)

but you will need to set paths pointing to your project folder and your WRDS connection (see below).  Most of this code is written in Stata.

*Optional (i.e. code is modular and will work even if you do not do that)*: To construct signals that rely on IBES, 13F, TAQ or OptionMetrics data run the SAS scripts in `PrepScripts` on the WRDS server. See the [WRDS instructions](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-sas/) for different ways to run these scripts on the WRDS server. Copy the output of those scripts to `Signals/Data/Prep`. Code to construct trading costs from TAQ data is provided separately and can be downloaded [here](https://drive.google.com/open?id=1W256-g-RxqOZBjNtkSJuuWXUqHZEYHsM).

*See **Data access** part of the readme below for some data access steps that you need to complete before you can run the code.*


### 2. Portfolios

The **Portfolios** code constructs portfolio returns from the signal files. `master.R` runs all of the files, but once again you need to set the paths.

All of this code is written in R.  So if you do not have access to Stata, you can still use the portfolio code by downloading the individual signal csvs from the data page and running `master.R`.  More detailed instructions on how to skip to the portfolio code will be coming when we get the chance.

### 3. Shipping

This code just zips up selected files, makes some quality checks, and copies files for uploading to Gdrive for sharing.  You shouldn't need to use this but we keep it with the rest of the code to stay organized.

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

## Stata and R Setup

Stata code was tested on Ubuntu 18.04.5 running Stata 16.1.

R code was tested on Windows 10, Rstudio Version 1.4.1106, R Version 4.0.5 (2021-21-15), and Rtools 4.0.0.  To install: 
1. Download and install most recent R from https://cran.r-project.org/bin/windows/base/old/
2. Download and install most Rtools from https://cran.r-project.org/bin/windows/Rtools/history.html
3. Download and install Rstudio from https://www.rstudio.com/products/rstudio/download/
4. Add Rtools to path by running in R: writeLines('PATH="${RTOOLS40_HOME}\\usr\\bin;${PATH}"', con = "~/.Renviron") 
	see	https://cran.r-project.org/bin/windows/Rtools/


----

## Contribute

Please let us know if you find typos in the code or think that we should add additional signals. You can let us know about any suggested changes via pull requests for this repo. We will keep the code up to date for other researchers to use it.

*Git Integration* 

If you use RStudio, take a look at [Hendrik Bruns' guide](https://www.hendrikbruns.tk/post/using-rstudio-and-git-version-control/) to set up version control.

As a stand-alone client for Windows, we recommend [Sourcetree](https://www.sourcetreeapp.com/).
