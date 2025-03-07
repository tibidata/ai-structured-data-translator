#!/bin/bash

# Exit on error
set -e

# Function to show usage
usage() {
    echo "Usage: $0 --major | --minor | --patch"
    exit 1
}

# Fetch the latest tags
git fetch --tags

# Get the latest tag
LATEST_TAG=$(git describe --tags --abbrev=0 2>/dev/null || echo "0.0.0")
IFS='.' read -r MAJOR MINOR PATCH <<< "$LATEST_TAG"

# Parse arguments
while [[ "$#" -gt 0 ]]; do
    case "$1" in
        --major)
            ((MAJOR++))
            MINOR=0
            PATCH=0
            ;;
        --minor)
            ((MINOR++))
            PATCH=0
            ;;
        --patch)
            ((PATCH++))
            ;;
        *)
            usage
            ;;
    esac
    shift
done

# Ensure an argument was provided
if [[ -z "$MAJOR" || -z "$MINOR" || -z "$PATCH" ]]; then
    usage
fi

NEW_TAG="$MAJOR.$MINOR.$PATCH"

echo "Merging develop into main..."
git checkout main
git pull origin main
git merge --no-ff develop

echo "Tagging new version: $NEW_TAG"
git tag "$NEW_TAG"

echo "Pushing changes to remote repository..."
git push origin main --tags

echo "Merge and tagging complete. New version: $NEW_TAG"
