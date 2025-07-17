#!/usr/bin/env python3
"""
ABOUTME: approve_failure.py - CLI tool for managing validation override approvals
ABOUTME: Interactive tool to add, remove, and validate override entries in overrides.yaml

Usage:
    cd pyCode/
    source .venv/bin/activate
    python3 utils/approve_failure.py add --dataset CompustatAnnual --check missing_rows
    python3 utils/approve_failure.py list
    python3 utils/approve_failure.py validate

Commands:
    add         Add a new override approval (accepted) or rejection (rejected)
    list        List all current overrides with status indicators
    validate    Validate overrides.yaml format and detect obsolete entries
    remove      Remove an existing override

Example Workflow:
    # Accept a failure as OK (with custom threshold)
    python3 utils/approve_failure.py add --dataset GNPdefl --check imperfect_rows
    # Interactive prompts: accepted, 30%, "Precision differences acceptable"
    
    # Reject a failure as unacceptable
    python3 utils/approve_failure.py add --dataset BadDataset --check missing_rows  
    # Interactive prompts: rejected, "Data quality issue requiring investigation"

Inputs:
    - DataDownloads/overrides.yaml (read/write)
    - Latest validation reports from test_dl.py and test_predictors.py

Outputs:
    - Updated DataDownloads/overrides.yaml with new approvals/rejections
    - Console feedback on override status and validation

YAML Format Example:
    CompustatAnnual:
      - check: missing_rows
        status: accepted
        reviewed_on: 2025-07-16
        reviewed_by: ac
        details: |
          Database access limitations cause expected missing rows.
          Python API has different historical coverage than Stata WRDS.
    
    GNPdefl:
      - check: imperfect_rows
        status: accepted
        max_ratio_allowed: 30%
        reviewed_on: 2025-07-16
        reviewed_by: ac
        details: Precision differences in 6th decimal place are acceptable
      
      - check: imperfect_cells
        status: rejected
        reviewed_on: 2025-07-16
        reviewed_by: ac
        details: |
          High cell error rate indicates systematic calculation problem.
          Must investigate and fix before accepting this validation failure.
"""

import yaml
import argparse
import sys
from pathlib import Path
from datetime import datetime
import getpass

OVERRIDES_FILE = "DataDownloads/overrides.yaml"
VALID_DL_CHECKS = [
    "missing_rows", "imperfect_rows", "imperfect_cells", 
    "column_names", "column_types", "row_count"
]
VALID_PREDICTOR_CHECKS = [
    "superset_check", "precision_check", "column_names"
]

