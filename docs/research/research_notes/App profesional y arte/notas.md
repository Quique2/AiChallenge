# Que la app se sienta profesional: menos texto y más arte

Investigación del 31 de octubre de 2026, a partir de los comentarios del equipo ("hay mucho texto y no tanto arte"; "como los minijuegos de Pou, con nombre e ícono con instrucciones"). Las juntas con la socioformadora no se citan aquí: las grabaciones tienen datos personales y no van al repo.

## Lo que muestran apps publicadas

| App | Lo que se puede comprobar | Qué tomamos |
|---|---|---|
| **Tiimo** (iPhone App of the Year 2025, enfocada en neurodivergencia) | La ficha describe un resumen del día con color y "a timeline with soothing colors"; tareas con íconos, colores y subtareas; un temporizador que llama "calming" | El contenido se reconoce por su ícono y color antes de leerlo. Tono tranquilo |
| **Finch** | Una crítica de diseño elogia el botón constante y la barra de progreso, y critica pantallas saturadas y propone divulgación progresiva | Botón siempre en el mismo lugar (ya lo teníamos); mostrar poco y abrir lo demás a un toque |
| **Pou** (según el comentario del equipo; no se revisó la app) | Menú de minijuegos con nombre, ícono e instrucciones | Solo el patrón de menú. El arte y los juegos son propios |

**Límite:** no encontré análisis serios del arte de estas apps ni de menús de minijuegos en apps tranquilas. Lo anterior sale de fichas de la tienda, una crítica académica y el comentario del equipo, no de estudios con usuarios.

## Skills revisadas

Se leyeron como referencia; no se instaló nada.

| Skill | Lo útil | Decisión |
|---|---|---|
| `expo-design-system` (Expo, oficial): lista "native slop" | Emoji como ícono, todo en tarjetas, entradas animadas en cada visita, barras de pestañas flotantes | Se usa como lista de revisión |
| `RubenGlez/mobile-design` (MIT): `visual-system.md` | Para bienestar: "soft contrast, supportive copy, calm hierarchy". Jerarquía antes que decoración; evitar texto que describe funciones en vez de ayudar a actuar | Se usa como lista de revisión |
| `draftbit/mobile-taste-skill` (MIT) | Señala emoji como íconos y pilas de tarjetas blancas; tiene un puntaje de "AI slop" | Útil para una auditoría futura |

## Lo que se hizo

1. **Un sistema de arte, no dibujos sueltos:** 41 íconos de 20 × 20 con la paleta de la marca, sobre baldosa propia para que funcionen en las 12 paletas y en modo oscuro. Sustituyen a los emoji.
2. **Dibujo y texto juntos:** el texto no se quita de las opciones, por accesibilidad. Se quitó lo que explicaba de más.
3. **Pausa Zen como menú** con instrucciones de tres pasos antes de empezar.
4. **Hoy con accesos visuales** en vez de botones de texto apilados.

## Lo que falta por validar

Nada de esto se ha probado con personas neurodivergentes. Más dibujos también puede ser más estímulo: conviene preguntarlo en las pruebas.

## Fuentes

- [Ficha de Tiimo en App Store](https://apps.apple.com/TR/app/id1480220328)
- [Tiimo, iPhone App of the Year 2025](https://www.freepressjournal.in/tech/apple-app-store-awards-2025-tiimo-wins-iphone-app-of-the-year-as-ai-apps-dominate-full-winners-list)
- [Crítica de diseño de Finch (Pratt)](https://ixd.prattsi.org/2026/02/design-critique-finch-self-care-pet-ios-app/)
- [RubenGlez/mobile-design](https://github.com/RubenGlez/mobile-design)
- [draftbit/mobile-taste-skill](https://github.com/draftbit/mobile-taste-skill)
- [Skills de Expo](https://docs.expo.dev/skills.md)
