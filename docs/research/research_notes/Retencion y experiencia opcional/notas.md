# Retención sin culpa y modo opcional "Con detalles" (animación en pixel art, sonidos suaves y recordatorios) para personas adultas autistas y con TDAH: notas con fuentes para SpaceEase

> Notas de investigación en español. Las citas textuales de fuentes en inglés se dejan en inglés. Fecha de consulta: 26-10-2026.
> Convención: **Hallazgos citados** = solo lo verificado en la fuente enlazada. **Inferencias** = traducción a reglas para SpaceEase (mías, no de la fuente). **Vacíos** = lo que no se encontró o no se pudo verificar.
> Escala de solidez (la del informe, más una categoría):
> - **Normativa:** texto legal o guía oficial de la plataforma (Apple, W3C).
> - **Fuerte:** metaanálisis o revisión sistemática.
> - **Moderada:** estudios empíricos.
> - **Débil:** estudios cualitativos, pilotos, pósteres o defensa.
> - **Experta (nueva):** guía de diseño de otra plataforma o de profesionales (Material, Microsoft, sesiones WWDC, libros de práctica).
> - **Inferencia:** deducción propia.

## 0. Qué ya está decidido (no se repite aquí)

- **Informe, tabla "Decisiones de producto":**
  - #7: recompensa relativa y brazo "sin cambiar nada".
  - #10: frase al estilo Self-E, tentativa desde 3 episodios.
  - #11: un aviso por episodio, sin sonido, como mucho 5 al día.
  - #12: el rechazo cuenta como preferencia.
  - #16: Reducir movimiento y un ajuste propio.
  - #17: sin rachas, pérdidas, rankings ni culpa; totales acumulados y "Todo está como lo dejaste".
- **`DESIGN.md` §5–6:** movimiento ≤ 250 ms, ease-out, vibración apagada, sin sonido y recordatorios solo a petición.
- **`research_notes/.../diseno_neuroinclusivo.md`:**
  - §3 cubre Apple HIG Motion y Reduce Motion, WCAG 2.2.2/2.3.1/2.3.3, duraciones NN/g y la háptica.
  - §6 cubre Silverman & Barasch 2023, COGA sobre recordatorios, los niveles de interrupción de iOS y el onboarding.

Estas notas añaden lo que faltaba: por qué se sostiene el uso, qué recompensas sí y cuáles no, lo propio de la población autista y con TDAH, los sonidos de interfaz, las celebraciones y la animación en reposo del modo opcional, y la redacción de los recordatorios diarios.

### Estado del código revisado (26-10-2026, ~18:07)

`apps/mobile/src/lib/{settings,feedback,sounds,animations,notifications,desk,checkout}.ts(x)`, `components/desk/desk-scene.tsx`, `app/checkout/[id]/result.tsx` y `docs/brand/make_sounds.py`.

**Lo que ya existe**
- Interruptores separados `details`, `sounds` y `haptics`, todos apagados por defecto.
- Sonidos en la categoría `ambient` (callan con el interruptor de silencio y se mezclan), con un hueco mínimo de 200 ms entre sonidos.
- Escena "Tu escritorio" que se mueve 5 s y luego se detiene.
- Avisos locales sin sonido.
- Resumen semanal a las 10:00 del día elegido.
- Un objeto en la escena por cada ajuste que "ayudó", y **la única celebración ocurre cuando algo ayudó por primera vez**.

Lo que esta investigación cambia está en §6.

---

## 1. Retención: qué sostiene el uso sin castigar

### Takeaway
Lo que sostiene el uso en mHealth es que la app sea **relevante, controlable y comprensible**, no la presión. Las revisiones lo agrupan en autonomía, competencia y relación (SDT). El objetivo correcto es el **"uso efectivo"**: el suficiente para lograr el resultado. No es el máximo uso posible, y dejar la app tras aprender lo necesario no es un fracaso.

El progreso visible motiva: el principio de progreso, el gradiente de meta y el progreso dotado. Sin embargo, sus versiones de "falta poco" crean presión, y la de progreso "dotado" puede ser artificial.

Las recompensas tangibles y esperadas reducen la motivación intrínseca. La retroalimentación informativa la aumenta. Los puntos, niveles y rankings suben la cantidad, pero no la motivación.

Para SpaceEase hay un hallazgo clave. **Premiar el contenido de la respuesta empeora los datos**: las recompensas por completar encuestas volvieron las respuestas menos fiables, y las personas evitan registrar lo negativo. Como la celebración actual depende de que la persona responda "ayudó", contamina la medición.

La intervención que más funcionó en un megaestudio de 54 fue premiar el **regreso tras un fallo**. Perder un día no afecta la formación del hábito. Los recordatorios tienen efectos pequeños que se desgastan.

### Hallazgos citados

