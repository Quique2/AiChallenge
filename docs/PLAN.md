# Plan del proyecto — SpaceEase

> **Equipo:** Spy Family · **Reto:** North American AI Challenge (Arizona State University) · **Socioformador:** Specialisterne
> Última actualización: 26 oct 2026. Este documento es la fuente de verdad: si cambia una decisión, se cambia aquí.

## 1. El reto

Specialisterne promueve la empleabilidad de personas neurodivergentes. Busca una solución innovadora para la parte ejecutiva: que una persona neurodivergente rinda en igualdad de condiciones que una persona neurotípica, en un trabajo de cualquier tipo. Dos condiciones:

- **No puede ser genérica.**
- **Tiene que ser un FMVP** (Functional Minimal Valuable Product): desplegado y usable, de preferencia en TestFlight o Expo. No basta con vender la idea.

### Lo que dice la evidencia (investigación del 26 oct 2026)

Informe completo, con fuentes y nivel de evidencia: [`docs/research/reports/`](research/reports/Ajustes%20sensoriales%20laborales%20y%20neurodivergencia.md). Notas por tema en `docs/research/research_notes/`.

- **El problema es real.** Las diferencias sensoriales son casi universales en adultos autistas y comunes en TDAH. En oficinas, las voces ajenas y la densidad de gente encabezan la lista; luego la luz y la temperatura.
- **Lo que mueve la aguja es el control.** En 206 personas autistas que trabajan en oficina, las barreras sensoriales se asocian con menos satisfacción, desempeño y autoeficacia. El mediador es el control percibido sobre el entorno, y eso es lo que la app devuelve.
- **La eficacia de los ajustes no está probada.** La revisión principal no encontró ningún estudio que midiera si un ajuste sensorial funciona. SpaceEase puede generar esa evidencia persona por persona, si mide con honestidad.
- **El hueco es pedir.** En EE. UU., el 70 % no sabe a qué ajustes tiene derecho y el 70 % teme revelar su condición. En los tres países se puede empezar una solicitud describiendo la tarea y la barrera, sin diagnóstico.
- **El riesgo está en el micrófono, la cámara y el empleador**, no en el algoritmo.

Decisiones que ya están en el producto: medida principal de molestia del entorno, resultado relativo a la mejora típica de cada persona, comparación transparente "sin cambios", exploración mínima, consentimiento expreso, solicitud en cinco partes sin diagnóstico, cero acceso del empleador, sin rachas y reglas de diseño cognitivamente accesible ([`docs/DESIGN.md`](DESIGN.md)).

## 2. La propuesta

**SpaceEase** (elegido por el equipo) ayuda a descubrir qué del entorno está dificultando una tarea concreta, propone **un solo ajuste viable** y comprueba si funcionó. Con cada prueba aprende qué le sirve **a esa persona**, para **esa tarea** y en **ese espacio**, en lugar de dar recomendaciones universales.

### Ciclo central

1. **Registrar.** Qué tarea hace, cómo se siente con ella, dónde está (se omite si solo tiene un lugar), cuánto le molesta el entorno y cuánto esfuerzo le cuesta. Cada escala tiene 5 botones con palabras.
2. **Descubrir.** Una pantalla por dominio (sonido, luz, lo que ves, el cuerpo), con "Nada de esto" y "No sé". Si marca varias cosas, elige la que más le afecta ahora.
   - *Iteración 2:* foto y 10 s de audio como apoyo. La IA propone hipótesis ("Posible reflejo en la pantalla. ¿Te molesta?") y solo cuenta lo que la persona confirma.
3. **Un solo ajuste.** Lo elige el motor personal (3.4), con su motivo. Hay botones para "Dame otra idea" y "No puedo hacerlo aquí". Si ya no quedan ideas propias, propone algo para pedir a la empresa. De vez en cuando propone **"Esta vez no cambies nada"** para comparar, y se puede rechazar.
4. **Comprobar.** Si la persona lo pide, un aviso silencioso a los 25 o 50 minutos. Repite la molestia y el esfuerzo y pregunta "¿Crees que el ajuste ayudó?". Cuenta como ayuda si mejoró **más que su mejora típica**.
5. **Aprender.** "Lo que me sirve" guarda lo que ayudó por tarea y lugar, con cuántas veces se probó ("ayudó 2 de 3 veces; todavía no es seguro"). Desde ahí se arma una **solicitud a la empresa** en cinco partes, sin diagnóstico, que la persona comparte si quiere.