def load_overrides():
    """Load current overrides from YAML file"""
    overrides_path = Path(OVERRIDES_FILE)
    if not overrides_path.exists():
        return {}
    
    try:
        with open(overrides_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Handle empty file
            if not content.strip():
                return {}
            return yaml.safe_load(content) or {}
    except Exception as e:
        print(f"Error loading overrides: {e}")
        return {}

def save_overrides(overrides):
    """Save overrides to YAML file"""
    overrides_path = Path(OVERRIDES_FILE)
    
    try:
        with open(overrides_path, 'w', encoding='utf-8') as f:
            # Write header comment
            f.write("# Manual Overrides for Validation Failures\n")
            f.write("# This file is managed by utils/approve_failure.py\n")
            f.write("# Do not edit manually unless you understand the format\n\n")
            
            if overrides:
                yaml.dump(overrides, f, default_flow_style=False, indent=2, 
                         allow_unicode=True, sort_keys=True)
            else:
                f.write("# No overrides currently defined\n")
                
        print(f"Overrides saved to {OVERRIDES_FILE}")
        return True
    except Exception as e:
        print(f"Error saving overrides: {e}")
        return False

def validate_check_name(check, dataset_type="dl"):
    """Validate that check name is supported"""
    if dataset_type == "dl":
        return check in VALID_DL_CHECKS
    elif dataset_type == "predictor":
        return check in VALID_PREDICTOR_CHECKS
    return False

def parse_ratio(ratio_str):
    """Parse ratio string like '30%' or '0.30' to float"""
    if ratio_str.endswith('%'):
        return float(ratio_str[:-1]) / 100
    return float(ratio_str)

def format_ratio(ratio_float):
    """Format ratio float to percentage string"""
    return f"{ratio_float * 100:.2f}%"

def add_override_interactive(dataset, check):
    """Interactive process to add a new override"""
    overrides = load_overrides()
    
    # Validate check name
    if not validate_check_name(check, "dl") and not validate_check_name(check, "predictor"):
        print(f"Error: Invalid check name '{check}'")
        print(f"Valid DataDownloads checks: {VALID_DL_CHECKS}")
        print(f"Valid Predictor checks: {VALID_PREDICTOR_CHECKS}")
        return False
    
    # Check if override already exists
    if dataset in overrides:
        existing_checks = [override.get('check') for override in overrides[dataset]]
        if check in existing_checks:
            print(f"Override already exists for {dataset}.{check}")
            print("Use 'remove' command to delete it first if you want to replace it")
            return False
    
    print(f"Adding override for {dataset}.{check}")
    print("\nPlease provide the following information:")
    print("\nAPPROVAL DECISION:")
    print("  accepted - The validation failure is acceptable and should be overridden")
    print("  rejected - The failure indicates a real issue that needs to be fixed")
    print("\nExamples:")
    print("  accepted: 'Database access differences cause expected missing rows'")
    print("  rejected: 'High error rate indicates data quality problem that must be resolved'")
    
    # Get approval/rejection decision
    while True:
        status_input = input("\nApproval decision (accepted/rejected) [accepted]: ").strip().lower()
        if status_input in ['', 'accepted', 'rejected']:
            status = status_input or 'accepted'
            break
        else:
            print("Please enter 'accepted' or 'rejected'")
    
    # Get reviewer ID (default to current user)
    default_reviewer = getpass.getuser()
    reviewer = input(f"Reviewer ID [{default_reviewer}]: ").strip() or default_reviewer
    
    # Get today's date
    today = datetime.now().strftime('%Y-%m-%d')
    date_input = input(f"Review date [{today}]: ").strip() or today
    
    # Check if custom threshold is needed (only for accepted status)
    custom_threshold = None
    if status == 'accepted' and check in ["imperfect_rows", "imperfect_cells"]:
        threshold_input = input(f"Custom threshold (e.g., '30%' or leave empty for binary override): ").strip()
        if threshold_input:
            try:
                custom_threshold = parse_ratio(threshold_input)
                print(f"Using custom threshold: {format_ratio(custom_threshold)}")
            except ValueError:
                print("Invalid threshold format. Using binary override.")
    
    # Get details/justification
    print(f"\nJUSTIFICATION for {status.upper()} decision:")
    if status == 'accepted':
        print("Explain why this validation failure is acceptable:")
        print("Examples:")
        print("  - 'Precision differences in 6th decimal place due to different calculation libraries'")
        print("  - 'Missing rows caused by API access limitations, not data quality issues'")
        print("  - 'Text encoding differences that don't affect analysis results'")
    else:
        print("Explain why this validation failure should NOT be overridden:")
        print("Examples:")
        print("  - 'High error rate indicates systematic data quality problem requiring investigation'")
        print("  - 'Missing key observations suggest incomplete data download that needs fixing'")
        print("  - 'Large numerical differences indicate calculation errors that must be resolved'")
    
    print("\nEnter your detailed justification (press Enter twice when done):")
    details_lines = []
    while True:
        line = input()
        if line == "" and details_lines and details_lines[-1] == "":
            break
        details_lines.append(line)
    
    # Remove trailing empty line
    if details_lines and details_lines[-1] == "":
        details_lines.pop()
    
    details = "\n".join(details_lines)
    if not details.strip():
        print("Error: Justification details are required")
        return False
    
    # Create override entry
    override_entry = {
        'check': check,
        'status': status,
        'reviewed_on': date_input,
        'reviewed_by': reviewer,
        'details': details
    }
    
    if custom_threshold is not None:
        override_entry['max_ratio_allowed'] = format_ratio(custom_threshold)
    
    # Add to overrides
    if dataset not in overrides:
        overrides[dataset] = []
    
    overrides[dataset].append(override_entry)
    
    # Show preview
    print("\n" + "="*50)
    print("PREVIEW OF NEW OVERRIDE:")
    print("="*50)
    print(f"Dataset: {dataset}")
    print(f"Check: {check}")
    print(f"Status: {status}")
    print(f"Reviewed by: {reviewer}")
    print(f"Reviewed on: {date_input}")
    if custom_threshold:
        print(f"Custom threshold: {format_ratio(custom_threshold)}")
    print(f"Details: {details}")
    print("="*50)
    
    # Confirm
    confirm = input("\nSave this override? (y/N): ").lower().strip()
    if confirm in ['y', 'yes']:
        if save_overrides(overrides):
            print("✅ Override added successfully")
            return True
        else:
            print("❌ Failed to save override")
            return False
    else:
        print("Override cancelled")
        return False

def list_overrides():
    """List all current overrides"""
    overrides = load_overrides()
    
    if not overrides:
        print("No overrides currently defined")
        return
    
    print("Current Validation Overrides:")
    print("="*60)
    
    total_count = 0
    for dataset, dataset_overrides in sorted(overrides.items()):
        print(f"\n{dataset}:")
        for i, override in enumerate(dataset_overrides, 1):
            check = override.get('check', 'unknown')
            status = override.get('status', override.get('accepted_by') and 'accepted' or 'unknown')  # Backward compatibility
            reviewed_by = override.get('reviewed_by', override.get('accepted_by', 'unknown'))  # Backward compatibility
            reviewed_on = override.get('reviewed_on', override.get('accepted_on', 'unknown'))  # Backward compatibility
            custom_threshold = override.get('max_ratio_allowed')
            
            threshold_text = f" (threshold: {custom_threshold})" if custom_threshold else ""
            status_icon = "✅" if status == 'accepted' else "❌" if status == 'rejected' else "❓"
            print(f"  {i}. {status_icon} {check}{threshold_text}")
            print(f"     Status: {status.upper()}")
            print(f"     Reviewed by: {reviewed_by} on {reviewed_on}")
            
            details = override.get('details', '').strip()
            if details:
                # Show first line of details
                first_line = details.split('\n')[0]
                if len(first_line) > 60:
                    first_line = first_line[:57] + "..."
                print(f"     Details: {first_line}")
            
            total_count += 1
    
    print(f"\nTotal overrides: {total_count}")

def validate_overrides():
    """Validate overrides.yaml format and detect issues"""
    print("Validating overrides.yaml...")
    
    overrides = load_overrides()
    if not overrides:
        print("✅ No overrides to validate")
        return True
    
    errors = []
    warnings = []
    
    for dataset, dataset_overrides in overrides.items():
        if not isinstance(dataset_overrides, list):
            errors.append(f"{dataset}: Must be a list of overrides")
            continue
            
        for i, override in enumerate(dataset_overrides):
            prefix = f"{dataset}[{i}]"
            
            # Required fields
            if 'check' not in override:
                errors.append(f"{prefix}: Missing 'check' field")
            elif not validate_check_name(override['check'], "dl") and not validate_check_name(override['check'], "predictor"):
                errors.append(f"{prefix}: Invalid check name '{override['check']}'")
            
            # Check for status field (with backward compatibility)
            if 'status' in override:
                if override['status'] not in ['accepted', 'rejected']:
                    errors.append(f"{prefix}: Invalid status '{override['status']}' (must be 'accepted' or 'rejected')")
            
            # Check reviewer fields (support both new and old formats)
            if 'reviewed_by' not in override and 'accepted_by' not in override:
                errors.append(f"{prefix}: Missing 'reviewed_by' or 'accepted_by' field")
            
            if 'reviewed_on' not in override and 'accepted_on' not in override:
                errors.append(f"{prefix}: Missing 'reviewed_on' or 'accepted_on' field")
            else:
                # Validate date format (check both possible fields)
                date_field = override.get('reviewed_on', override.get('accepted_on'))
                if date_field:
                    try:
                        datetime.strptime(date_field, '%Y-%m-%d')
                    except ValueError:
                        errors.append(f"{prefix}: Invalid date format '{date_field}' (use YYYY-MM-DD)")
            
            if 'details' not in override or not override['details'].strip():
                errors.append(f"{prefix}: Missing or empty 'details' field")
            
            # Validate max_ratio_allowed if present
            if 'max_ratio_allowed' in override:
                try:
                    parse_ratio(override['max_ratio_allowed'])
                except ValueError:
                    errors.append(f"{prefix}: Invalid max_ratio_allowed format '{override['max_ratio_allowed']}'")
    
    # Print results
    if errors:
        print("❌ Validation FAILED")
        print("\nErrors:")
        for error in errors:
            print(f"  - {error}")
    
    if warnings:
        print("\nWarnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    if not errors and not warnings:
        print("✅ All overrides are valid")
    
    return len(errors) == 0

def remove_override(dataset, check):
    """Remove an existing override"""
    overrides = load_overrides()
    
    if dataset not in overrides:
        print(f"No overrides found for dataset '{dataset}'")
        return False
    
    # Find and remove the override
    dataset_overrides = overrides[dataset]
    removed = False
    
    for i, override in enumerate(dataset_overrides):
        if override.get('check') == check:
            removed_override = dataset_overrides.pop(i)
            removed = True
            print(f"Removed override: {dataset}.{check}")
            print(f"  Approved by: {removed_override.get('accepted_by', 'unknown')}")
            print(f"  Approved on: {removed_override.get('accepted_on', 'unknown')}")
            break
    
    if not removed:
        print(f"No override found for {dataset}.{check}")
        return False
    
    # Clean up empty dataset entries
    if not dataset_overrides:
        del overrides[dataset]
    
    return save_overrides(overrides)

def main():
    parser = argparse.ArgumentParser(description='Manage validation override approvals')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a new override approval')
    add_parser.add_argument('--dataset', required=True, help='Dataset name')
    add_parser.add_argument('--check', required=True, help='Check name')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all current overrides')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate overrides.yaml format')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove an existing override')
    remove_parser.add_argument('--dataset', required=True, help='Dataset name')
    remove_parser.add_argument('--check', required=True, help='Check name')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    # Check that script is being run from the correct directory
    if not Path("DataDownloads/00_map.yaml").exists():
        print("ERROR: This script must be run from the pyCode/ directory.")
        print("Usage: cd pyCode/ && python3 utils/approve_failure.py")
        sys.exit(1)
    
    if args.command == 'add':
        success = add_override_interactive(args.dataset, args.check)
        sys.exit(0 if success else 1)
    
    elif args.command == 'list':
        list_overrides()
    
    elif args.command == 'validate':
        success = validate_overrides()
        sys.exit(0 if success else 1)
    
    elif args.command == 'remove':
        success = remove_override(args.dataset, args.check)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()