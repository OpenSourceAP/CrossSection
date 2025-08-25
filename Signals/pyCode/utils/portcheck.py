# ABOUTME: Portfolio analysis script for testing signal performance
# ABOUTME: Usage: python3 utils/portcheck.py [signal_acronym] (defaults to BM)

import os
import sys
import argparse
import numpy as np
import pandas as pd

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stata_replication import stata_lag

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Portfolio analysis for signal performance')
    parser.add_argument('signal', nargs='?', default='BM', help='Signal acronym (default: BM)')
    args = parser.parse_args()
    
    signalcur = args.signal
    
    # Change to pyCode directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

    print(f'Analyzing signal: {signalcur}')
    print('Reading in data...')
    
    # Read signaldoc and extract settings for selected signal
    signaldoc0 = pd.read_csv('../DocsForClaude/SignalDoc-Copy.csv')
    signaldoc = signaldoc0[['Acronym', 'SampleStartYear','SampleEndYear','Stock Weight','LS Quantile','Test in OP','T-Stat']]
    
    # Assume EW, 0.10, if missing
    signaldoc.loc[signaldoc['Stock Weight'].isna(), 'Stock Weight'] = 'EW'
    signaldoc.loc[signaldoc['LS Quantile'].isna(), 'LS Quantile'] = 0.10
    
    # Extract settings for current signal
    signal_settings = signaldoc[signaldoc['Acronym'] == signalcur]
    if signal_settings.empty:
        print(f'ERROR: Signal {signalcur} not found in SignalDoc')
        sys.exit(1)
    
    settings = signal_settings.iloc[0]
    start_year = int(settings['SampleStartYear'])
    end_year = int(settings['SampleEndYear']) 
    weight_scheme = settings['Stock Weight']
    ls_quantile = float(settings['LS Quantile'])
    
    print(f'Signal settings: {weight_scheme} weights, {ls_quantile} quantile, sample {start_year}-{end_year}')
    
    # Read monthly CRSP data
    crsp = pd.read_stata('../Data/Intermediate/monthlyCRSP.dta',
                         columns=['permno','time_avail_m','ret','mve_c'])
    
    # Read the selected signal
    try:
        signal = pd.read_csv(f'../Data/Predictors/{signalcur}.csv')
    except FileNotFoundError:
        print(f'ERROR: Signal file ../Data/Predictors/{signalcur}.csv not found')
        sys.exit(1)
    
    print('Lagging signal and market equity...')
    
    # Convert signal yyyymm to datetime first
    signal['time_avail_m'] = pd.to_datetime(signal['yyyymm'], format='%Y%m')
    
    # Lag signal by 1 month using stata_lag
    signal[f'{signalcur}_lag1'] = stata_lag(signal, 'permno', 'time_avail_m', signalcur, 1, freq='M')
    
    # Lag mve_c by 1 month  
    crsp['mve_c_lag1'] = stata_lag(crsp, 'permno', 'time_avail_m', 'mve_c', 1, freq='M')
    
    # Merge lagged signal with CRSP
    print('Merging data...')
    merged = pd.merge(crsp, signal[['permno', 'time_avail_m', f'{signalcur}_lag1']], 
                     on=['permno', 'time_avail_m'], how='inner')
    
    # Drop rows with missing signal or return data
    merged = merged.dropna(subset=[f'{signalcur}_lag1', 'ret', 'mve_c_lag1'])
    
    print('Forming portfolios...')
    
    # Form portfolios for each month
    portfolio_returns = []
    
    for date, group in merged.groupby('time_avail_m'):
        if len(group) < 10:  # Need minimum stocks
            continue
            
        # Calculate quantile breakpoints
        signal_values = group[f'{signalcur}_lag1']
        low_cutoff = signal_values.quantile(ls_quantile)
        high_cutoff = signal_values.quantile(1 - ls_quantile)
        
        # Assign to portfolios
        short_port = group[signal_values <= low_cutoff]
        long_port = group[signal_values >= high_cutoff]
        
        if len(short_port) == 0 or len(long_port) == 0:
            continue
            
        # Calculate portfolio returns
        if weight_scheme == 'EW':
            short_ret = short_port['ret'].mean()
            long_ret = long_port['ret'].mean()
        else:  # VW
            short_weights = short_port['mve_c_lag1'] / short_port['mve_c_lag1'].sum()
            long_weights = long_port['mve_c_lag1'] / long_port['mve_c_lag1'].sum()
            short_ret = (short_port['ret'] * short_weights).sum()
            long_ret = (long_port['ret'] * long_weights).sum()
        
        # Long-short return
        ls_ret = long_ret - short_ret
        portfolio_returns.append({'time_avail_m': date, 'ls_return': ls_ret})
    
    # Convert to DataFrame
    if len(portfolio_returns) == 0:
        print('ERROR: No portfolio returns calculated')
        sys.exit(1)
        
    port_df = pd.DataFrame(portfolio_returns)
    port_df['year'] = port_df['time_avail_m'].dt.year
    
    print('Computing statistics...')
    
    # Filter to sample period for statistics
    sample_data = port_df[(port_df['year'] >= start_year) & (port_df['year'] <= end_year)]
    
    if len(sample_data) == 0:
        print(f'ERROR: No data available in sample period {start_year}-{end_year}')
        sys.exit(1)
    
    # Calculate statistics
    mean_ret = sample_data['ls_return'].mean()
    vol = sample_data['ls_return'].std()
    n_obs = len(sample_data)
    t_stat = mean_ret / (vol / np.sqrt(n_obs)) if vol > 0 else np.nan
    
    # Output results
    print('\n' + '='*50)
    print(f'PORTFOLIO ANALYSIS RESULTS: {signalcur}')
    print('='*50)
    print(f'Sample Period: {start_year}-{end_year}')
    print(f'Weighting Scheme: {weight_scheme}')
    print(f'Long-Short Quantile: {ls_quantile:.2f}')
    print(f'Number of Months: {n_obs}')
    print(f'Mean L-S Return: {mean_ret*100:.4f}%')
    print(f'Volatility: {vol*100:.4f}%')
    print(f'T-Statistic: {t_stat:.4f}')
    print('='*50)


if __name__ == '__main__':
    main()
