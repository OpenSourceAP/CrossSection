#!/usr/bin/env python3
"""
ABOUTME: Batch validation script for systematically validating DataDownloads script groups
ABOUTME: Enables systematic validation of the 47 Python scripts organized into logical groups

This script provides batch validation functionality for the DataDownloads scripts,
organized into logical groups for systematic validation and fixing.

Usage:
    python3 utils/batch_validate_groups.py --group A  # Validate Group A (CCM & Compustat)
    python3 utils/batch_validate_groups.py --group ALL  # Validate all groups
    python3 utils/batch_validate_groups.py --summary  # Show validation summary
"""

import argparse
import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

# Import the main validation functionality
from validate_by_keys import validate_all_datasets, print_summary_stats, save_reports

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Dataset groups based on our validation plan
DATASET_GROUPS = {
    'A': {
        'name': 'CCM & Compustat Scripts',
        'datasets': [
            'CCMLinkingTable',
            'CCMLinkingTable.csv', 
            'CompustatAnnual',
            'a_aCompustat',
            'm_aCompustat',
            'm_QCompustat',
            'CompustatPensions',
            'CompustatSegments',
            'CompustatSegmentDataCustomers',
            'monthlyShortInterest'
        ],
        'notes': 'B_CompustatAnnual.py and C_CompustatQuarterly.py already fixed'
    },
    'B': {
        'name': 'CRSP Scripts',
        'datasets': [
            'CRSPdistributions',
            'mCRSP',
            'monthlyCRSP',
            'monthlyCRSPraw',
            'dailyCRSP',
            'dailyCRSPprc',
            'm_CRSPAcquisitions'
        ],
        'notes': 'Daily CRSP data is very large - may need special handling'
    },
    'C': {
        'name': 'IBES Scripts',
        'datasets': [
            'IBES_EPS_Unadj',
            'IBES_EPS_Adj',
            'IBES_Recommendations',
            'IBES_UnadjustedActuals'
        ],
        'notes': 'IBES data uses tickerIBES as stock identifier'
    },
    'D': {
        'name': 'Market Data Scripts',
        'datasets': [
            'dailyFF',
            'monthlyFF',
            'monthlyMarket',
            'monthlyLiquidity',
            'd_qfactor',
            'd_vix',
            'GNPdefl',
            'TBill3M'
        ],
        'notes': 'Market-level data (no stock identifiers), W_BrokerDealerLeverage.py already fixed'
    },
    'E': {
        'name': 'Credit & Specialized Scripts',
        'datasets': [
            'brokerLev',  # Already fixed
            'm_SP_creditratings',
            'm_CIQ_creditratings'
        ],
        'notes': 'Credit ratings and broker-dealer leverage data'
    },
    'F': {
        'name': 'Advanced Analytics Scripts',
        'datasets': [
            'IPODates',
            'pin_monthly',
            'GovIndex',
            'BAspreadsCorwin',
            'TR_13F',
            'IBESCRSPLinkingTable',
            'hf_spread',
            'OptionMetricsVolume',
            'OptionMetricsVolSurf',
            'OptionMetricsXZZ',
            'OptionMetricsBH',
            'OPTIONMETRICSCRSPLinkingTable',
            'PatentDataProcessed',
            'InputOutputMomentumProcessed',
            'customerMom'
        ],
        'notes': 'Complex analytics including options, patents, and linking tables'
    }
}


