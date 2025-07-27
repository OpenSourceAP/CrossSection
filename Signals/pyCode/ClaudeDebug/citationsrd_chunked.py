# ABOUTME: Debug version with chunked processing to avoid timeouts
# ABOUTME: Run from pyCode/ directory: python3 ClaudeDebug/citationsrd_chunked.py

import pandas as pd
import numpy as np

print("Testing chunked processing approach...")

# Test the key fix - assign missing tempCitationsRD to bottom tercile
df_test = pd.DataFrame({
    'time_avail_m': pd.to_datetime(['1989-06-01'] * 5),
    'tempCitationsRD': [np.nan, 0.5, np.nan, 1.2, np.nan],
    'sizecat': [1, 1, 1, 1, 2]
})

def calculate_terciles(group):
    group['maincat'] = np.nan
    # KEY FIX: Assign maincat=1 to observations with missing tempCitationsRD
    group.loc[group['tempCitationsRD'].isna(), 'maincat'] = 1
    
    valid_data = group.dropna(subset=['tempCitationsRD'])
    if len(valid_data) > 0:
        try:
            terciles = pd.qcut(valid_data['tempCitationsRD'], q=3, labels=[1, 2, 3], duplicates='drop')
            group.loc[valid_data.index, 'maincat'] = terciles
        except ValueError:
            # Simple fallback
            sorted_data = valid_data.sort_values('tempCitationsRD')
            n = len(sorted_data)
            group.loc[sorted_data.index[:n//3 or 1], 'maincat'] = 1
            group.loc[sorted_data.index[n//3:2*n//3], 'maincat'] = 2
            group.loc[sorted_data.index[2*n//3:], 'maincat'] = 3
    return group

df_test = df_test.groupby('time_avail_m').apply(calculate_terciles).reset_index(drop=True)

df_test['CitationsRD'] = np.nan
df_test.loc[(df_test['sizecat'] == 1) & (df_test['maincat'] == 1), 'CitationsRD'] = 0
df_test.loc[(df_test['sizecat'] == 1) & (df_test['maincat'] == 3), 'CitationsRD'] = 1

print("Test results:")
print(df_test[['tempCitationsRD', 'sizecat', 'maincat', 'CitationsRD']].to_string())

# This shows the fix works - missing tempCitationsRD gets CitationsRD=0 when small size
missing_assigned = df_test[(df_test['tempCitationsRD'].isna()) & (df_test['sizecat'] == 1)]
print(f"\nMissing tempCitationsRD with sizecat=1 gets CitationsRD: {missing_assigned['CitationsRD'].tolist()}")