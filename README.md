# Open source cross sectional asset pricing

This repo accompanies our paper:
[Chen and Zimmermann (2021), "Open source cross-sectional asset pricing"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626)

If you use data or code based on our work, please cite the paper: 

~~~
@article{ChenZimmermann2021,
  title={Open Source Cross Sectional Asset Pricing},
  author={Chen, Andrew Y. and Tom Zimmermann},
  journal={Critical Finance Review},
  year={2022},
  pages={207-264},
  volume={11},
  number={2}
}
~~~


----

## Data

If you are mostly interested in working with the data, we provide both stock-level signals (characteristics) and a bunch of different portfolio implementations for direct download at [the dedicated data page](https://www.openassetpricing.com). Please see the data page for answers to [FAQs](https://www.openassetpricing.com/faq/).

However, this repo may still be useful for understanding the data.  For example, if you want to know exactly how we construct BrandInvest (Belo, Lin, and Vitorino 2014), you can just open up `BrandInvest.py` in the repo's webpage for [Signals/pyCode/Predictors/](https://github.com/OpenSourceAP/CrossSection/tree/master/Signals/pyCode/Predictors)

----

## Code 

The code is separated into three folders:

1. `Signals/pyCode/` Downloads data from WRDS and elsewhere, constructs stock-level signals in Python, and outputs to `Signals/pyData/`.
2. `Portfolios/Code/` Takes in signals and outputs portfolios to `Portfolios/Data/`.  Entirely in R.
3. `Shipping/Code/` Used to prepare data for sharing.

We separate the code so you can choose which parts you want to run.  If you only want to create signals, you can run the files in `Signals/pyCode/` and then do your thing.  If you just want to create portfolios, you can skip the signal generation by directly downloading its output via the [data page](https://www.openassetpricing.com/).  The whole thing is about 15,000 lines, so you might want to pick your battles.

More details are below.

### 1. Signals/pyCode/

`master.py` runs the end-to-end Python pipeline. It calls the staged scripts in:

* `DataDownloads/` downloads data from WRDS and elsewhere and writes to `Signals/pyData/`
* `SignalMasterTable.py` builds the join table used across predictors
* `Predictors/` constructs stock-level predictors and outputs to `Signals/pyData/Predictors/`
* `Placebos/` constructs "not predictors" and "indirect evidence" signals and outputs to `Signals/pyData/Placebos/`

The orchestrator blocks are written to keep running even if a particular download fails (for example due to a missing subscription) so you get as much data as possible. You can track progress in `Signals/Logs/`.

#### Minimal Setup

1. From `Signals/pyCode/`, create a Python 3 virtual environment (e.g. `python3 -m venv .venv`) and install the requirements via `pip install -r requirements.txt` after activating the environment. `set_up_pyCode.py` automates these steps if you prefer.
2. Copy `dotenv.template` to `.env` and populate credentials such as `WRDS_USERNAME`, `WRDS_PASSWORD`, and any other keys you need (e.g. `FRED_API_KEY`).
3. Run the full pipeline with `python master.py` (from inside `Signals/pyCode/`). You can also run `01_DownloadData.py` and `02_CreatePredictors.py` individually if you just need part of the workflow.
4. Outputs are written to `Signals/pyData/`, and detailed logs are saved under `Signals/Logs/`.

#### Optional Setup

The minimal setup produces the vast majority of signals. Thanks to exception handling, the pipeline will keep going even if a particular source is unavailable.

To reproduce every signal:

* For IBES, 13F, OptionMetrics, and bid-ask spread signals, run the helper scripts in `Signals/pyCode/PrepScripts/` (many are designed for WRDS Cloud) and place the resulting files in `Signals/pyData/Prep/`.
* For signals that use the VIX, inflation, or broker-dealer leverage, request an [API key from FRED](https://research.stlouisfed.org/docs/api/api_key.html) and add `FRED_API_KEY` to `.env` before running the download scripts.
* For signals that rely on patent citations, BEA input-output tables, or Compustat customer data, ensure that `Rscript` is available on your system because some helper scripts shell out to R.

### 2. Signals/LegacyStataCode/

`master.do` runs the original Stata pipeline.  It calls every .do file in the following folders:

* `DataDownloads/` downloads data from WRDS and elsewhere
* `Predictors/` constructs stock-level predictors and outputs to `Signals/Data/Predictors/`
* `Placebos/` constructs "not predictors" and "indirect evidence" signals and outputs to `Signals/Data/Placebos/`

`master.do` employs exception handling so if any of these .do files errors out (due to lack of a subscription, code being out of date, etc.), it'll keep running and output as much as it can.

The full run takes roughly 24 hours, but the predictors will be done much sooner, probably within 12 hours.  You can keep track of how it's going by checking out the log files in `Signals/Logs/`.

#### Minimal Setup

In `master.do`, set `pathProject` to the root directory of the project (where `SignalDoc.csv` is located) and `wrdsConnection` to the name you selected for your ODBC connection to WRDS (a.k.a. dsn).

If you don't have an ODBC connection to WRDS, you'll need to set it up.  WRDS provides instructions for [Windows users](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-stata/stata-from-your-computer/) and for [WRDS cloud users](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-stata/stata-wrds-cloud/).  Note that `wrdsConnection` (name of the ODBC connection) in the WRDS cloud example is `"wrds-postgres"`.  If neither of these solutions works, please see our [troubleshooting wiki](https://github.com/OpenSourceAP/CrossSection/wiki/Troubleshooting).

#### Optional Setup

The minimal setup will allow you to produce the vast majority of signals.  And due to the exception handling in `master.do`, the code will run even if you're not set up to produce the remainder.

But if you want signals that use IBES, 13F, OptionMetrics, FRED, or a handful of other random signals, you'll want to do the following:

* For IBES, 13F, OptionMetrics, and bid-ask-spread signals: Run `Signals/LegacyStataCode/PrepScripts/master.sh` on the WRDS Cloud, and download the output to `Signals/Data/Prep/`.  The most important outputs from this optional setup are `iclink.csv` and `oclink.csv`, which allow for merging of IBES, OptionMetrics, and CRSP data.  The code here relies heavily on work by Luis Palacios, Rabih Moussawi, Denys Glushkov, Stacey Jacobsen, Craig Holden, Mihail Velikov, Shane Corwin, and Paul Schultz.

* For signals that use the VIX, inflation, or broker-dealer leverage, you will need to [request an API key from FRED](https://research.stlouisfed.org/docs/api/api_key.html). Before you run the download scripts, save your API key in Stata (either via the context menu or via `set fredkey`).  See [this Stata blog entry](https://blog.stata.com/2017/08/08/importing-data-with-import-fred/) for more details.

* For signals that use patent citations, BEA input-output tables, or Compustat customer data, the code uses Stata to call R scripts, and thus this may need some setup.  If you're on a Windows machine, you will need to point `master.do` to your R installation, by setting `RSCRIPT_PATH` to the path of `Rscript.exe`.  If you're on Linux, you will need to just make sure that the `rscript` command is executable from the shell.

### 3. Portfolios/Code/

`master.R` runs everything. It:

1. Takes in signal data located in `Signals/Data/Predictors/` or `Signals/pyData/Predictors/`, and `Signals/Data/Placebos/` or `Signals/pyData/Placebos/`
2. Outputs portfolio data to `Portfolios/Data/Portfolios/`
3. Outputs exhibits found in the paper to `Results/`

It also uses `SignalDoc.csv` as a guide for how to run the portfolios.

By default the code skips the daily portfolios (`skipdaily = T`), and takes about 8 hours, assuming you examine all 300 or so signals.  However, the baseline portfolios (based on predictability results in the original papers) will be done in just 30 minutes. You can keep an eye on how it's going by checking the csvs outputted to `Portfolios/Data/Portfolios/`.  Every 30 minutes or so the code should output another set of portfolios.  Adding the daily portfolios (`skipdaily = F`) takes an additional 12ish hours.

#### Minimal Setup

All you need to do is set `pathProject` in `master.R` to the project root directory (where `SignalDoc.csv` is).  Then `master.R` will create portfolios for Price, Size, and STreversal in `Portfolios/Data/Portfolios/`.

#### Probable Setup

You probably want more than Price, Size, and STreversal portfolios, and so you probably want to set up more signal data before you run `master.R`.  

There are a couple ways to set up this signal data:

* Run the code in `Signals/pyCode/` (see above) or, if you prefer the original implementation, `Signals/LegacyStataCode/`.
* Download `Firm Level Characteristics/Full Sets/PredictorsIndiv.zip` and `Firm Level Characteristics/Full Sets/PlacebosIndiv.zip` via the [data page](https://sites.google.com/site/chenandrewy/open-source-ap) and unzip to `Signals/Data/Predictors/` and `Signals/Data/Placebos/`.
* Download only some selected csvs via the [data page](https://sites.google.com/site/chenandrewy/open-source-ap) and place in `Signals/Data/Predictors/` (e.g. just download `BM.csv`, `AssetGrowth.csv`, and `EarningsSurprise.csv` and put them in `Signals/Data/Predictors/`).


### 4. Shipping/Code/

This code zips up the data, makes some quality checks, and copies files for uploading to Gdrive.  You shouldn't need to use this but we keep it with the rest of the code for replicability.

----

## Contribute

Please let us know if you find typos in the code or think that we should add additional signals. You can let us know about any suggested changes via pull requests for this repo. We will keep the code up to date for other researchers to use it.