**Qué es el engagement y qué lo sostiene**
- **Perski et al. 2017** (revisión con síntesis interpretativa crítica, 117 artículos).
  - Definen el engagement como "(1) the extent (e.g. amount, frequency, duration, depth) of usage and (2) a subjective experience characterised by attention, interest and affect".
  - Influencias hipotetizadas o encontradas: técnicas de cambio de conducta (metas, planes de acción, retroalimentación, automonitoreo), personalización, recordatorios, recompensas, control, novedad, facilidad de uso, tono del mensaje y estética.
  - Sobre recordatorios: "results from a meta-analysis indicate a positive effect of reminders on engagement", con riesgo de "e-mail fatigue".
  - Sobre recompensas: "evidence from trials in which the presence of rewards or incentives has been manipulated is scarce".
  - Proponen un "optimal dose" de engagement que varía por persona.
  - [PMC5526809](https://pmc.ncbi.nlm.nih.gov/articles/PMC5526809/) — **Fuerte (revisión), conceptual**
- **Yardley et al. 2016** (consenso de expertos, *AJPM*): "it may be more valuable to establish and promote 'effective engagement,' rather than simply more engagement". El uso efectivo es el suficiente para lograr los resultados buscados — [UCL Discovery](https://discovery.ucl.ac.uk/id/eprint/1528600/) — **Moderada (consenso)**
- **Baykoca et al. 2026** (*JMIR mHealth*; revisión de revisiones: 19 revisiones, 262 estudios, 98 apps, personas adultas con condiciones crónicas).
  - Lo que influye en cada necesidad: la autonomía depende de la relevancia personal y la flexibilidad; la competencia, de la usabilidad y el apoyo técnico; la relación, del aval clínico y la conexión con pares.
  - Esos factores "underpin intrinsic engagement". 7 de 8 revisiones encontraron una asociación positiva entre engagement y resultados.
  - La nota del King's College dice que dejar la app puede significar que la persona "simply gained what they needed". Quien la usa solo en las crisis "may be using it exactly as intended". Y: "When an app is abandoned, the problem is not automatically a lack of motivation."
  - Fuentes: [JMIR mHealth 2026;e88382](https://mhealth.jmir.org/2026/1/e88382) y [KCL](https://www.kcl.ac.uk/why-do-we-stop-using-health-apps-and-is-that-always-a-problem) — **Fuerte (revisión de revisiones), conceptualmente heterogénea**
- **Borghouts et al. 2021** (*JMIR*, 208 artículos sobre intervenciones digitales de salud mental).
  - Barreras: "technical issues, and a lack of personalization".
  - Facilitadores: "social connectedness, increased insight into health, and a feeling of being in control of one's health".
  - [JMIR 2021;23(3):e24387](https://www.jmir.org/2021/3/e24387) — **Fuerte (revisión)**
- **Szinay et al. 2020** (*JMIR*, revisión según COM-B). Entre los factores de capacidad están "statistical information on progress", "well-designed reminders", "features to reduce cognitive load" y "self-monitoring features" — [JMIR 2020;22(5):e17572](https://jmir.org/2020/5/e17572) — **Fuerte (revisión)**
- **Abandono esperable** (Baumel et al. 2019): en 93 apps de salud mental, la retención mediana fue del 3,9 % a 15 días y del 3,3 % a 30 días. Las de seguimiento ("tracker") retuvieron el 6,1 % a 30 días — [JMIR 2019;21(9):e14567](https://www.jmir.org/2019/9/e14567) — **Moderada**

**Progreso**
- **Principio de progreso** (Amabile y Kramer 2011).
  - El subtítulo del artículo es "Help them see their own progress".
  - Estudio de diarios: casi 12.000 entradas de 238 personas en 7 empresas.
  - Según resúmenes secundarios, hubo avances en el 76 % de los días de mejor ánimo y contratiempos en el 67 % de los peores. Los contratiempos pesan más que los avances.
  - Fuentes: [HBR 2011](https://hbr.org/2011/05/the-power-of-small-wins); cifras vía [Silicon Canals](https://siliconcanals.com/m-after-combing-nearly-12000-daily-diary-entries-from-238-workers-researchers-found-that-the-strongest-force-behind-motivation-and-creativity-wasnt-the-lever-managers-reach-for-pay-or-prai/).
  - **Moderada** (diarios, no experimento; anterior a 2015; cifras no verificadas en el original).
- **Gradiente de meta** (Kivetz, Urminsky y Zheng 2006, *JMR*).
  - El esfuerzo aumenta al acercarse a la recompensa. Lo mostraron con tarjetas de café y con calificación de canciones.
  - El "illusionary goal progress" también acelera.
  - Quienes aceleraron más hacia la primera recompensa volvieron antes.
  - [Columbia PDF](https://business.columbia.edu/sites/default/files-efs/pubfiles/1200/goalgradient.pdf) — **Moderada (clásico)**
- **Progreso dotado** (Nunes y Drèze 2006, *JCR*).
  - Tarjetas de lavado de autos: 8 sellos necesarios, frente a 10 con 2 ya puestos.
  - Canjearon el 34 % de quienes tenían la tarjeta con sellos, frente al 19 % con la tarjeta vacía (cifras de fuente secundaria).
  - El efecto es mayor "when consumers are provided with a reason for the endowment", aunque sea una razón engañosa.
  - Fuentes: [Wharton](https://knowledge.wharton.upenn.edu/?p=5630); cifras vía [Coglode](https://coglode.com/nuggets/endowed-progress-effect) — **Moderada**
- **Hipótesis del área pequeña** (Koo y Fishbach 2012, *JCR*). Al inicio motiva más mirar lo acumulado, y cerca del final, lo que falta. El efecto viene de una "illusion of fast progress" — [IDEAS/RePEc](https://ideas.repec.org/a/oup/jconrs/doi10.1086-663827.html) — **Moderada**

**Rachas, fallos y regreso**
- **Silverman y Barasch 2023:** ver una racha rota reduce el uso posterior. Ya está en las notas previas y en la decisión #17 — [UDSpace](https://udspace.udel.edu/items/42ce576b-8e1f-429a-8541-e29e48dbcfbb) — **Moderada**
- **Gershon** (experimento de campo de 6 semanas con la app "one sec"; seminario de CHIBE): las rachas "created new goals—to maintain or break streaks—that competed with users' original goals", y en conjunto aumentaron el uso de redes sociales que se quería reducir — [CHIBE](https://chibe.upenn.edu/event/rachel-gershon-phd%E2%94%82chibe-research-seminar/) — **Débil (resumen de seminario; trabajo sin publicar)**
- **Lally et al. 2010** (82 personas, 12 semanas).
  - Tiempo hasta la automaticidad máxima: 66 días, con un rango de 18 a 254.
  - "a single missed day had little impact on later automaticity gains", aunque muchos fallos repetidos sí reducen el máximo.
  - [BPS Research Digest](https://bps.org.uk/research-digest/how-form-habit) — **Moderada (muestra pequeña, sin réplica)**
- **Megaestudio de Milkman et al. 2021** (*Nature*; 61.293 personas, 54 intervenciones de 4 semanas).
  - "the top-performing intervention offered microrewards for returning to the gym after a missed workout": 125 puntos (0,09 USD) dieron +0,40 visitas por semana, un 27 % más que el placebo.
  - "Only 8% of interventions induced behaviour change that was significant and measurable after the four-week intervention."
  - [PDF](https://www.gwern.net/doc/statistics/prediction/2021-milkman.pdf) — **Moderada a fuerte (ECA masivo, población de gimnasio)**
- **Beshears et al. 2021** (*Management Science*): "Routine incentives generated fewer gym visits than flexible incentives", durante la intervención y después, cuando se pagaba solo en una franja fija de 2 h — [INFORMS](https://pubsonline.informs.org/doi/suppl/10.1287/mnsc.2020.3706) y [HBS Working Knowledge](https://www.library.hbs.edu/working-knowledge/unexpected-exercise-advice-for-the-super-busy-ditch-the-rigid-routine) — **Moderada**
- **Efecto "nuevo comienzo"** (Dai, Milkman y Riis 2014, *Management Science*): las búsquedas de "diet", las visitas al gimnasio y los compromisos con metas aumentan tras hitos temporales (lunes, inicio de mes, cumpleaños) — [PDF](https://faculty.wharton.upenn.edu/wp-content/uploads/2014/06/Dai_Fresh_Start_2014_Mgmt_Sci.pdf) — **Moderada**

**Recompensas y gamificación**
- **Deci, Koestner y Ryan 1999** (*Psychological Bulletin*; metaanálisis de 128 estudios).
  - Las recompensas contingentes a participar, completar o rendir bajaron la motivación intrínseca de libre elección (d = −0,40, −0,36 y −0,28), como "all tangible rewards, and all expected rewards".
  - "Positive feedback enhanced both free-choice behavior (d = 0.33) and self-reported interest (d = 0.31)."
  - La retroalimentación positiva "controladora" baja la motivación. Ejemplo del estudio: "Excellent, you should keep up the good work". La informativa, que da el resultado y su significado, la sube.
  - Las recompensas inesperadas no la afectaron (Tang y Hall, citados ahí).
  - [PDF](https://depts.washington.edu/techdocs/papers/deciExtrinsicRewardsAndIntrinsicMotivation99.pdf) — **Fuerte (clásico, debatido por Cameron y Pierce)**
- **Mekler et al. 2017** (*Computers in Human Behavior*): los puntos, niveles y rankings "did not significantly affect competence or intrinsic motivation". Solo subieron la cantidad de trabajo, porque funcionaron como incentivo extrínseco — [PDF](https://glassmanlab.seas.harvard.edu/annotated_works/mekler17.pdf) — **Moderada**
- **Mazeas et al. 2022** (*JMIR*; metaanálisis de ECA de gamificación y actividad física): a unas 14 semanas tras terminar, el efecto fue "very small to small" (g = 0,15; IC 0,07–0,23) — [JMIR 2022;24(1):e26779](https://www.jmir.org/2022/1/E26779/) — **Fuerte**
- **Koivisto y Hamari 2014** (195 personas usuarias de Fitocracy): "Perceived enjoyment and usefulness of the gamification decline with use, suggesting… novelty effects" — [Tampere](https://researchportal.tuni.fi/en/publications/demographic-differences-in-perceived-benefits-from-gamification/) — **Moderada (transversal)**
- **Dejonckheere et al. 2024** (*Computers in Human Behavior* 160:108360; muestreo de experiencias, 193 personas asignadas al azar).
  - Dar monedas virtuales al completar cada encuesta subió las respuestas "but only for participants who frequently bought rewards".
  - Y: "Paradoxically, momentary gamification also caused participants' responses to be slightly more unreliable."
  - [Tilburg](https://research.tilburguniversity.edu/en/publications/real-time-incentivizing-survey-completion-with-game-based-rewards/) — **Moderada**
  - En sentido contrario, van Berkel et al. 2017 encontraron mejor calidad con un ESM gamificado en otra tarea (describir lugares) — [UCL](https://discovery.ucl.ac.uk/id/eprint/10074318/) — **Moderada**. El efecto depende del diseño.
- **Schueller et al. 2021** (*JMIR Mental Health*, entrevistas con personas que usan apps de ánimo): "Some users reported less inclination to document their negative mood states and preferred to document their positive moods" — [JMIR 2021;8(8):e29368](https://mental.jmir.org/2021/8/e29368) y [PMC8387890](https://pmc.ncbi.nlm.nih.gov/articles/PMC8387890/) — **Débil (cualitativo)**
- **Sesgo de demanda** (de Quidt, Haushofer y Roth 2018, *AER*): cuando la gente infiere qué quiere el investigador, sus respuestas se mueven. En 11 tareas, el sesgo acotado fue de ~0,13 DE en promedio, "probably modest" — [AEA](https://www.aeaweb.org/doi/10.1257/aer.20171330) — **Moderada**

**Planes si-entonces y hábitos pequeños**
- **Sheeran, Listrom y Gollwitzer 2024/2025** (*European Review of Social Psychology*, 642 pruebas): las intenciones de implementación funcionaron para resultados cognitivos, afectivos y conductuales (0,27 ≤ d ≤ 0,66). "Effect sizes were larger when plans had a contingent (if-then) format, participants were highly motivated… and plans were rehearsed" — [KOPS](https://kops.uni-konstanz.de/handle/123456789/69905) — **Fuerte**
- **Tiny Habits (Fogg, 2019):** no encontré ensayos controlados publicados del método. Lo que hay son afirmaciones del autor y datos de coaching — [CNBC](https://www.cnbc.com/2020/02/14/stanford-scientist-on-proven-habits-that-will-make-you-more-productive.html) — **Débil o experta**

**Recompensa variable y patrones engañosos**
- **El modelo Hooked** (Eyal) describe cuatro pasos: disparador, acción, recompensa variable e inversión. "Variable schedules of reward are one of the most powerful tools that companies use to hook users"; compara con las tragamonedas y con "a lab animal in a Skinner box" — [Nir Eyal](https://www.nirandfar.com/how-to-manufacture-desire/) — **Experta** (describe la técnica; no es evidencia de beneficio)
- **Monge Roffarello, Lukoff y De Russis 2023** (CHI; revisión de 43 artículos). Los "attention capture damaging patterns" son "recurring patterns that designers adopt to manipulate users into spending attention in ways that often lead to a loss of sense of control and time, and feelings of regret". Encontraron 11 tipos, divididos en engañosos y seductores — [deceptive.design](https://deceptive.design/articles/defining-and-identifying-attention-capture-deceptive-designs-in-digital-interfaces) y [DOI](https://doi.org/10.1145/3544548.3580729) — **Moderada (revisión)**
- **Mathur et al. 2019** (CSCW, unos 11.000 sitios): el "confirmshaming" usa palabras y presión emocional para alejar de una opción; hallaron 169 casos — [Princeton](https://webtransparency.cs.princeton.edu/dark-patterns) — **Moderada**
- **FTC 2022**, *Bringing Dark Patterns to Light*: "deceptive design practices that trick or manipulate"; incluye las apps móviles — [Venable (resumen)](https://www.venable.com/insights/blogs/2022/09/the-ftc-brings-more-light-to-dark-patterns-in-new) — **Normativa (EE. UU., informe del personal)**
- **Robinhood:** quitó el confeti tras los hitos después de la denuncia de Massachusetts por "gamificación". El acuerdo de 7,5 M USD exigió revisar sus prácticas de "digital engagement" — [NBC Boston](https://www.nbcboston.com/news/local/massachusetts-looks-to-bar-trading-app-robinhood-company-sues/2357245/?amp=1) e [InvestmentNews](https://investmentnews.com/regulation-and-legislation/robinhood-to-pay-75m-to-settle-massachusetts-charges/248214) — **Normativa (caso regulatorio; sector financiero)**
- **Digital Fairness Act de la UE:** está "announced", con fecha indicativa del 4.º trimestre de 2026, y apunta al "addictive design of digital products". No está aprobada — [Parlamento Europeo, actualizado al 20-09-2026](https://www.europarl.europa.eu/legislative-train/theme-protecting-our-democracy-upholding-our-values/file-digital-fairness-act) — **Normativa en preparación**

### Inferencias para SpaceEase
- **Premiar el ensayo, no el resultado.** En SpaceEase, "ayudó" es una respuesta de la persona. Si solo "ayudó" trae objeto, arpegio y celebración, la app premia una respuesta concreta, que además no depende de la persona sino del entorno.
  - Riesgos: inflar los "ayudó" (Dejonckheere, de Quidt), evitar los "no ayudó" (Schueller) y contaminar el bandit y la frase "me ayudó en 5 de 6" de la solicitud.
  - Además, Deci 1999 muestra que las recompensas contingentes al rendimiento bajan la motivación intrínseca.
  - Por eso: **la misma respuesta (visual, sonora y háptica) para "ayudó", "no ayudó" y "no está claro"**. Lo que se celebra es "ya sabes algo más de este espacio".
- **Lo que se acumula y nunca baja:** pruebas terminadas, cosas aprendidas (incluido "esto no me sirve aquí") y solicitudes redactadas. Nunca días seguidos.
  - Sin huecos vacíos ni "3 de 12 objetos": el gradiente de meta y el área pequeña son justo mecanismos de presión.
  - El progreso dotado solo vale si es real. Por ejemplo, "Ya diste el primer paso: describiste tu espacio" cuenta algo que sí pasó.
- **Volver es lo que se premia, no la constancia.** Tras una ausencia: "Todo está como lo dejaste", más una acción de un toque para retomar. Sin decir cuántos días pasaron (Milkman, Lally, Silverman y Barasch). Un lunes o inicio de mes puede ofrecer, dentro de la app, "¿Empezamos una semana nueva?" (nuevo comienzo).
- **Sin franjas fijas obligatorias** (Beshears). La persona puede registrar cuando quiera; el recordatorio es una ayuda, no una cita.
- **Plan si-entonces opcional** al aceptar un ajuste: "Cuando me siente a leer en el escritorio, me pondré los tapones". Se rellena con la tarea y el espacio (Sheeran: mejor con formato si-entonces y repasado). El aviso "¿Cómo fue?" se ancla al bloque que la persona definió (decisión #11).
- **Medir el uso efectivo:** ensayos con valoración, ajustes aprendidos y solicitudes enviadas. No sesiones diarias. Hay que asumir de entrada que el uso caerá (Baumel; Perski; Yardley; decisión #19).

### Vacíos
- No hay estudios de recompensas, rachas ni celebraciones en apps con **personas adultas neurodivergentes**. Todo lo anterior es población general.
- No encontré el texto completo de Nunes y Drèze 2006 ni del artículo de Amabile en HBR; las cifras vienen de fuentes secundarias.
- El trabajo de Gershon sobre rachas está sin publicar (solo hay resumen de seminario).
- No hay ECA de Tiny Habits.
- Dejonckheere 2024 premiaba completar la encuesta, no una respuesta concreta. **No encontré** un estudio que mida directamente el efecto de premiar el contenido de una autoevaluación. La regla es una extrapolación razonable.

---

## 2. Lo específico de personas adultas autistas y con TDAH

### Takeaway
En el autismo, la **intolerancia a la incertidumbre** se asocia fuertemente con la ansiedad. Los estímulos imprevisibles provocan más reactividad sensorial que los previsibles, y el agotamiento ("burnout") baja la tolerancia a los estímulos durante meses. Por eso, en esta población la recompensa sorpresa y la variabilidad (el motor de Hooked) son contraproducentes. Lo que funciona es lo previsible, anunciado y personalizable.

En el TDAH, la **preferencia por lo inmediato** (descuento por demora, d = 0,43), la propensión al aburrimiento y la desregulación emocional (g = 1,17) piden respuesta inmediata, variedad y nada de vergüenza. Ojo: la novedad de la gamificación se gasta.

La tensión entre "previsible" (autismo) y "con novedad" (TDAH) se resuelve así: **la estructura y las reglas son fijas, y la variedad es opcional y la elige la persona**.

No encontré estudios de gamificación con personas adultas autistas o con TDAH, más allá de pilotos y pósteres.

### Hallazgos citados

**Autismo**
- **Jenkinson, Milne y Thompson 2020** (*Autism*; 12 estudios, 10 metaanalizados): la intolerancia a la incertidumbre y la ansiedad se correlacionan con r = 0,62 (IC 0,52–0,71) — [PMC7539603](https://pmc.ncbi.nlm.nih.gov/articles/PMC7539603/) — **Fuerte (pocos estudios)**
- **Normansell-Mossa et al. 2021** (55 personas adultas autistas y 199 no autistas): el mejor modelo fue sensibilidad sensorial → intolerancia a la incertidumbre → ansiedad. Los datos son transversales — [PMC8635111](https://pmc.ncbi.nlm.nih.gov/articles/PMC8635111/) — **Moderada**
- **Yosef et al. 2026** (*Autism Research*; fMRI, 13–27 años).
  - Encontraron "sensory cortical hyper-reactivity in ASD… in the Unpredictable condition", mientras que con estímulos anunciados por una imagen 2 s antes las respuestas "were overall similar".
  - La interacción grupo × condición no fue significativa.
  - [PMC13377290](https://pmc.ncbi.nlm.nih.gov/articles/PMC13377290/) — **Moderada**
- **Sinha et al. 2014** (*PNAS*, teoría): "A key determinant of habituation is stimulus predictability"; la falta de previsibilidad lleva a hipersensibilidad — [PMC4210351](https://pmc.ncbi.nlm.nih.gov/articles/PMC4210351) — **Experta (teoría)**
- **AASPIRE (Raymaker et al. 2019)**, guía web hecha con personas adultas autistas:
  - "highly consistent site behavior".
  - "Avoid textured backgrounds, moving images, decorative elements that do not convey information" y el "sonic 'clutter'".
  - Selección de paletas de color.
  - "Be specific and precise in language".
  - [PMC6485264](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/) — **Normativa o de consenso (participativa)**
- **Ng y Lee** (U. Delaware, 48 personas adultas autistas, entrevistas sobre apps de actividad física): lo negativo fue "unclear app use instructions and limited customization of reminder schedules"; lo favorable, "intuitive interfaces and a variety of accessibility features" — [UDel](https://www.urp.udel.edu/?p=17877) — **Débil (resumen de investigación estudiantil)**
- **Póster de SOUPS 2024** (BYU; 3 + 6 personas adultas autistas): preferían "customizable games that did not cause cognitive overload" — [USENIX](https://usenix.org/system/files/soups2024_poster53_abstract-xing_final.pdf) — **Débil**
- **Raymaker et al. 2020** (*Autism in Adulthood*, investigación participativa): el burnout autista implica agotamiento prolongado (normalmente 3 meses o más), pérdida de funciones y "reduced tolerance to stimulus" — [PubMed 32851204](https://pubmed.ncbi.nlm.nih.gov/32851204/) — **Débil a moderada (cualitativo)**
- **Nishith et al. 2025** (*J Autism Dev Disord*, 85 personas adultas autistas, trabajo): los temas fueron aceptación, comunicación, **autonomía** y ajustes. Solo se leyó el resumen — [MIT DSpace](https://dspace.mit.edu/handle/1721.1/163972?show=full) — **Moderada (encuesta)**
- **Elogio:** el único estudio encontrado (Weyman y Sy 2018) tiene 3 personas adultas con autismo y discapacidad intelectual. Aprendieron un poco más rápido con elogio entusiasta, y sus preferencias fueron mixtas. **No es generalizable** — [MDSOAR](https://mdsoar.org/handle/11603/7869) — **Débil**
- **Monotropismo** (Murray, Lesser y Lawson 2005, *Autism*): la atención autista tiende a concentrarse en "túneles"; las interrupciones cuestan más — [monotropism.org](https://monotropism.org/murray-lesser-lawson/) — **Experta (teoría)**

**TDAH**
- **Jackson y MacKillop 2016** (metaanálisis, 21 estudios, N = 3913): el descuento por demora es mayor en el TDAH (d = 0,43), sin diferencias por edad — [PMC5049699](https://pmc.ncbi.nlm.nih.gov/articles/PMC5049699) — **Fuerte**
- **Aburrimiento y TDAH** (metaanálisis 2026, 18 estudios, N = 22.365): r = 0,40 (IC 0,35–0,46). No pude verificar la edad de las muestras — [Springer](https://link.springer.com/article/10.1007/s10567-026-00563-9) — **Moderada (correlacional)**
- **Beheshti, Chavanon y Christiansen 2020** (*BMC Psychiatry*, 13 estudios con personas adultas): la desregulación emocional fue mayor en el TDAH (g = 1,17), y la labilidad, de g = 1,20 — [PMC7069054](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7069054/) — **Fuerte**
- **Bijlenga et al. 2017** (116 personas adultas con TDAH): más hiper- e hiposensibilidad, "especially apparent in the… Auditory" modality, con independencia de los rasgos autistas — [European Psychiatry](https://www.cambridge.org/core/journals/european-psychiatry/article/atypical-sensory-profiles-as-core-features-of-adult-adhd-irrespective-of-autistic-symptoms/B64037075E93613CF99CCF271F328DB8) — **Moderada**
- **Recordatorios con TDAH:** Nordby 2022 (SMS sin efecto en los inicios de sesión) y Spiel 2022 (contra el encuadre de déficit) ya están en el informe y en las notas previas.

### Inferencias para SpaceEase
- **Anunciar antes lo que va a pasar.** La primera vez se explica, con palabras y en el mismo lugar, qué hace el modo con detalles y cuándo suena algo. Ninguna celebración llega por sorpresa: lo previsible se habitúa mejor (Sinha, Yosef).
- **Cero recompensa variable:** nada de objetos raros, cofres, sorteos ni "a veces sale un brillo". La misma acción produce siempre la misma respuesta.
- **Variedad elegida, no impuesta.** Para el TDAH, la novedad vive en lo que la persona activa: temas de la escena, el cielo según la hora (ya existe) o un ajuste nuevo marcado como "Probemos algo nuevo" (decisión #10). Nunca en recompensas al azar.
- **Respuesta inmediata** tras la acción (descuento por demora): el resultado se ve en la misma pantalla, no "mañana tendrás tu objeto".
- **Sin vergüenza** (desregulación emocional, burnout): ningún mensaje cuenta ausencias. Tras semanas sin uso, la app recibe igual que siempre.
- **Elogio informativo y literal**, sin juicios sobre la persona (Deci; AASPIRE).
  - Sí: "Probaste los tapones 3 veces leyendo aquí; ayudó en 2. Todavía no es seguro."
  - No: "¡Increíble, eres un crack! ¡Sigue así!"
- **No interrumpir el túnel** (monotropismo): nada de celebraciones, pop-ups ni sonidos mientras la persona responde una pregunta. Las celebraciones solo van en la pantalla de resultado.

### Vacíos
- No encontré estudios publicados sobre gamificación, rachas o elogios con personas **adultas** autistas o con TDAH. El proyecto de Royal Holloway con estudiantes neurodivergentes estaba pendiente de publicación — [Royal Holloway](https://pure.royalholloway.ac.uk/en/projects/attitudes-of-neurodiverse-students-towards-gamification-in-higher/).
- La evidencia sobre lo imprevisible viene de estímulos aversivos, no de recompensas positivas sorpresa.
- La "rejection sensitive dysphoria" del TDAH no es un constructo validado, así que no la uso.

---

## 3. Sonidos de interfaz opcionales

(Búsqueda delegada en un subagente que abrió cada fuente. Las páginas de Material y de Apple se leyeron desde su JSON, y el código de Expo desde GitHub.)

### Takeaway
La tolerancia reducida al sonido es muy frecuente en el autismo: un 41 % actual y un 61 % a lo largo de la vida en el metaanálisis, sobre todo con muestras infantiles. Las personas adultas describen como lo peor los sonidos agudos, cortantes, repetitivos y repentinos. La misofonía se asocia con rasgos autistas, y en adultos con TDAH la sensibilidad auditiva también está aumentada.

Las guías coinciden:
- Sonido apagado por defecto, con su propio interruptor.
- Nada en acciones frecuentes.
- Sonidos cortos (menos de 1 s) y suaves.
- Bordes suaves (sin ataque brusco).
- Graves moderados y medios: evitar la zona de 2,5–5,5 kHz, que es la más desagradable, y la rugosidad de 30–150 Hz de las alarmas.
- Respetar el interruptor de silencio de iOS (categoría `.ambient`).

### Hallazgos citados

**Prevalencia y experiencia**
- **Williams, Suzman y Woynaroski 2021** (*Ear & Hearing*; 103 estimaciones, 13.093 personas autistas).
  - Hiperacusia actual: 41,42 % (37,23–45,84). A lo largo de la vida: 60,58 % (50,37–69,76).
  - El intervalo de predicción es amplio (10,96–74,22 %) y la edad media de la muestra, de 7,88 años.
  - [PMC8349927](https://pmc.ncbi.nlm.nih.gov/articles/PMC8349927/) — **Fuerte**
- **Landon, Shepherd y Lodhia 2016** (10 personas adultas autistas):
  - "All participants reported high-pitched or sharp sounds… as particularly problematic."
  - Los repetitivos molestan: "ticking, clocks… those repetitive things that don't stop".
  - Los repentinos, como el silbido de un hervidor, desbordan.
  - [PDF](https://autismnz.org.nz/wp-content/uploads/2021/02/2016-Landon-ASD.pdf) — **Débil**
- **Park et al.** (U. Michigan, ASSETS 2024): para relajarse, las personas participantes preferían sonidos graves (250, 125 y 60 Hz), una de ellas prefería el silencio, y pedían controlar "volume, pitch, regularity". El estudio trata sonidos de enmascaramiento, no de interfaz — [PDF](https://soundability.eecs.umich.edu/img/portfolio/Park_MaskSound_ASSETS2024.pdf) — **Débil**
- **Misofonía** (Swedo et al. 2022, consenso): "Trigger stimuli are often repetitive" y coexiste con el autismo y el TDAH — [Frontiers](https://www.frontiersin.org/journals/neuroscience/articles/10.3389/fnins.2022.841816/full) — **Normativa o de consenso**. Rinaldi et al. 2022 encontraron rasgos autistas elevados en la misofonía (AQ 24,7 frente a 17,3) — [PMC9986206](https://pmc.ncbi.nlm.nih.gov/articles/PMC9986206) — **Moderada**
- **Sobresalto** (Takahashi et al. 2018): las niñas y niños autistas tuvieron mayor respuesta de sobresalto ante estímulos **débiles** — [Frontiers](https://www.frontiersin.org/journals/psychiatry/articles/10.3389/fpsyt.2018.00355/pdf) — **Moderada (infancia)**

**Qué hace desagradable un sonido**
- **Kumar et al. 2008:** la desagradabilidad se concentra en "spectral frequencies between 2500 and 5500 Hz" y en modulaciones temporales de 1–16 Hz — [Newcastle](https://eprints.ncl.ac.uk/150198) — **Moderada**
- **Arnal et al. 2015:** los gritos ocupan las modulaciones de "∼30–150 Hz" (rugosidad), y "alarm but not musical sounds exploit scream-like rough modulations" — [PMC4562283](https://pmc.ncbi.nlm.nih.gov/articles/PMC4562283) — **Moderada**
- **Máxima sensibilidad del oído:** alrededor de 4 kHz (*Sonification Handbook*, cap. 3) — [PDF](https://sonification.de/handbook/download/TheSonificationHandbook-chapter3.pdf) — **Experta (clásico)**
- **Brewster, sobre Edworthy:** captan la atención "High pitch, a wide pitch range, rapid onset and offset times, irregular harmonics", y los sonidos con "low intensity and regular rhythm" se pueden ignorar. Las notas van de 125–150 Hz a 5 kHz — [Glasgow](https://www.dcs.gla.ac.uk/~stephen/earcon_guidelines.shtml) — **Experta (clásico)**

**Guías de diseño de sonido**
- **Microsoft, Windows UX** — [Learn](https://learn.microsoft.com/en-us/windows/win32/uxguide/vis-sound) — **Experta**
  - "short (less than one second)", "soft or moderate in volume" y "mid to high frequency (600 Hertz [Hz] to 2 kilohertz [kHz])".
  - "a soft fade-in and fade-out (soft 'edges')".
  - "Don't repeat a sound more than two times consecutively"; en una serie de eventos, sonido solo en el primero.
  - "Consider not assigning sounds to frequently occurring events by default" y "When in doubt, don't use sound".
  - Su consejo de no poner control de volumen depende del mezclador por app de Windows y no se aplica a iOS.
- **Material Design** — [Applying sound](https://m2.material.io/design/sound/applying-sound-to-ui.html) y [Sound attributes](https://m2.material.io/design/sound/sound-attributes.html) — **Experta**
  - El sonido no suele convenir en "Actions that are performed frequently" ni con "Users who have requested no interruptions".
  - "Limit the frequency of decorative sound to reduce user fatigue."
  - "Use softer, quieter timbres for low-priority sounds."
  - "A softer attack is more ambient."
  - "Repetition commonly indicates thinking, waiting, or lack of progress."
  - Medir la sonoridad percibida en dB(A), no los picos.
- **Apple WWDC 2017, sesión 803** — [Designing Sound](https://developer.apple.com/videos/play/wwdc2017/803/) — **Experta**
  - "Silence is golden."
  - Un sonido de interfaz "has a much lower volume than a notification sound" y hay que dar "the option for people to turn them off".
  - Desfasar sonido y háptica "as little as ten milliseconds sometimes makes a difference".
- **Apple WWDC 2019, sesión 810** — [Audio-Haptic](https://developer.apple.com/videos/play/wwdc2019/810/) — **Experta**
  - "Use moderation. Don't add sound and haptics just because you can."
  - "imagine using it 100 times more… are you overwhelmed?"
- **Apple HIG** — **Normativa**
  - [Playing audio](https://developer.apple.com/design/human-interface-guidelines/playing-audio): con el modo silencio se callan los "nonessential sounds, such as keyboard clicks, sound effects".
  - [Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications): un sonido propio debe ser "short, distinctive".
- **Estudios con personas** — **Moderada**
  - Schmidmaier et al. 2020 (CHI EA, 39 personas; melodías de 420–680 ms): las ascendentes y mayores se percibieron como más confiables, y la altura no tuvo efecto — [PDF](https://www.medien.ifi.lmu.de/pubdb/publications/pub/schmidmaier2020chi/schmidmaier2020chi.pdf)
  - Bhatara et al. 2025 (100 personas, 30 sonidos de aparatos): el ataque, la liberación, la frecuencia fundamental y el centroide influyen en la emoción percibida. Solo se verificó el resumen — [DOI](https://doi.org/10.1155/hbe2/5925146)

**iOS y Expo** — **Normativa**
- [`.ambient`](https://developer.apple.com/documentation/avfaudio/avaudiosession/category-swift.struct/ambient): "audio from other apps mixes with your audio. Screen locking and the Silent switch… silence your audio".
- [`.playback`](https://developer.apple.com/documentation/avfaudio/avaudiosession/category-swift.struct/playback) ignora el interruptor de silencio.
- [`duckOthers`](https://developer.apple.com/documentation/avfaudio/avaudiosession/categoryoptions-swift.struct/duckothers): "Don't use it to duck the audio of other apps for more than a few seconds".
- [expo-audio](https://docs.expo.dev/versions/latest/sdk/audio/): **`playsInSilentMode` vale `true` por defecto**, es decir, `.playback`. Hay que poner `playsInSilentMode: false` con `interruptionMode: 'mixWithOthers'` para obtener `.ambient` (ver el [código fuente](https://github.com/expo/expo/blob/main/packages/expo-audio/ios/AudioModule.swift)). **SpaceEase ya lo hace.**
- Por defecto, el botón de Acción activa y desactiva el modo silencio — [Apple Support](https://support.apple.com/105103).
- "Reduce Loud Audio" solo afecta a los auriculares, no al altavoz — [Apple Support](https://support.apple.com/guide/iphone/check-your-headphone-audio-levels-iph0596a9152/ios).
- WCAG 1.4.2: lo que suena solo más de 3 s necesita control — [W3C](https://www.w3.org/WAI/WCAG22/Understanding/audio-control.html).

### Inferencias (cifras para los sonidos de SpaceEase)

| Parámetro | Regla | Base |
|---|---|---|
| Por defecto | Apagado, con su propio interruptor, separado de "Con detalles" y de la vibración; vista previa en Ajustes | Microsoft, WWDC17, prevalencia del 41 % |
| Categoría | `.ambient` (`playsInSilentMode: false`, `mixWithOthers`); nunca reducir el volumen de otras apps; restaurar tras grabar | Apple, Expo (ya implementado) |
| Cuándo suena | Solo como respuesta inmediata (≤ 100 ms) a un toque de la persona, o cuando aparece en pantalla el resultado que está mirando. Nada al elegir, al pasar de pregunta ni al desplazarse | Material, Microsoft, Yosef |
| Cuántos | 1 por acción; ≤ 3 por registro; el mismo, como mucho 2 veces seguidas; los grupos se funden en uno | Microsoft, WWDC19 |
| Duración | Confirmar ≤ 400 ms; resultado ≤ 700 ms; tope de 1 s con la cola | Microsoft; Schmidmaier |
| Notas | 1–2 (máx. 3), cada una ≥ 80 ms; intervalo ascendente consonante para "listo"; sin figuras repetidas (suenan a "esperando") | Brewster, Material, Schmidmaier |
| Frecuencias | Fundamentales de 400–1000 Hz; energía de 2,5–5,5 kHz al menos ~20 dB por debajo; nada sobre 5 kHz; nada que dependa de menos de ~200 Hz (el altavoz no lo reproduce) | Kumar, Brewster, Landon, WWDC17 |
| Rugosidad | Sin trémolo, batidos ni modulaciones de 30–150 Hz, ni de 1–16 Hz en contenido brillante | Arnal, Kumar |
| Envolvente | Ataque ≥ 10 ms (mejor 15–30 ms, coseno); caída exponencial ≥ 150 ms, nunca cortada | Microsoft, Material, Brewster |
| Volumen | Misma sonoridad percibida (±1 dB, LUFS o dB(A)); "resultado" nunca más fuerte que "confirmar"; mantener el nivel bajo actual de los archivos y no subirlo | Material, Brewster, WWDC17 |
| Avisos | Sin sonido por defecto (`sound: false`); nunca un sonido propio | Material, HIG, Expo (ya implementado) |
| Coherencia | Una sola familia (mismo timbre y tonalidad); el mismo sonido siempre significa lo mismo; sin variación aleatoria; nunca es la única señal | Microsoft, Material, HIG |

**Diferencias con el código actual**
- `success` dura 900 ms: pasarlo a ≤ 700 ms.
- `make_sounds.py` usa ataques de 6–10 ms: subirlos a ≥ 15 ms.
- El filtro de paso bajo a 3,2 kHz deja el 4.º armónico de 880 Hz (3,52 kHz) dentro de la banda 2,5–5,5 kHz: bajar el corte o el sobretono.
- `pixel` suena en cada toque de la escena: limitarlo a uno por ventana "viva" de 5 s.

### Vacíos
- No hay estudios que midan sonidos de interfaz con personas adultas autistas o con TDAH. Todas las reglas son extrapolaciones.
- Sin umbral humano verificado de "ataque suave" a volumen de interfaz.
- Las tablas de ISO 226 son de pago.
- Ninguna plataforma da un objetivo LUFS para sonidos de interfaz.
- El efecto de Yosef 2026 no tuvo interacción significativa.

---

## 4. Animación en el modo opcional: celebraciones, escena en reposo y seguridad vestibular

### Takeaway
El modo opcional puede tener más vida, pero con el mismo criterio que el modo tranquilo:
- **Movimiento con propósito, local y breve**; nada en lo frecuente; siempre se puede interrumpir.
- **Reducir movimiento manda sobre "Con detalles"**.

Sobre las celebraciones:
- Más "jugo" no es mejor: el efecto sobre la experiencia tiene forma de U invertida.
- **Amplificar** el efecto, sin ligarlo a un éxito real, redujo la motivación.
- La celebración más famosa del sector (el confeti de Robinhood) acabó retirada tras la presión regulatoria.

Sobre la animación en reposo:
- Debe detenerse antes de 5 s.
- Sin oscilaciones sostenidas (Apple señala ~0,2 Hz).
- Sin destellos (> 3/s).
- Un solo elemento a la vez.

### Hallazgos citados
- **Apple HIG: Motion** — [HIG](https://developer.apple.com/design/human-interface-guidelines/motion) — **Normativa**
  - "Add motion purposefully… Don't add motion for the sake of adding motion. Gratuitous or excessive animation can distract people and may make them feel disconnected or physically uncomfortable."
  - "In apps, generally avoid adding motion to UI interactions that occur frequently."
  - "Aim for brevity and precision in feedback animations… a succinct animation that's precisely tied to a successful action."
  - "Let people cancel motion."
  - En la sección de visionOS: "Avoid showing objects that oscillate in a sustained way… avoid showing an oscillation that has a frequency of around 0.2 Hz because people can be very sensitive to this frequency… keep the amplitude low". También advierte sobre el movimiento en la periferia.
- **WCAG 2.2:**
  - 2.2.2: lo que se mueve solo más de 5 s debe poder pausarse.
  - 2.3.1: no más de 3 destellos por segundo.
  - 2.3.3: la animación por interacción se puede desactivar.
  - Fuente: [Understanding 2.3.3](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html) — **Normativa** (ya en las notas previas, §3)
- **AASPIRE:** "Avoid… moving images, decorative elements that do not convey information" — [PMC6485264](https://pmc.ncbi.nlm.nih.gov/articles/PMC6485264/) — **Normativa o de consenso**
- **Burke et al. 2005** (*ACM TOCHI*): los banners redujeron la velocidad de búsqueda visual, y con animación aumentó la carga percibida (NASA-TLX: frustración y demanda mental) — [PDF](https://thoughtcrumbs.com/publications/ToCHI04.pdf) — **Moderada (clásico)**
- **Kao 2020** (*Entertainment Computing* 34): cuatro niveles de "jugo" en un RPG de acción; "none and extreme amounts of juiciness significantly decrease player experience", y los niveles medio y alto fueron los mejores — [arXiv 2208.06155, que lo cita](https://arxiv.org/pdf/2208.06155) y [resumen](https://www.goodreads.com/author_blog_posts/19932694-the-effects-of-juiciness-in-an-action-rpg-new-study) — **Moderada (no leí el original)**
- **Kao et al. 2024** (CHI, preinscrito, 1699 personas): "Success dependence enhanced all motives, while amplification unexpectedly reduced them, possibly because the tested condition unintentionally impeded players' sense of agency" — [Imperial](https://spiral.imperial.ac.uk/entities/publication/253c32f5-d124-4a23-88b5-9aaaf114608d) — **Moderada**
- **WWDC19:** "imagine using it 100 times more… are you overwhelmed?" — [Apple](https://developer.apple.com/videos/play/wwdc2019/810/) — **Experta**
- **Robinhood:** dejó de usar "animations of confetti bursting on users' screens after they made their first trade and reached other milestones" tras la denuncia de Massachusetts — [NBC Boston](https://www.nbcboston.com/news/local/massachusetts-looks-to-bar-trading-app-robinhood-company-sues/2357245/?amp=1) — **Normativa (caso)**

### Inferencias para SpaceEase ("Con detalles")
- **Una celebración por hito, no por acción.**
  - Ocurre cuando se aprende algo nuevo de un espacio, sea "ayudó", "no ayudó" o "no está claro" (§1), o al redactar la primera solicitud.
  - Como mucho una por sesión. Nunca al guardar un registro, al elegir ni al navegar (HIG, WWDC19).
- **Local y breve.**
  - Ocurre dentro de la escena en pixel art, no a pantalla completa.
  - ≤ 1–1,5 s en total, a pocos fotogramas (`Easing.steps`), sin partículas, confeti, sacudidas, zoom ni rebotes.
  - Se puede interrumpir tocando o navegando, y el contenido es legible desde el primer fotograma (HIG; Kao 2020 y 2024).
- **Ligada a lo que pasó.** El objeto que aparece corresponde al ajuste probado (dependencia del éxito, Kao 2024). Nada de brillos genéricos.
- **Escena en reposo** (la implementación actual cumple):
  - Se mueve solo al llegar o al tocarla, ≤ 5 s y luego queda quieta.
  - Un elemento a la vez, con pausas, amplitud de pocos píxeles y nada que oscile de forma continua.
  - Se para fuera de pantalla.
  - Añadir: **nunca en pantallas de pregunta**, solo en Hoy y en el resultado (Burke; monotropismo).
- **Sin destellos:** los cambios de brillo del pixel art (pantalla, cielo) son lentos y de bajo contraste; nunca alternancias por encima de 3/s (WCAG 2.3.1).
- **Reducir movimiento gana siempre.** Con él activo, la celebración se vuelve texto estático ("Nuevo en tu escritorio: lámpara"), y el sonido o la vibración solo suenan si la persona los activó aparte. Ya está implementado con `useMotionLevel`.

### Vacíos
- No hay estudios sobre celebraciones o animación de interfaz con personas adultas autistas o con TDAH.
- El umbral de 0,2 Hz viene de la guía de visionOS, que es inmersivo; en iOS es una precaución, no un requisito.
- No encontré una cifra de "cuántas celebraciones antes de que sean ruido"; la regla de "una por sesión" es inferencia.

---

## 5. Recordatorio diario opcional: cuándo y cómo decirlo

### Takeaway
Los recordatorios tienen efectos **pequeños y que se desgastan**. En una app de bienestar laboral, enviar un aviso subió la probabilidad de uso en 24 h solo un 3,9 %.

Las guías oficiales coinciden en:
- Solo a petición, con la persona eligiendo frecuencia, hora y canal.
- Nunca repetir el mismo aviso si no hubo respuesta.
- Nada sensible en la pantalla de bloqueo.
- No ordenar tareas.
- Urgencia honesta.

Las personas adultas autistas se quejan, precisamente, de recordatorios poco personalizables.

El lenguaje controlador ("deberías") y el que avergüenza ("confirmshaming") están documentados como presión. El efecto de cambiar "debes" por "podrías" fue nulo en un ECA, así que la regla se justifica por respeto y por la población, no por eficacia.

### Hallazgos citados
- **COGA (W3C)** — [W3C COGA](https://www.w3.org/TR/coga-usable/) — **Normativa (guía suplementaria)**
  - "Reminders must be set only at the user's request and the user must be able to personalize the remainder method."
  - "I need to control when reminders are sent, the frequency and type of reminders so that I do not become distracted by too many reminders."
  - "Always give the option to set a reminder at the end of the task so that the user does not get interrupted."
  - "It is essential not to add unwanted reminders."
  - "The user is the best person to know how many reminders, and which type, will best meet their needs."
- **Apple HIG** — [Notifications](https://developer.apple.com/design/human-interface-guidelines/notifications) y [Managing notifications](https://developer.apple.com/design/human-interface-guidelines/managing-notifications) — **Normativa**
  - "Avoid sending multiple notifications for the same thing, even if someone hasn't responded."
  - "Avoid sending a notification that tells people to perform specific tasks within your app."
  - "Avoid including sensitive, personal, or confidential information in a notification."
  - "Provide generically descriptive text to display when notification previews aren't available."
  - "Build trust by accurately representing the urgency of each notification."
- **Bidargaddi et al. 2018** (*JMIR mHealth*; ensayo microaleatorizado, 1255 personas, app de **bienestar laboral**, 89 días).
  - Enviar un aviso subió el uso en 24 h un 3,9 % (RR 1,039).
  - El efecto se atenuó con el tiempo, aunque esa atenuación no fue significativa.
  - El mayor efecto fue a las 12:30 en fin de semana (+11,8 %).
  - [JMIR mHealth 2018;6(11):e10123](https://mhealth.jmir.org/2018/11/e10123) — **Moderada**
- **Alkhaldi et al. 2016** (*JMIR*, revisión sistemática; 14 estudios, 8774 personas): "borderline small-to-moderate positive effects", con heterogeneidad alta. "No firm conclusions were drawn about which characteristics of strategies were associated with effectiveness" — [JMIR 2016;18(1):e6](https://jmir.org/2016/1/e6), vía [Mental Elf](https://nationalelfservice.net/treatment/other/internet-based-treatment/do-prompts-help-sustain-engagement-with-digital-interventions) — **Fuerte (revisión), efecto pequeño**
- **Klasnja et al. 2018** (HeartSteps, 44 personas): las sugerencias empezaron con +66 % de pasos en 30 min, y el efecto "diminished over time" — [PMC6401341](https://pmc.ncbi.nlm.nih.gov/articles/PMC6401341) — **Moderada** (ya en la decisión #9)
- **Ng y Lee:** a las personas adultas autistas no les gustó la "limited customization of reminder schedules" — [UDel](https://www.urp.udel.edu/?p=17877) — **Débil**
- **Altendorf et al. 2019** (*Digital Health*, 521 personas): el lenguaje que apoya la autonomía, frente al controlador ("You must drink less"), y ofrecer elección no cambiaron ni la autonomía percibida ni la reactancia — [PMC6393822](https://pmc.ncbi.nlm.nih.gov/articles/PMC6393822/) — **Moderada (nulo)**
- **Deci 1999:** la retroalimentación con "should" se vive como presión y baja la motivación intrínseca frente a la informativa — [PDF](https://depts.washington.edu/techdocs/papers/deciExtrinsicRewardsAndIntrinsicMotivation99.pdf) — **Fuerte en la dirección; 2 estudios en lo concreto**
- **Culpa:** Peng et al. 2023 (metaanálisis de 26 estudios) encontraron resultados mixtos. Pedir una reparación ("compénsalo") puede hacer que la gente se sienta coaccionada y debilita el mensaje — [PMC10568480](https://pmc.ncbi.nlm.nih.gov/articles/PMC10568480/) — **Fuerte (otro dominio)**
- **Confirmshaming:** Mathur et al. 2019 — [Princeton](https://webtransparency.cs.princeton.edu/dark-patterns) — **Moderada**

### Inferencias para SpaceEase
- **Cuándo:**
  - La persona elige el **día y la hora**. Ahora el resumen semanal está fijo a las 10:00; hay que dejar cambiar la hora (Ng y Lee; COGA).
  - El recordatorio diario se ofrece **al terminar** un registro ("¿Quieres que te lo recuerde mañana a esta hora?"), nunca al instalar (COGA: "at the end of the task").
  - Por defecto se propone la misma hora del registro que se acaba de hacer, que es su propia rutina (planes si-entonces).
- **Cuántos:**
  - Como mucho **1 al día** para el registro diario, aparte de los "¿Cómo fue?" que ya están acotados (decisión #11).
  - **Si no se contesta, no se repite** (HIG).
  - Tras 5 recordatorios seguidos sin abrir, se suspende solo y, la próxima vez que la persona abra la app (nunca con otro aviso), se pregunta: "¿Seguimos, cambiamos la hora o lo dejamos?" (HIG; Klasnja; KCL). La cifra de 5 es inferencia.
- **Nivel:** `passive` para el diario y el semanal, `active` solo para "¿Cómo fue?". Nunca `timeSensitive`, sin insignia en el icono y sin sonido por defecto (HIG; §3).
- **Pantalla de bloqueo:** texto genérico. **Nunca** el nombre del ajuste (por ejemplo, "Pedir un separador", que revela un ajuste laboral), "molestia", "ruido de tus compañeros", "sensorial" ni diagnósticos (HIG; el 70 % teme revelar, informe #1).
  - Hoy, `notificationBody` dice "Cuéntanos cómo te fue con “${adjustment}”": hay que cambiarlo, o mostrar el detalle solo si la persona lo activa en Ajustes.
- **Redacción** (estable, literal, sin exclamaciones ni emoji, en segunda persona y sin "deberías"):

  | Sí | No |
  |---|---|
  | "SpaceEase · Tu registro de hoy, si te viene bien." | "¡No rompas tu racha!" / "Llevas 3 días sin registrar" |
  | "¿Cómo fue el bloque? Puedes contestar ahora o más tarde." | "Te echamos de menos" / "Tu escritorio te espera 😢" |
  | "Tu semana en SpaceEase: tres cosas, para cuando quieras verlas." (ya existe) | "Deberías registrar para mejorar" / "No pierdas tu progreso" |
  | Acciones: "Registrar" · "Mañana" · "Cambiar hora" | Al apagar: "No, prefiero seguir con molestias" (confirmshaming) |
  | Al volver tras semanas: "Todo está como lo dejaste." | "Bienvenido de nuevo, hace 23 días que no venías" |

- **El mismo texto cada día**, sin variantes "creativas" que cambien al azar: lo previsible tranquiliza (§2), y la variación es para el contenido que la persona elige.

### Vacíos
- No hay evidencia sobre la hora o el tono óptimos para personas adultas autistas o con TDAH.
- No hay estudios que comparen el texto genérico con el detallado en la pantalla de bloqueo.
- La cifra de suspender tras 5 avisos sin abrir es inferencia.

---

## 6. Síntesis: reglas para el modo "Con detalles" y para lo que está activo por defecto

Prioridad: **P0** antes de lanzar el modo; **P1** en la siguiente iteración.

| # | P | Regla | Evidencia | Solidez |
|---|---|---|---|---|
| 1 | P0 | **Premiar el ensayo, no el resultado.** La misma respuesta para "ayudó", "no ayudó" y "no está claro" ("Ya sabes algo más de este espacio"). Quitar "Si te ayuda, aparecerá en tu escritorio" de antes de la valoración. El objeto llega en silencio y, como el resto de la app, se marca como tentativo hasta que haya más evidencia | Dejonckheere 2024; Schueller 2021; Deci 1999 (recompensa por rendimiento, d = −0,28); de Quidt 2018 | Moderada + inferencia |
| 2 | P0 | **El progreso solo se acumula:** pruebas hechas, cosas aprendidas y solicitudes. Sin días seguidos, caducidad ni ceros, y sin huecos vacíos ni "3 de 12" | Silverman y Barasch 2023; Lally 2010; Gershon; Koo y Fishbach 2012 | Moderada |
| 3 | P0 | **Volver es lo que cuenta:** "Todo está como lo dejaste" y retomar con un toque; nunca contar ausencias. Dejar la app tras aprender no es un fracaso | Milkman 2021; Dai 2014; Raymaker 2020; Baykoca 2026; Yardley 2016 | Moderada |
| 4 | P0 | **Nada aleatorio:** la misma acción produce siempre la misma respuesta, explicada antes. Sin sorpresas, rarezas, cofres ni "a veces" | Hooked (Eyal); Monge Roffarello 2023; Jenkinson 2020 (r = 0,62); Yosef 2026; Sinha 2014 | Moderada |
| 5 | P0 | **Retroalimentación informativa, no elogio a la persona.** "Probaste 3 veces; ayudó en 2", nunca "¡Eres genial!" ni "Sigue así" ni "deberías" | Deci 1999 (informativa d = +0,33; "should" controla); Mekler 2017; AASPIRE | Fuerte en la dirección |
| 6 | P0 | **"Con detalles" es una elección, no un empujón:** se ofrece una vez, con vista previa y "Así está bien" igual de visible, y se revierte en Ajustes. Animación, sonido y vibración son interruptores separados, apagados por defecto, que nunca se activan solos tras una actualización | Microsoft UX; COGA; AASPIRE; Williams 2021 (41 % de tolerancia reducida al sonido) | Normativa + fuerte |
| 7 | P0 | **Reducir movimiento manda:** con él activo, sin movimiento (solo fundidos) y celebración en texto estático | WCAG 2.3.3; Apple HIG | Normativa |
| 8 | P0 | **Sonido solo si lo provocó la persona:** respuesta ≤ 100 ms a su toque o al resultado que mira. `.ambient`, sin reducir el volumen de otras apps; nada al elegir o navegar; ≤ 1 por acción, ≤ 3 por registro | Apple AVAudioSession; Material; Microsoft; WWDC19; Yosef 2026 | Normativa + experta |
| 9 | P0 | **Avisos genéricos en la pantalla de bloqueo** (sin nombre del ajuste ni palabras sensibles), sin sonido, sin insignia; `passive` o `active`, nunca `timeSensitive` | Apple HIG Notifications; informe #1 | Normativa |
| 10 | P1 | **Acústica:** confirmar ≤ 400 ms, resultado ≤ 700 ms, tope 1 s; 1–2 notas; fundamentales de 400–1000 Hz; −20 dB en 2,5–5,5 kHz y nada sobre 5 kHz; ataque ≥ 15 ms y caída ≥ 150 ms; sin trémolo de 30–150 Hz; misma sonoridad ±1 dB | Kumar 2008; Arnal 2015; Landon 2016; Brewster; Microsoft | Moderada + experta |
| 11 | P1 | **Celebración local, breve y ligada al hecho:** dentro de la escena, ≤ 1–1,5 s, a pasos, interrumpible, una por hito y como mucho una por sesión. Sin confeti, partículas, zoom ni rebotes | Apple HIG Motion; Kao 2020; Kao 2024; Robinhood; WWDC19 | Moderada + normativa |
| 12 | P1 | **Escena en reposo:** solo al llegar o al tocarla, ≤ 5 s, un elemento a la vez, amplitud de pocos píxeles, sin oscilación sostenida (~0,2 Hz), sin destellos > 3/s; nunca en pantallas de pregunta | WCAG 2.2.2 y 2.3.1; HIG visionOS; AASPIRE; Burke 2005 | Normativa + moderada |
| 13 | P1 | **Recordatorio diario:** se ofrece al terminar un registro; la persona elige día **y hora**; 1 al día como máximo; nunca se repite si no hay respuesta; tras 5 sin abrir se suspende y se pregunta dentro de la app | COGA; HIG; Ng y Lee; Bidargaddi 2018 (+3,9 %); Alkhaldi 2016; Klasnja 2018 | Normativa + moderada |
| 14 | P1 | **Texto de aviso estable y sin presión:** invitación con opción ("si te viene bien"), acciones "Mañana" y "Cambiar hora", y "No, gracias" neutro al apagar | Deci 1999; Mathur 2019; Peng 2023; Altendorf 2019 (efecto nulo: se hace por respeto) | Moderada |
| 15 | P1 | **Plan si-entonces opcional** al aceptar un ajuste ("Cuando me siente a leer aquí, me pondré…"), sin exigir hora fija | Sheeran 2024 (642 pruebas, d = 0,27–0,66); Beshears 2021 | Fuerte |
| 16 | P1 | **Variedad que elige la persona** (temas de la escena, "Probemos algo nuevo" señalado), con respuesta inmediata en la misma pantalla. La estructura nunca cambia | Jackson y MacKillop 2016 (d = 0,43); Koivisto y Hamari 2014; Mazeas 2022 (g = 0,15); aburrimiento r = 0,40 | Fuerte (rasgos) + inferencia (diseño) |
| 17 | P1 | **Relación sin comparación:** sin rankings ni invitaciones a compartir. La relación viene del tono, de "otras personas con tareas parecidas probaron…" (agregado, con umbral de privacidad) y de compartir con alguien de confianza si la persona quiere | Borghouts 2021; Baykoca 2026; Perski 2017; informe #1 | Fuerte (factor) + inferencia |
| 18 | P1 | **Medir el uso efectivo:** ensayos valorados, cosas aprendidas y solicitudes enviadas. No sesiones diarias ni tiempo en la app, y no hacer pruebas A/B de textos de presión | Yardley 2016; Baumel 2019 (3,3 % a 30 días); Perski 2017 | Moderada |

### Lo que NO se hace
- **Celebrar solo "ayudó"** o anunciar antes de la valoración que habrá premio si ayuda.
- **Rachas** de cualquier tipo, incluidas las "perdonables" con congelación (siguen siendo una racha). Tampoco "días seguidos", ceros ni contadores que bajen.
- **Recompensa variable:** cofres, sorteos, objetos raros, desbloqueos sorpresa, contenido de celebración al azar.
- **Puntos, XP, niveles, insignias y rankings.**
- **Colecciones con huecos** ("3 de 12", siluetas vacías) o barras de "casi lo tienes".
- **Confeti, partículas, sacudidas, zoom y rebotes**, o celebraciones al guardar, elegir o navegar, o más de una por sesión.
- **Sonido:** al tocar, elegir o navegar, o en los avisos. Tampoco ignorar el interruptor de silencio (`.playback`), bajar la música de la persona ni superar 1 s. Nada de campanas agudas (fundamentales > 2 kHz) ni trémolo.
- **Textos de culpa, miedo a perderse algo o "deberías":** "Te echamos de menos", "No pierdas tu progreso", "Llevas X días sin…", "Tu escritorio te espera".
- **Confirmshaming** al rechazar o apagar ("No, prefiero seguir con molestias").
- **Avisos repetidos** por lo mismo, avisos para "recuperar" a quien no abre la app, `timeSensitive` o insignias en el icono.
- **Datos sensibles en la pantalla de bloqueo:** nombre del ajuste, "molestia", "sensorial" o diagnósticos.
- **Activar solo "Con detalles" o los sonidos** tras una actualización, o preguntarlo más de una vez.
- **Bucles de animación que no paran**, movimiento en pantallas de pregunta u oscilaciones lentas continuas.

### Pendiente fuera de estas notas
- **`DESIGN.md`:** §5 dice "Sonido: Ninguno" y §6 no menciona el modo opcional, pero el código ya tiene sonidos y "Con detalles". Según la regla del propio documento, hay que **actualizar `DESIGN.md` antes** con una sección "Con detalles" que recoja las reglas 1–18.
- **Co-diseño:** validar con personas autistas y con TDAH (informe #21) la celebración, los cuatro sonidos y el texto de los avisos, con escucha en el altavoz del iPhone y a volumen bajo.