### Principios no negociables

- Nada de diagnósticos ni "puntuación de neurodivergencia". El sujeto de las frases es el entorno, no la persona.
- Los hallazgos de la IA son **hipótesis que la persona confirma**.
- "No sé" disponible en todas las preguntas. Todo se puede saltar, y no hay rachas ni presión de tiempo.
- El empleador no tiene acceso a nada.
- Reglas de lenguaje, color, movimiento y medición en [`docs/DESIGN.md`](DESIGN.md).

## 3. Inteligencia artificial

### 3.1 Arquitectura híbrida

| Capa | Qué hace | Tecnología | Estado |
|---|---|---|---|
| Decisión | Elige el único ajuste a proponer y aprende de cada resultado | **Motor personal propio** (Thompson sampling, `apps/api/src/engine.rs`) | Hecho |
| Visión | Hipótesis sobre reflejos, luz y saturación visual: ≤ 3 marcadores en JSON | Claude Opus 5.5 (API, salida estructurada y respaldos del servidor), con caras pixeladas en el teléfono | Hecho |
| Audio | Voces, ruido constante y ruidos repentinos | **En el teléfono** (`audio-features.ts`); el audio se borra y nunca se envía. El modelo propio se entrena sobre rasgos no reconstruibles | Heurística hecha; modelo en curso |
| Redacción | Pule la solicitud a la empresa y las tarjetas de aprendizaje | Claude Haiku 5.5 (hoy: plantillas) | Iteración 3 |

La idea central del pitch: **el modelo de lenguaje percibe y redacta, pero qué ajuste proponer lo decide un modelo que aprende de la evidencia de cada persona.** Por eso no es genérico, y se puede medir y explicar ("ayudó 2 de 3 veces leyendo en este escritorio").

Gemini queda como proveedor alternativo detrás de la variable `AI_PROVIDER`, por si los créditos del challenge resultan útiles o Claude falla.

### 3.2 Por qué no entrenamos un modelo de visión propio

- Con 8 GB de VRAM (RTX 5070 Laptop) no da para entrenar, en días, algo que compita con Claude o Gemini detectando reflejos o saturación visual.
- Railway no tiene GPU: servirlo dependería de que una laptop esté prendida durante la demo.

### 3.3 Modelo de audio propio (track de Quique, en paralelo)

Una cabeza de clasificación entrenada sobre un modelo preentrenado en AudioSet, con datos públicos y **grabaciones del equipo en oficinas reales**. Grabar conversaciones de colegas es el caso prohibido en los tres países, así que el audio se procesa en el teléfono y nunca se envía la forma de onda. Por eso el modelo se entrena sobre **rasgos que no permiten reconstruir la voz**: niveles por banda y por segundo. Sigue dando una historia real de "entrenamos nuestro modelo", con métricas. El contrato está en [`ml/README.md`](../ml/README.md) y se ajusta en la iteración 2.

### 3.4 Motor personal (el diferenciador)

- **Catálogo** versionado (`apps/api/catalog/catalog.json`): 13 estímulos en 4 dominios y 29 ajustes en español e inglés. Cada ajuste dice qué estímulos atiende, si es propio o se pide, y para qué tareas no aplica. Las pruebas garantizan que cada estímulo tenga un ajuste propio para cada tarea.
- **Contexto** de cada prueba: estímulo × tarea × lugar.
- **Modelo:** una Beta(α, β) por ajuste con un prior débil del catálogo (α + β = 2). Se suma la evidencia de la persona en ese contexto (peso 1), la de la persona en otros contextos (peso 0.5) y la de todas las personas (peso 0.1, con un tope equivalente a 3 pruebas).
- **Elección:** Thompson sampling, más un 10 % de exploración al azar. Lo que falló dos veces en un contexto sin ningún éxito deja de proponerse mientras haya otras opciones.
- **Recompensa relativa:** "ayudó" significa que la molestia del entorno bajó **más que la mejora típica de esa persona**, calculada con sus últimos 20 registros y ajustada hacia 0.5 cuando hay pocos. Si hay al menos 2 comparaciones "sin cambios", se usan solo esas. Si la persona dice que no ayudó, no ayudó.
- **Explicación al estilo Self-E:** primer intento, "probemos algo nuevo para aprender", o "ayudó X de Y veces aquí". Desde 3 pruebas se da una frase tentativa y desde 5 una más firme.

