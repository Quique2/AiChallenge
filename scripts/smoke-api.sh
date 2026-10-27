#!/usr/bin/env bash
# Prueba de punta a punta de la API: crea una cuenta desechable, recorre los endpoints y la borra.
# Uso: scripts/smoke-api.sh [URL]   (por defecto http://localhost:8080; en Railway, la URL pública)
set -euo pipefail

BASE="${1:-http://localhost:8080}"
KEY="smoke-$(python -c 'import secrets; print(secrets.token_urlsafe(32))')"
AUTH=(-H "Authorization: Bearer $KEY" -H "Content-Type: application/json")
FAILS=0

# check <descripción> <código esperado> <curl args...>; deja el cuerpo en $BODY
check() {
  local desc="$1" expected="$2"
  shift 2
  local out
  out="$(curl -s -w $'\n%{http_code}' "$@")"
  BODY="${out%$'\n'*}"
  local code="${out##*$'\n'}"
  if [[ "$code" == "$expected" ]]; then
    echo "ok   $code $desc"
  else
    echo "FAIL $code (esperaba $expected) $desc: $BODY"
    FAILS=$((FAILS + 1))
  fi
}

json() { python -c "import sys, json; print(json.load(sys.stdin)$1)" <<<"$BODY"; }

check "health" 200 "$BASE/health"
check "aviso de privacidad" 200 "$BASE/privacy"
check "sin llave → 401" 401 "$BASE/v1/me"
check "llave corta → 400" 400 -X POST "$BASE/v1/auth/device" -H "Content-Type: application/json" -d '{"device_key":"corta"}'
check "sin consentimiento → 400" 400 -X POST "$BASE/v1/auth/device" -H "Content-Type: application/json" -d "{\"device_key\":\"$KEY\"}"
check "crear cuenta" 201 -X POST "$BASE/v1/auth/device" -H "Content-Type: application/json" -d "{\"device_key\":\"$KEY\",\"consent_version\":1}"
check "misma llave no duplica" 200 -X POST "$BASE/v1/auth/device" -H "Content-Type: application/json" -d "{\"device_key\":\"$KEY\"}"
check "me" 200 "${AUTH[@]}" "$BASE/v1/me"
check "cambiar idioma" 200 -X PATCH "${AUTH[@]}" "$BASE/v1/me" -d '{"locale":"en"}'
[[ "$(json "['locale']")" == "en" ]] || { echo "FAIL locale no cambió"; FAILS=$((FAILS + 1)); }
check "crear espacio" 201 -X POST "${AUTH[@]}" "$BASE/v1/spaces" -d '{"name":"Mi escritorio","kind":"office"}'
SPACE_ID="$(json "['id']")"
check "espacio inválido → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/spaces" -d '{"name":"","kind":"office"}'
check "listar espacios" 200 "${AUTH[@]}" "$BASE/v1/spaces"
[[ "$(json '.__len__()')" == "1" ]] || { echo "FAIL esperaba 1 espacio"; FAILS=$((FAILS + 1)); }

expect() { [[ "$(json "$1")" == "$2" ]] || { echo "FAIL $3: $(json "$1") ≠ $2"; FAILS=$((FAILS + 1)); }; }

check "catálogo" 200 "$BASE/v1/catalog?locale=es"
expect "['domains'].__len__()" 4 "dominios del catálogo"

CHECKIN=$(cat <<JSON
{"space_id":"$SPACE_ID","task":"reading","feeling":"focus","effort_before":4,"discomfort_before":4,
 "observations":[{"stimulus":"voices","response":"yes"},{"stimulus":"glare","response":"yes"},
                 {"stimulus":"light_dim","response":"no"}],
 "focus_stimulus":"voices"}
JSON
)
check "registrar con foco" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins" -d "$CHECKIN"
CHECKIN_ID="$(json "['checkin']['id']")"
FIRST="$(json "['proposal']['adjustment']['id']")"
expect "['proposal']['adjustment']['kind']" self "la primera propuesta es algo propio"
expect "['proposal']['reason']['kind']" first_try "sin historia es un primer intento"

check "otra idea" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$CHECKIN_ID/decline" -d '{"reason":"other_idea"}'
SECOND="$(json "['proposal']['adjustment']['id']")"
[[ "$SECOND" != "$FIRST" ]] || { echo "FAIL otra idea repitió $FIRST"; FAILS=$((FAILS + 1)); }
check "no puedo aquí" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$CHECKIN_ID/decline" -d '{"reason":"cannot_here"}'
ADJUSTMENT="$(json "['proposal']['adjustment']['id']")"
check "motivo inválido → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$CHECKIN_ID/decline" -d '{"reason":"x"}'

check "aceptar con recordatorio" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$CHECKIN_ID/accept" -d '{"remind_in_minutes":25}'
expect "['status']" trying "estado tras aceptar"
check "en curso" 200 "${AUTH[@]}" "$BASE/v1/checkins?status=trying"
expect ".__len__()" 1 "registros en curso"
check "resultado" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$CHECKIN_ID/outcome" -d '{"effort_after":2,"discomfort_after":1,"attribution":"yes"}'
expect "['checkin']['outcome']" helped "resultado"
expect "['here']['trials']" 1 "pruebas en este contexto"
check "resultado repetido → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$CHECKIN_ID/outcome" -d '{"effort_after":2,"discomfort_after":1,"attribution":"yes"}'

# El escaneo real gasta tokens: aquí solo se prueba que rechace lo inválido.
check "foto que no es JPEG → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/scan/photo" -d '{"image_base64":"aG9sYQ==","task":"reading"}'
check "audio inválido → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/scan/photo" -d '{"image_base64":"aG9sYQ==","task":"reading","audio":["smells"]}'

check "mis ajustes" 200 "${AUTH[@]}" "$BASE/v1/playbook"
expect ".__len__()" 1 "entradas en mis ajustes"
expect "[0]['adjustment']['id']" "$ADJUSTMENT" "ajuste guardado"
check "progreso" 200 "${AUTH[@]}" "$BASE/v1/progress"
expect "['tried'][0]" "$ADJUSTMENT" "ajuste probado en el progreso"

check "varios sin foco → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins" \
  -d '{"task":"writing","feeling":"drained","effort_before":3,"discomfort_before":3,"observations":[{"stimulus":"voices","response":"yes"},{"stimulus":"too_cold","response":"yes"}]}'
check "sin estímulo claro" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins" \
  -d '{"task":"writing","feeling":"other","effort_before":3,"discomfort_before":2,"observations":[{"stimulus":"voices","response":"unsure"}]}'
expect "['proposal']" None "sin estímulo no hay propuesta"
check "dejarlo" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$(json "['checkin']['id']")/abandon"
check "esfuerzo fuera de rango → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins" \
  -d '{"task":"writing","feeling":"other","effort_before":9,"discomfort_before":3}'

check "borrar espacio" 204 -X DELETE "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID"
check "borrar cuenta" 204 -X DELETE "${AUTH[@]}" "$BASE/v1/me"
check "cuenta borrada → 401" 401 "${AUTH[@]}" "$BASE/v1/me"

if ((FAILS > 0)); then
  echo "$FAILS prueba(s) fallaron"
  exit 1
fi
echo "todo bien"
