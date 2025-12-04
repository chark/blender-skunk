#!/bin/bash

set -euo pipefail

# Inputs
releaseVersion="${RELEASE_VERSION}"
changelogFile="${CHANGELOG_FILE:-CHANGELOG.md}"

# Execute
echo "Extracting changelog for version ${releaseVersion}"
changelogContent=$(
awk -v ver="${releaseVersion}" '
  BEGIN { found=0 }
  $0 ~ "\\[" ver "\\]" { found=1; next }
  found && /^## \[/ { exit }
  found { print }
' "${changelogFile}"
)

# Store in GitHub variables
changelogContent=$(echo "${changelogContent}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
echo "changelogContent=${changelogContent}" >> "${GITHUB_OUTPUT}"
