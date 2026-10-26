# Plan del proyecto — Sensa

> **Equipo:** Spy Family · **Reto:** North American AI Challenge (Arizona State University) · **Socioformador:** Specialisterne
> Última actualización: 26 oct 2026. Este documento es la fuente de verdad: si cambia una decisión, se cambia aquí.

## 1. El reto

Specialisterne promueve la empleabilidad de personas neurodivergentes. Busca una solución innovadora para la parte ejecutiva: que una persona neurodivergente rinda en igualdad de condiciones que una persona neurotípica, en un trabajo de cualquier tipo. Dos condiciones:

- **No puede ser genérica.**
- **Tiene que ser un FMVP** (Functional Minimal Valuable Product): desplegado y usable, de preferencia en TestFlight o Expo. No basta con vender la idea.

## 2. La propuesta

**Sensa** (nombre de trabajo) ayuda a descubrir qué del entorno está dificultando una tarea concreta, propone **un solo ajuste viable** y comprueba si funcionó. Con cada prueba aprende qué le sirve **a esa persona**, para **esa tarea** y en **ese espacio**, en lugar de dar recomendaciones universales.

### Ciclo central (< 2 min hasta el primer ajuste)

1. **Registrar.** Qué siento (me cuesta concentrarme / termino agotado / siento incomodidad / otro), qué tarea hago (lectura, escritura, llamadas, código, reuniones…), en qué espacio, y esfuerzo percibido del 1 al 5.
2. **Descubrir.** Grabar ~10 s de audio y tomar una foto del lugar, revisando cada captura antes de enviarla. La IA devuelve:
   - hasta **3 marcadores sobre la foto**, formulados como pregunta: *"Parece haber un reflejo en la pantalla. ¿Te incomoda al leer?"*
   - **observaciones del audio**: *"Se perciben voces de fondo. ¿Te distraen o puedes ignorarlas?"*
   - 1–3 preguntas breves para lo que no se ve ni se oye (temperatura, movimiento alrededor, parpadeo de luz).

   Cada pregunta se responde **Sí / No / No sé**. Descubrirlo es parte del producto. Si la persona no quiere usar foto o audio, hace solo las preguntas.
3. **Un solo ajuste.** Lo elige nuestro motor personal (sección 3.4) entre los que la persona dijo que puede hacer. Va etiquetado:
   - **Lo puedo hacer yo:** girar la pantalla, alejarse del pasillo, reducir estímulos visibles, probar otro lugar para esa tarea.
   - **Lo necesito pedir:** la app redacta la solicitud de ajuste para jefe o RH **sin revelar diagnóstico**. Esto conecta directo con la misión de empleabilidad de Specialisterne.
4. **Comprobar.** Un recordatorio local tras el bloque de trabajo ("¿Cómo te fue?") repite la valoración del 1 al 5. Si bajó el esfuerzo, el ajuste se guarda en **Mis ajustes**: qué funcionó, para qué tarea y en qué espacio.
5. **Aprender.** Tarjetas basadas en el historial de la persona:
   > *"En este escritorio te cuesta leer documentos cuando hay conversaciones cerca. Probaste una ubicación más alejada y reportaste menor esfuerzo. ¿Guardamos ese ajuste para tareas de lectura?"*

### Principios no negociables

- Nada de diagnósticos ni "puntuación de neurodivergencia". Los hallazgos de la IA son **hipótesis que la persona confirma**.
- "No sé" disponible en todas las preguntas.
- Lenguaje llano, una acción por pantalla, navegación predecible.
- Sin rachas, sin presión de tiempo, todo se puede saltar.
- Respeta *Reducir movimiento* y *Dynamic Type*; paleta de bajo estímulo.

## 3. Inteligencia artificial

### 3.1 Arquitectura híbrida

| Capa | Qué hace | Tecnología |
|---|---|---|
| Visión y razonamiento | Detecta reflejos, iluminación, saturación visual y ubicación; devuelve ≤ 3 marcadores (x, y normalizados) en JSON | Claude Sonnet 5.5 (API) |
| Audio | Nivel en dB, constante vs. intermitente, eventos (voces, teclado, zumbido de clima, tráfico, música…) | Procesamiento de señal propio + **clasificador de audio entrenado por nosotros**, en CPU dentro de la API |
| Decisión | Elige el único ajuste a proponer | **Motor personal propio** (bandit contextual) |
| Redacción | Redacta el ajuste concreto, las tarjetas y la solicitud a la empresa | Claude Haiku 5.5 |

