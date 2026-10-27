import { createAudioPlayer, setAudioModeAsync, type AudioPlayer } from 'expo-audio';

/**
 * Sonidos de la interfaz (síntesis en docs/brand/make_sounds.py). Suenan en la categoría
 * `ambient` de iOS: callan con el interruptor de silencio y se mezclan con la música de la
 * persona en lugar de cortarla. Nunca suenan si "Sonidos" está apagado (lo está por defecto).
 */
const SOURCES = {
  tap: require('@/assets/sounds/tap.wav'),
  step: require('@/assets/sounds/step.wav'),
  confirm: require('@/assets/sounds/confirm.wav'),
  success: require('@/assets/sounds/success.wav'),
  reveal: require('@/assets/sounds/reveal.wav'),
  listenStart: require('@/assets/sounds/listenStart.wav'),
  listenEnd: require('@/assets/sounds/listenEnd.wav'),
  pixel: require('@/assets/sounds/pixel.wav'),
} as const;

export type Sound = keyof typeof SOURCES;

/** Duración de cada sonido, para esperar a que termine antes de grabar. */
export const SOUND_MS: Record<Sound, number> = {
  tap: 80,
  step: 200,
  confirm: 400,
  success: 900,
  reveal: 420,
  listenStart: 300,
  listenEnd: 340,
  pixel: 120,
};

export const VOLUME = { low: 0.45, medium: 0.8 } as const;

const players: Partial<Record<Sound, AudioPlayer>> = {};
let sessionReady = false;

/** Vuelve a la sesión de audio de la interfaz (por ejemplo, después de grabar). */
export async function restoreInterfaceAudio() {
  sessionReady = true;
  await setAudioModeAsync({ playsInSilentMode: false, interruptionMode: 'mixWithOthers', allowsRecording: false }).catch(
    () => {},
  );
}

function player(sound: Sound) {
  players[sound] ??= createAudioPlayer(SOURCES[sound]);
  return players[sound];
}

/** Carga los sonidos para que el primero no llegue tarde. */
export function preloadSounds() {
  if (!sessionReady) restoreInterfaceAudio();
  for (const sound of Object.keys(SOURCES) as Sound[]) player(sound);
}

export function playSound(sound: Sound, volume: number) {
  if (!sessionReady) restoreInterfaceAudio();
  const p = player(sound);
  p.volume = volume;
  p.seekTo(0)
    .then(() => p.play())
    .catch(() => {});
}
