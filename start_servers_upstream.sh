#!/usr/bin/env bash
# Starts the llama.cpp server for OptChat / Apothicaire on UPSTREAM llama.cpp (no PrismML fork):
# Bonsai 2 27B in the Q2_0 packing (Hadamard support merged upstream in b11555+; the file name
# "prism-fork-required" and the HF README are outdated). Same slots and flags as start_servers.sh.
# Measured 2026-10-17 on the RTX 3060 with build b11700 CUDA 12.4: ~8.4 GB VRAM, ~31 tok/s,
# 25-exercise benchmark 193/200 turns correct, 0/897 unverified numbers (fork: 195/200, 0/926).
#   -> http://127.0.0.1:18435
LLAMA="/c/Users/abdou/llama-upstream/bin/llama-server.exe"
M27="/c/Users/abdou/AppData/Local/hermes/models/Ternary-Bonsai-2-27B-Q2_0-prism-fork-required.gguf"
DIR="$(cd "$(dirname "$0")" && pwd)"; mkdir -p "$DIR/run"
"$LLAMA" -m "$M27" --host 127.0.0.1 --port 18435 -c 24576 -np 2 -ngl 99 --jinja -fa on -ctk q8_0 -ctv q8_0 --slots --metrics --reasoning-budget 4096 > "$DIR/run/server27b-upstream.log" 2>&1 &
echo "server starting (upstream llama.cpp); check: curl http://127.0.0.1:18435/health"
