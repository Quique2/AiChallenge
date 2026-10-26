# ml — Modelo de audio propio

Clasifica sonidos de oficina en ~10 s de audio para que la app pueda decir *"parece que hay voces cerca"* sin depender de una API externa. Se entrena aquí (GPU RTX 5070) y **corre en el teléfono**.

## Por qué en el teléfono

Grabar conversaciones de otras personas es el caso legalmente más delicado en EE. UU., Canadá y México. Ver la investigación en [`docs/research/reports`](../docs/research/reports/Ajustes%20sensoriales%20laborales%20y%20neurodivergencia.md), decisión 2. Por eso **el audio nunca sale del teléfono**: se analiza ahí y se borra. Lo único que llega al servidor son las etiquetas que la persona confirma ("voces", "ruido constante", "ruidos repentinos").

Hoy la app usa heurísticas de señal en [`apps/mobile/src/lib/audio-features.ts`](../apps/mobile/src/lib/audio-features.ts):

- **Voces:** energía concentrada en la banda del habla (300–3400 Hz) que sube y baja al ritmo de las sílabas (2–8 Hz).
- **Ruido constante:** el nivel apenas varía entre ventanas.
- **Ruidos repentinos:** subidas bruscas más fuertes que el resto de la grabación.

[`checks/audio-features.check.ts`](checks/audio-features.check.ts) las prueba con señales sintéticas. El modelo entrenado las reemplaza.

## Clases v1

Multi-etiqueta (sigmoid): en una oficina suenan varias cosas a la vez. Las tres primeras se conectan directo con el catálogo de la app; las demás sirven para mejorar la precisión y para futuros ajustes.

| id | Estímulo del catálogo | Ejemplos |
|---|---|---|
| `voces` | `voices` | Compañeros hablando, llamadas ajenas |
| `zumbido` | `noise_constant` | Clima, ventilación, ventiladores de PC |
| `golpes` | `noise_sudden` | Puertas, impresora, teléfonos, objetos que caen |
| `teclado` | — | Tecleo, mouse |
| `trafico` | — | Coches, claxon, obras |
| `musica` | — | Bocinas, radio |
| `tranquilo` | — | Nada destacable |

## Contrato con la app

Esto es lo que `apps/mobile` espera. Si algo cambia, se actualiza aquí y en la app al mismo tiempo.

- **Entrada: rasgos, no audio.** Una matriz float32 `[10, 16]`: 10 ventanas de 1 s × 16 bandas en escala mel, en dB relativos, de 125 Hz a 7.5 kHz, calculadas sobre PCM mono a 16 kHz. A esta resolución no se puede reconstruir lo que alguien dijo. La app calcula esos rasgos con el mismo código que la heurística actual; antes de entrenar hay que fijar la función exacta (ventana, FFT, filtros) y compartirla entre `ml/` y la app con una prueba de paridad.
- **Modelo:** pequeño, como un MLP o una CNN 1D de unas decenas de miles de parámetros, para que corra en JavaScript sin módulos nativos y siga funcionando en Expo Go.
- **Exportación:** pesos en `audio_model.json` (capas, formas y valores) + `labels.json` (ids en el orden de las salidas). Se copian a `apps/mobile/src/lib/`. Si el modelo crece, la alternativa es ONNX con `onnxruntime-react-native`, que ya exige una build nativa.
- **Salida:** probabilidad por clase, ya con sigmoid. La app usa un umbral por clase, elegido en validación para que haya pocos falsos positivos: preguntar de más cansa.
- **Latencia objetivo:** < 50 ms en el teléfono.

## Receta sugerida

1. **Datos:**
   - Subconjuntos de FSD50K y ESC-50 mapeados a nuestras clases.
   - **Grabaciones propias** en oficinas, cafés y salones reales, que son las más valiosas. Grábenlas solo con el consentimiento de quienes salgan.
   - Revisar licencias: ESC-50 y parte de FSD50K son no comerciales.
2. **Rasgos:** calcular la misma matriz `[10, 16]` que calculará la app. Con aumentos de nivel (±12 dB) se simula que el micrófono no está calibrado.
3. **Modelo:**
   - Empezar con un MLP sobre los rasgos aplanados.
   - Si hace falta más precisión, usar una CNN 1D en el tiempo.
   - Comparar contra la heurística actual como línea base.
4. **Validación:**
   - Separar por lugar o sesión de grabación, no al azar. Si no, el modelo memoriza la sala y la métrica miente.
   - Reportar macro-F1 por clase y falsos positivos por grabación.
5. **RTX 5070 (Blackwell):** usar PyTorch con CUDA ≥ 12.8 (`pip install torch --index-url https://download.pytorch.org/whl/cu128` o una versión más nueva). Las builds con CUDA más viejo no reconocen la GPU.

## Para el pitch

- macro-F1 por clase en validación, comparado con la heurística
- matriz de confusión
- latencia en el teléfono
- la frase clave: **"el audio nunca sale de tu teléfono"**
