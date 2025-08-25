#%%
# ABOUTME: Portfolio analysis script for testing signal performance
# ABOUTME: Usage: python3 utils/portcheck.py [signal_acronym] (defaults to BM)

import os
import sys
import argparse
import numpy as np
import pandas as pd

# Change to pyCode directory
os.chdir(os.path.dirname(os.path.abspath(__file__)) + '/..')

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stata_replication import stata_lag

def run_portcheck(signalcur):
    """Run portfolio check for given signal and return results"""
    
    print(f'Analyzing signal: {signalcur}')
    print('Reading in data...')

    # Read signaldoc and extract settings for selected signal
    signaldoc0 = pd.read_csv('../DocsForClaude/SignalDoc-Copy.csv')
    signaldoc = signaldoc0[['Acronym', 'SampleStartYear','SampleEndYear','Cat.Form','Stock Weight','LS Quantile','Test in OP','T-Stat']]

    # Assume EW, 0.10, if missing
    signaldoc.loc[signaldoc['Stock Weight'].isna(), 'Stock Weight'] = 'EW'
    signaldoc.loc[signaldoc['LS Quantile'].isna(), 'LS Quantile'] = 0.10

    # Read the selected signal
    signal0 = pd.read_csv(f'../pyData/Predictors/{signalcur}.csv')

    signal = signal0.copy()
    signal['time_avail_m'] = pd.to_datetime(signal['yyyymm'], format='%Y%m')
    signal.rename(columns={signalcur: 'signal'}, inplace=True)

    # Read monthly CRSP data
    crsp0 = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet')

    print('Lagging signal and market equity...')
    crsp = crsp0.copy()
    crsp['ret'] = crsp['ret']*100 # convert to percent

    # Lag signal by 1 month using most robust method
    signal_lag = pd.DataFrame(
        {
            'permno': signal['permno'],
            'time_avail_m': signal['time_avail_m'] + pd.DateOffset(months=1),
            'signal_lag': signal['signal']
        }
    )

    # Lag mve_c by 1 month  
    temp_lag = pd.DataFrame(
        {
            'permno': crsp['permno'],
            'time_avail_m': crsp['time_avail_m'] + pd.DateOffset(months=1),
            'me_lag': crsp['mve_c']
        }
    )
    crsp = pd.merge(crsp, temp_lag, on=['permno', 'time_avail_m'], how='left')

    # Merge lagged signal with CRSP
    print('Merging data...')
    crsp = pd.merge(crsp[['permno', 'time_avail_m', 'ret', 'me_lag']], 
        signal_lag[['permno', 'time_avail_m', 'signal_lag']], 
        on=['permno', 'time_avail_m'], how='left')
    crsp = crsp.dropna(subset=['signal_lag', 'ret', 'me_lag'])

    # grab settings for current signal
    doccur = signaldoc.query('Acronym == @signalcur').to_dict('records')[0]

    # assign port
    if doccur['Cat.Form'] == 'discrete':
        print('Discrete signal, port = signal_lag')
        crsp['port'] = crsp['signal_lag']
    else:
        # continuous signal, port is the quantile of signal_lag
        crsp['port'] = crsp.groupby('time_avail_m')['signal_lag'].transform(
            lambda x: pd.qcut(x, round(1/doccur['LS Quantile']), labels=False) + 1
        )

    # calculate weighted returns
    if doccur['Stock Weight'] == 'EW':
        crsp['weight'] = 1
    else:
        crsp['weight'] = crsp['me_lag']
    crsp['weight'] = crsp['weight'] / \
        crsp.groupby(['time_avail_m','port'])['weight'].transform('sum')
    crsp['ret_weighted'] = crsp['ret'] * crsp['weight']

    # calculate portfolio returns
    port = crsp.groupby(['time_avail_m','port']).agg(
        # ret = ("ret_weighted", "sum"),
        ret = ("ret", "mean"),
        nstock = ("permno", "count")
    ).reset_index()

    # long-short portfolio
    longport = port['port'].max()
    shortport = port['port'].min()

    long = port.query(f"port == {longport}").rename({'ret': 'retlong', 'nstock': 'nlong'}, axis=1).drop('port', axis=1)
    short = port.query(f"port == {shortport}").rename({'ret': 'retshort', 'nstock': 'nshort'}, axis=1).drop('port', axis=1)

    ls = pd.merge(long, short, on='time_avail_m', how='left')\
        .assign(
            ret = lambda x: x['retlong'] - x['retshort']
        )

    # portfolio returns
    datestart = pd.to_datetime(f'{doccur["SampleStartYear"]}-01-01')
    dateend = pd.to_datetime(f'{doccur["SampleEndYear"]}-12-31')

    ls_samp = ls.query('time_avail_m >= @datestart'
          '& time_avail_m <= @dateend')

    # Calculate statistics
    stats = ls_samp['ret'].agg(rbar='mean', vol='std', T='count')
    tstat = stats['rbar'] / stats['vol'] * np.sqrt(stats['T'])
    
    sample_period = ls_samp['time_avail_m'].agg(min='min', max='max')
    
    nstocks = ls_samp[['nlong', 'nshort']].mean()
    
    return {
        'signal': signalcur,
        'rbar': stats['rbar'],
        'vol': stats['vol'],
        'T': stats['T'],
        'tstat': round(tstat, 2),
        'tstat_op': doccur['T-Stat'],
        'sample_start': sample_period['min'],
        'sample_end': sample_period['max'],
        'nlong': int(round(nstocks['nlong'])),
        'nshort': int(round(nstocks['nshort']))
    }

def main():
    """Main function with command line interface"""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Portfolio analysis for signal performance')
    parser.add_argument('signal', nargs='?', default='BM', help='Signal acronym (default: BM)')
    args = parser.parse_args()

    signalcur = args.signal
    
    try:
        results = run_portcheck(signalcur)
        
        # Format output
        print("\n" + "="*60)
        print(f"PORTFOLIO ANALYSIS RESULTS: {results['signal']}")
        print("="*60)
        
        print(f"\nReturn Statistics:")
        print(f"  Mean Return:     {results['rbar']:8.4f}%")
        print(f"  Volatility:      {results['vol']:8.4f}%")
        print(f"  Observations:    {results['T']:8.0f}")
        print(f"  T-Statistic:     {results['tstat']:8.2f}")
        print(f"  T-Stat (OP):     {results['tstat_op']:8.2f}")
        
        print(f"\nSample Period:")
        print(f"  Start:           {results['sample_start'].strftime('%Y-%m-%d')}")
        print(f"  End:             {results['sample_end'].strftime('%Y-%m-%d')}")
        
        print(f"\nPortfolio Composition:")
        print(f"  Avg Long Stocks: {results['nlong']:8d}")
        print(f"  Avg Short Stocks:{results['nshort']:8d}")
        
        print("="*60)
        
    except Exception as e:
        print(f"Error analyzing signal {signalcur}: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()