# ABOUTME: Creates Industry Return Big Companies (IndRetBig) predictor by calculating industry returns for large companies
# ABOUTME: Run from pyCode/ directory: python3 Predictors/IndRetBig.py

# IndRetBig predictor translation from Code/Predictors/IndRetBig.do
# Line-by-line translation preserving exact order and logic

import pandas as pd
import numpy as np
import sys
sys.path.append('.')
from utils.savepredictor import save_predictor
from utils.relrank import relrank

# DATA LOAD
# Stata: use permno time_avail_m ret mve_c sicCRSP using "$pathDataIntermediate/SignalMasterTable", clear
df = pd.read_parquet('../pyData/Intermediate/SignalMasterTable.parquet')
df = df[['permno', 'time_avail_m', 'ret', 'mve_c', 'sicCRSP']].copy()

# Convert datetime time_avail_m to integer yyyymm to match Stata format
df['yyyymm'] = df['time_avail_m'].dt.year * 100 + df['time_avail_m'].dt.month

print(f"Loaded {len(df)} observations from SignalMasterTable")

# SIGNAL CONSTRUCTION

# Stata: sicff sicCRSP, generate(tempFF48) industry(48)
# Implement Fama-French 48 industry classification
def get_ff48(sic):
    """
    Accurate Fama-French 48 industry classification based on SIC code
    Extracted directly from sicff.ado lines 521-615 for exact replication
    """
    if pd.isna(sic):
        return np.nan
    try:
        sic = int(sic)
    except:
        return np.nan
    
    # Industry 1: Agriculture
    if ((100 <= sic <= 199) or (200 <= sic <= 299) or (700 <= sic <= 799) or 
        (910 <= sic <= 919) or (sic == 2048)):
        return 1
    
    # Industry 2: Food Products
    elif ((2000 <= sic <= 2009) or (2010 <= sic <= 2019) or (2020 <= sic <= 2029) or 
          (2030 <= sic <= 2039) or (2040 <= sic <= 2046) or (2050 <= sic <= 2059) or 
          (2060 <= sic <= 2063) or (2070 <= sic <= 2079) or (2090 <= sic <= 2092) or 
          (sic == 2095) or (2098 <= sic <= 2099)):
        return 2
    
    # Industry 3: Candy & Soda
    elif ((2064 <= sic <= 2068) or (sic == 2086) or (sic == 2087) or 
          (sic == 2096) or (sic == 2097)):
        return 3
    
    # Industry 4: Beer & Liquor
    elif ((sic == 2080) or (sic == 2082) or (sic == 2083) or 
          (sic == 2084) or (sic == 2085)):
        return 4
    
    # Industry 5: Tobacco Products
    elif (2100 <= sic <= 2199):
        return 5
    
    # Industry 6: Recreation
    elif ((920 <= sic <= 999) or (3650 <= sic <= 3652) or (sic == 3732) or 
          (3930 <= sic <= 3931) or (3940 <= sic <= 3949)):
        return 6
    
    # Industry 7: Entertainment
    elif ((7800 <= sic <= 7829) or (7830 <= sic <= 7833) or (7840 <= sic <= 7841) or 
          (sic == 7900) or (7910 <= sic <= 7911) or (7920 <= sic <= 7929) or 
          (7930 <= sic <= 7933) or (7940 <= sic <= 7949) or (sic == 7980) or 
          (7990 <= sic <= 7999)):
        return 7
    
    # Industry 8: Printing and Publishing
    elif ((2700 <= sic <= 2709) or (2710 <= sic <= 2719) or (2720 <= sic <= 2729) or 
          (2730 <= sic <= 2739) or (2740 <= sic <= 2749) or (2770 <= sic <= 2771) or 
          (2780 <= sic <= 2789) or (2790 <= sic <= 2799)):
        return 8
    
    # Industry 9: Consumer Goods
    elif ((sic == 2047) or (2391 <= sic <= 2392) or (2510 <= sic <= 2519) or 
          (2590 <= sic <= 2599) or (2840 <= sic <= 2844) or (3160 <= sic <= 3161) or 
          (3170 <= sic <= 3172) or (3190 <= sic <= 3199) or (sic == 3229) or 
          (sic == 3260) or (3262 <= sic <= 3263) or (sic == 3269) or 
          (3230 <= sic <= 3231) or (3630 <= sic <= 3639) or (3750 <= sic <= 3751) or 
          (sic == 3800) or (3860 <= sic <= 3861) or (3870 <= sic <= 3873) or 
          (3910 <= sic <= 3911) or (sic == 3914) or (sic == 3915) or 
          (3960 <= sic <= 3962) or (sic == 3991) or (sic == 3995)):
        return 9
    
    # Industry 10: Apparel
    elif ((2300 <= sic <= 2390) or (3020 <= sic <= 3021) or (3100 <= sic <= 3111) or 
          (3130 <= sic <= 3131) or (3140 <= sic <= 3151) or (3963 <= sic <= 3965)):
        return 10
    
    # Industry 11: Healthcare
    elif (8000 <= sic <= 8099):
        return 11
    
    # Industry 12: Medical Equipment
    elif ((sic == 3693) or (3840 <= sic <= 3851)):
        return 12
    
    # Industry 13: Pharmaceutical Products
    elif ((sic == 2830) or (sic == 2831) or (sic == 2833) or 
          (sic == 2834) or (sic == 2835) or (sic == 2836)):
        return 13
    
    # Industry 14: Chemicals
    elif ((2800 <= sic <= 2809) or (2810 <= sic <= 2819) or (2820 <= sic <= 2829) or 
          (2850 <= sic <= 2859) or (2860 <= sic <= 2869) or (2870 <= sic <= 2879) or 
          (2890 <= sic <= 2899)):
        return 14
    
    # Industry 15: Rubber and Plastic Products
    elif ((sic == 3031) or (sic == 3041) or (3050 <= sic <= 3053) or 
          (3060 <= sic <= 3069) or (3070 <= sic <= 3079) or (3080 <= sic <= 3089) or 
          (3090 <= sic <= 3099)):
        return 15
    
    # Industry 16: Textiles
    elif ((2200 <= sic <= 2269) or (2270 <= sic <= 2279) or (2280 <= sic <= 2284) or 
          (2290 <= sic <= 2295) or (sic == 2297) or (sic == 2298) or (sic == 2299) or 
          (2393 <= sic <= 2395) or (2397 <= sic <= 2399)):
        return 16
    
    # Industry 17: Construction Materials
    elif ((800 <= sic <= 899) or (2400 <= sic <= 2439) or (2450 <= sic <= 2459) or 
          (2490 <= sic <= 2499) or (2660 <= sic <= 2661) or (2950 <= sic <= 2952) or 
          (sic == 3200) or (3210 <= sic <= 3211) or (3240 <= sic <= 3241) or 
          (3250 <= sic <= 3259) or (sic == 3261) or (sic == 3264) or 
          (3270 <= sic <= 3275) or (3280 <= sic <= 3281) or (3290 <= sic <= 3293) or 
          (3295 <= sic <= 3299) or (3420 <= sic <= 3429) or (3430 <= sic <= 3433) or 
          (3440 <= sic <= 3441) or (sic == 3442) or (sic == 3446) or (sic == 3448) or 
          (sic == 3449) or (3450 <= sic <= 3452) or (3490 <= sic <= 3499) or 
          (sic == 3996)):
        return 17
    
    # Industry 18: Construction
    elif ((1500 <= sic <= 1511) or (1520 <= sic <= 1529) or (1530 <= sic <= 1539) or 
          (1540 <= sic <= 1549) or (1600 <= sic <= 1699) or (1700 <= sic <= 1799)):
        return 18
    
    # Industry 19: Steel Works Etc
    elif ((sic == 3300) or (3310 <= sic <= 3317) or (3320 <= sic <= 3325) or 
          (3330 <= sic <= 3339) or (3340 <= sic <= 3341) or (3350 <= sic <= 3357) or 
          (3360 <= sic <= 3369) or (3370 <= sic <= 3379) or (3390 <= sic <= 3399)):
        return 19
    
    # Industry 20: Fabricated Products
    elif ((sic == 3400) or (sic == 3443) or (sic == 3444) or 
          (3460 <= sic <= 3469) or (3470 <= sic <= 3479)):
        return 20
    
    # Industry 21: Machinery
    elif ((3510 <= sic <= 3519) or (3520 <= sic <= 3536) or (sic == 3538) or 
          (3540 <= sic <= 3569) or (3580 <= sic <= 3582) or (3585 <= sic <= 3586) or 
          (sic == 3589) or (3590 <= sic <= 3599)):
        return 21
    
    # Industry 22: Electrical Equipment
    elif ((sic == 3600) or (3610 <= sic <= 3613) or (3620 <= sic <= 3621) or 
          (3623 <= sic <= 3629) or (3640 <= sic <= 3646) or (3648 <= sic <= 3649) or 
          (sic == 3660) or (3690 <= sic <= 3692) or (sic == 3699)):
        return 22
    
    # Industry 23: Automobiles and Trucks
    elif ((sic == 2296) or (sic == 2396) or (3010 <= sic <= 3011) or (sic == 3537) or 
          (sic == 3647) or (sic == 3694) or (sic == 3700) or (3710 <= sic <= 3711) or 
          (sic == 3713) or (3714 <= sic <= 3716) or (sic == 3792) or 
          (3790 <= sic <= 3791) or (sic == 3799)):
        return 23
    
    # Industry 24: Aircraft
    elif ((sic == 3720) or (sic == 3721) or (3723 <= sic <= 3725) or 
          (3728 <= sic <= 3729)):
        return 24
    
    # Industry 25: Shipbuilding, Railroad Equipment
    elif ((3730 <= sic <= 3731) or (3740 <= sic <= 3743)):
        return 25
    
    # Industry 26: Defense
    elif ((3760 <= sic <= 3769) or (sic == 3795) or (3480 <= sic <= 3489)):
        return 26
    
    # Industry 27: Precious Metals
    elif (1040 <= sic <= 1049):
        return 27
    
    # Industry 28: Non-Metallic and Industrial Metal Mining
    elif ((1000 <= sic <= 1039) or (1050 <= sic <= 1119) or (1400 <= sic <= 1499)):
        return 28
    
    # Industry 29: Coal
    elif (1200 <= sic <= 1299):
        return 29
    
    # Industry 30: Petroleum and Natural Gas
    elif ((sic == 1300) or (1310 <= sic <= 1319) or (1320 <= sic <= 1329) or 
          (1330 <= sic <= 1339) or (1370 <= sic <= 1382) or (sic == 1389) or 
          (2900 <= sic <= 2912) or (2990 <= sic <= 2999)):
        return 30
    
    # Industry 31: Utilities
    elif ((sic == 4900) or (4910 <= sic <= 4911) or (4920 <= sic <= 4925) or 
          (4930 <= sic <= 4932) or (sic == 4939) or (4940 <= sic <= 4942)):
        return 31
    
    # Industry 32: Communication
    elif ((sic == 4800) or (4810 <= sic <= 4813) or (4820 <= sic <= 4822) or 
          (4830 <= sic <= 4841) or (4880 <= sic <= 4892) or (sic == 4899)):
        return 32
    
    # Industry 33: Personal Services
    elif ((7020 <= sic <= 7021) or (7030 <= sic <= 7033) or (sic == 7200) or 
          (7210 <= sic <= 7212) or (sic == 7214) or (7215 <= sic <= 7217) or 
          (sic == 7219) or (7220 <= sic <= 7221) or (7230 <= sic <= 7231) or 
          (7240 <= sic <= 7241) or (7250 <= sic <= 7251) or (7260 <= sic <= 7269) or 
          (7270 <= sic <= 7299) or (sic == 7395) or (sic == 7500) or 
          (7510 <= sic <= 7515) or (7520 <= sic <= 7549) or (sic == 7600) or 
          (sic == 7620) or (sic == 7622) or (sic == 7623) or (sic == 7629) or 
          (7630 <= sic <= 7631) or (7640 <= sic <= 7641) or (7690 <= sic <= 7699) or 
          (8100 <= sic <= 8199) or (8200 <= sic <= 8299) or (8300 <= sic <= 8399) or 
          (8400 <= sic <= 8499) or (8600 <= sic <= 8699) or (8800 <= sic <= 8899)):
        return 33
    
    # Industry 34: Business Services
    elif ((2750 <= sic <= 2759) or (sic == 3993) or (sic == 7218) or 
          (sic == 7300) or (7310 <= sic <= 7319) or (7320 <= sic <= 7329) or 
          (7330 <= sic <= 7342) or (sic == 7349) or (7350 <= sic <= 7353) or 
          (sic == 7359) or (7360 <= sic <= 7372) or (7374 <= sic <= 7385) or 
          (7389 <= sic <= 7397) or (sic == 7399) or (sic == 7519) or 
          (sic == 8700) or (8710 <= sic <= 8713) or (8720 <= sic <= 8721) or 
          (8730 <= sic <= 8734) or (8740 <= sic <= 8748) or (8900 <= sic <= 8911) or 
          (8920 <= sic <= 8999) or (4220 <= sic <= 4229)):
        return 34
    
    # Industry 35: Computers
    elif ((3570 <= sic <= 3579) or (3680 <= sic <= 3689) or (sic == 3695) or 
          (sic == 7373)):
        return 35
    
    # Industry 36: Electronic Equipment
    elif ((sic == 3622) or (3661 <= sic <= 3666) or (sic == 3669) or 
          (3670 <= sic <= 3679) or (sic == 3810) or (sic == 3812)):
        return 36
    
    # Industry 37: Measuring and Control Equipment
    elif ((sic == 3811) or (3820 <= sic <= 3827) or (sic == 3829) or 
          (3830 <= sic <= 3839)):
        return 37
    
    # Industry 38: Business Supplies
    elif ((2520 <= sic <= 2549) or (2600 <= sic <= 2639) or (2670 <= sic <= 2699) or 
          (2760 <= sic <= 2761) or (3950 <= sic <= 3955)):
        return 38
    
    # Industry 39: Shipping Containers
    elif ((2440 <= sic <= 2449) or (2640 <= sic <= 2659) or (3220 <= sic <= 3221) or 
          (3410 <= sic <= 3412)):
        return 39
    
    # Industry 40: Transportation
    elif ((4000 <= sic <= 4013) or (4040 <= sic <= 4049) or (sic == 4100) or 
          (4110 <= sic <= 4119) or (4120 <= sic <= 4121) or (4130 <= sic <= 4131) or 
          (4140 <= sic <= 4142) or (4150 <= sic <= 4151) or (4170 <= sic <= 4173) or 
          (4190 <= sic <= 4219) or (4230 <= sic <= 4231) or (4240 <= sic <= 4249) or 
          (4400 <= sic <= 4499) or (4500 <= sic <= 4699) or (sic == 4700) or 
          (4710 <= sic <= 4712) or (4720 <= sic <= 4749) or (sic == 4780) or 
          (4782 <= sic <= 4785) or (sic == 4789)):
        return 40
    
    # Industry 41: Wholesale
    elif ((sic == 5000) or (5010 <= sic <= 5015) or (5020 <= sic <= 5023) or 
          (5030 <= sic <= 5060) or (5063 <= sic <= 5065) or (5070 <= sic <= 5078) or 
          (5080 <= sic <= 5088) or (5090 <= sic <= 5094) or (sic == 5099) or 
          (sic == 5100) or (5110 <= sic <= 5113) or (5120 <= sic <= 5122) or 
          (5130 <= sic <= 5172) or (5180 <= sic <= 5182) or (5190 <= sic <= 5199)):
        return 41
    
    # Industry 42: Retail
    elif ((sic == 5200) or (5210 <= sic <= 5231) or (5250 <= sic <= 5251) or 
          (5260 <= sic <= 5261) or (5270 <= sic <= 5271) or (sic == 5300) or 
          (5310 <= sic <= 5311) or (sic == 5320) or (5330 <= sic <= 5331) or 
          (sic == 5334) or (5340 <= sic <= 5349) or (5390 <= sic <= 5400) or 
          (5410 <= sic <= 5412) or (5420 <= sic <= 5469) or (5490 <= sic <= 5579) or 
          (5590 <= sic <= 5799) or (sic == 5900) or (5910 <= sic <= 5912) or 
          (5920 <= sic <= 5932) or (5940 <= sic <= 5949) or (5950 <= sic <= 5989) or 
          (sic == 5990) or (5992 <= sic <= 5995) or (sic == 5999)):
        return 42
    
    # Industry 43: Restaurants, Hotels, Motels
    elif ((5800 <= sic <= 5829) or (5890 <= sic <= 5899) or (sic == 7000) or 
          (7010 <= sic <= 7019) or (7040 <= sic <= 7049) or (sic == 7213)):
        return 43
    
    # Industry 44: Banking
    elif ((sic == 6000) or (6010 <= sic <= 6036) or (6040 <= sic <= 6062) or 
          (6080 <= sic <= 6082) or (6090 <= sic <= 6100) or (6110 <= sic <= 6113) or 
          (6120 <= sic <= 6179) or (6190 <= sic <= 6199)):
        return 44
    
    # Industry 45: Insurance
    elif ((6300 <= sic <= 6331) or (6350 <= sic <= 6351) or (6360 <= sic <= 6361) or 
          (6370 <= sic <= 6379) or (6390 <= sic <= 6411)):
        return 45
    
    # Industry 46: Real Estate
    elif ((sic == 6500) or (sic == 6510) or (6512 <= sic <= 6515) or 
          (6517 <= sic <= 6532) or (6540 <= sic <= 6541) or (6550 <= sic <= 6553) or 
          (6590 <= sic <= 6599) or (6610 <= sic <= 6611)):
        return 46
    
    # Industry 47: Trading
    elif ((6200 <= sic <= 6299) or (sic == 6700) or (6710 <= sic <= 6726) or 
          (6730 <= sic <= 6733) or (6740 <= sic <= 6779) or (6790 <= sic <= 6795) or 
          (sic == 6798) or (sic == 6799)):
        return 47
    
    # Industry 48: Almost Nothing
    elif ((4950 <= sic <= 4959) or (4960 <= sic <= 4961) or (4970 <= sic <= 4971) or 
          (4990 <= sic <= 4991)):
        return 48
    
    else:
        # Default for any unmatched SIC codes
        return 48

