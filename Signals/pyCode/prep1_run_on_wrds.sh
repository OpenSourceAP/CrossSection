#!/usr/bin/env bash
# """
# Inputs: Expects WRDS_USERNAME and WRDS_PASSWORD loaded from .env; requires PrepScripts/ populated locally
# Outputs: Copies PrepScripts files into ~/temp_prep on wrds-cloud.wharton.upenn.edu and submits run_all_prep.sh via qsub
# How to run: ./prep1_copy_to_wrds.sh
# Example: ./prep1_copy_to_wrds.sh
# """

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

LOCAL_PREP_DIR="${SCRIPT_DIR}/PrepScripts"

if [[ ! -d "${LOCAL_PREP_DIR}" ]]; then
  echo "PrepScripts directory not found at ${LOCAL_PREP_DIR}" >&2
  exit 1
fi

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

if [[ $# -ne 0 ]]; then
  echo "This script no longer accepts command-line arguments; configure WRDS_USERNAME in ${SCRIPT_DIR}/.env instead." >&2
  exit 1
fi

WRDS_USER="${WRDS_USERNAME}"

DEST_HOST="wrds-cloud.wharton.upenn.edu"
REMOTE_PREP_DIR="~/temp_prep"
DEST="${WRDS_USER}@${DEST_HOST}:${REMOTE_PREP_DIR}"
REMOTE_CMD="cd ${REMOTE_PREP_DIR} && qsub run_all_prep.sh"
SSH_COMMON_OPTS=(-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null)
SSH_COMMON_OPTS_STR='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'

echo "Copying PrepScripts to ${DEST} ..."

if command -v sshpass >/dev/null 2>&1; then
  sshpass -p "${WRDS_PASSWORD}" scp "${SSH_COMMON_OPTS[@]}" -r "${LOCAL_PREP_DIR}/." "${DEST}"
  echo "Submitting run_all_prep.sh on ${DEST_HOST} ..."
  sshpass -p "${WRDS_PASSWORD}" ssh "${SSH_COMMON_OPTS[@]}" "${WRDS_USER}@${DEST_HOST}" "${REMOTE_CMD}"
elif command -v expect >/dev/null 2>&1; then
  LOCAL_PREP_DIR="${LOCAL_PREP_DIR}" DEST="${DEST}" DEST_HOST="${DEST_HOST}" REMOTE_CMD="${REMOTE_CMD}" WRDS_USER="${WRDS_USER}" WRDS_PASSWORD="${WRDS_PASSWORD}" SSH_COMMON_OPTS_STR="${SSH_COMMON_OPTS_STR}" expect <<'EOF'
set timeout -1
proc run_with_password {command password} {
    spawn /bin/sh -c $command
    expect {
        -re "(?i)yes/no" {send "yes\r"; exp_continue}
        -re "(?i)assword:" {send "$password\r"; exp_continue}
        eof
    }
}
set local_dir $env(LOCAL_PREP_DIR)
set dest $env(DEST)
set dest_host $env(DEST_HOST)
set remote_cmd $env(REMOTE_CMD)
set username $env(WRDS_USER)
set password $env(WRDS_PASSWORD)
set ssh_opts $env(SSH_COMMON_OPTS_STR)
run_with_password "scp $ssh_opts -r \"$local_dir/.\" \"$dest\"" $password
send_user "Submitting run_all_prep.sh on $dest_host ...\n"
run_with_password "ssh $ssh_opts \"$username@$dest_host\" \"$remote_cmd\"" $password
EOF
else
  echo "Neither sshpass nor expect is installed. Install sshpass (recommended) or expect to enable password automation." >&2
  exit 1
fi

cat <<'EON'
Prep scripts copied and run_all_prep.sh submitted on WRDS Cloud.
Next steps:
  - Monitor queue: ssh <wrds_username>@wrds-cloud.wharton.upenn.edu && qstat
  - Tail logs in ~/temp_prep once the job starts (e.g., less run_all_prep.sh.o<JOBID>)
  - Review README.md for timing expectations and troubleshooting tips.
EON