### 3.5 Privacidad

- Cuenta anónima: el servidor guarda solo el SHA-256 de la llave del dispositivo.
- **Consentimiento expreso**, sin marcar de antemano, versionado y guardado con fecha. El aviso está en `GET /privacy` (LFPDPPP art. 8 y Apple 5.1.1).
- El botón **Borrar todos mis datos** borra en cascada en el servidor y limpia el teléfono.
- Cero acceso del empleador. Nada sale de la app salvo lo que la persona comparte.
- **Foto y sonido** (iteración 2): son opcionales y cada uno tiene su propio consentimiento, apagado por defecto y revocable en Ajustes.
  - **Sonido:** se analiza y se borra en el teléfono; nunca se envía.
  - **Foto:** un módulo nativo (Apple Vision + Core Image) pixela caras y siluetas antes de enviarla, y la persona ve exactamente lo que se enviará. La API la tiene solo en memoria y no la guarda ni la registra.
  - **Instrucciones a Claude:** no describir personas, emociones ni salud, y formular cada hallazgo como hipótesis. Solo lo que la persona confirma cuenta.
  - **En Expo Go,** sin el módulo nativo, la foto no sale del teléfono.
  - **Anthropic:** borra las entradas de la API en 30 días y no entrena con ellas por defecto.

### 3.6 Costo

Medido el 26 oct: un escaneo con Claude Opus 5.5 ($4 / $20 por millón de tokens de entrada y de salida) tarda 4–10 s y cuesta del orden de 3 centavos de dólar. Con ~200 USD alcanza para unos miles de escaneos. Hay un límite de 30 escaneos al día por persona y se registran los tokens de cada uno (tabla `scans`, sin imágenes). Para bajar a la mitad el costo y la latencia, basta poner `CLAUDE_VISION_MODEL=claude-sonnet-5-5` en Railway.

## 4. Arquitectura técnica

```
App Expo (iOS / TestFlight)  ──HTTPS──►  API Rust/Axum (Railway, Docker)  ──►  Postgres (Railway)
  cámara, audio,                            ├─ Claude: visión y redacción
  notificaciones locales                    ├─ audio: señal + modelo ONNX propio
  EAS Build + EAS Update                    └─ motor personal
```

### 4.1 App — `apps/mobile`

- Expo SDK 58, TypeScript, Expo Router con pestañas nativas (`expo-router/native-tabs`) y encabezados nativos.
- `expo-secure-store` (llave del dispositivo), `@react-native-async-storage/async-storage` (preferencias), `expo-notifications` (solo avisos locales), `expo-haptics` (apagado por defecto), `expo-symbols` (SF Symbols), TanStack Query.
- Textos en **es/en** (`src/i18n/`), según el idioma del teléfono o el que elija la persona.
- Iteración 2: `expo-camera`, `expo-audio`, `expo-image-manipulator`, `expo-file-system` y el módulo local `modules/privacy-blur` (Swift). Este último no existe en Expo Go: ahí funciona todo menos enviar la foto.

### 4.2 API — `apps/api` (Rust)

**Por qué Rust:** respuestas en milisegundos, binario pequeño, poca memoria en Railway (se cobra por uso), arranque rápido y tipos estrictos en todo el contrato. **Por qué no C++:** mismo rendimiento, pero mucho más lento de escribir y sin garantías de memoria; no aporta nada que Rust no dé.

| Pieza | Crate |
|---|---|
| Servidor HTTP | `axum` + `tokio` + `tower-http` (CORS, límites de tamaño, trazas) |
| Base de datos | `sqlx` 0.9 (Postgres 18, migraciones al arrancar) |
| Motor personal | `rand` + `rand_distr` (Beta) |
| Auth | Llave del dispositivo → SHA-256 (`sha2`); sin contraseñas ni JWT |
| Claude API | `src/claude.rs`: HTTP con `reqwest` (no hay SDK oficial de Rust), salida estructurada (`output_config.format`) y `fallbacks: "default"` |
| Logs | `tracing` |

