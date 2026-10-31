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
expect "['domains'].__len__()" 5 "dominios del catálogo"

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

# Memoria por lugar. OTHER_ID es un lugar que no es de esta cuenta.
OTHER_ID="00000000-0000-4000-8000-000000000000"
check "memoria del lugar" 200 "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/memory"
expect "['space']['kind']" office "tipo de lugar en la memoria"
expect "['trials']" 1 "pruebas aquí"
expect "['known']" 1 "cosas que sabe aquí"
expect "['stimuli'].__len__()" 2 "lo que molesta aquí"
expect "['tried'][0]['adjustment']['id']" "$ADJUSTMENT" "probado aquí"
expect "['tried'][0]['stimulus']" voices "estímulo de lo probado"
expect "['tried'][0]['helped']" 1 "ayudó aquí"
expect "['blocked'][0]['id']" "$SECOND" "no puedo aquí"
check "memoria de un lugar ajeno → 404" 404 "${AUTH[@]}" "$BASE/v1/spaces/$OTHER_ID/memory"

# "Usarlo otra vez": repeat <ajuste> [foco]
repeat() {
  echo "{\"space_id\":\"$SPACE_ID\",\"task\":\"reading\",\"feeling\":\"focus\",\"effort_before\":3,\"discomfort_before\":3,\"focus_stimulus\":\"${2:-voices}\",\"adjustment_id\":\"$1\"}"
}
check "usarlo otra vez" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins" -d "$(repeat "$ADJUSTMENT")"
expect "['proposal']['reason']['kind']" chosen "motivo de lo elegido"
expect "['proposal']['adjustment']['id']" "$ADJUSTMENT" "propone lo elegido"
REPEAT_ID="$(json "['checkin']['id']")"
check "usarlo otra vez: aceptar" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$REPEAT_ID/accept" -d '{}'
check "usarlo otra vez: resultado" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$REPEAT_ID/outcome" -d '{"effort_after":3,"discomfort_after":3,"attribution":"no"}'
expect "['here']['trials']" 2 "pruebas aquí al repetir"
check "elegir un ajuste desconocido → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins" -d "$(repeat nada)"
check "elegir la comparación → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins" -d "$(repeat no_change)"
check "elegir lo que no se puede aquí → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins" -d "$(repeat "$SECOND")"
check "foco que el ajuste no atiende → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins" -d "$(repeat "$ADJUSTMENT" too_cold)"
check "memoria tras repetir" 200 "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/memory"
expect "['tried'][0]['trials']" 2 "veces probado aquí"

check "este lugar cambió" 204 -X POST "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/reset"
check "cambiar un lugar ajeno → 404" 404 -X POST "${AUTH[@]}" "$BASE/v1/spaces/$OTHER_ID/reset"
check "memoria tras el cambio" 200 "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/memory"
expect "['trials']" 2 "el historial no se borra"
expect "['trials_since_reset']" 0 "pruebas desde el cambio"
expect "['space']['reset_at'] is not None" True "fecha del cambio"
check "registrar tras el cambio" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins" -d "$CHECKIN"
expect "['proposal']['reason']['kind'] != 'tried_here'" True "lo de antes del cambio ya no es de aquí"
check "dejarlo" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$(json "['checkin']['id']")/abandon"

# Cuarto del lugar. Con catalog/room.json se arma con su tamaño, cascarón y un objeto de base;
# siempre lleva un tipo que el catálogo no conoce, que se guarda sin revisar.
ROOM="$(python -c '
import json, os, sys
size, floor, wall, items = {"w": 5, "d": 5}, "oak", "teal", []
if os.path.exists(sys.argv[1]):
    c = json.load(open(sys.argv[1], encoding="utf-8"))
    size, floor, wall = c["size"], c["shell"]["floors"][0], c["shell"]["walls"][0]
    for kind, t in c["types"].items():
        fw, fd = t["footprint"][::-1] if t["facings"][0] % 2 else t["footprint"]
        if t.get("base") and "floor" in t["place"] and fw <= size["w"] and fd <= size["d"]:
            place = {"on": "floor", "x": 0, "y": 0, "rot": t["facings"][0]}
            items.append({"uid": "smoke001", "type": kind, "variant": t["variants"][0], "place": place})
            break
