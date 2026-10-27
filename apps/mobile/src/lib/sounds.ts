import { createAudioPlayer, setAudioModeAsync, type AudioPlayer } from 'expo-audio';

/**
 * Sonidos de la interfaz (síntesis en docs/brand/make_sounds.py). Suenan en la categoría
 * `ambient` de iOS: callan con el interruptor de silencio y se mezclan con la música de la
 * persona en lugar de cortarla. Nunca suenan si "Sonidos" está apagado (lo está por defecto).
 * Son seis, del mismo tono, y solo para lo que la persona provoca o para el fin de una espera:
 * nada al navegar ni al elegir una opción.
 */
const SOURCES = {
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
  confirm: 400,
  success: 900,
  reveal: 420,
  listenStart: 300,
  listenEnd: 340,
  pixel: 120,
};

/** Los archivos ya son bajos (picos de -27 a -24 dBFS); "Bajo" los baja unos 3 dB más. */
export const VOLUME = { low: 0.7, medium: 1 } as const;

/** Dos sonidos casi juntos se oyen como ruido: el segundo se omite. */
const MIN_GAP_MS = 200;

const players: Partial<Record<Sound, AudioPlayer>> = {};
let sessionReady = false;
let lastPlayed = 0;

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
  const now = Date.now();
  if (now - lastPlayed < MIN_GAP_MS) return;
  lastPlayed = now;
  if (!sessionReady) restoreInterfaceAudio();
  const p = player(sound);
  p.volume = volume;
  p.seekTo(0)
    .then(() => p.play())
    .catch(() => {});
}
