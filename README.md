# Open source cross sectional asset pricing

This repo accompanies our paper:
[Chen and Zimmermann (2020), "Open source cross-sectional asset pricing"](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3604626)

If you use data or code based on our work, please cite the paper: [Bibtex entry](https://drive.google.com/open?id=1eP-Tuvmcbs5A7073d_9g2wQbvitqfdPz)

## Data

If you are mostly interested in working with the data, we provide benchmark signal and portfolio returns in separate files for direct download. 

You can access the benchmark data [here](https://drive.google.com/open?id=1oeX3PVd5KxKqnQuVuPdRwORrqyt1WnJo).

The folder contains 4 files

- Portfolio Returns Benchmark Signals: portbase.zip
- Portfolio Returns Additional Signals: portadditional.zip
- Firm-level benchmark signals: signalbase.zip
- Firm-level additional signals: signaladditional.zip

For reference to individual signals, their acronyms and construction please see the [online appendix to our paper](https://drive.google.com/open?id=1vXRzjxYucXZV-tgLxM26fvRZ5zKvlBXH) and the file **SignalDocumentation.xls** that is part of this repo.


## Code 

The code is separated into different files that download and prepare the data, and construct signals and portfolios. Please see the file **runEverything.txt** to get an overview of how the entire code can be run. The current code does some parts in R and some in Stata, so you will need both to run everything.

Code to construct trading costs from TAQ data is provided separately and can be downloaded [here](https://drive.google.com/open?id=1W256-g-RxqOZBjNtkSJuuWXUqHZEYHsM).

## Data access

To download raw data from the original sources, you will need access to WRDS. At a minimum, you will need access to the following databases:

- CRSP
- Compustat
- IBES

WRDS provides [instructions for setting up WRDS to work via RStudio on your computer](https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-r/r-from-your-computer/)

## Contribute

Please let us know if you find typos in the code or think that we should add additional signals. You can let us know about any suggested changes via pull requests for this repo. We will keep the code up to date for other researchers to use it.

*Git Integration* 

If you use RStudio, take a look at [Hendrik Bruns' guide](https://www.hendrikbruns.tk/post/using-rstudio-and-git-version-control/) to set up version control.

As a stand-alone client for Windows, we recommend [Sourcetree](https://www.sourcetreeapp.com/).
