# Escritorio isométrico: evaluación técnica

Fecha: 2026-10-26. **No se instaló nada ni se cambió código de la app.** Las versiones se verificaron en fuentes primarias (enlaces al final). Para comprobar la proyección, el sombreado, las rotaciones, el empaquetado del atlas y el orden de dibujo, hice un prototipo desechable en Python, guardado en [`prototipo/`](prototipo/) (`python prototipo/iso_proto.py`). Sus medidas reales están en §5.4.

Objetivo: una sala por cada espacio guardado (`spaces`), en isométrico 2.5D y pixel art original (del género Habbo, sin copiar su arte). En ella la persona coloca, mueve y gira los objetos que ganó (15–40 tipos con pocas variantes). Lleva pocas animaciones tranquilas y el cielo en la ventana, y el layout se guarda en la API de Rust como JSON.

---

## 0. Resumen

**Recomendación: (b) `@shopify/react-native-skia` en la versión exacta 2.14.0.** Va con un núcleo de lógica en TypeScript puro (matemática iso, colisiones, orden de dibujo, *hit test*, layout) y una capa de vistas RN transparentes encima del lienzo para VoiceOver y los controles sin arrastre. Los sprites salen de un pipeline Python de vóxeles a isométrico, a 1× y con la paleta de marca, en **un solo atlas PNG más un manifiesto JSON**.

Por qué Skia y no Views:

1. **Pixeles nítidos en cualquier pantalla con un solo atlas a 1×.** Se dibuja con `FilterMode.Nearest` (hay que pedirlo: el muestreo por defecto es lineal) y a una escala entera calculada en el momento. Con Views y expo-image, que no tiene opción de vecino más cercano, habría que preescalar cada sprite por densidad, en cientos de archivos.
2. **Arrastrar y reordenar ocurre en el hilo de UI.** `Atlas` con `useRSXformBuffer` y `useRectBuffer` recibe *shared values* de Reanimated y no hace *re-render* de React mientras se arrastra.
3. **Pruebas de imagen con el mismo árbol de componentes.** Skia corre *headless* en Node (CanvasKit), así que se pueden comparar PNG pixel a pixel sin teléfono.
4. **Está en Expo Go SDK 58, en la versión 2.14.0.** Skia v3 (Graphite) **no** corre en Expo Go, y ese es el riesgo principal (§1).

