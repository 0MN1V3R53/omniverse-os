#!/usr/bin/env bash
set -e

echo "=== LiveCodeBench Automated PR Submission Pipeline ==="
echo "Target Model: omniverse-os-leviathan-999"
echo "Generations: /Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/livecodebench_omniverse_os/lcb_generations.jsonl"

if ! command -v gh &> /dev/null; then
    echo "[!] GitHub CLI ('gh') is not installed."
    echo "Files prepared in: /Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/livecodebench_omniverse_os"
    exit 0
fi

WORKDIR=$(mktemp -d)
echo "[*] Cloning LiveCodeBench fork in $WORKDIR..."
cd "$WORKDIR"
gh repo fork LiveCodeBench/LiveCodeBench --clone=true
cd LiveCodeBench

BRANCH_NAME="eval/omniverse-os-leviathan-999_$(date +%Y%m%d)"
git checkout -b "$BRANCH_NAME"

DEST_DIR="results/omniverse-os-leviathan-999"
mkdir -p "$DEST_DIR"
cp "/Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/livecodebench_omniverse_os/lcb_generations.jsonl" "$DEST_DIR/generations.jsonl"
cp "/Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/livecodebench_omniverse_os/lcb_metadata.json" "$DEST_DIR/metadata.json"

git add "$DEST_DIR"
git commit -m "Add LiveCodeBench evaluation for omniverse-os-leviathan-999"
echo "[*] Ready to push branch: $BRANCH_NAME"
echo "[*] Run: git push origin $BRANCH_NAME && gh pr create --repo LiveCodeBench/LiveCodeBench --title 'Add omniverse-os-leviathan-999 Results' --body 'Adds official LiveCodeBench code generation evaluation for omniverse-os-leviathan-999.'"
