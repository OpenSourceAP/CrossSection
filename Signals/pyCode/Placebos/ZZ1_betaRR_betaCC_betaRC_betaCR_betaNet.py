# ABOUTME: Calculates liquidity betas (betaRR, betaCC, betaRC, betaCR, betaNet) using Acharya-Pedersen methodology
# ABOUTME: Input: dailyCRSP, monthlyCRSP, monthlyMarket parquet files; Output: 5 CSV files in pyData/Placebos/
#%%
import pandas as pd
import numpy as np
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from utils.saveplacebo import save_placebo
from utils.stata_replication import fill_date_gaps, stata_multi_lag
from utils.stata_regress import asreg
#%%

def main():
    #%%
    print("Starting ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet.py")
    
    # DATA LOAD - Compute illiquidity from daily CRSP data
    print("Loading daily CRSP data...")
    daily_crsp = pd.read_parquet('../../pyData/Intermediate/dailyCRSP.parquet', 
                                columns=['permno', 'time_d', 'ret', 'vol', 'prc'])
    
    # Convert time_d to monthly periods (equivalent to mofd)
    daily_crsp['time_avail_m'] = daily_crsp['time_d'].dt.to_period('M').dt.start_time
    
    # Compute illiquidity with explicit null handling
    daily_crsp['ill'] = (daily_crsp['ret'].abs() / (daily_crsp['prc'].abs() * daily_crsp['vol'])) * 1e6
    
    # Collapse by permno and time_avail_m to get mean illiquidity
    temp_ill = daily_crsp.groupby(['permno', 'time_avail_m'])['ill'].mean().reset_index()
    
    print("Loading monthly CRSP data...")
    # Load monthly data
    monthly_crsp = pd.read_parquet('../../pyData/Intermediate/monthlyCRSP.parquet',
                                  columns=['permno', 'time_avail_m', 'ret', 'prc', 'exchcd', 'shrout'])
    
    # Merge with illiquidity data
    df = monthly_crsp.merge(temp_ill, on=['permno', 'time_avail_m'], how='left')
    
    # Merge with market data
    market = pd.read_parquet('../../pyData/Intermediate/monthlyMarket.parquet',
                            columns=['time_avail_m', 'vwretd', 'usdval'])
    df = df.merge(market, on='time_avail_m', how='inner')
    
    # SIGNAL CONSTRUCTION
    print("Processing signal construction...")
    
    # Index market capitalization relative to July 1962
    july_1962 = pd.to_datetime('1962-07-01')
    july_1962_val = df.loc[df['time_avail_m'] == july_1962, 'usdval'].mean()
    if pd.isna(july_1962_val):
        print("Warning: No July 1962 market cap data found, using first available value")
        july_1962_val = df['usdval'].dropna().iloc[0]
    
    df['usdval'] = df['usdval'] / july_1962_val
    df = df.rename(columns={'usdval': 'MarketCapitalization'})
    
    # Use fill_date_gaps for proper calendar-based lags
    print("Filling date gaps for proper lag operations...")
    df = fill_date_gaps(df, 'permno', 'time_avail_m')
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Create lags using stata_multi_lag for calendar-based alignment
    df = stata_multi_lag(df, 'permno', 'time_avail_m', 'MarketCapitalization', [1, 2], prefix='l')
    df = stata_multi_lag(df, 'permno', 'time_avail_m', 'ill', [1, 2], prefix='l')
    
    # Compute c_i with proper bounds
    df['c_i'] = np.minimum(0.25 + 0.3 * df['ill'] * df['MarketCapitalization'], 30)
    
    # Compute market illiquidity innovation and market return innovation
    print("Computing market innovations...")
    
    # Market filtering ONLY for market aggregation (like Stata preserve/restore)
    market_subset = df[
        (df['prc'].abs() > 5) & 
        (df['prc'].abs() < 1000) & 
        ((df['exchcd'] == 1) | (df['exchcd'] == 2)) &
        df['prc'].notna() & 
        df['exchcd'].notna()
    ].copy()
    
    print(f"Market aggregation: {len(df)} -> {len(market_subset)} observations after filtering")
    
    # Market cap of stock i
    market_subset['temp'] = market_subset['shrout'] * market_subset['prc'].abs()
    
    # Unnormalized liquidity with proper missing handling  
    # Convert Float64 to float64 to avoid aggregation issues
    market_subset['ill_float64'] = market_subset['ill'].astype('float64')
    market_subset['temp2'] = np.minimum(
        market_subset['ill_float64'], 
        (30 - 0.25) / (0.3 * market_subset['MarketCapitalization'])
    )
    market_subset.loc[market_subset['ill_float64'].isna(), 'temp2'] = np.nan
    
    # Calculate weighted averages by time_avail_m
    market_agg = market_subset.groupby('time_avail_m').apply(
        lambda x: pd.Series({
            'MarketIlliquidity': (x['temp2'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan,
            'rM': (x['vwretd'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan,
            'MarketCapitalization': (x['MarketCapitalization'] * x['temp']).sum() / x['temp'].sum() if x['temp'].sum() > 0 else np.nan
        })
    ).reset_index()
    
    # Sort market data and create proper calendar-based lags
    market_agg = market_agg.sort_values('time_avail_m')
    
    # Create a dummy group column for market aggregation (single time series)
    market_agg['market_group'] = 'market'
    
    # Create proper calendar-based lags using stata_multi_lag
    market_agg = stata_multi_lag(market_agg, 'market_group', 'time_avail_m', 'MarketCapitalization', [1, 2], prefix='l')
    market_agg = stata_multi_lag(market_agg, 'market_group', 'time_avail_m', 'MarketIlliquidity', [1, 2], prefix='l')
    market_agg = stata_multi_lag(market_agg, 'market_group', 'time_avail_m', 'rM', [1, 2], prefix='l')
    
    # Drop the dummy group column
    market_agg = market_agg.drop('market_group', axis=1)
    
    # Compute temp variables for illiquidity regression
    market_agg['temp'] = 0.25 + market_agg['MarketIlliquidity'] * market_agg['l1_MarketCapitalization']
    market_agg['templ1'] = 0.25 + market_agg['l1_MarketIlliquidity'] * market_agg['l1_MarketCapitalization']
    market_agg['templ2'] = 0.25 + market_agg['l2_MarketIlliquidity'] * market_agg['l1_MarketCapitalization']
    
    # Rolling regression for market illiquidity (asreg temp templ1 templ2)
    print("Running rolling regressions for market model...")
    
    # Use proper asreg function for illiquidity regression
    illiquidity_results = asreg(
        market_agg,
        y='temp',
        X=['templ1', 'templ2'],
        time='time_avail_m',
        window=60,
        min_obs=48,
        add_constant=True,
        compute_se=False
    )
    
    # Extract coefficients and calculate residuals manually (matching Stata asreg behavior)
    market_agg['APa0'] = illiquidity_results['_b_cons']
    market_agg['APa1'] = illiquidity_results['_b_templ1']
    market_agg['APa2'] = illiquidity_results['_b_templ2']
    
    # Calculate residuals manually for illiquidity regression
    fitted_temp = (market_agg['APa0'] + 
                   market_agg['APa1'] * market_agg['templ1'] + 
                   market_agg['APa2'] * market_agg['templ2'])
    market_agg['eps_c_M'] = market_agg['temp'] - fitted_temp
    
    # Use proper asreg function for return regression
    return_results = asreg(
        market_agg,
        y='rM',
        X=['l1_rM', 'l2_rM'],
        time='time_avail_m',
        window=60,
        min_obs=48,
        add_constant=True,
        compute_se=False
    )
    
    # Calculate residuals manually for return regression
    fitted_rM = (return_results['_b_cons'] + 
                 return_results['_b_l1_rM'] * market_agg['l1_rM'] + 
                 return_results['_b_l2_rM'] * market_agg['l2_rM'])
    market_agg['eps_r_M'] = market_agg['rM'] - fitted_rM
    
    # Keep only needed columns for merge
    temp_placebo = market_agg[['time_avail_m', 'eps_c_M', 'eps_r_M', 'APa0', 'APa1', 'APa2']].copy()
    
    # Merge with proper coefficient preservation
    print("Merging market innovations back to stock data...")
    df = df.merge(temp_placebo, on='time_avail_m', how='left')
    
    # Compute stock-level innovation in illiquidity
    print("Computing stock-level illiquidity innovations...")
    
    # Unnormalized liquidity for each stock (exactly as in Stata)
    df['tempIll'] = np.minimum(df['ill'], (30 - 0.25) / (0.3 * df['MarketCapitalization']))
    df.loc[df['ill'].isna(), 'tempIll'] = np.nan  # Handle missing values correctly
    
    # Create lags for tempIll using calendar-based lags  
    df = stata_multi_lag(df, 'permno', 'time_avail_m', 'tempIll', [1, 2], prefix='l')
    
    # Stock-specific temp variables (not using market values!)
    df['temp'] = 0.25 + df['tempIll'] * df['l1_MarketCapitalization']
    df['templ1'] = 0.25 + df['l1_tempIll'] * df['l1_MarketCapitalization'] 
    df['templ2'] = 0.25 + df['l2_tempIll'] * df['l1_MarketCapitalization']
    
    # Stock illiquidity innovation using STOCK-SPECIFIC temp variables with MARKET coefficients
    # This is the exact Stata formula: eps_c_i = temp - (APa0 + APa1*templ1 + APa2*templ2)
    df['eps_c_i'] = df['temp'] - (df['APa0'] + df['APa1'] * df['templ1'] + df['APa2'] * df['templ2'])
    
    # Compute betas using rolling statistics (asrol equivalents)
    print("Computing rolling statistics for beta calculations...")
    
    def asrol_calendar_efficient(group, column, stat='mean', window_months=60, min_periods=24):
        """Efficient calendar-based rolling using pandas reindexing"""
        group = group.sort_values('time_avail_m')
        
        # Create complete monthly index for this group's date range
        if len(group) == 0:
            return pd.Series(np.nan, index=group.index)
            
        start_date = group['time_avail_m'].min()
        end_date = group['time_avail_m'].max()
        
        # Create complete monthly range
        complete_range = pd.date_range(start_date, end_date, freq='MS')
        
        # Reindex to complete monthly grid (fills gaps with NaN)
        temp_series = group.set_index('time_avail_m')[column].reindex(complete_range)
        
        # Apply rolling operation on complete grid
        if stat == 'mean':
            rolled = temp_series.rolling(window=window_months, min_periods=min_periods).mean()
        elif stat == 'std':
            rolled = temp_series.rolling(window=window_months, min_periods=min_periods).std()
        else:
            raise ValueError(f"Unsupported stat: {stat}")
        
        # Map back to original index
        result_dict = rolled.to_dict()
        result = group['time_avail_m'].map(result_dict).fillna(np.nan)
        
        return result
    
    # Sort for rolling operations
    df = df.sort_values(['permno', 'time_avail_m'])
    
    # Use efficient calendar-based rolling (matching Stata asrol window(time_avail_m 60))
    print("Computing efficient calendar-based rolling statistics...")
    df['mean60_ret'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'ret', 'mean')).values
    df['mean60_eps_r_M'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'eps_r_M', 'mean')).values
    df['mean60_eps_c_i'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'eps_c_i', 'mean')).values
    df['mean60_eps_c_M'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'eps_c_M', 'mean')).values
    
    # Use efficient calendar-based rolling std for variance (matching Stata)
    df['tempEpsDiff'] = df['eps_r_M'] - df['eps_c_M']
    df['sd60_tempEpsDiff'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'tempEpsDiff', 'std')).values
    df['sd60_tempEpsDiff'] = df['sd60_tempEpsDiff'] ** 2  # Square for variance
    
    ########################CHECKPOINT 5##################################
    #%%
    #stata_df = pd.read_stata("../../pyData/Debug/checkpoint5.dta")
    stata_df.head()
    #%%
    stata_df = stata_df[['permno', 'time_avail_m', 'ret', 'mean60_ret', 'eps_r_M', 'mean60_eps_r_M', 'eps_c_i', 'mean60_eps_c_i', 'eps_c_M', 'mean60_eps_c_M', 'sd60_tempEpsDiff']]
    id_cols = [c for c in ['permno', 'date', 'time_avail_m'] if c in stata_df.columns]
    stata_df_long = (
        stata_df.melt(id_vars=id_cols, var_name='variable', value_name='value')
                .sort_values(id_cols + ['variable'])
                .reset_index(drop=True)
    )
    stata_df_long.head()

    stata_df_long = stata_df_long = stata_df_long[(stata_df_long["permno"] == 93436) &
                    (stata_df_long["time_avail_m"] > pd.Timestamp("2015-01-01"))].copy()
    stata_df_long.rename(columns={'value': 'stata'}, inplace=True)
    stata_df_long
    #%%
    #%%

    #%%
    python_df = df[['permno', 'time_avail_m', 'ret', 'mean60_ret', 'eps_r_M', 'mean60_eps_r_M', 'eps_c_i', 'mean60_eps_c_i', 'eps_c_M', 'mean60_eps_c_M', 'sd60_tempEpsDiff']]
    id_cols = [c for c in ['permno', 'date', 'time_avail_m'] if c in python_df.columns]
    python_df_long = (
        python_df.melt(id_vars=id_cols, var_name='variable', value_name='value')
                .sort_values(id_cols + ['variable'])
                .reset_index(drop=True)
    )
    python_df_long = python_df_long = python_df_long[(python_df_long["permno"] == 93436) &
                    (python_df_long["time_avail_m"] > pd.Timestamp("2015-01-01"))].copy()
    python_df_long.rename(columns={'value': 'python'}, inplace=True)
    python_df_long
    #%%
    both = stata_df_long.merge(python_df_long, on=['permno', 'time_avail_m', 'variable'], how='outer')
    both['diff'] = both['stata'] - both['python']
    both
    #%%
    ####################################################################

    # Compute covariance terms
    df['tempRR'] = (df['ret'] - df['mean60_ret']) * (df['eps_r_M'] - df['mean60_eps_r_M'])
    df['tempCC'] = (df['eps_c_i'] - df['mean60_eps_c_i']) * (df['eps_c_M'] - df['mean60_eps_c_M'])
    df['tempRC'] = (df['ret'] - df['mean60_ret']) * (df['eps_c_M'] - df['mean60_eps_c_M'])
    df['tempCR'] = (df['eps_c_i'] - df['mean60_eps_c_i']) * (df['eps_r_M'] - df['mean60_eps_r_M'])
    
    # Efficient calendar-based rolling means of covariance terms
    df['mean60_tempRR'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'tempRR', 'mean')).values
    df['mean60_tempCC'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'tempCC', 'mean')).values
    df['mean60_tempRC'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'tempRC', 'mean')).values
    df['mean60_tempCR'] = df.groupby('permno').apply(lambda group: asrol_calendar_efficient(group, 'tempCR', 'mean')).values
    
    # Calculate final betas
    print("Computing final beta measures...")
    df['betaRR'] = df['mean60_tempRR'] / df['sd60_tempEpsDiff']
    df['betaCC'] = df['mean60_tempCC'] / df['sd60_tempEpsDiff']
    df['betaRC'] = df['mean60_tempRC'] / df['sd60_tempEpsDiff']
    df['betaCR'] = df['mean60_tempCR'] / df['sd60_tempEpsDiff']
    df['betaNet'] = df['betaRR'] + df['betaCC'] - df['betaRC'] - df['betaCR']
    
    # Apply price filter as in Stata
    for var in ['betaRR', 'betaCC', 'betaRC', 'betaCR', 'betaNet']:
        df.loc[df['prc'].abs() > 1000, var] = np.nan
    
    ########################CHECKPOINT 7##################################
    #%%
    stata_df = pd.read_stata("../../pyData/Debug/checkpoint7.dta")
    stata_df = stata_df[['permno', 'time_avail_m', 'betaRR']]
    stata_df = stata_df = stata_df[(stata_df["permno"] == 93436) &
                    (stata_df["time_avail_m"] > pd.Timestamp("2015-01-01"))].copy()
    stata_df.rename(columns={'betaRR': 'stata'}, inplace=True)
    #%%
    python_df = df[['permno', 'time_avail_m', 'betaRR']]
    python_df = python_df[['permno', 'time_avail_m', 'betaRR']]
    python_df = python_df = python_df[(python_df["permno"] == 93436) &
                    (python_df["time_avail_m"] > pd.Timestamp("2015-01-01"))].copy()
    python_df.rename(columns={'betaRR': 'python'}, inplace=True)
    #%%
    both = stata_df.merge(python_df, on=['permno', 'time_avail_m'], how='outer')
    both['diff'] = both['stata'] - both['python']
    both
    #%%
    ####################################################################

    # SAVE
    print("Saving placebo signals...")
    save_placebo(df, 'betaRR')
    save_placebo(df, 'betaCC') 
    save_placebo(df, 'betaRC')
    save_placebo(df, 'betaCR')
    save_placebo(df, 'betaNet')
    
    print("ZZ1_betaRR_betaCC_betaRC_betaCR_betaNet.py completed successfully")

if __name__ == "__main__":
    main()
# %%
