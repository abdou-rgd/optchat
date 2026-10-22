#!/usr/bin/env bash
# LEGACY: kept to reproduce the measurements made on the PrismML fork. Current runtime: start_servers_upstream.sh.
# Starts the llama.cpp server used by OptChat (PrismML fork, CUDA): Bonsai 2 27B, 2 slots
# (slot 0 = chat, slot 1 = compactor), 12k tokens of context each. ~7.3 GB VRAM on the RTX 3060 (clean measurement).
#   -> http://127.0.0.1:18435
# The Bonsai 8B compactor experiment (models/Ternary-Bonsai-8B-PQ2_0.gguf) was a quality failure
# (bench v3: recall 2/8); it is kept on disk but not started.
LLAMA="/c/Users/abdou/mitsuba/llama/llama-server.exe"
M27="/c/Users/abdou/AppData/Local/hermes/models/Ternary-Bonsai-2-27B-PTQ1_0.gguf"
DIR="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$DIR/run"
"$LLAMA" -m "$M27" --host 127.0.0.1 --port 18435 -c 24576 -np 2 -ngl 99 --jinja -fa on -ctk q8_0 -ctv q8_0 --slots --metrics > "$DIR/run/server27b.log" 2>&1 &
echo "server starting; check: curl http://127.0.0.1:18435/health"
