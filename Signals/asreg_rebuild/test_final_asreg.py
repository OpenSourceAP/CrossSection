#!/usr/bin/env python3
# ABOUTME: Test asreg function on MWE 4 (cross-sectional analysis)
# ABOUTME: Verifies that asreg with cross_sectional=True matches Stata's "bys time_avail_m: asreg"

import pandas as pd
from stata_regress import asreg

def main():
    # Load data
    df = pd.read_csv("mwe/tf_mwe4.csv")
    
    print("Final test: Cross-sectional asreg for MWE 4")
    print("=" * 55)
    
    # Run cross-sectional asreg using the enhanced asreg function
    results = asreg(
        df,
        y='fRet',
        X='A_*',  # Will be expanded to all A_* columns
        by='time_avail_m',
        cross_sectional=True,  # This is the key parameter!
        add_constant=True,
        drop_collinear=True
    )
    
    print(f"Results shape: {results.shape}")
    print(f"Columns: {list(results.columns)}")
    
    # Show results for permno == 10006 (to match Stata output)
    permno_10006_results = results[df['permno'] == 10006].copy()
    permno_10006_results['time_avail_m'] = df.loc[df['permno'] == 10006, 'time_avail_m'].values
    
    print("\nResults for permno == 10006:")
    print("-" * 40)
    
    display_cols = ['time_avail_m', '_Nobs', '_R2', '_adjR2']
    # Add key coefficient columns
    key_coefs = ['_b_A_3', '_b_A_5', '_b_A_10', '_b_A_20', '_b_A_50', '_b_A_100', '_b_A_200', '_b_A_400', '_b_A_600', '_b_A_800', '_b_A_1000', '_b_cons']
    available_coefs = [col for col in key_coefs if col in results.columns]
    
    all_display_cols = display_cols + available_coefs
    available_display_cols = [col for col in all_display_cols if col in permno_10006_results.columns or col == 'time_avail_m']
    
    print(permno_10006_results[available_display_cols].head().to_string(index=False, float_format='%.6f'))
    
    # Compare with Stata output
    print(f"\n" + "="*55)
    print("Comparison with Stata (first 5 periods):")
    print("="*55)
    
    stata_expected = [
        ('1926m1', 433, 0.013602, 0.551264, -0.013161, -0.056446, -0.438033),
        ('1926m2', 436, 0.059242, 1.443288, -0.986575, -0.161710, -0.305843),
        ('1926m3', 440, 0.069036, -0.611443, -0.272397, 1.670925, 0.024574),
        ('1926m4', 442, 0.085879, -0.555893, 0.231018, 1.207497, -0.092095),
        ('1926m5', 448, 0.064038, -0.808939, 0.969909, -0.941667, 0.111988)
    ]
    
    print("Period    Metric      Python     Stata      Match")
    print("-" * 55)
    
    for i, (period, st_nobs, st_r2, st_a3, st_a5, st_a10, st_cons) in enumerate(stata_expected):
        if i < len(permno_10006_results):
            py_row = permno_10006_results.iloc[i]
            
            nobs_match = "✅" if abs(py_row['_Nobs'] - st_nobs) < 0.1 else "❌"
            r2_match = "✅" if abs(py_row['_R2'] - st_r2) < 1e-5 else "❌"
            a3_match = "✅" if abs(py_row['_b_A_3'] - st_a3) < 1e-5 else "❌"
            cons_match = "✅" if abs(py_row['_b_cons'] - st_cons) < 1e-5 else "❌"
            
            print(f"{period}   _Nobs      {py_row['_Nobs']:.0f}        {st_nobs}        {nobs_match}")
            print(f"{period}   _R2        {py_row['_R2']:.6f}   {st_r2:.6f}   {r2_match}")
            print(f"{period}   _b_A_3     {py_row['_b_A_3']:.6f}   {st_a3:.6f}   {a3_match}")
            print(f"{period}   _b_cons    {py_row['_b_cons']:.6f}   {st_cons:.6f}   {cons_match}")
            print()

    # Summary
    all_match = True
    for i, (period, st_nobs, st_r2, st_a3, st_a5, st_a10, st_cons) in enumerate(stata_expected):
        if i < len(permno_10006_results):
            py_row = permno_10006_results.iloc[i]
            if (abs(py_row['_Nobs'] - st_nobs) >= 0.1 or 
                abs(py_row['_R2'] - st_r2) >= 1e-5 or
                abs(py_row['_b_A_3'] - st_a3) >= 1e-5 or
                abs(py_row['_b_cons'] - st_cons) >= 1e-5):
                all_match = False
                break
    
    if all_match:
        print("🎉 SUCCESS: All results match Stata within numerical precision!")
        print("The cross-sectional asreg implementation works correctly!")
    else:
        print("❌ Some differences found - check implementation")

if __name__ == "__main__":
    main()