df['tempFF48'] = df['sicCRSP'].apply(get_ff48)

# Stata: drop if mi(tempFF48)
df = df.dropna(subset=['tempFF48'])

print(f"After dropping missing FF48 industries: {len(df)} observations")

# Stata: bys tempFF48 time_avail_m: relrank mve_c, gen(tempRK) ref(mve_c)
# Use utils/relrank to match Stata's exact behavior
df = relrank(df, 'mve_c', by=['tempFF48', 'yyyymm'], out='tempRK')

print(f"Calculated tempRK ranks for {df['tempRK'].notna().sum()} observations")

# Stata: preserve
df_original = df.copy()

# Stata: keep if tempRK >=.7 & !mi(tempRK)
df_big = df[(df['tempRK'] >= 0.7) & df['tempRK'].notna()].copy()

print(f"Large companies (tempRK >= 0.7): {len(df_big)} observations")

# Stata: gcollapse (mean) ret, by(tempFF48 time_avail_m)
# Calculate mean returns by industry-month for large companies only
industry_returns = df_big.groupby(['tempFF48', 'yyyymm'])['ret'].mean().reset_index()
industry_returns = industry_returns.rename(columns={'ret': 'IndRetBig'})

print(f"Calculated industry returns for {len(industry_returns)} industry-month groups")

# Stata: save "$pathtemp/temp",replace
# Stata: restore
df = df_original.copy()
# Ensure yyyymm column exists for merge (df_original was created after yyyymm conversion)
# No need to recreate yyyymm since df_original already contains it

# Stata: merge m:1 tempFF48 time_avail_m using "$pathtemp/temp", nogenerate
df = df.merge(industry_returns, on=['tempFF48', 'yyyymm'], how='left')

# Stata: replace IndRetBig = . if tempRK >= .7
# Set IndRetBig to missing for companies that are themselves large (>= 70th percentile)
df.loc[df['tempRK'] >= 0.7, 'IndRetBig'] = np.nan

print(f"Set IndRetBig to missing for {(df['tempRK'] >= 0.7).sum()} large companies")

# Stata: label var IndRetBig "Industry return big companies"
# (No need to implement label in Python)

print(f"Final dataset has {len(df)} observations with {df['IndRetBig'].notna().sum()} non-missing IndRetBig values")

# SAVE
# Stata: do "$pathCode/savepredictor" IndRetBig
save_predictor(df, 'IndRetBig')

print("IndRetBig predictor saved successfully")