#!/bin/bash
WORKSPACE="/home/da/lab1_OIS1"
cd "$WORKSPACE" || exit 1

echo "Updating code..."
git fetch origin
git reset --hard "origin/lab1"

COMMIT_HASH=$(git rev-parse HEAD)
echo "Commit hash: $COMMIT_HASH"

TARGET_FILE=$(grep -rEl 'meta name="deployref"' . --exclude-dir={venv,__pycache__,.git} | head -n 1)

if [ -n "$TARGET_FILE" ]; then
    echo "Found target file: $TARGET_FILE"
    sed -i 's/content="[^"]*"/content="'"$COMMIT_HASH"'"/' "$TARGET_FILE"
    echo "Hash injected into $TARGET_FILE"
else
    echo "WARNING: No file with deployref found"
fi

echo "Restarting application..."
sudo systemctl restart app

echo "Deploy complete"
