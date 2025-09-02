# Overview
Code for high-frequency direct trading costs used in "Zeroing in on the Expected Returns of Anomalies" by Andrew Y. Chen and Mihail Velikov.

Generates permno-month effective bid-ask spreads for in csv form using data from 
* Daily TAQ (via WRDS Intraday Indicators)
* Monthly TAQ (via WRDS Intraday Indicators)
* ISSM (from the raw high-frequency ISSM data)
* CRSP (for permnos)

This data covers 
* Essentially all transactions on the NYSE and AMEX from 1983-present
* Almost all transactions on NASDAQ from 1987-present
  * About 8 months of NASDAQ data between 1987-1991 are missing from ISSM (also found missing by Barber, Odean, and Zhu 2008)

For further details, please see the paper

https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3073681

For the code that generates low-frequency costs, portfolio implementations, etc, please see

https://github.com/velikov-mihail/Chen-Velikov


# Thank Yous
* Craig Holden and Stacey Jacobsen.  The ISSM code is a minor adaptation of the code for their 2014 JF, which they graciously shared.
* Rabih Moussawi.  We use his TAQ-CRSP link macro to merge MTAQ permnos
* WRDS Support for their assistance with understanding the IID data

# Instructions
upload to wrds server, run "qsub main.sh" at the linux prompt.

Takes about 1 hour, mostly for the issm data.

main.sh makes folders
* ~/temp_output/ - output data (csv format) goes here 
* ~/temp_log/ - sas log files go here	

helful wrds cloud commands:
* qstat: check status of jobs
* qdel [job number]: delete a job.
	
# Other Details
* Previous versions of the paper used Holden and Jacobsen's code to construct spreads directly from TAQ (instead of WRDS IID).  This led to very similar results, and since the WRDS IID code makes everything so much faster and doesn't hog up server capacity (and is probably better for the environment), we just went with WRDS IID in the 2021 revision.
* The code converts permno-day spreads to permno-month spreads two ways
  1. Equal-weight average across days.  This is the data used in the paper.
  2. Using the last observation of the month.  This is arguably more appropriate given that the CRSP gross returns are month end to month end.  But the results look mostly the same and previous papers use averaging so we went with that.  
      * I spent some time arguing with a friend the other day about whether scholars should do what's right or what the literature does.  He's a real hardliner for doing what's right (shrug).  I have a more grey view that there are tradeoffs between (lit-wide) replicability and transparency, and in this case the replicability and transparency issues won out.  
