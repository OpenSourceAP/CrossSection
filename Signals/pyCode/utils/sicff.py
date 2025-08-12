# ABOUTME: Fama-French industry classification functions translated from sicff.ado
# ABOUTME: Provides FF17 and FF48 industry classifications based on SIC codes

"""
sicff.py - Fama-French Industry Classification

Usage:
    from utils.sicff import sicff, get_ff17, get_ff48
    
    # Main function (mimics Stata sicff command)
    df['ff48'] = sicff(df['sicCRSP'], industry=48)
    df['ff17'] = sicff(df['sicCRSP'], industry=17)
    
    # Individual functions
    df['ff48'] = df['sicCRSP'].apply(get_ff48) 
    df['ff17'] = df['sicCRSP'].apply(get_ff17)

Inputs:
    - SIC codes (numeric or pandas Series)
    - industry: 17 or 48 (classification scheme)

Outputs:
    - FF industry classification codes (integer or pandas Series)

Features:
    - Exact translation of sicff.ado for FF17 and FF48 classifications
    - Handles missing/invalid SIC codes (returns NaN)
    - Supports both scalar and Series inputs
"""

import pandas as pd
import numpy as np


def sicff(sic_input, industry=48):
    """
    Main sicff function that mimics Stata's sicff command
    
    Parameters:
    -----------
    sic_input : scalar, list, or pandas Series
        SIC codes to classify
    industry : int
        Classification scheme (17 or 48)
        
    Returns:
    --------
    scalar, list, or pandas Series
        FF industry classifications
    """
    if industry == 17:
        if isinstance(sic_input, (pd.Series, list, np.ndarray)):
            return pd.Series(sic_input).apply(get_ff17)
        else:
            return get_ff17(sic_input)
    elif industry == 48:
        if isinstance(sic_input, (pd.Series, list, np.ndarray)):
            return pd.Series(sic_input).apply(get_ff48)
        else:
            return get_ff48(sic_input)
    else:
        raise ValueError(f"Industry classification {industry} not supported. Use 17 or 48.")


