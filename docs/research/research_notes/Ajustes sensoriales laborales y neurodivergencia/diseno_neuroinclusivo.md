# Diseño de apps móviles cognitivamente accesibles y neuroafirmativas (personas adultas autistas, con TDAH y disléxicas): checklist con fuentes para SpaceEase (iOS, React Native/Expo)

> Notas de investigación (español; las citas textuales de fuentes en inglés se dejan en inglés). Fecha de consulta: 26-10-2026.
> Convención: "Cited Findings" = solo lo verificado en la fuente enlazada; "Inferences" = traducción a reglas implementables (mías, no de la fuente); "Gaps" = lo no encontrado o no verificable.

---

## 1. ¿Qué exigen o recomiendan W3C COGA (2021) y los criterios de WCAG 2.2 relevantes para la cognición?

### Takeaway
COGA ("Making Content Usable…", Nota del W3C del 29-04-2021) es guía suplementaria, no obligatoria, organizada en 8 objetivos con patrones muy concretos: palabras comunes, párrafos de 50 palabras como máximo, 5 opciones principales por pantalla como máximo, recordatorios solo a petición, interrupciones controladas por la persona y nada de timeouts. WCAG 2.2 (05-10-2023) aporta los umbrales normativos: contraste 4.5:1/3:1, espaciado de texto 1.5/2/0.12/0.16, objetivos táctiles de 24×24 (AA) y 44×44 (AAA), avisos de tiempo con 20 s para ampliarlo, ayuda en posición constante, no volver a pedir datos y autenticación sin pruebas cognitivas.

### Cited Findings

