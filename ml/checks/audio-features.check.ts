// Prueba las heurísticas de audio con señales sintéticas.
// Uso (Node 24): node ml/checks/audio-features.check.ts file:///<ruta absoluta>/apps/mobile/src/lib/audio-features.ts
import assert from 'node:assert/strict';

const { analyzeAudio, decodePcm } = await import(process.argv[2]);
const sr = 16000;
const seconds = 10;
let seed = 7;
const noise = () => {
  seed = (seed * 1103515245 + 12345) % 2 ** 31;
  return (seed / 2 ** 31) * 2 - 1;
};
const make = (f: (t: number) => number) => {
  const s = new Float32Array(sr * seconds);
  for (let i = 0; i < s.length; i++) s[i] = f(i / sr);
  return { samples: s, sampleRate: sr };
};

const cases: [string, ReturnType<typeof make>, { voices: boolean; constant: boolean; sudden: boolean }][] = [
  ['silencio', make(() => noise() * 0.0003), { voices: false, constant: false, sudden: false }],
  ['ventilación constante', make(() => noise() * 0.05), { voices: false, constant: true, sudden: false }],
  [
    'voces (armónicos de 180 Hz con sílabas a 4 Hz)',
    make((t) => {
      const syllable = Math.max(0, Math.sin(2 * Math.PI * 4 * t)) ** 2;
      let v = 0;
      for (let h = 2; h <= 16; h++) v += Math.sin(2 * Math.PI * 180 * h * t) / h;
      return 0.2 * syllable * v + noise() * 0.002;
    }),
    { voices: true, constant: false, sudden: false },
  ],
  [
    'tres golpes',
    make((t) => (Math.abs(t - 2) < 0.08 || Math.abs(t - 5) < 0.08 || Math.abs(t - 8) < 0.08 ? noise() * 0.6 : noise() * 0.003)),
    { voices: false, constant: false, sudden: true },
  ],
];

for (const [name, pcm, expected] of cases) {
  const found = analyzeAudio(pcm);
  assert.deepEqual(found, expected, `${name}: ${JSON.stringify(found)}`);
  console.log('ok', name, JSON.stringify(found));
}

// WAV de 16 bits ida y vuelta.
const pcm = cases[1][1].samples;
const wav = new Uint8Array(44 + pcm.length * 2);
const v = new DataView(wav.buffer);
const w = (o: number, s: string) => [...s].forEach((c, i) => (wav[o + i] = c.charCodeAt(0)));
w(0, 'RIFF'); v.setUint32(4, 36 + pcm.length * 2, true); w(8, 'WAVE'); w(12, 'fmt ');
v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true); v.setUint32(24, sr, true);
v.setUint32(28, sr * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); w(36, 'data');
v.setUint32(40, pcm.length * 2, true);
pcm.forEach((s, i) => v.setInt16(44 + i * 2, Math.round(s * 32767), true));
const decoded = decodePcm(wav);
assert.equal(decoded.sampleRate, sr);
assert.equal(decoded.samples.length, pcm.length);
assert.ok(Math.abs(decoded.samples[100] - pcm[100]) < 1e-3);
console.log('ok wav ida y vuelta');
const start = performance.now();
analyzeAudio(decoded);
console.log(`análisis de 10 s: ${(performance.now() - start).toFixed(0)} ms en Node`);
