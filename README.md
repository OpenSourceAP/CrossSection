# Open source cross sectional asset pricing

This repo accompanies our paper:
[Chen and Zimmermann (2020), "Open source cross-sectional asset pricing"](SSRN link)

## Code 

The code is separated into different files that download and prepare the data, and construct signals and portfolios. Please see the file **runEverything.txt** to get an overview of how the entire code can be run. The current code does some parts in R and some in Stata, so you will need both to run everything.


## Data access

To download data, you will need access to WRDS. At a minimum, you will need access to the following databases:

- CRSP
- Compustat
- IBES

Here are instructions for setting up WRDS to work via RStudio on your computer: https://wrds-www.wharton.upenn.edu/pages/support/programming-wrds/programming-r/r-from-your-computer/

## Contribute

Please let us know if you find typos in the code or think that we should add additional signals. You can let us know about any suggested changes via pull requests for this repo. We will keep the code up to date for other researchers to use it.

*Git Integration* 

If you use RStudio, take a look at [Hendrik Bruns' guide](https://www.hendrikbruns.tk/post/using-rstudio-and-git-version-control/) to set up version control.

As a stand-alone client for Windows, we recommend [Sourcetree](https://www.sourcetreeapp.com/).