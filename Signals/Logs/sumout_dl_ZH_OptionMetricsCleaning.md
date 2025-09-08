# Summary Statistics: ZH_OptionMetricsCleaning
Generated on: 2025-09-08 13:14:30

**Total datasets**: 3

## OptionMetricsVolSurf

**File**: `../pyData/Intermediate/OptionMetricsVolSurf.parquet`
**Dimensions**: 4,617,772 rows × 7 columns

|       Variable       |   Count    |    Mean    |  Std Dev   |   25th %   |   75th %   |
|----------------------|------------|------------|------------|------------|------------|
| secid                |  4,617,772 | 123278.816 | 37038.0100 | 105438.000 | 128882.000 |
| days                 |  4,617,772 |    60.5000 |    30.5000 |    30.0000 |    91.0000 |
| delta                |  4,617,772 |     0.0000 |    50.0000 |   -50.0000 |    50.0000 |
| cp_flag              |  4,617,772 |    N/A     |    N/A     |    N/A     |    N/A     |
| time_avail_m         |  4,617,772 |    N/A     |    N/A     |    N/A     |    N/A     |
| date                 |  4,617,772 |    N/A     |    N/A     |    N/A     |    N/A     |
| impl_vol             |  4,617,772 |     0.5685 |     0.6915 |     0.2720 |     0.6136 |

## OptionMetricsXZZ

**File**: `../pyData/Intermediate/OptionMetricsXZZ.parquet`
**Dimensions**: 611,701 rows × 3 columns

|       Variable       |   Count    |    Mean    |  Std Dev   |   25th %   |   75th %   |
|----------------------|------------|------------|------------|------------|------------|
| secid                |    611,701 | 121573.255 | 34479.4743 | 105243.000 | 126953.000 |
| time_avail_m         |    611,701 |    N/A     |    N/A     |    N/A     |    N/A     |
| skew1                |    611,701 |     0.0548 |     0.0888 |     0.0178 |     0.0707 |

## OptionMetricsBH

**File**: `../pyData/Intermediate/OptionMetricsBH.parquet`
**Dimensions**: 2,852,712 rows × 7 columns

|       Variable       |   Count    |    Mean    |  Std Dev   |   25th %   |   75th %   |
|----------------------|------------|------------|------------|------------|------------|
| secid                |  2,852,712 | 120685.305 | 35276.9464 | 105169.000 | 125971.000 |
| time_avail_m         |  2,852,712 |    N/A     |    N/A     |    N/A     |    N/A     |
| cp_flag              |  2,852,712 |    N/A     |    N/A     |    N/A     |    N/A     |
| mean_imp_vol         |  2,852,712 |     0.4483 |     0.2597 |     0.2711 |     0.5555 |
| mean_day             |  2,852,712 |    21.4536 |     4.9225 |    19.0000 |    24.6667 |
| nobs                 |  2,852,712 |    13.1269 |    41.6293 |     3.0000 |    11.0000 |
| ticker               |  2,852,712 |    N/A     |    N/A     |    N/A     |    N/A     |
