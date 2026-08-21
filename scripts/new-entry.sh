#!/usr/bin/env bash
# Convenience wrapper: ./scripts/new-entry.sh "Chunked Prefill" llm-inference
set -euo pipefail
cd "$(dirname "$0")/.."
PYTHONPATH=tools python3 -m encyclopedia new "$1" --category "$2"
