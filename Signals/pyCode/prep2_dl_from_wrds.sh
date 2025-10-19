#!/usr/bin/env bash
# """
# Inputs: Expects WRDS_USERNAME and WRDS_PASSWORD loaded from .env; optional local destination (defaults to ../pyData/Prep/)
# Outputs: Downloads WRDS prep outputs into the local prep directory using password auth
# How to run: ./prep2_dl_from_wrds.sh [local_dest]
# Example: ./prep2_dl_from_wrds.sh ../pyData/Prep
# """

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -f "${SCRIPT_DIR}/.env" ]]; then
  echo "No .env file found in ${SCRIPT_DIR}. Please copy dotenv.template to .env and fill in your credentials." >&2
  exit 1
fi

set -a
# shellcheck source=/dev/null
source "${SCRIPT_DIR}/.env"
set +a

if [[ -z "${WRDS_USERNAME:-}" ]]; then
  echo "WRDS_USERNAME is not set in ${SCRIPT_DIR}/.env. Populate the variable before running this script." >&2
  exit 1
fi

if [[ -z "${WRDS_PASSWORD:-}" ]]; then
  echo "WRDS_PASSWORD is not set in ${SCRIPT_DIR}/.env. Populate the variable before running this script." >&2
  exit 1
fi

if [[ $# -gt 1 ]]; then
  echo "Usage: ./prep2_dl_from_wrds.sh [local_dest]" >&2
  exit 1
fi

resolve_path() {
  python3 - "$1" "$SCRIPT_DIR" <<'PY'
import os
import sys
target, script_dir = sys.argv[1:3]
if not target:
    print(os.path.realpath(os.path.join(script_dir, "..", "pyData", "Prep")))
else:
    if not os.path.isabs(target):
        target = os.path.join(script_dir, target)
    print(os.path.realpath(target))
PY
}

LOCAL_DEST_INPUT="${1:-}"
LOCAL_DEST="$(resolve_path "${LOCAL_DEST_INPUT}")"

WRDS_USER="${WRDS_USERNAME}"
WRDS_PASS="${WRDS_PASSWORD}"
DEST_HOST="wrds-cloud.wharton.upenn.edu"
REMOTE_PREP_DIR="~/temp_prep"
REMOTE_DL_PATH="${REMOTE_PREP_DIR}/data_for_dl/"
REMOTE_PATH="${WRDS_USER}@${DEST_HOST}:${REMOTE_DL_PATH}"
SSH_COMMON_OPTS=(-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null)
SSH_COMMON_OPTS_STR='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'

mkdir -p "${LOCAL_DEST}"

echo "Downloading WRDS prep outputs from ${REMOTE_PATH} to ${LOCAL_DEST} ..."

if command -v sshpass >/dev/null 2>&1; then
  sshpass -p "${WRDS_PASS}" scp "${SSH_COMMON_OPTS[@]}" -r "${REMOTE_PATH}"* "${LOCAL_DEST}/"
elif command -v expect >/dev/null 2>&1; then
  LOCAL_DEST="${LOCAL_DEST}" REMOTE_PATH="${REMOTE_PATH}" WRDS_USER="${WRDS_USER}" DEST_HOST="${DEST_HOST}" WRDS_PASS="${WRDS_PASS}" SSH_COMMON_OPTS_STR="${SSH_COMMON_OPTS_STR}" expect <<'EOF'
set timeout -1
proc run_with_password {command password} {
    spawn /bin/sh -c $command
    expect {
        -re "(?i)yes/no" {send "yes\r"; exp_continue}
        -re "(?i)assword:" {send "$password\r"; exp_continue}
        eof
    }
}
set remote_path $env(REMOTE_PATH)
set local_dest $env(LOCAL_DEST)
set password $env(WRDS_PASS)
set ssh_opts $env(SSH_COMMON_OPTS_STR)
run_with_password "scp $ssh_opts -r ${remote_path}* \"$local_dest/\"" $password
EOF
else
  echo "Neither sshpass nor expect is installed. Install sshpass (recommended) or expect to enable password automation." >&2
  exit 1
fi

cat <<EON
Prep outputs downloaded. Next steps:
  - Verify files such as tr_13f.csv, corwin_schultz_spread.csv, hf_monthly.csv, OptionMetrics*.csv, bali_hovak_imp_vol.csv now reside in ${LOCAL_DEST}
  - Optionally copy ~/temp_prep/log/ for troubleshooting (scp -r ${WRDS_USER}@wrds-cloud.wharton.upenn.edu:~/temp_prep/log/ Logs/wrds_prep_logs)
Consult README.md for timing expectations and monitoring tips (qstat, log files).
EON
