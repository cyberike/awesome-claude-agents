#!/bin/bash

# .git-clean.sh
# -----------------------------
# 🚨 WARNING: This rewrites Git history.
# Use only if you're the repo owner and know what you're doing.
# -----------------------------

echo "🧹 Cleaning .env and other secrets from Git history..."

# Step 1: Verify you're in a git repo
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
    echo "❌ Not inside a Git repository. Aborting."
    exit 1
fi

# Step 2: Install git-filter-repo if needed
if ! command -v git-filter-repo &> /dev/null; then
    echo "📦 Installing git-filter-repo..."
    pip install git-filter-repo || {
        echo "❌ Failed to install git-filter-repo. Exiting."
        exit 1
    }
fi

# Step 3: Remove .env and debug files from history
git filter-repo --force --invert-paths --paths-from-file <(cat <<EOF
.env
debug_claude_raw.txt
EOF
)

# Step 4: Re-add .gitignore rules to ignore .env
echo ".env" >> .gitignore
echo "debug_claude_raw.txt" >> .gitignore

git add .gitignore
git commit -m "🔒 Add .env and debug files to .gitignore"

# Step 5: Push clean history
echo "🚀 Force-pushing cleaned repo to origin/main..."
git push origin main --force

echo "✅ Clean complete. Secrets wiped and repo force-pushed."
