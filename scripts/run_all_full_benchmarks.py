#!/usr/bin/env python3
"""
OMNIVERSE MASTER BENCHMARK RUNNER - EXECUTE ALL FULL BENCHMARKS
Executes all 5 full-scale benchmark pipelines end-to-end:
1. GPQA Diamond (All 198 Questions)
2. MATH-500 (All 500 Problems)
3. AIME 2024 (All 30 Problems: AIME I & AIME II)
4. HumanEval (All 164 Coding Tasks)
5. SWE-bench Verified (All 500 Predictions)
"""

import os
import sys
import json
import time
import subprocess

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(WORKSPACE_ROOT, "scripts")
REPORTS_DIR = os.path.join(SCRIPTS_DIR, "benchmark_reports")
os.makedirs(REPORTS_DIR, exist_ok=True)

def run_script(script_name):
    script_path = os.path.join(SCRIPTS_DIR, script_name)
    print("\n" + "#" * 80)
    print(f"🚀 EXECUTING: {script_name}")
    print("#" * 80)
    res = subprocess.run([sys.executable, script_path], capture_output=False, text=True)
    if res.returncode != 0:
        print(f"[!] Warning: {script_name} exited with code {res.returncode}")
    return res.returncode == 0

def main():
    start_time = time.time()
    print("=" * 80)
    print("⚡ OMNIVERSE MASTER FULL-SCALE BENCHMARK EXECUTION PIPELINE")
    print("Timestamp:", time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()))
    print("=" * 80)

    # 1. GPQA Diamond (198 Questions)
    run_script("run_full_gpqa_diamond.py")

    # 2. MATH-500 (500 Problems)
    run_script("run_full_math_500.py")

    # 3. AIME 2024 (30 Problems)
    run_script("run_full_aime_2024.py")

    # 4. HumanEval / Coding (164 Tasks)
    run_script("run_full_humaneval_coding.py")

    # 5. SWE-bench Verified (500 Predictions)
    run_script("generate_full_swebench_predictions.py")

    total_time = time.time() - start_time
    print("\n" + "=" * 80)
    print(f"🎉 ALL 5 FULL-SCALE BENCHMARKS EXECUTED IN {total_time:.2f}s")
    print("All individual and summary reports saved in:", REPORTS_DIR)
    print("=" * 80)

if __name__ == "__main__":
    main()
