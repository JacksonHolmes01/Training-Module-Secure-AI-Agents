#!/usr/bin/env bash
# Creates every secret this lab needs. Safe to run more than once:
# existing secrets are kept, never overwritten.
set -euo pipefail
cd "$(dirname "$0")/.."

gen() { openssl rand -base64 48 | tr -d '/+=\n' | cut -c1-40; }

mkdir -p secrets
for name in postgres_password kb_ingest_password agent_app_password internal_api_key; do
  f="secrets/${name}.txt"
  if [[ -s "$f" ]]; then echo "  kept     $f"; else gen > "$f"; echo "  created  $f"; fi
done
chmod 600 secrets/*.txt

if [[ ! -f .env ]]; then cp .env.example .env; echo "  created  .env (from .env.example)"; fi
setkey() {  # setkey <VAR> <value>
  if grep -qE "^$1=.{20,}" .env; then echo "  kept     $1 in .env"
  else sed -i.bak "s|^$1=.*|$1=$2|" .env && rm -f .env.bak; echo "  created  $1 in .env"; fi
}
setkey ALICE_API_KEY "$(gen)"
setkey BOB_API_KEY "$(gen)"
setkey INTERNAL_API_KEY "$(cat secrets/internal_api_key.txt)"
chmod 600 .env
docker volume create secure-ai-agents_ollama_data >/dev/null
echo "  ready    model volume secure-ai-agents_ollama_data (shared by Parts 1 to 5)"
echo "Secrets ready."
