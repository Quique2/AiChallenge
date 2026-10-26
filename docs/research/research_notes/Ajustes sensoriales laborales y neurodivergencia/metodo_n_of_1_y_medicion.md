# Método n-of-1, EMA, medidas breves y personalización por persona (base para SpaceEase)

*Notas en español; citas textuales en inglés. Etiquetas de evidencia: **[Alta]** guía de consenso, RCT o meta-análisis grande; **[Moderada]** estudio empírico controlado o revisión sistemática pequeña; **[Baja]** piloto, tesis, preprint, fuente secundaria o nota de prensa. **[Seminal]** = fuente metodológica clásica anterior a 2015. Fecha de consulta: 2026-10-26.*

## 1. ¿Producen los ensayos n-of-1 y los autoexperimentos personales (StudyMe, Self-E, "personal science", Quantified Self) conclusiones personales válidas y útiles? Trampas y diseño mínimo recomendado

### Takeaway
Los n-of-1 bien diseñados (varios ciclos A/B aleatorizados, medición repetida, análisis que tenga en cuenta la autocorrelación) son un método reconocido para tomar decisiones individuales, y sus resultados cambian decisiones en aproximadamente la mitad de los casos. Las apps para usuarios no expertos (StudyMe, Self-E) son usables y factibles, pero la evidencia de que *mejoren resultados* es débil (PREEMPT fue negativo en su resultado primario). Las amenazas principales en autoexperimentos sin cegamiento son la expectativa/placebo (fuerte: el microdosing autociego no superó al placebo), las creencias previas del usuario, la regresión a la media, la autocorrelación y tener muy pocas repeticiones. Self-E ya usa distribuciones Beta + Thompson sampling con calificaciones 1–5, igual que SpaceEase, y da el resultado cuando hay al menos 3 días por condición.