def get_ff17(sic):
    """
    Fama-French 17 industry classification based on SIC code
    Translated directly from sicff.ado lines 184-216
    """
    if pd.isna(sic):
        return np.nan
    
    try:
        sic = int(sic)
    except (ValueError, TypeError):
        return np.nan
    
    # FF17 Industry 1: Food
    if ((100 <= sic <= 199) or (200 <= sic <= 299) or (700 <= sic <= 799) or 
        (900 <= sic <= 999) or (2000 <= sic <= 2009) or (2010 <= sic <= 2019) or
        (2020 <= sic <= 2029) or (2030 <= sic <= 2039) or (2040 <= sic <= 2046) or
        (sic == 2047) or (sic == 2048) or (2050 <= sic <= 2059) or 
        (2060 <= sic <= 2063) or (2064 <= sic <= 2068) or (2070 <= sic <= 2079) or
        (sic == 2080) or (sic == 2082) or (sic == 2083) or (sic == 2084) or
        (sic == 2085) or (sic == 2086) or (sic == 2087) or (2090 <= sic <= 2092) or
        (sic == 2095) or (sic == 2096) or (sic == 2097) or (2098 <= sic <= 2099) or
        (5140 <= sic <= 5149) or (5150 <= sic <= 5159) or (5180 <= sic <= 5182) or
        (sic == 5191)):
        return 1
        
    # FF17 Industry 2: Mining and Minerals  
    elif ((1000 <= sic <= 1009) or (1010 <= sic <= 1019) or (1020 <= sic <= 1029) or
          (1030 <= sic <= 1039) or (1040 <= sic <= 1049) or (1060 <= sic <= 1069) or
          (1080 <= sic <= 1089) or (1090 <= sic <= 1099) or (1200 <= sic <= 1299) or
          (1400 <= sic <= 1499) or (5050 <= sic <= 5052)):
        return 2
        
    # FF17 Industry 3: Oil and Petroleum Products
    elif ((sic == 1300) or (1310 <= sic <= 1319) or (1320 <= sic <= 1329) or
          (sic == 1380) or (sic == 1381) or (sic == 1382) or (sic == 1389) or
          (2900 <= sic <= 2912) or (5170 <= sic <= 5172)):
        return 3
        
    # FF17 Industry 4: Textiles, Apparel & Footwear
    elif ((2200 <= sic <= 2269) or (2270 <= sic <= 2279) or (2280 <= sic <= 2284) or
          (2290 <= sic <= 2295) or (sic == 2296) or (sic == 2297) or (sic == 2298) or
          (sic == 2299) or (2300 <= sic <= 2390) or (2391 <= sic <= 2392) or
          (2393 <= sic <= 2395) or (sic == 2396) or (2397 <= sic <= 2399) or
          (3020 <= sic <= 3021) or (3100 <= sic <= 3111) or (3130 <= sic <= 3131) or
          (3140 <= sic <= 3149) or (3150 <= sic <= 3151) or (3963 <= sic <= 3965) or
          (5130 <= sic <= 5139)):
        return 4
        
    # FF17 Industry 5: Consumer Durables
    elif ((2510 <= sic <= 2519) or (2590 <= sic <= 2599) or (3060 <= sic <= 3069) or
          (3070 <= sic <= 3079) or (3080 <= sic <= 3089) or (3090 <= sic <= 3099) or
          (3630 <= sic <= 3639) or (3650 <= sic <= 3651) or (sic == 3652) or
          (3860 <= sic <= 3861) or (3870 <= sic <= 3873) or (3910 <= sic <= 3911) or
          (sic == 3914) or (sic == 3915) or (3930 <= sic <= 3931) or
          (3940 <= sic <= 3949) or (3960 <= sic <= 3962) or (5020 <= sic <= 5023) or
          (sic == 5064) or (sic == 5094) or (sic == 5099)):
        return 5
        
    # FF17 Industry 6: Chemicals
    elif ((2800 <= sic <= 2809) or (2810 <= sic <= 2819) or (2820 <= sic <= 2829) or
          (2860 <= sic <= 2869) or (2870 <= sic <= 2879) or (2890 <= sic <= 2899) or
          (5160 <= sic <= 5169)):
        return 6
        
    # FF17 Industry 7: Drugs, Soap, Perfumes, Tobacco
    elif ((2100 <= sic <= 2199) or (sic == 2830) or (sic == 2831) or (sic == 2833) or
          (sic == 2834) or (2840 <= sic <= 2843) or (sic == 2844) or
          (5120 <= sic <= 5122) or (sic == 5194)):
        return 7
        
    # FF17 Industry 8: Construction and Construction Materials
    elif ((800 <= sic <= 899) or (1500 <= sic <= 1511) or (1520 <= sic <= 1529) or
          (1530 <= sic <= 1539) or (1540 <= sic <= 1549) or (1600 <= sic <= 1699) or
          (1700 <= sic <= 1799) or (2400 <= sic <= 2439) or (2440 <= sic <= 2449) or
          (2450 <= sic <= 2459) or (2490 <= sic <= 2499) or (2850 <= sic <= 2859) or
          (2950 <= sic <= 2952) or (sic == 3200) or (3210 <= sic <= 3211) or
          (3240 <= sic <= 3241) or (3250 <= sic <= 3259) or (sic == 3261) or
          (sic == 3264) or (3270 <= sic <= 3275) or (3280 <= sic <= 3281) or
          (3290 <= sic <= 3293) or (3420 <= sic <= 3429) or (3430 <= sic <= 3433) or
          (3440 <= sic <= 3441) or (sic == 3442) or (sic == 3446) or (sic == 3448) or
          (sic == 3449) or (3450 <= sic <= 3451) or (sic == 3452) or
          (5030 <= sic <= 5039) or (5070 <= sic <= 5078) or (sic == 5198) or
          (5210 <= sic <= 5211) or (5230 <= sic <= 5231) or (5250 <= sic <= 5251)):
        return 8
        
    # FF17 Industry 9: Steel Works Etc
    elif ((sic == 3300) or (3310 <= sic <= 3317) or (3320 <= sic <= 3325) or
          (3330 <= sic <= 3339) or (3340 <= sic <= 3341) or (3350 <= sic <= 3357) or
          (3360 <= sic <= 3369) or (3390 <= sic <= 3399)):
        return 9
        
    # FF17 Industry 10: Fabricated Products
    elif ((3410 <= sic <= 3412) or (sic == 3443) or (sic == 3444) or
          (3460 <= sic <= 3469) or (3470 <= sic <= 3479) or (3480 <= sic <= 3489) or
          (3490 <= sic <= 3499)):
        return 10
        
    # FF17 Industry 11: Machinery and Business Equipment  
    elif ((3510 <= sic <= 3519) or (3520 <= sic <= 3529) or (sic == 3530) or
          (sic == 3531) or (sic == 3532) or (sic == 3533) or (sic == 3534) or
          (sic == 3535) or (sic == 3536) or (3540 <= sic <= 3549) or
          (3550 <= sic <= 3559) or (3560 <= sic <= 3569) or (3570 <= sic <= 3579) or
          (sic == 3580) or (sic == 3581) or (sic == 3582) or (sic == 3585) or
          (sic == 3586) or (sic == 3589) or (3590 <= sic <= 3599) or
          (sic == 3600) or (3610 <= sic <= 3613) or (3620 <= sic <= 3621) or
          (sic == 3622) or (3623 <= sic <= 3629) or (3670 <= sic <= 3679) or
          (sic == 3680) or (sic == 3681) or (sic == 3682) or (sic == 3683) or
          (sic == 3684) or (sic == 3685) or (sic == 3686) or (sic == 3687) or
          (sic == 3688) or (sic == 3689) or (sic == 3690) or (3691 <= sic <= 3692) or
          (sic == 3693) or (sic == 3694) or (sic == 3695) or (sic == 3699) or
          (sic == 3810) or (sic == 3811) or (sic == 3812) or (sic == 3820) or
          (sic == 3821) or (sic == 3822) or (sic == 3823) or (sic == 3824) or
          (sic == 3825) or (sic == 3826) or (sic == 3827) or (sic == 3829) or
          (3830 <= sic <= 3839) or (3950 <= sic <= 3955) or (sic == 5060) or
          (sic == 5063) or (sic == 5065) or (sic == 5080) or (sic == 5081)):
        return 11
        
    # FF17 Industry 12: Automobiles
    elif ((sic == 3710) or (sic == 3711) or (sic == 3714) or (sic == 3716) or
          (3750 <= sic <= 3751) or (sic == 3792) or (5010 <= sic <= 5015) or
          (5510 <= sic <= 5521) or (5530 <= sic <= 5531) or (5560 <= sic <= 5561) or
          (5570 <= sic <= 5571) or (5590 <= sic <= 5599)):
        return 12
        
    # FF17 Industry 13: Transportation
    elif ((sic == 3713) or (sic == 3715) or (sic == 3720) or (sic == 3721) or
          (sic == 3724) or (sic == 3725) or (sic == 3728) or (3730 <= sic <= 3731) or
          (sic == 3732) or (3740 <= sic <= 3743) or (3760 <= sic <= 3769) or
          (sic == 3790) or (sic == 3795) or (sic == 3799) or (4000 <= sic <= 4013) or
          (sic == 4100) or (4110 <= sic <= 4119) or (4120 <= sic <= 4121) or
          (4130 <= sic <= 4131) or (4140 <= sic <= 4142) or (4150 <= sic <= 4151) or
          (4170 <= sic <= 4173) or (4190 <= sic <= 4199) or (sic == 4200) or
          (4210 <= sic <= 4219) or (4220 <= sic <= 4229) or (4230 <= sic <= 4231) or
          (4400 <= sic <= 4499) or (4500 <= sic <= 4599) or (4600 <= sic <= 4699) or
          (sic == 4700) or (4710 <= sic <= 4712) or (4720 <= sic <= 4729) or
          (4730 <= sic <= 4739) or (4740 <= sic <= 4742) or (sic == 4780) or
          (sic == 4783) or (sic == 4785) or (sic == 4789)):
        return 13
        
    # FF17 Industry 14: Utilities
    elif ((sic == 4900) or (4910 <= sic <= 4911) or (4920 <= sic <= 4922) or
          (sic == 4923) or (4924 <= sic <= 4925) or (4930 <= sic <= 4931) or
          (sic == 4932) or (sic == 4939) or (4940 <= sic <= 4942)):
        return 14
        
    # FF17 Industry 15: Retail Stores
    elif ((5260 <= sic <= 5261) or (5270 <= sic <= 5271) or (sic == 5300) or
          (5310 <= sic <= 5311) or (sic == 5320) or (5330 <= sic <= 5331) or
          (sic == 5334) or (5390 <= sic <= 5399) or (sic == 5400) or
          (5410 <= sic <= 5411) or (sic == 5412) or (5420 <= sic <= 5421) or
          (5430 <= sic <= 5431) or (5440 <= sic <= 5441) or (5450 <= sic <= 5451) or
          (5460 <= sic <= 5461) or (5490 <= sic <= 5499) or (5540 <= sic <= 5541) or
          (5550 <= sic <= 5551) or (5600 <= sic <= 5699) or (sic == 5700) or
          (5710 <= sic <= 5719) or (5720 <= sic <= 5722) or (5730 <= sic <= 5733) or
          (sic == 5734) or (sic == 5735) or (sic == 5736) or (sic == 5750) or
          (5800 <= sic <= 5813) or (sic == 5890) or (sic == 5900) or
          (5910 <= sic <= 5912) or (5920 <= sic <= 5921) or (5930 <= sic <= 5932) or
          (sic == 5940) or (sic == 5941) or (sic == 5942) or (sic == 5943) or
          (sic == 5944) or (sic == 5945) or (sic == 5946) or (sic == 5947) or
          (sic == 5948) or (sic == 5949) or (5960 <= sic <= 5963) or
          (5980 <= sic <= 5989) or (sic == 5990) or (sic == 5992) or (sic == 5993) or
          (sic == 5994) or (sic == 5995) or (sic == 5999)):
        return 15
        
    # FF17 Industry 16: Banks, Insurance Companies, and Other Financials
    elif ((6010 <= sic <= 6019) or (sic == 6020) or (sic == 6021) or (sic == 6022) or
          (sic == 6023) or (sic == 6025) or (sic == 6026) or (6028 <= sic <= 6029) or
          (6030 <= sic <= 6036) or (6040 <= sic <= 6049) or (6050 <= sic <= 6059) or
          (6060 <= sic <= 6062) or (6080 <= sic <= 6082) or (6090 <= sic <= 6099) or
          (sic == 6100) or (6110 <= sic <= 6111) or (sic == 6112) or
          (6120 <= sic <= 6129) or (6140 <= sic <= 6149) or (6150 <= sic <= 6159) or
          (6160 <= sic <= 6163) or (sic == 6172) or (sic == 6199) or
          (6200 <= sic <= 6299) or (sic == 6300) or (6310 <= sic <= 6312) or
          (6320 <= sic <= 6324) or (6330 <= sic <= 6331) or (6350 <= sic <= 6351) or
          (6360 <= sic <= 6361) or (6370 <= sic <= 6371) or (6390 <= sic <= 6399) or
          (6400 <= sic <= 6411) or (sic == 6500) or (sic == 6510) or (sic == 6512) or
          (sic == 6513) or (sic == 6514) or (sic == 6515) or (6517 <= sic <= 6519) or
          (6530 <= sic <= 6531) or (sic == 6532) or (6540 <= sic <= 6541) or
          (6550 <= sic <= 6553) or (sic == 6611) or (sic == 6700) or
          (6710 <= sic <= 6719) or (6720 <= sic <= 6722) or (sic == 6723) or
          (sic == 6724) or (sic == 6725) or (sic == 6726) or (6730 <= sic <= 6733) or
          (sic == 6790) or (sic == 6792) or (sic == 6794) or (sic == 6795) or
          (sic == 6798) or (sic == 6799)):
        return 16
        
    # FF17 Industry 17: Other
    elif (100 <= sic <= 9999):
        return 17
        
    else:
        return np.nan


