# Summary Statistics: ZH_OptionMetricsCleaning
Generated on: 2025-09-09 06:22:17

**Total datasets**: 4

## OptionMetricsVolume

**File**: `../pyData/Intermediate/OptionMetricsVolume.parquet`
**Dimensions**: 64,867,671 rows × 5 columns

|       Variable       |   Count    |    Mean    |  Std Dev   |   25th %   |   75th %   |
|----------------------|------------|------------|------------|------------|------------|
| secid                | 64,867,671 | 145182.549 | 44576.1762 | 107899.000 | 205208.000 |
| date                 | 64,867,671 |    N/A     |    N/A     |    N/A     |    N/A     |
| cp_flag              | 64,867,671 |    N/A     |    N/A     |    N/A     |    N/A     |
| volume               | 64,867,671 |    34.2470 |   585.7393 |     0.0000 |     0.0000 |
| open_interest        |          0 |    N/A     |    N/A     |    N/A     |    N/A     |

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
