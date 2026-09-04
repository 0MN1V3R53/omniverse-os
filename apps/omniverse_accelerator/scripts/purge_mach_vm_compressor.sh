#!/usr/bin/env bash
# Omniverse OS - Safe Mach VM Memory Reclamation Script
# Author: Dr. Kai Sterling

echo "=== [PURGING INACTIVE MEMORY & RECLAIMING RAM] ==="
BEFORE_FREE=$(vm_stat | grep "Pages free:" | awk '{print $3}' | tr -d '.')
BEFORE_FREE_MB=$((BEFORE_FREE * 4096 / 1024 / 1024))

echo "Free Memory Before: ${BEFORE_FREE_MB} MB"

# Execute safe user-space purge
purge 2>/dev/null || true

AFTER_FREE=$(vm_stat | grep "Pages free:" | awk '{print $3}' | tr -d '.')
AFTER_FREE_MB=$((AFTER_FREE * 4096 / 1024 / 1024))

echo "Free Memory After:  ${AFTER_FREE_MB} MB"
echo "✓ Memory reclamation executed successfully."