La idea central del pitch: **el modelo de lenguaje percibe y redacta, pero qué ajuste proponer lo decide un modelo que aprende de la evidencia de cada persona.** Por eso no es genérico, y se puede medir y explicar ("te funcionó 2 de 2 veces leyendo").

Gemini queda como proveedor alternativo detrás de la variable `AI_PROVIDER`, por si los créditos del challenge resultan útiles o Claude falla.

### 3.2 Por qué no entrenamos un modelo de visión propio

- Con 8 GB de VRAM (RTX 5070 Laptop) no da para entrenar, en días, algo que compita con Claude o Gemini detectando reflejos o saturación visual.
- Railway no tiene GPU: servirlo dependería de que una laptop esté prendida durante la demo.

### 3.3 Modelo de audio propio (track de Quique, en paralelo)

Una cabeza de clasificación entrenada sobre un modelo preentrenado en AudioSet, con datos públicos y **grabaciones del equipo en oficinas reales**. Se exporta a ONNX y corre en CPU dentro de la API (< 100 ms por audio). Nos da una historia real de "entrenamos nuestro modelo", con métricas, sin riesgo en la demo. El contrato y la receta están en [`ml/README.md`](../ml/README.md).

### 3.4 Motor personal (el diferenciador)

- **Catálogo** curado de ~30 ajustes. Cada uno indica: estímulo que atiende, tareas donde aplica, si es propio o se pide a la empresa, y esfuerzo de implementarlo.
- **Contexto** de cada prueba: estímulo confirmado × tipo de tarea × espacio.
- **Modelo:** para cada persona y ajuste, una distribución Beta(α, β) de "probabilidad de que me ayude" en ese contexto.
  - Si hay pocos datos, se usa el siguiente nivel de detalle: persona+estímulo+tarea → persona+estímulo → prior global (catálogo + datos agregados de todos).
- **Elección:** Thompson sampling entre los ajustes viables (filtrados por lo que la persona dijo que puede modificar). Así explora sin dejar de proponer lo que ya le funcionó.
- **Recompensa:** 1 si el esfuerzo bajó al menos un punto, 0 si no; "no lo probé" no actualiza.
- **Explicación:** cada propuesta muestra por qué ("te funcionó 2 de 2 veces leyendo en este escritorio").

### 3.5 Privacidad

- La foto y el audio se analizan y **se descartan**: el servidor solo guarda lo derivado (marcadores, etiquetas, dB).
- La foto se queda en el teléfono para dibujar los marcadores. Importa porque en una oficina salen compañeros.
- Cuenta anónima por dispositivo y botón **Borrar mis datos**.

### 3.6 Costo

Cada escaneo usa unos pocos miles de tokens (foto reducida a ~1024 px + instrucciones + JSON corto). Con el crédito disponible (~200 USD) alcanza para miles de escaneos. Las tarifas exactas se confirman al integrar la API; habrá límite diario por usuario para evitar sorpresas.

## 4. Arquitectura técnica

```
App Expo (iOS / TestFlight)  ──HTTPS──►  API Rust/Axum (Railway, Docker)  ──►  Postgres (Railway)
  cámara, audio,                            ├─ Claude: visión y redacción
  notificaciones locales                    ├─ audio: señal + modelo ONNX propio
  EAS Build + EAS Update                    └─ motor personal
```

### 4.1 App — `apps/mobile`

- Expo SDK más reciente, TypeScript, Expo Router.
- `expo-camera` / `expo-image-picker`, `expo-audio` (WAV 16 kHz mono en iOS), `expo-notifications` (solo locales), `expo-secure-store`.
- TanStack Query para datos del servidor; i18n **es/en** (los jueces de ASU probablemente evalúan en inglés).
- **Solo módulos compatibles con Expo Go**, para que el plan B (QR) siempre funcione.

### 4.2 API — `apps/api` (Rust)

**Por qué Rust:** respuestas en milisegundos, binario pequeño, poca memoria en Railway (se cobra por uso), arranque rápido y tipos estrictos en todo el contrato. **Por qué no C++:** mismo rendimiento, pero mucho más lento de escribir y sin garantías de memoria; no aporta nada que Rust no dé.

