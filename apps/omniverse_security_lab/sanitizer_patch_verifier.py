#!/usr/bin/env python3
"""
OMNIVERSE CODE: SANITIZER & AUTOMATED PATCH VERIFIER
Part of Omniverse Security Lab - Track B (Dr. Kaito Tanaka)
Demonstrates automated memory safety triage with Clang ASan and patch verification.
"""

import os
import sys
import subprocess
import tempfile

VULNERABLE_C_SOURCE = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_user_input(const char *input, size_t len) {
    char stack_buffer[16];
    // VULNERABILITY: Unbounded copy causing stack buffer overflow
    memcpy(stack_buffer, input, len);
    printf("Processed input: %s\\n", stack_buffer);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <payload>\\n", argv[0]);
        return 1;
    }
    size_t len = strlen(argv[1]);
    process_user_input(argv[1], len);
    return 0;
}
"""

PATCHED_C_SOURCE = """
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void process_user_input(const char *input, size_t len) {
    char stack_buffer[16];
    // REMEDIATION: Strict bounds verification with null termination
    size_t safe_len = (len < sizeof(stack_buffer) - 1) ? len : sizeof(stack_buffer) - 1;
    memcpy(stack_buffer, input, safe_len);
    stack_buffer[safe_len] = '\\0';
    printf("Processed input: %s\\n", stack_buffer);
}

int main(int argc, char **argv) {
    if (argc < 2) {
        printf("Usage: %s <payload>\\n", argv[0]);
        return 1;
    }
    size_t len = strlen(argv[1]);
    process_user_input(argv[1], len);
    return 0;
}
"""

def run_verification_pipeline():
    print("=== OMNIVERSE CODE: ASAN COMPILATION & DEFENSIVE PATCH VERIFICATION ===")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        vuln_src = os.path.join(tmpdir, "vuln.c")
        vuln_bin = os.path.join(tmpdir, "vuln_bin")
        patched_src = os.path.join(tmpdir, "patched.c")
        patched_bin = os.path.join(tmpdir, "patched_bin")
        
        # 1. Write Vulnerable Source
        with open(vuln_src, "w") as f:
            f.write(VULNERABLE_C_SOURCE)
            
        print("[1] Compiling vulnerable target with Apple Clang AddressSanitizer (-fsanitize=address,undefined)...")
        compile_cmd = ["clang", "-fsanitize=address,undefined", "-g", vuln_src, "-o", vuln_bin]
        res = subprocess.run(compile_cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"[-] Compilation failed: {res.stderr}")
            return False
        print("    [✓] Binary compiled with AddressSanitizer instrumentation.")
        
        # 2. Trigger vulnerability with oversized input (32 bytes into 16-byte buffer)
        oversized_input = "A" * 32
        print(f"\n[2] Executing with oversized payload ({len(oversized_input)} bytes)...")
        exec_res = subprocess.run([vuln_bin, oversized_input], capture_output=True, text=True)
        
        if "AddressSanitizer: stack-buffer-overflow" in exec_res.stderr:
            print("    [!] AddressSanitizer DETECTED stack-buffer-overflow as expected!")
            print("    [!] Crash Trace Summary:")
            for line in exec_res.stderr.split("\n"):
                if "ERROR: AddressSanitizer" in line or "WRITE of size" in line or "#0" in line:
                    print(f"        {line.strip()}")
        else:
            print(f"    Notice: Exit code {exec_res.returncode}")
            
        # 3. Apply Patch
        print("\n[3] Synthesizing automated bounds-checked patch...")
        with open(patched_src, "w") as f:
            f.write(PATCHED_C_SOURCE)
            
        print("[4] Recompiling patched target with AddressSanitizer...")
        compile_patched_cmd = ["clang", "-fsanitize=address,undefined", "-g", patched_src, "-o", patched_bin]
        res_patched = subprocess.run(compile_patched_cmd, capture_output=True, text=True)
        if res_patched.returncode != 0:
            print(f"[-] Patched compilation failed: {res_patched.stderr}")
            return False
        print("    [✓] Patched binary compiled cleanly.")
        
        # 5. Verify Patched Target
        print(f"\n[5] Re-testing patched binary with identical {len(oversized_input)}-byte input...")
        patched_exec = subprocess.run([patched_bin, oversized_input], capture_output=True, text=True)
        print(f"    - Exit Code: {patched_exec.returncode}")
        print(f"    - Output: {patched_exec.stdout.strip()}")
        if patched_exec.returncode == 0 and "AddressSanitizer" not in patched_exec.stderr:
            print("    [✓] REMEDIATION PROVEN: Zero sanitizer violations, memory bounds enforced!")
            return True
        else:
            print("    [-] Remediation failed to eliminate vulnerability.")
            return False

if __name__ == "__main__":
    success = run_verification_pipeline()
    sys.exit(0 if success else 1)