Docker multi-stage con `cargo-chef` para que las builds en Railway reutilicen dependencias compiladas. El catálogo se valida al arrancar: si está roto, el healthcheck nunca pasa y no se despliega.

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
| `POST /v1/auth/device` | Crea la cuenta anónima (requiere `consent_version`) o confirma que existe |
| `GET/PATCH/DELETE /v1/me` | Idioma y borrar todos los datos |
| `GET/POST /v1/spaces`, `DELETE /v1/spaces/{id}` | Lugares de trabajo |
| `GET /v1/catalog?locale=` | Tareas, sensaciones, dominios, estímulos y ajustes |
| `POST /v1/checkins` | Registra respuestas y devuelve **una** sugerencia |
| `POST /v1/checkins/{id}/decline` | "Otra idea" o "no puedo aquí" → siguiente sugerencia |
| `POST /v1/checkins/{id}/accept` | Empieza la prueba (con o sin recordatorio) |
| `POST /v1/checkins/{id}/outcome` | Molestia, esfuerzo y "¿ayudó?" → resultado relativo |
| `POST /v1/checkins/{id}/abandon`, `GET /v1/checkins[?status=]`, `GET /v1/checkins/{id}` | Dejarlo e historial |
| `GET /v1/playbook` | Lo que me sirve, por tarea × lugar × estímulo |
| `GET /v1/progress` | Pruebas terminadas y ajustes ya probados, sea cual sea el resultado ("Tu escritorio") |
| `POST /v1/scan/photo` | JPEG ya pixelado + tarea + pistas del audio → hasta 3 hipótesis con punto y pregunta (503 sin llave, 429 al pasar el límite diario) |
| `GET /privacy` | Aviso de privacidad (es/en) |
| `GET /health` | Salud del servicio, versión y commit |

Prueba de punta a punta: `scripts/smoke-api.sh [URL]` (27 comprobaciones; crea y borra una cuenta desechable).

### 4.5 Datos

`users` (hash de la llave, idioma, consentimiento), `spaces`, `checkins` (tarea, sensación, molestia y esfuerzo antes y después, estímulo foco, ajuste, ideas descartadas, mejora, mejora típica, opinión, resultado), `observations` (estímulo, respuesta y origen: pregunta, foto o audio), `space_blocks` (lo que no se puede hacer en cada lugar) y `scans` (modelo y tokens de cada análisis, sin imagen).

## 5. Repos y despliegue

### 5.1 Repos

| Repo | Para qué |
|---|---|
| `Quique2/AiChallenge` (privado) | **Monorepo de trabajo.** Todo se integra aquí y desde aquí despliegan Railway y EAS |
| `nina-col/AiChallengeFront` | Espejo de `apps/mobile`; el equipo trabaja aquí en la app |
| `nina-col/AiChallengeBack` | Espejo de `apps/api`; el equipo trabaja aquí en el backend |

El equipo trabaja en los espejos y el monorepo integra sus cambios sin cambiar la app de golpe (decisión de Quique, 27 oct):

1. **Importar:** `scripts/import-team-repos.sh` trae cada commit del equipo hecho después del último sync, uno por uno y con su autor, a una rama `equipo/<front|back>-<fecha>`. Cada commit queda marcado con `Mirror-Commit: <repo>@<sha>` y nunca se importa dos veces. Si el monorepo cambió lo mismo, se detiene en esa rama para resolverlo a mano.
2. **Revisar y mezclar:** tipos, lint y pruebas (y `scripts/smoke-api.sh` si toca la API); después `git merge --no-ff` a main. Mezclar cambios de `apps/api` despliega en Railway.
3. **Sincronizar:** `scripts/sync-team-repos.sh` publica el monorepo en los espejos con un commit normal `sync monorepo@<sha>`, **sin force-push**. Se detiene si un espejo tiene commits del equipo que todavía no están en lo que se publica, así nunca sobrescribe su trabajo.

### 5.2 Railway

- Proyecto **spaceease**: servicio `api` (Rust, se despliega solo al hacer push a `main`) + Postgres 18 (solo accesible por la red privada de Railway).
- URL pública de la API: `https://api-production-a0b6.up.railway.app` (`/health` para revisar que está viva).
- La configuración del servicio (root `apps/api`, healthcheck, reinicios, redespliegue solo si cambia `apps/api/**`) se aplica con `scripts/railway-configure.sh`. Railway ya no acepta `railway.toml`.
- Variables: `DATABASE_URL` (referencia a Postgres) y `PORT=8080` hoy; después `JWT_SECRET`, `ANTHROPIC_API_KEY`, `AI_PROVIDER`, `GEMINI_API_KEY` (opcional).
- Las llaves viven solo en Railway; nunca en git.

