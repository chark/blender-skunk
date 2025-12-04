#!/bin/bash

set -euo pipefail

# Inputs
releaseVersion="${RELEASE_VERSION}"
changelogContent="${CHANGELOG_CONTENT}"

# Execute
echo "Creating GitHub release ${releaseVersion}"
gh release create releaseVersion \
  zipfile \
  --title "${releaseVersion}" \
  --notes "${changelogContent}"