**Estado y estructura de COGA**
- COGA es una "W3C Working Group Note" publicada el 29-04-2021 (NOTE-coga-usable-20210429). Es guía suplementaria: seguirla no es necesario para cumplir WCAG y los grupos "do not expect this document to become a W3C Recommendation" — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Sus 8 objetivos son: (1) ayudar a entender qué son las cosas y cómo usarlas; (2) ayudar a encontrar lo que se necesita; (3) usar contenido claro y comprensible; (4) ayudar a evitar errores y a corregirlos; (5) ayudar a concentrarse; (6) que los procesos no dependan de la memoria; (7) dar ayuda y apoyo; (8) apoyar la adaptación y la personalización — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Memoria de trabajo: algunas personas solo retienen "one to three items" a la vez (sección 2.2). En el apartado de login se dice que muchas personas "can remember one to four pieces of information". Las dos cifras no coinciden del todo — [W3C COGA](https://www.w3.org/TR/coga-usable/)

**Objetivo 1–2: entender y encontrar (COGA)**
- Título o encabezado claro que resuma el propósito de cada página o pantalla (4.2.1). Jerarquía y diseño familiares, con ubicaciones convencionales (4.2.2). Diseño visual consistente en encabezados, controles y estilos de foco (4.2.3). Cada paso claro, con migas de pan o indicador de pasos completados, actual y pendientes (4.2.4) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Los elementos no pulsables no deben parecer enlaces ni controles. Los controles deben ser "large enough so that users can click on it and not the item next to it". Las instrucciones de controles poco habituales deben estar en la misma página o "one click away" — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Iconos: un icono por significado, situado a la izquierda del texto en idiomas LTR. Evitar páginas densas llenas de iconos (4.2.7) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Tareas clave visibles sin hacer scroll. Menús poco profundos. Agrupar con bordes, sombreado y espacio en blanco. Dividir los medios en segmentos de "6 minutes or less in duration" con transcripción (4.3.x) — [W3C COGA](https://www.w3.org/TR/coga-usable/)

**Objetivo 3: lenguaje (COGA)**
- Usar las ~1500 palabras o frases más comunes y explicar la jerga, los acrónimos y las abreviaturas a un toque/clic de distancia (4.4.1) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Presente y voz activa (4.4.2). Evitar dobles negaciones y oraciones subordinadas anidadas (4.4.3). Lenguaje literal: explicar metáforas y símiles entre paréntesis o en un pop-up (4.4.4) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Texto breve: dividir los párrafos de "more than 50 words", una idea por frase, lista cuando haya "three or more things in a row" y lista numerada para "three or more steps" (4.4.5) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Resúmenes de documentos de más de 300 palabras (4.4.8, 4.8.2). Separar cada instrucción e incluir pasos "obvios" (4.4.9). Espacio en blanco generoso y ajustable, sin empujar el contenido clave por debajo del scroll (4.4.10). Fondo liso detrás del texto (4.4.11). Explicar el contenido implícito, como sarcasmo o emoción (4.4.12). Acompañar los números con palabras, por ejemplo "frío/caliente" (4.4.13) — [W3C COGA](https://www.w3.org/TR/coga-usable/)

**Objetivo 4: errores (COGA)**
- Los controles y el contenido no deben moverse durante la carga salvo por acción de la persona. Mostrar un indicador de carga claro (4.5.1) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- "Atrás" siempre debe funcionar y conservar el trabajo y la posición. Acciones de volver y deshacer claramente etiquetadas (4.5.2, 4.5.5) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Formularios: pedir el mínimo de información, marcar los campos obligatorios, aceptar formatos diversos, autocorregir solo cuando la corrección sea fiable (si no, sugerir), y mostrar un resumen antes de enviar que se pueda editar con un toque sin perder datos (4.5.4–4.5.8) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Evitar timeouts y "let the user save their work as they go". Si un timeout es imprescindible, decir al inicio cuánto tiempo hay y si se perderán datos. Tras volver a iniciar sesión, "all the work is still in place" (4.5.9) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Feedback: "easily-recognizable success or failure feedback with every user action". Marca de verificación en los pasos completados, estados pulsado/seleccionado visibles y mensajes explícitos del tipo "se ha enviado" (4.5.10) — [W3C COGA](https://www.w3.org/TR/coga-usable/)

**Objetivo 5: foco (COGA)**
- Las interrupciones, los recordatorios y los cambios de contenido los controla la persona "unless they are started by the user or involve an emergency". Pausa fácil para el contenido en movimiento. Evitar pop-ups que haya que cerrar para continuar. Dejar elegir el tipo de notificación (visual, sonido o ninguna) (4.6.1) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Rutas críticas cortas: solo "the minimally necessary steps". Los pasos opcionales (upsells, donaciones) van antes o después de la tarea principal, nunca dentro (4.6.2) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- "five or less main choices on each screen". Lo extra va bajo un enlace "más" claramente etiquetado, y la función principal debe ser mucho más grande que el resto (4.6.3) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Antes de una tarea de varios pasos, indicar el tiempo probable, los recursos necesarios y una visión general (por ejemplo: "The average time for booking an airline ticket is 15-30 minutes"). Mostrar claramente cuándo una tarea está "in-process" y cuándo está completa (4.6.4) — [W3C COGA](https://www.w3.org/TR/coga-usable/)

**Objetivos 6–8: memoria, ayuda y personalización (COGA)**
- Login sin memorizar, copiar, calcular, resolver puzles ni reconocer caracteres distorsionados. Admitir passkeys, biometría, dispositivo de confianza e inicio de sesión de terceros. Ofrecer una opción "simple, single-step", permitir pegar en el campo de contraseña y evitar preguntas de seguridad y códigos que haya que copiar (4.7.x) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Cada paso debe contener la información necesaria para continuar, sin depender de pasos anteriores. Indicador de paso y forma simple de volver (4.7.5) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Ayuda humana fácil de encontrar en cada pantalla y paso. Formulario de contacto con "no more than 3 required fields" (4.8.1, 4.8.5) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Explicar beneficios, riesgos y consecuencias de cada opción. Pedir confirmación ante cambios inusuales o difíciles de revertir (4.8.3). Dar instrucciones al inicio del formulario, no solo en los mensajes de error (4.8.4) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Recordatorios solo "at the user's request", con el método que elija la persona. Ofrecer añadir la cita al calendario al final de la tarea. No saturar el calendario con recordatorios no deseados (4.8.7) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- El objetivo 8 incluye los patrones 4.9.1 "Let Users Control When Content Moves or Changes", 4.9.3 "Support Simplification" y 4.9.4 "Support a Personalized and Familiar Interface" (verificados solo como títulos) — [W3C COGA](https://www.w3.org/TR/coga-usable/)

**WCAG 2.2 (W3C Recommendation, 05-10-2023)**
- Publicada el 5 de octubre de 2023. Se eliminó 4.1.1 Parsing — [W3C: What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- 1.4.3 Contraste mínimo (AA): texto ≥ 4.5:1 y texto grande ≥ 3:1. 1.4.6 Contraste mejorado (AAA): ≥ 7:1 y ≥ 4.5:1 para texto grande. 1.4.11 Contraste no textual (AA): ≥ 3:1 frente a los colores adyacentes — [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 1.4.12 Espaciado de texto (AA): la interfaz debe seguir funcionando con "Line height … at least 1.5 times the font size", espaciado tras párrafo de "at least 2 times", "Letter spacing … at least 0.12 times" y "Word spacing … at least 0.16 times the font size" — [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 2.2.1 Tiempo ajustable (A): poder ajustar el límite "over a wide range that is at least ten times", o recibir un aviso antes de que expire con "at least 20 seconds to extend the time limit with a simple action". Excepción si el límite es "longer than 20 hours" — [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 2.2.2 Pausar, detener, ocultar (A): aplica al contenido que se mueve, parpadea o desplaza y que empieza solo, "lasts more than five seconds" y se presenta junto a otro contenido — [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 2.2.4 Interrupciones (AAA): "Interruptions can be postponed or suppressed by the user, except interruptions involving an emergency." 2.2.5 Reautenticación (AAA): continuar "without loss of data after re-authenticating". 2.2.6 Timeouts (AAA): avisar de la duración de la inactividad que pueda causar pérdida de datos, "unless the data is preserved for more than 20 hours" — [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 2.3.1 (A): nada que destelle "more than three times in any one second period". 2.3.3 Animación por interacciones (AAA): "Motion animation triggered by interaction can be disabled, unless the animation is essential" — [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- 2.5.5 Tamaño de objetivo mejorado (AAA): "at least 44 by 44 CSS pixels", con excepciones para controles equivalentes, en línea, del agente de usuario y esenciales — [WCAG 2.2 Understanding 2.5.5](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html)
- 2.5.8 Tamaño de objetivo mínimo (AA): 24×24 CSS px, o espaciado tal que los círculos de 24 px no se solapen. 2.5.7 Movimientos de arrastre (AA): toda acción de arrastre debe poder hacerse con un toque simple — [W3C: What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)
- 3.2.6 Ayuda consistente (A): los mecanismos de ayuda repetidos aparecen en el mismo orden relativo. 3.3.7 Entrada redundante (A): lo ya introducido en el mismo proceso se autocompleta o se puede seleccionar. 3.3.8 Autenticación accesible mínima (AA): no exigir pruebas cognitivas (recordar o transcribir una contraseña, puzles) sin una alternativa o un mecanismo de ayuda. 3.3.9 (AAA): tampoco se admiten reconocimiento de objetos ni contenido personal como única opción. Todos se describen como beneficiosos para personas con discapacidad cognitiva — [W3C: What's new in WCAG 2.2](https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/)

### Inferences
- **Reglas SpaceEase derivadas de COGA y WCAG:**
  1. Cada pantalla tiene un título que dice para qué sirve, como máximo 5 acciones principales y una acción primaria visualmente dominante.
  2. Microcopy: frases de una sola idea, párrafos de ≤ 50 palabras, listas a partir de 3 elementos y pasos numerados a partir de 3 pasos. Sin metáforas, modismos ni dobles negaciones.
  3. Sin timeouts de sesión en la app. Autoguardado continuo de borradores, por ejemplo con AsyncStorage o SecureStore al cambiar cada campo. Si un flujo externo (pago, OTP) impone tiempo, avisarlo al inicio y ofrecer ampliación con un toque y ≥ 20 s de margen (2.2.1).
  4. Toda acción produce feedback explícito de éxito o fallo, con texto + icono + haptic opcional, nunca solo color.
  5. Antes de una tarea larga (por ejemplo, configurar un perfil sensorial o un ajuste laboral), mostrar "Te llevará unos X min · Necesitas: … · Pasos: 1-2-3" y un indicador de paso simple.
  6. Login sin memoria: passkeys o Sign in with Apple, Face ID o Touch ID, magic link, pegado permitido y ningún CAPTCHA (3.3.8).
  7. Botón de ayuda humana o "¿Necesitas ayuda?" siempre en el mismo lugar en todas las pantallas (3.2.6).
  8. No volver a pedir datos ya dados (3.3.7). Mostrar lo introducido en pasos anteriores.
  9. Recordatorios desactivados por defecto. Se activan solo si la persona los pide, eligiendo canal, hora y frecuencia (COGA 4.8.7, 4.6.1).
- WCAG está pensada para la web. Aplicarla a una app nativa es una práctica habitual (traduciendo "CSS px" a puntos de iOS), pero esa equivalencia no la he verificado aquí; ver Gaps.

### Gaps
- No pude leer completas las secciones 4.9.x de COGA (personalización y simplificación) ni el apartado de "user stories"/personas. Solo verifiqué sus títulos.
- COGA no da cifras de tamaño de letra, interlineado ni duración de timeouts. Esas cifras vienen de WCAG, Apple y la BDA.
- No recuperé el texto normativo exacto de 3.3.1, 3.3.3, 3.3.4 (prevención de errores) ni de 3.1.5 (nivel de lectura) en esta sesión.
- No verifiqué la guía WCAG2ICT (aplicación de WCAG a software no web o móvil) para la equivalencia CSS px ↔ pt.
- La regla de "las 1500 palabras más comunes" es específica del inglés. No investigué un equivalente en español (por ejemplo, Lectura Fácil/UNE 153101 EX).

---

## 2. ¿Qué recomiendan los pósteres "Dos and don'ts" del UK Home Office (autismo, dislexia, baja visión, ansiedad) y la guía de estilo de la British Dyslexia Association (2023)? (Más la evidencia tipográfica de Rello y colaboradores)

### Takeaway
Los pósteres (2016, CC BY-NC-SA, repositorio archivado en octubre de 2026) piden, para autismo, colores sencillos sin contrastes chillones (pero ≥ 4.5:1), lenguaje literal, frases cortas con viñetas, botones descriptivos y layouts simples y consistentes. Para dislexia piden texto alineado a la izquierda, sin subrayado, cursiva ni mayúsculas, sin depender de la memoria ni de la ortografía y con poca información por pantalla. Para ansiedad piden tiempo suficiente, explicar qué viene después y las consecuencias, ayuda fácil de encontrar y revisar antes de enviar. La BDA fija sans serif, 12–14 pt (16–19 px), interlineado de 1.5, espaciado entre letras de ~35 % del ancho medio de letra, espaciado entre palabras de ≥ 3.5× el espaciado entre letras, títulos ≥ 20 % más grandes, fondo claro no blanco (crema o pastel), sin justificar, sin columnas, voz activa y frases cortas. La investigación de Rello respalda las fuentes sans serif o monoespaciadas, un tamaño de ~18 pt y los fondos cálidos, y no respalda las fuentes "especiales para dislexia".

### Cited Findings

**UK Home Office: contexto**
- Los pósteres cubren 7 perfiles (autismo, dislexia, baja visión, ansiedad, discapacidad física o motora, personas sordas, usuarios de lector de pantalla) y están bajo licencia "Creative Commons BY-NC-SA". El repositorio se archivó como solo lectura el 14-10-2026. El post de origen data del 02-09-2016 — [UKHomeOffice/posters README](https://github.com/UKHomeOffice/posters/blob/master/accessibility/dos-donts/README.md)

**Póster de autismo (paráfrasis del fetch)**
- (1) Usar colores sencillos y evitar los colores brillantes y contrastados, que pueden causar ansiedad o dolor, manteniendo un contraste de texto de al menos 4.5:1 y probándolo con usuarios. (2) Escribir en lenguaje llano, sin figuras retóricas ni modismos, que pueden leerse literalmente. (3) Frases simples y viñetas, sin grandes bloques de texto. (4) Botones descriptivos, nunca vagos ni impredecibles. (5) Layouts simples y consistentes, con la navegación y la búsqueda arriba y bien visibles — [UK Home Office: autism poster](https://ukhomeoffice.github.io/accessibility-posters/autism)

**Póster de dislexia (literal)**
- Do: "Use images and diagrams to support text"; "Align text to the left and keep a consistent layout"; "Consider producing materials in other formats (for example, audio or video)"; "Keep content short and simple, make clear prompts"; "Let users change the contrast between the background and text" — [UK Home Office: dyslexia poster](https://ukhomeoffice.github.io/accessibility-posters/dyslexia)
- Don't: "Don't use large blocks of heavy text"; "Don't underline words, use italics or write in capitals"; "Don't force users to remember things from previous pages - give reminders and prompts"; "Don't rely on accurate spelling. Use autocorrect or provide suggestions"; "Don't put too much information in one place" — [UK Home Office: dyslexia poster](https://ukhomeoffice.github.io/accessibility-posters/dyslexia)

**Póster de ansiedad (paráfrasis del fetch)**
- (1) Dar tiempo suficiente: no meter prisa ni poner límites de tiempo poco prácticos, porque las personas con ansiedad pueden tardar más por cautela o miedo a equivocarse. (2) Explicar qué pasa después y cuánto tarda. (3) Dejar claras las consecuencias de cada acción. (4) Ayuda fácil de alcanzar, a veces con una persona. (5) Dejar revisar y cambiar las respuestas antes de enviar — [UK Home Office: anxiety poster](https://ukhomeoffice.github.io/accessibility-posters/anxiety)

**British Dyslexia Association: Dyslexia Style Guide (texto de la página web de la BDA, que remite al PDF "Dyslexia Style Guide 2023")**
- La guía cubre correos, presentaciones, páginas web e impresos, y pide combinarla con WCAG — [BDA Dyslexia friendly style guide (copia de la página BDA en BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx); página original: [BDA](https://www.bdadyslexia.org.uk/advice/employers/creating-a-dyslexia-friendly-workplace/dyslexia-friendly-style-guide)
- Fuentes: "Use sans serif fonts, such as Arial and Comic Sans… Alternatives include Verdana, Tahoma, Century Gothic, Trebuchet, Calibri, Open Sans." — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx)
- Tamaño: "Font size should be 12-14 point or equivalent (e.g. 1-1.2em / 16-19 px). Some dyslexic readers may request a larger font." — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx)
- Espaciado: "Larger inter-letter / character spacing … ideally around 35% of the average letter width. If letter spacing is excessive it can reduce readability."; "Inter-word spacing should be at least 3.5 times the inter-letter spacing."; interlineado "proportional to inter-word spacing; 1.5/150% is preferable." — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx)
- Énfasis: evitar subrayado y cursiva ("cause crowding") y usar negrita. Evitar MAYÚSCULAS en texto continuo — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx)
- Títulos: "at least 20% larger than the normal text", con negrita si hace falta más énfasis. Espacio extra alrededor de los títulos y entre párrafos. Los enlaces deben distinguirse de títulos y texto — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx)
- Color: fondos de un solo color, sin patrones ni imágenes; "Use dark coloured text on a light (not white) background"; "White can appear too dazzling. Use cream or a soft pastel colour. Some dyslexic people will have their own colour preference." Evitar verde y rojo/rosa por el daltonismo — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx)
- Layout: "Left align text, without justification"; evitar varias columnas; "Write short simple sentences: 60 to 70 characters is optimal" (la frase mezcla longitud de frase y de línea; ver Gaps); espacio en blanco para agrupar — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx)
- Estilo de escritura: voz activa, concisión, palabras cotidianas, imágenes y diagramas de flujo para procedimientos, viñetas y numeración, instrucciones claras, sin dobles negaciones, abreviaturas desarrolladas la primera vez y glosario — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx)
- Dyslexia Scotland recomienda aumentar el espaciado entre letras y entre palabras un 30–35 % del tamaño de fuente (o según la preferencia de quien lee) y un interlineado de 1.5× (dato del snippet de búsqueda, no del fetch completo) — [Dyslexia Scotland: typed formats](https://dyslexiascotland.org.uk/dyslexia-friendly-typed-formats)

**Investigación de Rello y colaboradores**
- Rello & Baeza-Yates (ASSETS 2013), "Good fonts for dyslexia": eye-tracking con 48 personas con dislexia diagnosticada (11–50 años) y 12 fuentes. Fuentes como Arial y Helvetica fueron más fáciles de leer, y las "especiales" como OpenDyslexic no — [BYU Editing Research (resumen)](https://editingresearch.byu.edu/2020/05/28/which-fonts-are-best-for-dyslexia/); paper: [doi:10.1145/2513383.2513447](https://doi.org/10.1145/2513383.2513447)
- Rello, Pielot, Marcos, Carlini (W4A 2013), "Size Matters (Spacing Not): 18 Points for a Dyslexic-Friendly Wikipedia": 28 personas con dislexia. El interlineado no tuvo efectos significativos y se recomienda texto de 18 pt (fuente secundaria) — [a11y-paradise (resumen)](https://a11y-paradise.onrender.com/reviews/69c083aebb27ccd8963e779f); [DBLP Rello](https://dblp.dagstuhl.de/pid/50/9125.html)
- Rello, Pielot, Marcos (CHI 2016), "Make It Big!": 104 participantes y tamaños de 10 a 26 pt. La legibilidad y la comprensión mejoraron hasta 18 pt, y los interlineados extremos (el más pequeño y el más grande) se asociaron con peor comprensión (resumen secundario) — [BYU Editing Research](https://editingresearch.byu.edu/?p=10398)
- Rello & Bigham (ASSETS 2017), "Good Background Colors for Readers": 341 participantes (89 con dislexia). Los fondos cálidos (melocotón, naranja, amarillo) mejoraron la lectura frente a los fríos (azul, azul grisáceo, verde), en lectores con y sin dislexia. Todos los colores se probaron con texto negro y contraste > 7:1 — [Rello & Bigham 2017 (PDF)](https://www.changedyslexia.org/publications/pdfs/2017-ASSETS-Good%20Background%20Colors.pdf)

### Inferences
- **Tipografía SpaceEase:**
  - Fuente del sistema (SF Pro) u otra sans serif sin cursiva para el cuerpo.
  - Cuerpo por defecto de 17 pt, el estilo Body de iOS (ver la pregunta 3). Equivale aproximadamente a los 16–19 px de la BDA.
  - Ofrecer un ajuste de "texto grande" con cuerpo de ~20–22 pt, alineado con el resultado de 18 pt "tipográficos web" de Rello (es una conversión aproximada; ver Gaps).
  - Respetar Dynamic Type. Títulos ≥ 1.2× el cuerpo y en negrita.
  - Interlineado: `lineHeight = 1.5 × fontSize`.
  - Opción "espaciado amplio": `letterSpacing ≈ 0.12 × fontSize` (mínimo WCAG 1.4.12; la BDA sugiere ~35 % del ancho medio de letra).
  - Párrafos separados por ≥ 2× el tamaño de fuente.
  - Texto alineado a la izquierda, sin justificar, sin columnas y con líneas de ≤ ~60–70 caracteres. En iPad, limitar el ancho del contenedor de lectura.
  - Énfasis solo con negrita: nada de subrayado, cursiva ni MAYÚSCULAS en el texto corrido. Los enlaces se distinguen por color + icono o peso, no solo por subrayado.
- **Fondos:** en modo claro, fondo crema o cálido muy suave en lugar de `#FFFFFF`, con texto casi negro y contraste ≥ 7:1 (como en Rello & Bigham). Ofrecer selector de tema: crema, gris neutro, oscuro y un tema de bajo contraste opcional (ver la pregunta 4).
- **Contenido:** pantallas con poca información. Recordar a la persona lo que hizo en pasos previos, sin pedirle que lo memorice. Autocorrección y sugerencias en los campos de texto libre. Alternativa de audio (TTS) para los textos largos (póster de dislexia: "other formats").
- **Ansiedad:** sin cronómetros. Pantalla "¿Qué pasa después?" tras cada envío. Explicar las consecuencias en los botones destructivos. Pantalla "Revisa tus respuestas" editable antes de guardar. Ayuda humana visible.
- No usar fuentes "especiales para dislexia" (OpenDyslexic) por defecto: la evidencia de 2013 no muestra beneficio. Se pueden ofrecer como opción si la comunidad lo pide en el co-diseño.

### Gaps
- No pude descargar el PDF "BDA-Style-Guide-2023" (HTTP 403) ni la página web de la BDA (HTTP 404 en la fecha de consulta). El texto citado procede de una copia literal de la página web de la BDA alojada por Boston University (docx creado el 28-05-2024), que remite al PDF de 2023. No pude comprobar si el PDF de 2023 añade apartados específicos para web o apps.
- La frase de la BDA "Write short simple sentences: 60 to 70 characters is optimal" es ambigua: parece referirse a la longitud de línea, pero aparece como longitud de frase.
- Las fichas de los pósteres de autismo y ansiedad salieron parafraseadas (la herramienta no reprodujo el texto literal). Los pósteres de baja visión y motor no se consultaron.
- Los pósteres son de 2016, anteriores al rango 2019–2026 preferido, aunque siguen siendo referencia.
- Los resultados de "Size Matters" y "Make It Big" se obtuvieron de resúmenes secundarios, no del paper completo. La unidad "18 points" en un estudio web (pt CSS ≈ 24 px) no equivale directamente a los puntos de iOS. No encontré una conversión validada.
- No encontré estudios de Rello sobre pantallas móviles específicamente para adultos.

---

## 3. Movimiento y animación: investigación para personas neurodivergentes y con sensibilidad vestibular, Apple HIG (Reduce Motion), buenas prácticas (duraciones, easing, sin parallax ni autoplay) y háptica

### Takeaway
Apple pide que el movimiento sea intencional, breve, cancelable y opcional, y que no sea el único canal de información. Con Reduce Motion activo hay que quitar zooms, escalados y movimiento periférico, sustituir los desplazamientos por fundidos, no animar profundidad ni desenfoques y endurecer los muelles. WCAG 2.3.3 reconoce mareo, náusea y distracción, y señala el parallax como ejemplo típico. NN/g fija la mayoría de las animaciones en 100–500 ms (feedback ~100 ms, cambios de pantalla 200–300 ms, máximo ~400 ms), con ease-out y sin movimiento lineal. La háptica debe ser causal, corta, poco frecuente y desactivable. React Native expone `isReduceMotionEnabled`, `reduceMotionChanged` y `prefersCrossFadeTransitions`.

### Cited Findings
- "Add motion purposefully, supporting the experience without overshadowing it." "Don't add motion for the sake of adding motion. Gratuitous or excessive animation can distract people and may make them feel disconnected or physically uncomfortable." — [Apple HIG: Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- "Make motion optional… avoid using it as the only way to communicate important information… supplement visual feedback by also using alternatives like haptics and audio." — [Apple HIG: Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- "In apps, generally avoid adding motion to UI interactions that occur frequently." "Aim for brevity and precision in feedback animations." — [Apple HIG: Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- "Let people cancel motion… don't make people wait for an animation to complete before they can do anything, especially if they have to experience the animation more than once." — [Apple HIG: Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- Movimiento realista y coherente con el gesto: si una vista se revela deslizando hacia abajo, no se espera cerrarla deslizando hacia un lado — [Apple HIG: Motion](https://developer.apple.com/design/human-interface-guidelines/motion)
- Reduce Motion: "When this setting is active, ensure your app or game responds by reducing automatic and repetitive animations, including zooming, scaling, and peripheral motion." Buenas prácticas: endurecer los muelles para reducir el rebote, que las animaciones sigan directamente el gesto, no animar cambios de profundidad en el eje z, sustituir las transiciones en x/y/z por fundidos y no animar la entrada ni la salida de desenfoques — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- "Avoid autoplaying audio and video content without also providing controls to start and stop it." Responder al ajuste "Dim Flashing Lights" en vídeo — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- WCAG 2.3.3, intención: "Some users experience distraction or nausea from animated content". El movimiento no esencial puede causar mareo, dolor de cabeza y náusea en personas con trastornos vestibulares, y además distrae a quienes se distraen con facilidad. Ejemplo: parallax ("backgrounds move at a different rate to foregrounds"). La "motion animation" se define como "addition of steps between conditions to create the illusion of movement"; los cambios de color, desenfoque u opacidad que no alteran tamaño, forma o posición no cuentan como tal. Técnicas: evitar la animación innecesaria, ofrecer un control para desactivarla y respetar el ajuste del sistema (C39 `prefers-reduced-motion`) — [WCAG 2.2 Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html)
- WCAG 2.2.2: el contenido en movimiento que empieza solo y dura más de 5 s debe poder pausarse, detenerse u ocultarse. 2.3.1: como máximo 3 destellos por segundo — [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- Duraciones (NN/g): "the duration of most animations should be in the range of 100–500 ms". Feedback pequeño (checkbox, toggle) ≈ 100 ms; cambios de pantalla sustanciales (un modal) 200–300 ms; grandes desplazamientos hasta 400 ms ("a very slow animation"). La entrada dura algo más que la salida (por ejemplo, 300 ms de entrada y 200–250 ms de salida). A 500 ms empiezan a sentirse lentas, y es "far more common for animations to be too long than too short" — [NN/g: Executing UX Animations: Duration and Motion Characteristics](https://www.nngroup.com/articles/animation-duration/)
- Easing (NN/g): ease-out para la entrada, ease-in o ease-in-out a veces para la salida. El movimiento lineal resulta "weird and unnatural". El parallax y el scroll-jacking pueden causar mareo o náusea con trastornos vestibulares. Con "reduce motion" activado deben quitarse las animaciones — [NN/g](https://www.nngroup.com/articles/animation-duration/)
- Háptica: crear "a clear, causal relationship between each haptic and the action that causes it"; usar los patrones del sistema solo con su significado documentado; armonizar la háptica con la animación y el sonido; evitar el abuso ("can… become tiresome when it plays frequently"); preferir hápticos cortos para eventos discretos; "Let people turn off or mute haptics, and make sure people can still enjoy your app or game without them." Tipos estándar: notificación (success, warning, error), impacto (light, medium, heavy, rigid, soft) y selección — [Apple HIG: Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)
- React Native `AccessibilityInfo`:
  - Multiplataforma: `isReduceMotionEnabled()` y el evento `reduceMotionChanged`. En Android también reflejan "Transition Animation Scale" = "Animation off".
  - Solo iOS: `prefersCrossFadeTransitions()`, `isReduceTransparencyEnabled()`, `isBoldTextEnabled()`, `isDarkerSystemColorsEnabled()`, `isGrayscaleEnabled()` e `isInvertColorsEnabled()`, más los eventos `boldTextChanged` y `reduceTransparencyChanged`.
  - Solo Android: `getRecommendedTimeoutMillis()` (lee el ajuste "Accessibility timeout") e `isHighTextContrastEnabled()`.
  - Multiplataforma: `announceForAccessibility()` e `isScreenReaderEnabled()`.
  - Fuente: [React Native: AccessibilityInfo](https://reactnative.dev/docs/accessibilityinfo)

### Inferences
- **Tokens de movimiento SpaceEase:**

  | Token | Duración | Easing |
  |---|---|---|
  | `micro` (toggles, checks) | 100 ms | ease-out |
  | `standard` (entrada de tarjetas o modales) | 250 ms de entrada, 200 ms de salida | ease-out |
  | `large` (pantallas completas) | ≤ 350 ms | ease-out |

  Nunca más de 400 ms ni movimiento lineal. Nada de rebotes elásticos fuertes (usar muelles críticamente amortiguados).
- **Modo de movimiento reducido** (se activa si `isReduceMotionEnabled()` es true, si `prefersCrossFadeTransitions()` es true o si la persona lo activa en la app):
  - Sustituir las transiciones de navegación con slide o push por cross-fades de ~150–200 ms, o por cambios instantáneos.
  - Quitar escalados, zooms, parallax, fondos animados, shimmer y skeletons animados (sustituirlos por placeholders estáticos), confetti y animaciones de celebración.
  - Escuchar `reduceMotionChanged` en tiempo real.
  - Un fundido de opacidad no cuenta como "motion" según WCAG 2.3.3, así que es el sustituto seguro.
- **Ajuste propio en la app** de "Animaciones: Normal / Reducidas / Ninguna", independiente del sistema (WCAG 2.3.3 "Gx": preferencia del usuario). Algunas personas autistas o con TDAH no activan Reduce Motion en el sistema pero se benefician de él en una app concreta.
- **Sin autoplay** de vídeo, audio ni carruseles. Nada se mueve solo más de 5 s sin un botón de pausa, y ningún destello supera 3/s.
- **Animaciones interrumpibles:** la persona puede tocar o navegar durante cualquier transición, y no hay splash animados largos (HIG onboarding: splash "just long enough").
- **Háptica:** apagada o con intensidad "suave" por defecto en las acciones frecuentes. Usar `success` solo al completar tareas significativas, `selection` en pickers, y nunca `error` o `warning` como castigo. Interruptor "Vibraciones: activadas/desactivadas" en Ajustes. Toda háptica va acompañada de un cambio visual y textual. En Expo, `expo-haptics` expone esos tipos (API no verificada aquí).
- Equivalencia en Reanimated: hook `useReducedMotion` y opción `reduceMotion` por animación. Ver Gaps: no lo verifiqué en esta sesión.

### Gaps
- No encontré estudios revisados por pares que midan el efecto de la animación de UI específicamente en personas adultas autistas, con TDAH o disléxicas. La evidencia sobre el sistema vestibular y la distracción procede de WCAG Understanding y de NN/g (práctica profesional).
- No consulté la guía de accesibilidad de movimiento de Material/Android (la página de Material es de render JS). Solo verifiqué el comportamiento de "Transition Animation Scale" vía la documentación de React Native.
- No verifiqué las APIs de `react-native-reanimated` (`useReducedMotion`, `ReduceMotion.System`) ni de `expo-haptics` en esta sesión.
- Apple HIG no da duraciones numéricas para las animaciones de UI. Las cifras proceden de NN/g.

---

## 4. Diseño visual sensorialmente amable (paletas apagadas, evitar blanco y negro puros, modo oscuro), previsibilidad (una tarea por pantalla, indicadores de progreso) y reducción de ansiedad (deshacer, sin estados rojos de alarma, "omitir" y "no lo sé")

### Takeaway
Las guías AASPIRE para usuarios web autistas, co-diseñadas y evaluadas con 170 personas, piden al menos una paleta neutra de bajo contraste, temas claro y oscuro, cero fondos texturados, imágenes en movimiento y decoración sin función, una interfaz lo más simple posible, iconos redundantes con el texto, todas las funciones importantes visibles y "alternatives to definitive response items". Esa paleta de bajo contraste entra en tensión con el 4.5:1 de WCAG, que el póster de autismo también exige, así que conviene ofrecerla como opción. La BDA y Rello respaldan los fondos no blancos y cálidos. Material usa #121212 en lugar de negro puro y texto blanco al 87 %, por razones de diseño y no de estudios controlados. GOV.UK y Apple respaldan "una pregunta por página", el enlace "Atrás" y los indicadores de progreso solo si hacen falta. GOV.UK también pide mensajes de error positivos y sin culpa.

### Cited Findings

**Sensorial y visual**
- AASPIRE Web Accessibility Guidelines (Raymaker et al., 2019, *Autism in Adulthood*), accesibilidad física, en literal:
  - "Provide at least one low-contrast neutral-color palette option to accommodate sensitive vision"
  - "Provide a selection of color palettes, including one with a dark background and one with a light background"
  - "Provide a no-style option"
  - "Provide simple consistent navigation and highly consistent site behavior"
  - "Avoid textured backgrounds, moving images, decorative elements that do not convey information"
  - "Provide smaller font sizes in addition to larger ones"
  - "Use a plain accessible font such as a sans-serif font"
  - Fuente: [Raymaker et al. 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/)
- AASPIRE, accesibilidad intelectual:
  - "Use the simplest interface possible"
  - "Use simple concrete icons or images to communicate redundant information with text"
  - "Clearly label site elements with their purpose"
  - "Provide concrete examples"
  - "Minimize scrolling"
  - "Show all important features and site navigation, as opposed to within combo box drop-down areas"
  - "Make content as concise as possible without sacrificing precision and specificity"
  - Fuente: [Raymaker et al. 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/)
- AASPIRE, accesibilidad social:
  - "Be specific and precise in language; avoid colloquialisms, idioms, and ambiguity"
  - "Explain the reason behind any nonstandard instructions or unusual information"
  - "Provide alternatives to definitive response items on surveys and forms"
  - "Use FAQ formats to organize complex information"
  - "Define terms that might have different meanings depending on social context"
  - "Attend to autistic culture and community preferences"
  - Fuente: [Raymaker et al. 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/)
- Evaluación AASPIRE: 170 personas (adultos autistas, personas de apoyo y proveedores). El 97 % lo valoró fácil de usar, el 95 % fácil de entender y el 92 % lo recomendaría. No hubo asociación con el nivel educativo, el navegador ni el dispositivo. La cifra del 97 % aparece ligada a "N = 120" en el artículo, una inconsistencia interna — [Raymaker et al. 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/)
- Póster de autismo del UK Home Office: evitar colores brillantes y contrastados (pueden causar ansiedad o dolor), pero mantener un contraste de texto ≥ 4.5:1 — [UK Home Office: autism](https://ukhomeoffice.github.io/accessibility-posters/autism). **Tensión** con la "low-contrast palette option" de AASPIRE — [Raymaker et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/)
- BDA: fondo claro "not white" (crema o pastel), porque el blanco "can appear too dazzling" — [BDA (copia BU)](https://www.bumc.bu.edu/jmedday/files/2025/05/Dyslexia-friendly-style-guide.docx). Rello & Bigham 2017: los fondos cálidos mejoran la lectura — [PDF](https://www.changedyslexia.org/publications/pdfs/2017-ASSETS-Good%20Background%20Colors.pdf)
- Material Design (equipo de Android): el tema oscuro usa gris #121212 en vez de #000000. El negro puro ahorra energía en OLED, pero con imágenes brillantes el contraste resultante es mucho mayor, "which can increase eye strain". El texto usa blanco con opacidad del 87 % (alta énfasis), 60 % (media) y 38 % (deshabilitado) — [Android Developers (Medium): Dark Theme with MDC](https://medium.com/androiddevelopers/dark-theme-with-mdc-4c6fc357d956)
- Contrapunto, de un blog de diseño y no verificado en la fuente primaria: Apple usa #000000 como base oscura. El negro puro con texto blanco brillante produce "halation" (letras que parecen sangrar), sobre todo con astigmatismo — [Made Good Designs: Dark mode](https://madegooddesigns.com/dark-mode-design/)
- Apple: "Prefer system-defined colors", que se adaptan a "Increase Contrast" y al modo claro u oscuro. Comprobar el contraste mínimo "in both light and dark appearances". Si el contraste por defecto no llega al mínimo, ofrecer al menos un esquema de mayor contraste con Increase Contrast — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- Apple: "Convey information with more than color alone… Offer visual indicators, like distinct shapes or icons, in addition to color" — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)

**Previsibilidad**
- GOV.UK: "Start by asking one question per page." "Asking just one question per question page helps users understand what you're asking them to do." Incluir siempre un enlace "Atrás" arriba, que no rompa el botón atrás del navegador. Botón "Continue" (no "Next") alineado a la izquierda. Progreso: probar primero sin indicador; si la gente sigue teniendo dificultades, añadir "a simple step or question indicator"; evitar los indicadores que muestran todas las preguntas a la vez ("often not noticed", "take up lots of space") — [GOV.UK Design System: Question pages](https://design-system.service.gov.uk/patterns/question-pages/)
- Apple (Assistive Access): "Break up multistep workflows so people can focus on a single interaction per screen"; "Identify the core functionality of your app and consider removing noncritical workflows and UI elements"; "Always ask for confirmation twice whenever people perform an action that's difficult to recover from" — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- Apple: "Ensure that people can navigate your interface using easy-to-remember and consistent interactions. Prefer system gestures and behaviors people are already familiar with over creating custom gestures." — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- Apple: las vistas que se cierran solas con un temporizador "can be problematic for people who need longer to process information… Prefer dismissing views with an explicit action." — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- Apple: control de 44×44 pt por defecto (mínimo 28×28) en iOS, ~12 pt de margen alrededor de los elementos con borde y ~24 pt alrededor de los que no lo tienen. Texto Body de 17 pt por defecto (mínimo 11 pt) y ampliable al menos al 200 % — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility)
- COGA: indicador de pasos completados, actual y pendientes (4.2.4); "Atrás" que conserva el trabajo y deshacer (4.5.2, 4.5.5); aviso del tiempo y los recursos antes de una tarea (4.6.4) — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- Un estudio de 2024 con apps de movilidad urbana concluye que las personas autistas enfrentan "greater challenges of cognitive overload" (dato del resumen de búsqueda, no del fetch completo) — [arXiv 2410.14033](https://arxiv.org/abs/2410.14033)

**Reducción de ansiedad y errores**
- GOV.UK, mensajes de error: "plain English, use positive language and get to the point". Describir qué ha pasado y cómo arreglarlo. Evitar mensajes genéricos ("An error occurred"). Instrucción para los campos vacíos ("Enter your name") y descripción para los erróneos. Evitar 'forbidden', 'illegal', 'you forgot' y 'prohibited', 'please' ("implies a choice"), 'sorry' ("does not help fix the problem"), 'valid'/'invalid' y 'oops'. "Do not clear any form fields when showing the Error message" — [GOV.UK Design System: Error message](https://design-system.service.gov.uk/components/error-message/)
- Póster de ansiedad: tiempo suficiente, explicar los siguientes pasos y las consecuencias, ayuda fácil y revisar las respuestas antes de enviar — [UK Home Office: anxiety](https://ukhomeoffice.github.io/accessibility-posters/anxiety)
- Opciones "no lo sé" o no definitivas: AASPIRE pide "Provide alternatives to definitive response items on surveys and forms" — [Raymaker et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/). Las guías AASPIRE de investigación advierten de los "vague terms that might be subject to varied interpretations" en las opciones de respuesta — [Nicolaidis et al. 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6776684/)

### Inferences
- **Paleta SpaceEase:**
  - Por defecto, tonos apagados y desaturados. Fondo claro crema o cálido muy suave (no `#FFF`) con texto gris casi negro (≥ 7:1 para el cuerpo si es posible, ≥ 4.5:1 como mínimo). Fondo oscuro gris tipo `#121212` (no `#000`) con texto blanco al ~87 %.
  - Componentes no textuales (bordes de inputs, iconos de estado) ≥ 3:1.
  - Opción "Suave/bajo contraste" (AASPIRE) en Ajustes. Avisar de que reduce el contraste y que no sea el tema por defecto, para conciliarla con WCAG.
  - Respetar `isDarkerSystemColorsEnabled()` (Increase Contrast) y el modo oscuro del sistema.
- **Sin "alarma roja":** los errores se comunican con icono + texto + un color de acento no saturado (por ejemplo, ámbar o terracota apagado), sin pantallas completas en rojo ni sacudidas animadas. Los estados se diferencian también por forma o icono (Apple). Es una inferencia: no encontré un estudio que pruebe que el rojo, en concreto, aumenta la ansiedad (ver Gaps).
- **Una tarea por pantalla** en los flujos de configuración (perfil sensorial, ajustes laborales): una pregunta por pantalla, con "Atrás" siempre arriba, "Continuar" como acción primaria e indicador simple del tipo "Paso 2 de 5", solo si las pruebas lo justifican.
- **Opciones de escape en cada pregunta:**
  - "Omitir por ahora" (no bloqueante, se retoma luego).
  - "No lo sé / No estoy seguro/a" como respuesta válida.
  - "Prefiero no decirlo" en los datos sensibles (diagnóstico, salud).
  - Un enlace "¿Por qué te lo preguntamos?" que explique el motivo (AASPIRE: "Explain the reason behind any nonstandard instructions").
- **Deshacer en lugar de confirmar** en las acciones frecuentes: toast "Eliminado · Deshacer" que **no se cierra solo** o dura bastante. Apple desaconseja el auto-dismiss, así que lo mejor es un banner que la persona descarta explícitamente. Para las acciones irreversibles (borrar cuenta o datos), confirmación explícita (Apple pide confirmar dos veces) con explicación de las consecuencias.
- **Copy de errores** en español, positivo y específico: "Escribe tu correo con el formato nombre@dominio.com" en vez de "Correo inválido". Nada de "¡Ups!", "Has olvidado…", "Error" a secas ni "Lo sentimos". Nunca borrar lo escrito.
- **Pantalla "Revisa antes de guardar"** con edición en un toque. Tras guardar, "Qué pasa ahora" (por ejemplo: "Tu solicitud de ajuste está guardada. Puedes enviarla a RR. HH. cuando quieras").
- Todas las funciones importantes deben ser visibles, sin esconderlas en menús desplegables (AASPIRE). Barra de pestañas estable con como máximo 4–5 pestañas (COGA: ≤ 5 opciones principales). Gestos estándar de iOS, sin gestos personalizados ocultos.
- **Objetivos táctiles:** 44×44 pt como norma (HIG y WCAG 2.5.5 AAA), nunca menos de 24×24 (WCAG 2.5.8 AA), con 12–24 pt de separación. Toda acción de arrastre (sliders, reordenar) tiene una alternativa con botones (2.5.7).

### Gaps
- No encontré estudios controlados sobre la fatiga visual con #121212 frente a #000000, ni sobre la "halation" en el modo oscuro. Las fuentes son guías de diseño y blogs.
- No encontré evidencia empírica de que los estados de error en rojo aumenten la ansiedad en personas neurodivergentes. La recomendación de evitarlos es una inferencia de las guías ("avoid bright contrasting colours", "positive language").
- No encontré estudios específicos sobre el efecto de "Skip" o "No lo sé" en apps para adultos neurodivergentes, más allá de la pauta de AASPIRE.
- La revisión sistemática de 2026 (33 estudios) sobre interfaces para usuarios autistas que aparecía en la búsqueda no tenía una URL identificable con claridad, así que no se incluye.
- No encontré un estudio CHI/ASSETS sobre la sensibilidad sensorial de adultos autistas en apps móviles en concreto (la búsqueda solo devolvió trabajos cercanos).

---

## 5. Lenguaje neuroafirmativo y co-diseño participativo ("nothing about us without us", ASAN, identidad-primero vs persona-primero, guías AASPIRE)

### Takeaway
En inglés, la mayoría de las personas autistas adultas prefieren el lenguaje de identidad-primero ("autistic person"): ASAN lo defiende y Bottema-Beutel et al. (2021) ofrecen una tabla de alternativas no capacitistas. Pero la preferencia depende del idioma. En neerlandés, el 68,3 % de los adultos autistas prefirió "persona con autismo". En España, una encuesta de 2023 (n = 366) halló que las personas autistas usan sobre todo "autista" y luego "persona autista", mientras que familias y profesionales prefieren "TEA". No hay consenso, y la recomendación común es preguntar a la persona. AASPIRE (Nicolaidis 2019) y la investigación de HCI reciente (CHI 2022, 2023 y 2025) piden co-diseño real: reparto de poder, pago, formas múltiples de participar, tiempo para procesar y lenguaje concreto.

### Cited Findings

**Identidad-primero vs persona-primero**
- ASAN (texto de Lydia Brown, publicado originalmente en Autistic Hoya, 2011): "It is impossible to separate a person from autism"; "Autism, however, is not a disease"; el autismo es "an edifying and meaningful component of a person's identity" — [ASAN: Identity-First Language](https://autisticadvocacy.org/about-asan/identity-first-language/)
- Kenny et al. (2016, *Autism*): encuesta a 3470 personas en el Reino Unido. "Autism" y "on the autism spectrum" fueron los términos más aceptados en todos los grupos. Las personas autistas adultas y las familias aceptaron "autistic" mucho más que los profesionales, y casi la mitad de los profesionales aceptaba "person with autism". Los autores recomiendan preguntar a cada persona — [Kenny et al. 2016 (SAGE)](https://journals.sagepub.com/doi/10.1177/1362361315588200)
- Matiz: la pregunta era de selección múltiple. Cuando se elige solo un término, "autistic" es el más popular pero obtiene solo ~20 % — [BPS Research Digest](https://www.bps.org.uk/research-digest/what-correct-way-talk-about-autism-there-isnt-one)
- Bottema-Beutel et al. (2021, *Autism in Adulthood*), "Avoiding Ableist Language", alternativas sugeridas:

  | Término a evitar | Alternativa |
  |---|---|
  | "special interests" | "areas of interest or areas of expertise, focused, intense, or passionate interests" |
  | "special needs" | describir las necesidades específicas |
  | "high/low functioning" | "Describe specific strengths and needs", reconociendo que las necesidades de apoyo varían por dominio |
  | "suffering from autism" | "impact, effect" |
  | "co-morbid" | "co-occurring" |
  | "symptoms" | "characteristics, features, or traits" |
  | "treatment" | "support, services, educational strategies" |
  | "healthy controls" | "nonautistic"/"neurotypical" |
  | "autism as a puzzle" | "autism as part of neurodiversity" |
  | "cure/recovery" | resultados de calidad de vida "that prioritize what autistic people want for themselves" |
  | priorizar el "passing" | "Prioritizing mental health and well-being, which can include embracing autistic identities" |

  También recomiendan el lenguaje de identidad-primero o "on the autism spectrum" como opción relativamente neutra — [Bottema-Beutel et al. 2021 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC8992888/)
- Buijsman et al. (2022), Países Bajos y Bélgica: 414 adultos autistas de habla neerlandesa. El 68,3 % de los adultos autistas (y el 82,5 % de los padres) prefirió "persona con autismo". Los autores lo atribuyen en parte a la lengua y la cultura, y recomiendan usar ambas formas — [Buijsman et al. 2022 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC10074744/)
- España: Carbonell Renart & Resina Curado (2023), réplica de Kenny et al. con 366 personas (personas autistas, familiares y amigos, profesionales). "El concepto 'autista' es el más utilizado por los autistas para describirse a sí mismos, seguido de 'persona autista', mientras que 'TEA' es el preferido por los familiares, amigos y profesionales". "No hay un consenso único", y concluyen: "deberemos preguntar a la persona como quiere ser nombrada" (comunicación póster) — [Rev. Logopedia, Foniatría y Audiología 43 (2023), doi:10.1016/j.rlfa.2023.100459](https://doi.org/10.1016/j.rlfa.2023.100459)
- Guía en español "Hablar de autismo de otra manera" (2017, autoría no confirmada): recomienda "autista/persona autista" y "condición autista", y desaconseja "trastorno", "enfermedad" y "persona afectada de autismo" (dato del snippet de búsqueda) — [PDF](https://autcreatifs.com/wp-content/uploads/2017/07/hablar-de-autismo-de-otra-manera.pdf). Autismo España tiene un manual de estilo para medios, cuyo contenido no verifiqué — [Autismo España: manual de estilo (PDF)](https://autismo.org.es/sites/default/files/como-abordar-el-trastorno-en-los-medios.pdf)

**Co-diseño y participación**
- AASPIRE practice-based guidelines (Nicolaidis et al., 2019, *Autism* 23(8):2007–2019): etnografía institucional de 3 colaboraciones participativas (2006–2018). Para co-investigadores cubre transparencia, definición de roles, comunicación y reparto de poder, confianza, difusión y compensación justa. Para participantes cubre autonomía, consentimiento accesible, modos múltiples de participación e instrumentos adaptados — [Nicolaidis et al. 2019 (SAGE)](https://journals.sagepub.com/doi/10.1177/1362361319830523); [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC6776684/)
- Recomendaciones concretas de AASPIRE (literales):
  - "substitute difficult vocabulary words, confusing terms, or figures of speech with more straightforward terms"
  - "add hotlinks that define the term or offer examples or clarifications"
  - escalas gráficas ("cylinders filled to varying proportions; frowning/smiling faces")
  - "providing text-to-speech versions of online consent forms"
  - opciones "in-person, telephone, and online"
  - comunicación oral y escrita, síncrona y asíncrona
  - "the option to review materials in advance"
  - "Allow adequate time and space for partners to process information"
  - "actively work to equalize power"
  - "Whenever possible, use a participatory process to assess, create, and/or adapt instruments"
  - "Find ways to pay community partners"
  - Fuente: [Nicolaidis et al. 2019 (PMC)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6776684/)
- AASPIRE Web Guidelines: "Attend to autistic culture and community preferences". Las guías se desarrollaron con "autistic end-user involvement at all stages" — [Raymaker et al. 2019](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/)
- Maye & Brodersen Hansen (CHI 2025), revisión de alcance de 11 proyectos (18 papers) de co-diseño de tecnología con adultos autistas: la inclusión sigue siendo desigual, con posiciones mixtas sobre cuánto guía la perspectiva autista vivida la elección de temas y tecnologías. La mayoría de los proyectos usó infraestructuras de participación (varias formas de participar, metodología adaptada). Recomiendan aprovechar las múltiples formas de pericia de los adultos autistas — [Maye & Brodersen Hansen 2025 (UCC CORA)](https://cora.ucc.ie/items/60943f0e-62c7-40de-8642-1dc975546099)
- Barros Pena et al. (CHI 2023), "My Perfect Platform would be Telepathy": 12 sesiones de diseño participativo con 20 adultos autistas. Las plataformas sociales están "primarily designed to address neurotypical sensitivities" y fallan por falta de control del usuario, por mecanismos pobres para expresar tono e intención y por el peso de la interacción fática — [Barros Pena et al. 2023 (U. Birmingham)](https://research.birmingham.ac.uk/en/publications/my-perfect-platform-would-be-telepathy-reimagining-the-design-of-)
- Spiel, Hornecker, Williams & Good (CHI '22), "ADHD and Technology Research – Investigated by Neurodivergent Readers": la investigación tecnológica sobre el TDAH privilegia resultados neuronormativos. La tecnología se usa sobre todo para "mitigar" experiencias que se perciben como disruptivas según estándares neurotípicos, y hay poca co-construcción con personas con TDAH — [UvA DARE](https://dare.uva.nl/id/b5158a6b-ee52-48a7-b4be-772d430bad4a)

### Inferences
- **Guía de voz para SpaceEase (español):**
  1. No etiquetar a la persona en la UI: hablar de **preferencias, necesidades y ajustes**, no de diagnósticos. Por ejemplo, "Tus preferencias sensoriales" en vez de "Tus síntomas"; "Ajustes que te ayudan" en vez de "Tratamiento"; "Lo que te cuesta más" o "Lo que te agota" en vez de "Tus déficits".
  2. En el onboarding, preguntar opcionalmente "¿Cómo prefieres que nos refiramos a ti?", con las opciones "persona autista / autista", "persona con autismo", "persona con TDAH / TDAH" y "prefiero que no se mencione", y usar la respuesta en los textos. La preferencia varía por idioma y persona (Kenny, Buijsman, Carbonell Renart).
  3. En el contenido editorial genérico en español, usar "personas autistas" o "personas neurodivergentes", nunca "que padecen" ni "afectadas por". Evitar "alto/bajo funcionamiento", "grave/leve", "normal" (usar "neurotípico/a" o "no autista"), "trastorno" en el copy de la UI e "intereses especiales" (usar "intereses intensos" o "áreas de pasión").
  4. Encuadre de fortalezas y del modelo social: el problema es el entorno (ruido, luz, interrupciones), no la persona. Por ejemplo: "Este espacio tiene mucha luz fluorescente" en vez de "Tienes hipersensibilidad".
  5. Nada de lenguaje infantilizador, emojis de "ánimo" ni falsa urgencia. El tono es adulto, directo y literal.
- **Proceso de co-diseño (AASPIRE):**
  - Incluir a personas adultas autistas, con TDAH y disléxicas como co-diseñadoras pagadas, no solo como testers.
  - Ofrecer participación asíncrona por escrito además de las sesiones en vivo, y materiales previos.
  - Dar tiempo para procesar, con 2–4 rondas de respuesta.
  - Validar con ellas el glosario de términos y la paleta.
  - Documentar en el repositorio cómo se toman las decisiones (reparto de poder).

### Gaps
- No verifiqué en una fuente primaria el uso del lema "Nothing about us without us" por ASAN (la página consultada no lo menciona). Su origen en el movimiento de derechos de las personas con discapacidad no se ha citado aquí.
- No encontré estudios sobre preferencias de lenguaje de **adultos con TDAH** ("persona con TDAH" vs "TDAH" vs "ADHDer") ni de **personas disléxicas**, ni en inglés ni en español.
- El estudio español (Carbonell Renart & Resina Curado, 2023) es un resumen de póster: no tengo porcentajes ni el desglose por grupo. Tampoco verifiqué el listado de términos del manual de Autismo España.
- No consulté guías de lenguaje de organizaciones autistas latinoamericanas.

---

## 6. Patrones específicos para TDAH: reducir fricción, riesgos de la gamificación (culpa por rachas) y recordatorios que no avergüencen

### Takeaway
No encontré estudios revisados por pares sobre rachas o recordatorios en adultos con TDAH. La evidencia más sólida es general: Silverman & Barasch (JCR 2023, 7 estudios) muestran que ver una racha rota reduce la implicación posterior, que el efecto empeora cuando la persona se atribuye la ruptura y que se atenúa cuando la racha se puede "reparar". COGA y Apple dan reglas operativas: recordatorios solo a petición y configurables, interrupciones aplazables, rutas mínimas, onboarding breve, opcional y saltable, permisos en el momento de uso, niveles de interrupción honestos y ningún marketing sin consentimiento. Spiel et al. (CHI '22) advierten contra diseñar para "mitigar" el TDAH según normas neurotípicas.

### Cited Findings
- Silverman & Barasch (2023), "On or Off Track: How (Broken) Streaks Affect Consumer Decisions", *Journal of Consumer Research* 49(6):1095–1117. En 7 estudios, mostrar una racha intacta en un registro aumentó la implicación posterior frente a mostrar una racha rota, con independencia de la conducta real. El efecto se amplifica cuando la persona atribuye la ruptura a sí misma y se debilita cuando la reparación es posible — [UDSpace (U. Delaware)](https://udspace.udel.edu/items/42ce576b-8e1f-429a-8541-e29e48dbcfbb)
- Según la nota de prensa de CU Boulder (paráfrasis de prensa, no del paper), los mensajes que destacan un fallo reciente con un empujón para "volver al camino" no suelen funcionar, y la gente abandona cuando su racha se rompe — [CU Boulder Leeds School of Business](https://www.colorado.edu/business/faculty-research/2023/04/19/or-track-how-broken-streaks-affect-consumer-decisions)
- Testimonios anecdóticos de desarrolladores (no evidencia empírica) describen el ciclo racha rota → vergüenza → abandono, y mensajes del tipo "You missed 3 days" que generan culpa — [DEV Community (blog de desarrollador)](https://dev.to/nucleusos/why-streaks-make-adhd-worse-and-what-actually-helps-5147)
- Spiel et al. (CHI '22): la tecnología para TDAH se orienta mayoritariamente a "mitigar" experiencias percibidas como disruptivas según normas neurotípicas, con poca co-construcción y con resistencia de los participantes al encuadre de déficit — [UvA DARE](https://dare.uva.nl/id/b5158a6b-ee52-48a7-b4be-772d430bad4a)
- COGA: recordatorios solo "at the user's request" y con el método elegido. Interrupciones controladas por la persona. Pop-ups que no bloqueen. Rutas críticas con "the minimally necessary steps". Como máximo 5 opciones principales por pantalla. Guardar el trabajo sobre la marcha. Indicar el tiempo y los recursos antes de una tarea — [W3C COGA](https://www.w3.org/TR/coga-usable/)
- WCAG 2.2.4 (AAA): las interrupciones se pueden aplazar o suprimir, salvo emergencias — [WCAG 2.2](https://www.w3.org/TR/WCAG22/)
- Notificaciones en iOS:
  - Niveles de interrupción: Passive ("view at their leisure"), Active (por defecto), Time Sensitive ("requires their immediate attention") y Critical (salud y seguridad, requiere entitlement).
  - "Build trust by accurately representing the urgency of each notification."
  - Time Sensitive solo para un evento "happening now or will happen within an hour".
  - "Don't use notifications to send marketing or promotional content unless people explicitly agree."
  - Ofrecer "an in-app settings screen that lets people change their choice".
  - Focus y "scheduled summary" permiten a la persona filtrar y agrupar.
  - Fuente: [Apple HIG: Managing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications)
- Onboarding (Apple): "design a flow that's fast, fun, and optional"; "doesn't require people to memorize a lot of information"; si se salta el tutorial, "don't present it again on subsequent launches, but make sure it's easy for people to find"; enseñanza interactiva donde la persona "can safely test an action"; "Postpone nonessential setup flows or customization steps"; pedir permisos "when people first access the specific function"; "Prefer letting people experience your app… before prompting them for ratings or purchases" — [Apple HIG: Onboarding](https://developer.apple.com/design/human-interface-guidelines/onboarding)
- Apple: evitar las vistas que se cierran solas con un temporizador y preferir el cierre explícito — [Apple HIG: Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility). Android expone el ajuste del sistema "Accessibility timeout" vía `getRecommendedTimeoutMillis()` — [React Native AccessibilityInfo](https://reactnative.dev/docs/accessibilityinfo)

### Inferences
- **Sin rachas punitivas.** Si se registra la constancia, mostrar el **total acumulado** ("Has usado tus ajustes 23 días") en lugar de la racha consecutiva. Si hay racha, debe ser reparable, tener días de gracia y no mostrar nunca un contador roto ni un "0" (Silverman & Barasch: la reparación atenúa el efecto negativo y la autoatribución lo agrava). Sin pérdidas, castigos, puntos negativos ni rankings sociales.
- **Copy de reentrada sin culpa.** Nunca "Has perdido 3 días" ni "Te echamos de menos". Usar en su lugar "Bienvenido/a de nuevo. ¿Retomamos donde lo dejaste?" o "Todo está como lo dejaste", que destacan la continuidad y no la falta.
- **Recordatorios:**
  - Desactivados por defecto.
  - La persona elige qué, cuándo (hora concreta o franja), por qué canal y con qué frecuencia.
  - Cada notificación ofrece las acciones "Hecho", "Más tarde (posponer 1 h / mañana)" y "No volver a recordarme esto".
  - Interruption level Passive o Active. Time Sensitive nunca, salvo un evento propio de la persona en < 1 h. Cero marketing sin opt-in explícito.
  - Agrupar en el resumen programado de iOS cuando se pueda.
  - Respetar Focus.
  - Pantalla de Ajustes > Notificaciones dentro de la app.
- **Reducir fricción (TDAH):**
  - Acción principal en ≤ 2 toques desde el inicio.
  - Captura rápida (un campo y "Guardar"; los detalles, después).
  - Valores por defecto razonables y autoguardado.
  - Sin formularios largos. Flujos reanudables desde donde se dejaron.
  - Sin modales que bloqueen. Sin pedir valoración en la App Store durante una tarea.
  - Permisos (notificaciones, ubicación) solo cuando se usa la función concreta.
- **Onboarding SpaceEase:** de 3 a 5 pantallas como máximo, con "Omitir" visible en todas. Explica qué hace la app y cuánto tarda la configuración ("2 minutos"). Si se omite, no reaparece, y queda accesible en Ajustes > "Ver introducción". Login diferido o sin contraseña.
- **Encuadre:** las funciones se presentan como herramientas que la persona elige ("Configura tu entorno"), no como correcciones de su conducta ("Mejora tu concentración"), en línea con Spiel et al. 2022.

#### Resumen transversal por área (checklist SpaceEase, con las cifras clave)

| Área | Regla implementable | Cifra o umbral | Fuente principal |
|---|---|---|---|
| Layout | 1 tarea o pregunta por pantalla; ≤ 5 acciones principales; acción primaria dominante; funciones importantes visibles (no en desplegables); fondo liso | ≤ 5 opciones | COGA 4.6.3; GOV.UK; AASPIRE |
| Lenguaje | Literal, presente, voz activa; 1 idea por frase; párrafos ≤ 50 palabras; listas desde 3 ítems; sin modismos ni dobles negaciones; jerga explicada a 1 toque | ≤ 50 palabras por párrafo | COGA 4.4.x; UK HO autismo; BDA |
| Tipografía | Sans serif; cuerpo de 17 pt con Dynamic Type hasta ≥ 200 %; interlineado de 1.5; títulos ≥ 1.2×; solo negrita para el énfasis; izquierda sin justificar; líneas de ~60–70 caracteres; opción de espaciado amplio | 17 pt; 1.5; 0.12 em; ≥ 20 % | Apple HIG; WCAG 1.4.12; BDA; Rello |
| Color y contraste | Texto ≥ 4.5:1 (objetivo 7:1); no texto ≥ 3:1; fondo claro crema (no `#FFF`); oscuro `#121212` con texto al 87 %; tema bajo contraste opcional; nunca solo color | 4.5:1 / 7:1 / 3:1 | WCAG 1.4.3/1.4.6/1.4.11; BDA; Material; AASPIRE |
| Movimiento | 100 ms micro; 200–300 ms estándar; ≤ 400 ms; ease-out; sin parallax, autoplay ni zoom; fundidos con Reduce Motion; ajuste propio en la app; interrumpible | 100–400 ms; 5 s; 3 destellos/s | Apple HIG; NN/g; WCAG 2.2.2/2.3.1/2.3.3 |
| Feedback | Éxito o fallo explícito en cada acción con texto + icono (+ háptica opcional); háptica causal, corta, desactivable | — | COGA 4.5.10; Apple Haptics |
| Navegación | Tab bar estable; "Atrás" siempre conserva el estado; ayuda en el mismo lugar; gestos estándar; alternativa al arrastre | — | COGA 4.5.2; WCAG 3.2.6, 2.5.7; Apple |
| Objetivos táctiles | 44×44 pt por defecto; nunca < 24×24; separación de 12–24 pt | 44 / 24 pt | Apple HIG; WCAG 2.5.5/2.5.8 |
| Errores | Mensaje positivo, específico, con cómo arreglarlo; no borrar datos; deshacer; sin rojo de alarma ni "Ups"; revisión antes de guardar | — | GOV.UK; COGA 4.5.x; UK HO ansiedad |
| Tiempo | Sin timeouts; autoguardado; sin auto-dismiss; si hay límite externo, aviso + ≥ 20 s para ampliar | 20 s; ×10; 20 h | WCAG 2.2.1/2.2.6; COGA 4.5.9; Apple |
| Notificaciones | Opt-in; la persona elige canal y hora; posponer o silenciar; nivel Passive/Active; Time Sensitive solo < 1 h; sin marketing; ajustes en la app | < 1 h | COGA 4.6.1/4.8.7; Apple Notifications; WCAG 2.2.4 |
| Onboarding | Breve, opcional, "Omitir" siempre, no reaparece, interactivo; permisos al usar la función; login sin memoria (passkeys o Face ID) | 3–5 pantallas (inferencia) | Apple Onboarding; WCAG 3.3.8; COGA 4.7 |
| Formularios | "No lo sé", "Omitir" y "Prefiero no decirlo"; explicar por qué se pregunta; no repetir datos; aceptar formatos; autocorrección y sugerencias | — | AASPIRE; WCAG 3.3.7; UK HO dislexia |
| Lenguaje afirmativo | Preferencias y ajustes, no síntomas ni déficits; preguntar cómo nombrar a la persona; modelo social | — | Bottema-Beutel 2021; Carbonell Renart 2023; ASAN |
| Gamificación | Sin rachas punitivas; totales acumulados; reparación y gracia; sin pérdidas, rankings ni copy de culpa | — | Silverman & Barasch 2023 |

### Gaps
- No encontré estudios revisados por pares sobre rachas, gamificación o diseño de recordatorios **específicamente en adultos con TDAH**. Lo encontrado son blogs de desarrolladores o vendedores con estadísticas sin fuente verificable. Una cifra sobre retención con gamificación ("48 % más en JMIR Serious Games 2022") no se pudo verificar y se excluye.
- No encontré evidencia empírica sobre la frecuencia o el tono óptimos de los recordatorios para personas con TDAH.
- Las cifras del onboarding (3–5 pantallas) y de la "acción principal en ≤ 2 toques" son inferencias de diseño, no umbrales de una guía.
- No investigué el "body doubling", los temporizadores visuales tipo Pomodoro ni la "time blindness" en apps. Son patrones populares en la comunidad TDAH, pero no se verificaron aquí.
