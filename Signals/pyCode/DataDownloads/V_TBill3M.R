# ABOUTME: R script to replicate Stata V_TBill3M.do exactly
# ABOUTME: Downloads TB3MS from FRED and processes to match Stata output precisely

# Load required libraries
library(fredr)
library(dplyr)
library(lubridate)

# Set FRED API key (assumes FRED_API_KEY environment variable)
fred_api_key <- Sys.getenv("FRED_API_KEY")
if (fred_api_key == "") {
  stop("ERROR: FRED_API_KEY not found in environment variables")
}
fredr_set_key(fred_api_key)

cat("Processing 3-month T-bill rate in R...\n")

# Stata: import fred TB3MS, clear aggregate(q, avg)
cat("Downloading TB3MS from FRED...\n")
monthly_data <- fredr(
  series_id = "TB3MS",
  observation_start = as.Date("1900-01-01")
)

cat(sprintf("Downloaded %d monthly observations\n", nrow(monthly_data)))

# Convert to quarterly data using R's aggregate function to match Stata exactly
# Stata's aggregate(q, avg) behavior
monthly_data$quarter_year <- paste0(year(monthly_data$date), "Q", quarter(monthly_data$date))
quarterly_data <- monthly_data %>%
  mutate(
    year = year(date),
    qtr = quarter(date)
  ) %>%
  group_by(year, qtr) %>%
  summarise(
    TB3MS = mean(value, na.rm = TRUE),
    date = max(date),  # Use last date of quarter
    .groups = 'drop'
  )

cat(sprintf("Aggregated to %d quarterly observations\n", nrow(quarterly_data)))

# Stata: gen TbillRate3M = TB3MS/100
quarterly_data$TbillRate3M <- quarterly_data$TB3MS / 100

# Stata: keep year qtr TbillRate3M
final_data <- quarterly_data %>%
  select(year, qtr, TbillRate3M) %>%
  arrange(year, qtr)

cat(sprintf("Final dataset: %d quarterly records\n", nrow(final_data)))
cat(sprintf("Date range: %dQ%d to %dQ%d\n", 
           min(final_data$year), min(final_data$qtr[final_data$year == min(final_data$year)]),
           max(final_data$year), max(final_data$qtr[final_data$year == max(final_data$year)])))

# Save results for comparison
write.csv(final_data, "../pyData/Intermediate/TBill3M_R.csv", row.names = FALSE)

cat("3-month T-bill rate data saved to TBill3M_R.csv\n")

# Show sample data
cat("\nSample data:\n")
print(head(final_data))

# Show summary statistics
cat("\nT-bill rate summary:\n")
cat(sprintf("Mean: %.6f\n", mean(final_data$TbillRate3M)))
cat(sprintf("Std: %.6f\n", sd(final_data$TbillRate3M)))
cat(sprintf("Min: %.6f\n", min(final_data$TbillRate3M)))
cat(sprintf("Max: %.6f\n", max(final_data$TbillRate3M)))

# Show first few values with high precision for comparison
cat("\nFirst 5 values with high precision:\n")
for (i in 1:min(5, nrow(final_data))) {
  cat(sprintf("Row %d: %dQ%d = %.15f\n", 
             i, final_data$year[i], final_data$qtr[i], final_data$TbillRate3M[i]))
}