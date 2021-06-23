# Open source cross sectional asset pricing

This repo accompanies our paper:
[Chen and Zimmermann (2021), "Open source cross-sectional asset pricing"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626)

If you use data or code based on our work, please cite the paper: 

~~~
@article{ChenZimmermann2021,
  title={Open Source Cross Sectional Asset Pricing},
  author={Chen, Andrew Y. and Tom Zimmermann},
  journal={Critical Finance Review},
  year={Forthcoming}
}
~~~


----

## Data

If you are mostly interested in working with the data, we provide both stock-level signals (characteristics) and a bunch of different portfolio implementations for direct download at [the dedicated data page](https://www.openassetpricing.com).  

However, this repo may still be useful for understanding the data.  For example, if you want to know exactly how we construct BrandInvest (Belo, Lin, and Vitorino 2014), you can just open up `BrandInvest.do` in the repo's webpage for [Signals/Code/Predictors/](https://github.com/OpenSourceAP/CrossSection/tree/master/Signals/Code/Predictors)

----

## Code 

The code is separated into three folders:

1. `Signals/Code/` Downloads data from WRDS and elsewhere.  Constructs stock-level signals (characteristics) and ouputs to `Signals/Data/`.  Mostly written in Stata.
2. `Portfolios/Code/` Takes in signals from `Signals/Data/` and outputs portfolios to `Portfolios/Data/`.  Entirely in R.
3. `Shipping/Code/` You shouldn't need this.  We use this to prepare data for sharing.

We separate the code so you can choose which parts you want to run.  If you only want to create signals, you can run the files in `Signals/Code/` and then do your thing.  If you just want to create portfolios, you can skip `Signals/Code/` by directly downloading its output via the [data page](https://www.openassetpricing.com/).  The whole thing is about 15,000 lines, so you might want to pick your battles.

More details are below.

### 1. Signals/Code/

`master.do` runs everything.  It calls every .do file in the following folders:

* `DataDownloads/` downloads data from WRDS and elsewhere
* `Predictors/` construct stock-level predictors and outputs to `Signals/Data/Predictors/`
* `Placebos/` constructs "not predictors" and "indirect evidence" signals and outputs to `Signals/Data/Placebos/` 

`master.do` employs exception handling so if any of these .do files errors out (due to lack of a subscription, code being out of date, etc), it'll keep running and output as much as it can.

The whole thing takes roughly 24 hours, but the predictors will be done much sooner, probably within 12 hours.  You can keep track of how it's going by checking out the log files in `Signals/Logs/`.

#### Minimal Setup

In master.do, set `pathProject` to the root directory of the project (where `SignalDocumentation.xlsx` is located) and `wrdsConnection` to the name you selected for your ODBC connection to WRDS (a.k.a. dsn).

If you don't have an ODBC connection to WRDS, you'll need to set it up.  WRDS provides instructions for [Windows users](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-stata/stata-from-your-computer/) and for [WRDS cloud users](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-stata/stata-wrds-cloud/).  Note that `wrdsConnection` (name of the ODBC connection) in the WRDS cloud example is `"wrds-postgres"`.  If neither of these solutions works, please see our [troubleshooting wiki](https://github.com/OpenSourceAP/CrossSection/wiki/Troubleshooting).


#### Optional Setup

The minimal setup will allow you to produce the vast majority of signals.  And due to the exception handling in `master.do`, the code will run even if you're not set up to produce the remainder.

But if you want signals that use IBES, 13F, OptionMetrics, FRED, or a handful of other random signals, you'll want to do the following:

* For IBES signals, 13F signals, and BidAskSpread: Run `Signals/Code/PrepScripts/master.sas` on the WRDS Cloud, and download the output to `Signals/Data/Prep/`.  See `master.sas` and [WRDS-Cloud SAS instructions](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-sas/) for more details.   <ins>The most important part of this optional setup is the construction of `iclink.csv`</ins>, which allows for merging of IBES and CRSP data.

* For signals that use the VIX, inflation, or broker-dealer leverage, you will need to [request an API key from FRED](https://research.stlouisfed.org/docs/api/api_key.html). Before you run the download scripts, save your API key in Stata (either via the context menu or via `set fredkey`).  See [this Stata blog entry](
https://blog.stata.com/2017/08/08/importing-data-with-import-fred/) for more details.

* For signals that use patent citations, BEA input-output tables, or Compustat customer data, you will need to point `master.do` to your R installation, by setting `RSCRIPT_PATH` to the path of `Rscript.exe`.  

* There is one placebo that is based on effective spreads from TAQ (BidAskTAQ).  Hou and Lou (2016) find that this signal is insignificant in a multivariate regression, and consistent with this we find the long-short portfolio generates a t-stat of 0.4 in Hou and Lou's 1984-2012 sample.  This is also consistent with the fact that BidAskSpread based on Corwin-Schultz doesn't predict returns well after the publication of Amihud and Mendelsohn (1986).  Anyway, you don't really need to produce this signal, but if you really want to, Chen and Velikov (2020) provide code based on Holden and Jacobsen [here](https://sites.google.com/site/chenandrewy/code), and WRDS has recently provided a way to download these spreads directly.


### 2. Portfolios/Code/

`master.R` runs everything. It:

1. Takes in signal data located in `Signals/Data/Predictors/` and `Signals/Data/Placebos/`
2. Outputs portfolio data to `Portfolios/Data/Portfolios/`
3. Outputs exhibits found in the paper to `Results/`

It also uses `SignalDocumentation.xlsx` as a guide for how to run the portfolios.

By default the code skips the daily portfolios (`skipdaily = T`), and takes about 8 hours, assuming you examine all 300 or so signals.  However, the baseline portfolios (based on predictability results in the original papers) will be done in just 30 minutes. You can keep an eye on how it's going by checking the csvs outputted to `Portfolios/Data/Portfolios/`.  Every 30 minutes or so the code should output another set of portfolios.  Adding the daily portfolios (`skipdaily = F`) takes an additional 12ish hours.

#### Minimal Setup

All you need to do is set `pathProject` in `master.R` to the project root directory (where `SignalDocumentation.xlsx` is).  Then `master.R` will create portfolios for Price, Size, and STreversal in `Portfolios/Data/Portfolios/`.

#### Probable Setup

You probably want more than Price, Size, and STreversal portfolios, and so you probably want to set up more signal data before you run `master.R`.  

There are a couple ways to set up this signal data:

* Run the code in `Signals/Code/` (see above)
* Download `Firm Level Characteristics/Full Sets/PredictorsIndiv.zip` and `Firm Level Characteristics/Full Sets/PlacebosIndiv.zip` via the [data page](https://sites.google.com/site/chenandrewy/open-source-ap) and unzip to `Signals/Data/Predictors/` and `Signals/Data/Placebos/`
* Download only some selected csvs via the [data page](https://sites.google.com/site/chenandrewy/open-source-ap) and place in `Signals/Data/Predictors/` (e.g. just download `BM.csv`, `AssetGrowth.csv`, and `EarningsSurprise.csv` and put them in `Signals/Data/Predictors/`).


### 3. Shipping/Code/

This code zips up the data, makes some quality checks, and copies files for uploading to Gdrive.  You shouldn't need to use this but we keep it with the rest of the code for replicability.

----

## Stata and R Setup

Stata code was tested on both Windows and Linux.  Linux was Ubuntu 18.04.5 running Stata 16.1.

R code was tested on 

* Windows 10, Rstudio Version 1.4.1106, R 4.0.5, and Rtools 4.0.0
* Ubuntu 18.04.5, EMACS 26.1, ESS 17.11, and R 4.0.2

To install the Windows R setup

1. Download and install R from https://cran.r-project.org/bin/windows/base/old/
2. Download and install Rtools from https://cran.r-project.org/bin/windows/Rtools/history.html
3. Download and install Rstudio from https://www.rstudio.com/products/rstudio/download/
4. Add Rtools to path by running in R: `writeLines('PATH="${RTOOLS40_HOME}\\usr\\bin;${PATH}"', con = "~/.Renviron")` 
	see	https://cran.r-project.org/bin/windows/Rtools/


----

## Git Integration
If you use RStudio, take a look at [Hendrik Bruns' guide](https://www.hendrikbruns.tk/post/using-rstudio-and-git-version-control/) to set up version control.

As a stand-alone client for Windows, we recommend [Sourcetree](https://www.sourcetreeapp.com/).

If you use Git, you should definitely add the following lines to .gitignore:

```
Signals/Data/**
Shipping/Data/**
Portfolios/Data/**
```

These folders contain a ton of data and will make Git slow to a crawl or crash.



----

## Contribute

Please let us know if you find typos in the code or think that we should add additional signals. You can let us know about any suggested changes via pull requests for this repo. We will keep the code up to date for other researchers to use it.



