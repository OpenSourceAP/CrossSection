"""
ABOUTME: Runs the Python shipping pipeline: build -> check -> manual approval -> Hugging Face upload
ABOUTME: Replaces master_shipping.r for parquet / Hugging Face releases

How to run (from anywhere, after the Signals and Portfolios pipelines finish):
    python Shipping/Code/ship_master.py
    Each step can also be run alone: ship_1_build.py, ship_2_check.py, ship_3_upload_hf.py

INPUTS:
    - Shipping/Code/ship_settings.yaml
    - outputs of Signals/, Portfolios/, Results/, and SignalDoc.csv (see ship_1_build.py)

OUTPUTS:
    1. the release folder at out_gdrive (Google Drive, shared publicly), must start empty
    2. out_gdrive/storage_checks.txt, reviewed by hand
    3. a copy of out_gdrive on Hugging Face at hf_repo, branch hf_branch (only if
       the checks pass and the user approves)
"""

import ship_1_build
import ship_2_check
import ship_3_upload_hf
from ship_utils import CHECKS_FILE, load_settings


def main():
    settings = load_settings()
    print('Shipping configuration (ship_settings.yaml):')
    for key, value in settings.items():
        print(f'  {key:12s} {value}')
    response = input('Proceed with shipping? [y/N]: ').strip().lower()
    if response not in ('y', 'yes'):
        raise SystemExit('Shipping aborted by user.')

    # 1. write to the Google Drive location
    ship_1_build.main(settings['out_gdrive'])

    # 2. check the Google Drive location
    if not ship_2_check.main(settings['out_gdrive'], settings['old_release']):
        raise SystemExit(f'Automated checks failed; see {settings["out_gdrive"] / CHECKS_FILE}. Not uploading.')

    # 3. manual approval, then post to Hugging Face
    ship_3_upload_hf.main(settings)


if __name__ == '__main__':
    main()