def validate_group(group_id: str, tolerance: float = 1e-6, 
                  output_dir: str = "../Logs") -> Dict[str, Any]:
    """Validate all datasets in a specific group.
    
    Args:
        group_id: Group identifier (A, B, C, D, E, F)
        tolerance: Tolerance for numeric comparisons
        output_dir: Output directory for reports
        
    Returns:
        Dictionary with validation results and summary statistics
    """
    if group_id not in DATASET_GROUPS:
        raise ValueError(f"Invalid group ID: {group_id}. Valid groups: {list(DATASET_GROUPS.keys())}")
    
    group_info = DATASET_GROUPS[group_id]
    datasets = group_info['datasets']
    
    logger.info(f"Starting validation of Group {group_id}: {group_info['name']}")
    logger.info(f"Datasets to validate: {len(datasets)}")
    logger.info(f"Notes: {group_info['notes']}")
    
    # Run validation
    start_time = datetime.now()
    results = validate_all_datasets(datasets, tolerance)
    end_time = datetime.now()
    
    # Generate summary statistics
    total_datasets = len(results)
    perfect_matches = sum(1 for r in results 
                         if r.get('comparison', {}).get('match_status') == 'perfect_match')
    minor_differences = sum(1 for r in results 
                           if r.get('comparison', {}).get('match_status') == 'minor_differences')
    major_differences = sum(1 for r in results 
                           if r.get('comparison', {}).get('match_status') == 'major_differences')
    errors = sum(1 for r in results if r['status'] == 'error')
    
    summary = {
        'group_id': group_id,
        'group_name': group_info['name'],
        'total_datasets': total_datasets,
        'perfect_matches': perfect_matches,
        'minor_differences': minor_differences,
        'major_differences': major_differences,
        'errors': errors,
        'processing_time': (end_time - start_time).total_seconds(),
        'validation_timestamp': datetime.now().isoformat(),
        'tolerance': tolerance,
        'results': results
    }
    
    # Save group-specific reports
    group_output_dir = Path(output_dir) / f"Group_{group_id}"
    group_output_dir.mkdir(parents=True, exist_ok=True)
    
    save_reports(results, str(group_output_dir))
    
    # Save group summary
    summary_file = group_output_dir / "group_summary.json"
    with open(summary_file, 'w') as f:
        # Create a copy without the full results for the summary JSON
        summary_for_json = summary.copy()
        summary_for_json.pop('results', None)
        json.dump(summary_for_json, f, indent=2, default=str)
    
    logger.info(f"Group {group_id} validation completed in {summary['processing_time']:.1f} seconds")
    logger.info(f"Results: {perfect_matches} perfect, {minor_differences} minor diff, "
               f"{major_differences} major diff, {errors} errors")
    
    return summary


def validate_all_groups(tolerance: float = 1e-6, 
                       output_dir: str = "../Logs") -> List[Dict[str, Any]]:
    """Validate all dataset groups.
    
    Args:
        tolerance: Tolerance for numeric comparisons
        output_dir: Output directory for reports
        
    Returns:
        List of validation summaries for each group
    """
    logger.info("Starting validation of ALL dataset groups")
    
    all_summaries = []
    
    for group_id in sorted(DATASET_GROUPS.keys()):
        try:
            summary = validate_group(group_id, tolerance, output_dir)
            all_summaries.append(summary)
        except Exception as e:
            logger.error(f"Failed to validate group {group_id}: {e}")
            # Create error summary
            error_summary = {
                'group_id': group_id,
                'group_name': DATASET_GROUPS[group_id]['name'],
                'error': str(e),
                'validation_timestamp': datetime.now().isoformat()
            }
            all_summaries.append(error_summary)
    
    # Generate consolidated summary report
    total_datasets = sum(s.get('total_datasets', 0) for s in all_summaries)
    total_perfect = sum(s.get('perfect_matches', 0) for s in all_summaries)
    total_minor = sum(s.get('minor_differences', 0) for s in all_summaries)
    total_major = sum(s.get('major_differences', 0) for s in all_summaries)
    total_errors = sum(s.get('errors', 0) for s in all_summaries)
    
    consolidated_summary = {
        'validation_type': 'ALL_GROUPS',
        'total_groups': len(DATASET_GROUPS),
        'total_datasets': total_datasets,
        'perfect_matches': total_perfect,
        'minor_differences': total_minor,
        'major_differences': total_major,
        'errors': total_errors,
        'validation_timestamp': datetime.now().isoformat(),
        'group_summaries': all_summaries
    }
    
    # Save consolidated summary
    summary_file = Path(output_dir) / "ALL_GROUPS_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(consolidated_summary, f, indent=2, default=str)
    
    logger.info(f"ALL GROUPS validation completed")
    logger.info(f"Total: {total_datasets} datasets across {len(DATASET_GROUPS)} groups")
    logger.info(f"Results: {total_perfect} perfect, {total_minor} minor diff, "
               f"{total_major} major diff, {total_errors} errors")
    
    return all_summaries


