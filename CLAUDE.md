# Contexto para agentes

- Monorepo de **SpaceEase** (equipo Spy Family, socioformador Specialisterne, North American AI Challenge de ASU). Plan y decisiones en `docs/PLAN.md`; actualizarlo cuando cambie una decisión.
- `apps/mobile`: Expo + TypeScript. Solo módulos compatibles con Expo Go (plan B por QR). Textos en es/en.
- `apps/api`: Rust (Axum, sqlx, ort). Despliega en Railway desde este repo.
- `ml/`: Python, entrenamiento del modelo de audio; el contrato con la API está en `ml/README.md`.
- `nina-col/AiChallengeFront` y `nina-col/AiChallengeBack` son espejos de `apps/mobile` y `apps/api`, y el equipo trabaja en ellos. Sus commits se traen con `scripts/import-team-repos.sh`: uno por uno, con su autor, a una rama `equipo/<front|back>-<fecha>` que se revisa (tipos, lint, pruebas, smoke) antes de mezclarla a main con `--no-ff`; nunca se reescriben ni se descartan. Los espejos se actualizan con `scripts/sync-team-repos.sh` (commit normal, nunca force-push; se detiene si hay commits del equipo sin importar), solo cuando el usuario lo pida.
- Nada de secretos en git: llaves en Railway y EAS.
- Producto: sin diagnósticos ni puntuaciones; los hallazgos de la IA son hipótesis que la persona confirma; "No sé" siempre disponible.
- Diseño, lenguaje, movimiento y medición: seguir `docs/DESIGN.md`. La evidencia detrás está en `docs/research/reports/`.
- API: `scripts/smoke-api.sh [URL]` debe pasar antes de cada push que toque `apps/api` (Postgres local en `localhost:5433`, ver `apps/api/.env.example`).
