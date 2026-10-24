# Shipping

Packages the Signals and Portfolios outputs into a data release, posted to
Google Drive and Hugging Face.

## Pipeline (parquet + Hugging Face)

Run from anywhere with the `openap` venv (`~/venvloc/openap`):

```
python Shipping/Code/master.py
```

Steps (each can also be run alone):

1. `1_build.py`: writes the release as parquet to `out_gdrive` (must be empty).
2. `2_check.py`: checks the release and writes `storage_checks.txt` into it.
   Review that file by hand.
3. `3_upload_hf.py`: needs the PASS line in `storage_checks.txt`, a y/N
   approval, and an empty branch; then uploads to `hf_repo` @ `hf_branch` in
   one commit and verifies file names and sizes.

Locations are in `Code/ship_settings.yaml`. Helpers are in `Code/ship_utils.py`.

`master.py` runs each step as its own process and stops at the first failure.

The R scripts that built the zip/csv layout of the 2025.10 release were removed;
they are in git history at commit `d5286cc` (`Shipping/Code/master_shipping.r`).

## Upload log

| Date | Branch | Size | Files | Upload time | Notes |
| ---- | ------ | ---- | ----- | ----------- | ----- |
| 2026-10-22 | `Test-Data-2026.10` | 6.69 GB | 67 | ~38 min (16:52 to 17:30) | Test with mixed-vintage data. Fast at first (~19 MB/s), then one connection on a large parquet slowed to ~1 MB/s. Build + checks took about 5 min. |
