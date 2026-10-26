# ml — Modelo de audio propio

Clasifica sonidos de oficina en ~10 s de audio para que la app pueda decir *"se perciben voces de fondo"* sin depender de una API externa. Se entrena aquí (GPU RTX 5070) y se sirve en CPU dentro de la API en Rust con ONNX Runtime.

## Clases v1

Multi-etiqueta (sigmoid): en una oficina suenan varias cosas a la vez.

| id | Etiqueta | Ejemplos |
|---|---|---|
| `voces` | Voces / conversación cercana | Compañeros hablando, llamadas ajenas |
| `teclado` | Teclado y clics | Tecleo, mouse |
| `zumbido` | Zumbido constante | Clima, ventilación, ventiladores de PC |
| `trafico` | Tráfico / calle | Coches, claxon, obras |
| `musica` | Música | Bocinas, radio |
| `telefono` | Teléfonos y notificaciones | Timbres, alertas |
| `movimiento` | Pasos y puertas | Gente pasando, puertas |
| `maquinas` | Máquinas | Impresora, cafetera |
| `tranquilo` | Ambiente tranquilo | Nada destacable |

## Contrato con la API

Esto es lo que `apps/api` espera. Si algo cambia, se actualiza aquí y en la API al mismo tiempo.

- **Archivos:** `audio_classifier.onnx` + `labels.json` (ids en el orden de las salidas). Se copian a `apps/api/models/`.
- **Entrada:** `waveform`, float32 `[1, N]`, mono, 16 kHz, valores en [-1, 1]. `N` variable (la app manda 10 s = 160 000 muestras).
- **Salida:** `scores`, float32 `[T, C]`: probabilidad (ya con sigmoid) por ventana de ~1 s y por clase. Va por ventana para que la API distinga si un sonido es constante o intermitente.
- **Frontend dentro del grafo:** de preferencia, el cálculo de log-mel va dentro del ONNX (export con opset ≥ 17), así no hay diferencias entre entrenamiento y servidor. Si no se puede, documentar los parámetros exactos (sample rate, n_fft, hop, n_mels, fmin, fmax, offset del log) y se replican en Rust con una prueba de paridad.
- **Tamaño:** < 50 MB, para versionarlo en git sin LFS.
- **Latencia objetivo:** < 100 ms por 10 s de audio en CPU.

## Receta sugerida

1. **Backbone** preentrenado en AudioSet: YAMNet (port a PyTorch) o EfficientAT (MobileNet, PyTorch nativo). Primero congelado entrenando solo una cabeza nueva; si da tiempo, afinar las últimas capas.
2. **Datos:** subconjuntos de FSD50K y ESC-50 mapeados a nuestras clases + **grabaciones propias** en oficinas, cafés y salones reales (las más valiosas). Revisar licencias: ESC-50 y parte de FSD50K son no comerciales.
3. **Validación:** separar por lugar o sesión de grabación, no al azar; si no, el modelo memoriza la sala y la métrica miente. Reportar macro-F1 por clase.
4. **RTX 5070 (Blackwell):** usar PyTorch con CUDA ≥ 12.8 (`pip install torch --index-url https://download.pytorch.org/whl/cu128` o una versión más nueva). Las builds con CUDA más viejo no reconocen la GPU.
5. **Exportar** con `torch.onnx.export(..., opset_version=17, dynamic_axes=...)` y verificar con `onnxruntime` en CPU que las salidas coinciden con PyTorch.

## Para el pitch

- macro-F1 por clase en validación
- matriz de confusión
- latencia en CPU
