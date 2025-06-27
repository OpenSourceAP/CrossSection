#!/usr/bin/env python3
"""
ABOUTME: Progress tracking dashboard for monitoring DataDownloads validation status
ABOUTME: Provides real-time progress tracking across all 47 Python scripts

This script creates a progress tracking dashboard to monitor validation status
and fixes applied across all DataDownloads Python scripts.

Usage:
    python3 utils/progress_tracker.py --dashboard  # Show progress dashboard
    python3 utils/progress_tracker.py --update SCRIPT_NAME STATUS  # Update script status
"""

import argparse
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Progress tracking file
PROGRESS_FILE = Path("../Logs/progress_tracking.json")

# Script status definitions
SCRIPT_STATUSES = {
    'not_started': '⚪ Not Started',
    'validation_failed': '🔴 Validation Failed', 
    'validation_passed': '🟡 Validation Passed',
    'fixes_in_progress': '🟠 Fixes In Progress',
    'fixes_completed': '🟢 Fixes Completed',
    'retesting': '🔵 Retesting',
    'verified': '✅ Verified'
}

# Issue type categories
ISSUE_TYPES = {
    'identifier_mismatch': 'Identifier Type/Format Mismatch',
    'time_calculation': 'Time Calculation/Period Arithmetic',
    'missing_values': 'Missing Value Handling',
    'column_mismatch': 'Column Count/Name Mismatch',
    'data_precision': 'Data Precision/Statistical Algorithm',
    'file_not_found': 'Output File Not Found',
    'unknown': 'Unknown/Other Issue'
}

# Dataset groups from batch validation script
DATASET_GROUPS = {
    'A': ['CCMLinkingTable', 'CCMLinkingTable.csv', 'CompustatAnnual', 'a_aCompustat', 
          'm_aCompustat', 'm_QCompustat', 'CompustatPensions', 'CompustatSegments', 
          'CompustatSegmentDataCustomers', 'monthlyShortInterest'],
    'B': ['CRSPdistributions', 'mCRSP', 'monthlyCRSP', 'monthlyCRSPraw', 
          'dailyCRSP', 'dailyCRSPprc', 'm_CRSPAcquisitions'],
    'C': ['IBES_EPS_Unadj', 'IBES_EPS_Adj', 'IBES_Recommendations', 'IBES_UnadjustedActuals'],
    'D': ['dailyFF', 'monthlyFF', 'monthlyMarket', 'monthlyLiquidity', 
          'd_qfactor', 'd_vix', 'GNPdefl', 'TBill3M'],
    'E': ['brokerLev', 'm_SP_creditratings', 'm_CIQ_creditratings'],
    'F': ['IPODates', 'pin_monthly', 'GovIndex', 'BAspreadsCorwin', 'TR_13F', 
          'IBESCRSPLinkingTable', 'hf_spread', 'OptionMetricsVolume', 'OptionMetricsVolSurf', 
          'OptionMetricsXZZ', 'OptionMetricsBH', 'OPTIONMETRICSCRSPLinkingTable', 
          'PatentDataProcessed', 'InputOutputMomentumProcessed', 'customerMom']
}

# Known completed scripts from Journal lessons learned
KNOWN_COMPLETED = {
    'CompustatAnnual': 'verified',  # From CompustatAnnual_Validation_Lessons.md
    'm_QCompustat': 'verified',  # From C_CompustatQuarterly_Data_Pipeline_Fixes.md  
    'brokerLev': 'verified'  # From W_BrokerDealerLeverage_lessons_learned.md
}


def load_progress() -> Dict[str, Any]:
    """Load progress tracking data from file."""
    if not PROGRESS_FILE.exists():
        return initialize_progress()
    
    try:
        with open(PROGRESS_FILE, 'r') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading progress file: {e}")
        return initialize_progress()


def save_progress(progress_data: Dict[str, Any]) -> None:
    """Save progress tracking data to file."""
    try:
        PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(PROGRESS_FILE, 'w') as f:
            json.dump(progress_data, f, indent=2, default=str)
    except Exception as e:
        logger.error(f"Error saving progress file: {e}")


def initialize_progress() -> Dict[str, Any]:
    """Initialize progress tracking structure."""
    all_datasets = []
    for group_datasets in DATASET_GROUPS.values():
        all_datasets.extend(group_datasets)
    
    progress = {
        'created_timestamp': datetime.now().isoformat(),
        'last_updated': datetime.now().isoformat(),
        'total_scripts': len(all_datasets),
        'scripts': {}
    }
    
    # Initialize all scripts with default status
    for dataset in all_datasets:
        status = KNOWN_COMPLETED.get(dataset, 'not_started')
        progress['scripts'][dataset] = {
            'status': status,
            'issues': [],
            'fixes_applied': [],
            'last_validation': None,
            'notes': '',
            'group': get_dataset_group(dataset)
        }
    
    return progress


