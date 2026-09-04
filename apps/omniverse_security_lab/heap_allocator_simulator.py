#!/usr/bin/env python3
"""
OMNIVERSE CODE: HEAP ALLOCATOR & SAFE LINKING SIMULATOR
Part of Omniverse Security Lab - Track C (Dr. Vivienne Laurent)
Models glibc 2.32 - 2.39+ Safe Linking (Pointer Mangling) and Tcache Invariants.
"""

import sys

def mangle_pointer(ptr_address: int, target_pointer: int) -> int:
    """
    glibc 2.32+ Safe Linking pointer mangling macro:
    #define PROTECT_PTR(pos, ptr) ((pos >> 12) ^ (ptr))
    """
    page_key = (ptr_address >> 12)
    return page_key ^ target_pointer

def demangle_pointer(ptr_address: int, mangled_pointer: int) -> int:
    """
    glibc 2.32+ Safe Linking pointer de-mangling / recovery formula:
    #define REVEAL_PTR(pos, ptr) ((pos >> 12) ^ (ptr))
    """
    page_key = (ptr_address >> 12)
    return page_key ^ mangled_pointer

class TcacheBin:
    def __init__(self, size_class: int):
        self.size_class = size_class
        self.count = 0
        self.head = 0  # Points to first chunk address
        self.entries = []

    def push(self, chunk_addr: int):
        """Pushes a chunk onto the tcache singly-linked list with pointer mangling."""
        mangled_next = mangle_pointer(chunk_addr, self.head) if self.head != 0 else mangle_pointer(chunk_addr, 0)
        self.entries.append({
            "chunk_addr": chunk_addr,
            "raw_next": self.head,
            "mangled_fd": mangled_next
        })
        self.head = chunk_addr
        self.count += 1

    def inspect(self):
        print(f"[*] Tcache Bin [Size: {self.size_class} bytes] - Count: {self.count}")
        for idx, entry in enumerate(reversed(self.entries)):
            print(f"    [Node {idx}] Addr: 0x{entry['chunk_addr']:012x} -> Mangled FD: 0x{entry['mangled_fd']:012x} -> Raw Target: 0x{entry['raw_next']:012x}")

def run_heap_modeling_demo():
    print("=== OMNIVERSE CODE: GLIBC 2.32+ HEAP ALLOCATOR SIMULATION ===")
    
    # Simulate heap base at 0x55555556a000
    heap_base = 0x55555556a000
    chunk1 = heap_base + 0x2a0
    chunk2 = heap_base + 0x300
    chunk3 = heap_base + 0x360
    
    bin_64 = TcacheBin(64)
    print("[1] Allocating and freeing 3 chunks in 64-byte size class...")
    bin_64.push(chunk1)
    bin_64.push(chunk2)
    bin_64.push(chunk3)
    
    bin_64.inspect()
    
    print("\n[2] Safe Linking Mathematical Verification:")
    page_key = chunk3 >> 12
    mangled_val = bin_64.entries[-1]["mangled_fd"]
    recovered = demangle_pointer(chunk3, mangled_val)
    print(f"    - Chunk Address:      0x{chunk3:012x}")
    print(f"    - ASLR Page Key:      0x{page_key:012x} (chunk >> 12)")
    print(f"    - Mangled Stored Val: 0x{mangled_val:012x}")
    print(f"    - Recovered Target:   0x{recovered:012x}")
    assert recovered == chunk2, "De-mangling mathematical assertion failed!"
    print("    [✓] Pointer de-mangling matches target chunk2 perfectly!")
    
    print("\n[3] Defensive Mitigation Analysis:")
    print("    - glibc Safe Linking prevents unaligned pointer corruption without a heap leak.")
    print("    - To bypass: Attacker must leak any heap address to compute page_key, then XOR desired target.")
    print("    - Defensive Hardening: Enforce 16-byte chunk alignment checks on all tcache dereferences.")

if __name__ == "__main__":
    run_heap_modeling_demo()
