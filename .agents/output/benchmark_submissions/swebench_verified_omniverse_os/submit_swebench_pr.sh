#!/usr/bin/env bash
set -e

echo "=== Princeton NLP SWE-bench Verified Automated Submission Pipeline ==="
echo "Target Model: omniverse-os-leviathan-999"
echo "Payload: /Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/swebench_verified_omniverse_os/preds.json"

if ! command -v gh &> /dev/null; then
    echo "[!] GitHub CLI ('gh') is not installed. Please install gh or submit via browser."
    echo "Files prepared in: /Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/swebench_verified_omniverse_os"
    exit 0
fi

WORKDIR=$(mktemp -d)
echo "[*] Cloning princeton-nlp/SWE-bench fork in $WORKDIR..."
cd "$WORKDIR"
gh repo fork princeton-nlp/SWE-bench --clone=true
cd SWE-bench

BRANCH_NAME="eval/omniverse-os-leviathan-999_$(date +%Y%m%d)"
git checkout -b "$BRANCH_NAME"

DEST_DIR="evaluation/verified/$(date +%Y%m%d)_omniverse-os-leviathan-999"
mkdir -p "$DEST_DIR"
cp "/Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/swebench_verified_omniverse_os/preds.json" "$DEST_DIR/all_preds.json"
cp "/Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/swebench_verified_omniverse_os/metadata.yaml" "$DEST_DIR/metadata.yaml"
cp "/Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/swebench_verified_omniverse_os/README.md" "$DEST_DIR/README.md"

git add "$DEST_DIR"
git commit -m "Add evaluation results for omniverse-os-leviathan-999 on SWE-bench Verified"
echo "[*] Ready to push branch: $BRANCH_NAME"
echo "[*] Run: git push origin $BRANCH_NAME && gh pr create --repo princeton-nlp/SWE-bench --title 'Add omniverse-os-leviathan-999 on SWE-bench Verified' --body 'Adds official evaluation predictions and metadata for omniverse-os-leviathan-999.'"
