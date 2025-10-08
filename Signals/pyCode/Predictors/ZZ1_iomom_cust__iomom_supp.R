## ABOUTME: Calculate Input-Output Momentum following Menzly-Ozbas methodology
## ABOUTME: Creates supplier and customer momentum signals from BEA IO tables and CRSP returns

## Input-Output Momentum Signal Construction
## Based on Menzly-Ozbas (2010) methodology with 5-year lag from survey to release
## Uses BEA Input-Output tables (pre-1997 and 1997-present) with ~70 industries
## Supplier momentum: industry's returns weighted by purchases from other industries (Use table)
## Customer momentum: industry's returns weighted by sales to other industries (Make/Supply table)

# Environment -------------------------------------------------------------

rm(list = ls())

# Load required packages
required_packages <- c('tidyverse', 'data.table', 'stringr', 'readxl', 'lubridate', 'arrow')
missing_packages <- setdiff(required_packages, rownames(installed.packages()))

if (length(missing_packages) > 0) {
  options(repos = c(CRAN = "https://cloud.r-project.org/"))
  install.packages(missing_packages)
}

library(tidyverse)
library(data.table)
library(stringr)
library(readxl)
library(lubridate)
library(arrow)

# Parse arguments
args = commandArgs(trailingOnly = TRUE)
if (length(args)) {
  project_root <- args[1]
} else {
  stop('Supply project root path as argument')
}

# Set download method based on system
dlmethod = ifelse(Sys.info()[1] == "Linux", 'wget', 'auto')


# Helper Functions --------------------------------------------------------

# Read and process IO matrix from Excel file
read_io_matrix <- function(file_path, sheet_name, is_pre1997 = FALSE) {
  if (is_pre1997) {
    # Pre-1997 format
    df <- read_excel(file_path, sheet_name, skip = 6) %>%
      rename(beaind = Code) %>%
      select(-2) %>%
      mutate_at(vars(-beaind), as.numeric)
  } else {
    # 1997-present format
    df <- read_excel(file_path, sheet_name, skip = 5) %>%
      rename(beaind = "...1") %>%
      filter(beaind != "IOCode") %>%
      select(-2) %>%
      mutate_at(vars(-beaind), as.numeric)
  }
  return(as.data.frame(df))
}

# Convert IO matrix to long format with weights
convert_to_long <- function(io_matrix, year_value) {
  io_matrix %>%
    pivot_longer(-beaind, names_to = "beaindmatch", values_to = "weight") %>%
    filter(!is.na(weight)) %>%
    mutate(year_avail = as.numeric(year_value) + 5)
}

# Process all IO tables from Excel files (reproducing original logic exactly)
process_io_tables <- function(file_pre1997, file_post1997, momentum_type) {
  indweight <- data.frame()

  # Process pre-1997 data
  sheets_pre1997 <- excel_sheets(file_pre1997)[-c(1,2)]  # Skip first two non-data sheets
  for (sheet in sheets_pre1997) {
    temp1 <- read_io_matrix(file_pre1997, sheet, is_pre1997 = TRUE)

    # Original transpose logic for supplier momentum
    if (momentum_type == 'supplier') {
      tempa <- temp1 %>% select(-beaind)
      rownames(tempa) <- temp1$beaind
      tempb <- as.data.frame(t(as.matrix(tempa)))
      tempc <- data.frame(beaind = rownames(tempb))
      temp1 <- cbind(tempc, tempb)
      rownames(temp1) <- NULL
    }

    temp2 <- convert_to_long(temp1, sheet)
    indweight <- rbind(indweight, temp2)
  }

  # Process 1997-present data (reproducing original bug)
  sheets_post1997 <- excel_sheets(file_post1997)
  for (sheet in sheets_post1997) {
    temp1 <- read_io_matrix(file_post1997, sheet, is_pre1997 = FALSE)

    # Original transpose logic with bug for supplier momentum
    if (momentum_type == 'supplier') {
      tempa <- temp1 %>% select(-beaind)
      rownames(tempa) <- temp1$beaind
      tempb <- as.data.frame(t(as.matrix(tempa)))
      tempc <- data.frame(beaind = rownames(tempb))
      temp <- cbind(tempc, tempb)  # BUG: using temp instead of temp1
      rownames(temp) <- NULL
      # Note: temp1 is still used below, so this creates inconsistency
    }

    temp2 <- convert_to_long(temp1, sheet)  # Still uses temp1
    indweight <- rbind(indweight, temp2)
  }

  return(indweight)
}

