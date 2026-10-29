#!/usr/bin/env bash
# Trae al monorepo los commits que el equipo hizo en los espejos, uno por uno y sin tocar main:
#   nina-col/AiChallengeFront -> apps/mobile
#   nina-col/AiChallengeBack  -> apps/api
#
# Cada commit del equipo (los que no son "sync monorepo@…") se aplica con su autor, fecha y
# mensaje en una rama de revisión `equipo/<front|back>-<fecha>`, y se marca con el trailer
# `Mirror-Commit: <repo>@<sha>`. Así se ve qué hizo cada quien y la app no cambia de golpe:
# se revisa la rama y se mezcla a main cuando está lista. Un commit ya importado no se repite.
#
# Uso: scripts/import-team-repos.sh [front|back|all] [rama]
#   (por defecto: all y la rama principal del espejo; con rama, por ejemplo `front magda`)
set -euo pipefail

FRONT_REMOTE="${FRONT_REMOTE:-https://github.com/nina-col/AiChallengeFront.git}"
BACK_REMOTE="${BACK_REMOTE:-https://github.com/nina-col/AiChallengeBack.git}"

ROOT="$(git rev-parse --show-toplevel)"
STAMP="$(date +%Y%m%d-%H%M)"
BRANCH="${2:-}"

if [[ -n "$(git -C "$ROOT" status --porcelain)" ]]; then
  echo "Hay cambios sin commit en el monorepo; haz commit antes de importar." >&2
  exit 1
fi

# Nombre del repo en el trailer: nina-col/AiChallengeFront
repo_name() { sed -E 's#^https://github.com/##; s#\.git$##' <<<"$1"; }

import_one() {
  local name="$1" src="$2" remote="$3"
  local repo tmp
  repo="$(repo_name "$remote")"
  tmp="$(mktemp -d)"
  trap 'rm -rf "$tmp"' RETURN

  if [[ -n "$BRANCH" ]] && ! git ls-remote --exit-code --heads "$remote" "$BRANCH" >/dev/null; then
    echo "[$name] $repo no tiene la rama $BRANCH."
    return 0
  fi
  git clone --quiet -c core.autocrlf=false ${BRANCH:+--branch "$BRANCH"} "$remote" "$tmp/mirror"

  # Desde el último sync hacia acá; si nunca hubo sync, todo el historial.
  local last range
  last="$(git -C "$tmp/mirror" log -1 --format=%H --grep='^sync monorepo@' || true)"
  range="${last:+$last..}HEAD"

  local pending=()
  while read -r sha; do
    [[ -z "$sha" ]] && continue
    if [[ "$(git -C "$tmp/mirror" log -1 --format=%s "$sha")" == sync\ monorepo@* ]]; then continue; fi
    if git -C "$ROOT" log --all --format=%H --grep="^Mirror-Commit: $repo@$sha" | grep -q .; then continue; fi
    pending+=("$sha")
  done < <(git -C "$tmp/mirror" rev-list --reverse --no-merges "$range")

  if [[ ${#pending[@]} -eq 0 ]]; then
    echo "[$name] sin commits nuevos del equipo."
    return 0
  fi

  local branch="equipo/$name${BRANCH:+-$BRANCH}-$STAMP" start n=2
  while git -C "$ROOT" show-ref --quiet --verify "refs/heads/$branch"; do
    branch="equipo/$name${BRANCH:+-$BRANCH}-$STAMP-$n"
    n=$((n + 1))
  done
  start="$(git -C "$ROOT" rev-parse --abbrev-ref HEAD)"
  git -C "$ROOT" switch --quiet -c "$branch"

  for sha in "${pending[@]}"; do
    # -3: si el monorepo cambió el mismo archivo después del sync, se intenta una mezcla de tres vías.
    if ! git -C "$tmp/mirror" format-patch --binary -1 --stdout "$sha" \
        | git -C "$ROOT" am --quiet -3 --keep-cr --directory="$src"; then
      echo "[$name] no se pudo aplicar $repo@${sha:0:7} sin conflictos (el monorepo cambió lo mismo)." >&2
      echo "  En la rama $branch: resuelve el archivo, 'git add' y 'git am --continue'. Después márcalo" >&2
      echo "  para que el sync lo reconozca y vuelve a correr este script desde esa rama por el resto:" >&2
      echo "    git commit --amend --no-edit --trailer \"Mirror-Commit: $repo@$sha\"" >&2
      echo "  O descarta el intento con 'git am --abort'." >&2
      exit 1
    fi
    git -C "$ROOT" commit --quiet --amend --no-edit --trailer "Mirror-Commit: $repo@$sha"
    echo "[$name] $(git -C "$ROOT" log -1 --format='%h %an: %s')"
  done

  git -C "$ROOT" switch --quiet "$start"
  echo "[$name] ${#pending[@]} commit(s) en la rama $branch. Revísala y, si está bien:"
  echo "    git merge --no-ff $branch"
}

case "${1:-all}" in
  front) import_one front apps/mobile "$FRONT_REMOTE" ;;
  back)  import_one back apps/api "$BACK_REMOTE" ;;
  all)   import_one front apps/mobile "$FRONT_REMOTE"; import_one back apps/api "$BACK_REMOTE" ;;
  *)     echo "Uso: $0 [front|back|all] [rama]" >&2; exit 2 ;;
esac
