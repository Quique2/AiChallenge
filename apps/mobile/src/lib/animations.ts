import { Easing, FadeIn, ZoomIn } from 'react-native-reanimated';

import { Motion } from '@/constants/theme';
import type { MotionLevel } from '@/lib/feedback';

/**
 * Entradas compartidas, según el nivel de movimiento (`useMotionLevel`). Con detalles, las cosas
 * crecen a saltos (`Easing.steps`), como un pixel que se enciende; en modo tranquilo son
 * fundidos cortos; con movimiento reducido no hay animación.
 */

/** La palomita de lo que se elige. */
export function checkEntering(level: MotionLevel) {
  if (level === 'reduced') return undefined;
  if (level === 'detailed') return ZoomIn.duration(150).easing(Easing.steps(3));
  return FadeIn.duration(Motion.fast);
}

/** Algo nuevo que conviene mirar, como los marcadores de la foto. `index` los ordena uno tras otro. */
export function revealEntering(level: MotionLevel, index = 0) {
  if (level === 'reduced') return undefined;
  if (level === 'detailed') return ZoomIn.delay(150 + index * 120).duration(240).easing(Easing.steps(4));
  return FadeIn.duration(Motion.base);
}

/** Un bloque de contenido que cambia (la sugerencia, el resultado). */
export function contentEntering(level: MotionLevel) {
  if (level === 'reduced') return undefined;
  return FadeIn.duration(Motion.base).easing(Motion.easeOut);
}
