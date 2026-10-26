#!/usr/bin/env bash
# Aplica la configuración del servicio `api` en Railway: directorio raíz, healthcheck, reinicios y
# watch paths. Railway ya no acepta railway.toml, así que este script es la fuente de verdad.
# Railway detecta solo el Dockerfile dentro del directorio raíz (apps/api/Dockerfile).
#
# Requiere `railway login`. Uso: scripts/railway-configure.sh
set -euo pipefail

SERVICE_ID="${SERVICE_ID:-08258d77-e29d-486c-bbfc-23b19c0bb23e}"         # spaceease / api
ENVIRONMENT_ID="${ENVIRONMENT_ID:-b64940bb-38e9-4e7e-b69b-644b0335f7a4}" # spaceease / production

railway api '
mutation($sid: String!, $eid: String) {
  serviceInstanceUpdate(serviceId: $sid, environmentId: $eid, input: {
    rootDirectory: "/apps/api"
    watchPatterns: ["/apps/api/**"]
    healthcheckPath: "/health"
    healthcheckTimeout: 120
    restartPolicyType: ON_FAILURE
    restartPolicyMaxRetries: 5
  })
}' --raw-var sid="$SERVICE_ID" --raw-var eid="$ENVIRONMENT_ID" --compact

railway api '
query($sid: String!, $eid: String!) {
  serviceInstance(serviceId: $sid, environmentId: $eid) {
    rootDirectory watchPatterns healthcheckPath healthcheckTimeout restartPolicyType
  }
}' --raw-var sid="$SERVICE_ID" --raw-var eid="$ENVIRONMENT_ID" --compact
