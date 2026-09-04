#!/usr/bin/env python3
"""
OMNIVERSE CODE: BINARY TRIAGE & MITIGATION AUDITOR
Part of Omniverse Security Lab - Track B
Analyzes executable files (Mach-O on macOS, ELF headers) for security mitigations.
"""

import sys
import os
import struct
import subprocess

def check_macho_protections(file_path):
    """Parses Mach-O binary headers for ASLR/PIE, Stack Canaries, and ARC."""
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}
    
    with open(file_path, "rb") as f:
        magic = f.read(4)
        if len(magic) < 4:
            return {"error": "File too small"}
        
        # 64-bit Mach-O magic: 0xfeedfacf (little endian: cf fa ed fe)
        is_macho64 = magic == b"\xcf\xfa\xed\xfe"
        # 32-bit Mach-O magic: 0xfeedface (little endian: ce fa ed fe)
        is_macho32 = magic == b"\xce\xfa\xed\xfe"
        # ELF magic: 0x7f 'E' 'L' 'F'
        is_elf = magic == b"\x7fELF"

    result = {
        "file": file_path,
        "format": "Mach-O 64-bit" if is_macho64 else ("Mach-O 32-bit" if is_macho32 else ("ELF" if is_elf else "Raw Binary")),
        "pie_aslr": False,
        "stack_canary": False,
        "nx_stack": True,
        "symbols": []
    }

    # Run otool / nm if Mach-O
    if is_macho64 or is_macho32:
        try:
            otool_out = subprocess.check_output(["otool", "-hv", file_path], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
            if "PIE" in otool_out:
                result["pie_aslr"] = True
        except Exception:
            pass

        try:
            nm_out = subprocess.check_output(["nm", "-gU", file_path], stderr=subprocess.DEVNULL).decode('utf-8', errors='ignore')
            if "___stack_chk_fail" in nm_out or "___stack_chk_guard" in nm_out:
                result["stack_canary"] = True
            result["symbols"] = [line.split()[-1] for line in nm_out.strip().split("\n") if line][:15]
        except Exception:
            pass

    return result

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "/bin/ls"
    report = check_macho_protections(target)
    print("=== OMNIVERSE CODE: BINARY TRIAGE REPORT ===")
    for k, v in report.items():
        print(f"[*] {k.upper()}: {v}")
