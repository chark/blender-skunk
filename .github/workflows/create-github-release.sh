#!/bin/bash

set -euo pipefail

# Inputs
releaseVersion="${RELEASE_VERSION}"
releaseMessage="${RELEASE_MESSAGE}"

# Create notes
echo 'Creating release notes'
if [[ -f "${releaseMessage}" ]]; then
  notes=$(cat "${releaseMessage}")
else
  notes="${releaseMessage}"
fi

# Find package
echo 'Looking for release .zip file'
zipFile=$(find . -maxdepth 1 -type f -name '*.zip' | head -n 1)

# Execute
echo "Creating GitHub release ${releaseVersion}"
gh release create "${releaseVersion}" \
  "${zipFile}" \
  --title "${releaseVersion}" \
  --notes "${notes}"
