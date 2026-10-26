# SpaceEase — Spy Family × Specialisterne

App que ayuda a personas neurodivergentes a descubrir qué del entorno les dificulta una tarea, probar **un solo ajuste viable** y guardar lo que les funciona para cada tarea y espacio. North American AI Challenge (Arizona State University).

**Plan completo y decisiones:** [docs/PLAN.md](docs/PLAN.md)

## Estructura

| Carpeta | Qué hay | Espejo para el equipo |
|---|---|---|
| `apps/mobile` | App Expo (iOS vía TestFlight; Expo Go como plan B) | [nina-col/AiChallengeFront](https://github.com/nina-col/AiChallengeFront) |
| `apps/api` | API en Rust (Axum) desplegada en Railway | [nina-col/AiChallengeBack](https://github.com/nina-col/AiChallengeBack) |
| `ml` | Entrenamiento del modelo de audio propio | — |
| `docs` | Plan, guion de demo, notas del pitch | — |
| `scripts` | Utilidades del monorepo | — |

## Espejos del equipo

Este monorepo es donde se trabaja y desde donde despliega Railway. Los repos de `nina-col` se actualizan al cerrar cada iteración:

```bash
scripts/sync-team-repos.sh          # ambos
scripts/sync-team-repos.sh front    # solo la app
scripts/sync-team-repos.sh back     # solo la API
```

Cada sync es un commit normal (`sync monorepo@<sha>` + lista de cambios), nunca un force-push. Si alguien hace commit directo en un espejo, hay que integrarlo aquí antes del siguiente sync o se sobrescribe.