| Pieza | Crate |
|---|---|
| Servidor HTTP | `axum` + `tokio` + `tower-http` (CORS, límites de tamaño, trazas) |
| Base de datos | `sqlx` (Postgres, migraciones) |
| Modelo de audio | `ort` (ONNX Runtime) |
| Decodificar audio | `symphonia` (WAV de iOS; AAC/M4A de Android) |
| Claude API | cliente propio con `reqwest` + `serde` (no hay SDK oficial de Rust) |
| Auth | `jsonwebtoken` |
| Logs | `tracing` |

Docker multi-stage con `cargo-chef` para que las builds en Railway reutilicen dependencias compiladas.

### 4.3 Dónde se va el tiempo (y cómo lo bajamos)

El lenguaje del backend no es lo que hará sentir lenta la app; lo es la llamada a la IA. Por eso el flujo está pensado para que la espera no se note:

| Paso | Tiempo típico (estimado, se mide en iteración 2) | Cómo lo bajamos |
|---|---|---|
| Subir audio | < 1 s | WAV de 10 s a 16 kHz mono ≈ 320 KB |
| Analizar audio | < 100 ms | Rust + ONNX en CPU. **Se graba primero el audio**: se procesa mientras la persona toma la foto |
| Subir foto | < 1 s | Se reduce en el teléfono a ~1024 px JPEG (≈ 150 KB) |
| Visión con Claude | ~4–12 s | Foto reducida, salida JSON corta, pantalla de progreso por pasos; comparar Sonnet vs. Haiku con nuestro set de prueba |
| Resto de la API | milisegundos | Rust |

### 4.4 Endpoints (v1)

| Método y ruta | Qué hace |
|---|---|
| `POST /v1/auth/device` | Cuenta anónima por dispositivo → JWT |
| `GET/POST /v1/spaces` | Espacios de trabajo de la persona |
| `POST /v1/checkins` | Dificultad, tarea, espacio, esfuerzo inicial |
| `POST /v1/checkins/{id}/audio` | Audio 10 s → observaciones (rápido) |
| `POST /v1/checkins/{id}/photo` | Foto → hasta 3 marcadores (usa el audio como contexto) |
| `POST /v1/checkins/{id}/answers` | Sí / No / No sé + qué puedo modificar → **un** ajuste |
| `POST /v1/checkins/{id}/outcome` | Esfuerzo final → resultado + tarjeta de aprendizaje |
| `GET /v1/playbook` | Mis ajustes que funcionan, por tarea × espacio |
| `GET /v1/insights` | Tarjetas de aprendizaje |
| `POST /v1/requests` | Solicitud de ajuste para la empresa |
| `DELETE /v1/me` | Borrar todos mis datos |
| `GET /health` | Salud del servicio |

### 4.5 Datos

`users`, `spaces`, `checkins`, `observations` (origen foto/audio/pregunta, estímulo, respuesta), `adjustments` (catálogo), `trials` (ajuste probado + contexto + resultado).

## 5. Repos y despliegue

### 5.1 Repos

| Repo | Para qué |
|---|---|
| `Quique2/AiChallenge` (privado) | **Monorepo de trabajo.** Aquí se edita todo y desde aquí despliega Railway |
| `nina-col/AiChallengeFront` | Espejo de `apps/mobile`, para que el equipo lea el código de la app |
| `nina-col/AiChallengeBack` | Espejo de `apps/api`, para que el equipo lea el código del backend |

Los espejos se actualizan con `scripts/sync-team-repos.sh` al cerrar cada iteración: un commit normal `sync monorepo@<sha>` con la lista de cambios, **sin force-push**, así no se pierde su historial. Si alguien hace commit directo en un espejo, avisar para integrarlo en el monorepo antes del siguiente sync (si no, se sobrescribe).

### 5.2 Railway

- Un proyecto con el servicio `api` (root `apps/api`, se redespliega solo si cambia `apps/api/**`) y un Postgres.
- Variables: `DATABASE_URL`, `JWT_SECRET`, `ANTHROPIC_API_KEY`, `AI_PROVIDER`, `GEMINI_API_KEY` (opcional).
- Las llaves viven solo en Railway; nunca en git.

### 5.3 TestFlight (cuenta Apple Developer de Quique)

1. Crear la app en App Store Connect. **Decidir antes el nombre público y el bundle id**: el nombre debe ser único en la App Store y el bundle id no se puede cambiar después.
2. Crear una App Store Connect API Key y registrarla en EAS (`eas credentials`) para que las builds no pidan login cada vez.
3. `eas build -p ios --profile production` (compila en la nube; no hace falta Mac) → `eas submit -p ios` → TestFlight.
4. **Probadores internos** (hasta 100, sin revisión) desde el día 1.
5. **Grupo externo con enlace público** para jueces y Specialisterne: requiere *Beta App Review* (normalmente < 24 h). Se manda al cerrar la iteración 1.
6. Cambios de JS/UI se publican con **EAS Update** directo a la build de TestFlight, sin recompilar. Solo cambios nativos requieren build nueva.
7. **Plan B siempre listo:** la misma app abre en Expo Go con QR.

