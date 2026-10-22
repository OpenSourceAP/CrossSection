"""
ABOUTME: Runs the Python shipping pipeline: build -> check -> manual approval -> Hugging Face upload
ABOUTME: Each step runs as its own process; the pipeline stops at the first nonzero exit code

How to run (from anywhere, after the Signals and Portfolios pipelines finish):
    python Shipping/Code/master.py
    Each step can also be run alone: 1_build.py, 2_check.py, 3_upload_hf.py

INPUTS:
    - Shipping/Code/ship_settings.yaml
    - outputs of Signals/, Portfolios/, Results/, and SignalDoc.csv (see 1_build.py)

OUTPUTS:
    1. the release folder at out_gdrive (Google Drive, shared publicly), must start empty
    2. out_gdrive/storage_checks.txt, reviewed by hand
    3. a copy of out_gdrive on Hugging Face at hf_repo, branch hf_branch (only if
       the checks pass and the user approves)
"""

import subprocess
import sys

from ship_utils import CHECKS_FILE, CODE_DIR, load_settings


def run(script):
    return subprocess.run([sys.executable, str(CODE_DIR / script)]).returncode


def main():
    settings = load_settings()
    print('Shipping configuration (ship_settings.yaml):')
    for key, value in settings.items():
        print(f'  {key:12s} {value}')
    response = input('Proceed with shipping? [y/N]: ').strip().lower()
    if response not in ('y', 'yes'):
        raise SystemExit('Shipping aborted by user.')

    # 1. write to the Google Drive location
    if run('1_build.py'):
        raise SystemExit('Build failed. Not checking or uploading.')

    # 2. check the Google Drive location
    if run('2_check.py'):
        raise SystemExit(f'Automated checks failed; see {settings["out_gdrive"] / CHECKS_FILE}. Not uploading.')

    # 3. manual approval, then post to Hugging Face
    if run('3_upload_hf.py'):
        raise SystemExit('Hugging Face upload failed or was aborted.')


if __name__ == '__main__':
    main()
