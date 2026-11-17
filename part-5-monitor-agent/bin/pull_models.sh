#!/usr/bin/env bash
# Downloads the agent model and the embedding model into Ollama (about 2.2 GB the first time).
set -euo pipefail
cd "$(dirname "$0")/.."
LLM="$(grep -E '^AGENT_MODEL=' .env | cut -d= -f2-)"
EMB="$(grep -E '^OLLAMA_EMBED_MODEL=' .env | cut -d= -f2-)"
for m in "${LLM:-qwen2.5:3b}" "${EMB:-nomic-embed-text}"; do
  echo "Pulling $m ..."
  docker exec agent-ollama ollama pull "$m"
done
docker exec agent-ollama ollama list
