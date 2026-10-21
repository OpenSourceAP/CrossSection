# ABOUTME: One-time Google Drive login for the OptionMetrics 2023 patch (issue #156)
# ABOUTME: Caches a gargle OAuth token so utils/gdrive_download.R can run headless
#
# Usage (from Signals/pyCode/, in an INTERACTIVE R session; Rscript cannot
# wait for the pasted code):
#     R
#     > source("gdrive_login.R")
#
# Open the printed URL, sign in with any Google account, tick
# "See and download all your Google Drive files", and paste the code back
# into R. The token is cached in ~/.cache/gargle/, so later runs skip this.
#
# Inputs:
#   - Google account login (interactive)
#   - Open AP 2023 release file CPVolSpread.csv (metadata only, as a smoke test)
# Outputs:
#   - Cached OAuth token in ~/.cache/gargle/
#   - Console: logged-in user and a success line

suppressPackageStartupMessages(library(googledrive))

# Container has no browser: print the login URL instead of opening it
options(browser = function(url) message("\nOpen this URL in your browser:\n", url, "\n"))

# Always use the copy-paste flow. Google retired it for "installed" clients
# (400 invalid_request), so use the "web" client, which redirects to a
# tidyverse page that shows the code to paste. Force use_oob even when httpuv
# is installed (e.g. on a Mac): the "web" client rejects gargle's localhost
# redirect (400 redirect_uri_mismatch)
options(gargle_oauth_client_type = "web")

drive_auth(scopes = "drive.readonly", use_oob = TRUE)
print(drive_user())

# Smoke test: read metadata of one known 2023 file (no download)
smoke <- tryCatch(
  drive_get(as_id("1FQZ1t7B5A8Ei48io6daobimtZ_0dB5Z8")),
  error = function(e) {
    message("\nERROR: Drive call failed: ", conditionMessage(e))
    message("If this is '403 insufficient authentication scopes', you did not tick")
    message("'See and download all your Google Drive files'. Delete the token in")
    message("~/.cache/gargle/ and run source(\"gdrive_login.R\") again.")
    NULL
  }
)

if (!is.null(smoke)) {
  cat("\nSUCCESS: Google Drive login works. Found", smoke$name, "\n")
  cat("The token is cached; pipeline runs can now download the 2023 OptionMetrics signals.\n")
}
