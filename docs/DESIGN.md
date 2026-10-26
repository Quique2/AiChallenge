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

## 5. Movimiento y vibración

| Regla | Valor |
|---|---|
| Lo frecuente no se anima | Cambiar de pestaña, elegir una opción, el teclado |
| Al tocar | Cambio de opacidad o de fondo inmediato; sin "aplastar" el botón |
| Lo que sí se anima | Solo un fundido de 200 ms cuando cambia la sugerencia |
| Curvas | Salida suave (`Easing.bezier(0.23, 1, 0.32, 1)`); nunca `ease-in`, rebotes ni elásticos |
| Duración máxima | 250 ms; las transiciones de pantalla son las nativas |
| Reducir movimiento | Se respeta el de iOS (en vivo) y además hay un ajuste propio: solo fundidos |
| Vibración | **Apagada por defecto.** Si se activa, solo al confirmar, una vez por acción y nunca como única señal |
| Sonido | Ninguno. Los avisos son silenciosos |

## 6. Avisos

- Recordatorios solo cuando la persona los pide (25 o 50 minutos, o ninguno). Uno por prueba y como mucho 5 al día. El permiso se pide en ese momento, no al instalar.
- Nada de rachas, insignias, rankings ni mensajes del tipo "llevas 3 días sin…".

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
