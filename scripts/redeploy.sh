#!/usr/bin/env bash
# Redeploy the course site on demand.
#
# Usage:
#   ./scripts/redeploy.sh [ISO_UTC_TIMESTAMP]
#
# Without arguments, rebuilds at the current time: if it is past a lecture's
# 15:00 release moment, that week unlocks immediately.
# With an ISO UTC timestamp, rebuilds as if it were that moment (for previews).
set -euo pipefail

WORKFLOW="Deploy static site to GitHub Pages"

if [[ $# -gt 0 ]]; then
    gh workflow run "$WORKFLOW" -f build_time="$1"
else
    gh workflow run "$WORKFLOW"
fi

RUN_ID="$(gh run list --workflow "$WORKFLOW" --limit 1 --json databaseId --jq '.[0].databaseId')"
echo "Deploy triggered (run $RUN_ID). Watching..."
gh run watch "$RUN_ID" --exit-status >/dev/null
echo "Done."