### 5.3 TestFlight (cuenta Apple Developer de Quique)

1. Nombre **SpaceEase**, bundle id `com.spyfamily.spaceease` (ya en `app.json`; no se puede cambiar después de la primera build). Proyecto EAS: `@quiqueexpo-2/spaceease`.
2. Hecho el 26 oct: la app existe en App Store Connect (ASC App ID `6827277889`, ya en `eas.json`) y la build 1.0.0 (1) se subió a TestFlight. EAS guarda los certificados y una API Key de App Store Connect, así que no vuelve a pedir el Apple ID.
3. Builds nativas nuevas, desde `apps/mobile`: `eas build -p ios --profile production --auto-submit` (compila en la nube; no hace falta Mac). En Windows `npx testflight` falla con `spawn npx ENOENT`; este comando hace lo mismo.
4. **Probadores internos** (hasta 100, sin revisión) desde el día 1.
5. **Grupo externo con enlace público** para jueces y Specialisterne: requiere *Beta App Review* (normalmente < 24 h). Se manda al cerrar la iteración 1.
6. Cambios de JS/UI se publican con **EAS Update** directo a la build de TestFlight, sin recompilar. Solo cambios nativos requieren build nueva.
7. **Plan B siempre listo:** la misma app abre en Expo Go con QR.

## 6. Iteraciones

Cada iteración termina con: deploy en Railway + build o update en TestFlight + sync a los espejos.

| # | Estado | Entregable |
|---|---|---|
| 0 | ✅ 26 oct | Monorepo, API Rust + Postgres en Railway, app en TestFlight (1.0.0) y sync a los espejos |
| 1 | ✅ 26 oct | **Ciclo completo sin IA (FMVP)** con la investigación aplicada: registrar, descubrir, sugerencia con motivo, comparación, recordatorio, resultado relativo, Lo que me sirve, solicitud a la empresa, es/en y accesibilidad. App 1.1.0 + API 0.2.0 |
| 2 | ✅ 26 oct | **Escaneo con foto y sonido:** consentimientos aparte, audio en el teléfono, foto pixelada en el teléfono y Claude Opus 5.5 con hipótesis que la persona confirma. App 1.2.0 + API 0.3.0 |
| 3 | ✅ 26 oct | **Experiencia y retención sin presión:** arreglos del permiso del micrófono y de los botones fuera de la pantalla; "Tu escritorio" (un objeto por cada prueba terminada, haya ayudado o no, que nunca se pierde); tres niveles de movimiento; sonidos suaves opcionales; resumen semanal opcional; plan "si…, entonces…". App 1.3.0 + API 0.4.0 |
| 4 | ✅ 29 oct | **Cuarto isométrico y memoria por lugar** (sección 10): memoria por lugar en el motor, "Lo que sé de este lugar", "Usarlo otra vez", cuarto decorable por lugar con editor accesible y el castor en pixel art. App 1.4.0 + API 0.5.0 |
| 4.1 | ✅ 30 oct | **Animaciones del cuarto:** entrada, llegada de lo ganado, mover, girar, guardar y reposo por nivel de movimiento; arrastre opcional en el editor; el cuarto en Hoy, resultado, Listo, semana y Ajustes; integración de `expo-speech` y los cambios de Magda en una build. App 1.5.0 + API 0.5.1 |
| 4.2 | | **Lo que pidió la socioformadora y más arte:** ruta cognitiva con el mismo ciclo de aprendizaje (empezar, ordenar, cambios, preocupaciones, instrucciones poco claras); "Mi energía"; "Estrategias"; molestias y ajustes nuevos; Pausa Zen como menú de minijuegos con Pintar por números y Decorar; íconos de pixel art en lugar de emoji y menos texto. App 1.6.0 + API 0.6.0 |
| 5 | | Redacción con Claude Haiku 5.5 (solicitud y tarjetas), "¿qué puede pedirte tu empresa?" por país y tarjetas de aprendizaje |
| 6 | | Usuario demo con historial sembrado, revisión de accesibilidad con VoiceOver y texto grande, y enlace público de TestFlight |
| 7 | | **Validación** con 3–5 personas, idealmente vía Specialisterne y con co-diseño pagado |
| 8 | | **Pitch:** guion de demo, métricas reales, limitaciones declaradas (tabla del informe) y video de respaldo |
| ‖ | | **Modelo de audio** (Quique, GPU) sobre niveles por banda → ONNX; se conecta en la iteración 2 |