## 6. Iteraciones

Cada iteración termina con: deploy en Railway + build o update en TestFlight + sync a los espejos.

| # | Días | Entregable |
|---|---|---|
| 0 | 1 | **Cimientos.** Monorepo, app "hola" en TestFlight interno, API Rust `/health` + Postgres en Railway, sync a espejos funcionando |
| 1 | 2–3 | **Ciclo completo sin IA:** inicio, espacios, registrar, preguntas, ajuste por reglas, comprobar, Mis ajustes. **Esto ya es un FMVP.** Se abre el enlace público de TestFlight |
| 2 | 4–5 | **Escaneo multimodal:** audio + foto con revisión, Claude visión, audio propio, marcadores sobre la foto, confirmar hipótesis |
| 3 | 6 | **Motor personal**, tarjetas de aprendizaje, "¿por qué esta sugerencia?", solicitud a la empresa |
| 4 | 7 | **Pulido:** accesibilidad, inglés, errores y sin conexión, borrar datos, usuario demo con historial sembrado |
| 5 | 8–9 | **Validación** con 3–5 personas (idealmente vía Specialisterne) y ajustes según su feedback |
| 6 | 10 | **Pitch:** guion de demo, métricas reales de uso, video de respaldo por si falla la demo en vivo |
| ‖ | 2–5 | **Modelo de audio** (Quique, GPU) → ONNX; se conecta en la iteración 2–3 |

### Checklist de la iteración 0

- [ ] Quique: `eas login` y `railway login` en su terminal (piden navegador)
- [ ] Instalar Rust con `rustup` (Visual Studio Build Tools 2022 ya está)
- [ ] Mover el monorepo fuera de OneDrive (ver Decisiones pendientes)
- [ ] `apps/mobile`: proyecto Expo, bundle id, `eas.json` (development / preview / production), canal de EAS Update
- [ ] `apps/api`: Axum con `/health`, migraciones sqlx, Dockerfile, `railway.toml`
- [ ] Railway: proyecto + Postgres + servicio `api` conectado a GitHub
- [ ] App Store Connect: crear la app y la API Key para EAS
- [ ] Primera build iOS → TestFlight interno
- [ ] Primer sync a los espejos

## 7. Demo de 2 minutos

1. "Estoy leyendo y me cuesta concentrarme."
2. Audio con voces de fondo → foto del escritorio junto a una ventana.
3. Marcadores: reflejo en la pantalla, luz directa de la ventana; en audio, voces.
4. Confirma el reflejo y que puede mover la pantalla → ajuste: girar la pantalla, con el porqué.
5. Comprobación: esfuerzo 4 → 2 → se guarda en Mis ajustes para lectura en ese escritorio.
6. Tarjeta de aprendizaje con su historial.
7. Cierre: solicitud de un espacio tranquilo para llamadas, redactada para RH sin revelar diagnóstico.

## 8. Riesgos

| Riesgo | Mitigación |
|---|---|
| Cola o cuota de builds gratis de EAS | Compilar temprano; iterar por EAS Update |
| Revisión de Apple para el enlace público | Mandarla al cerrar la iteración 1, no al final |
| Latencia de la IA | Audio primero, progreso por pasos; si falla, se sigue con las preguntas |
| Coordenadas aproximadas de Claude | Marcadores tipo pin con opción "no es aquí"; Gemini si hace falta más precisión |
| Builds de Rust lentas en Railway | `cargo-chef` para cachear dependencias |
| Parecer genérico | Mostrar el aprendizaje por persona × tarea × espacio y la solicitud a la empresa |
| Demo en vivo falla | Usuario demo sembrado + video de respaldo |

## 9. Decisiones pendientes

- **Nombre público de la app y bundle id**, antes de la primera build.
- **Mover el monorepo fuera de OneDrive** (por ejemplo a `C:\dev\AIChallenge`): `node_modules` y `target/` son decenas de miles de archivos y OneDrive bloquea archivos mientras sincroniza.
- **Contacto en Specialisterne** para las pruebas con usuarios de la iteración 5.