### Cited Findings
**Estándares y guías metodológicas**
- CENT 2015 (CONSORT Extension for N-of-1 Trials) es la guía de reporte de n-of-1 basada en CONSORT 2010. Tiene declaración principal (Vohra et al., BMJ 2015;350:h1738) y documento de explicación y elaboración (Shamseer et al., BMJ 2015;350:h1793). Añade guía específica a 14 de los 25 ítems de CONSORT 2010 y recomienda un diagrama para representar cada ensayo individual. [Alta; guía de reporte, no de diseño] — [BMJ E&E](https://www.bmj.com/content/350/bmj.h1793); [NOF1 Society, CENT 2015](https://www.nof1sced.org/resources/guidelines-standards/guidelines-cent-2015). *Nota: no pude descargar el texto completo de BMJ (HTTP 403), así que no verifiqué el texto literal sobre washout ni número de periodos.*
- La guía de AHRQ "Design and Implementation of N-of-1 Trials: A User's Guide" (Kravitz y Duan, eds., AHRQ Pub. No. 13(14)-EHC122-EF, febrero de 2014) es la referencia práctica de diseño en EE. UU. [Alta; Seminal] — [registro del catálogo](https://pedpalascnetlibrary.omeka.net/items/show/14798). *La copia en PDF de AAFP devolvió 404, así que no extraje sus recomendaciones textuales.*
- Una referencia clínica secundaria dice que "generally recommended that an n-of-1 trial includes a minimum of three cycles of treatment". [Baja; secundaria, sin verificar contra AHRQ] — [GPnotebook](https://gpnotebook.com/pages/evidence-based-medicine/n-of-1-trial).
- Las diapositivas de C. Schmid (2024) indican que los n-of-1 pueden necesitar washout para controlar el carryover. También listan entre las indicaciones del método que la persistencia del efecto sea despreciable (es decir, sin carryover). [Moderada; experto en el área] — [Schmid 2024](https://medstat.umg.eu/fileadmin/Redaktion/Medizinische_Statistik/Dokumente/Vortr%C3%A4ge/2024_Presentation-Chris-Schmid.pdf).
- Diseños de caso único (What Works Clearinghouse): una fase con ≥5 datos "cumple sin reservas", con 3–4 datos "cumple con reservas" y con <3 "no cumple". [Moderada; estándar educativo] — [tabla WWC en PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC3992321/table/T1). La División de Investigación del CEC criticó la exigencia de 5 puntos por rígida y propuso que a veces basten menos. — [CEC-DR position statement](https://cecdr.org/sites/default/files/2021-01/_DR_Position_Statement_5_data_points_WWC_SCD_final.pdf).

**Potencia y número de repeticiones**
- Estudio de potencia en n-of-1 cruzados con 400 observaciones totales y un efecto de 0,3 DE:
  - Sin autocorrelación (ρ=0), la potencia es 0,851 con cualquier número de periodos.
  - Con ρ=0,5, la potencia sube de 0,330 (un solo par A/B) a 0,674 (40 pares). Con ρ=0,75 sube de 0,126 a 0,681.
  - Alternar más veces compensa en parte la autocorrelación.
  - El washout reduce un poco la potencia y solo conviene si se espera carryover.
  - La potencia para *detectar* carryover es baja en todos los escenarios.
  - Con autocorrelación fuerte, el tamaño del efecto pesa más que las decisiones de diseño (0,9 DE con ρ=0,75 y 4 pares: potencia 0,842).
  - Limitaciones: modelo AR(1), dos intervenciones y respuesta constante.
  
  [Moderada; simulación/analítico] — [Power and Design Issues in Crossover-Based N-of-1 Trials (PMC6787650)](https://pmc.ncbi.nlm.nih.gov/articles/PMC6787650/).

**¿Son útiles? Evidencia empírica**
- Revisión sistemática de n-of-1 médicos publicados entre 1985 y 2010: 108 ensayos con 2.154 participantes. De los 488 participantes con información sobre cambio de tratamiento, el 54% tomó decisiones posteriores coherentes con el resultado del ensayo, el 8% decisiones contrarias y el 38% tuvo resultados ambiguos. [Alta/Moderada; revisión sistemática] — [Gabler et al., Med Care 2011](https://pubmed.ncbi.nlm.nih.gov/21478771/).
- PREEMPT (RCT, JAMA Intern Med 2018;178(10)): 215 pacientes con dolor musculoesquelético crónico (108 asignados a n-of-1 multi-crossover apoyado por la app "Trialist" y 107 a atención habitual). La app fue factible y tuvo experiencia de usuario satisfactoria, pero **no mejoró significativamente la interferencia del dolor a 6 meses** frente a la atención habitual. [Alta; RCT] — [Healio](https://www.healio.com/news/orthopedics/20180904/musculoskeletal-pain-did-not-improve-with-use-of-mobile-health-app); [eScholarship PDF](https://escholarship.org/content/qt3pn8j188/qt3pn8j188.pdf).
- StudyMe (Zenner, Böttinger, Konigorski, *Trials* 2022), app abierta para n-of-1 centrados en el usuario:
  - Diseño por defecto ABAB con fases de 7 días (28 días en total). Las fases van emparejadas (AB/BA) y en orden alternado (ABAB) o contrabalanceado (ABBA). Los autores advierten que las secuencias desbalanceadas "can yield challenges in the statistical analysis when temporal effects are present".
  - Encuesta (n=272): las ideas de intervención de los usuarios eran poco específicas; por ejemplo, 114 menciones de "exercise" sin especificar frente a 55 que sí nombraban una actividad.
  - Evaluación (n=13): todos crearon un ensayo y el SUS medio fue 82/100 (rango 60–100). Un usuario redujo el diseño a un solo par AB, que los autores califican de "not an optimal design".
  - No incluye cegamiento ni aleatorización ("challenging to execute in self-defined and self-administered trials").
  - El análisis es descriptivo. No recomienda un número mínimo de ciclos; elegir el número de observaciones diarias, la duración y la estructura es "not trivial".
  
  [Baja/Moderada; evaluación de usabilidad hecha por los propios autores] — [StudyMe, PMC9793632](https://pmc.ncbi.nlm.nih.gov/articles/PMC9793632/).
- Self-E (Daskalova et al., CHI 2021), el análogo más cercano a SpaceEase:
  - Cada experimento tiene dos condiciones ("Today, meditate" / "Today, don't meditate") aleatorizadas por día.
  - El efecto se mide **solo con una calificación 1–5**, con un máximo de 5 check-ins al día (6:00–23:45). Se eligió así porque los cuestionarios largos y la fatiga de registro dañan la calidad de los datos.
  - El análisis usa **distribuciones Beta actualizadas con cada dato y Thompson sampling**: se muestrea 1.000 veces de cada Beta y se convierte en "porcentaje de probabilidad de que la condición ayude". El resultado solo se calcula cuando hay **≥3 días en cada condición**.
  - Frase de resultado mostrada: "Based on the 8 days of data tracked so far, it is most likely (about 73% likelihood) that your energy level is 0.8 levels higher when you meditate in the morning". Los usuarios la encontraron clara; uno dijo: "what was ultimately more helpful was the result sentence".
  - Las intervenciones preconfiguradas se eligieron para que fueran poco propensas al carryover.
  
  [Moderada/Baja; estudio cualitativo con n=16 locales + segundo estudio con usuarios experimentados] — [Self-E PDF](https://jeffhuang.com/papers/SelfE_CHI21.pdf).
- Self-E, adherencia y sesgos:
  - El cumplimiento de la condición asignada fue del 73%, frente a 22,5% en QuantifyMe, 60% en SleepBandits y 95% en TummyTrials.
  - Cuando no podían cumplir, los usuarios "do the best [they] could", es decir, sustituían la conducta por otra parecida.
  - Algunos evitaban la condición que creían "dañina" aunque ellos mismos habían configurado el experimento. Cuando el resultado contradecía sus creencias, desconfiaban y buscaban confusores.
  - Los autores proponen introducir esas creencias como *priors* del Thompson sampling, pero advierten que "feeding assumptions as priors might lead to potential biases".
  - Los usuarios experimentados acotaron variables amplias como "mood" a indicadores más específicos (irritabilidad, sueño, etc.). Uno eliminó una variable dependiente para reducir el carryover.
  
  [Moderada/Baja] — [Self-E PDF](https://jeffhuang.com/papers/SelfE_CHI21.pdf).
- Personal science (Wolf y De Groot, 2020): la definen como "using empirical methods to pursue personal health questions", con cinco actividades (questioning, designing, observing, reasoning, discovering) extraídas de prácticas de la comunidad Quantified Self. Comparan esta práctica con la ciencia ciudadana y los n-of-1 médicos y discuten barreras de adopción. [Baja/Moderada; artículo de perspectiva conceptual, sin datos de validez] — [Frontiers in Computer Science 2020](https://www.frontiersin.org/article/10.3389/fcomp.2020.00021/full).
- Existe una propuesta de análisis bayesiano centrado en el paciente para autoexperimentos (Schroeder, Karkar, Fogarty, Kientz, Munson, Kay, J Healthc Inform Res 2019;3(1):124–155). Es de la línea de trabajo de TummyTrials (SII, desencadenantes alimentarios) y del marco de autoexperimentación de Karkar et al. (JAMIA 2016). [Moderada; solo verifiqué la cita bibliográfica] — [AHRQ Digital, cita](https://digital.ahrq.gov/ahrq-funded-projects/sharing-patient-lifelog-data-primary-care-team-two-patient-populations/citation/patient).
- Un capítulo-primer reciente (Daza, agosto de 2026) revisa los n-of-1 y los diseños de caso único para datos digitales densos de una sola persona ("small data", "esametry"). [Baja; preprint, solo leí el abstract] — [arXiv 2608.15526](https://arxiv.org/abs/2608.15526).

**Trampas: expectativa/placebo y regresión a la media**
- Microdosing con autocegamiento (Szigeti et al., eLife 2021): 191 participantes completaron el estudio, con placebos en cápsulas opacas y códigos QR. Todos los resultados psicológicos mejoraron desde la línea base en el grupo de microdosis, pero **el grupo placebo también mejoró y no hubo diferencias significativas entre grupos**. Las pequeñas diferencias se explican por participantes que rompieron el ciego. Ejemplo directo de cómo la expectativa domina el efecto percibido en autoexperimentos sin cegamiento. [Moderada/Alta; ensayo controlado con placebo en ciencia ciudadana] — [eLife 62878](https://elifesciences.org/articles/62878).
- Regresión a la media (Barnett, van der Pols, Dobson, Int J Epidemiol 2005): la variación normal en mediciones repetidas puede parecer un cambio real. El efecto crece con el error de medición y cuando solo se sigue a quienes fueron seleccionados por un valor basal extremo. Debe considerarse siempre como posible causa del cambio observado. Remedios: grupo control, ajuste por la línea base (ANCOVA) y medir la línea base en un momento distinto del que sirvió para la selección. [Alta; Seminal] — [PubMed 15333621](https://pubmed.ncbi.nlm.nih.gov/15333621/).

### Inferences
- El bucle de SpaceEase (dificultad → calificación previa 1–5 → un ajuste → trabajar → calificación posterior) es un **diseño AB dentro de cada episodio, sin condición control**. La diferencia pre/post confunde el efecto del ajuste con:
  - **Regresión a la media**: el usuario registra el episodio justo cuando la dificultad es alta, así que la calificación previa está seleccionada por ser extrema y la posterior tenderá a mejorar sin que haga falta ningún ajuste.
  - **Expectativa**: el usuario sabe qué ajuste aplicó y espera que funcione.
  - **Fatiga por tiempo en tarea**: trabajar cansa, lo que sesga en contra del ajuste.
  - **Contexto**: hora del día, tipo de tarea.
  
  Por eso, la mejora pre/post *media* sobreestimará la eficacia de *todos* los ajustes por igual. La comparación válida es **entre ajustes** (o frente a un brazo "sin cambio / ajuste mínimo") en contextos parecidos, no la mejora absoluta.
- Opciones de bajo coste, en línea con Self-E y StudyMe:
  - Incluir de vez en cuando un brazo de control ("hoy, trabaja sin cambiar nada y califica igual") o un ajuste neutro.
  - Calcular la recompensa como *diferencia frente a la mejora típica del propio usuario* (línea base personal móvil), no como un umbral absoluto de +1.
  - Pedir de vez en cuando una segunda calificación basal (por ejemplo, al abrir la app sin haber registrado dificultad) para estimar la regresión a la media.
- Umbrales razonables para mostrar al usuario "esto parece funcionarte":
  - **≥3 episodios por ajuste** (criterio de Self-E) como mínimo para un mensaje *tentativo*.
  - **≥5** (heurística WWC de puntos por fase) para un mensaje *más firme*.
  - Siempre con lenguaje probabilístico ("probablemente", "en 6 de 8 veces").
  
  Con autocorrelación y efectos pequeños, ni 10 pares dan una potencia alta (PMC6787650). Por eso SpaceEase debería presentar resultados como **orientaciones revisables** y no como verdades.
- Los ajustes ambientales (auriculares, cambiar la luz, moverse de sitio) suelen tener inicio y fin rápidos, lo que favorece el n-of-1 porque hay poco carryover. Aun así, cambios persistentes en el espacio (reordenar el escritorio) generan carryover entre episodios. Conviene marcar los ajustes "persistentes" y no compararlos episodio a episodio.
- La creencia previa del usuario sesga tanto el cumplimiento como la confianza (Self-E). SpaceEase puede pedir la expectativa antes de aplicar el ajuste ("¿crees que te ayudará?") y usarla como covariable o para explicar resultados sorprendentes, en lugar de meterla como prior fuerte.

### Gaps
- No obtuve el texto completo de CENT 2015 (BMJ 403) ni de la guía AHRQ (PDF 404). Sus recomendaciones textuales sobre número de ciclos, washout y análisis quedan sin verificar; la cifra de "≥3 ciclos" viene de una fuente secundaria.
- No verifiqué los requisitos de WWC sobre "tres demostraciones del efecto" ni sobre el número de repeticiones en diseños de tratamientos alternados.
- No encontré estudios de n-of-1 o autoexperimentos sobre **ajustes ambientales/sensoriales en el trabajo** ni con población **autista o TDAH** específicamente.
- No hay evidencia publicada de validez *predictiva* de las conclusiones de apps como StudyMe o Self-E (si lo que "funciona" según la app sigue funcionando después).
- No leí el texto completo de Schroeder et al. 2019 ni de TummyTrials (diseño y número de días).

## 2. EMA / muestreo de experiencias con adultos autistas y con TDAH: factibilidad, cumplimiento, carga, frecuencia y adaptaciones de accesibilidad

### Takeaway
En adultos autistas (jóvenes y de mediana edad, con inteligencia y lenguaje en rango medio o superior) la EMA es aceptable y factible, con una tasa de respuesta media de ~72% (rango 40–100%). La frecuencia de muestreo no se asoció con la respuesta; la longitud del cuestionario sí importa. Hay adaptaciones claras: lenguaje simple, apoyos visuales, anclas "nada / mucho", ventanas horarias personalizables, entradas iniciadas por el usuario y modo vibración. En TDAH adulto la EMA se ha implementado con éxito, pero no encontré tasas de cumplimiento publicadas específicas de adultos con TDAH. El referente general es ~79% de cumplimiento con ~6 avisos al día durante 7 días, y los incentivos económicos lo aumentan.

### Cited Findings
**Autismo**
- Revisión sistemática de EMA en autismo (Chen, Xi, Greene, Mandy, *Autism* 2024/2025): 32 estudios con 930 participantes autistas.
  - Respuesta en muestreo por señal (k=21): media 72,1% (DE 13,4; rango 40–100%). En muestreo por intervalo (k=5): 75,1% (DE 20,7; rango 53,7–100%). Los autores concluyen que "~72% appears to be acceptable and adequate".
  - Un estudio con 7 cuestionarios al día tuvo 34% de cumplimiento. En dos estudios de 14 días la respuesta bajó con el tiempo.
  - **La frecuencia de muestreo no se correlacionó con la tasa de respuesta** (r = −0,06, p = 0,802).
  - Los cuestionarios tenían de 1 a 38 ítems (media 12,2). Los 8 estudios que reportaron tiempo de respuesta tardaban menos de 5 minutos.
  - La evidencia de aceptabilidad y factibilidad se limita a adultos jóvenes y de mediana edad con inteligencia y lenguaje en rango medio o superior.
  
  [Alta/Moderada; revisión sistemática] — [Chen et al., PMC12089685](https://pmc.ncbi.nlm.nih.gov/articles/PMC12089685/).
- Adaptaciones recomendadas en esa misma revisión:
  - "easy and straightforward language" y apoyos visuales.
  - Formatos simples (preguntas dicotómicas o sliders) y, para respuestas abiertas, permitir dibujo o grabación oral.
  - Anclas "very slightly" / "extremely" sustituidas por **"not at all" / "a lot"**.
  - Ventanas horarias personalizadas (solo horas de vigilia; distintas entre semana y fin de semana).
  - **Ensayos iniciados por el participante** para reducir la frustración de ser interrumpido.
  - Control de volumen o modo vibración.
  - Ráfagas de medición con descansos, cuestionarios cortos con ramificación, y descartar los primeros registros mientras se aprende el procedimiento.
  - Conversaciones de seguimiento para aclarar respuestas ambiguas y consulta con colaboradores autistas.
  - Los incentivos económicos se asociaron a más respuesta "irrespective of the monetary amount". Recomiendan considerar los intereses especiales como recompensa.
  - **No se reportaron adaptaciones sensoriales específicas**.
  
  [Alta/Moderada] — [Chen et al., PMC12089685](https://pmc.ncbi.nlm.nih.gov/articles/PMC12089685/).
- Piloto de EMA sobre ocio en adultos autistas (Song et al., 2023): 40 participantes completaron la encuesta diaria una media de 27,05 de 30 días (DE 3,92). La mayoría encontró el horario conveniente y las respuestas fáciles de introducir. [Baja/Moderada; piloto] — [ICI, U. Minnesota](https://ici.umn.edu/products/5Nhz9CiyQFuDDh-eybFKcg).
- Contraejemplo: intervención momentánea ecológica de una semana (n=31) en adultos autistas. La retención fue alta, pero la adherencia autorreportada quedó por debajo del umbral a priori del 80% y la aceptabilidad tampoco alcanzó su umbral. [Baja; tesis doctoral] — [Drexel, tesis](https://researchdiscovery.drexel.edu/esploro/outputs/graduate/Feasibility-acceptability-and-efficacy-of-an/991022170253304721).
- EMA de experiencias sensorias diarias (41 adultos autistas, 3 cuestionarios al día durante 2 semanas): las experiencias sensoriales positivas, negativas y neutras se asociaron con el entorno y el contexto (lugar, compañía, estado de ánimo), **no** con las puntuaciones en escalas estandarizadas de rasgos autistas. [Baja; tesis de máster] — [Western University, tesis](https://ir.lib.uwo.ca/etd/10304).
- Grupos focales con 18 adultos autistas: hipersensibilidades visuales (luz, movimiento, patrones, colores) que contribuyen a la distracción. [Moderada; cualitativo] — [Parmar et al., Frontiers in Psychology 2021](https://www.frontiersin.org/articles/10.3389/fpsyg.2021.633037/full).

**TDAH**
- Revisión sistemática de EMA en TDAH (2018): 23 estudios, solo 8 exclusivamente con adultos. Concluye que "ecological momentary assessment can be successfully implemented with attention-deficit/hyperactivity disorder patients". El seguimiento máximo fue de 28 días y piden periodos más largos. [Moderada] — [Miguélez-Fernández et al., 2018](https://produccioncientifica.ucm.es/documentos/5eef3b902999522e441e6b3a?lang=en).
- Revisión de e-diarios en TDAH: 20 estudios con niños y adolescentes y 13 con adultos. Concluye que el ambulatory assessment sirve para captar patrones dinámicos. [Moderada] — [U. Bristol, "Using e-diaries to investigate ADHD"](https://research-information.bris.ac.uk/en/publications/using-e-diaries-to-investigate-adhd-state-of-the-art-and-the-prom/).
- Precedente de diseño intensivo (Knouse et al.): 206 adultos jóvenes con hasta 56 evaluaciones momentáneas en una semana mediante PDA. No obtuve su tasa de cumplimiento. [Moderada; Seminal ~2008] — [EdITLib](https://mail.editlib.org/p/69133).
- Piloto con 13 chicas adolescentes con TDAH: "high level of compliance" (población no adulta). [Baja] — [PMC7294398](https://pmc.ncbi.nlm.nih.gov/articles/PMC7294398).
- Predictores de no respuesta en jóvenes (sin diagnóstico de TDAH medido):
  - Menor autocontrol se asoció a menor adherencia, pero solo en análisis sin ajustar.
  - Más estrés y afecto negativo en el momento predijeron perder el siguiente aviso.
  
  Esto sugiere que los rasgos de autorregulación asociados al TDAH podrían bajar el cumplimiento. [Baja; inferido de poblaciones adyacentes] — [PMC10698810](https://pmc.ncbi.nlm.nih.gov/articles/PMC10698810/); [U. Edinburgh, prompt-level predictors](https://www.research.ed.ac.uk/en/publications/prompt-level-predictors-of-compliance-in-an-ecological-momentary-/).

**Referentes generales de cumplimiento y carga**
- Meta-análisis de EMA (Wrzus y Neubauer, *Assessment* 2023): 477 artículos, 496 muestras, N = 677.536.
  - El estudio típico programa **6 evaluaciones al día durante 7 días** y obtiene **79% de cumplimiento**.
  - Programar más evaluaciones al día va de la mano de menos días de estudio, pero **el número de evaluaciones no predijo el cumplimiento ni el abandono**.
  - Los **incentivos económicos** se asociaron a un cumplimiento significativamente mayor.
  
  [Alta; meta-análisis] — [registro Heidelberg](https://heibib.ub.uni-heidelberg.de/search/Record/1839595345).
- Experimento sobre diseño de ESM (Eisele et al., *Assessment* 2022): 163 estudiantes con cuestionarios de 30 o 60 ítems, 3, 6 o 9 veces al día durante 14 días. **Los cuestionarios largos aumentaron la carga percibida y redujeron cantidad y calidad de datos; la mayor frecuencia no.** [Alta/Moderada; experimental] — [Maastricht CRIS](https://cris.maastrichtuniversity.nl/en/publications/the-effects-of-sampling-frequency-and-questionnaire-length-on-per/). Sin embargo, un reanálisis de los mismos datos con tiempos en pantalla encontró que **la frecuencia (no la longitud) aumentó las respuestas descuidadas**. [Moderada] — [Ulitzsch et al., IPN Leibniz](https://www.leibniz-ipn.de/en/research/publications/investigating-the-effect-of-experience-sampling-study-design-on-careless-and-insufficient-effort-responding-identified-with-a-screen-time-based-mixture-model).
- Población adyacente (deterioro cognitivo leve, 8 avisos al día durante 6 días): 78,7% de cumplimiento entre quienes siguieron; 3 de 21 abandonaron por olvidar el teléfono o las instrucciones. [Baja; población distinta] — [JMIR Aging 2020, PMC7600012](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7600012/).

### Inferences
- El bucle de SpaceEase es **iniciado por el usuario** (registra una dificultad) y luego pide una sola calificación tras el trabajo, lo que en EMA equivale a un diseño *event-contingent*. Esto encaja con la recomendación de ensayos iniciados por el participante en autismo y evita interrupciones aleatorias.
- Con ~72–79% de respuesta como referente, SpaceEase debe **asumir que se perderán ~20–30% de las calificaciones posteriores**. Ese dato faltante probablemente no es aleatorio: es más probable cuando la sesión fue mal o el usuario quedó agotado, lo que sesgaría la recompensa a favor de los ajustes. Conviene registrar "sin respuesta" como dato, permitir calificar más tarde ("¿cómo fue tu sesión de las 11:00?") y no tratar la ausencia como neutra.
- Para usuarios autistas: lenguaje literal, anclas "nada" / "mucho", apoyo visual (iconos), botones grandes, previsibilidad (avisar al inicio cuándo llegará la pregunta), vibración en lugar de sonido y control del usuario sobre ventanas horarias.
- Para usuarios con TDAH: la evidencia indirecta sugiere menor adherencia con estrés o bajo autocontrol. Hace falta fricción mínima (un toque), recordatorio a la hora que elija el usuario y tolerancia a respuestas tardías.
- Mantener el registro en **1–2 ítems** pesa más que la frecuencia para la carga (Eisele). Pero preguntar muchas veces al día eleva las respuestas descuidadas, así que conviene poner un tope diario de seguimientos (por ejemplo, ≤5, como Self-E).

### Gaps
- **No encontré una tasa de cumplimiento EMA publicada específica de adultos con TDAH** (las revisiones de 2018 y de Bristol no dieron cifras en lo que pude leer).
- No hay estudios de EMA en autismo que reporten adaptaciones *sensoriales* de la propia interfaz (la revisión de Chen lo marca como laguna).
- Faltan datos de EMA en adultos autistas mayores, con discapacidad intelectual o en contexto laboral.
- No leí los textos completos del estudio Song 2023 ni de la tesis de Western (protocolos exactos).

## 3. Medidas breves de un solo ítem validadas para esfuerzo percibido, fatiga mental, concentración y malestar sensorial: fiabilidad como ítem 1–5 o 0–10 y redacción en lenguaje llano

### Takeaway
La escala de esfuerzo mental de Paas (1992; 9 puntos, de "very, very low" a "very, very high mental effort") es la medida de un solo ítem más usada para esfuerzo cognitivo. Se le atribuye una fiabilidad test-retest de ~0,90 (dato de fuente secundaria) y distingue tareas simples de complejas, aunque su validez se discute (deseabilidad social, un solo ítem). Para fatiga existen ítems únicos con validez convergente en diarios ("How fatigued do you currently feel?") y VAS únicas tan sensibles al cambio como escalas largas. Las subescalas sueltas de NASA-TLX exigen revalidación si se modifican. En móvil, los botones discretos (radio) dan menos no respuesta que los sliders. **No encontré ninguna medida validada de un solo ítem para "malestar sensorial" ni para "concentración" en adultos.**

### Cited Findings
**Esfuerzo mental (Paas)**
- Escala de Paas: un ítem de 9 puntos (1 = "very, very low mental effort" … 9 = "very, very high mental effort") de 1992. Un catálogo la clasifica como validada con test-retest de 0,90. [Moderada; Seminal; la cifra de 0,90 viene de un catálogo secundario y no la verifiqué en el original] — [Learning Lab, U. Duisburg-Essen](https://learninglab.uni-due.de/research-instrument/13339).
- Ouwehand, van der Kroef, Wong y Paas (Frontiers in Education 2021), n = 46, compararon la escala Likert de 9 puntos, una VAS 0–100%, una escala de emoticonos y una escala "encarnada" de pesas.
  - Redacción del ítem: "Indicate on this scale how much mental effort it cost you to solve the problem".
  - **Todas las escalas distinguieron problemas simples de complejos**.
  - Las numéricas (9 puntos y VAS) se correlacionaron más con el rendimiento en problemas complejos (por ejemplo, r = −0,37 con la precisión). Las pictóricas lo hicieron en problemas simples (pesas: r = −0,57).
  - Preferencias: 16 eligieron la original, 14 la VAS, 13 los emoticonos y 3 las pesas. La preferencia no predijo la validez.
  - Los autores califican de "debatable" la fiabilidad y validez de las medidas subjetivas y piden replicación.
  
  [Moderada; experimental pequeño, estudiantes] — [Frontiers in Education 2021](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2021.702616/full).
- Críticas a la escala Paas: su sensibilidad y validez se han cuestionado por tener pocos ítems y facilitar la deseabilidad social. Aun así, en un experimento de doble tarea fue más sensible que el NASA-TLX (la escala WP fue la mejor de las tres). [Baja/Moderada] — [Journal of Psychological Science (ECNU) 2013](https://jps.ecnu.edu.cn/EN/Y2013/V36/I1/195).
- Ítem único frente a varios ítems: el ítem único ofrece brevedad, menos carga y facilidad de integración en estudios sensibles al tiempo. Las escalas de varios ítems se consideran más fiables y completas. [Baja/Moderada] — [Krieglstein et al., EARLI](https://www.earli.org/assets/images/Kriegelstein-et-al.pdf).
- Escala relacionada RSME (Rating Scale Mental Effort, Zijlstra): correlaciones test-retest de 0,96 en un estudio iraní. Es otra escala, útil como comparación. [Baja/Moderada] — [IJOH](https://ijoh.tums.ac.ir/index.php/ijoh/article/view/424).

**NASA-TLX**
- Hart 2006 ("NASA-TLX; 20 Years Later") revisó 550 estudios y concluye que la herramienta es fácil de usar y sensible a manipulaciones experimentales. Muchos usan la versión "Raw TLX" sin ponderaciones. [Alta; Seminal] — [Hart 2006, NASA](https://humansystems.arc.nasa.gov/publications/HFES_2006_Paper.pdf).
- Las seis subescalas se correlacionan entre sí (r = 0,28–0,76). Si se elimina o modifica alguna, en la práctica se crea un cuestionario nuevo que necesita su propia validación. [Baja; fuentes secundarias] — [MeasuringU](https://measuringu.com/nasa-tlx/); [Wikipedia NASA-TLX](https://en.wikipedia.org/wiki/NASA-TLX).

**Fatiga**
- Ítem único de fatiga diaria "How fatigued do you currently feel?" (van Hooff et al., J Occup Health 2007): 120 académicos, diario de 9 días con 3 mediciones diarias. Mostró validez convergente y discriminante con medidas relacionadas con fatiga. [Moderada] — [TNO PDF](https://publications.tno.nl/publication/34619116/6i56Za/hooff-2007-how.pdf).
- VAS única de fatiga en 7.760 pacientes con artritis reumatoide (Wolfe 2004): fue tan buena o mejor que tres cuestionarios largos en sensibilidad al cambio y se correlacionó de forma parecida con variables clínicas. Las escalas largas tuvieron algo más de fiabilidad transversal. Se trata de fatiga física y clínica, no mental. [Moderada] — [J Rheumatol](https://www.jrheum.org/node/8825).

**Formato de respuesta (Likert/radio frente a slider/VAS)**
- Experimento en encuesta web (N = 4.180): no respuesta por ítem de 7,3–7,7% con sliders, 5,5% con VAS y 3,8% con botones radio, concentrada en personas con menor educación formal. [Moderada] — [ESRA 2015](https://europeansurveyresearch.org/conf2015/prog.php?sess=63).
- Funke, Reips y Thomas (2011) desaconsejan los sliders y encontraron efectos negativos frente a VAS y botones radio. [Moderada] — [Funke et al. 2011 PDF](https://iscience.uni-konstanz.de/wp-content/uploads/2011/09/2011FunkeReipsThomas_final.pdf). Otros estudios no hallaron diferencias significativas: los sliders tardan más y los usuarios prefieren los botones radio. [Baja/Moderada] — [MeasuringU sliders](https://measuringu.com/?p=29896); [Journal of Research Practice](https://jrp.icaap.org/index.php/jrp/article/download/509/413-inline=1.html).
- **Posible conflicto** para población autista: la revisión de Chen et al. cita los sliders y las preguntas dicotómicas como "simpler options" y recomienda las anclas "not at all" / "a lot" y apoyos visuales. [Moderada] — [PMC12089685](https://pmc.ncbi.nlm.nih.gov/articles/PMC12089685/).

### Inferences
- SpaceEase usa una escala 1–5 de "esfuerzo percibido". Lo más cercano validado es Paas (9 puntos). Reducirla a 5 puntos es una **modificación no validada**, aunque razonable por simplicidad. Para un análisis personal con pocos datos, 5 categorías bien ancladas probablemente bastan; con 1–5, un cambio de 1 punto puede estar dentro del ruido.
- Propuesta de redacción en lenguaje llano, inspirada en Paas y en las anclas de Chen:
  - Antes: "Ahora mismo, ¿cuánto esfuerzo te cuesta concentrarte en esta tarea?"
  - Después: "¿Cuánto esfuerzo te costó la sesión?"
  - Escala: 1 = "casi nada", 2 = "poco", 3 = "algo", 4 = "bastante", 5 = "muchísimo". Poner etiqueta visible en cada punto, no solo en los extremos, y usar el mismo icono y color en todas las pantallas.
- Conviene separar **esfuerzo** de **malestar sensorial** (por ejemplo, "¿cuánto te molestó el entorno (ruido, luz, gente)?" de 1 a 5). Si el ajuste es sensorial, el malestar sensorial es el resultado más directo y el esfuerzo el más distal. No hay ítem validado para malestar sensorial, así que habría que presentarlo como medida propia y exploratoria.
- Para la interfaz: botones discretos grandes (5 opciones) en lugar de slider por defecto, por menor no respuesta y mayor rapidez, y ofrecer opcionalmente emoticonos o iconos para usuarios que prefieran lo visual. Es coherente con que los formatos pictóricos funcionen en juicios simples (Ouwehand 2021).
- Para la "fatiga mental" puede adaptarse el ítem de van Hooff ("¿Qué tan cansado/a te sientes ahora?"), siempre con la misma redacción y anclas y en el mismo momento del bucle.

### Gaps
- **No encontré** ítems únicos validados para *malestar sensorial momentáneo* ni para *concentración* en adultos, ni validaciones de Paas, NASA-TLX o VAS en adultos **autistas o con TDAH**.
- No verifiqué en fuentes primarias el test-retest de 0,90 de Paas (1992) ni sus anclas intermedias.
- No busqué validaciones del Borg CR10 aplicado al esfuerzo mental o cognitivo; queda sin evidencia en estas notas.
- No encontré la diferencia mínima importante (MCID) en un ítem 1–5 de esfuerzo o fatiga, que haría falta para fijar el umbral de "mejoró".

## 4. Personalización en mHealth: bandits contextuales, JITAI, Thompson sampling (HeartSteps), explicabilidad y estrategias de arranque en frío

### Takeaway
El marco JITAI (Nahum-Shani et al. 2018) define seis componentes: puntos de decisión, opciones de intervención, variables de ajuste, reglas de decisión, y resultados proximales y distales. HeartSteps es la referencia empírica: su ensayo micro-aleatorizado mostró que las sugerencias funcionan al principio pero **el efecto decae ~2% al día por habituación**. Su versión con aprendizaje por refuerzo usa Thompson sampling por usuario con **priors informativos a partir de datos piloto**, una variable de "dosis" contra la habituación y **probabilidades acotadas a [0,1; 0,8]** para seguir explorando. El "pooling" jerárquico (IntelligentPooling) reduce el arrepentimiento ~26% al compartir información entre usuarios, lo que respalda la estrategia de backoff jerárquico de SpaceEase. La explicabilidad está poco estudiada en estos algoritmos. Self-E muestra una fórmula simple que los usuarios entienden (probabilidad + tamaño del efecto + número de días), y hay evidencia de que los usuarios confían de más en algoritmos opacos, incluso aleatorios.

### Cited Findings
**Marco JITAI**
- Componentes de un JITAI según Nahum-Shani et al. (2018): resultados proximales, resultados distales, reglas de decisión, puntos de decisión, opciones de intervención y variables de ajuste. Estas últimas incluyen estados internos (ánimo, motivación) y contexto (agenda, entorno). [Alta; Seminal; tomado de una revisión secundaria, no del original] — [revisión en PMC12784143](https://pmc.ncbi.nlm.nih.gov/articles/PMC12784143).
- Las variables de ajuste son información específica de la persona (y a veces del momento) para decidir si y cómo intervenir. [Moderada] — [Dziak y Nahum-Shani 2025, arXiv](https://arxiv.org/abs/2506.03054v1).
- Receptividad, siguiendo a Nahum-Shani: "the person's ability to receive, process, and use the support provided". [Moderada] — [Künzler et al. 2019](https://cs.dartmouth.edu/dfk/research/kunzler-receptivity/index.html).

**HeartSteps (ensayo micro-aleatorizado y aprendizaje por refuerzo)**
- MRT HeartSteps (Klasnja et al., Ann Behav Med 2019;53(6):573–582): 6 semanas, 37 analizados, hasta 5 puntos de decisión al día a horas elegidas por el usuario.
  - Aleatorización: 0,4 sin sugerencia, 0,3 sugerencia de caminar, 0,3 sugerencia antisedentaria. Disponibilidad ~80%.
  - Efecto medio de cualquier sugerencia: +14% en pasos a 30 minutos (+35 pasos sobre 253; p = 0,06).
  - **El día 1 el efecto fue +66% (p < 0,01) y decayó ~2% al día hasta ser indistinguible de cero hacia el día 28**. Las sugerencias de caminar tuvieron +24% de media (p = 0,02).
  - En entrevistas de salida, los participantes dijeron que las sugerencias se volvían aburridas a las 2–4 semanas. Se suprimían las sugerencias cuando el usuario estaba caminando, conduciendo o acababa de hacer actividad.
  
  [Alta; MRT] — [Klasnja et al., PMC6401341](https://pmc.ncbi.nlm.nih.gov/articles/PMC6401341).
- Personalized HeartSteps (Liao, Greenewald, Klasnja, Murphy):
  - Bandit lineal contextual con Thompson sampling desplegado **por separado en cada usuario**, 5 decisiones al día durante 90 días.
  - **Prior construido a partir del piloto V1** (37 participantes, 42 días). Las variables significativas toman la estimación poblacional como media del prior y la variabilidad entre personas como DE. Las no significativas toman media 0 y la mitad de la DE.
  - **Variable de dosis** X(t+1) = 0,95·X(t) + envío, para captar habituación y carga.
  - **Probabilidades de envío acotadas a [0,1; 0,8]** para no fijar una política determinista y para permitir análisis posteriores.
  - En simulación superó al Thompson sampling estándar en 29 de 37 participantes. En el piloto V2, 7 de 8 aumentaron ~125 pasos.
  - Se eligieron modelos lineales de baja dimensión para reducir varianza y acelerar el aprendizaje.
  
  [Moderada; algoritmo con piloto pequeño] — [ar5iv 1909.03539](https://ar5iv.labs.arxiv.org/html/1909.03539).
- IntelligentPooling (Tomkins, Liao, Klasnja, Murphy): Thompson sampling que ajusta *para cada usuario* su grado de personalización usando datos de otros usuarios. Aborda la heterogeneidad entre personas, los pocos datos individuales y la no estacionariedad. **26% menos arrepentimiento** que los métodos del estado del arte y capacidad de aprender incluso con pocos usuarios en un ensayo real. [Moderada; preprint/estudio de métodos] — [arXiv 2008.01571](https://arxiv.org/abs/2008.01571).
- Existe un "precio de la personalización": un compromiso entre optimizar la eficacia global y la equidad de la eficacia individual. [Moderada] — [Harvard DASH](https://dash.harvard.edu/entities/publication/c088a98e-abd2-46bd-959f-bd7f3a524bf6).
- "Did we personalize?" (Ghosh et al. 2023): método de remuestreo para comprobar si la personalización aparente del algoritmo de HeartSteps es real o un artefacto de su aleatoriedad ("truth-in-advertising" de la personalización). [Moderada; métodos] — [arXiv 2304.05365](https://arxiv.org/abs/2304.05365).
- Marco PCS (predictibilidad, computabilidad, estabilidad) para diseñar algoritmos de aprendizaje por refuerzo en intervenciones digitales, con simuladores antes de desplegar (Trella et al., Algorithms 2022). Aplicado en Oralytics, desplegado en un ensayo de otoño de 2023 a verano de 2024 a partir de datos previos, conocimiento experto y simulación. [Moderada] — [MDPI Algorithms](https://www.mdpi.com/1999-4893/15/8/255); [arXiv 2406.13127](https://arxiv.org/abs/2406.13127v1).

**Explicabilidad y confianza**
- Self-E muestra el resultado de su Thompson sampling Beta como una frase con probabilidad, tamaño del efecto y días de datos ("about 73% likelihood … 0.8 levels higher … 8 days"), que la mayoría encontró clara. Los usuarios desconfiaban cuando el resultado contradecía sus creencias o cuando sospechaban confusores. Los autores proponen "empathy and scaffolding" y explicar por qué se aleatoriza. [Moderada/Baja] — [Self-E PDF](https://jeffhuang.com/papers/SelfE_CHI21.pdf).
- "Dice in the Black Box" (Springer, Hollis, Whittaker 2018): una herramienta que decía evaluar la emoción de textos daba en realidad resultados aleatorios, y los usuarios **confiaron en exceso** en ella al presentarse como inteligente. Los autores recomiendan enfoques correctivos. [Baja/Moderada; cualitativo, preprint] — [arXiv 1812.03219](https://arxiv.org/abs/1812.03219).
- La personalización "abierta" (consultar al usuario sus preferencias antes de personalizar) se percibió como más confiable y usable que la personalización oculta. [Baja; nota de prensa de un estudio presentado en CHI] — [Penn State News](https://www.psu.edu/news/research/story/user-control-and-transparency-are-key-trusting-personalized-mobile-apps).

### Inferences
- El diseño de SpaceEase (Beta por estímulo × tarea × espacio con backoff a priors globales) se alinea con HeartSteps (priors poblacionales informativos) y con IntelligentPooling (aprendizaje compartido). Ajustes recomendados:
  1. **Priors débiles**: equivalentes a pocas observaciones (por ejemplo, α+β ≈ 2–4), para que unos pocos episodios personales dominen pronto. HeartSteps redujo a la mitad la DE de los efectos no significativos y ajustó la fuerza del prior con datos.
  2. **Exploración mínima garantizada**: probabilidad de cada opción viable acotada (por ejemplo, ≥10%), al estilo de HeartSteps [0,1; 0,8].
  3. **Olvido o descuento** de observaciones antiguas, porque los efectos decaen por habituación (HeartSteps: −2% al día) y las preferencias sensoriales cambian.
  4. **Control de "dosis"**: no repetir la misma sugerencia muchas veces seguidas.
  5. **Comprobar si personaliza de verdad** comparando con el prior global (Ghosh 2023) antes de afirmar al usuario que el sistema "aprendió" algo.
- El Beta-Bernoulli exige binarizar la recompensa. Opciones: "mejoró ≥1 punto frente a la previa" o, mejor, "mejoró más que tu mejora típica" (ver Pregunta 1, regresión a la media). Self-E binariza de forma parecida: datos que "lead to improvement or not, over the running average".
- La celda estímulo × tarea × espacio fragmenta mucho los datos. Con 3 dimensiones, un usuario tendrá pocas observaciones por celda durante semanas, así que el backoff jerárquico es imprescindible. Conviene que la explicación indique de qué nivel viene la sugerencia ("esto suele ayudar a otras personas en tareas de lectura" frente a "te ha ayudado 4 de 5 veces en tu oficina").
- Explicabilidad, siguiendo a Self-E:
  - Una frase con *número de veces probado*, *proporción de veces que ayudó* y *grado de certeza* en palabras ("todavía poco seguro" / "bastante seguro").
  - Distinguir sugerencias de **exploración** ("probemos algo nuevo para aprender") de las de **explotación**.
  - Dar control al usuario para vetar o fijar sugerencias (personalización abierta).
  - Para evitar la sobreconfianza (Dice in the Black Box), mostrar la incertidumbre y el número de datos.

### Gaps
- No leí el artículo original de Nahum-Shani et al. 2018; los seis componentes vienen de una revisión secundaria.
- No encontré estudios empíricos sobre **explicaciones de bandits o de aprendizaje por refuerzo a usuarios finales en mHealth** (cómo afectan a la confianza o la adherencia). Es una laguna de la literatura.
- No hay ensayos de JITAI o bandits en población **autista o con TDAH** ni para **ajustes ambientales o sensoriales**.
- No obtuve los resultados finales del ensayo HeartSteps V2/V3 a gran escala (solo el piloto de 8 personas).

## 5. Diseño de recordatorios/notificaciones: momento óptimo para el "¿cómo fue?", fatiga de notificaciones y TDAH

### Takeaway
Notificar en **puntos de quiebre** entre tareas reduce la frustración y el tiempo de reacción frente a interrumpir a mitad de la tarea. La receptividad depende del contexto (hora, uso del teléfono, ubicación). Las notificaciones tienen efectos pequeños y que se desgastan: +3,9% de engagement en 24 h en un ensayo micro-aleatorizado de 1.255 usuarios, y el efecto de HeartSteps desaparece hacia la 4.ª semana. En adultos con TDAH, recordatorios SMS semanales fijos tuvieron efectos mínimos, y los autores recomiendan que el usuario elija horario y frecuencia, con contenido personalizado. Las herramientas para TDAH a menudo asumen erróneamente rutinas estables y una respuesta positiva a los recordatorios.

### Cited Findings
- Iqbal y Bailey (CHI 2008; TOCHI 2010): programar notificaciones en puntos de quiebre de la tarea reduce la frustración y el tiempo de reacción frente a entregarlas de inmediato. Los modelos estadísticos detectan esos puntos con 69–87% de precisión media según el tipo. El "coste" medido fue sobre todo el tiempo de reanudación. [Moderada/Alta; Seminal, laboratorio] — [Iqbal y Bailey CHI08](https://www.interruptions.net/literature/Iqbal-CHI08.pdf); [survey de notificaciones inteligentes](https://arxiv.org/pdf/1711.10171).
- Künzler et al. (IMWUT 2019): 189 participantes durante 6 semanas con un coach-chatbot de actividad física. La receptividad global se asoció a edad, personalidad y tipo de dispositivo. La receptividad momentánea se asoció a hora del día, batería, interacción con el teléfono, actividad física y ubicación. Los modelos de detección mejoraron el F1 hasta un 77% frente a un clasificador aleatorio sesgado. [Moderada] — [Dartmouth, Künzler et al.](https://cs.dartmouth.edu/dfk/research/kunzler-receptivity/index.html).
- Bidargaddi et al. (JMIR mHealth uHealth 2018), ensayo micro-aleatorizado con 1.255 usuarios de una app de bienestar laboral durante 89 días, con aleatorización a una de 6 horas al día: enviar un mensaje personalizado aumentó la probabilidad de autorregistro en las 24 h siguientes en **3,9%** (RR 1,039; IC95% 1,01–1,08). [Alta/Moderada; MRT] — [JMIR mHealth 2018](https://mhealth.jmir.org/2018/11/e10123).
- Habituación: en HeartSteps el efecto de las sugerencias decayó ~2% al día y se volvieron "aburridas" a las 2–4 semanas. [Alta] — [PMC6401341](https://pmc.ncbi.nlm.nih.gov/articles/PMC6401341).
- Nordby et al. (Frontiers in Digital Health 2022), adultos con TDAH autorreportado (n = 109) en una intervención online autoguiada, con un SMS a las ~17:00 a quienes no habían terminado el módulo en 48 h:
  - Solo en el módulo 2 aumentó el login en 48 h (40,0% frente a 18,4%; p = 0,049).
  - Sin efecto en el total de logins, en módulos completados ni en la práctica de estrategias.
  - El primer login llegó ~64 minutos antes y se dedicaron ~3,9 minutos más por módulo.
  - Los autores sugieren recordatorios personalizados, contenido motivacional, **horario y frecuencia elegidos por el participante** y gamificación. Un recordatorio semanal pudo ser demasiado infrecuente, y más frecuencia arriesga intrusión.
  
  [Moderada; ensayo micro-aleatorizado pequeño] — [Frontiers in Digital Health 2022](https://www.frontiersin.org/journals/digital-health/articles/10.3389/fdgth.2022.821031/full).
- Trabajos de Chalmers (tesis de estudiantes):
  - Encuesta (n = 69) a adultos con TDAH o dificultades de foco: las herramientas existentes suelen asumir "stable planning ability, consistent routines, low setup effort, and positive responses to reminders".
  - Estudio de wearables: se recomiendan notificaciones, alarmas y temporizadores personalizables alineados con la rutina, notas de voz rápidas y ayuda de configuración personalizada.
  
  [Baja; tesis] — [Chalmers ODR (1)](https://odr.chalmers.se/items/b2823e79-9286-446c-8a53-2f7219fc0b45); [Chalmers ODR (2)](https://odr.chalmers.se/items/602f3701-7897-44fe-9b82-1abb6a336824/full).
- Expertos por experiencia mencionan calendarios, recordatorios y apps como Tiimo y Finch. Los problemas de usabilidad fueron una barrera importante para adoptar herramientas digitales para TDAH. [Baja; informe de servicio] — [Health Innovation East Midlands, D4ND](https://healthinnovation-em.org.uk/images/D4ND_Hubs_Thematic_Analysis_and_Final_Report.pdf).
- En autismo, recomendaciones de la revisión EMA: ventanas horarias elegidas por el participante, modo vibración, entradas iniciadas por el participante para reducir la frustración por interrupción, y caída de respuesta en estudios de 14 días. [Alta/Moderada] — [PMC12089685](https://pmc.ncbi.nlm.nih.gov/articles/PMC12089685/).
- Topes de frecuencia en sistemas comparables: Self-E, máximo 5 check-ins al día; HeartSteps, 5 puntos de decisión al día con supresión cuando el usuario no está disponible; EMA típico, ~6 al día. [Moderada] — [Self-E PDF](https://jeffhuang.com/papers/SelfE_CHI21.pdf); [ar5iv 1909.03539](https://ar5iv.labs.arxiv.org/html/1909.03539); [Wrzus y Neubauer](https://heibib.ub.uni-heidelberg.de/search/Record/1839595345).

### Inferences
- El "¿cómo fue?" debería llegar **al final del bloque de trabajo que el propio usuario define**: un temporizador con duración elegida ("avísame en 25/45/90 min"), o bien el usuario pulsa "terminé". Así cae en un punto de quiebre (Iqbal y Bailey) y es un aviso *event-contingent*, iniciado por el usuario, como se recomienda en autismo.
- Ofrecer un **"pospón 10 min"** y una **calificación retroactiva** ("¿cómo fue tu sesión de esta mañana?") en la siguiente apertura de la app, con tolerancia de unas horas, para no perder datos cuando hay hiperfoco (TDAH) o cuando interrumpir causaría malestar. Hay que guardar el retraso de la calificación como metadato, porque las calificaciones tardías tienen más sesgo de memoria.
- Un solo aviso por episodio, sin recordatorios repetidos, y un tope diario (por ejemplo, ≤5 seguimientos). Vibración o aviso silencioso por defecto, sin sonido, y texto corto y literal.
- Como las notificaciones se desgastan (HeartSteps, Bidargaddi), conviene **variar la redacción**, no insistir, y medir la tasa de respuesta por usuario como señal de carga. Si cae, reducir los avisos en vez de aumentarlos.
- Para TDAH: horario y frecuencia elegidos por el usuario (Nordby), configuración inicial muy ligera y no presuponer rutinas estables. El valor está en que el aviso aparezca justo cuando acaba el bloque, no en recordatorios a horas fijas.

### Gaps
- No encontré estudios empíricos sobre el **momento óptimo del seguimiento post-tarea** ("¿cómo fue?") en apps de autogestión, ni de fatiga de notificaciones medida específicamente en **adultos con TDAH o autistas**.
- No verifiqué en fuente primaria la relación entre el retraso de la calificación y su precisión (sesgo de memoria) para ítems de esfuerzo o fatiga.
- No identifiqué con certeza qué tesis de Chalmers corresponde a cada hallazgo (los dos enlaces se citan juntos).
