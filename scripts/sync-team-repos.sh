#!/usr/bin/env bash
# Copia apps/mobile -> nina-col/AiChallengeFront y apps/api -> nina-col/AiChallengeBack.
# Cada sync es un commit normal "sync monorepo@<sha>" con la lista de cambios; nunca force-push.
#
# Uso: scripts/sync-team-repos.sh [front|back|all]   (por defecto: all)
set -euo pipefail

FRONT_REMOTE="${FRONT_REMOTE:-https://github.com/nina-col/AiChallengeFront.git}"
BACK_REMOTE="${BACK_REMOTE:-https://github.com/nina-col/AiChallengeBack.git}"

ROOT="$(git rev-parse --show-toplevel)"
SHA="$(git -C "$ROOT" rev-parse --short HEAD)"

if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
  echo "Hay cambios sin commit en el monorepo; haz commit antes de sincronizar." >&2
  exit 1
fi

sync_one() {
  local src="$1" remote="$2"

  if [[ -z "$(git -C "$ROOT" ls-files "$src")" ]]; then
    echo "[$src] no tiene archivos versionados; no se sincroniza." >&2
    return 1
  fi

  local tmp
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' RETURN

  git clone --quiet "$remote" "$tmp/mirror"

  # Rango de cambios desde el último sync (si el espejo lo registra).
  local last range
  last="$(git -C "$tmp/mirror" log -1 --format=%s 2>/dev/null | sed -n 's/.*monorepo@\([0-9a-f]\{7,\}\).*/\1/p')"
  if [[ -n "$last" ]] && git -C "$ROOT" cat-file -e "${last}^{commit}" 2>/dev/null; then
    range="${last}..HEAD"
  else
    range="HEAD"
  fi

  # Reemplazar el contenido del espejo con los archivos versionados de $src (sin node_modules, target, .env…).
  find "$tmp/mirror" -mindepth 1 -maxdepth 1 ! -name .git -exec rm -rf {} +
  local depth
  depth="$(awk -F/ '{print NF}' <<<"${src%/}")"
  git -C "$ROOT" archive HEAD "$src" | tar -x -C "$tmp/mirror" --strip-components="$depth"

  git -C "$tmp/mirror" add -A
  if git -C "$tmp/mirror" diff --cached --quiet; then
    echo "[$src] sin cambios."
    return 0
  fi

  local changes trailers msg
  changes="$(git -C "$ROOT" log --no-merges --format='- %s' "$range" -- "$src")"
  trailers="$(git -C "$ROOT" log --format='%(trailers:key=Co-Authored-By)' "$range" -- "$src" | sed '/^$/d' | sort -u)"
  msg="sync monorepo@${SHA}"$'\n\n'"${changes:-- (sin commits nuevos en $src)}"
  [[ -n "$trailers" ]] && msg+=$'\n\n'"$trailers"

  git -C "$tmp/mirror" commit --quiet -m "$msg"
  git -C "$tmp/mirror" push --quiet origin HEAD
  echo "[$src] -> $remote ($(git -C "$tmp/mirror" rev-parse --short HEAD))"
}

case "${1:-all}" in
  front) sync_one apps/mobile "$FRONT_REMOTE" ;;
  back)  sync_one apps/api "$BACK_REMOTE" ;;
  all)   sync_one apps/mobile "$FRONT_REMOTE"; sync_one apps/api "$BACK_REMOTE" ;;
  *)     echo "Uso: $0 [front|back|all]" >&2; exit 2 ;;
esac