### Checklist de la iteración 4.2

- [x] Ruta cognitiva con aprendizaje; al servidor solo llegan categorías, nunca texto libre
- [x] "Mi energía" (solo en el teléfono) y "Estrategias"
- [x] Aglomeración, humedad y cámara como molestias; ajustes nuevos (cámara, horarios, instrucciones por escrito…)
- [x] Pausa Zen como menú de minijuegos; Pintar por números; Decorar desde Zen
- [x] 41 íconos de pixel art propios; sin emoji como ícono; el porqué de cada sugerencia a un toque
- [ ] Mostrarle la 1.6.0 a Ale y preguntarle por la ruta cognitiva y por el cuarto
- [ ] Pedirle permiso a Ale para haber adaptado su idea del registro de energía
- [ ] Corregir el documento del pitch: el objeto se gana por terminar la prueba, no porque haya servido

### Checklist de la iteración 4.1

- [x] Arte: casillas de edición, sombras y cuadros de reposo; animaciones puras con pruebas (reloj, poses, arrastre)
- [x] Revisión contra cuadros renderizados con los módulos reales y contra las reglas de `DESIGN.md`
- [ ] Probar en un iPhone la build 1.5.0: nitidez, arrastre dentro del scroll, VoiceOver, Reducir movimiento y el ciclo completo de ganar un objeto

### Checklist de la iteración 4

- [x] Integrar los cambios de Magda (UX de los registros y mascota) desde la rama `magda` del espejo
- [x] Motor: nivel "este lugar", recencia de 60 días, "Este lugar cambió" y punto de partida por tipo de lugar
- [x] API 0.5.0: memoria por lugar, reset, "Usarlo otra vez" y cuartos (GET/PUT con revisión y validación)
- [x] Arte del cuarto (26 tipos, 4 giros, atlas de 19 KB) con castor en pixel art
- [x] Lógica isométrica pura con 108 pruebas, misma validación que Rust
- [x] "Lo que sé de este lugar", cuarto o lista, corcho, editor accesible y objeto ganado que aparece en su cuarto
- [ ] Probar en un iPhone la build 1.4.0: nitidez del pixel art, editor con VoiceOver, Reducir movimiento
- [ ] Probar con 3–5 personas el cuarto frente a la lista y revisar que no cambie la proporción de respuestas "ayudó"

### Checklist de la iteración 3

- [x] Micrófono: el plugin de la cámara borraba `NSMicrophoneUsageDescription`; ahora iOS pregunta y, si ya no puede, la app ofrece "Abrir Configuración"
- [x] Botones siempre visibles: flujos a pantalla completa, pie fijo con márgenes seguros y cámara de medio alto como mucho
- [x] "Tu escritorio": escena por capas (`docs/brand/draw_scene.py`), 14 objetos, cielo según la hora y onda que se calma
- [x] Movimiento en tres niveles, barra de pasos en pixeles, medidor al escuchar y franja al analizar la foto
- [x] Sonidos propios (`docs/brand/make_sounds.py`): cinco, apagados por defecto, categoría `ambient` de iOS, con límites acústicos que el script verifica
- [x] Resumen semanal opcional y "Mostrar Tu escritorio en Hoy"
- [x] Investigación de retención ética y revisión de skills de sonido, movimiento y retención
- [x] Se premia la prueba, no el resultado: el escritorio y el tono final no dependen de si "ayudó" (`GET /v1/progress`)
- [x] Avisos sin datos sensibles en la pantalla bloqueada; resumen con día y hora; pregunta tras 5 semanas sin abrirlo
- [ ] Probar la build 1.3.0 en un iPhone: permiso del micrófono, pie de los pasos con texto grande, sonidos con el interruptor de silencio
- [ ] Escuchar los sonidos en el teléfono y ajustar volumen o timbre si hace falta

### Checklist de la iteración 2

