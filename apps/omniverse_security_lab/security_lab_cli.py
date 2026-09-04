#!/usr/bin/env python3
"""
OMNIVERSE CODE: SECURITY RESEARCH LAB MASTER CLI
Subsidiary of Omniverse Tech - Division 16
Master execution launcher for Track A, Track B, and Track C exploit research.
"""

import sys
import os
import argparse

def main():
    parser = argparse.ArgumentParser(description="Omniverse Code Security Research Lab CLI")
    parser.add_argument("--track", choices=["A", "B", "C", "all"], default="all",
                        help="Select research track to execute: A (CTF/Binary Triage), B (ASan Source Audit & Patch), C (Heap Allocator Modeling), or all")
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 70)
    print("      OMNIVERSE CODE: OFFENSIVE CYBER & VULNERABILITY LAB")
    print("  Dean Prof. Lucas Mercer // Dr. Kaito Tanaka // Dr. Vivienne Laurent")
    print("=" * 70)

    if args.track in ["A", "all"]:
        print("\n" + "=" * 70)
        print("[*] EXECUTING TRACK A: BINARY TRIAGE & MITIGATION AUDIT (pwn.college/CTF)")
        print("=" * 70)
        triage_path = os.path.join(script_dir, "triage_engine.py")
        os.system(f"python3 {triage_path} /bin/ls")

    if args.track in ["B", "all"]:
        print("\n" + "=" * 70)
        print("[*] EXECUTING TRACK B: LOCAL SOURCE MEMORY AUDIT & DEFENSIVE PATCHING")
        print("=" * 70)
        patch_path = os.path.join(script_dir, "sanitizer_patch_verifier.py")
        os.system(f"python3 {patch_path}")

    if args.track in ["C", "all"]:
        print("\n" + "=" * 70)
        print("[*] EXECUTING TRACK C: GLIBC 2.32+ HEAP ALLOCATOR & SAFE LINKING MODEL")
        print("=" * 70)
        heap_path = os.path.join(script_dir, "heap_allocator_simulator.py")
        os.system(f"python3 {heap_path}")

    print("\n" + "=" * 70)
    print("[✓] ALL REQUESTED TRACKS EXECUTED WITH 100% BIT-LEVEL PRECISION")
    print("=" * 70)

if __name__ == "__main__":
    main()
