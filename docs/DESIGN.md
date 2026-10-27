# Reglas de diseño de SpaceEase

Estas reglas salen de la investigación en [`docs/research/reports`](research/reports/Ajustes%20sensoriales%20laborales%20y%20neurodivergencia.md) y de las guías de Expo y de Anthropic sobre interfaces nativas y no genéricas. Si una pantalla rompe una regla, se cambia la pantalla, no la regla. Para cambiar una regla, primero se actualiza este documento.

## 1. Principio

La app habla del **entorno**, no de la persona. No diagnostica, no puntúa y no promete productividad. Devuelve control: la persona decide qué probar, qué guardar y qué compartir.

## 2. Lenguaje

| Regla | Ejemplo |
|---|---|
| El sujeto es el entorno | "Este espacio tiene mucha luz directa", nunca "tienes hipersensibilidad" |
| Sin términos clínicos | Nada de "síntomas", "trastorno", "déficit", "alto/bajo funcionamiento" |
| Género neutro | "Si tienes dudas", no "si estás seguro o segura" |
| Frases cortas | Párrafos de 50 palabras o menos (COGA) |
| Errores sin culpa ni alarma | Dicen qué pasó y qué hacer; nunca "¡Ups!" ni "inválido"; lo escrito no se borra |
| Resultados honestos | "Lo probaste 3 veces aquí; ayudó en 2. Todavía no es seguro." (Self-E) |
| Sin promesas legales | "Puedes pedir un ajuste describiendo la tarea y la barrera", nunca "nunca tendrás que revelar nada" |

## 3. Estructura de pantallas

- **Una pregunta por pantalla** y, como mucho, **5 opciones principales** a la vista; lo demás, a un toque ("Ver más tareas").
- Siempre hay **"No sé"** o **"Nada de esto"**. Todo se puede omitir o dejar.
- Sin tiempos límite. Las respuestas se guardan en el borrador mientras se avanza.
- Encabezados **nativos** del Stack (título grande en las pestañas). No se arman a mano.
- "Cerrar" en texto, siempre arriba a la derecha de los flujos.
- Listas **agrupadas** con separadores finos, no una tarjeta por fila. Lo elegido se marca con fondo **y** con ícono, nunca solo con color.
- Íconos SF Symbols. Nada de emoji como ícono.
- Cada pantalla contempla cargando, vacío, error y contenido. Sin spinners de pantalla completa.

## 4. Color y texto