def get_dataset_group(dataset: str) -> str:
    """Get the group (A-F) for a given dataset."""
    for group, datasets in DATASET_GROUPS.items():
        if dataset in datasets:
            return group
    return 'Unknown'


def update_script_status(script_name: str, status: str, 
                        issues: Optional[List[str]] = None,
                        fixes: Optional[List[str]] = None,
                        notes: Optional[str] = None) -> None:
    """Update the status of a specific script.
    
    Args:
        script_name: Name of the dataset/script
        status: New status (key from SCRIPT_STATUSES)
        issues: List of issue types found
        fixes: List of fixes applied
        notes: Additional notes
    """
    if status not in SCRIPT_STATUSES:
        raise ValueError(f"Invalid status: {status}. Valid statuses: {list(SCRIPT_STATUSES.keys())}")
    
    progress = load_progress()
    
    if script_name not in progress['scripts']:
        logger.warning(f"Script {script_name} not found in progress tracking. Adding it.")
        progress['scripts'][script_name] = {
            'status': 'not_started',
            'issues': [],
            'fixes_applied': [],
            'last_validation': None,
            'notes': '',
            'group': get_dataset_group(script_name)
        }
    
    # Update status
    progress['scripts'][script_name]['status'] = status
    progress['scripts'][script_name]['last_validation'] = datetime.now().isoformat()
    
    # Update issues if provided
    if issues is not None:
        progress['scripts'][script_name]['issues'] = issues
    
    # Update fixes if provided
    if fixes is not None:
        progress['scripts'][script_name]['fixes_applied'] = fixes
    
    # Update notes if provided
    if notes is not None:
        progress['scripts'][script_name]['notes'] = notes
    
    progress['last_updated'] = datetime.now().isoformat()
    
    save_progress(progress)
    logger.info(f"Updated {script_name} status to: {SCRIPT_STATUSES[status]}")


