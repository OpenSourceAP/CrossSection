# Run: Rscript Portfolios/tests/test_portfolio_function.R (from any working directory).
# Inputs: installed R dependencies and Portfolios/Code/01_PortfolioFunction.R; no research data.
# Outputs: assertions on a tiny synthetic signal and returns file, deleted on completion.

suppressPackageStartupMessages({
  library(tidyverse)
  library(data.table)
  library(fst)
})
test_file <- sub("^--file=", "", grep("^--file=", commandArgs(), value = TRUE))[1L]
code_dir <- normalizePath(file.path(dirname(test_file), "..", "Code"))
source(file.path(code_dir, "01_PortfolioFunction.R"))

# Fixtures live in R's session temp directory, which R deletes on exit.
temporary <- tempfile("portfolio-function-")
dir.create(temporary)
pathPredictors <- pathCRSPPredictors <- pathPlacebos <- pathtemp <- paste0(temporary, "/")
feed.verbose <- FALSE

# Signal in 2020-01 for stocks 1-4; returns in 2020-02 (the lagged month) for
# stocks 1-5. Stock 5 has no signal and stock 2 has a missing return on day 2.
write.csv(data.frame(permno = 1:4, yyyymm = 202001, Sig = c(1, 2, 3, 4)),
          file.path(temporary, "Sig.csv"), row.names = FALSE)
crspinfo <- data.table(permno = 1:5, yyyymm = 202001, exchcd = 1)
returns <- CJ(permno = 1:5, date = as.Date(c("2020-02-03", "2020-02-04")))
returns[, `:=`(yyyymm = 202002, ret = permno / 100 + as.numeric(date - min(date)) / 1000,
               melag = permno * 10, passgain = 1 + permno / 50)]
returns[permno == 2 & date == max(date), ret := NA]
crspretpath <- file.path(temporary, "crspret.fst")
write_fst(returns, crspretpath)

# Expected portfolio returns, computed directly: median split, port 01 = stocks
# 1-2, port 02 = stocks 3-4, LS = 02 - 01.
expected <- function(weight) {
  x <- returns[permno <= 4 & !is.na(ret)][, port := if_else(permno <= 2, 1L, 2L)]
  x[, w := weight(.SD)]
  x[, .(ret = weighted.mean(ret, w), Nlong = .N), by = .(port, date)][order(port, date)]
}
check <- function(weight, ...) {
  got <- signalname_to_ports("Sig", q_cut = 0.5, ...)
  want <- expected(weight)
  ports <- got %>% filter(port != "LS") %>% arrange(port, date)
  ls <- got %>% filter(port == "LS") %>% arrange(date)
  stopifnot(identical(ports$port, sprintf("%02d", want$port)),
            isTRUE(all.equal(ports$ret, want$ret)),
            identical(ports$Nlong, want$Nlong),
            isTRUE(all.equal(ls$ret, want[port == 2]$ret - want[port == 1]$ret)))
}

check(function(x) 1)                                          # equal weights
check(function(x) x$melag, sweight = "VW")                    # value weights
check(function(x) x$passgain, passive_gain = TRUE)            # EW with passive gains
check(function(x) x$melag * x$passgain, sweight = "VW", passive_gain = TRUE)

# Rereading gives the same answer on repeated calls (no leftover columns), and
# the returns file is never modified.
check(function(x) 1)
stopifnot(identical(read_fst(crspretpath, as.data.table = TRUE), returns))

# The by-reference join assumes one signal per stock-month.
write.csv(data.frame(permno = c(1:4, 1), yyyymm = 202001, Sig = c(1, 2, 3, 4, 5)),
          file.path(temporary, "Sig.csv"), row.names = FALSE)
stopifnot(inherits(tryCatch(signalname_to_ports("Sig", q_cut = 0.5), error = identity), "error"))

message("Portfolio function tests passed.")