def get_ff48(sic):
    """
    Fama-French 48 industry classification based on SIC code
    Translated directly from sicff.ado lines 521-615
    """
    if pd.isna(sic):
        return np.nan
    
    try:
        sic = int(sic)
    except (ValueError, TypeError):
        return np.nan
    
    # FF48 Industry 1: Agriculture
    if ((100 <= sic <= 199) or (200 <= sic <= 299) or (700 <= sic <= 799) or
        (910 <= sic <= 919) or (sic == 2048)):
        return 1
        
    # FF48 Industry 2: Food Products
    elif ((2000 <= sic <= 2009) or (2010 <= sic <= 2019) or (2020 <= sic <= 2029) or
          (2030 <= sic <= 2039) or (2040 <= sic <= 2046) or (2050 <= sic <= 2059) or
          (2060 <= sic <= 2063) or (2070 <= sic <= 2079) or (2090 <= sic <= 2092) or
          (sic == 2095) or (2098 <= sic <= 2099)):
        return 2
        
    # FF48 Industry 3: Candy & Soda
    elif ((2064 <= sic <= 2068) or (sic == 2086) or (sic == 2087) or (sic == 2096) or
          (sic == 2097)):
        return 3
        
    # FF48 Industry 4: Beer & Liquor
    elif ((sic == 2080) or (sic == 2082) or (sic == 2083) or (sic == 2084) or
          (sic == 2085)):
        return 4
        
    # FF48 Industry 5: Tobacco Products
    elif (2100 <= sic <= 2199):
        return 5
        
    # FF48 Industry 6: Recreation
    elif ((920 <= sic <= 999) or (3650 <= sic <= 3651) or (sic == 3652) or
          (sic == 3732) or (3930 <= sic <= 3931) or (3940 <= sic <= 3949)):
        return 6
        
    # FF48 Industry 7: Entertainment
    elif ((7800 <= sic <= 7829) or (7830 <= sic <= 7833) or (7840 <= sic <= 7841) or
          (sic == 7900) or (7910 <= sic <= 7911) or (7920 <= sic <= 7929) or
          (7930 <= sic <= 7933) or (7940 <= sic <= 7949) or (sic == 7980) or
          (7990 <= sic <= 7999)):
        return 7
        
    # FF48 Industry 8: Printing and Publishing
    elif ((2700 <= sic <= 2709) or (2710 <= sic <= 2719) or (2720 <= sic <= 2729) or
          (2730 <= sic <= 2739) or (2740 <= sic <= 2749) or (2770 <= sic <= 2771) or
          (2780 <= sic <= 2789) or (2790 <= sic <= 2799)):
        return 8
        
    # FF48 Industry 9: Consumer Goods
    elif ((sic == 2047) or (2391 <= sic <= 2392) or (2510 <= sic <= 2519) or
          (2590 <= sic <= 2599) or (2840 <= sic <= 2843) or (sic == 2844) or
          (3160 <= sic <= 3161) or (3170 <= sic <= 3171) or (sic == 3172) or
          (3190 <= sic <= 3199) or (sic == 3229) or (sic == 3260) or
          (3262 <= sic <= 3263) or (sic == 3269) or (3230 <= sic <= 3231) or
          (3630 <= sic <= 3639) or (3750 <= sic <= 3751) or (sic == 3800) or
          (3860 <= sic <= 3861) or (3870 <= sic <= 3873) or (3910 <= sic <= 3911) or
          (sic == 3914) or (sic == 3915) or (3960 <= sic <= 3962) or
          (sic == 3991) or (sic == 3995)):
        return 9
        
    # FF48 Industry 10: Apparel
    elif ((2300 <= sic <= 2390) or (3020 <= sic <= 3021) or (3100 <= sic <= 3111) or
          (3130 <= sic <= 3131) or (3140 <= sic <= 3149) or (3150 <= sic <= 3151) or
          (3963 <= sic <= 3965)):
        return 10
        
    # FF48 Industry 11: Healthcare
    elif (8000 <= sic <= 8099):
        return 11
        
    # FF48 Industry 12: Medical Equipment
    elif ((sic == 3693) or (3840 <= sic <= 3849) or (3850 <= sic <= 3851)):
        return 12
        
    # FF48 Industry 13: Pharmaceutical Products
    elif ((sic == 2830) or (sic == 2831) or (sic == 2833) or (sic == 2834) or
          (sic == 2835) or (sic == 2836)):
        return 13
        
    # FF48 Industry 14: Chemicals
    elif ((2800 <= sic <= 2809) or (2810 <= sic <= 2819) or (2820 <= sic <= 2829) or
          (2850 <= sic <= 2859) or (2860 <= sic <= 2869) or (2870 <= sic <= 2879) or
          (2890 <= sic <= 2899)):
        return 14
        
    # FF48 Industry 15: Rubber and Plastic Products
    elif ((sic == 3031) or (sic == 3041) or (3050 <= sic <= 3053) or
          (3060 <= sic <= 3069) or (3070 <= sic <= 3079) or (3080 <= sic <= 3089) or
          (3090 <= sic <= 3099)):
        return 15
        
    # FF48 Industry 16: Textiles
    elif ((2200 <= sic <= 2269) or (2270 <= sic <= 2279) or (2280 <= sic <= 2284) or
          (2290 <= sic <= 2295) or (sic == 2297) or (sic == 2298) or (sic == 2299) or
          (2393 <= sic <= 2395) or (2397 <= sic <= 2399)):
        return 16
        
    # FF48 Industry 17: Construction Materials
    elif ((800 <= sic <= 899) or (2400 <= sic <= 2439) or (2450 <= sic <= 2459) or
          (2490 <= sic <= 2499) or (2660 <= sic <= 2661) or (2950 <= sic <= 2952) or
          (sic == 3200) or (3210 <= sic <= 3211) or (3240 <= sic <= 3241) or
          (3250 <= sic <= 3259) or (sic == 3261) or (sic == 3264) or
          (3270 <= sic <= 3275) or (3280 <= sic <= 3281) or (3290 <= sic <= 3293) or
          (3295 <= sic <= 3299) or (3420 <= sic <= 3429) or (3430 <= sic <= 3433) or
          (3440 <= sic <= 3441) or (sic == 3442) or (sic == 3446) or (sic == 3448) or
          (sic == 3449) or (3450 <= sic <= 3451) or (sic == 3452) or
          (3490 <= sic <= 3499) or (sic == 3996)):
        return 17
        
    # FF48 Industry 18: Construction
    elif ((1500 <= sic <= 1511) or (1520 <= sic <= 1529) or (1530 <= sic <= 1539) or
          (1540 <= sic <= 1549) or (1600 <= sic <= 1699) or (1700 <= sic <= 1799)):
        return 18
        
    # FF48 Industry 19: Steel Works Etc
    elif ((sic == 3300) or (3310 <= sic <= 3317) or (3320 <= sic <= 3325) or
          (3330 <= sic <= 3339) or (3340 <= sic <= 3341) or (3350 <= sic <= 3357) or
          (3360 <= sic <= 3369) or (3370 <= sic <= 3379) or (3390 <= sic <= 3399)):
        return 19
        
    # FF48 Industry 20: Fabricated Products
    elif ((sic == 3400) or (sic == 3443) or (sic == 3444) or (3460 <= sic <= 3469) or
          (3470 <= sic <= 3479)):
        return 20
        
    # FF48 Industry 21: Machinery
    elif ((3510 <= sic <= 3519) or (3520 <= sic <= 3529) or (sic == 3530) or
          (sic == 3531) or (sic == 3532) or (sic == 3533) or (sic == 3534) or
          (sic == 3535) or (sic == 3536) or (sic == 3538) or (3540 <= sic <= 3549) or
          (3550 <= sic <= 3559) or (3560 <= sic <= 3569) or (sic == 3580) or
          (sic == 3581) or (sic == 3582) or (sic == 3585) or (sic == 3586) or
          (sic == 3589) or (3590 <= sic <= 3599)):
        return 21
        
    # FF48 Industry 22: Electrical Equipment
    elif ((sic == 3600) or (3610 <= sic <= 3613) or (3620 <= sic <= 3621) or
          (3623 <= sic <= 3629) or (3640 <= sic <= 3644) or (sic == 3645) or
          (sic == 3646) or (3648 <= sic <= 3649) or (sic == 3660) or (sic == 3690) or
          (3691 <= sic <= 3692) or (sic == 3699)):
        return 22
        
    # FF48 Industry 23: Automobiles and Trucks
    elif ((sic == 2296) or (sic == 2396) or (3010 <= sic <= 3011) or (sic == 3537) or
          (sic == 3647) or (sic == 3694) or (sic == 3700) or (sic == 3710) or
          (sic == 3711) or (sic == 3713) or (sic == 3714) or (sic == 3715) or
          (sic == 3716) or (sic == 3792) or (3790 <= sic <= 3791) or (sic == 3799)):
        return 23
        
    # FF48 Industry 24: Aircraft
    elif ((sic == 3720) or (sic == 3721) or (3723 <= sic <= 3724) or (sic == 3725) or
          (3728 <= sic <= 3729)):
        return 24
        
    # FF48 Industry 25: Shipbuilding, Railroad Equipment
    elif ((3730 <= sic <= 3731) or (3740 <= sic <= 3743)):
        return 25
        
    # FF48 Industry 26: Defense
    elif ((3760 <= sic <= 3769) or (sic == 3795) or (3480 <= sic <= 3489)):
        return 26
        
    # FF48 Industry 27: Precious Metals
    elif (1040 <= sic <= 1049):
        return 27
        
    # FF48 Industry 28: Non-Metallic and Industrial Metal Mining
    elif ((1000 <= sic <= 1009) or (1010 <= sic <= 1019) or (1020 <= sic <= 1029) or
          (1030 <= sic <= 1039) or (1050 <= sic <= 1059) or (1060 <= sic <= 1069) or
          (1070 <= sic <= 1079) or (1080 <= sic <= 1089) or (1090 <= sic <= 1099) or
          (1100 <= sic <= 1119) or (1400 <= sic <= 1499)):
        return 28
        
    # FF48 Industry 29: Coal
    elif (1200 <= sic <= 1299):
        return 29
        
    # FF48 Industry 30: Petroleum and Natural Gas
    elif ((sic == 1300) or (1310 <= sic <= 1319) or (1320 <= sic <= 1329) or
          (1330 <= sic <= 1339) or (1370 <= sic <= 1379) or (sic == 1380) or
          (sic == 1381) or (sic == 1382) or (sic == 1389) or (2900 <= sic <= 2912) or
          (2990 <= sic <= 2999)):
        return 30
        
    # FF48 Industry 31: Utilities
    elif ((sic == 4900) or (4910 <= sic <= 4911) or (4920 <= sic <= 4922) or
          (sic == 4923) or (4924 <= sic <= 4925) or (4930 <= sic <= 4931) or
          (sic == 4932) or (sic == 4939) or (4940 <= sic <= 4942)):
        return 31
        
    # FF48 Industry 32: Communication
    elif ((sic == 4800) or (4810 <= sic <= 4813) or (4820 <= sic <= 4822) or
          (4830 <= sic <= 4839) or (4840 <= sic <= 4841) or (4880 <= sic <= 4889) or
          (sic == 4890) or (sic == 4891) or (sic == 4892) or (sic == 4899)):
        return 32
        
    # FF48 Industry 33: Personal Services
    elif ((7020 <= sic <= 7021) or (7030 <= sic <= 7033) or (sic == 7200) or
          (7210 <= sic <= 7212) or (sic == 7214) or (7215 <= sic <= 7216) or
          (sic == 7217) or (sic == 7219) or (7220 <= sic <= 7221) or
          (7230 <= sic <= 7231) or (7240 <= sic <= 7241) or (7250 <= sic <= 7251) or
          (7260 <= sic <= 7269) or (7270 <= sic <= 7290) or (sic == 7291) or
          (7292 <= sic <= 7299) or (sic == 7395) or (sic == 7500) or
          (7520 <= sic <= 7529) or (7530 <= sic <= 7539) or (7540 <= sic <= 7549) or
          (sic == 7600) or (sic == 7620) or (sic == 7622) or (sic == 7623) or
          (sic == 7629) or (7630 <= sic <= 7631) or (7640 <= sic <= 7641) or
          (7690 <= sic <= 7699) or (8100 <= sic <= 8199) or (8200 <= sic <= 8299) or
          (8300 <= sic <= 8399) or (8400 <= sic <= 8499) or (8600 <= sic <= 8699) or
          (8800 <= sic <= 8899) or (7510 <= sic <= 7515)):
        return 33
        
    # FF48 Industry 34: Business Services
    elif ((2750 <= sic <= 2759) or (sic == 3993) or (sic == 7218) or (sic == 7300) or
          (7310 <= sic <= 7319) or (7320 <= sic <= 7329) or (7330 <= sic <= 7339) or
          (7340 <= sic <= 7342) or (sic == 7349) or (7350 <= sic <= 7351) or
          (sic == 7352) or (sic == 7353) or (sic == 7359) or (7360 <= sic <= 7369) or
          (7370 <= sic <= 7372) or (sic == 7374) or (sic == 7375) or (sic == 7376) or
          (sic == 7377) or (sic == 7378) or (sic == 7379) or (sic == 7380) or
          (7381 <= sic <= 7382) or (sic == 7383) or (sic == 7384) or (sic == 7385) or
          (7389 <= sic <= 7390) or (sic == 7391) or (sic == 7392) or (sic == 7393) or
          (sic == 7394) or (sic == 7396) or (sic == 7397) or (sic == 7399) or
          (sic == 7519) or (sic == 8700) or (8710 <= sic <= 8713) or
          (8720 <= sic <= 8721) or (8730 <= sic <= 8734) or (8740 <= sic <= 8748) or
          (8900 <= sic <= 8910) or (sic == 8911) or (8920 <= sic <= 8999) or
          (4220 <= sic <= 4229)):
        return 34
        
    # FF48 Industry 35: Computers
    elif ((3570 <= sic <= 3579) or (sic == 3680) or (sic == 3681) or (sic == 3682) or
          (sic == 3683) or (sic == 3684) or (sic == 3685) or (sic == 3686) or
          (sic == 3687) or (sic == 3688) or (sic == 3689) or (sic == 3695) or
          (sic == 7373)):
        return 35
        
    # FF48 Industry 36: Electronic Equipment
    elif ((sic == 3622) or (sic == 3661) or (sic == 3662) or (sic == 3663) or
          (sic == 3664) or (sic == 3665) or (sic == 3666) or (sic == 3669) or
          (3670 <= sic <= 3679) or (sic == 3810) or (sic == 3812)):
        return 36
        
    # FF48 Industry 37: Measuring and Control Equipment
    elif ((sic == 3811) or (sic == 3820) or (sic == 3821) or (sic == 3822) or
          (sic == 3823) or (sic == 3824) or (sic == 3825) or (sic == 3826) or
          (sic == 3827) or (sic == 3829) or (3830 <= sic <= 3839)):
        return 37
        
    # FF48 Industry 38: Business Supplies
    elif ((2520 <= sic <= 2549) or (2600 <= sic <= 2639) or (2670 <= sic <= 2699) or
          (2760 <= sic <= 2761) or (3950 <= sic <= 3955)):
        return 38
        
    # FF48 Industry 39: Shipping Containers
    elif ((2440 <= sic <= 2449) or (2640 <= sic <= 2659) or (3220 <= sic <= 3221) or
          (3410 <= sic <= 3412)):
        return 39
        
    # FF48 Industry 40: Transportation
    elif ((4000 <= sic <= 4013) or (4040 <= sic <= 4049) or (sic == 4100) or
          (4110 <= sic <= 4119) or (4120 <= sic <= 4121) or (4130 <= sic <= 4131) or
          (4140 <= sic <= 4142) or (4150 <= sic <= 4151) or (4170 <= sic <= 4173) or
          (4190 <= sic <= 4199) or (sic == 4200) or (4210 <= sic <= 4219) or
          (4230 <= sic <= 4231) or (4240 <= sic <= 4249) or (4400 <= sic <= 4499) or
          (4500 <= sic <= 4599) or (4600 <= sic <= 4699) or (sic == 4700) or
          (4710 <= sic <= 4712) or (4720 <= sic <= 4729) or (4730 <= sic <= 4739) or
          (4740 <= sic <= 4749) or (sic == 4780) or (sic == 4782) or (sic == 4783) or
          (sic == 4784) or (sic == 4785) or (sic == 4789)):
        return 40
        
    # FF48 Industry 41: Wholesale
    elif ((sic == 5000) or (5010 <= sic <= 5015) or (5020 <= sic <= 5023) or
          (5030 <= sic <= 5039) or (5040 <= sic <= 5042) or (sic == 5043) or
          (sic == 5044) or (sic == 5045) or (sic == 5046) or (sic == 5047) or
          (sic == 5048) or (sic == 5049) or (5050 <= sic <= 5059) or (sic == 5060) or
          (sic == 5063) or (sic == 5064) or (sic == 5065) or (5070 <= sic <= 5078) or
          (sic == 5080) or (sic == 5081) or (sic == 5082) or (sic == 5083) or
          (sic == 5084) or (sic == 5085) or (5086 <= sic <= 5087) or (sic == 5088) or
          (sic == 5090) or (5091 <= sic <= 5092) or (sic == 5093) or (sic == 5094) or
          (sic == 5099) or (sic == 5100) or (5110 <= sic <= 5113) or
          (5120 <= sic <= 5122) or (5130 <= sic <= 5139) or (5140 <= sic <= 5149) or
          (5150 <= sic <= 5159) or (5160 <= sic <= 5169) or (5170 <= sic <= 5172) or
          (5180 <= sic <= 5182) or (5190 <= sic <= 5199)):
        return 41
        
    # FF48 Industry 42: Retail
    elif ((sic == 5200) or (5210 <= sic <= 5219) or (5220 <= sic <= 5229) or
          (5230 <= sic <= 5231) or (5250 <= sic <= 5251) or (5260 <= sic <= 5261) or
          (5270 <= sic <= 5271) or (sic == 5300) or (5310 <= sic <= 5311) or
          (sic == 5320) or (5330 <= sic <= 5331) or (sic == 5334) or
          (5340 <= sic <= 5349) or (5390 <= sic <= 5399) or (sic == 5400) or
          (5410 <= sic <= 5411) or (sic == 5412) or (5420 <= sic <= 5429) or
          (5430 <= sic <= 5439) or (5440 <= sic <= 5449) or (5450 <= sic <= 5459) or
          (5460 <= sic <= 5469) or (5490 <= sic <= 5499) or (sic == 5500) or
          (5510 <= sic <= 5529) or (5530 <= sic <= 5539) or (5540 <= sic <= 5549) or
          (5550 <= sic <= 5559) or (5560 <= sic <= 5569) or (5570 <= sic <= 5579) or
          (5590 <= sic <= 5599) or (5600 <= sic <= 5699) or (sic == 5700) or
          (5710 <= sic <= 5719) or (5720 <= sic <= 5722) or (5730 <= sic <= 5733) or
          (sic == 5734) or (sic == 5735) or (sic == 5736) or (5750 <= sic <= 5799) or
          (sic == 5900) or (5910 <= sic <= 5912) or (5920 <= sic <= 5929) or
          (5930 <= sic <= 5932) or (sic == 5940) or (sic == 5941) or (sic == 5942) or
          (sic == 5943) or (sic == 5944) or (sic == 5945) or (sic == 5946) or
          (sic == 5947) or (sic == 5948) or (sic == 5949) or (5950 <= sic <= 5959) or
          (5960 <= sic <= 5969) or (5970 <= sic <= 5979) or (5980 <= sic <= 5989) or
          (sic == 5990) or (sic == 5992) or (sic == 5993) or (sic == 5994) or
          (sic == 5995) or (sic == 5999)):
        return 42
        
    # FF48 Industry 43: Restaurants, Hotels, Motels
    elif ((5800 <= sic <= 5819) or (5820 <= sic <= 5829) or (5890 <= sic <= 5899) or
          (sic == 7000) or (7010 <= sic <= 7019) or (7040 <= sic <= 7049) or
          (sic == 7213)):
        return 43
        
    # FF48 Industry 44: Banking
    elif ((sic == 6000) or (6010 <= sic <= 6019) or (sic == 6020) or (sic == 6021) or
          (sic == 6022) or (6023 <= sic <= 6024) or (sic == 6025) or (sic == 6026) or
          (sic == 6027) or (6028 <= sic <= 6029) or (6030 <= sic <= 6036) or
          (6040 <= sic <= 6059) or (6060 <= sic <= 6062) or (6080 <= sic <= 6082) or
          (6090 <= sic <= 6099) or (sic == 6100) or (6110 <= sic <= 6111) or
          (6112 <= sic <= 6113) or (6120 <= sic <= 6129) or (6130 <= sic <= 6139) or
          (6140 <= sic <= 6149) or (6150 <= sic <= 6159) or (6160 <= sic <= 6169) or
          (6170 <= sic <= 6179) or (6190 <= sic <= 6199)):
        return 44
        
    # FF48 Industry 45: Insurance
    elif ((sic == 6300) or (6310 <= sic <= 6319) or (6320 <= sic <= 6329) or
          (6330 <= sic <= 6331) or (6350 <= sic <= 6351) or (6360 <= sic <= 6361) or
          (6370 <= sic <= 6379) or (6390 <= sic <= 6399) or (6400 <= sic <= 6411)):
        return 45
        
    # FF48 Industry 46: Real Estate
    elif ((sic == 6500) or (sic == 6510) or (sic == 6512) or (sic == 6513) or
          (sic == 6514) or (sic == 6515) or (6517 <= sic <= 6519) or
          (6520 <= sic <= 6529) or (6530 <= sic <= 6531) or (sic == 6532) or
          (6540 <= sic <= 6541) or (6550 <= sic <= 6553) or (6590 <= sic <= 6599) or
          (6610 <= sic <= 6611)):
        return 46
        
    # FF48 Industry 47: Trading
    elif ((6200 <= sic <= 6299) or (sic == 6700) or (6710 <= sic <= 6719) or
          (6720 <= sic <= 6722) or (sic == 6723) or (sic == 6724) or (sic == 6725) or
          (sic == 6726) or (6730 <= sic <= 6733) or (6740 <= sic <= 6779) or
          (6790 <= sic <= 6791) or (sic == 6792) or (sic == 6793) or (sic == 6794) or
          (sic == 6795) or (sic == 6798) or (sic == 6799)):
        return 47
        
    # FF48 Industry 48: Almost Nothing
    elif ((4950 <= sic <= 4959) or (4960 <= sic <= 4961) or (4970 <= sic <= 4971) or
          (4990 <= sic <= 4991)):
        return 48
        
    else:
        return np.nan