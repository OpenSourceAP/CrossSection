# ABOUTME: Headless Google Drive download using a cached googledrive login
# ABOUTME: Used by utils/optionm_patch.py for the OptionMetrics 2023 patch (issue #156)
#
# Usage (from Signals/pyCode/):
#     Rscript utils/gdrive_download.R <file_id> <dest_path> [<file_id> <dest_path> ...]
#
# Requires a cached token from an interactive `source("gdrive_login.R")`.
#
# Inputs:
#   - Pairs of Google Drive file ids and destination paths (command-line args)
#   - Cached gargle OAuth token in ~/.cache/gargle/
# Outputs:
#   - Each file written to its destination path
#   - Exit status 0 on success, 1 on any failure

suppressPackageStartupMessages(library(googledrive))

args <- commandArgs(trailingOnly = TRUE)
if (length(args) == 0 || length(args) %% 2 != 0) {
  message("Usage: Rscript utils/gdrive_download.R <file_id> <dest_path> [...]")
  quit(status = 1)
}

# Same client settings as gdrive_login.R, so the cached token matches
options(browser = function(url) message(url))
options(gargle_oauth_client_type = "web")

ok <- tryCatch({
  # email = TRUE picks the cached token without prompting; with no token, a
  # non-interactive session errors instead of waiting for a login
  drive_auth(scopes = "drive.readonly", email = TRUE)
  TRUE
}, error = function(e) {
  message("ERROR: Google Drive login not available: ", conditionMessage(e))
  message("Log in once: from Signals/pyCode/, start R and run source(\"gdrive_login.R\")")
  FALSE
})
if (!ok) quit(status = 1)

pairs <- matrix(args, ncol = 2, byrow = TRUE)
for (i in seq_len(nrow(pairs))) {
  id <- pairs[i, 1]
  dest <- pairs[i, 2]
  ok <- tryCatch({
    dir.create(dirname(dest), recursive = TRUE, showWarnings = FALSE)
    drive_download(as_id(id), path = dest, overwrite = TRUE)
    TRUE
  }, error = function(e) {
    message("ERROR: download of ", id, " to ", dest, " failed: ", conditionMessage(e))
    FALSE
  })
  if (!ok) quit(status = 1)
}
