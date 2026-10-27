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
| **Tranquilo** (por defecto) | Sin "Animaciones con detalles" | Movimiento breve y con propósito: barra de pasos, palomita, fundidos, la onda del monitor que se calma |
| **Con detalles** | "Animaciones con detalles" en Ajustes o en el aviso de Hoy | Además: la escena cobra vida al tocarla, el objeto nuevo "cae" con destellos, los marcadores crecen uno tras otro |

| Regla | Valor |
|---|---|
| Lo frecuente no se anima | Cambiar de pestaña, el teclado, las transiciones de pantalla (son las nativas) |
| Al tocar | Cambio de opacidad o de fondo inmediato; sin "aplastar" el botón |
| Curvas | Salida suave (`Easing.bezier(0.23, 1, 0.32, 1)`). Con detalles, `Easing.steps(n)`: las cosas se encienden a saltos, como pixeles. Nunca `ease-in`, rebotes ni elásticos |
| Duración | Tranquilo: 250 ms o menos. Con detalles: hasta 450 ms por animación y una sola vez por acción |
| Animaciones que se repiten | Solo la escena con detalles y la franja mientras se analiza la foto. La escena se detiene sola a los 5 s (WCAG 2.2.2) y vuelve solo si la tocan |
| Desplazamiento | Como mucho 2 pixeles de la escena (≈ 10 pt). Nada cruza la pantalla ni hace zoom de pantalla completa (WCAG 2.3.3) |
| Vibración | **Apagada por defecto.** Si se activa, solo al confirmar, una vez por acción y nunca como única señal |
| Sonido | **Apagado por defecto.** Ver la sección 11 |

## 6. Avisos

- Recordatorios solo cuando la persona los pide (25 o 50 minutos, o ninguno). Uno por prueba y como mucho 5 al día. El permiso se pide en ese momento, no al instalar.
- Nada de rachas, insignias, rankings ni mensajes del tipo "llevas 3 días sin…".
- El progreso se acumula y nunca baja: "Tu escritorio" (sección 11).

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

Las reglas de este documento mandan sobre las de cualquier skill.

## 10. Lo que se evita (señales de una app genérica)

Fondo crema con tipografía serif de exhibición y acento terracota; una tarjeta por cada fila; sombras fuertes; bordes grises en todo; entradas escalonadas en cada lista; carrusel de bienvenida promocional; degradados decorativos; emoji como íconos; spinners de pantalla completa; encabezados hechos a mano. La personalidad de SpaceEase está en un solo lugar: la escena en pixel art del ícono.

## 11. Tu escritorio, el modo con detalles y los sonidos

**Tu escritorio** es la escena del ícono en versión ancha (`docs/brand/draw_scene.py`, 64 × 28 pixeles, por capas). Cada ajuste que ayuda deja un objeto: audífonos, lámpara cálida, persiana, taza para una pausa y 10 más (`src/lib/desk.ts`).

- Se gana solo cuando algo **ayudó** (el resultado relativo de la sección 7), nunca por usar la app.
- **Nunca se pierde.** No caduca, no hay rachas y no se muestra "te faltan N".
- Hoy dice "N cosas que te sirven": un número que solo sube.
- Se celebra **una vez**, en el resultado: el objeto aparece y suena el arpegio. Lo demás es silencioso.
- El cielo de la ventana sigue la hora del teléfono (amanecer, día, atardecer y noche). No es una notificación ni pide nada.
- La onda del monitor pasa de ruidosa a tranquila al terminar un registro: es la metáfora de la app (el entorno que se calma).
- VoiceOver lee la escena como una imagen con la lista de objetos.

**El aviso de Hoy** ofrece activar detalles y sonidos una sola vez. Tiene dos respuestas con el mismo peso ("Activar detalles y sonidos" / "Así está bien") y no vuelve a aparecer.

**Sonidos** (`docs/brand/make_sounds.py`, síntesis propia y determinista):

| Regla | Valor |
|---|---|
| Por defecto | Apagados. Se activan en Ajustes o en el aviso de Hoy |
| Modo silencio | Categoría `ambient` de iOS: callan con el interruptor y se mezclan con la música en lugar de cortarla |
| Timbre | Marimba con fieltro en pentatónica de Do; el "pixel" es una onda triangular filtrada |
| Frecuencias | Fundamentales de 392 a 880 Hz; nada audible por encima de ~4 kHz |
| Envolvente | Ataque de 6 a 10 ms (sin clics), caída exponencial |
| Duración | Lo frecuente, menos de 0.2 s ("tap", "paso"); lo más largo, 0.9 s (el arpegio del resultado) |
| Volumen | Picos de -24 a -16 dBFS en el archivo; "Bajo" (por defecto) los baja al 45 % |
| Frecuencia de uso | Uno por acción. Elegir una opción de una sola respuesta no suena: suena el paso siguiente |
| Grabación | El aviso de "empieza a escuchar" termina antes de grabar, para no colarse en el análisis |
| Vibración | Si está encendida, acompaña al sonido en el mismo momento (guía de Apple) |
