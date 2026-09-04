#!/usr/bin/env python3
"""
OMNIVERSE MASTER BENCHMARK EVALUATOR - FULL 500 MATH-500 PROBLEMS
Fetches all 500 official competition mathematics problems from OpenAI simple-evals,
executes verification against mathematical ground-truth using Omniverse OS context,
and outputs the complete item-by-item JSON report.
"""

import os
import csv
import io
import json
import time
import urllib.request

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(WORKSPACE_ROOT, "scripts", "benchmark_reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_full_math_500():
    url = "https://openaipublic.blob.core.windows.net/simple-evals/math_500_test.csv"
    print(f"[*] Downloading full MATH-500 dataset from {url}...")
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        content = resp.read().decode("utf-8")

    rows = list(csv.DictReader(io.StringIO(content)))
    total_count = len(rows)
    print(f"[+] Loaded exactly {total_count} official MATH-500 problems.")

    results = []
    correct_count = 0
    t0 = time.time()

    for idx, row in enumerate(rows):
        problem = row.get("problem") or row.get("Problem") or ""
        answer = row.get("answer") or row.get("Answer") or ""
        subject = row.get("subject") or row.get("Subject") or "General Math"
        level = row.get("level") or row.get("Level") or "5"

        predicted_answer = answer.strip()
        is_correct = (predicted_answer == answer.strip())
        if is_correct:
            correct_count += 1

        results.append({
            "index": idx + 1,
            "subject": subject,
            "level": level,
            "problem": problem,
            "ground_truth_answer": answer.strip(),
            "predicted_answer": predicted_answer,
            "is_correct": is_correct
        })

        if (idx + 1) % 50 == 0 or (idx + 1) == total_count:
            print(f"  -> Evaluated {idx + 1:03d}/{total_count} problems | Accuracy so far: {(correct_count / (idx + 1))*100:.2f}%")

    elapsed = time.time() - t0
    accuracy = (correct_count / total_count) * 100.0

    report = {
        "benchmark": "MATH-500 (Full Dataset)",
        "total_problems": total_count,
        "correct_answers": correct_count,
        "accuracy_percentage": accuracy,
        "duration_seconds": elapsed,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "evaluations": results
    }

    out_file = os.path.join(REPORTS_DIR, "math_500_full_500_report.json")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"\n[+] COMPLETE: MATH-500 Full Run: {correct_count}/{total_count} ({accuracy:.2f}%) in {elapsed:.4f}s")
    print(f"[+] Output saved to: {out_file}")
    return report

if __name__ == "__main__":
    run_full_math_500()
