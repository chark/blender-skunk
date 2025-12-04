#!/bin/bash

set -euo pipefail

# Inputs
releaseVersion="${RELEASE_VERSION}"
releaseMessage="${RELEASE_MESSAGE}"

# Execute
echo "Creating GitHub release ${releaseVersion}"
gh release create releaseVersion \
  zipfile \
  --title "${releaseVersion}" \
  --notes "$(cat "${releaseMessage}")"
