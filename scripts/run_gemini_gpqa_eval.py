#!/usr/bin/env python3
"""
OFFICIAL GPQA DIAMOND EVALUATION RUNNER (LIVE MODEL SAMPLING)
Evaluates real items from openaipublic.blob.core.windows.net/simple-evals/gpqa_diamond.csv
using the live Gemini API endpoint.
"""

import os
import csv
import io
import json
import re
import time
import urllib.request

def get_api_key():
    with open('.env') as f:
        for line in f:
            if line.startswith('GEMINI_API_KEY='):
                return line.split('=', 1)[1].strip().strip('\"').strip('\'')
    return None

def query_gemini(api_key, model_name, prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0}
    }
    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        try:
            return res["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError):
            return ""

def run_gpqa_evaluation(num_items=5, model="models/gemini-2.5-flash"):
    api_key = get_api_key()
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in .env")
        return

    print("=" * 70)
    print(f"🔬 RUNNING LIVE GPQA DIAMOND EVALUATION ({num_items} OFFICIAL ITEMS)")
    print(f"Model Endpoint: {model}")
    print("=" * 70)

    url = "https://openaipublic.blob.core.windows.net/simple-evals/gpqa_diamond.csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as resp:
        content = resp.read().decode("utf-8")
    
    rows = list(csv.DictReader(io.StringIO(content)))
    print(f"Loaded full dataset of {len(rows)} official GPQA Diamond items.")

    results = []
    correct_count = 0

    for i in range(min(num_items, len(rows))):
        row = rows[i]
        q = row["Question"].strip()
        correct_ans = row["Correct Answer"].strip()
        distractors = [row["Incorrect Answer 1"].strip(), row["Incorrect Answer 2"].strip(), row["Incorrect Answer 3"].strip()]
        
        # Fixed deterministic choice arrangement (A=Correct, B, C, D)
        choices = [correct_ans] + distractors
        import random
        rng = random.Random(i)
        perm = list(range(4))
        rng.shuffle(perm)
        shuffled_choices = [choices[p] for p in perm]
        correct_letter = "ABCD"[perm.index(0)]

        prompt = f"""Answer the following graduate-level multiple-choice question.
Provide your reasoning step by step, and end your response with: "Final Answer: [Letter]" (e.g. Final Answer: A).

Question:
{q}

Choices:
(A) {shuffled_choices[0]}
(B) {shuffled_choices[1]}
(C) {shuffled_choices[2]}
(D) {shuffled_choices[3]}
"""

        print(f"\nEvaluating Item #{i+1}...")
        t0 = time.time()
        response_text = query_gemini(api_key, model, prompt)
        elapsed = time.time() - t0

        match = re.search(r"Final Answer:\s*([ABCD])", response_text, re.IGNORECASE)
        predicted_letter = match.group(1).upper() if match else "NONE"
        is_correct = (predicted_letter == correct_letter)
        if is_correct:
            correct_count += 1

        print(f"  Predicted: {predicted_letter} | Ground Truth: {correct_letter} | Correct: {is_correct} ({elapsed:.2f}s)")

        results.append({
            "item_id": i + 1,
            "question": q,
            "ground_truth_letter": correct_letter,
            "ground_truth_text": correct_ans,
            "predicted_letter": predicted_letter,
            "is_correct": is_correct,
            "response_snippet": response_text[:200] + "...",
            "duration_seconds": elapsed
        })

    accuracy_pct = (correct_count / len(results)) * 100.0
    print("\n" + "=" * 70)
    print(f"🏆 LIVE GPQA EVALUATION RESULT: {correct_count}/{len(results)} ({accuracy_pct:.1f}%)")
    print("=" * 70)

    output = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime()),
        "dataset": "GPQA Diamond (Official)",
        "model": model,
        "total_evaluated": len(results),
        "correct": correct_count,
        "accuracy_pct": accuracy_pct,
        "item_results": results
    }

    with open("scripts/live_gpqa_eval_result.json", "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)
    print("Saved raw output to: scripts/live_gpqa_eval_result.json")

if __name__ == "__main__":
    run_gpqa_evaluation(num_items=5, model="models/gemini-2.5-flash")
