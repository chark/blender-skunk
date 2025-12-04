#!/bin/bash

set -euo pipefail

# Inputs
releaseVersion="${RELEASE_VERSION}"
changelogFile="${CHANGELOG_FILE:-CHANGELOG.md}"

# Update repo before making any changes
echo 'Updating repo'
git pull --rebase --autostash

# Change date in changelog
today=$(date +%Y-%m-%d)
sed -i -E "s/^(## \[${releaseVersion}\]\(.*\) - ).*/\1${today}/" "${changelogFile}"

# Commit changes
git add "${changelogFile}"
if ! git diff --cached --quiet; then
  git commit -m "Set release ${releaseVersion} date to ${today}"
  git push
else
  echo "No changes detected in '${changelogFile}', skipping commit"
fi
