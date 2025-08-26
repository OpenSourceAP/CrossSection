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
    signaldoc = signaldoc0[['Acronym', 'SampleStartYear','SampleEndYear','Cat.Form','Stock Weight','LS Quantile',
                           'Quantile Filter','Portfolio Period','Start Month','Test in OP','T-Stat']]

    # Read old t-statistics from PredictorSummaryOld.xlsx
    try:
        sumold = pd.read_excel('../DocsForClaude/PredictorSummaryOld.xlsx')
        old_tstat_dict = dict(zip(sumold['signalname'], sumold['tstat']))
        old_tstat = old_tstat_dict.get(signalcur, None)
    except:
        old_tstat = None

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
    
    # Also need exchcd for NYSE filtering
    crsp_exchcd = pd.read_parquet('../pyData/Intermediate/monthlyCRSP.parquet', 
                                  columns=['permno', 'time_avail_m', 'exchcd'])

    print('Processing portfolio assignments...')
    crsp = crsp0.copy()
    crsp['ret'] = crsp['ret']*100 # convert to percent
    
    # Merge exchcd for NYSE filtering
    signal = pd.merge(signal, crsp_exchcd[['permno', 'time_avail_m', 'exchcd']], 
                     on=['permno', 'time_avail_m'], how='left')

    # grab settings for current signal
    doccur = signaldoc.query('Acronym == @signalcur').to_dict('records')[0]
    
    # Fill in defaults for missing values
    if pd.isna(doccur.get('Portfolio Period')):
        doccur['Portfolio Period'] = 1
    if pd.isna(doccur.get('Start Month')):
        doccur['Start Month'] = 6
        
    # Helper function to assign portfolios using breakpoints
    def assign_portfolios_with_breakpoints(signal_df, q_cut, q_filt):
        """Assign portfolios using custom breakpoints similar to R implementation"""
        signal_df = signal_df.copy()
        
        # Apply quantile filter (e.g., NYSE only)
        tempbreak = signal_df.copy()
        if not pd.isna(q_filt) and q_filt == 'NYSE':
            tempbreak = tempbreak[tempbreak['exchcd'] == 1]
        
        # Create breakpoint list
        if q_cut <= 1/3:
            plist = np.arange(q_cut, 1-q_cut, q_cut).tolist() + [1-q_cut]
        else:
            plist = [q_cut, 1-q_cut] if q_cut != 1-q_cut else [q_cut]
        
        # Calculate breakpoints for each month
        breakpoints = []
        for pi, p in enumerate(plist, 1):
            breaks = tempbreak.groupby('time_avail_m')['signal'].quantile(p).reset_index()
            breaks.columns = ['time_avail_m', f'break{pi}']
            breakpoints.append(breaks)
        
        # Merge all breakpoints
        if breakpoints:
            breaklist = breakpoints[0]
            for breaks in breakpoints[1:]:
                breaklist = pd.merge(breaklist, breaks, on='time_avail_m')
        else:
            return signal_df
            
        # Merge breakpoints with signal data
        signal_df = pd.merge(signal_df, breaklist, on='time_avail_m', how='left')
        
        # Assign portfolios with tiebreaking rules
        signal_df['port'] = np.nan
        
        # Lowest portfolio: signal <= break1
        signal_df.loc[signal_df['signal'] <= signal_df['break1'], 'port'] = 1
        
        # Middle portfolios: strict inequality
        for i in range(2, len(plist) + 1):
            mask = (signal_df['port'].isna()) & (signal_df['signal'] < signal_df[f'break{i}'])
            signal_df.loc[mask, 'port'] = i
        
        # Highest portfolio: signal >= last break
        last_break = f'break{len(plist)}'
        mask = (signal_df['port'].isna()) & (signal_df['signal'] >= signal_df[last_break])
        signal_df.loc[mask, 'port'] = len(plist) + 1
        
        # Drop breakpoint columns
        signal_df = signal_df.drop(columns=[c for c in signal_df.columns if c.startswith('break')])
        
        return signal_df

    # Assign portfolios
    if doccur['Cat.Form'] == 'discrete':
        print('Discrete signal, port = signal')
        signal['port'] = signal['signal']
    else:
        # Continuous signal, use breakpoint-based assignment
        print('Continuous signal, assigning portfolios using breakpoints')
        signal = assign_portfolios_with_breakpoints(
            signal, 
            doccur['LS Quantile'], 
            doccur.get('Quantile Filter')
        )
    
    # Handle portfolio period and rebalancing months
    portperiod = int(doccur['Portfolio Period']) if not pd.isna(doccur['Portfolio Period']) else 1
    startmonth = int(doccur['Start Month']) if not pd.isna(doccur['Start Month']) else 6
    
    if portperiod > 1:
        # Calculate rebalancing months
        rebmonths = [(startmonth + i * portperiod - 1) % 12 + 1 for i in range(12)]
        rebmonths = sorted(list(set(rebmonths)))
        
        # Extract month from time_avail_m
        signal['month'] = pd.to_datetime(signal['time_avail_m']).dt.month
        
        # Only keep portfolio assignments in rebalancing months
        signal.loc[~signal['month'].isin(rebmonths), 'port'] = np.nan
        
        # Forward fill portfolio assignments
        signal = signal.sort_values(['permno', 'time_avail_m'])
        signal['port'] = signal.groupby('permno')['port'].ffill()
        
        # Drop intermediate columns
        signal = signal.drop(columns=['month'])
    
    # Remove rows with no portfolio assignment
    signal = signal.dropna(subset=['port'])
    signal['port'] = signal['port'].astype(int)
    
    # Lag signal and portfolio assignment by 1 month using manual yyyymm increment
    signal_lag = signal[['permno', 'time_avail_m', 'signal', 'port']].copy()
    
    # Convert time_avail_m to yyyymm for manual increment
    signal_lag['yyyymm'] = pd.to_datetime(signal_lag['time_avail_m']).dt.year * 100 + \
                           pd.to_datetime(signal_lag['time_avail_m']).dt.month
    signal_lag['yyyymm'] = signal_lag['yyyymm'] + 1
    
    # Handle month overflow (13 -> next year's January)
    signal_lag.loc[signal_lag['yyyymm'] % 100 == 13, 'yyyymm'] = \
        signal_lag.loc[signal_lag['yyyymm'] % 100 == 13, 'yyyymm'] + 100 - 12
    
    # Convert back to datetime
    signal_lag['time_avail_m'] = pd.to_datetime(
        (signal_lag['yyyymm'] // 100).astype(str) + '-' + 
        (signal_lag['yyyymm'] % 100).astype(str).str.zfill(2) + '-01'
    )
    
    signal_lag = signal_lag.rename(columns={'signal': 'signal_lag', 'port': 'port_lag'})
    signal_lag = signal_lag[['permno', 'time_avail_m', 'signal_lag', 'port_lag']]

    # Lag mve_c by 1 month using manual yyyymm increment
    temp_lag = crsp[['permno', 'time_avail_m', 'mve_c']].copy()
    temp_lag['yyyymm'] = pd.to_datetime(temp_lag['time_avail_m']).dt.year * 100 + \
                         pd.to_datetime(temp_lag['time_avail_m']).dt.month
    temp_lag['yyyymm'] = temp_lag['yyyymm'] + 1
    temp_lag.loc[temp_lag['yyyymm'] % 100 == 13, 'yyyymm'] = \
        temp_lag.loc[temp_lag['yyyymm'] % 100 == 13, 'yyyymm'] + 100 - 12
    temp_lag['time_avail_m'] = pd.to_datetime(
        (temp_lag['yyyymm'] // 100).astype(str) + '-' + 
        (temp_lag['yyyymm'] % 100).astype(str).str.zfill(2) + '-01'
    )
    temp_lag = temp_lag.rename(columns={'mve_c': 'me_lag'})
    temp_lag = temp_lag[['permno', 'time_avail_m', 'me_lag']]
    
    crsp = pd.merge(crsp, temp_lag, on=['permno', 'time_avail_m'], how='left')

    # Merge lagged signal with CRSP
    print('Merging data...')
    crsp = pd.merge(crsp[['permno', 'time_avail_m', 'ret', 'me_lag']], 
        signal_lag[['permno', 'time_avail_m', 'signal_lag', 'port_lag']], 
        on=['permno', 'time_avail_m'], how='left')
    crsp = crsp.dropna(subset=['signal_lag', 'port_lag', 'ret', 'me_lag'])

    # Use the port assignments that were already calculated and lagged
    crsp['port'] = crsp['port_lag']

    # calculate weighted returns
    if doccur['Stock Weight'] == 'EW':
        crsp['weight'] = 1
    else:
        crsp['weight'] = crsp['me_lag']
    crsp['weight'] = crsp['weight'] / \
        crsp.groupby(['time_avail_m','port'])['weight'].transform('sum')
    crsp['ret_weighted'] = crsp['ret'] * crsp['weight']

    # calculate portfolio returns
    if doccur['Stock Weight'] == 'EW':
        port = crsp.groupby(['time_avail_m','port']).agg(
            ret = ("ret", "mean"),
            nstock = ("permno", "count")
        ).reset_index()
    else:
        # Value-weighted returns
        port = crsp.groupby(['time_avail_m','port']).agg(
            ret = ("ret_weighted", "sum"),
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
        'tstat_old': old_tstat,
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
        if results['tstat_old'] is not None:
            print(f"  T-Stat (Old):    {results['tstat_old']:8.2f}")
        else:
            print(f"  T-Stat (Old):         N/A")
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