# Map Compustat firms to BEA industries
assign_firms_to_industries <- function(comp_data, indweight) {
  # Create industry list with NAICS prefixes
  indlist <- indweight %>%
    select(year_avail, beaind) %>%
    distinct() %>%
    mutate(naicspre = as.numeric(gsub("([0-9]+).*$", "\\1", beaind))) %>%
    filter(!is.na(naicspre))

  # Create multiple NAICS levels for matching
  comp_with_naics <- comp_data %>%
    mutate(
      naics2 = floor(naics6/1e4),
      naics3 = floor(naics6/1e3),
      naics4 = floor(naics6/1e2)
    )

  # Join with BEA industries at different NAICS levels
  result <- comp_with_naics %>%
    left_join(indlist %>% rename(beaind2 = beaind),
              by = c("year_avail", "naics2" = "naicspre")) %>%
    left_join(indlist %>% rename(beaind3 = beaind),
              by = c("year_avail", "naics3" = "naicspre")) %>%
    left_join(indlist %>% rename(beaind4 = beaind),
              by = c("year_avail", "naics4" = "naicspre")) %>%
    mutate(beaind = coalesce(beaind4, beaind3, beaind2)) %>%
    select(gvkey, year_avail, naics6, beaind) %>%
    filter(!is.na(beaind))

  return(result)
}

# Calculate value-weighted industry returns
calculate_industry_returns <- function(crsp_data, ccm_data, comp_mapped) {
  # Link CRSP with Compustat
  crsp_linked <- crsp_data %>%
    left_join(ccm_data, by = "permno") %>%
    filter(date >= linkdt, date <= linkenddt) %>%
    select(permno, date, ret, mve_c, gvkey) %>%
    mutate(year = year(date), month = month(date))

  # Add BEA industries
  crsp_with_ind <- crsp_linked %>%
    left_join(comp_mapped, by = c("gvkey", "year" = "year_avail")) %>%
    filter(!is.na(beaind))

  # Calculate industry returns
  ind_returns <- crsp_with_ind %>%
    group_by(year, month, beaind) %>%
    summarize(
      ret = weighted.mean(ret, mve_c),
      n = n(),
      .groups = 'drop'
    ) %>%
    filter(year >= 1986)  # NAICS available from 1986

  return(list(industry_returns = ind_returns, crsp_with_industries = crsp_with_ind))
}

# Calculate matched industry returns using IO weights
calculate_matched_returns <- function(ind_returns, indweight) {
  # Expand weights to monthly frequency, excluding own-industry
  monthly_weights <- ind_returns %>%
    select(year, month) %>%
    distinct() %>%
    left_join(indweight %>% filter(beaind != beaindmatch),
              by = c("year" = "year_avail"))

  # Add matched industry returns
  with_matched_ret <- monthly_weights %>%
    left_join(ind_returns %>%
                rename(retmatch = ret) %>%
                select(-n),
              by = c("beaindmatch" = "beaind", "year", "month")) %>%
    filter(!is.na(retmatch))

  # Calculate weighted average returns
  matched_returns <- with_matched_ret %>%
    group_by(year, month, beaind) %>%
    summarize(retmatch = weighted.mean(retmatch, weight), .groups = 'drop')

  return(matched_returns)
}

# Create momentum portfolios and assign firms
create_momentum_signal <- function(comp_mapped, matched_returns, crsp_with_ind) {
  # Assign industries to portfolios based on matched returns
  ind_portfolios <- matched_returns %>%
    filter(!is.na(retmatch)) %>%
    group_by(year, month) %>%
    mutate(portind = findInterval(retmatch,
                                  quantile(retmatch, 0:10/10),
                                  rightmost.closed = TRUE)) %>%
    ungroup()

  # Assign firms to portfolios
  firm_momentum <- crossing(comp_mapped,
                           data.frame(month_avail = 1:12)) %>%
    left_join(ind_portfolios %>%
                select(year, month, beaind, retmatch, portind),
              by = c("year_avail" = "year",
                    "month_avail" = "month",
                    "beaind"))

  # Validate portfolio performance (1986-2005 sample)
  print("checking stock assignments:")
  portfolio_returns <- crsp_with_ind %>%
    left_join(firm_momentum,
              by = c('gvkey', 'year' = 'year_avail', 'month' = 'month_avail')) %>%
    mutate(portfolio = lag(portind, n = 1)) %>%
    filter(year >= 1986, year <= 2005) %>%
    group_by(year, month, portfolio) %>%
    summarize(ret = mean(ret, na.rm = TRUE), .groups = 'drop') %>%
    pivot_wider(names_from = portfolio,
                values_from = ret,
                names_prefix = 'port') %>%
    mutate(portLS = port10 - port1)

  # Calculate portfolio statistics
  portfolio_stats <- portfolio_returns %>%
    pivot_longer(contains('port'), names_to = 'port', values_to = 'ret') %>%
    group_by(port) %>%
    summarize(
      mean = mean(ret, na.rm = TRUE),
      vol = sd(ret, na.rm = TRUE),
      nmonths = n(),
      tstat = mean/vol * sqrt(nmonths)
    )

  print(portfolio_stats)

  return(firm_momentum)
}


