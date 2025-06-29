#!/usr/bin/env python3
"""
ABOUTME: Extract column schemas from DTA files using existing column_standardizer
ABOUTME: This script reads actual DTA files to capture column names and order

This script uses the existing column_standardizer.get_dta_column_order() function
to extract column information from DTA files, preparing for YAML-based replacement.
"""

import os
import sys
import yaml
from pathlib import Path

# Add parent directory to path to import column_standardizer
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from utils.column_standardizer import get_dta_column_order

def extract_dataset_schema(dataset_name, dta_filename):
    """
    Extract column schema for a specific dataset.
    
    Args:
        dataset_name (str): Name of the dataset
        dta_filename (str): Name of the DTA file
        
    Returns:
        dict: Schema information with columns list
    """
    # Path to DTA file
    dta_path = f"../Data/Intermediate/{dta_filename}"
    
    print(f"\n=== Extracting schema for {dataset_name} ===")
    print(f"DTA file: {dta_path}")
    
    # Check if file exists
    if not os.path.exists(dta_path):
        print(f"❌ File not found: {dta_path}")
        return None
    
    # Get column order from DTA file
    try:
        columns = get_dta_column_order(dta_path)
        
        if columns is None:
            print(f"❌ Failed to read columns from {dta_path}")
            return None
            
        print(f"✅ Successfully read {len(columns)} columns")
        print(f"Columns: {columns}")
        
        schema = {
            'dataset_name': dataset_name,
            'dta_file': dta_filename,
            'columns': columns,
            'num_columns': len(columns)
        }
        
        return schema
        
    except Exception as e:
        print(f"❌ Error reading {dta_path}: {e}")
        return None

def analyze_special_cases(dataset_name):
    """
    Analyze special handling cases from column_standardizer.py
    """
    special_cases = []
    
    # Check for known special cases
    if dataset_name == "pin_monthly":
        special_cases.append({
            "type": "special_handling", 
            "description": "PIN model parameters with defaults",
            "details": "Removes 'pin' column, adds PIN params (a=0.25, eb=5.5, es=15.0, u=0.12, d=0.65)"
        })
    
    if dataset_name == "OptionMetricsVolSurf":
        special_cases.append({
            "type": "missing_column_default",
            "description": "Date placeholder", 
            "details": "Adds 'date' column with '2020-01-01' if missing"
        })
    
    # Check for unwanted columns (these are always removed)
    special_cases.append({
        "type": "column_removal",
        "description": "Index columns removed",
        "details": "Removes columns starting with '__index_level_' or named 'index'"
    })
    
    return special_cases

def generate_yaml_schema(schemas):
    """
    Generate YAML schema from extracted schemas
    """
    yaml_data = {}
    yaml_data['# Column Schemas'] = 'Generated from DTA files using extract_column_schemas.py'
    yaml_data['# This replaces column_standardizer.py DTA file dependencies'] = None
    
    # Group schemas by type
    for dataset_name, schema in schemas.items():
        yaml_data[dataset_name] = {
            'columns': schema['columns'],
            'special_handling': {}
        }
        
        # Add special handling rules
        for case in schema['special_cases']:
            if case['type'] == 'special_handling':
                yaml_data[dataset_name]['special_handling']['pin_parameters'] = {
                    'remove_columns': ['pin'],
                    'add_defaults': {
                        'a': 0.25,
                        'eb': 5.5, 
                        'es': 15.0,
                        'u': 0.12,
                        'd': 0.65
                    }
                }
            elif case['type'] == 'missing_column_default':
                yaml_data[dataset_name]['special_handling']['default_values'] = {
                    'date': '2020-01-01'
                }
        
        # Add common rules (apply to all datasets)
        yaml_data[dataset_name]['special_handling']['remove_patterns'] = [
            '__index_level_*',
            'index'
        ]
    
    return yaml_data

def save_yaml_schema(schemas, output_file="column_schemas.yaml"):
    """Save schemas to YAML file"""
    yaml_data = generate_yaml_schema(schemas)
    
    output_path = os.path.join(os.path.dirname(__file__), output_file)
    
    with open(output_path, 'w') as f:
        # Custom YAML dump to make it more readable
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False, width=120)
    
    print(f"\n✅ YAML schema saved to: {output_path}")
    return output_path

def main():
    """Extract schemas for test datasets"""
    print("Column Schema Extraction Tool")
    print("=" * 50)
    
    # Test datasets - start with these 3, plus a few more to test
    test_datasets = [
        ("pin_monthly", "pin_monthly.dta"),
        ("CRSPdistributions", "CRSPdistributions.dta"), 
        ("a_aCompustat", "a_aCompustat.dta"),
        ("m_aCompustat", "m_aCompustat.dta"),
        ("monthlyCRSP", "monthlyCRSP.dta")
    ]
    
    schemas = {}
    
    for dataset_name, dta_filename in test_datasets:
        schema = extract_dataset_schema(dataset_name, dta_filename)
        if schema:
            # Add special case analysis
            schema['special_cases'] = analyze_special_cases(dataset_name)
            schemas[dataset_name] = schema
    
    print(f"\n=== Summary ===")
    print(f"Successfully extracted {len(schemas)} schemas")
    
    for name, schema in schemas.items():
        print(f"\n{name}:")
        print(f"  Columns: {schema['num_columns']}")
        print(f"  Column list: {', '.join(schema['columns'][:5])}{'...' if len(schema['columns']) > 5 else ''}")
        if schema['special_cases']:
            print(f"  Special cases: {len(schema['special_cases'])}")
            for case in schema['special_cases']:
                print(f"    - {case['description']}")
    
    # Generate and save YAML schema
    save_yaml_schema(schemas)
    
    return schemas

if __name__ == "__main__":
    main()