#!/bin/bash

set -euo pipefail

# Execute
echo 'Looking for release .zip file'
zipfile=$(find . -maxdepth 1 -type f -name '*.zip' | head -n 1)
zipFileBaseName="${zipfile%.zip}"

echo "Extracting version from ${zipfile}"
releaseVersion="${zipFileBaseName##*-}"

# Store in GitHub variables
echo "releaseVersion=${releaseVersion}" >> "${GITHUB_OUTPUT}"