def show_dashboard() -> None:
    """Display the progress tracking dashboard."""
    progress = load_progress()
    
    print("=" * 100)
    print("DATADOWNLOADS PYTHON SCRIPTS - VALIDATION PROGRESS DASHBOARD")
    print("=" * 100)
    print(f"Last Updated: {progress.get('last_updated', 'Unknown')[:19]}")
    print(f"Total Scripts: {progress.get('total_scripts', 0)}")
    print()
    
    # Count status distribution
    status_counts = {}
    for script_data in progress['scripts'].values():
        status = script_data['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    # Show overall progress
    print("OVERALL PROGRESS:")
    print("-" * 50)
    for status, count in status_counts.items():
        percentage = (count / progress['total_scripts']) * 100 if progress['total_scripts'] > 0 else 0
        print(f"{SCRIPT_STATUSES.get(status, status):<25} {count:>3} ({percentage:>5.1f}%)")
    print()
    
    # Show group-by-group progress
    print("GROUP-BY-GROUP PROGRESS:")
    print("-" * 50)
    
    for group_id in sorted(DATASET_GROUPS.keys()):
        group_datasets = DATASET_GROUPS[group_id]
        print(f"\nGroup {group_id} ({len(group_datasets)} scripts):")
        
        group_status_counts = {}
        for dataset in group_datasets:
            if dataset in progress['scripts']:
                status = progress['scripts'][dataset]['status']
                group_status_counts[status] = group_status_counts.get(status, 0) + 1
            else:
                group_status_counts['not_started'] = group_status_counts.get('not_started', 0) + 1
        
        for status, count in group_status_counts.items():
            if count > 0:
                print(f"  {SCRIPT_STATUSES.get(status, status):<25} {count}")
    
    print("\n" + "=" * 100)
    print("DETAILED SCRIPT STATUS:")
    print("=" * 100)
    
    # Show detailed status for each group
    for group_id in sorted(DATASET_GROUPS.keys()):
        group_datasets = DATASET_GROUPS[group_id]
        print(f"\nGroup {group_id}:")
        print("-" * 30)
        
        for dataset in group_datasets:
            if dataset in progress['scripts']:
                script_data = progress['scripts'][dataset]
                status = script_data['status']
                status_icon = SCRIPT_STATUSES.get(status, status)
                
                print(f"{status_icon} {dataset}")
                
                # Show issues if any
                if script_data.get('issues'):
                    issues_str = ', '.join(script_data['issues'])
                    print(f"    Issues: {issues_str}")
                
                # Show fixes if any
                if script_data.get('fixes_applied'):
                    fixes_str = ', '.join(script_data['fixes_applied'])
                    print(f"    Fixes: {fixes_str}")
                
                # Show notes if any
                if script_data.get('notes'):
                    print(f"    Notes: {script_data['notes']}")
                
                # Show last validation
                if script_data.get('last_validation'):
                    print(f"    Last Validation: {script_data['last_validation'][:19]}")
            else:
                print(f"⚪ Not Started {dataset}")
    
    print("\n" + "=" * 100)


def show_priorities() -> None:
    """Show prioritized list of scripts that need attention."""
    progress = load_progress()
    
    print("=" * 80)
    print("PRIORITIZED ACTION ITEMS")
    print("=" * 80)
    
    # Group scripts by priority
    high_priority = []  # validation_failed, fixes_in_progress
    medium_priority = []  # not_started, validation_passed
    low_priority = []  # retesting, fixes_completed
    completed = []  # verified
    
    for script_name, script_data in progress['scripts'].items():
        status = script_data['status']
        
        if status in ['validation_failed', 'fixes_in_progress']:
            high_priority.append((script_name, script_data))
        elif status in ['not_started', 'validation_passed']:
            medium_priority.append((script_name, script_data))
        elif status in ['retesting', 'fixes_completed']:
            low_priority.append((script_name, script_data))
        elif status == 'verified':
            completed.append((script_name, script_data))
    
    print(f"🔴 HIGH PRIORITY ({len(high_priority)} scripts):")
    print("-" * 40)
    for script_name, script_data in high_priority:
        status_icon = SCRIPT_STATUSES.get(script_data['status'], script_data['status'])
        print(f"  {status_icon} {script_name}")
        if script_data.get('issues'):
            print(f"    Issues: {', '.join(script_data['issues'])}")
    
    print(f"\n🟡 MEDIUM PRIORITY ({len(medium_priority)} scripts):")
    print("-" * 40)
    for script_name, script_data in medium_priority:
        status_icon = SCRIPT_STATUSES.get(script_data['status'], script_data['status'])
        print(f"  {status_icon} {script_name}")
    
    print(f"\n🟢 COMPLETED ({len(completed)} scripts):")
    print("-" * 40)
    for script_name, script_data in completed:
        print(f"  ✅ Verified {script_name}")
    
    print(f"\n📊 SUMMARY:")
    print(f"  High Priority:   {len(high_priority):>2}")
    print(f"  Medium Priority: {len(medium_priority):>2}")
    print(f"  Low Priority:    {len(low_priority):>2}")
    print(f"  Completed:       {len(completed):>2}")
    print(f"  Total:           {len(progress['scripts']):>2}")
    print("=" * 80)


def main():
    """Main function with command-line interface."""
    parser = argparse.ArgumentParser(
        description="Progress tracking for DataDownloads validation"
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Dashboard command
    dashboard_parser = subparsers.add_parser('dashboard', help='Show progress dashboard')
    
    # Priorities command
    priorities_parser = subparsers.add_parser('priorities', help='Show prioritized action items')
    
    # Update command
    update_parser = subparsers.add_parser('update', help='Update script status')
    update_parser.add_argument('script_name', help='Name of the script/dataset')
    update_parser.add_argument('status', choices=list(SCRIPT_STATUSES.keys()),
                              help='New status for the script')
    update_parser.add_argument('--issues', nargs='*', 
                              choices=list(ISSUE_TYPES.keys()),
                              help='Issue types found')
    update_parser.add_argument('--fixes', nargs='*',
                              help='Fixes applied')
    update_parser.add_argument('--notes', help='Additional notes')
    
    # Initialize command
    init_parser = subparsers.add_parser('init', help='Initialize progress tracking')
    
    args = parser.parse_args()
    
    if args.command == 'dashboard':
        show_dashboard()
    elif args.command == 'priorities':
        show_priorities()
    elif args.command == 'update':
        update_script_status(args.script_name, args.status, 
                           args.issues, args.fixes, args.notes)
    elif args.command == 'init':
        progress = initialize_progress()
        save_progress(progress)
        print("Progress tracking initialized!")
        print(f"Tracking {progress['total_scripts']} scripts across {len(DATASET_GROUPS)} groups")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()