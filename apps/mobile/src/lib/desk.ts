import { ITEMS, type ItemId } from '@/components/desk/layers';
import { usePlaybook } from '@/lib/queries';
import type { PlaybookEntry } from '@/lib/types';

/**
 * "Tu escritorio": cada ajuste que te ayudó deja un objeto en la escena. Es progreso que se
 * acumula y nunca se pierde (no hay rachas ni nada que caduque). Los ajustes "para pedir a tu
 * empresa" no se prueban aquí, pero comparten el objeto de su tema por si algún día cuentan.
 */
export const ITEM_FOR_ADJUSTMENT: Record<string, ItemId> = {
  noise_cancelling: 'headphones',
  earplugs: 'headphones',
  ask_noise_source: 'headphones',
  soft_masking: 'speaker',
  move_from_voices: 'succulent',
  book_quiet_room: 'succulent',
  move_from_smell: 'succulent',
  ask_quiet_desk: 'succulent',
  silence_notifications: 'phone',
  batch_messages: 'phone',
  focus_signal: 'sign',
  ask_focus_hours: 'sign',
  close_blinds: 'blinds',
  rotate_screen: 'blinds',
  turn_from_light: 'blinds',
  screen_brightness: 'screenDim',
  bigger_text: 'screenDim',
  one_window: 'screenDim',
  ask_antiglare: 'screenDim',
  desk_lamp: 'lamp',
  ask_lighting: 'lamp',
  clear_desk: 'tray',
  face_away: 'divider',
  ask_divider: 'divider',
  cooler_spot: 'fan',
  ask_temperature: 'fan',
  warm_layer: 'sweater',
  short_reset: 'mug',
  ask_remote_focus: 'frame',
};

/** Orden fijo para leerlos con VoiceOver: de izquierda a derecha en la escena. */
const ORDER = (Object.keys(ITEMS) as ItemId[]).sort((a, b) => ITEMS[a].box[0] - ITEMS[b].box[0]);

export function deskItems(playbook: PlaybookEntry[] | undefined): ItemId[] {
  const owned = new Set<ItemId>();
  for (const entry of playbook ?? []) {
    const item = ITEM_FOR_ADJUSTMENT[entry.adjustment.id];
    if (item && entry.helped > 0) owned.add(item);
  }
  return ORDER.filter((item) => owned.has(item));
}

export function useDesk() {
  const playbook = usePlaybook();
  return { items: deskItems(playbook.data), ready: playbook.isSuccess };
}
