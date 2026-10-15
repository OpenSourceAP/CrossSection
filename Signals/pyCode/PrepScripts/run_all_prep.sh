#!/bin/bash
#$ -cwd
#$ -m abe
#$ -t 1-4
#$ -tc 4

# Run: upload PrepScripts/* to ~/temp_prep on WRDS, then from that directory:
#   qsub run_all_prep.sh
# Inputs: the R/SAS scripts in ~/temp_prep and their WRDS source datasets.
# Outputs: data_for_dl/*, temp_output/hf_monthly.csv, and per-script logs in log/.
# Four array tasks, about 1 hour each (times measured in 2026-10):
#   1: OptionMetrics volume
#   2: OptionMetrics vol surface, XZZ, and Bali-Hovak
#   3: HF spreads (IID, ISSM, combine, add permnos)
#   4: 13F and LF spreads (Corwin-Schultz)
# Each array task gets its own 2 slots / 16 GB; peak use is about 6 GB.
# Each task runs sequentially and continues past failures (SAS exits 1 on mere
# warnings); check log/ for errors. qstat tracks all four.
# Rerun one task with: qsub -t 3 run_all_prep.sh
# For a direct run on a WRDS compute node: bash run_all_prep.sh
# (This starts all four workers and waits for them; do not run on a login node.)

set -uo pipefail

mkdir -p ~/temp_prep/data_for_dl ~/temp_prep/temp_output ~/temp_prep/log
cd ~/temp_prep/

run_om_volume() {
    # ==== OPTION METRICS: Volume ====
    echo "CREATING OPTION METRICS VOLUME (about 1 hour)"
    R CMD BATCH --no-save --no-restore OptionMetricsVolume.R log/OptionMetricsVolume.log
}

run_om_other() {
    # ==== OPTION METRICS: Vol Surface ====
    echo "CREATING OPTION METRICS VOL SURFACE (about 12 min)"
    R CMD BATCH --no-save --no-restore OptionMetricsVolSurf.R log/OptionMetricsVolSurf.log

    # ==== OPTION METRICS: XZZ (Smirk/Skew1) ====
    echo "CREATING OPTION METRICS XZZ (Smirk/Skew1, about 20 min)"
    R CMD BATCH --no-save --no-restore OptionMetricsXZZ.R log/OptionMetricsXZZ.log

    # ==== OPTION METRICS: Bali-Hovak ====
    echo "CREATING BALI-HOVAK IMPLIED VOL (about 25 min)"
    R CMD BATCH --no-save --no-restore bali_hovak.R log/bali_hovak.log
}

run_hf_spreads() {
    # === HF SPREADS ====
    # below copied from Chen-Velikov's hf-spreads-all/main.sh
    echo "RUNNING CHEN-VELIKOV FORTH, JFQA HF SPREADS"

    echo "WRDS IID SPREADS, OUTPUTS TO temp_output/ (about 10 min)"
    sas taq-chen-velikov/iid_to_monthly.sas -log log/iid_to_monthly.log

    echo "CALCULATING ISSM SPREADS, OUTPUTS TO temp_output/ (about 45 min)"
    # run spreads code day by day (full issm sample is 1983-1992)
    for year in $(seq 1983 1992)
    do
        echo "Finding spreads for nyse/amex ${year}. Today is $(date)"
        sas taq-chen-velikov/issm_spreads.sas -set yyyy "${year}" -set exchprefix nyam -log "log/log_nyam_${year}.log"

        echo "Finding spreads for nasdaq ${year}. Today is $(date)"
        sas taq-chen-velikov/issm_spreads.sas -set yyyy "${year}" -set exchprefix nasd -log "log/log_nasd_${year}.log"
    done
    sas taq-chen-velikov/combine_and_average.sas -log log/combine_and_average.log

    echo "ADDING PERMNOS TO IID AND ISSM (a few min)"
    sas taq-chen-velikov/add_permnos.sas -log log/add_permnos.log
}

run_13f_lf_spreads() {
    # ==== TR 13F ====
    echo "CREATING 13F DATA (about 7 min)"
    sas tr13f_pmg_edit.sas -log log/tr13f_pmg_edit.log

    # ==== LF SPREADS (CORWIN-SCHULTZ) ====
    echo "CREATING LF SPREADS (CORWIN-SCHULTZ, about 5 min)"
    sas corwin_schultz_edit.sas -log log/corwin_schultz_edit.log
}

run_task() {
    echo "Starting prep task $1 at $(date)"
    case "$1" in
        1) run_om_volume ;;
        2) run_om_other ;;
        3) run_hf_spreads ;;
        4) run_13f_lf_spreads ;;
        *) echo "Invalid prep task: $1 (expected 1-4)" >&2; return 1 ;;
    esac
    echo "Finished prep task $1 at $(date)"
}

if [[ -n "${SGE_TASK_ID:-}" && "${SGE_TASK_ID}" != undefined ]]; then
    run_task "$SGE_TASK_ID"
else
    # Direct execution mirrors the four array tasks and reports any failure.
    pids=()
    for task in 1 2 3 4; do
        run_task "$task" &
        pids+=($!)
    done
    status=0
    for i in "${!pids[@]}"; do
        wait "${pids[$i]}" || { echo "Prep task $((i + 1)) failed; see log/" >&2; status=1; }
    done
    exit "$status"
fi
