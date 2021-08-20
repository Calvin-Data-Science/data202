#!/bin/bash

set -ex

REPO_NAME="$1"
SOURCE_PATH="$2"
ASSIGNMENT_NAME="$3"

COMMON_DIR="$(dirname "$0")/repo-common"

repodir="repos/${REPO_NAME}"

FORCE=1

if [ -e "$repodir" ]; then
    if [ "$FORCE" == 1 ]; then
        echo "Removing existing repo"
        rm -rf "$repodir"
    else
        echo "Repo already exists!"
        exit 1
    fi
fi

# Include common data
rsync -a "${COMMON_DIR}/" "$repodir"

cat > "$repodir/${ASSIGNMENT_NAME}.Rproj" <<EOF
Version: 1.0

RestoreWorkspace: No
SaveWorkspace: No
AlwaysSaveHistory: Default

EnableCodeIndexing: Yes
UseSpacesForTab: Yes
NumSpacesForTab: 2
Encoding: UTF-8

RnwWeave: Sweave
LaTeX: pdfLaTeX

AutoAppendNewline: Yes
StripTrailingWhitespace: Yes
EOF

# Include specific data
rsync -a "${SOURCE_PATH}/" --exclude "*solution*" "$repodir"


# Create and push the repo
(
    cd "$repodir"
    git init
    git add .
    git commit -m "Initial import"
    git remote add origin "git@github.com:Calvin-DS202-FA20/${REPO_NAME}.git"
    git push --force -u origin master
)