- Paleta "Quiet workspace" del ícono (`src/constants/theme.ts`). Fondo papel cálido (#F4EEE2), no blanco puro, como recomienda la guía de la British Dyslexia Association. Modo oscuro verde azulado profundo (#152F32), no negro puro.
- Contraste AA (≥ 4.5:1) en todo el texto. El acento (#3F8A7B) solo va en iconos y bordes. La opción **Contraste suave** baja la diferencia sin pasar de AA (AASPIRE).
- Sin rojos de alarma. Los avisos usan un tono cálido apagado.
- Fuente del sistema con Dynamic Type. Cuerpo de 17 pt, interlineado ≈ 1.45, pesos 400 y 600. Sin itálicas ni MAYÚSCULAS.
- Toques de al menos **48 pt** (botones de 52 pt).

## 5. Movimiento, sonido y vibración

Hay tres niveles de movimiento (`useMotionLevel` en `src/lib/feedback.ts`). La persona elige; la app nunca sube el nivel por su cuenta.

| Nivel | Cuándo | Qué se mueve |
|---|---|---|
| **Reducido** | "Reducir movimiento" de iOS (en vivo) o "Siempre reducido" en Ajustes. Gana siempre | Solo fundidos. Nada se repite ni se desplaza. Sin franja de análisis ni columnas de nivel |
| **Tranquilo** (por defecto) | Sin "Animaciones con detalles" | Movimiento breve y con propósito: barra de pasos, fundidos, la franja al analizar la foto y la onda del monitor que se calma |
| **Con detalles** | "Animaciones con detalles" en Ajustes o en el aviso de Hoy | Además: la escena se mueve un rato al aparecer o al tocarla, el objeto nuevo "cae" dos pixeles y se enciende a saltos (sin partículas ni confeti), los marcadores se encienden en orden y la palomita aparece con un fundido |

| Regla | Valor |
|---|---|
| Lo frecuente no se anima | Cambiar de pestaña, el teclado, elegir una opción (en modo tranquilo) y las transiciones de pantalla, que son las nativas |
| Al tocar | Cambio de opacidad o de fondo inmediato; sin "aplastar" el botón |
| Curvas | Salida suave (`Easing.bezier(0.23, 1, 0.32, 1)`). Con detalles, `Easing.steps(n)`: las cosas se encienden a saltos, como pixeles. Nunca `ease-in`, rebotes ni elásticos |
| Entradas | Fundidos. Nada crece desde cero ni se desliza. Los marcadores de la foto, con detalles, se encienden con 40 ms entre uno y otro (menos de 300 ms en total) |
| Duración | Tranquilo: 250 ms o menos. Con detalles: hasta 450 ms por animación y una sola vez por acción |
| Lo que se repite | La franja de la foto da como mucho 3 pasadas (3.6 s) y se queda quieta. La escena, con detalles, se mueve 5 s al aparecer o al tocarla: un solo elemento a la vez (planta, vapor, ventilador), con pausas. Se detiene antes de 5 s (WCAG 2.2.2) y al salir de la pantalla. Nada de oscilaciones continuas (las de ~0.2 Hz marean, según la guía de Apple) |
| Desplazamiento | Como mucho 2 pixeles de la escena (≈ 10 pt). Nada cruza la pantalla ni hace zoom de pantalla completa (WCAG 2.3.3) |
| Momento firma | La onda del monitor pasa de ruidosa a tranquila en 3 cuadros (300 ms). El sonido y la vibración llegan en el cuadro en que queda tranquila, nunca antes |
| Vibración | **Apagada por defecto.** Si se activa, solo al confirmar, una vez por acción y nunca como única señal |
| Sonido | **Apagado por defecto.** Ver la sección 11 |

## 6. Avisos

- Recordatorios solo cuando la persona los pide (25 o 50 minutos, o ninguno). Uno por prueba y como mucho 5 al día. El permiso se pide en ese momento, no al instalar.
- Lo que se ve con el teléfono bloqueado no dice qué ajuste ni qué molesta: "¿Cómo te fue? Cuando quieras, cuéntanos cómo te fue con la prueba". Sin sonido, sin número en el ícono y nunca "urgente" (`active` para el "¿cómo te fue?", `passive` para el resumen).
- Un aviso no se repite si no se contesta. Nada de avisos para "recuperar" a quien dejó de usar la app.
- Nada de rachas, insignias, rankings ni mensajes del tipo "llevas 3 días sin…".
- El progreso se acumula y nunca baja: "Tu escritorio" (sección 11). Se puede ocultar.
- **Resumen semanal** (opcional, apagado por defecto): un aviso sin sonido el día y a la hora que la persona elige (9:00, 13:00 o 17:00). Se ofrece una sola vez, al terminar una prueba, y se puede activar en Ajustes. Trae tres partes, siempre en el mismo orden: lo que probó, lo que ayudó y lo que más le sirve. Lo predecible es el hábito; no hay sorpresas, premios variables ni nada que se desbloquee. Si no hubo pruebas: "Puede que hayas descansado o que no lo hayas anotado. Las dos cosas están bien". Tras 5 semanas sin abrirlo, Hoy pregunta una vez si lo sigue queriendo ("Está bien de las dos formas").

## 7. Medición

- **Medida principal:** "¿Cuánto te molesta el entorno?". **Secundaria:** "¿Cuánto esfuerzo te cuesta la tarea?". Ambas con 5 botones y palabra en cada punto (casi nada, poco, algo, bastante, muchísimo); sin deslizador. Son medidas propias, no clínicas.
- "Ayudó" = mejoró **más que la mejora típica de esa persona**, no solo "bajó un punto". Así se descuenta la regresión a la media.
- De vez en cuando (10 %, tras 3 registros) se propone **"Esta vez no cambies nada"**, de forma transparente y con la opción de no hacerlo. Es la comparación que separa un ajuste del paso del tiempo.

## 8. Privacidad por diseño

- Cuenta anónima por dispositivo; el servidor guarda solo el SHA-256 de la llave.
- Consentimiento expreso para guardar registros, sin marcar de antemano. El aviso está en `GET /privacy` de la API.
- El empleador no tiene acceso. La solicitud de ajuste se comparte desde la app solo si la persona lo decide, y los datos propios van solo si los incluye.
- "Borrar todos mis datos" en Ajustes borra el servidor y el teléfono.
- **Foto y sonido** son opcionales, cada uno con su consentimiento (apagado por defecto y revocable en Ajustes).
  - El audio se analiza en el teléfono y se borra; nunca se envía. Mientras se graba hay un indicador visible y un botón "Detener".
  - La foto se toma con la cámara de la app (sin acceso a la fototeca). Las caras y siluetas se pixelan en el teléfono, y la persona ve exactamente lo que se enviará.
  - Cada hallazgo es una pregunta prudente ("Parece haber…", "Posible…") con Sí / No / No sé. Solo lo confirmado cuenta, y se guarda de dónde vino.
  - Los marcadores sobre la foto repiten una lista, que es la que lee VoiceOver.

## 9. Skills para quien trabaje con Claude Code

`.claude/settings.json` habilita dos plugins del marketplace oficial; Claude Code ofrece instalarlos al abrir el repo:

| Plugin | Para qué | Qué ignorar en esta app |
|---|---|---|
| `expo` (Expo) | `expo-animation`, `expo-design-system`, `expo-native-ui`, router y EAS: qué animar, en qué hilo, con qué curva; las 20 señales de una app genérica | El "presupuesto de deleite" y las celebraciones, los resortes con rebote, el "aplastado" al tocar y la vibración "para deleitar" |
| `frontend-design` (Anthropic) | Plan de diseño → revisión contra el brief → construir → criticar; lista de señales de diseño hecho por IA | "Tomar riesgos estéticos" y la animación de entrada orquestada: la personalidad va en el pixel art, no en el movimiento |

Para el modo con detalles, los sonidos y la retención se revisaron más skills (informe completo en [`research_notes/Retencion y experiencia opcional/skills.md`](research/research_notes/Retencion%20y%20experiencia%20opcional/skills.md)). Se recomiendan, **revisándolas antes de instalar**:

| Skill | Instalar | Para qué | Qué ignorar en esta app |
|---|---|---|---|
| `ux-sound` (jal-co, MIT) + `ui-sound-design` (dannyjpwilliams, MIT) | `npx skills add jal-co/skills --skill ux-sound` y `npx skills add dannyjpwilliams/ui-sound-design-skill` | Si suena, qué y qué tan fuerte; recetas de síntesis | La ruta "generate" con API de pago y los sonidos de navegación o de "procesando" |
| `motion-design` (LottieFiles, MIT) | `npx skills add LottieFiles/motion-design-skill` | Tablas de duración, escalonado y sobrepaso | "Siempre tres capas de movimiento", la respiración continua de 3–6 s y el "shake" de error |
| `interaction-design`, `inclusive-interaction` y `cognitive-accessibility` (Owl-Listener, MIT) | `/plugin marketplace add Owl-Listener/designer-skills` | Tiempos de carga, final de las experiencias y sensibilidad al movimiento | La skill `zeigarnik-effect` (presión para terminar) |
| `ux-copy` (Anthropic, Apache-2.0) | Copiar solo `design/skills/ux-copy/SKILL.md` de `anthropics/knowledge-work-plugins` | Textos de éxito, vacío, error y permisos | El plugin completo de diseño, que suma 9 conectores |
| `gamification-loops` (omer-metin, Apache-2.0) | Solo como revisión de lo que retiene | Sus "líneas rojas": castigar por no usar, culpa, recompensas variables | Bonos sorpresa y tablas de posiciones |

No se instalan: Rive y `react-native-audio-api` (requieren build propia y rompen el plan B de Expo Go), skills de onboarding con cargas falsas o testimonios "aspiracionales", ni las que sostienen que "si a una persona neurotípica le parece demasiado, está bien para TDAH".

Las reglas de este documento mandan sobre las de cualquier skill.

## 10. Lo que se evita (señales de una app genérica)

Fondo crema con tipografía serif de exhibición y acento terracota; una tarjeta por cada fila; sombras fuertes; bordes grises en todo; entradas escalonadas en cada lista; carrusel de bienvenida promocional; degradados decorativos; emoji como íconos; spinners de pantalla completa; encabezados hechos a mano. La personalidad de SpaceEase está en un solo lugar: la escena en pixel art del ícono.

## 11. Tu escritorio, el modo con detalles y los sonidos

**Tu escritorio** es la escena del ícono en versión ancha (`docs/brand/draw_scene.py`, 64 × 28 pixeles, por capas). Cada ajuste que la persona **prueba hasta el final** deja un objeto: audífonos, lámpara cálida, persiana, taza para una pausa y 10 más (`src/lib/desk.ts`, `GET /v1/progress`).

- **Se premia la prueba, no el resultado.** El objeto llega haya ayudado o no, y el final suena y se ve igual para "ayudó", "no ayudó" y "no está claro": "Ya sabes algo más de este espacio". Antes de contestar nunca se promete nada por una respuesta. Si solo "ayudó" ganara algo, la app empujaría a contestarlo, y ese es justo el dato que aprende el motor y que va en la solicitud a la empresa (premiar respuestas empeora su calidad: Dejonckheere et al., 2024; regla 1 de las notas de retención).
- **Nunca se pierde.** No caduca, no hay rachas, no hay huecos vacíos ni "te faltan N" o "3 de 14".
- Hoy dice "N pruebas terminadas": un número que solo sube.
- Se celebra **una vez por prueba**, en el resultado y dentro de la escena: la onda se calma, el objeto nuevo aparece y suena el tono del resultado. Lo demás es silencioso.
- El cielo de la ventana sigue la hora del teléfono (amanecer, día, atardecer y noche). No es una notificación ni pide nada.
- La onda del monitor pasa de ruidosa a tranquila al terminar un registro: es la metáfora de la app (el entorno que se calma).
- VoiceOver lee la escena como una imagen con la lista de objetos.

**El aviso de Hoy** ofrece una sola vez las animaciones con detalles ("Activar animaciones con detalles" / "Así está bien") y no vuelve a aparecer. Los sonidos y la vibración no se encienden con él: cada uno pide su propio interruptor en Ajustes, donde también se pueden probar.

**Progreso** sin presión: el único "premio" es información sobre el entorno ("Lo probaste 3 veces aquí; ayudó en 2") y el objeto de lo que se probó. Sin puntos, niveles ni frases sobre la persona ("¡Eres genial!", "Sigue así", "deberías"). Antes de sumar algo que retenga, tres preguntas: ¿se puede dejar sin perder nada? ¿castiga tomarse un descanso? (prueba de la propuesta de Ley de Equidad Digital de la UE) ¿premia una respuesta en lugar de la participación?

**Plan "si…, entonces…"**: al aceptar un ajuste, "Listo" muestra "Tu plan: la próxima vez que toque «Leer» aquí, usa audífonos con cancelación de ruido". Decir cuándo y dónde se hará algo ayuda a hacerlo (Sheeran et al., 2024, 642 pruebas); no lleva hora fija, porque las ventanas rígidas salieron peor (Beshears et al., 2021).

**Qué se mide** para saber si la app sirve: pruebas terminadas, cosas aprendidas y solicitudes escritas, no el uso diario. Que el uso baje con el tiempo es lo esperado en apps de salud (3.3 % siguen a los 30 días: Baumel et al., 2019) y no es un fracaso si la persona ya aprendió lo que le sirve.

**Sonidos** (`docs/brand/make_sounds.py`, síntesis propia y determinista):

| Regla | Valor |
|---|---|
| Por defecto | Apagados. Se activan en Ajustes, con un botón para probarlos |
| Cuándo | Solo lo que la persona provoca o el fin de una espera: empieza la escucha, ya están los hallazgos, aceptar un ajuste, terminar una prueba (el mismo tono para cualquier resultado) y tocar la escena. **Nunca** al navegar, elegir una opción, escribir, abrir la app, en errores ni en los avisos |
| Cuántos | Cinco, en la misma tonalidad. Como mucho 3 en un registro y 1 por acción. Entre un sonido y otro pasan al menos 200 ms, y tocar la escena suena como mucho una vez cada 2 s |
| Modo silencio | Categoría `ambient` de iOS: callan con el interruptor y se mezclan con la música en lugar de cortarla |
| Timbre | Marimba con fieltro en pentatónica de Do; el "pixel" es una onda triangular filtrada |
| Frecuencias | Fundamentales de 440 a 880 Hz, una o dos notas. Al menos 20 dB menos de energía entre 2.5 y 5.5 kHz (la banda más áspera) y nada por encima de 5 kHz |
| Envolvente | Ataque de 18 ms (sin clics) y caída larga; sin trémolo |
| Duración | Confirmar, 0.4 s; el resultado, 0.65 s; nada pasa de 0.7 s |
| Volumen | Mismo volumen percibido (RMS de -33 dBFS, ±1 dB) y picos de -24 dBFS, nunca más de -20; "Bajo" (por defecto) los baja unos 3 dB. El script falla si un sonido no cumple |
| Grabación | El aviso de "empieza a escuchar" termina antes de grabar, para no colarse en el análisis |
| Vibración | Si está encendida, acompaña al sonido en el mismo momento (guía de Apple) |
