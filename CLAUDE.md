# Contexto para agentes

- Monorepo de **SpaceEase** (equipo Spy Family, socioformador Specialisterne, North American AI Challenge de ASU). Plan y decisiones en `docs/PLAN.md`; actualizarlo cuando cambie una decisión.
- `apps/mobile`: Expo + TypeScript. Solo módulos compatibles con Expo Go (plan B por QR). Textos en es/en.
- `apps/api`: Rust (Axum, sqlx, ort). Despliega en Railway desde este repo.
- `ml/`: Python, entrenamiento del modelo de audio; el contrato con la API está en `ml/README.md`.
- `nina-col/AiChallengeFront` y `nina-col/AiChallengeBack` son espejos de `apps/mobile` y `apps/api`. Se actualizan solo con `scripts/sync-team-repos.sh` (commit normal, nunca force-push) y solo cuando el usuario lo pida.
- Nada de secretos en git: llaves en Railway y EAS.
- Producto: sin diagnósticos ni puntuaciones; los hallazgos de la IA son hipótesis que la persona confirma; "No sé" siempre disponible.