- [x] `POST /v1/scan/photo` con salida estructurada, respaldos del servidor, límite diario y registro de tokens
- [x] Escaneo real probado contra producción (4–10 s; hipótesis prudentes y sin describir personas)
- [x] Audio en el teléfono: voces, ruido constante y ruidos repentinos, probados con señales sintéticas
- [x] Módulo nativo `privacy-blur` y pantallas de consentimiento, escuchar, foto y "Esto es lo que notamos"
- [ ] Probar en un iPhone la build 1.2.0, sobre todo el pixelado y los umbrales del audio en oficinas reales
- [ ] Medir cuánto inventa Claude con 20 fotos reales de oficina (decisión 22 del informe)

### Checklist de la iteración 1

- [x] Investigación psicológica y práctica (5 temas) e informe con 23 decisiones de producto
- [x] Reglas de diseño (`docs/DESIGN.md`) a partir de la investigación y de las skills de Expo y Anthropic
- [x] API 0.2: cuentas, lugares, catálogo, registros, motor personal, resultado relativo, comparación, consentimiento y aviso de privacidad
- [x] App 1.1: bienvenida, registro, sugerencia, recordatorio, resultado, Lo que me sirve, solicitud y ajustes
- [x] Smoke test de punta a punta contra producción
- [ ] Probar la build 1.1.0 en un iPhone (Quique)
- [ ] Definir el correo de contacto del equipo para el aviso de privacidad, antes del TestFlight externo

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

- **Correo de contacto** del equipo para el aviso de privacidad (lo exige la LFPDPPP y conviene para Apple).
- **Contacto en Specialisterne** para las pruebas con usuarios y el co-diseño de la iteración 5.
- Si el piloto en TestFlight cuenta como investigación con personas, ¿hace falta consentimiento informado y un comité de ética?

## 10. Cuarto isométrico y memoria por lugar

**Estado:** implementada (fases 0 a 3 el 29 de octubre; animaciones y arrastre de la fase 4 el 30). Reglas de diseño en `docs/DESIGN.md` §12. Falta probar Skia en un iPhone real (fase 0) con la build 1.5.0 y, con usuarios, el cuarto frente a la lista.

- Investigación: [diseño y evidencia](research/research_notes/Escritorio%20isometrico/diseno.md) y [técnica](research/research_notes/Escritorio%20isometrico/tecnica.md).
- Prototipo: [`prototipo/iso_proto.py`](research/research_notes/Escritorio%20isometrico/prototipo/).
- Maqueta: [`docs/brand/room-mockup.png`](brand/room-mockup.png).

### La idea

Cada lugar guardado ("Mi escritorio", "Casa", "Sala de juntas") tiene su propio cuarto isométrico en pixel art. Se toma el género de los cuartos isométricos, no ningún juego en particular; el arte es propio de SpaceEase. Los objetos del cuarto son lo que la persona probó en ese lugar, y cada uno recuerda cómo le fue. La persona decora el cuarto como quiere, y la app usa esa memoria para sugerirle cosas en ese lugar.

### Decisiones tomadas (Quique, 26 oct)

- **Se gana un objeto por cada prueba terminada, sea cual sea el resultado.** No hay puntos por mejorar, ni moneda, tienda o saldo. Premiar "ayudó" sesgaría justo la respuesta que aprende el motor, y también la cifra "ayudó en 5 de 6" que va en la solicitud a la empresa (Dejonckheere 2024; Deci 1999).
- **Decorar es libre desde el primer día:** colores, piso, plantas y cuadros, con 2 a 4 opciones por decisión.
- **Alcance:** fases 0 a 4 antes del pitch.

### Reglas que no se negocian (P0 del informe de diseño)

1. **El cuarto es opcional y nunca es la única vista.** Siempre hay una vista simple (lista o la escena 2D actual) con la misma información.
2. **El objeto se gana por participar, y se avisa antes:** cada prueba terminada deja su objeto, también con "No sé".
3. **Sin moneda, tienda, saldo ni "te faltan N".**
4. **Nada aleatorio, escaso ni pagado.** Nada se pierde ni se deteriora: no hay plantas que se mueren ni mascotas que piden atención.
5. **Sin puntuación del cuarto,** colecciones con huecos, rankings ni "me gusta".
6. **La persona decide dónde va cada cosa.** Un objeto nuevo aparece en un lugar razonable y la app nunca reacomoda nada.
7. **Se puede colocar sin arrastrar:** se toca el objeto, luego la casilla destino, o se usan botones. VoiceOver tiene acciones propias (WCAG 2.5.7). La cámara es fija, sin zoom libre.

