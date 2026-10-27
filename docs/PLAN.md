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
| `Quique2/AiChallenge` (privado) | **Monorepo de trabajo.** Aquí se edita todo y desde aquí despliega Railway |
| `nina-col/AiChallengeFront` | Espejo de `apps/mobile`, para que el equipo lea el código de la app |
| `nina-col/AiChallengeBack` | Espejo de `apps/api`, para que el equipo lea el código del backend |

Los espejos se actualizan con `scripts/sync-team-repos.sh` al cerrar cada iteración: un commit normal `sync monorepo@<sha>` con la lista de cambios, **sin force-push**, así no se pierde su historial. Si alguien hace commit directo en un espejo, avisar para integrarlo en el monorepo antes del siguiente sync (si no, se sobrescribe).

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
| 4 | | Redacción con Claude Haiku 5.5 (solicitud y tarjetas), "¿qué puede pedirte tu empresa?" por país y tarjetas de aprendizaje |
| 5 | | Usuario demo con historial sembrado, revisión de accesibilidad con VoiceOver y texto grande, y enlace público de TestFlight |
| 6 | | **Validación** con 3–5 personas, idealmente vía Specialisterne y con co-diseño pagado |
| 7 | | **Pitch:** guion de demo, métricas reales, limitaciones declaradas (tabla del informe) y video de respaldo |
| ‖ | | **Modelo de audio** (Quique, GPU) sobre niveles por banda → ONNX; se conecta en la iteración 2 |

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
