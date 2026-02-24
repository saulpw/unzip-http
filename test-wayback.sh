#!/bin/bash
# Smoke test: list files from a normal zip URL and a Wayback Machine URL
# Tests the fix for GitHub issue #23 (default headers)

set -eo pipefail

NORMAL_URL='https://dl.google.com/dl/android/aosp/coral-qq3a.200805.001-factory-875379d2.zip'
WAYBACK_URL='https://web.archive.org/web/20260116203754/https://dl.google.com/dl/android/aosp/coral-qq3a.200805.001-factory-875379d2.zip'
EXPECTED='coral-qq3a.200805.001/flash-all.sh'
TIMEOUT=240

echo "=== Normal URL ==="
timeout $TIMEOUT python -m unzip_http -l "$NORMAL_URL" 2>&1 | grep -q "$EXPECTED"
echo "PASS"

echo "=== Wayback Machine URL ==="
timeout $TIMEOUT python -m unzip_http -l "$WAYBACK_URL" 2>&1 | grep -q "$EXPECTED"
echo "PASS"