place = {"on": "floor", "x": size["w"] - 1, "y": size["d"] - 1, "rot": 0}
items.append({"uid": "smoke002", "type": "smoke_future", "variant": "x", "place": place})
window = {"wall": "right", "u": 0}
print(json.dumps({"v": 1, "size": size, "shell": {"floor": floor, "wall": wall, "window": window}, "items": items, "pinned": []}))
' "$(dirname "$0")/../apps/api/catalog/room.json")"
ROOM_DUP="$(python -c 'import json, sys; l = json.loads(sys.argv[1]); l["items"].append(l["items"][-1]); print(json.dumps(l))' "$ROOM")"
ROOM_V2="$(python -c 'import json, sys; l = json.loads(sys.argv[1]); l["v"] = 2; print(json.dumps(l))' "$ROOM")"
check "cuarto sin crear → 404" 404 "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/room"
check "crear cuarto" 200 -X PUT "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/room" -d "{\"revision\":0,\"layout\":$ROOM}"
expect "['revision']" 1 "revisión al crear"
check "leer cuarto" 200 "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/room"
expect "['revision']" 1 "revisión leída"
expect "['layout']['items'][-1]['type']" smoke_future "se conserva un tipo desconocido"
check "guardar cuarto" 200 -X PUT "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/room" -d "{\"revision\":1,\"layout\":$ROOM}"
expect "['revision']" 2 "revisión al guardar"
check "revisión vieja → 409" 409 -X PUT "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/room" -d "{\"revision\":1,\"layout\":$ROOM}"
expect "['revision']" 2 "revisión actual en el conflicto"
check "cuarto inválido → 422" 422 -X PUT "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/room" -d "{\"revision\":2,\"layout\":$ROOM_DUP}"
expect "['error']" invalid_layout "código de cuarto inválido"
expect "['problems'][-1].endswith('uid: duplicate')" True "problema del cuarto"
check "cuarto de una app más nueva → 422" 422 -X PUT "${AUTH[@]}" "$BASE/v1/spaces/$SPACE_ID/room" -d "{\"revision\":2,\"layout\":$ROOM_V2}"
expect "['error']" update_app "pide actualizar la app"
check "cuarto de un lugar ajeno → 404" 404 "${AUTH[@]}" "$BASE/v1/spaces/$OTHER_ID/room"
check "guardar en un lugar ajeno → 404" 404 -X PUT "${AUTH[@]}" "$BASE/v1/spaces/$OTHER_ID/room" -d "{\"revision\":0,\"layout\":$ROOM}"

check "varios sin foco → 400" 400 -X POST "${AUTH[@]}" "$BASE/v1/checkins" \
  -d '{"task":"writing","feeling":"drained","effort_before":3,"discomfort_before":3,"observations":[{"stimulus":"voices","response":"yes"},{"stimulus":"too_cold","response":"yes"}]}'
check "sin estímulo claro" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins" \
  -d '{"task":"writing","feeling":"other","effort_before":3,"discomfort_before":2,"observations":[{"stimulus":"voices","response":"unsure"}]}'
expect "['proposal']" None "sin estímulo no hay propuesta"
check "dejarlo" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$(json "['checkin']['id']")/abandon"
# Lo cognitivo: el mismo ciclo, sin preguntar por el entorno. Solo viajan categorías.
INNER='{"task":"writing","feeling":"focus","effort_before":4,"discomfort_before":4,"observations":[{"stimulus":"hard_to_start","response":"yes"}],"focus_stimulus":"hard_to_start"}'
check "registrar algo cognitivo" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins" -d "$INNER"
expect "['checkin']['focus_stimulus']" hard_to_start "el foco cognitivo se guarda"
check "dejar lo cognitivo" 200 -X POST "${AUTH[@]}" "$BASE/v1/checkins/$(json "['checkin']['id']")/abandon"
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
