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

### 2. Portfolios/Code/

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

* Run the code in `Signals/pyCode/` (see above).
* Download `Firm Level Characteristics/Full Sets/PredictorsIndiv.zip` and `Firm Level Characteristics/Full Sets/PlacebosIndiv.zip` via the [data page](https://sites.google.com/site/chenandrewy/open-source-ap) and unzip to `Signals/Data/Predictors/` and `Signals/Data/Placebos/`.
* Download only some selected csvs via the [data page](https://sites.google.com/site/chenandrewy/open-source-ap) and place in `Signals/Data/Predictors/` (e.g. just download `BM.csv`, `AssetGrowth.csv`, and `EarningsSurprise.csv` and put them in `Signals/Data/Predictors/`).


### 3. Shipping/Code/

This code zips up the data, makes some quality checks, and copies files for uploading to Gdrive.  You shouldn't need to use this but we keep it with the rest of the code for replicability.

----

## Contribute

Please let us know if you find typos in the code or think that we should add additional signals. You can let us know about any suggested changes via pull requests for this repo. We will keep the code up to date for other researchers to use it.
