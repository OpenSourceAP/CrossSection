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

More details are below

### `Signals/pyCode` Instructions

**1. Set up for Creating Signals (Python and R)**

* Install Python dependencies:
  ```bash
  cd Signals/pyCode/
  pip install -r requirements.txt
  ```
* Install required R packages: `googledrive` (pulls in `gargle`), used by `Signals/pyCode/`. In R: `install.packages("googledrive")`.
* **Google Drive login (for 7 OptionMetrics signals).** While `PATCH_OPTIONM_IV = True` in `Signals/pyCode/config.py` (see [#156](https://github.com/OpenSourceAP/CrossSection/issues/156)), CPVolSpread, dCPVolSpread, dVolCall, dVolPut, skew1, SmileSlope and RIVolSpread are downloaded from our 2023 data release with your Google account. Once, from `Signals/pyCode/`, start R interactively and run `source("gdrive_login.R")`. Open the printed URL, sign in, tick "See and download all your Google Drive files", and paste the code back into R. The login is cached, so later pipeline runs are headless.
  - Any Google account works, since the files are public. Access is read-only.
  - Skipping the login only loses those seven signals; `master.py` warns and asks before it starts.
* Copy `Signals/pyCode/dotenv.template` to `Signals/pyCode/.env` and add your WRDS and FRED credentials.
  - For FRED credentials, request an [API key from FRED](https://research.stlouisfed.org/docs/api/api_key.html)

**2. (Optional) Generate Prep Data**

This is only necessary for a handful of signals

If you have bash:
* from `Signals/pyCode/`
  - run `bash prep1_run_on_wrds.sh` to copy the prep scripts to the WRDS Cloud
  - the submission runs four concurrent array tasks of about 1 hour each: OptionMetrics volume; the other OptionMetrics scripts; high-frequency spreads; and 13F plus low-frequency spreads. Scripts within each task run sequentially
  - wait for all four tasks to finish (about 1 hour)
    - use qstat to check whether any task is still running
    - if impatient, check most recent file in `~/temp_prep/log/` on WRDS server.  
  - run `bash prep2_dl_from_wrds.sh` to download the prep data from the WRDS Cloud to `Signals/pyData/Prep/`

You can alternatively upload to the WRDS Cloud manually, ssh into WRDS, run `qsub run_all_prep.sh`, and then manually download the prep data.

**3. Run the Signals Code**

`master.py` runs the end-to-end Python pipeline. It calls the staged scripts in:

* `DataDownloads/` downloads data from WRDS and elsewhere and writes to `Signals/pyData/`
* `SignalMasterTable.py` builds the join table used across predictors
* `Predictors/` constructs stock-level predictors and outputs to `Signals/pyData/Predictors/`
* `Placebos/` constructs "not predictors" and "indirect evidence" signals and outputs to `Signals/pyData/Placebos/`

**To run:**
```bash
cd Signals/pyCode/
python master.py
```

The orchestrator blocks are written to keep running even if a particular download fails (for example due to a missing subscription) so you get as much data as possible. You can track progress in `Signals/Logs/`.


### `Portfolios/Code` Instructions

`master.R` runs everything. It:

1. Takes in signal data located in `Signals/pyData/Predictors/` and `Signals/pyData/Placebos/` (or `Signals/Data/...` for the legacy Stata signals)
2. Takes in CRSP v2 (CIZ) data from `Signals/pyData/Intermediate/` (see below)
3. Outputs portfolio data to `Portfolios/Data/Portfolios/`
4. Outputs exhibits found in the paper to `Results/`

It also uses `SignalDoc.csv` as a guide for how to run the portfolios.

**To run:**
* Option 1 - Command line:
  ```bash
  cd Portfolios/Code/
  Rscript master.R
  ```
* Option 2 - RStudio: Open `master.R` in RStudio and click "Source" or press Ctrl+Shift+S (Cmd+Shift+S on Mac)

**Before running:** You must set `pathProject` in `master.R` (line 30) to your project root directory (where `SignalDoc.csv` is located). If using RStudio, `pathProject = paste0(getwd(), '/')` should work automatically.

By default the code skips the daily portfolios (`skipdaily = T`), and takes about 8 hours, assuming you examine all 300 or so signals.  However, the baseline portfolios (based on predictability results in the original papers) will be done in just 30 minutes. You can keep an eye on how it's going by checking the csvs outputted to `Portfolios/Data/Portfolios/`.  Every 30 minutes or so the code should output another set of portfolios.  Adding the daily portfolios (`skipdaily = F`) takes an additional 12ish hours.

#### CRSP data for the portfolios

The portfolio code does not download anything itself. It reads the CRSP v2 (CIZ) files that `Signals/pyCode/` writes to `Signals/pyData/Intermediate/` (`monthlyCRSP.parquet`, and `dailyCRSP.parquet` if `skipdaily = F`), plus the three predictors built directly from CRSP (`Price`, `Size`, `STreversal`). These are the only portfolio inputs that cannot be downloaded from the data page, because CRSP data cannot be redistributed.

If you have run the full signals pipeline (`python master.py`), you already have them. If you only want to build portfolios from downloaded signals, run just the CRSP part of the pipeline:

```bash
cd Signals/pyCode/
pip install -r requirements.txt     # once
cp dotenv.template .env             # once; add your WRDS credentials
python crsp_only.py                 # add --skip-daily if master.R will run with skipdaily = T
```

This downloads monthly (and daily) CRSP and writes `Price.csv`, `Size.csv`, `STreversal.csv` to `Signals/pyData/Predictors/`. `master.R` stops with a message pointing to this command if any of these files are missing.

#### Minimal Setup

To get started quickly, `master.R` will create portfolios for Price, Size, and STreversal in `Portfolios/Data/Portfolios/` after running `crsp_only.py` as above.
To add other signals:

* Run the code in `Signals/pyCode/` (see above), or
* Download `Firm Level Characteristics/Full Sets/PredictorsIndiv.zip` and `Firm Level Characteristics/Full Sets/PlacebosIndiv.zip` via the [data page](https://www.openassetpricing.com) and unzip to `Signals/pyData/Predictors/` and `Signals/pyData/Placebos/`, or
* Download only some selected csvs via the [data page](https://www.openassetpricing.com) and place them in `Signals/pyData/Predictors/` (e.g. just download `BM.csv`, `AssetGrowth.csv`, and `EarningsSurprise.csv`).


### `Shipping/Code` Instructions

This code zips up the data, makes some quality checks, and copies files for uploading to Gdrive.  You shouldn't need to use this but we keep it with the rest of the code for replicability.




