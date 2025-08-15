#!/usr/bin/env python3
# ABOUTME: Runs a batch of predictor scripts and tests them
# ABOUTME: Automatically retrieves predictor names from YAML mapping and runs specified scripts

import subprocess
import sys
import time
import os
import yaml


# =============================================================================
# CONFIGURATION: Scripts to run (modify this list as needed)
# =============================================================================
PREDICTOR_SCRIPTS = "CitationsRD DivInit DivOmit DivSeason Herf HerfAsset HerfBE Investment MomOffSeason MomOffSeason06YrPlus MomOffSeason11YrPlus MomOffSeason16YrPlus MomVol RDAbility Recomm_ShortInterest TrendFactor VarCF ZZ1_RIO_MB_RIO_Disp_RIO_Turnover_RIO_Volatility"

def load_predictor_mapping():
    """Load predictor mapping from YAML file and return the mapping dict"""
    yaml_path = "Predictors/00_map_predictors.yaml"
    try:
        with open(yaml_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Could not find {yaml_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)

def get_test_predictors(scripts, mapping):
    """Extract predictor names from YAML mapping for given scripts"""
    test_predictors = []
    for script in scripts:
        script_key = f"{script}.py"
        if script_key in mapping:
            predictors = mapping[script_key].get('predictors', [])
            for predictor in predictors:
                # Remove .csv extension from predictor names
                predictor_name = predictor.replace('.csv', '')
                test_predictors.append(predictor_name)
        else:
            print(f"Warning: {script_key} not found in YAML mapping")
    return test_predictors

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n{'='*60}")
    print(f"Running: {description}")
    print(f"Command: {cmd}")
    print(f"{'='*60}")
    
    start_time = time.time()
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        elapsed = time.time() - start_time
        print(f"✅ SUCCESS ({elapsed:.1f}s): {description}")
        if result.stdout:
            print("STDOUT:", result.stdout[-500:])  # Last 500 chars
        return True
    except subprocess.CalledProcessError as e:
        elapsed = time.time() - start_time
        print(f"❌ FAILED ({elapsed:.1f}s): {description}")
        print("STDERR:", e.stderr)
        if e.stdout:
            print("STDOUT:", e.stdout[-500:])  # Last 500 chars
        return False

def main():
    # Ensure we're in pyCode directory
    if not os.path.basename(os.getcwd()) == 'pyCode':
        print("Error: This script must be run from the pyCode/ directory")
        return 1
        
    print(f"Working from: {os.getcwd()}")
    
    # Load predictor mapping from YAML
    print("Loading predictor mapping from YAML...")
    mapping = load_predictor_mapping()
    
    # Use the scripts defined at the top of the file
    predictor_scripts = PREDICTOR_SCRIPTS.split()
    
    # Automatically extract predictor names for testing from YAML
    test_predictors = get_test_predictors(predictor_scripts, mapping)
    
    if not test_predictors:
        print("Error: No valid predictors found for testing")
        return 1
    
    results = []
    
    print("Starting batch predictor run...")
    print(f"Scripts to run: {', '.join(predictor_scripts)}")
    print(f"Test predictors (from YAML): {', '.join(test_predictors)}")
    
    # Run each predictor script
    for script in predictor_scripts:
        cmd = f"python3 Predictors/{script}.py"
        success = run_command(cmd, f"Predictor: {script}")
        results.append((script, success))
    
    # Run the test
    test_cmd = f"python3 utils/test_predictors.py --predictors {' '.join(test_predictors)}"
    test_success = run_command(test_cmd, "Testing all predictors")
    
    # Summary
    print(f"\n{'='*60}")
    print("FINAL SUMMARY")
    print(f"{'='*60}")
    
    success_count = sum(1 for _, success in results if success)
    total_count = len(results)
    
    print(f"Predictor Scripts: {success_count}/{total_count} successful")
    for script, success in results:
        status = "✅" if success else "❌"
        print(f"  {status} {script}")
    
    test_status = "✅" if test_success else "❌"
    print(f"Test Suite: {test_status}")
    
    overall_success = success_count == total_count and test_success
    print(f"\nOverall: {'✅ ALL SUCCESSFUL' if overall_success else '❌ SOME FAILURES'}")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    main()