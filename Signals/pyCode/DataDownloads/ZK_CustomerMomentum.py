# ABOUTME: Creates customer momentum signals based on Compustat customer segment data
# ABOUTME: Direct Python translation of ZKR_CustomerSegments.R script for exact replication

import pandas as pd
import numpy as np
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def main():
    """
    Direct translation of ZKR_CustomerSegments.R script.
    Creates customer momentum by matching customer names and calculating average returns.
    """
    logger.info("Starting customer momentum processing...")
    
    # Data paths - using relative paths from pyCode directory
    data_path = Path("../Data/Intermediate")
    output_path = Path("../pyData/Intermediate")
    
    # Step 1: Load data exactly like R script (lines 29-37)
    logger.info("Loading input data...")
    
    # Load customer segment data
    seg_customer = pd.read_csv(data_path / "CompustatSegmentDataCustomers.csv")
    seg_customer['datadate'] = pd.to_datetime(seg_customer['datadate'], format='%d%b%Y')
    logger.info(f"Loaded customer segments: {len(seg_customer):,} rows")
    
    # Load CCM linking table
    ccm = pd.read_csv(data_path / "CCMLinkingTable.csv")
    ccm['linkdt'] = pd.to_datetime(ccm['linkdt'], format='%d%b%Y')
    ccm['linkenddt'] = pd.to_datetime(ccm['linkenddt'], format='%d%b%Y', errors='coerce')
    logger.info(f"Loaded CCM linking: {len(ccm):,} rows")
    
    # Load CRSP monthly data
    m_crsp = pd.read_csv(data_path / "mCRSP.csv")
    m_crsp['date'] = pd.to_datetime(m_crsp['date'], format='%d%b%Y')
    logger.info(f"Loaded CRSP monthly: {len(m_crsp):,} rows")
    
    # Step 2: Clean customer data exactly like R script (lines 41-65)
    logger.info("Cleaning customer data...")
    
    seg_customer = seg_customer.copy()
    # Filter for COMPANY type first
    seg_customer = seg_customer[seg_customer['ctype'] == 'COMPANY'].copy()
    # Handle missing values and convert to uppercase
    seg_customer = seg_customer.dropna(subset=['cnms']).copy()
    seg_customer['cnms'] = seg_customer['cnms'].astype(str).str.upper()
    # Remove punctuation (equivalent to R's removePunctuation)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r'[^\w\s]', '', regex=True)
    
    # Filter out specific patterns
    seg_customer = seg_customer[
        (seg_customer['cnms'] != 'NOT REPORTED') & 
        (~seg_customer['cnms'].str.endswith('CUSTOMERS')) & 
        (~seg_customer['cnms'].str.endswith('CUSTOMER'))
    ].copy()
    
    # Apply name transformations in exact R order (lines 48-63)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' INC$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' INC THE$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' CORP$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' LLC$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' PLC$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' LLP$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' LTD$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' CO$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' SA$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' AG$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' AB$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' CO LTD$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r' GROUP$', '', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r'[ ]', '', regex=True)  # Remove all spaces
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r'MTR', 'MOTORS', regex=True)
    seg_customer['cnms'] = seg_customer['cnms'].str.replace(r'MOTOR$', 'MOTORS', regex=True)
    
    # Select only needed columns
    seg_customer = seg_customer[['gvkey', 'datadate', 'cnms']].copy()
    logger.info(f"After cleaning customer data: {len(seg_customer):,} rows")
    
    # Step 3: Clean CCM data exactly like R script (lines 68-87)
    logger.info("Cleaning CCM data...")
    
    ccm0 = ccm.copy()
    # Handle missing values in company names
    ccm0 = ccm0.dropna(subset=['conm']).copy()
    ccm0['conm'] = ccm0['conm'].astype(str).str.upper()
    ccm0['conm'] = ccm0['conm'].str.replace(r'[^\w\s]', '', regex=True)  # Remove punctuation
    
    # Apply same transformations as customer names but to conm
    ccm0['conm'] = ccm0['conm'].str.replace(r' INC$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' INC THE$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' CORP$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' LLC$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' PLC$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' LLP$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' LTD$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' CO$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' SA$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' AG$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' AB$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' CO LTD$', '', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r' GROUP$', '', regex=True)
    # Two-step space removal like R (lines 83-84)
    ccm0['conm'] = ccm0['conm'].str.replace(r' ', '', regex=True)  # First remove single spaces
    ccm0['conm'] = ccm0['conm'].str.replace(r'[ ]', '', regex=True)  # Then remove all spaces
    ccm0['conm'] = ccm0['conm'].str.replace(r'MTR', 'MOTORS', regex=True)
    ccm0['conm'] = ccm0['conm'].str.replace(r'MOTOR$', 'MOTORS', regex=True)
    
    logger.info(f"Cleaned CCM data: {len(ccm0):,} rows")
    
    # Step 4: Add permno data (lines 92-106)
    logger.info("Adding permno data...")
    
    # Inner join to add firm permno (R line 93)
    seg_customer2 = seg_customer.merge(ccm0, on='gvkey', how='inner')
    logger.info(f"After inner join with CCM: {len(seg_customer2):,} rows")
    
    # Filter by date ranges (R line 94)
    date_filter = (
        (seg_customer2['datadate'] >= seg_customer2['linkdt']) &
        (seg_customer2['datadate'] <= seg_customer2['linkenddt'].fillna(pd.Timestamp('2030-12-31')))
    )
    seg_customer2 = seg_customer2[date_filter].copy()
    logger.info(f"After date filtering: {len(seg_customer2):,} rows")
    
    # Select and rename columns (R lines 95-96)
    seg_customer2 = seg_customer2[['gvkey', 'cnms', 'datadate', 'lpermno']].copy()
    seg_customer2 = seg_customer2.rename(columns={'lpermno': 'permno'})
    
    # Add customer permno by name matching (R lines 98-100)
    ccm_customers = ccm0[['conm', 'lpermno', 'linkdt', 'linkenddt']].copy()
    ccm_customers = ccm_customers.rename(columns={
        'lpermno': 'cust_permno',
        'linkdt': 'linkdt_cust',
        'linkenddt': 'linkenddt_cust'
    })
    
    # Left join by customer name (cnms = conm)
    seg_customer2 = seg_customer2.merge(
        ccm_customers, left_on='cnms', right_on='conm', how='left'
    )
    logger.info(f"After customer name matching: {len(seg_customer2):,} rows")
    
    # Filter for valid customer matches and date ranges (R lines 101-102)
    customer_filter = (
        seg_customer2['cust_permno'].notna() &
        (seg_customer2['datadate'] >= seg_customer2['linkdt_cust']) &
        (seg_customer2['datadate'] <= seg_customer2['linkenddt_cust'].fillna(pd.Timestamp('2030-12-31')))
    )
    seg_customer2 = seg_customer2[customer_filter].copy()
    logger.info(f"After customer filtering: {len(seg_customer2):,} rows")
    
    # Select final columns and arrange (R lines 103-104)
    seg_customer2 = seg_customer2[['permno', 'datadate', 'cust_permno']].copy()
    seg_customer2 = seg_customer2.sort_values(['permno', 'datadate'])
    
    # Set day to 28 like R (line 106)
    seg_customer2['datadate'] = seg_customer2['datadate'].dt.to_period('M').dt.to_timestamp() + pd.Timedelta(days=27)
    
    logger.info(f"Final customer-firm relationships: {len(seg_customer2):,} rows")
    
    # Step 5: Create monthly frame (lines 110-115)
    logger.info("Creating monthly frame...")
    
    # Filter CRSP to firms with customer data and create time_avail_m (R lines 110-112)
    unique_permnos = seg_customer2['permno'].unique()
    tempm0 = m_crsp[m_crsp['permno'].isin(unique_permnos)].copy()
    # R: time_avail_m = date %m-% months(1)
    tempm0['time_avail_m'] = tempm0['date'] - pd.DateOffset(months=1)
    tempm0 = tempm0[['permno', 'time_avail_m']].copy()
    
    # Set day to 28 like R (line 115)
    tempm0['time_avail_m'] = tempm0['time_avail_m'].dt.to_period('M').dt.to_timestamp() + pd.Timedelta(days=27)
    
    logger.info(f"Monthly frame: {len(tempm0):,} rows")
    
    # Step 6: Create wide customer data (lines 119-145)
    logger.info("Creating wide customer data...")
    
    # Create wide format with customer numbering (R lines 119-124)
    temp1_prep = seg_customer2.sort_values(['permno', 'datadate', 'cust_permno']).copy()
    temp1_prep['customeri'] = temp1_prep.groupby(['permno', 'datadate']).cumcount() + 1
    
    # Pivot to wide format (R spread function)
    temp1 = temp1_prep.pivot_table(
        index=['permno', 'datadate'],
        columns='customeri',
        values='cust_permno',
        fill_value=np.nan
    ).reset_index()
    
    # Replace NA with -1 like R (line 126)
    customer_cols = [col for col in temp1.columns if isinstance(col, int)]
    for col in customer_cols:
        temp1[col] = temp1[col].fillna(-1)
    
    # Rename customer columns to match R naming
    rename_dict = {col: f'customer{col}' for col in customer_cols}
    temp1 = temp1.rename(columns=rename_dict)
    customer_cols = [f'customer{col}' for col in customer_cols]
    
    logger.info(f"Wide format data: {len(temp1):,} rows, {len(customer_cols)} customer columns")
    
    # Create stop rows to avoid stale data (R lines 131-145)
    temp1b = temp1.sort_values(['permno', 'datadate']).copy()
    temp1b['next_permno'] = temp1b['permno'].shift(-1)
    temp1b['next_year'] = temp1b['datadate'].shift(-1).dt.year
    temp1b['current_year'] = temp1b['datadate'].dt.year
    
    # R logic: lastentry = (diffpermno>0) & (dyear != 1)
    temp1b['diffpermno'] = temp1b['next_permno'] - temp1b['permno']
    temp1b['dyear'] = temp1b['next_year'] - temp1b['current_year']
    temp1b['lastentry'] = (temp1b['diffpermno'] > 0) & (temp1b['dyear'] != 1)
    
    # Handle last rows (no next permno)
    temp1b.loc[temp1b['next_permno'].isna(), 'lastentry'] = True
    
    # Create stop rows (R lines 138-142)
    tempstop = temp1b[temp1b['lastentry']].copy()
    if len(tempstop) > 0:
        # Add one year to datadate
        tempstop['datadate'] = tempstop['datadate'] + pd.DateOffset(years=1)
        
        # Set all customer columns to -1
        for col in customer_cols:
            if col in tempstop.columns:
                tempstop[col] = -1
        
        # Select only needed columns
        tempstop = tempstop[['permno', 'datadate'] + [c for c in customer_cols if c in tempstop.columns]].copy()
        
        # Combine original and stop rows (R lines 144-145)
        temp1c = pd.concat([
            temp1[['permno', 'datadate'] + [c for c in customer_cols if c in temp1.columns]],
            tempstop
        ], ignore_index=True).sort_values(['permno', 'datadate'])
    else:
        temp1c = temp1[['permno', 'datadate'] + [c for c in customer_cols if c in temp1.columns]].copy()
    
    logger.info(f"Wide customer data with stop rows: {len(temp1c):,} rows")
    
    # Step 7: Merge and fill customer data (lines 148-164)
    logger.info("Merging and filling customer data...")
    
    # Add time_avail_m to customer data (R lines 149-150)
    temp1c_with_time = temp1c.copy()
    # R: time_avail_m = datadate %m+% months(6)
    temp1c_with_time['time_avail_m'] = temp1c_with_time['datadate'] + pd.DateOffset(months=6)
    temp1c_with_time['time_avail_m'] = temp1c_with_time['time_avail_m'].dt.to_period('M').dt.to_timestamp() + pd.Timedelta(days=27)
    
    # Merge with monthly frame (R lines 148-154)
    tempm1 = tempm0.merge(
        temp1c_with_time.drop(columns=['datadate']),
        on=['permno', 'time_avail_m'],
        how='left'
    )
    
    # Forward fill customer data (R lines 157-160)
    # R: fill(-permno,-time_avail_m) fills all columns except permno and time_avail_m
    customer_cols_in_data = [col for col in customer_cols if col in tempm1.columns]
    tempm1 = tempm1.sort_values(['permno', 'time_avail_m'])
    tempm1[customer_cols_in_data] = tempm1.groupby('permno')[customer_cols_in_data].ffill()
    
    # Convert back to long format (R lines 162-164)
    seg_customer3 = tempm1.melt(
        id_vars=['permno', 'time_avail_m'],
        value_vars=customer_cols_in_data,
        var_name='customeri',
        value_name='cust_permno'
    )
    
    # Filter out NA and -1 values
    seg_customer3 = seg_customer3[
        (seg_customer3['cust_permno'].notna()) & 
        (seg_customer3['cust_permno'] > 0)
    ][['permno', 'time_avail_m', 'cust_permno']].copy()
    
    logger.info(f"Long customer data after fill: {len(seg_customer3):,} rows")
    
    # Step 8: Calculate customer momentum (lines 168-183)
    logger.info("Calculating customer momentum...")
    
    # Get customer returns (R lines 168-174)
    unique_cust_permnos = seg_customer3['cust_permno'].unique()
    tempc = m_crsp[m_crsp['permno'].isin(unique_cust_permnos)].copy()
    # R: time_avail_m = date (no lag for returns)
    tempc['time_avail_m'] = tempc['date']
    tempc['cust_permno'] = tempc['permno']
    tempc['cust_ret'] = tempc['ret']
    
    # Set day to 28 (R line 176)
    tempc['time_avail_m'] = tempc['time_avail_m'].dt.to_period('M').dt.to_timestamp() + pd.Timedelta(days=27)
    
    tempc = tempc[['cust_permno', 'cust_ret', 'time_avail_m']].copy()
    tempc = tempc.dropna(subset=['cust_ret'])
    
    logger.info(f"Customer returns: {len(tempc):,} rows")
    
    # Merge and calculate average customer returns (R lines 178-183)
    customerMom = seg_customer3.merge(
        tempc,
        on=['time_avail_m', 'cust_permno'],
        how='left'
    )
    
    customerMom = customerMom.dropna(subset=['cust_ret'])
    logger.info(f"After merging customer returns: {len(customerMom):,} rows")
    
    # Calculate mean customer return by firm-month (R line 182)
    # R: summarize(CustMom = mean(cust_ret))
    customerMom = (customerMom
        .groupby(['time_avail_m', 'permno'])['cust_ret']
        .mean()
        .reset_index()
        .rename(columns={'cust_ret': 'custmom'})  # Match Stata output name
    )
    
    # Convert time_avail_m to first day of month to match Stata output format
    # The Stata script converts the R output using mofd() which sets day to 1
    customerMom['time_avail_m'] = customerMom['time_avail_m'].dt.to_period('M').dt.to_timestamp()
    
    logger.info(f"Final customer momentum: {len(customerMom):,} rows")
    
    # Step 9: Reorder columns to match Stata output and save
    customerMom = customerMom[['permno', 'custmom', 'time_avail_m']].copy()
    
    output_file = output_path / "customerMom.parquet"
    customerMom.to_parquet(output_file, index=False)
    
    logger.info(f"Successfully saved {len(customerMom):,} rows to {output_file}")
    logger.info("Customer momentum processing completed!")
    
    return customerMom


if __name__ == "__main__":
    main()