### Memoria por lugar

**Motor:**
- Un nivel nuevo, "este lugar, cualquier tarea".
- Lo reciente pesa más, por si el lugar cambia.
- Un botón "Este lugar cambió" para empezar de nuevo sin borrar el historial.
- Un punto de partida según el tipo de lugar (oficina o casa), solo con un mínimo de personas, por privacidad.

**API:**
- `GET /v1/spaces/{id}/memory`: lo que suele molestar ahí, lo probado con sus resultados y lo que no se puede hacer.
- Progreso por lugar.
- Tabla `rooms` con el acomodo (`layout` JSONB, `schema_version` y `revision`, para que dos guardados no se pisen).

**App:**
- Al tocar un objeto: "Probado 3 veces aquí; ayudó en 2", con el botón **"Usarlo otra vez"**. Abre un registro corto (tarea, molestia y esfuerzo) que salta directo a la prueba.
- Un corcho "Lo que me sirve aquí" donde la persona fija lo que quiera; la app nunca destaca nada por su cuenta.
- Un contador por lugar que solo sube, por ejemplo "Aquí: 7 pruebas · 4 cosas que sabes".

### Técnica

- **Skia 2.14.0** (`@shopify/react-native-skia`), la versión que trae Expo Go para SDK 58. La v3 no corre en Expo Go.
- Skia dibuja el cuarto. Encima van vistas invisibles para tocar y para VoiceOver.
- La lógica isométrica (proyección, colisiones, orden de dibujo y el formato del acomodo) va en TypeScript puro y se prueba con tests.
- Los sprites salen de un renderizador de vóxeles en Python con la paleta de la marca, y cada objeto da 4 rotaciones sin redibujarlo.
- Una sola hoja de sprites de unos 50 KB. Las capas de la escena actual ocupan unos 45 MB de memoria.
- El cuarto mide 5 × 5 mosaicos de 32 × 16 pixeles, a 2 pt por pixel en cualquier iPhone actual.
- **Descartados:**
  - **three.js / 3D real:** no arranca en Expo Go SDK 58 (bug abierto expo/expo#51543).
  - **Motor de juego en un WebView:** otro motor de JS y accesibilidad mixta.

### Fases

| Fase | Qué | Días-persona |
|---|---|---|
| 0 | Prueba de Skia en Expo Go en un iPhone real. Si falla, se usa la alternativa con vistas normales | ½–1 |
| 1 | Memoria por lugar: motor, API, tarjeta del lugar y "Usarlo otra vez". Sirve aunque el cuarto no llegue | 2–3 |
| 2 | Cuarto MVP: uno por lugar, con los objetos probados, sus tarjetas y la vista simple | 4–6 |
| 3 | Decorar: mover, rotar y guardar objetos (primero tocar y tocar, después arrastrar); decoración libre; acomodo en la API | 4–6 |
| 4 | Pulido: cielo según la hora, movimiento "con detalles" dentro de las reglas de DESIGN §5, sonido y prueba con usuarios | 3–5 |

### Riesgos

| Riesgo | Mitigación |
|---|---|
| **Tiempo:** 14 a 21 días-persona con poco más de una semana | Hacer las fases en orden; cada una deja algo que funciona. Si hace falta, la 4 queda para después del pitch |
| La versión de Skia de la app se separa de la de Expo Go | Fijar 2.14.0 y correr `npx expo install --check` antes de cada demo por QR |
| Pixeles borrosos | Muestreo de vecino más cercano explícito, escala entera y posiciones sin medios pixeles |
| Volumen de arte (40 tipos × variantes × 4 direcciones) | Vóxeles con rotación automática; empezar con los 14 objetos actuales |
| La gamificación se cuela | Revisar cada pantalla contra las reglas P0 |
| Reglas de validación repetidas en TypeScript y Rust | Un solo catálogo generado y casos de prueba compartidos |

### Para revisar en equipo

1. ¿Aprueban el modelo "objeto por prueba", sin puntos ni moneda?
2. ¿Quién afina el arte de los objetos y de la decoración?
3. Si la fase 0 falla, ¿se sigue con vistas normales o se recorta el cuarto?
4. ¿Se puede probar con personas de la comunidad de Specialisterne el cuarto frente a la vista simple, revisando que no cambie la proporción de respuestas "ayudó"?