# Main Processing --------------------------------------------------------

# Load input data
print("Loading input data...")
comp_data <- fread(paste0(project_root, '/pyData/Intermediate/CompustatAnnual.csv')) %>%
  as.data.frame() %>%
  mutate(
    naicsstr = str_pad(as.character(naicsh), 6, side = "right", pad = "0"),
    naics6 = as.numeric(naicsstr),
    year_avail = year(dmy(datadate) %m+% months(6)) + 1
  ) %>%
  filter(!is.na(naics6)) %>%
  select(gvkey, year_avail, naics6, datadate)

crsp_data <- read_parquet(paste0(project_root, '/pyData/Intermediate/monthlyCRSP.parquet')) %>%
  transmute(
    permno,
    date = as.Date(time_avail_m),
    ret = 100 * ret,
    mve_c = abs(prc) * shrout
  ) %>%
  filter(!is.na(ret), !is.na(mve_c))

ccm_data <- read_parquet(paste0(project_root, '/pyData/Intermediate/CCMLinkingTable.parquet')) %>%
  mutate(linkenddt = ifelse(is.na(timeLinkEnd_d), as.Date("3000-12-31"), as.Date(timeLinkEnd_d))) %>%
  transmute(
    gvkey = as.numeric(gvkey),
    permno = permno,
    linkprim,
    linkdt = as.Date(timeLinkStart_d),
    linkenddt = linkenddt
  )

# Check for BEA Input-Output tables (downloaded separately by BEA_InputOutput.py)
print("Checking for BEA Input-Output tables...")
data_dir <- paste0(project_root, '/pyData/Intermediate/')

# Define expected file paths
make_pre1997 <- paste0(data_dir, 'IOMake_Before_Redefinitions_1963-1996_Summary.xlsx')
use_pre1997 <- paste0(data_dir, 'IOUse_Before_Redefinitions_PRO_1963-1996_Summary.xlsx')

# Find 1997-present tables
fls <- list.files(data_dir, full.names = TRUE)
pathSupply <- fls[grepl("Supply_Tables_1997-2[0-9]{3}_Summary.xlsx", basename(fls), ignore.case = TRUE)]
pathUse <- fls[grepl("Supply-Use_Framework_1997-2[0-9]{3}_Summary.xlsx", basename(fls), ignore.case = TRUE)]

# Validate all required files exist
required_files <- c(make_pre1997, use_pre1997, pathSupply, pathUse)
missing_files <- required_files[!file.exists(required_files)]

if (length(missing_files) > 0) {
  cat("Missing BEA Input-Output files:\n")
  cat(paste(" -", missing_files, collapse = "\n"), "\n")
  stop("Please run BEA_InputOutput.py first to download required files")
}

if (length(pathSupply) != 1 || length(pathUse) != 1) {
  stop(paste("Expected exactly 1 Supply and 1 Use file, found", length(pathSupply), "and", length(pathUse)))
}

print("✓ All BEA Input-Output tables found")

# Process Customer Momentum
print("Calculating customer momentum...")
make_post1997 <- pathSupply

indweight_customer <- process_io_tables(make_pre1997, make_post1997, 'customer')
comp_mapped_customer <- assign_firms_to_industries(comp_data, indweight_customer)
returns_data_customer <- calculate_industry_returns(crsp_data, ccm_data, comp_mapped_customer)
matched_returns_customer <- calculate_matched_returns(returns_data_customer$industry_returns, indweight_customer)
customer_momentum <- create_momentum_signal(comp_mapped_customer, matched_returns_customer,
                                           returns_data_customer$crsp_with_industries)

# Process Supplier Momentum
print("Calculating supplier momentum...")
use_post1997 <- pathUse

indweight_supplier <- process_io_tables(use_pre1997, use_post1997, 'supplier')
comp_mapped_supplier <- assign_firms_to_industries(comp_data, indweight_supplier)
returns_data_supplier <- calculate_industry_returns(crsp_data, ccm_data, comp_mapped_supplier)
matched_returns_supplier <- calculate_matched_returns(returns_data_supplier$industry_returns, indweight_supplier)
supplier_momentum <- create_momentum_signal(comp_mapped_supplier, matched_returns_supplier,
                                           returns_data_supplier$crsp_with_industries)

# Combine and save results
print("Combining and saving results...")
final_output <- rbind(
  customer_momentum %>% mutate(type = 'customer'),
  supplier_momentum %>% mutate(type = 'supplier')
) %>%
  filter(!is.na(retmatch))

output_path <- paste0(project_root, '/pyData/Intermediate/InputOutputMomentum_R.csv')
fwrite(final_output, file = output_path)

print(paste0("Successfully saved output to: ", output_path))
print(paste0("Total rows: ", nrow(final_output)))