Descartadas: (c) three.js con R3F y expo-gl, porque el `expo-gl` 58.0.3 de Expo Go hace que three.js r163+ lance *"WebGL 1 is not supported"* (expo/expo#51543, abierto). (d) WebView con Pixi o Phaser, por accesibilidad, gestos y doble motor de JS. **Plan B: (a) Views con expo-image.** Comparte el núcleo TS y sirve si el *spike* de Skia falla o para la versión web.

Decisiones concretas que propongo:

| Tema | Propuesta |
|---|---|
| Rejilla | Baldosa 2:1 de **32 × 16 px de arte**, 8 vóxeles por lado de baldosa |
| Sala | **5 × 5 baldosas** al inicio, con 2 paredes de fondo de 48 px. El lienzo mide 164 × 132 px de arte |
| Escala | Entera, en pixeles de dispositivo: `k = floor(anchoDisponible_pt · PixelRatio / 164)`. Da **2 pt por pixel de arte** en todos los iPhone actuales, y la baldosa en pantalla mide 64 × 32 pt |
| Orden de dibujo | Por capas: piso y alfombras, paredes y objetos de pared, objetos de piso en **orden topológico** (método de Shaun Lebron), y los objetos de superficie justo después de su anfitrión |
| Datos | `rooms` 1:1 con `spaces`: `layout JSONB` + `schema_version` + `revision` para concurrencia optimista. El servidor valida con los mismos tipos y reglas |
| Accesibilidad | Tocar para elegir, luego tocar la celda destino o usar los botones "mover y girar" (WCAG 2.5.7), y acciones personalizadas de VoiceOver por objeto |

Esfuerzo aproximado con Skia: **unos 12–18 días-persona** en total. Por fase: *spike* de 0.5–1, sala MVP de 4–6, edición de 4–6 y pulido de 3–5 (§12). Con poco más de una semana, conviene cerrar el *spike*, la sala MVP y una edición mínima (tocar, botones y girar), y dejar el arrastre fino y las 40 variantes para después.

---

## 1. Restricción Expo Go (SDK 58): qué hay de verdad

Fuente principal: `apps/expo-go/package.json` en la rama `sdk-58` de expo/expo. `node_modules/expo/bundledNativeModules.json` dice **qué versión instala `npx expo install`, pero no qué trae Expo Go**: incluye `expo-dev-client`, `sentry-expo`, `react-native-bootsplash` y `@shopify/flash-list`, que no están en el `package.json` de Expo Go. Vale la lista de Expo Go.

| Módulo | En Expo Go SDK 58 | Versión | Notas |
|---|---|---|---|
| `@shopify/react-native-skia` | **Sí** | **2.14.0** (exacta, sin `~`) | No está instalado en `apps/mobile` todavía. `npx expo install @shopify/react-native-skia` elige 2.14.0 |
| `expo-gl` | Sí | 58.0.3 | Trae el cambio de herencia de `WebGL2RenderingContext` (ver §3c) |
| `react-native-webview` | Sí | 14.0.1 | Los DOM components (`'use dom'`) usan `@expo/dom-webview` ~58.0.2, que es dependencia de `expo` |
| `react-native-gesture-handler` | Sí | ~3.3.0 | API nueva de hooks: `usePanGesture`, `useTapGesture`, `useExclusiveGestures`… La de `Gesture.Pan()` sigue exportada |
| `react-native-reanimated` / `react-native-worklets` | Sí | 4.7.1 / 0.13.0 | `scheduleOnRN` para volver al hilo de JS |
| `expo-image` | Sí | ~58.0.17 | **Sin opción de muestreo por vecino más cercano** (docs SDK 58) |
| `react-native-svg`, `react-native-view-shot`, `lottie-react-native` | Sí | 15.16.0, 6.1.1, ^7.5.0 | `view-shot` sirve para capturas en el teléfono |
| three.js, `@react-three/fiber`, pixi.js, phaser | — | — | Son JS puro y no los limita Expo Go, pero dependen de `expo-gl` o de la WebView |

**El riesgo de versión de Skia es real y fácil de pisar:**

- Skia publicó v3.0.0 el 2 de octubre de 2026: *"This is React Native Skia Graphite. minSDK is now version 26 on Android and it is running Vulkan instead of OpenGL"*. Ya va en v3.8.0 (24 de octubre). La rama 2.x sigue recibiendo parches (2.15.2).
- La documentación oficial (ahora en `wcandillon.github.io/react-native-skia`) muestra v3 por defecto y dice que v3 *"does not run in Expo Go, which bundles the native code of v2"*. La documentación de v2 está en `/react-native-skia/v2/`, y las citas de este documento salen de la etiqueta `v2.14.0` del repo.
- Si el JS de Skia no coincide con el nativo de Expo Go, la app se cae al abrir. Hay que fijar `"@shopify/react-native-skia": "2.14.0"` sin `^`, revisar con `npx expo install --check` antes de cada QR, y no copiar ejemplos de v3 (por ejemplo, las APIs de WebGPU o Graphite).

---

## 2. Cómo funciona hoy

- `docs/brand/draw_scene.py` dibuja la escena frontal de 64 × 28 px en capas del tamaño del lienzo completo. Cada capa se preescala ×16 con `Image.NEAREST`, así que hay 29 PNG de 1024 × 448 (116 KB en disco), y el script genera `layers.ts`.
- `desk-scene.tsx` apila capas con `expo-image` (`contentFit="fill"`, `StyleSheet.absoluteFill`) y anima cambiando la opacidad entre cuadros. Respeta los tres niveles de movimiento (`useMotionLevel`), se mueve como mucho 5 s, mueve un solo elemento a la vez y se detiene al salir de la pantalla.
- **Esto no sirve para objetos que se mueven.** Una capa de lienzo completo por objeto y posición es combinatoria. Además, con `contentFit="fill"` expo-image nunca reduce la imagen al decodificar (lo dicen sus docs), así que cada capa ocupa unos 1.8 MB decodificada y unas 25 capas montadas suman unos 45 MB. Para la sala hacen falta sprites recortados con un ancla y posición propia.
- Lo que sí se reutiliza: la paleta (`PALETTE` de `draw_icon.py` y `draw_scene.py`, con rampas que ya cambian de tono), el detector de pixeles huérfanos (`orphans()`), los cielos por hora (`SKIES`), el patrón "el script genera el `.ts`" y las reglas de movimiento de DESIGN.md §5.

---

## 3. Comparación

| Criterio | (a) Views + expo-image | **(b) Skia 2.14** | (c) R3F + expo-gl | (d) WebView + Pixi/Phaser |
|---|---|---|---|---|
| Expo Go SDK 58 | Sí (ya se usa) | **Sí, solo 2.14.0** | `expo-gl` sí, pero three r163+ falla (#51543) | Sí (`react-native-webview` 14.0.1 o DOM components) |
| Pixeles nítidos | Solo con PNG preescalados a la escala exacta por densidad y posiciones en la rejilla. En Android con densidades fraccionarias se ve borroso | **Atlas 1× + `FilterMode.Nearest` + escala entera calculada → nítido en cualquier equipo** | `NearestFilter` y render a baja resolución, pero la luz 3D no coincide con la paleta hecha a mano y titila al moverse | `scaleMode: 'nearest'` funciona |
| Orden en la rejilla iso | `zIndex` entre hermanos; *re-render* de React al cambiar | Orden del arreglo del `Atlas`; se puede reordenar en un *worklet* | Z-buffer automático (gratis) | `zIndex` / `sortableChildren` |
| Tocar y arrastrar (RNGH + Reanimated) | Nativo por vista | Un `GestureDetector` para la sala, *hit test* en *worklet* y fantasma con *shared values* (receta *element tracking* de Skia) | Eventos de R3F en el hilo de JS, menos maduros en nativo | Sin RNGH: eventos de puntero dentro de la web y puente asíncrono |
| Girar | Otro archivo | Otro rectángulo del atlas | Girar la malla (giro real) | Otra textura |
| iPhone 11 / SE 2 (A13) | ~50 vistas de imagen: bien | Una llamada de dibujo; modo retenido con costo "casi cero" | Contexto GL y *parse* de three: funciona, con riesgo | Proceso WKWebView aparte, arranque lento y más memoria |
| Batería | Estático; se cambian cuadros | Redibuja solo cuando cambia un *shared value* | Bucle de render salvo `frameloop="demand"` | El *ticker* de Pixi corre siempre si no se detiene |
| Reducir movimiento | `useMotionLevel` actual | Igual, y además `ReduceMotion.System` de Reanimated | Hay que cablearlo | Hay que pasarlo por mensaje |
| VoiceOver | **Cada sprite es una vista con etiqueta y acciones** | Vistas transparentes encima del lienzo (receta oficial) | Vistas encima | Accesibilidad web dentro de la WebView: árbol mixto, la peor |
| Alternativa sin arrastre | Botones RN | Botones RN | Botones RN | Dentro de la web o en una capa RN |
| Web (`react-native-web`) | Trivial | CanvasKit de 2.9 MB gzip y cambio de *entry* | `expo-gl` web | Corre en web |
| Tamaño | 0 | +6 MB iOS / +4 MB Android en builds propias (0 en Expo Go) | three ~420 KB gzip (código sin minificar) + R3F | pixi ~237 KB gzip / phaser ~352 KB gzip dentro del HTML |
| Actualizaciones OTA (`expo-updates`) | Cientos de PNG por densidad | **1 atlas + 1 JSON** | Modelos y texturas | HTML y *bundle* |
| Pruebas de imagen | Sin render *headless*: solo paridad en Python o capturas en el teléfono | **Skia *headless* en Node con el mismo árbol** | Difícil | Difícil |
| Esfuerzo | M | M (+ *spike*) | XL | L |
| Veredicto | **Plan B** (y web) | **Recomendada** | Descartada | Descartada |

### (a) Views + expo-image con posición absoluta

- **Nitidez.** expo-image no tiene opción de muestreo (docs SDK 58: solo `contentFit`, `allowDownscaling`, `decodeFormat`…). Para que salga nítido, el bitmap tiene que mostrarse 1:1 en pixeles de dispositivo. Eso se logra con los sufijos `@2x` y `@3x`, que el *bundler* elige por densidad (docs de RN Images): `sprite@2x.png` preescalado ×4 y `sprite@3x.png` ×6 dan 2 pt por pixel de arte, exactos en iOS. RN redondea posición y tamaño a la rejilla de pixeles relativa a la raíz (docs de PixelRatio), así que las posiciones deben ser múltiplos de `k / PixelRatio`. En Android con densidad 2.625 o 2.75 elige `@3x` y reescala con filtro lineal, y se ve algo borroso.
- **Sin atlas.** expo-image no recorta un rectángulo de la fuente. Se puede simular con una vista recortada y la imagen desplazada, pero un atlas ×6 sería enorme (más de 6000 px de lado). En la práctica queda **un PNG por cuadro y por densidad**: 240 cuadros × 2 densidades son unos 480 archivos, que se suman a cada OTA.
- **Profundidad:** `zIndex` entre hermanos, recalculado en JS cuando un objeto cambia de celda. Con 40 objetos es barato.
- **Gestos:** lo más natural (un `GestureDetector` por objeto). Pero las cajas rectangulares se pisan en sus esquinas transparentes, así que de todos modos hace falta un *hit test* con máscara alfa (§6.6).
- **Accesibilidad:** la mejor. Cada objeto es una vista con `accessibilityLabel` y `accessibilityActions`.
- **Conclusión:** viable y sin dependencias nuevas, pero la nitidez depende de muchos archivos preescalados y no hay forma de probar las imágenes sin teléfono. Sirve como plan B y para web.

### (b) Skia 2.14.0 (recomendada)

- **Muestreo.** `<Image>` y `<Atlas>` aceptan `sampling` en v2.14.0 (`packages/skia/src/dom/types/Drawings.ts`): `sampling={{ filter: FilterMode.Nearest, mipmap: MipmapMode.None }}`. **El valor por defecto es lineal**: la documentación decía "nearest" hasta que se corrigió en 2.12 (#4051).
- **`Atlas`:** recibe la imagen, los `sprites` (rectángulos del atlas), los `transforms` (RSXform) y opcionalmente `colors` + `colorBlendMode` para teñir el fantasma. La documentación dice que sus transformaciones se animan *"with near-zero cost using worklets"* con `useRSXformBuffer` y `useRectBuffer`. Un usuario reporta buen rendimiento con unos 3,000 sprites (#4117); la sala tendrá menos de 100. Existe un reporte de 2024, en Android, de que `Atlas` rindió peor que `Picture` con 1,000 círculos animados en cada cuadro (#2688). No es nuestro caso, porque la escena casi siempre está quieta.
- **Modo retenido:** el árbol de React se convierte en una lista de dibujo y solo se redibuja cuando cambia un *shared value* o una prop. Encaja con "quieto la mayor parte del tiempo".
- **Escala entera:** un `Group` con `transform={[{ scale: k / PixelRatio.get() }]}` hace que cada pixel de arte mida exactamente `k` pixeles de dispositivo. Durante el arrastre hay que redondear la traslación a múltiplos de un pixel de arte en el *worklet*.
- **Gestos:** la documentación recomienda RNGH y muestra cómo seguir elementos con una `Animated.View` invisible encima de cada uno. Propongo un solo `GestureDetector` para la sala que convierte el toque a celda en un *worklet*, más vistas de accesibilidad encima.
- **Accesibilidad:** el `Canvas` acepta las props de accesibilidad de `View`. Para los elementos internos, la documentación dice: *"overlaying views on top of your canvas"*.
- **Web:** necesita CanvasKit (2.9 MB gzip) y `WithSkiaWeb` o `LoadSkiaWeb`, y con Expo Router el componente debe quedar **fuera** de `app/`. Opciones: cargar Skia solo en la pantalla de la sala, o mostrar la versión (a) en web.
- **Android:** si el lienzo no es opaco se usa `TextureView` (con una copia extra) y se compone bien. Basta para esta escena.

### (c) three.js con `@react-three/fiber/native` + `expo-gl` (descartada)

- **Bloqueo actual.** Desde expo-gl 56.0.5, `WebGL2RenderingContext` hereda de `WebGLRenderingContext` (CHANGELOG). Three.js r163+ (r186 es la actual) lanza `THREE.WebGLRenderer: WebGL 1 is not supported since r163.` si `context instanceof WebGLRenderingContext` (`src/renderers/WebGLRenderer.js`, línea 101). El reporte expo/expo#51543 sigue abierto y Expo Go SDK 58 trae expo-gl 58.0.3, que tiene ese cambio. Hay dos salidas: three ≤ r162 o un parche global, y ninguna está probada.
- **Otro problema abierto:** expo/expo#51948. Las builds *release* de Android con R8, que SDK 58 activa por defecto, se caen al crear `GLView`. Se arregla con una regla de *proguard*, pero solo afecta builds propias.
- R3F 9.8.2 acepta `react >=19 <19.4` y `expo-gl >=11`, así que es compatible en papel. Pero el soporte nativo tiene historial de problemas: #3517 *"React Native is no longer supported"*, cargadores de texturas que fallan con blobs (#3558).
- **Estilo:** el render 3D con luz no reproduce las rampas de color hechas a mano ni el contorno selectivo, y para parecer pixel art necesita render a baja resolución y *shaders* de contorno. Un pipeline de vóxeles a sprites da el mismo volumen con control total de cada pixel.
- **Costo:** three pesa unos 2.1 MB de código sin minificar (`three.core.js` + `three.module.js`, unos 417 KB gzip), además de R3F y un pipeline de modelos (.vox → glTF). Esfuerzo XL.

### (d) WebView con PixiJS o Phaser (descartada)

- Es técnicamente posible. Pixi v8 da pixel art nítido con `TextureStyle.defaultOptions.scaleMode = 'nearest'` (lo explica un *maintainer* en la discusión #11018), y los DOM components de Expo *"Supports Expo Go"*.
- En contra: las props cruzan un puente asíncrono y serializable, las funciones son "acciones nativas" asíncronas, la web *"is slower to parse and start up than optimized Hermes bytecode"*, y Expo recomienda usar vistas nativas siempre que se pueda. Los gestos no pasan por RNGH ni por Reanimated, VoiceOver ve un árbol web mezclado con el nativo, y textos, sonido, vibración y nivel de movimiento quedarían duplicados entre dos motores.
- Para una app accesible primero no compensa. Si algún día hiciera falta un editor solo para web, (a) o Skia web lo cubren.

---

## 4. Arquitectura recomendada

```
docs/brand/draw_room.py            → genera atlas + manifiesto + tipos TS + catálogo para la API
apps/mobile/assets/room/atlas.png  (1×)
apps/mobile/src/components/room/
  manifest.ts      (generado: marcos, anclas, huellas, máscaras, tipos)
  iso.ts           (celda ↔ arte ↔ pantalla, escala entera)
  occupancy.ts     (colisiones de piso, pared y superficie)
  depth.ts         (capas + orden topológico → DrawList)
  hit.ts           (objeto bajo el dedo, con máscara alfa)
  layout.ts        (tipos del JSON v1, validar, migrar, autocolocar)
  room-canvas.tsx  (Skia: DrawList → Atlas; cielo; animaciones)
  room-a11y.tsx    (vistas transparentes: etiqueta, acciones, objetivos táctiles)
  room-editor.tsx  (inventario, barra de selección, botones mover y girar, guardar)
apps/api/catalog/room.json         (generado: tipos, huellas, lugares, variantes)
apps/api/src/routes/rooms.rs       (GET/PUT + validación con las mismas reglas)
```

- **Una sola fuente de verdad: `DrawList`.** El núcleo TS convierte `(layout, manifest)` en `DrawList = [{ frame, ax, ay, tint? }]` en pixeles de arte, ya ordenada. Skia la dibuja, la capa de accesibilidad la usa para colocar sus vistas, las pruebas *headless* la renderizan, y la versión (a) podría consumirla igual. Así el renderer queda delgado y se puede cambiar.
- **Hilos.** El layout vive en JS (React Query, como `useDesk`). Al empezar a arrastrar, la ocupación y la posición se copian a *shared values*. El *worklet* calcula la celda, la validez y el orden durante el gesto, y al soltar `scheduleOnRN(commit)`. La app tiene `reactCompiler: true`, así que hay que usar `sv.get()` y `sv.set()` en vez de `.value` (docs de `useSharedValue`).
- **RNGH 3.** Esquema (los nombres se confirman en el *spike*):

```tsx
const pan = usePanGesture({
  enabled: editing && !screenReader,          // con VoiceOver se usan las acciones (§9)
  activateAfterLongPress: 150,                // no compite con el scroll ni con tocar
  onActivate: (e) => { 'worklet'; drag.set(beginDrag(e.x, e.y, scene.get())); },
  onUpdate:   (e) => { 'worklet'; drag.set(updateDrag(drag.get(), e.x, e.y, scene.get())); },
  onDeactivate: () => { 'worklet'; scheduleOnRN(commitDrag, drag.get()); },
});
const tap = useTapGesture({ onDeactivate: (e) => { 'worklet'; scheduleOnRN(selectAt, e.x, e.y); } });
<GestureDetector gesture={useExclusiveGestures(pan, tap)}>
  <Canvas style={{ width, height }}>{/* <Atlas …/> */}</Canvas>
</GestureDetector>
```

  En la v3, `onStart` pasa a `onActivate`, `onEnd` pasa a `onDeactivate`, y `onChange` se integra en `onUpdate`. La configuración acepta `runOnJS`, `enabled` y `hitSlop`.
- **La sala de cada espacio se crea cuando hace falta.** Si `GET /v1/spaces/{id}/room` devuelve 404, el cliente arma una sala por defecto de forma determinista (semilla = id del espacio), con el escritorio, la silla y la planta de base más los objetos ganados en celdas libres. El primer `PUT` la guarda.
- **Objeto nuevo.** Cuando termina una prueba en el espacio S, su objeto aparece en una celda libre de la sala de S con la misma entrada de hoy (cae 2 px a saltos, o un fundido, según el nivel). En las otras salas queda disponible en el inventario. Lo ganado es de la persona, no de una sala: cada tipo se puede poner en todas sus salas.
- **Reglas de producto (DESIGN.md §6 y §11) que el editor debe respetar:**
  - El inventario muestra solo lo que la persona tiene: sin siluetas bloqueadas ni "3 de 40".
  - Las variantes se eligen libremente, porque desbloquearlas por resultados premiaría una respuesta.
  - La sala se puede ocultar.
  - Nada se pierde: un tipo que salga del catálogo se conserva en el JSON.

---

## 5. Pipeline de assets (Python + Pillow)

### 5.1 Vóxeles → isométrico 2:1 en pixeles

Cada objeto se modela en código, como ya se hace en `draw_scene.py`: uniones de cajas, `box(x, y, z, w, d, h, material)`, en una rejilla de vóxeles. Opcionalmente se puede importar un `.vox` de MagicaVoxel, cuyo formato RIFF está documentado en `ephtracy/voxel-model`. Luego se proyecta:

```python
# esquina (x, y, z) del vóxel -> pixel de arte; 8 vóxeles = 1 baldosa de 32 x 16 px
def project(x, y, z):
    return 2 * (x - y), (x + y) - 2 * z

STAMP = [".TT.",   # cada vóxel es un hexágono de 4 x 4 px
         "LTTR",   # T = cara de arriba, L = izquierda, R = derecha
         "LLRR",
         ".LR."]

# Orden de pintor exacto: la dirección de vista de esta proyección es (1, 1, 1)
# (proj(1,1,1) = (0, 0)), así que basta ordenar por x + y + z.
for (x, y, z), mat in sorted(voxels.items(), key=lambda kv: sum(kv[0])):
    ...
```

- **Sombreado por cara con las rampas de la paleta:** la cara de arriba usa el tono claro, la izquierda el medio y la derecha la sombra, por ejemplo `oak_hi / oak / oak_shadow`, con `oak_deep` como contorno. La luz queda fija respecto a la cámara, como es habitual en el isométrico pixel art, y cada rotación sale con la misma iluminación.
- **Contorno selectivo:** un pixel alrededor de la silueta, con el tono más oscuro del material vecino y nunca negro puro.
- **Rotaciones gratis:** se gira la rejilla 90° (`(x, y) → (d-1-y, x)`) y se vuelve a proyectar. Cada tipo declara qué orientaciones permite (`facings`). Muchas piezas solo necesitan 2: un estante girado hacia la pared muestra su espalda, como se vio en el prototipo.
- **Detalles a mano:** después de proyectar se pueden pintar "calcomanías" por orientación, como la onda del monitor, las hojas o las letras.
- **Lints que se reutilizan:** solo colores de la paleta, cero huérfanos salvo el tramado intencional (`orphans()` de `draw_icon.py`), anclas dentro del sprite y un pixel de separación en el atlas.
- **Cuadros repetidos:** las piezas simétricas, como la alfombra, salen iguales en las 4 rotaciones. Se detectan por *hash* y se guardan una sola vez.

### 5.2 Atlas + manifiesto

Se empaqueta por estantes a 1× (un *packer* MaxRects si crece), con 1 px de separación para que el muestreo nearest nunca tome pixeles del vecino. El script genera:

- `apps/mobile/assets/room/atlas.png` y `apps/mobile/src/components/room/manifest.ts` (tipado, como `layers.ts`);
- `apps/api/catalog/room.json` (tipos, huellas, lugares, variantes y superficies), para validar en el servidor;
- `docs/brand/room-preview.png` (hoja de contacto y salas de ejemplo), para revisar el arte.

```json
{
  "version": 1,
  "tile": [32, 16], "voxelsPerTile": 8,
  "atlas": { "file": "atlas.png", "size": [512, 512] },
  "types": {
    "desk":  { "place": ["floor"], "footprint": [2, 1], "facings": [0, 1],
               "surface": { "z": 14, "slots": [[0, 0], [1, 0]] }, "variants": ["oak", "sage"], "base": true },
    "lamp":  { "place": ["surface", "floor"], "footprint": [1, 1], "facings": [0, 1],
               "variants": ["warm"], "anim": { "glow": 2 } },
    "frame": { "place": ["wall"], "span": [1, 1], "variants": ["home"] }
  },
  "frames": {
    "desk.oak.r0": { "rect": [0, 0, 50, 40], "anchor": [17, 15], "mask": "<base64, 1 bit por pixel>" }
  },
  "adjustments": { "desk_lamp": "lamp", "ask_lighting": "lamp", "close_blinds": "blinds" }
}
```

- `anchor` es el pixel del sprite que cae en la esquina trasera de su huella, con `z = 0`.
- `mask` permite un *hit test* exacto sin leer pixeles en el teléfono, y también se puede probar en Node.
- `adjustments` mueve a un solo lugar el mapeo `ITEM_FOR_ADJUSTMENT`, que hoy vive solo en `desk.ts`. El servidor lo necesita para validar qué objetos tiene la persona.

### 5.3 Tamaños y escala entera

Escala entera para una sala de 5 × 5 (164 px de arte) con 16 pt de margen por lado:

| Equipo | pt | PixelRatio | k (px de dispositivo por px de arte) | pt por px de arte | Ancho de la sala |
|---|---|---|---|---|---|
| iPhone SE 2/3 | 375 | 2 | 4 | 2.0 | 328 pt |
| iPhone 11 / XR | 414 | 2 | 4 | 2.0 | 328 pt |
| iPhone 12/13 mini | 375 | 3 | 6 | 2.0 | 328 pt |
| iPhone 15/16 | 393 | 3 | 6 | 2.0 | 328 pt |
| iPhone 16 Pro Max | 440 | 3 | 7 | 2.33 | 383 pt |
| Android 411 dp @2.625 | 411 | 2.625 | 6 | 2.29 | 375 dp |

- Una sala de 6 × 6 (196 px) baja a 1.5 pt por pixel de arte en @2x (k = 3) y a 1.67 en @3x (k = 5). Por eso 5 × 5 es el tamaño inicial: con baldosas de 64 × 32 pt no hace falta zoom para editar. DESIGN.md prohíbe el zoom animado de pantalla completa (WCAG 2.3.3).
- Hoy la escena frontal mide unos 5.5 pt por pixel de arte, así que la sala se verá más fina. Es una decisión visual que se prueba en el *spike*. Si se quiere más grueso, la baldosa de 16 × 8 da unos 4 pt por pixel de arte, pero los objetos pequeños quedarían de 3–4 px.

### 5.4 Resultados del prototipo

Medidos con paleta real, contorno selectivo y 4 rotaciones:

| Sprite (r0) | Huella | Tamaño en px de arte |
|---|---|---|
| Escritorio | 2 × 1 | 50 × 40 |
| Silla | 1 × 1 | 28 × 35 |
| Planta | 1 × 1 | 18 × 30 |
| Estante alto | 1 × 1 | 26 × 50 |
| Lámpara (superficie) | — | 14 × 24 |
| Alfombra (plana) | 2 × 2 | 66 × 36 |

- Atlas de 24 cuadros (6 tipos × 4 rotaciones, con duplicados): **256 × 159 px y 4.8 KB en PNG.**
- Si se escala a unos 240 cuadros (40 tipos × 3 variantes × 2 orientaciones), el atlas queda cerca de 512 × 800 px, unos 50 KB, y ocupa unos 1.6 MB en la GPU.
- Lienzo de la sala: 5 × 5 mide 164 × 132 px, 6 × 6 mide 196 × 148 y 8 × 8 mide 260 × 180 (paredes de 48 px).
- En el render de una sala de 6 × 6 con estante, escritorio con lámpara encima, sillas, plantas, alfombra y ventana con cielo de día, el orden topológico salió correcto, y el estilo encaja con la marca (el verde azulado de la pared, el roble y la salvia).
- **El piso y las paredes se arman con baldosas** (sprites de 32 × 16 y segmentos de pared, uno con hueco de ventana), no como una sola imagen. Así cambiar el piso o la pared no multiplica los sprites. El cielo se dibuja **detrás** del segmento con hueco, usando las rampas de `SKIES` (amanecer, día, atardecer y noche, como hoy).

---

## 6. Matemática isométrica

Las coordenadas de celda son `(x, y)`, con el origen en la esquina trasera del piso. `x` crece hacia abajo a la derecha y `y` hacia abajo a la izquierda. La pared **izquierda** está en el plano `x = 0` y la **derecha** en `y = 0`. Los objetos con `x + y` mayor están más cerca de quien mira.

### 6.1 Conversión (Clint Bellanger, *Isometric Tiles Math*)

```ts
export const TILE_W = 32, TILE_H = 16, VOX = 8;   // px de arte

/** Esquina trasera de la celda (x, y) a altura z (px) → px de arte, relativo al origen del piso. */
export function cellToArt(x: number, y: number, z = 0) {
  return { ax: (x - y) * (TILE_W / 2), ay: (x + y) * (TILE_H / 2) - z };
}

/** px de arte → celda entera, o null si cae fuera del piso. */
export function artToCell(ax: number, ay: number, w: number, d: number) {
  const fx = (ax / (TILE_W / 2) + ay / (TILE_H / 2)) / 2;
  const fy = (ay / (TILE_H / 2) - ax / (TILE_W / 2)) / 2;
  const x = Math.floor(fx), y = Math.floor(fy);
  return x >= 0 && y >= 0 && x < w && y < d ? { x, y } : null;
}

/** Toque (pt, relativo al lienzo) → px de arte. k = px de dispositivo por px de arte. */
export const touchToArt = (px: number, py: number, k: number, pr: number, o: { ax: number; ay: number }) =>
  ({ ax: (px * pr) / k - o.ax, ay: (py * pr) / k - o.ay });

export const pickScale = (availablePt: number, artW: number, pr: number) =>
  Math.max(1, Math.floor((availablePt * pr) / artW));
```

Comprobación: el centro de la celda (1, 0) es `(16, 16)` en px de arte, y `artToCell(16, 16)` da `fx = 1.5` y `fy = 0.5`, o sea `(1, 0)`.

### 6.2 Huella, rotación y arrastre

- `footprint(type, rot) = rot % 2 ? [d, w] : [w, d]`. El pivote es la esquina trasera. Si al girar el objeto se sale o choca, se prueba a correrlo dentro de su propia huella; si tampoco cabe, se rechaza con un mensaje ("No cabe girado aquí").
- **Al arrastrar se guarda el desfase del agarre:** `offset = celdaBajoElDedoAlEmpezar − celdaDelObjeto`, y el destino es `celdaBajoElDedo − offset`. Así el objeto no salta al dedo.

### 6.3 Colisiones

- **Piso:** `Int16Array(w * d)` con el índice de cada objeto, o −1. Un objeto cabe si todas sus celdas son −1 o suyas. Las alfombras (`flat`) usan otra rejilla, así que debajo de una alfombra se puede poner un mueble.
- **Paredes:** una rejilla por pared de `largo × 3` filas de 16 px. Los objetos de pared ocupan `span = [a lo largo, filas]`, y la ventana reserva sus celdas.
- **Superficies:** el anfitrión declara `surface.z` y `slots`, que se transforman con su rotación. Un objeto de superficie ocupa un *slot* y no se apila sobre otro objeto de superficie. Al mover el anfitrión se mueven sus objetos. Al guardarlo en el inventario, sus objetos vuelven al inventario, o se pregunta.

### 6.4 Orden de dibujo

1. Celdas del piso, luego alfombras.
2. Segmentos de pared y el cielo detrás del hueco de la ventana; luego los objetos de pared. Un objeto de piso nunca queda detrás de la pared.
3. **Objetos de piso en orden topológico.** A va antes que B si sus cajas en pantalla se solapan y A está detrás en un eje sin estar delante en el otro (`A.x1 <= B.x0 && !(B.y1 <= A.y0)`, o lo mismo con los ejes cambiados). Las huellas nunca se solapan, así que no hay ciclos: si dos huellas están separadas en sentidos opuestos en los dos ejes, sus proyecciones quedan separadas en horizontal (la altura solo crece hacia arriba en la pantalla). Con n ≤ 60, el algoritmo de Kahn en O(n²) no cuesta nada. Para empatar se usa `x0 + y0`. Es el método de Shaun Lebron (*Isometric Blocks*) aplicado a cajas sobre el piso. Ordenar solo por `x + y` falla con objetos de más de una celda.
4. Los objetos de superficie van justo después de su anfitrión, y los efectos (vapor) justo después de su objeto.
5. Encima de todo, el contorno de selección y el fantasma.

### 6.5 Orden durante el arrastre

El *worklet* recalcula el orden (los mismos 60 objetos en O(n²)) cuando cambia la celda del fantasma, y el `Atlas` lee el orden desde un *shared value*. Si en el *spike* esto se complica, el respaldo es dibujar el fantasma encima de todo y reordenar al soltar.

### 6.6 *Hit test*

Se recorre la `DrawList` de adelante hacia atrás: primero la caja del sprite y luego la máscara alfa del manifiesto en `(ax − x0, ay − y0)`. Si no se toca nada pero hay un objeto a menos de 12 pt, se elige el más cercano, porque los objetos pequeños (una taza de unos 10 px de arte, 20 pt) no llegan a 44 pt. Tocar otra vez en el mismo lugar recorre los candidatos que se solapan.

---

## 7. Esquema JSON del layout (versionado)

```jsonc
{
  "v": 1,
  "size": { "w": 5, "d": 5 },
  "shell": { "floor": "oak", "wall": "teal", "window": { "wall": "right", "u": 2, "variant": "arch" } },
  "items": [
    { "uid": "k3f9q2ab", "type": "desk",  "variant": "oak",  "place": { "on": "floor", "x": 2, "y": 0, "rot": 0 } },
    { "uid": "p1aa7c0d", "type": "lamp",  "variant": "warm", "place": { "on": "surface", "host": "k3f9q2ab", "slot": 1 } },
    { "uid": "w7c2m9xe", "type": "frame", "variant": "home", "place": { "on": "wall", "wall": "left", "u": 1, "row": 1 } }
  ]
}
```

- Todo es entero; `rot ∈ {0,1,2,3}` y debe estar en `facings`. `uid` son 8 caracteres `[a-z0-9]` únicos en la sala, generados en el cliente con `expo-crypto`, que ya está instalado. Máximo 60 objetos y 16 KB.
- **Un esquema JSON** (draft 2020-12) en `docs/` sirve de contrato y de prueba. Los tipos TS y Rust se escriben a mano a partir de él, porque es pequeño.
- **Versiones:** `v` crece cuando cambia la forma, con funciones `migrate(v1 → v2)` en TS y en Rust. El servidor rechaza un `v` mayor que el que conoce con 422 y "actualiza la app". Si llega un `type` desconocido para el catálogo actual, se conserva y no se dibuja.

---

## 8. Postgres y API

Tres opciones:

| Opción | A favor | En contra |
|---|---|---|
| Columna `room JSONB` en `spaces` | Una línea de migración | `GET /v1/spaces` cargaría todos los layouts, y guardar la sala bloquea la fila del espacio |
| **Tabla `rooms` 1:1 con JSONB** | Guardado atómico de toda la sala, versión y revisión propias, la lista de espacios sigue ligera, `ON DELETE CASCADE` | Un *join* para la autorización |
| Tabla normalizada `room_items` (una fila por objeto) | Consultas SQL por objeto | Muchas escrituras por guardado, el esquema se versiona en SQL y el orden y las superficies quedan incómodos |

Postgres recomienda `jsonb` *"unless there are quite specialized needs"*, y que cada documento sea *"an atomic datum"* de tamaño manejable, porque cada actualización bloquea la fila entera. Una sala cumple las dos cosas. Si algún día hace falta analizar, por ejemplo "cuántas salas tienen lámpara", se usa `@>` con un índice GIN `jsonb_path_ops`. No hace falta para el MVP.

```sql
-- 0006_rooms.sql
CREATE TABLE rooms (
    space_id UUID PRIMARY KEY REFERENCES spaces (id) ON DELETE CASCADE,
    schema_version SMALLINT NOT NULL,
    layout JSONB NOT NULL CHECK (jsonb_typeof(layout) = 'object' AND octet_length(layout::text) <= 16384),
    revision INT NOT NULL DEFAULT 1,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

- `GET /v1/spaces/{id}/room` devuelve `{ revision, layout }`, o 404 si todavía no hay sala.
- `PUT /v1/spaces/{id}/room` recibe `{ revision, layout }` (revisión 0 al crearla) y devuelve 200 con `{ revision }`. Devuelve 409 si otra pantalla guardó antes, con la versión del servidor para combinar, y 422 con la lista de problemas si el layout no es válido.

```sql
INSERT INTO rooms (space_id, schema_version, layout)
SELECT s.id, $2, $3 FROM spaces s WHERE s.id = $1 AND s.user_id = $4
ON CONFLICT (space_id) DO UPDATE
   SET layout = EXCLUDED.layout, schema_version = EXCLUDED.schema_version,
       revision = rooms.revision + 1, updated_at = now()
 WHERE rooms.revision = $5
RETURNING revision;   -- sin fila: 404 (espacio ajeno) o 409 (revisión vieja)
```

- **Rust:** hay que agregar la *feature* `json` a `sqlx` en `Cargo.toml`, porque `sqlx::types::Json<T>` *"Available on crate feature `json` only"*. Las variantes de lugar se modelan como `#[serde(tag = "on")] enum Place { Floor{..}, Wall{..}, Surface{..} }` con `deny_unknown_fields`.
- **Qué valida `validate(layout, catalog, owned)`:**
  - límites;
  - colisiones de piso, pared y superficie;
  - `rot` dentro de `facings`;
  - que el anfitrión exista y tenga *slot* libre;
  - `uid` únicos;
  - que la persona tenga cada tipo (los de base más los de `adjustments` de lo que probó, la misma consulta que `progress`);
  - el número máximo de objetos.
- El servidor guarda el JSON **ya normalizado**, es decir, vuelto a serializar desde los tipos.
- **Cliente:** guarda al tocar "Listo", no en cada movimiento. Mientras tanto, el borrador vive en AsyncStorage, y si el guardado falla no se pierde nada.

---

## 9. Accesibilidad y movimiento

- **VoiceOver fuera de la edición:** igual que hoy, la sala es una imagen con un resumen ("Tu espacio Casa: escritorio con lámpara, planta junto a la ventana…"). En el orden de lectura, de atrás hacia adelante y de izquierda a derecha.
- **VoiceOver en la edición:** cada objeto es una vista transparente encima del lienzo, con `accessibilityLabel` ("Lámpara, sobre el escritorio") y `accessibilityActions` personalizadas: "Mover hacia la ventana", "Mover hacia la puerta", "Mover a la izquierda", "Mover a la derecha", "Girar" y "Guardar en el inventario". Se manejan con `onAccessibilityAction`, y cada cambio se anuncia con `AccessibilityInfo.announceForAccessibility`. Con el lector de pantalla activo, el *pan* se apaga (`enabled: false`).
- **WCAG 2.5.7 (arrastre):** *"All functionality that uses a dragging movement for operation can be achieved by a single pointer without dragging"*. Los ejemplos de W3C son justo nuestros patrones: elegir y luego tocar el destino, y flechas al lado del elemento elegido. Aquí hay dos caminos sin arrastrar:
  1. Tocar el objeto y luego tocar la celda destino. Las celdas válidas se marcan con un contorno discontinuo, no solo con color.
  2. Una barra con botones de texto e ícono para las cuatro direcciones iso, "Girar", "Guardar" y "Listo".

  El arrastre es un atajo más.
- **WCAG 2.5.8:** los objetivos táctiles miden al menos 24 × 24 px. Las vistas de la capa se amplían con `hitSlop` hasta 44 pt cuando no se pisan entre sí. La baldosa de 64 × 32 pt ayuda.
- **Cuando un movimiento no se puede hacer,** el motivo se dice en texto ("Ese lugar está ocupado"). El fantasma usa contorno y trama, no solo verde y rojo. La vibración, si está activa, nunca es la única señal (DESIGN.md §5).
- **Movimiento:**
  - Con "Reducido", nada se mueve. Al soltar o en un movimiento no válido el objeto cambia de lugar al instante o con un fundido. Las animaciones de Reanimated con `ReduceMotion.System` saltan al final.
  - Con "Tranquilo", hay fundidos de 250 ms o menos.
  - Con "Con detalles", la sala cobra vida 5 s al aparecer o al tocarla, con un elemento a la vez: la planta se mece (2 cuadros), sale vapor de la taza (2), gira el ventilador (2) y la onda del monitor se calma (3, el momento firma). Ningún elemento se desplaza más de 2 px de arte.
  - Nunca hay rebotes ni resortes, y lo que se arrastra sigue al dedo sin inercia.
- **Textos en es/en** en `locales`, incluidas las etiquetas de cada tipo y variante.

---

## 10. Rendimiento y batería

- **Skia:**
  - Hay una sola `Canvas` con un solo `Atlas` (o dos: el de la estructura y el de los objetos) y nada en cada cuadro mientras no cambie un *shared value*.
  - Las animaciones de reposo cambian el índice de cuadro desde un temporizador de unos 300 ms, como `TICK_MS` hoy, y no con `useFrameCallback`. Así se redibuja unas 3 veces por segundo durante 5 s y luego nada.
  - Se pausa al perder el foco (`useFocusEffect`) y al pasar a segundo plano (`AppState`).
- **Memoria:** el atlas ocupa unos 1–4 MB en la GPU, contra unos 45 MB que ocupan hoy las capas a ×16 decodificadas.
- **iPhone 11 y SE 2 (A13):** son menos de 100 sprites en una sola llamada de dibujo. El riesgo real está en el JS: hacer el orden y el *hit test* en *worklets* y no hacer *re-render* de React mientras se arrastra.
- **Medición:** registro de energía de Xcode Instruments con 10 minutos en la pantalla de la sala, más el *Perf Monitor* de RN mientras se arrastra, en un iPhone SE 2 u 11 real.

---

## 11. Pruebas

- **TS** (con `jest-expo` ~58.0.12 como devDependency; no afecta a Expo Go):
  - `iso.test.ts`: ida y vuelta celda → arte → celda en todos los centros de una sala de 8 × 8, bordes asignados siempre a la misma celda, y la tabla de `pickScale` (§5.3).
  - `occupancy.test.ts`: colisiones, giro en el borde, *slots* de superficie, paredes con ventana.
  - `depth.test.ts`: casos fijos y una prueba de propiedades con 1,000 salas aleatorias sin solapes. Para cada par cuyas cajas se pisan en pantalla, el de adelante debe ir después.
  - `hit.test.ts`: máscaras del manifiesto.
  - `layout.test.ts`: esquema y migraciones.
- **Rust:** `cargo test` de `validate()` con **los mismos casos JSON** (`apps/api/catalog/room-fixtures/*.json`, generados o copiados por el script, porque los espejos del equipo separan `apps/mobile` y `apps/api`). Los casos incluyen los errores esperados.
- **Python** (`pytest` sobre `draw_room.py`):
  - salida determinista (comparación contra PNG de referencia);
  - solo colores de la paleta;
  - cero huérfanos fuera del tramado;
  - anclas y márgenes correctos;
  - cada tipo tiene todas sus orientaciones y variantes.
- **Pruebas de imagen:** Skia *headless* en Node (`drawOffscreen` + `makeOffscreenSurface`) renderiza salas de ejemplo a k = 1 con nearest, y se comparan **pixel a pixel** contra PNG de referencia de 164 × 132, que pesan pocos KB. El mismo caso compuesto por Python debe salir idéntico, lo que prueba a la vez anclas, orden y renderer. Para el entorno de Jest, Skia trae `jestEnv.js` y `jestSetup.js` con CanvasKit.
- **En el teléfono:** una lista de revisión en Expo Go y TestFlight: nitidez (captura ampliada), arrastre fluido, recorridos con VoiceOver, Reducir movimiento y batería. Más adelante, Maestro para los flujos de edición (no está instalado).

---

## 12. Fases, esfuerzo y riesgos

Estimación en días-persona con asistencia de Claude. Lo que manda es iterar el arte y probar en el teléfono.

| Fase | Contenido | (b) Skia | (a) Views |
|---|---|---|---|
| 0. *Spike* | Skia 2.14 en Expo Go en un iPhone real y en Android: atlas del prototipo a k entero con nearest, arrastrar un sprite con `usePanGesture` y Reanimated, render *headless* en Node. Decidir si se sigue | 0.5–1 | 0.5 |
| 1. Sala MVP | `draw_room.py` (vóxeles, contorno, rotaciones, atlas, manifiesto y salidas TS y API, más pruebas), unos 15 tipos con 1–2 variantes, núcleo TS con pruebas, sala de solo lectura con cielo por hora y animaciones por nivel, autocolocación de lo ganado, migración y GET/PUT con validación | 4–6 | 4–5.5 (+ copias por densidad) |
| 2. Decorar y editar | Pantalla de edición, inventario, elegir, tocar destino, botones mover y girar y guardar, acciones de VoiceOver y anuncios, arrastre en *worklet*, superficies y pared, 409 y borrador local, textos es/en | 4–6 | 4.5–6.5 (+ máscaras para tocar) |
| 3. Pulido | Hasta 40 tipos y variantes, sonidos y vibración con los interruptores actuales, pruebas de imagen, rendimiento y batería en el teléfono, nitidez en Android, decisión sobre web, actualizar PLAN.md y DESIGN.md §11 | 3–5 | 4–6 (+ capturas en el teléfono) |
| **Total** | | **≈ 12–18** | **≈ 13–18.5** |

(c) se estima en 25–40 días, con bloqueos de plataforma sin resolver. (d) en 18–25, con una deuda de accesibilidad.

**Riesgos principales y cómo atenuarlos:**

1. **Versión de Skia.** v3 no corre en Expo Go y la documentación por defecto es de v3. Fijar 2.14.0, usar la documentación v2 y correr `expo install --check` antes de cada demo.
2. **Nitidez.** El muestreo por defecto es lineal, una escala no entera o una traslación de medio pixel la arruinan. Una sola función `pickScale`, `sampling` constante y redondeo en el *worklet*. La prueba *headless* lo detecta.
3. **Capa de accesibilidad desalineada con el lienzo.** Las dos se derivan de la misma `DrawList`, con una prueba de que las cajas coinciden.
4. **Volumen de arte.** 40 tipos × variantes × orientaciones. Generación por procedimiento, 2 orientaciones por defecto y cuadros repetidos guardados una sola vez.
5. **Casos raros de orden** (varias celdas, superficies, la esquina entre paredes). Orden topológico más la prueba de propiedades.
6. **Tiempo** (poco más de una semana). La edición accesible con tocar y botones es más simple que el arrastre y además es obligatoria (WCAG 2.5.7), así que va primero; el arrastre después.
7. **Producto.** Que la sala no se vuelva gamificación: nada de siluetas bloqueadas, contadores "N de 40", rachas ni objetos que dependan de "ayudó" (DESIGN.md §6 y §11).
8. **Web.** Skia web pesa 2.9 MB más cambios de *entry*. Decidir si la sala se oculta en web o usa (a).
9. **Validación duplicada** en TS y Rust. Un solo catálogo generado y los mismos casos JSON en las dos pruebas.

---

## 13. Fuentes

**Expo y versiones**
- Expo Go SDK 58, dependencias nativas: https://github.com/expo/expo/blob/sdk-58/apps/expo-go/package.json
- `bundledNativeModules.json` (local): `apps/mobile/node_modules/expo/bundledNativeModules.json`
- Expo Skia (SDK 58, "Included in Expo Go"): https://docs.expo.dev/versions/latest/sdk/skia/
- Expo GLView (SDK 58): https://docs.expo.dev/versions/latest/sdk/gl-view/
- Expo Image (SDK 58, sin opción de muestreo): https://docs.expo.dev/versions/latest/sdk/image/
- Expo DOM components: https://docs.expo.dev/guides/dom-components/
- CHANGELOG de expo-gl (sdk-58): https://github.com/expo/expo/blob/sdk-58/packages/expo-gl/CHANGELOG.md
- expo/expo#51543 (WebGL2 `instanceof`): https://github.com/expo/expo/issues/51543
- expo/expo#51948 (R8 y GLView): https://github.com/expo/expo/issues/51948

**React Native Skia**
- Docs v2.14.0 en el repo:
  - https://github.com/wcandillon/react-native-skia/tree/v2.14.0/apps/docs/docs (`image.md`, `shapes/atlas.md`, `animations/gestures.md`, `animations/reanimated3.md`, `animations/hooks.md`, `animations/textures.md`, `canvas/canvas.md`, `canvas/rendering-modes.md`, `pictures.md`, `getting-started/installation.md`, `getting-started/web.mdx`, `getting-started/headless.md`)
  - Tipos `AtlasProps` e `ImageProps` con `sampling`: https://github.com/wcandillon/react-native-skia/blob/v2.14.0/packages/skia/src/dom/types/Drawings.ts
- Versiones y sitio:
  - v3.0.0 (Graphite, cambio incompatible): https://github.com/wcandillon/react-native-skia/releases/tag/v3.0.0
  - Docs v3 ("does not run in Expo Go"): https://wcandillon.github.io/react-native-skia/docs/getting-started/installation
  - Docs v2: https://wcandillon.github.io/react-native-skia/v2/
- Issues:
  - #4051 (el muestreo por defecto es lineal): https://github.com/wcandillon/react-native-skia/issues/4051
  - #4117 (unos 3,000 sprites con buen rendimiento): https://github.com/wcandillon/react-native-skia/issues/4117
  - #2688 (Atlas contra Picture): https://github.com/wcandillon/react-native-skia/issues/2688

**three.js y R3F**
- three.js, rechazo de WebGL 1: https://github.com/mrdoob/three.js/blob/dev/src/renderers/WebGLRenderer.js
- Instalación de R3F (React Native): https://github.com/pmndrs/react-three-fiber/blob/master/docs/getting-started/installation.mdx
- R3F #3517: https://github.com/pmndrs/react-three-fiber/issues/3517
- R3F #3558: https://github.com/pmndrs/react-three-fiber/issues/3558
- `@react-three/fiber` 9.8.2 (dependencias *peer*): https://www.npmjs.com/package/@react-three/fiber
- Tamaños medidos:
  - https://unpkg.com/three@0.186.1/build/
  - https://unpkg.com/pixi.js@8.22.0/dist/pixi.min.js
  - https://unpkg.com/phaser@4.2.1/dist/phaser.min.js

**PixiJS**
- Pixel art en v8: https://github.com/pixijs/pixijs/discussions/11018

**Gestos, animación y React Native**
- RNGH 3 (hooks y cambios de nombres): https://docs.swmansion.com/react-native-gesture-handler/docs/guides/upgrading-to-3
- Reanimated, accesibilidad y `ReduceMotion`: https://docs.swmansion.com/react-native-reanimated/docs/guides/accessibility/
- Reanimated `useSharedValue` (`get`/`set` con React Compiler): https://docs.swmansion.com/react-native-reanimated/docs/core/useSharedValue/
- Accesibilidad en RN: https://reactnative.dev/docs/accessibility
- AccessibilityInfo: https://reactnative.dev/docs/accessibilityinfo
- PixelRatio: https://reactnative.dev/docs/pixelratio
- Imágenes `@2x`/`@3x`: https://reactnative.dev/docs/images

**WCAG**
- 2.5.7 Dragging Movements: https://www.w3.org/WAI/WCAG22/Understanding/dragging-movements.html
- 2.5.8 Target Size (Minimum): https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- 2.2.2 Pause, Stop, Hide: https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html

**Isométrico y vóxeles**
- Clint Bellanger, *Isometric Tiles Math*: https://clintbellanger.net/articles/isometric_math/
- Shaun Lebron, *Isometric Blocks*: http://shaunlebron.github.io/IsometricBlocks y https://github.com/shaunlebron/IsometricBlocks
- Formato `.vox` de MagicaVoxel: https://github.com/ephtracy/voxel-model/blob/master/MagicaVoxel-file-format-vox.txt

**Datos**
- PostgreSQL, tipos JSON: https://www.postgresql.org/docs/current/datatype-json.html
- `sqlx::types::Json` (feature `json`): https://docs.rs/sqlx/0.9.0/sqlx/types/struct.Json.html