def show_validation_summary(output_dir: str = "../Logs") -> None:
    """Show summary of existing validation results."""
    
    print("=" * 80)
    print("DATADOWNLOADS VALIDATION SUMMARY")
    print("=" * 80)
    
    # Look for group summaries
    logs_dir = Path(output_dir)
    if not logs_dir.exists():
        print("No validation logs found. Run validation first.")
        return
    
    # Show group-by-group status
    for group_id in sorted(DATASET_GROUPS.keys()):
        group_info = DATASET_GROUPS[group_id]
        group_dir = logs_dir / f"Group_{group_id}"
        summary_file = group_dir / "group_summary.json"
        
        print(f"\nGroup {group_id}: {group_info['name']}")
        print(f"{'Datasets:':<12} {len(group_info['datasets'])}")
        
        if summary_file.exists():
            try:
                with open(summary_file, 'r') as f:
                    summary = json.load(f)
                
                print(f"{'Status:':<12} Validated on {summary.get('validation_timestamp', 'Unknown')[:19]}")
                print(f"{'Perfect:':<12} {summary.get('perfect_matches', 0)}")
                print(f"{'Minor Diff:':<12} {summary.get('minor_differences', 0)}")
                print(f"{'Major Diff:':<12} {summary.get('major_differences', 0)}")
                print(f"{'Errors:':<12} {summary.get('errors', 0)}")
                print(f"{'Time:':<12} {summary.get('processing_time', 0):.1f} seconds")
            except Exception as e:
                print(f"{'Status:':<12} Error reading summary: {e}")
        else:
            print(f"{'Status:':<12} Not validated yet")
    
    # Show consolidated summary if available
    consolidated_file = logs_dir / "ALL_GROUPS_summary.json"
    if consolidated_file.exists():
        try:
            with open(consolidated_file, 'r') as f:
                summary = json.load(f)
            
            print(f"\n{'=' * 80}")
            print(f"OVERALL SUMMARY")
            print(f"{'=' * 80}")
            print(f"{'Total Datasets:':<15} {summary.get('total_datasets', 0)}")
            print(f"{'Perfect Matches:':<15} {summary.get('perfect_matches', 0)} "
                  f"({summary.get('perfect_matches', 0)/summary.get('total_datasets', 1)*100:.1f}%)")
            print(f"{'Minor Differences:':<15} {summary.get('minor_differences', 0)} "
                  f"({summary.get('minor_differences', 0)/summary.get('total_datasets', 1)*100:.1f}%)")
            print(f"{'Major Differences:':<15} {summary.get('major_differences', 0)} "
                  f"({summary.get('major_differences', 0)/summary.get('total_datasets', 1)*100:.1f}%)")
            print(f"{'Errors:':<15} {summary.get('errors', 0)} "
                  f"({summary.get('errors', 0)/summary.get('total_datasets', 1)*100:.1f}%)")
            print(f"{'Last Updated:':<15} {summary.get('validation_timestamp', 'Unknown')[:19]}")
        except Exception as e:
            print(f"\nError reading consolidated summary: {e}")
    
    print(f"\n{'=' * 80}")


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Batch validation for DataDownloads script groups"
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--group', '-g',
        choices=['A', 'B', 'C', 'D', 'E', 'F', 'ALL'],
        help='Dataset group to validate (A-F or ALL for all groups)'
    )
    group.add_argument(
        '--summary', '-s',
        action='store_true',
        help='Show summary of existing validation results'
    )
    
    parser.add_argument(
        '--tolerance', '-t',
        type=float,
        default=1e-6,
        help='Tolerance for numeric comparisons (default: 1e-6)'
    )
    parser.add_argument(
        '--output-dir', '-o',
        default='../Logs',
        help='Output directory for reports (default: ../Logs)'
    )
    
    args = parser.parse_args()
    
    if args.summary:
        show_validation_summary(args.output_dir)
        return
    
    # Show group information before validation
    if args.group != 'ALL':
        group_info = DATASET_GROUPS[args.group]
        print(f"Group {args.group}: {group_info['name']}")
        print(f"Datasets ({len(group_info['datasets'])}): {', '.join(group_info['datasets'])}")
        print(f"Notes: {group_info['notes']}")
        print()
    
    try:
        if args.group == 'ALL':
            summaries = validate_all_groups(args.tolerance, args.output_dir)
            print("\nValidation completed for all groups!")
        else:
            summary = validate_group(args.group, args.tolerance, args.output_dir)
            print(f"\nValidation completed for Group {args.group}!")
            
        print(f"Reports saved to: {args.output_dir}")
        print("Use --summary to view validation status.")
        
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()