#!/bin/sh
# This script enforces that commits can only be made from branches
# starting with "feature/" or "fix/".

BRANCH=$(git rev-parse --abbrev-ref HEAD)

case "$BRANCH" in
  feature/*|fix/*)
    exit 0
    ;;
  *)
    echo "Error: Commits are only allowed on branches that start with 'feature/' or 'fix/'. Current branch: '$BRANCH'."
    exit 1
    ;;
esac
