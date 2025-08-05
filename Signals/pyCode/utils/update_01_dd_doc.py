#!/usr/bin/env python3
"""
ABOUTME: Generates documentation for Python DataDownloads scripts
ABOUTME: Creates 01_Python_DataDownloadsDoc.md by analyzing Python scripts and output files

This script automatically generates documentation for Python DataDownloads scripts
by analyzing the scripts themselves and their output parquet files.

Usage: python3 utils/update_01_dd_doc.py
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import pyarrow.parquet as pq
from datetime import datetime

# Hard-coded dataset identifiers extracted from validate_by_keys.py
DATASET_IDENTIFIERS = {
    # CCM Linking Tables
    'CCMLinkingTable.csv': {
        'stock': 'lpermno', 
        'time': 'linkdt',
        'stata_file': 'CCMLinkingTable.csv',
        'python_file': 'CCMLinkingTable.csv'
    },
    'CCMLinkingTable': {
        'stock': 'gvkey', 
        'time': 'timeLinkStart_d',
        'stata_file': 'CCMLinkingTable.dta',
        'python_file': 'CCMLinkingTable.parquet'
    },
    
    # Compustat Annual/Quarterly
    'CompustatAnnual': {
        'stock': 'gvkey', 
        'time': 'datadate',
        'stata_file': 'CompustatAnnual.csv',
        'python_file': 'CompustatAnnual.csv'
    },
    'a_aCompustat': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'a_aCompustat.dta',
        'python_file': 'a_aCompustat.parquet'
    },
    'm_aCompustat': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'm_aCompustat.dta',
        'python_file': 'm_aCompustat.parquet'
    },
    'm_QCompustat': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'm_QCompustat.dta',
        'python_file': 'm_QCompustat.parquet'
    },
    
    # Compustat Specialized
    'CompustatPensions': {
        'stock': 'gvkey', 
        'time': 'year',
        'stata_file': 'CompustatPensions.dta',
        'python_file': 'CompustatPensions.parquet'
    },
    'CompustatSegments': {
        'stock': 'gvkey', 
        'time': 'datadate',
        'stata_file': 'CompustatSegments.dta',
        'python_file': 'CompustatSegments.parquet'
    },
    'CompustatSegmentDataCustomers': {
        'stock': 'gvkey', 
        'time': 'datadate',
        'stata_file': 'CompustatSegmentDataCustomers.csv',
        'python_file': 'CompustatSegmentDataCustomers.csv'
    },
    'monthlyShortInterest': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'monthlyShortInterest.dta',
        'python_file': 'monthlyShortInterest.parquet'
    },
    
    # CRSP Data
    'CRSPdistributions': {
        'stock': 'permno', 
        'time': 'exdt',
        'stata_file': 'CRSPdistributions.dta',
        'python_file': 'CRSPdistributions.parquet'
    },
    'mCRSP': {
        'stock': 'permno', 
        'time': 'date',
        'stata_file': 'mCRSP.csv',
        'python_file': 'mCRSP.csv'
    },
    'monthlyCRSP': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'monthlyCRSP.dta',
        'python_file': 'monthlyCRSP.parquet'
    },
    'monthlyCRSPraw': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'monthlyCRSPraw.dta',
        'python_file': 'monthlyCRSPraw.parquet'
    },
    'dailyCRSP': {
        'stock': 'permno', 
        'time': 'time_d',
        'stata_file': 'dailyCRSP.dta',
        'python_file': 'dailyCRSP.parquet'
    },
    'dailyCRSPprc': {
        'stock': 'permno', 
        'time': 'time_d',
        'stata_file': 'dailyCRSPprc.dta',
        'python_file': 'dailyCRSPprc.parquet'
    },
    'm_CRSPAcquisitions': {
        'stock': 'permno', 
        'time': None,
        'stata_file': 'm_CRSPAcquisitions.dta',
        'python_file': 'm_CRSPAcquisitions.parquet'
    },
    
    # IBES Data
    'IBES_EPS_Unadj': {
        'stock': 'tickerIBES', 
        'time': 'time_avail_m',
        'stata_file': 'IBES_EPS_Unadj.dta',
        'python_file': 'IBES_EPS_Unadj.parquet'
    },
    'IBES_EPS_Adj': {
        'stock': 'tickerIBES', 
        'time': 'time_avail_m',
        'stata_file': 'IBES_EPS_Adj.dta',
        'python_file': 'IBES_EPS_Adj.parquet'
    },
    'IBES_Recommendations': {
        'stock': 'tickerIBES', 
        'time': 'time_avail_m',
        'stata_file': 'IBES_Recommendations.dta',
        'python_file': 'IBES_Recommendations.parquet'
    },
    'IBES_UnadjustedActuals': {
        'stock': 'tickerIBES', 
        'time': 'time_avail_m',
        'stata_file': 'IBES_UnadjustedActuals.dta',
        'python_file': 'IBES_UnadjustedActuals.parquet'
    },
    
    # Market-Level Data (no stock identifier)
    'dailyFF': {
        'stock': None, 
        'time': 'time_d',
        'stata_file': 'dailyFF.dta',
        'python_file': 'dailyFF.parquet'
    },
    'monthlyFF': {
        'stock': None, 
        'time': 'time_avail_m',
        'stata_file': 'monthlyFF.dta',
        'python_file': 'monthlyFF.parquet'
    },
    'monthlyMarket': {
        'stock': None, 
        'time': 'time_avail_m',
        'stata_file': 'monthlyMarket.dta',
        'python_file': 'monthlyMarket.parquet'
    },
    'monthlyLiquidity': {
        'stock': None, 
        'time': 'time_avail_m',
        'stata_file': 'monthlyLiquidity.dta',
        'python_file': 'monthlyLiquidity.parquet'
    },
    'd_qfactor': {
        'stock': None, 
        'time': 'time_d',
        'stata_file': 'd_qfactor.dta',
        'python_file': 'd_qfactor.parquet'
    },
    'd_vix': {
        'stock': None, 
        'time': 'time_d',
        'stata_file': 'd_vix.dta',
        'python_file': 'd_vix.parquet'
    },
    'GNPdefl': {
        'stock': None, 
        'time': 'time_avail_m',
        'stata_file': 'GNPdefl.dta',
        'python_file': 'GNPdefl.parquet'
    },
    'TBill3M': {
        'stock': None, 
        'time': ['qtr', 'year'],
        'stata_file': 'TBill3M.dta',
        'python_file': 'TBill3M.parquet'
    },
    'brokerLev': {
        'stock': None, 
        'time': ['qtr', 'year'],
        'stata_file': 'brokerLev.dta',
        'python_file': 'brokerLev.parquet'
    },
    
    # Credit Ratings
    'm_SP_creditratings': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'm_SP_creditratings.dta',
        'python_file': 'm_SP_creditratings.parquet'
    },
    'm_CIQ_creditratings': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'm_CIQ_creditratings.dta',
        'python_file': 'm_CIQ_creditratings.parquet'
    },
    
    # Other Specialized Data
    'IPODates': {
        'stock': 'ticker', 
        'time': None,
        'stata_file': 'IPODates.dta',
        'python_file': 'IPODates.parquet'
    },
    'pin_monthly': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'pin_monthly.dta',
        'python_file': 'pin_monthly.parquet'
    },
    'GovIndex': {
        'stock': 'ticker', 
        'time': 'time_avail_m',
        'stata_file': 'GovIndex.dta',
        'python_file': 'GovIndex.parquet'
    },
    'BAspreadsCorwin': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'BAspreadsCorwin.dta',
        'python_file': 'BAspreadsCorwin.parquet'
    },
    'TR_13F': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'TR_13F.dta',
        'python_file': 'TR_13F.parquet'
    },
    'hf_spread': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'hf_spread.dta',
        'python_file': 'hf_spread.parquet'
    },
    
    # OptionMetrics Data
    'OptionMetricsVolume': {
        'stock': 'secid', 
        'time': 'time_avail_m',
        'stata_file': 'OptionMetricsVolume.dta',
        'python_file': 'OptionMetricsVolume.parquet'
    },
    'OptionMetricsVolSurf': {
        'stock': 'secid', 
        'time': 'time_avail_m',
        'stata_file': 'OptionMetricsVolSurf.dta',
        'python_file': 'OptionMetricsVolSurf.parquet'
    },
    'OptionMetricsXZZ': {
        'stock': 'secid', 
        'time': 'time_avail_m',
        'stata_file': 'OptionMetricsXZZ.dta',
        'python_file': 'OptionMetricsXZZ.parquet'
    },
    'OptionMetricsBH': {
        'stock': 'secid', 
        'time': 'time_avail_m',
        'stata_file': 'OptionMetricsBH.dta',
        'python_file': 'OptionMetricsBH.parquet'
    },
    
    # Linking Tables (no time filtering needed)
    'IBESCRSPLinkingTable': {
        'stock': 'permno', 
        'time': None,
        'stata_file': 'IBESCRSPLinkingTable.dta',
        'python_file': 'IBESCRSPLinkingTable.parquet'
    },
    'OPTIONMETRICSCRSPLinkingTable': {
        'stock': 'permno', 
        'time': None,
        'stata_file': 'OPTIONMETRICSCRSPLinkingTable.dta',
        'python_file': 'OPTIONMETRICSCRSPLinkingTable.parquet'
    },
    
    # Patent Data
    'PatentDataProcessed': {
        'stock': 'gvkey', 
        'time': 'year',
        'stata_file': 'PatentDataProcessed.dta',
        'python_file': 'PatentDataProcessed.parquet'
    },
    
    # Input-Output Momentum Data
    'InputOutputMomentumProcessed': {
        'stock': 'gvkey', 
        'time': 'time_avail_m',
        'stata_file': 'InputOutputMomentumProcessed.dta',
        'python_file': 'InputOutputMomentumProcessed.parquet'
    },
    
    # Customer Momentum Data
    'customerMom': {
        'stock': 'permno', 
        'time': 'time_avail_m',
        'stata_file': 'customerMom.dta',
        'python_file': 'customerMom.parquet'
    }
}

# Hard-coded mapping of Python scripts to their output files
SCRIPT_OUTPUT_MAPPING = {
    'A_CCMLinkingTable.py': ['CCMLinkingTable.csv', 'CCMLinkingTable.parquet'],
    'B_CompustatAnnual.py': ['CompustatAnnual.csv', 'CompustatAnnual.parquet', 'a_aCompustat.parquet', 'm_aCompustat.parquet'],
    'C_CompustatQuarterly.py': ['m_QCompustat.parquet', 'CompustatQuarterly.parquet'],
    'D_CompustatPensions.py': ['CompustatPensions.parquet'],
    'E_CompustatBusinessSegments.py': ['CompustatSegments.parquet'],
    'F_CompustatCustomerSegments.py': ['CompustatSegmentDataCustomers.csv'],
    'G_CompustatShortInterest.py': ['monthlyShortInterest.parquet'],
    'H_CRSPDistributions.py': ['CRSPdistributions.parquet'],
    'I_CRSPmonthly.py': ['mCRSP.csv', 'monthlyCRSP.parquet'],
    'I2_CRSPmonthlyraw.py': ['monthlyCRSPraw.parquet'],
    'J_CRSPdaily.py': ['dailyCRSP.parquet', 'dailyCRSPprc.parquet'],
    'K_CRSPAcquisitions.py': ['m_CRSPAcquisitions.parquet'],
    'L_IBES_EPS_Unadj.py': ['IBES_EPS_Unadj.parquet'],
    'L2_IBES_EPS_Adj.py': ['IBES_EPS_Adj.parquet'],
    'M_IBES_Recommendations.py': ['IBES_Recommendations.parquet'],
    'N_IBES_UnadjustedActuals.py': ['IBES_UnadjustedActuals.parquet'],
    'O_Daily_Fama-French.py': ['dailyFF.parquet'],
    'P_Monthly_Fama-French.py': ['monthlyFF.parquet'],
    'Q_MarketReturns.py': ['monthlyMarket.parquet'],
    'R_MonthlyLiquidityFactor.py': ['monthlyLiquidity.parquet'],
    'S_QFactorModel.py': ['d_qfactor.parquet'],
    'T_VIX.py': ['d_vix.parquet'],
    'U_GNPDeflator.py': ['GNPdefl.parquet'],
    'V_TBill3M.py': ['TBill3M.parquet'],
    'W_BrokerDealerLeverage.py': ['brokerLev.parquet'],
    'X_SPCreditRatings.py': ['m_SP_creditratings.parquet'],
    'X2_CIQCreditRatings.py': ['m_CIQ_creditratings.parquet'],
    'ZA_IPODates.py': ['IPODates.parquet'],
    'ZB_PIN.py': ['pin_monthly.parquet'],
    'ZC_GovernanceIndex.py': ['GovIndex.parquet'],
    'ZD_CorwinSchultz.py': ['BAspreadsCorwin.parquet'],
    'ZE_13F.py': ['TR_13F.parquet'],
    'ZF_CRSPIBESLink.py': ['IBESCRSPLinkingTable.parquet'],
    'ZG_BidaskTAQ.py': ['hf_spread.parquet'],
    'ZH_OptionMetrics.py': ['OptionMetricsVolume.parquet', 'OptionMetricsVolSurf.parquet', 'OptionMetricsXZZ.parquet', 'OptionMetricsBH.parquet'],
    'ZI_PatentCitations.py': ['PatentDataProcessed.parquet'],
    'ZJ_InputOutputMomentum.py': ['InputOutputMomentumProcessed.parquet'],
    'ZK_CustomerMomentum.py': ['customerMom.parquet'],
    'ZL_CRSPOPTIONMETRICS.py': ['OPTIONMETRICSCRSPLinkingTable.parquet']
}


def scan_python_scripts() -> List[Path]:
    """Find all Python scripts in DataDownloads directory."""
    downloads_dir = Path("DataDownloads")
    if not downloads_dir.exists():
        raise FileNotFoundError("DataDownloads directory not found")
    
    scripts = []
    for file_path in downloads_dir.glob("*.py"):
        if not file_path.name.startswith("__"):
            scripts.append(file_path)
    
    return sorted(scripts)


def extract_script_metadata(script_path: Path) -> Dict[str, Any]:
    """Extract metadata from a Python script."""
    metadata = {
        'name': script_path.name,
        'description': '',
        'output_files': [],
        'stata_equivalent': script_path.stem.replace('_', ' ').title()
    }
    
    # Use hard-coded mapping for output files
    script_name = script_path.name
    if script_name in SCRIPT_OUTPUT_MAPPING:
        metadata['output_files'] = SCRIPT_OUTPUT_MAPPING[script_name].copy()
    
    try:
        with open(script_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract docstring description
        tree = ast.parse(content)
        if (tree.body and isinstance(tree.body[0], ast.Expr)):
            value = tree.body[0].value
            docstring = None
            
            # Handle both old ast.Str and new ast.Constant
            if hasattr(value, 's'):  # Old ast.Str
                docstring = value.s
            elif isinstance(value, ast.Constant) and isinstance(value.value, str):
                docstring = value.value
            
            if docstring:
                lines = docstring.strip().split('\n')
                metadata['description'] = lines[0] if lines else ''
    
    except Exception as e:
        print(f"Warning: Could not parse {script_path}: {e}")
    
    return metadata


def analyze_file(file_path: Path) -> Dict[str, Any]:
    """Analyze a parquet or CSV file and return metadata."""
    try:
        # Get file size
        file_size = file_path.stat().st_size
        
        if file_path.suffix.lower() == '.parquet':
            # Parquet file analysis
            parquet_file = pq.ParquetFile(file_path)
            schema = parquet_file.schema_arrow
            row_count = parquet_file.metadata.num_rows
            
            # Get column info
            columns = []
            for field in schema:
                col_info = {
                    'name': field.name,
                    'type': str(field.type)
                }
                columns.append(col_info)
            
            # Load small sample for sample data
            df_sample = pd.read_parquet(file_path).head(5)
            
        elif file_path.suffix.lower() == '.csv':
            # CSV file analysis
            df_sample = pd.read_csv(file_path, nrows=5)
            df_full = pd.read_csv(file_path, nrows=1000)  # Sample for row count
            row_count = len(df_full)
            
            # Get column info
            columns = []
            for col in df_full.columns:
                col_info = {
                    'name': col,
                    'type': str(df_full[col].dtype)
                }
                columns.append(col_info)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")
        
        # Process sample data
        sample_data = []
        for i, row in df_sample.iterrows():
            row_dict = {}
            for col in df_sample.columns[:10]:  # Limit to first 10 columns
                val = row[col]
                if pd.isna(val):
                    row_dict[col] = 'NA'
                elif isinstance(val, (int, float)):
                    if isinstance(val, float) and abs(val) >= 1000:
                        row_dict[col] = f"{val:.2e}"
                    else:
                        row_dict[col] = str(val)
                else:
                    row_dict[col] = str(val)[:20]  # Truncate long strings
            sample_data.append(row_dict)
        
        return {
            'size_bytes': file_size,
            'size_mb': file_size / (1024 * 1024),
            'rows': row_count,
            'columns': len(columns),
            'column_info': columns,
            'sample_data': sample_data
        }
    
    except Exception as e:
        return {
            'error': str(e),
            'size_bytes': 0,
            'size_mb': 0,
            'rows': 0,
            'columns': 0,
            'column_info': [],
            'sample_data': []
        }


def get_identifiers_for_file(filename: str) -> Tuple[Optional[str], Any]:
    """Get stock and time identifiers for a file."""
    # Remove extension for lookup
    base_name = filename.replace('.parquet', '').replace('.csv', '')
    
    if base_name in DATASET_IDENTIFIERS:
        config = DATASET_IDENTIFIERS[base_name]
        return config.get('stock'), config.get('time')
    
    # Try exact filename match
    if filename in DATASET_IDENTIFIERS:
        config = DATASET_IDENTIFIERS[filename]
        return config.get('stock'), config.get('time')
    
    return None, None


def format_sample_data(sample_data: List[Dict], max_cols: int = 6) -> str:
    """Format sample data for markdown display."""
    if not sample_data:
        return "No sample data available"
    
    # Get column names (limit to max_cols)
    all_cols = list(sample_data[0].keys())
    display_cols = all_cols[:max_cols]
    if len(all_cols) > max_cols:
        display_cols.append('...')
    
    # Create header
    header_parts = []
    for col in display_cols:
        if col == '...':
            header_parts.append(col)
        else:
            header_parts.append(f"{col} <chr>")
    
    lines = ['```']
    lines.append('  ' + ' '.join(f"{i+1:>2}" for i in range(len(display_cols))))
    lines.append('  ' + ' '.join(header_parts))
    
    # Add sample rows
    for i, row in enumerate(sample_data[:4]):
        row_parts = []
        for col in display_cols:
            if col == '...':
                row_parts.append('...')
            else:
                val = str(row.get(col, 'NA'))
                row_parts.append(val[:12])  # Truncate for display
        lines.append(f"{i+1} " + ' '.join(f"{part:>12}" for part in row_parts))
    
    lines.append('```')
    lines.append(f"... with {max(0, len(sample_data) - 4)} more rows")
    
    return '\n'.join(lines)


def generate_markdown() -> str:
    """Generate the complete markdown documentation."""
    scripts = scan_python_scripts()
    
    # Header
    md_lines = [
        "# Python DataDownloads Script Documentation",
        "",
        f"*Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
        "",
        "This document provides comprehensive documentation of Python scripts in the DataDownloads directory and their output files.",
        ""
    ]
    
    # Process each script
    script_counter = 1
    for script_path in scripts:
        print(f"Processing {script_path.name}...")
        
        metadata = extract_script_metadata(script_path)
        
        # Script header
        md_lines.extend([
            f"## {metadata['name']}",
            "",
            metadata['description'],
            ""
        ])
        
        # Process output files
        output_counter = 1
        pydata_dir = Path("../pyData/Intermediate")
        
        for output_file in metadata['output_files']:
            file_path = pydata_dir / output_file
            
            md_lines.extend([
                f"### {output_counter}. {output_file}",
                ""
            ])
            
            if file_path.exists():
                file_info = analyze_file(file_path)
                
                if 'error' not in file_info:
                    # File statistics
                    md_lines.extend([
                        f"Size: {file_info['size_mb']:.2f} MB",
                        f"Rows: {file_info['rows']:,}",
                        f"Columns: {file_info['columns']}",
                        ""
                    ])
                    
                    # Column information
                    if file_info['column_info']:
                        md_lines.append("All Columns:")
                        col_chunks = []
                        for i in range(0, len(file_info['column_info']), 3):
                            chunk = file_info['column_info'][i:i+3]
                            chunk_strs = []
                            for j, col in enumerate(chunk):
                                chunk_strs.append(f"{i+j+1:>2}. {col['name']} <{col['type']}>")
                            col_chunks.append('  ' + ' '.join(f"{s:<25}" for s in chunk_strs))
                        
                        md_lines.extend(col_chunks)
                        md_lines.append("")
                    
                    # Sample data
                    md_lines.extend([
                        "Sample Data:",
                        format_sample_data(file_info['sample_data']),
                        ""
                    ])
                    
                    # Identifiers
                    stock_id, time_id = get_identifiers_for_file(output_file)
                    md_lines.append("IDENTIFIERS:")
                    if stock_id:
                        md_lines.append(f"- stock: {stock_id}")
                    else:
                        md_lines.append("- stock: None")
                    
                    if time_id:
                        if isinstance(time_id, list):
                            md_lines.append(f"- time: {' + '.join(time_id)}")
                        else:
                            md_lines.append(f"- time: {time_id}")
                    else:
                        md_lines.append("- time: None")
                    
                else:
                    md_lines.extend([
                        f"*Error analyzing file: {file_info['error']}*",
                        ""
                    ])
            else:
                md_lines.extend([
                    "*File not found in pyData/Intermediate/ directory*",
                    ""
                ])
            
            output_counter += 1
        
        md_lines.append("")
        script_counter += 1
    
    return '\n'.join(md_lines)


def main():
    """Main function to generate documentation."""
    print("Generating Python DataDownloads documentation...")
    
    try:
        # Change to DataDownloads parent directory if needed
        if Path("DataDownloads").exists():
            os.chdir(".")
        elif Path("../DataDownloads").exists():
            os.chdir("..")
        elif Path("pyCode/DataDownloads").exists():
            os.chdir("pyCode")
        else:
            raise FileNotFoundError("Could not find DataDownloads directory")
        
        # Generate markdown
        markdown_content = generate_markdown()
        
        # Write to file
        output_path = Path("DataDownloads/01_Python_DataDownloadsDoc.md")
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        
        print(f"Documentation generated: {output_path}")
        print(f"File size: {output_path.stat().st_size:,} bytes")
        
    except Exception as e:
        print(f"Error generating documentation: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())