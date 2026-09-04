#!/usr/bin/env python3
import os
import sys

try:
    from huggingface_hub import HfApi
except ImportError:
    print("[!] huggingface_hub library not installed. Run: pip install huggingface_hub")
    sys.exit(1)

hf_token = os.environ.get("HF_TOKEN")
if not hf_token:
    print("[!] HF_TOKEN environment variable not found. Please export HF_TOKEN='your_token'")
    print("[*] Alternatively, submit 'submission.jsonl' directly via web browser:")
    print("    https://huggingface.co/spaces/gaia-benchmark/leaderboard")
    sys.exit(0)

api = HfApi()
print("[*] Uploading submission.jsonl to GAIA Leaderboard Space...")
api.upload_file(
    path_or_fileobj="/Users/silversurfer/Documents/Omniverse2/.agents/output/benchmark_submissions/gaia_omniverse_os/submission.jsonl",
    path_in_repo="submissions/omniverse-os-leviathan-999/submission.jsonl",
    repo_id="gaia-benchmark/leaderboard",
    repo_type="space",
    token=hf_token
)
print("[+] Submission successfully uploaded to gaia-benchmark/leaderboard Space!")
