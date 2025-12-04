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

# Create .tmp file for changelog contents as GitHub actions complains when storing directly in vars
changelogContent=$(echo "${changelogContent}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
changelogFile=$(mktemp "/tmp/CHANGELOG.XXXXXX.md")
echo "${changelogContent}" > "${changelogFile}"

# Store in GitHub variables
changelogContent=$(echo "${changelogContent}" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
echo "changelogFile=${changelogFile}" >> "${GITHUB_OUTPUT}"
