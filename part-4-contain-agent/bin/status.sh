#!/usr/bin/env bash
cd "$(dirname "$0")/.."
docker compose ps
echo; docker stats --no-stream --format 'table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}' agent-db agent-ollama agent-api agent-nginx agent-ui agent-mailpit agent-intranet agent-external 2>/dev/null
