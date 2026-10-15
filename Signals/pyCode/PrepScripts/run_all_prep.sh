#!/bin/bash
#$ -cwd
#$ -m abe
#$ -t 1-2
#$ -tc 2

# Run: upload PrepScripts/* to ~/temp_prep on WRDS, then from that directory:
#   qsub run_all_prep.sh
# Inputs: the R/SAS scripts in ~/temp_prep and their WRDS source datasets.
# Outputs: data_for_dl/*, temp_output/hf_monthly.csv, and per-script logs in log/.
# Task 1 runs all OptionMetrics scripts; task 2 runs 13F and LF/HF spreads.
# Each task runs sequentially and continues past failures (SAS exits 1 on mere
# warnings); check log/ for errors. qstat tracks both.
# For a direct run on a WRDS compute node: bash run_all_prep.sh
# (This starts both workers and waits for both; do not run on a login node.)

set -uo pipefail

mkdir -p ~/temp_prep/data_for_dl ~/temp_prep/temp_output ~/temp_prep/log
cd ~/temp_prep/

run_optionmetrics() {
    # ==== OPTION METRICS: Volume ====
    echo "CREATING OPTION METRICS VOLUME (about 60 minutes)"
    R CMD BATCH --no-save --no-restore OptionMetricsVolume.R log/OptionMetricsVolume.log

    # ==== OPTION METRICS: Vol Surface ====
    echo "CREATING OPTION METRICS VOL SURFACE (about 1 hour)"
    R CMD BATCH --no-save --no-restore OptionMetricsVolSurf.R log/OptionMetricsVolSurf.log

    # ==== OPTION METRICS: XZZ (Smirk/Skew1) ====
    echo "CREATING OPTION METRICS XZZ (Smirk/Skew1, about 2 hours)"
    R CMD BATCH --no-save --no-restore OptionMetricsXZZ.R log/OptionMetricsXZZ.log

    # ==== OPTION METRICS: Bali-Hovak ====
    echo "CREATING BALI-HOVAK IMPLIED VOL (about 30 min)"
    R CMD BATCH --no-save --no-restore bali_hovak.R log/bali_hovak.log
}

run_other_prep() {
    # ==== TR 13F ====
    echo "CREATING 13F DATA (10 min?)"
    sas tr13f_pmg_edit.sas -log log/tr13f_pmg_edit.log

    # ==== LF SPREADS (CORWIN-SCHULTZ, about 15 min) ====
    echo "CREATING LF SPREADS (CORWIN-SCHULTZ, about 15 min)"
    sas corwin_schultz_edit.sas -log log/corwin_schultz_edit.log

    # === HF SPREADS ====
    # below copied from Chen-Velikov's hf-spreads-all/main.sh
    echo "RUNNING CHEN-VELIKOV FORTH, JFQA HF SPREADS"

    echo "WRDS IID SPREADS, OUTPUTS TO temp_output/ (15 min?)"
    sas taq-chen-velikov/iid_to_monthly.sas -log log/iid_to_monthly.log

    echo "CALCULATING ISSM SPREADS, OUTPUTS TO temp_output/ (about 1 hour)"
    # run spreads code day by day (full issm sample is 1983-1992)
    for year in $(seq 1983 1992)
    do
        echo "Finding spreads for nyse/amex ${year}. Today is $(date)"
        sas taq-chen-velikov/issm_spreads.sas -set yyyy "${year}" -set exchprefix nyam -log "log/log_nyam_${year}.log"

        echo "Finding spreads for nasdaq ${year}. Today is $(date)"
        sas taq-chen-velikov/issm_spreads.sas -set yyyy "${year}" -set exchprefix nasd -log "log/log_nasd_${year}.log"
    done
    sas taq-chen-velikov/combine_and_average.sas -log log/combine_and_average.log

    echo "ADDING PERMNOS TO IID AND ISSM"
    sas taq-chen-velikov/add_permnos.sas -log log/add_permnos.log
}

run_task() {
    echo "Starting prep task $1 at $(date)"
    case "$1" in
        1) run_optionmetrics ;;
        2) run_other_prep ;;
        *) echo "Invalid prep task: $1 (expected 1 or 2)" >&2; return 1 ;;
    esac
    echo "Finished prep task $1 at $(date)"
}

if [[ -n "${SGE_TASK_ID:-}" && "${SGE_TASK_ID}" != undefined ]]; then
    run_task "$SGE_TASK_ID"
else
    # Direct execution mirrors the two array tasks and reports either failure.
    run_task 1 &
    optionmetrics_pid=$!
    run_task 2 &
    other_pid=$!
    status=0
    wait "$optionmetrics_pid" || { echo "OptionMetrics task failed; see log/" >&2; status=1; }
    wait "$other_pid" || { echo "Other prep task failed; see log/" >&2; status=1; }
    exit "$status"
fi
