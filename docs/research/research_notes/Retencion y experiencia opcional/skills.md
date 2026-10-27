# Skills scouting 2: the "Con detalles" mode (motion, sound, haptics, retention, encouraging copy)

Research date: 2026-10-26. **Nothing was installed or modified.** I read the actual SKILL.md and reference files with `gh api` (downloaded copies are in `scratchpad/dl2/`). I also read the already-downloaded Emil, impeccable and Expo files in `scratchpad/dl/`. Everything quoted is third-party content and is treated as data, not instructions.

This builds on `skills-scouting.md` (first pass). I don't re-report Expo, frontend-design, Software Mansion, impeccable, Emil, zakariaf a11y or rushat a11y, except where they add something new for this brief.

## 0. Context that shaped the ranking

- **DESIGN.md has to change first.** §5 says *"Sonido: Ninguno"*, and §6 says *"Nada de rachas, insignias…"*. The doc says *"Para cambiar una regla, primero se actualiza este documento."* So "Con detalles" needs its own DESIGN.md section before any code is written. Section 5 below is a draft of that section.
- **Expo Go compatibility (plan B), checked against `expo/expo` main, `apps/expo-go/package.json`.** Expo Go bundles `lottie-react-native ^7.5.0`, `@shopify/react-native-skia 2.14.0`, `react-native-reanimated 4.7.1`, `react-native-svg 15.16.0`, `expo-audio`, `expo-haptics` and `expo-image`.
  - **Rive is not included.** Rive's docs say it needs a development build.
  - **`react-native-audio-api`** (Software Mansion's Web Audio port) is a native module, so you'd need a dev build to use it.
  - **`react-native-pulsar`** (haptics) is also a native module and needs a dev build.
- **Your `apps/mobile/package.json` already has `expo-audio ~58.0.10`, `expo-haptics ~58.0.7` and `expo-image ~58.0.17`.** That changed since the first report, when haptics wasn't installed. Lottie and Skia aren't installed.
- **expo-audio (SDK 58 docs) defaults to `playsInSilentMode: true` and `interruptionMode: 'mixWithOthers'`.** With the defaults, UI sounds would play even with the silent switch on, so you must override `playsInSilentMode` (rule 9).
- **expo-image (SDK 58 docs) has no nearest-neighbour or resampling prop.** Pixel art has to be pre-scaled to integer multiples at build time. `draw_icon.py` already has `upscale(img, k)` using `Image.NEAREST`.
- **The brand already contains the best signature moment.** `draw_icon.py`, line 5: *"a monitor whose wave settles into a flat line (noise easing off)"*. That is the product's own metaphor, and it's the one place a "Con detalles" flourish has meaning.

---

## 1. Ranked recommendations (TL;DR)

| # | What | Install (review first) | Why |
|---|---|---|---|
| 1 | **`ux-sound`** (jal-co) + **`ui-sound-design`** (dannyjpwilliams), used as a pair | `npx skills add jal-co/skills --skill ux-sound` and `npx skills add dannyjpwilliams/ui-sound-design-skill`. Safer: copy `skills/ux-sound/` and `skills/ui-sound-design/` into `apps/mobile/.claude/skills/` | `ux-sound` decides **whether, what, how loud**: a dBFS ladder, a "butler" personality, *"most products need three sounds or fewer"*, and Reduce Motion mutes sound. `ui-sound-design` turns *"softer, warmer"* into synthesis parameters, and its HTML preview **exports WAV files** you can bundle for expo-audio. Both are Markdown-first, MIT, and calm-compatible. `ux-sound` explicitly delegates the mechanics to `ui-sound-design`. |
| 2 | **`motion-design`** (LottieFiles, org, 2.5k★) | `npx skills add LottieFiles/motion-design-skill`, or copy `skills/motion-design/` | The most concrete motion tables I found: ambient and idle amplitudes and cycle times, a success recipe, overshoot budgets, stagger budgets, a mobile ×0.8 factor, and "pause controls for animations >5 s". It needs overrides, because it says *"Always three motion layers"* (see §4). |
| 3 | **Owl-Listener `interaction-design`** (3.1k★) + **`inclusive-interaction` / `cognitive-accessibility`** (inclusive-design-skills, 107★) | `/plugin marketplace add Owl-Listener/designer-skills`, then `/plugin install interaction-design@designer-skills`, `/plugin install inclusive-interaction@designer-skills`, `/plugin install cognitive-accessibility@designer-skills` | Short, clean Markdown skills: motion tokens, loading thresholds, peak-end, onboarding, "interfaces that feel", motion sensitivity (WCAG flashes and >5 s auto-motion), and focus/attention (*"No autoplay audio"*). No skill-level scripts. Skip its `zeigarnik-effect` skill (it's about creating pressure to finish). |
| 4 | **UX writing:** `ux-writing` (content-designer, 248★) **or** Anthropic `ux-copy` (official) | `npx skills add content-designer/ux-writing-skill`. For Anthropic, copy only `design/skills/ux-copy/SKILL.md` from `anthropics/knowledge-work-plugins`, because the full `design` plugin adds 9 MCP connectors | Patterns for success, empty, error and permission copy; 40–60 characters per line; 7th-grade reading level. Pair it with the "encouragement without pressure" rules in §5. Those come from non-installable references (Marvin tone rules, Hifz-Companion, sobriety-app-design). |
| 5 | **Retention and ethics reviewer:** `gamification-loops` (omer-metin, 183★, Apache-2.0) + `hooked-review` ethics (tzn068) | `npx -y skills add omer-metin/skills-for-antigravity --skill gamification-loops --agent claude-code`, or copy `skills/gamification-loops/`. Copy `hooked-review/references/ethics.md` as a review checklist | Use these as *reviewers*, not generators. Each has a red-line list (punishment for not engaging, guilt-based retention, infinite variable rewards), an overjustification warning, and streak protections. Ignore their "surprise bonus" and leaderboard sections. |
| – | **Read, don't install** | Copy individual files into `docs/` if useful | `bixxter/app-growth-design` `retention-gamification.md` (best evidence base on streaks, shame and peak-end, but it also teaches loss aversion); `draftbit/mobile-taste-skill` (the `MOTION_INTENSITY` dial and value-first onboarding; license unclear; uses old `.value`/`runOnJS`); `enzomanuelmangano/skill` "reactiive" (good RN spring tokens; **no license**); `KaiChi888/ios-game-feel-design-skill` (feedback-matrix architecture; SwiftUI; **no license**); `dylantarre/animation-principles` (`calm-relaxation`, `loading-states`); `detaildotdesign/skill` (motion and easter-egg details; **no license**); `raphaelsalaja/userinterface-wiki` (audio rules); Axiom / johnrogers haptics design principles (Swift). |
| – | **Skip** | – | Rive skills (all need a dev build; no official skill); Pulsar skills (native); SoundWeaver (0★, web, ships a 1.26 MB base64 blob plus Python generator); clawfu (archived); `adamlyttleapps` questionnaire onboarding (fake loading, "aspirational" testimonials, sunk-cost paywall gate); `curiositech adhd-design-expert` (*"If a neurotypical person finds it 'too much,' it's probably right"*; also requests third-party MCP tools); gamedev `game-feel` (engine-specific); freshtechbro Lottie/Rive (web); `alphaparkinc` streak "skill" (a Python MCP client for a vendor); `dungnotnull` SDT (Python pipeline plus hooks). |

**Suggested setup:**
- Install #1 at **project scope** (`apps/mobile/.claude/skills/`), because sound is project-specific.
- Install #2 and #3 at project scope, alongside Expo, and add the override block from §6 to `apps/mobile/CLAUDE.md`.
- #4 can go at user scope.
- Load #5 only when designing the retention features.

---

## 2. Recipes from the already-downloaded files (Emil, impeccable, Expo)

They are grouped by the seven moments you asked about. Expo's copy of the Emil skill is the canonical RN one. The curves used below are `EASE_OUT = Easing.bezier(0.23, 1, 0.32, 1)`, `EASE_IN_OUT = (0.77, 0, 0.175, 1)` and `EASE_SHEET = (0.32, 0.72, 0, 1)`. Shared values use `.get()/.set()`, and worklets call back with `scheduleOnRN`.

| Moment | Recipe | Source |
|---|---|---|
| **Step-progress indicator** | Measure the steps once with `onLayout`, then animate the fill with `withTiming(x, { duration: 250, easing: EASE_IN_OUT })`. Animating `width` is *"the sanctioned width animation: the pill is absolutely positioned with no children."* Use `ease-in-out` *"because the pill is moving across the screen."* Fire `Haptics.selectionAsync()` *"on the press, not when the pill lands."* `linear` is only for *"Constant motion (progress, marquee)"*. | expo RECIPES "Tab / segmented indicator"; expo SKILL easing table |
| **Selection feedback** | Rows: *"Full-width list rows… highlight their background instead"* of scaling. Buttons: `scale 0.97`, 120 ms, `cubicBezier(0.23,1,0.32,1)` as a Reanimated CSS transition. *"Feedback on press-in, commit on press-out."* Frequency gate: *"Tens of times/day → under 150ms, or nothing."* Haptic: `selectionAsync()` for steps and detents. | expo RECIPES "Press feedback"; Emil find-animation-opportunities Gate §1 |
| **Success / celebration** | Only in the *"Rare / first-time… success states… celebration"* tier: *"The delight budget lives here."* Use `Haptics.notificationAsync(Success)`. impeccable allows a *"deliberately authored focal entrance"* at 500–800 ms, and *"Exit faster than entrance."* Emil's apple-design §16: *"Delight. The result of getting the other seven right, not confetti tacked on top."* | expo SKILL; impeccable animate.md; Emil apple-design |
| **Loading / scanning** | The Expo design-system "Spinner Blink" tell: no full-screen `ActivityIndicator`; use four-state screens. impeccable: *"Long feedback feels like latency."* Emil: *"Skeleton / Shimmer: a placeholder with a moving sheen"* (vocabulary only). SWM: infinite CSS animations need a Reduce Motion path (*"Cap `animationIterationCount` at `1`… use `1` (1ms), never `0`"*). | expo native-slop #19; SWM animations.md |
| **List / marker entrances** | `FadeInDown.duration(250).delay(index * 40)`, memoized per row; *"Stagger 30–80ms."* *"Never put `entering` on a row inside `FlatList`… Rows are recycled."* *"Entrance animations are for content the user asked for."* Start from `scale(0.9–0.97)` with `opacity: 0`, *"Never `scale(0)`."* Emil's gate: stagger is decorative and *"must never block interaction"*. | expo RECIPES "List entrances"; Emil find-animation-opportunities "Group entrances" |
| **Idle animation** | Emil (apple-design §14): *"avoid full-viewport moving backgrounds, slow looping oscillations (near 0.2 Hz / one cycle per 5s)…"* and *"Make large moving objects semi-transparent while they travel."* impeccable: *"Any nonessential loop must stop when offscreen or hidden."* SWM: *"`withRepeat` (infinite) does not start"* under reduced motion, but CSS animations ignore it. | Emil apple-design; impeccable animate.md; SWM |
| **Sound + haptic pairing** | Emil apple-design §13, from WWDC *Designing Audio-Haptic Experiences*: (1) **Causality**: *"Trigger it on the actual causal event"*. (2) **Harmony**: *"the visual, the sound, and the haptic must fire on the same frame."* (3) **Utility**: *"Reserve haptics/sound for meaningful moments… Over-feedback trains users to ignore all of it."* Expo's three absolute rules: *"Same frame as the visual… One per user action… Never the only feedback."* From a worklet: `scheduleOnRN(Haptics.selectionAsync)`. One-shot thresholds use `useAnimatedReaction`, so the JS call fires twice per pull, not every frame. | Emil apple-design; expo SKILL §8; expo RECIPES |

Emil's `mobile-native` skill is web/PWA only (tap highlight, `100dvh` and so on), so it doesn't apply here. `animation-vocabulary` is useful only for naming effects: *Stepped animation*, *Idle animation*, *Hold to confirm*, *Line drawing*, *Number ticker*.

---

## 3. New candidates, by topic

### 3.1 UI sound design

**(A) `ux-sound`, jal-co/skills.** https://github.com/jal-co/skills/tree/main/skills/ux-sound
- **Trust:** 6★, MIT, pushed 2026-07-29, individual maintainer, listed on skills.sh.
- **Files:** `SKILL.md` (23 KB) and `references/generating.md`. **Scripts (flagged):** `scripts/transients.mjs` and `scripts/trim-to-transient.sh`. They're optional, for measuring recorded clips. The GENERATE route in `generating.md` uses a paid generation API, but the skill says *"Never sign the user up for a paid service to finish a task."*
- **Install:** `npx skills add jal-co/skills --skill ux-sound`, or `cp -r skills/ux-sound ~/.claude/skills/`.
- **Key rules (quoted):**
  - Decision tree: *"Does the sound carry information the user cannot already see? … No → NO SOUND."* One *"signature moment (one per product)"* may skip that question.
  - *"Never play sound on page load, route change, or scroll."* Also *"Never sound on typing or keyboard navigation."*
  - Types and lengths: micro feedback 10–120 ms; earcon 200–600 ms; notification 300–900 ms.
  - **Level by measured dBFS peak, not by gain number:**

    | Level | Class | Target peak |
    |---|---|---|
    | 0 | Continuous (hum, drone, hold) | ≤ −40 dBFS |
    | 1 | Implicit micro feedback (hover) | −38 dBFS |
    | 1 | Explicit micro feedback (press, send) | −27 dBFS |
    | 2 | Notification | −20 dBFS |
    | 3 | Alert | −12 dBFS |

    *"A deliberate gesture may sit up to 9dB above the ambient one it accompanies, never more."*
  - *"Nothing sustained should carry energy in 2–5kHz"*. Verify it by rendering offline: under 1% of energy above 2 kHz. The fix in its case study was *"a 900Hz lowpass and nothing above 291Hz."*
  - **Personality:** *"The butler — discreet, never speaks first. Only ever confirms what the user did. Micro feedback only, level 1 maximum, no notifications without an explicit setting."* That is SpaceEase.
  - *"`prefers-reduced-motion: reduce` mutes sound by default… someone who asked an interface to stop moving did not ask it to start talking."* An explicit opt-in still wins.
  - Ship a mute control *"the user can find in the moment the sound annoys them"*. Persist it, and read it before every play.
  - *"Always debounce identical sounds by 90ms minimum."* Decode clips up front, not on first use.
  - Audit = *"deletions first, fixes second, additions last (usually empty)"*. *"Most products need three sounds or fewer."*
- **Fit:** excellent. It's web-centric (Web Audio, `localStorage`), so translate it to expo-audio plus your settings store.

**(B) `ui-sound-design`, dannyjpwilliams.** https://github.com/dannyjpwilliams/ui-sound-design-skill
- **Trust:** 43★, MIT, pushed 2026-04-08, individual maintainer.
- **Files:** `SKILL.md`; `references/` (`web-audio-api.md`, `sound-recipes.md`, `audio-rules.md`, `tone-js.md`, `audio-file-references.md`); `assets/sound-preview.html`. **Script (flagged):** `tools/analyze-sound.mjs` (40 KB, zero-dependency Node; non-WAV input needs ffmpeg). It's optional and only analyzes a reference file you give it.
- **Install:** `npx skills add dannyjpwilliams/ui-sound-design-skill`, or copy `skills/ui-sound-design/` to `.claude/skills/`.
- **Workflow:** *Describe → Generate → Listen → Refine*. The HTML preview *"exports a .wav file for use in production code"*. That is the expo-audio route: synthesize in the browser on your PC, download the WAV, bundle it.
- **Concrete parameters (quoted from the recipes):**
  - **Volume:** default gain `0.3`; *"Maximum volume: 0.8 — never exceed"*; hover `0.03–0.08`.
  - **Envelopes:** *"Never ramp gain to zero"* (use `0.001`). Stop the oscillator `+0.01 s` after the envelope to avoid a click.
  - **Vocabulary bridge:**
    - "Softer": volume 0.3 → 0.15, attack 0 → 0.01 s.
    - "Warmer": switch to sine or triangle, cutoff 3000 → 1200 Hz.
    - "More professional": *"Lower volume, sine wave, short duration"*.
  - **Soft click:** `{ frequency: 1200, Q: 1, duration: 0.06, volume: 0.15 }` (bandpass-filtered noise).
  - **Minimal toggle:** range 550–650 Hz, 0.08 s, volume 0.15.
  - **Gentle ding:** *"Single triangle note at 880Hz, duration 0.3, volume 0.2"*. Success is an *"Ascending major third"* (base 523 Hz, 0.12 s notes, 0.08 s gap); *"Gentler"* uses triangle, 0.15 volume, 0.18 s notes.
  - **Soft bell:** `{ frequency: 660, modRatio: 1.2, modDepth: 500, duration: 0.6, volume: 0.15 }`.
  - **Gentle error:** *"Sine wave, 350→250Hz, duration 0.2, volume 0.15"*.
- **Conflicts:**
  - **Whoosh for page transitions:** ignore; native transitions stay silent.
  - **Hover sounds:** don't apply on iOS.
  - *"More playful → higher pitch"*: keep pitch low (see rule 8).

**(C) `userinterface-wiki`, Raphael Salaja.** https://github.com/raphaelsalaja/userinterface-wiki
- **Trust:** 933★, MIT, pushed 2026-07-29, individual maintainer (a designer).
- **Files:** the repo is a Next.js site full of TS demos; the skill is just `skills/SKILL.md` (152 rules). Its referenced `rules/*.md` files weren't under `skills/` in the tree.
- **Install:** copy `skills/SKILL.md`.
- **Audio rules:** `a11y-visual-equivalent`, `a11y-toggle-setting`, *"`a11y-reduced-motion-check` - Respect prefers-reduced-motion for sound"*, `a11y-volume-control`, *"`appropriate-confirmations-only`"*, *"`appropriate-no-punishing` - Inform, don't punish with harsh sounds"*, *"`impl-default-subtle` (0.3)"*, *"`weight-match-action`"*, *"`param-click-duration` - Click sounds: 5-15ms"*.
- **Conflicts:**
  - `easing-exit-ease-in` (Expo says never ease-in).
  - `physics-active-state` (scale on every interactive element, against DESIGN §5).
  - `ux-zeigarnik-show-incomplete` (pressure to finish).

**(D) `ux-sound-design` + `sonic-branding`, ClawFu.** https://github.com/guia-matthieu/clawfu-skills
- **Trust:** 150★, MIT, **archived**. It references an MCP server `@clawfu/mcp-skills`. Copy only, if at all.
- **Useful rules:**
  - *"Calm | Soft attack, slow decay, filtered"*.
  - Pick a **tonal center** (*"All sounds should relate to this key"*).
  - **Loudness hierarchy:** feedback −6 dB and ambient −12 dB relative to notifications.
  - *"Throttle: max 1 sound per 200ms"*. *"No sound on app open"*.
  - **File spec:** *"Sample rate: 44.1kHz… 16-bit… Mono… Peak level: -1dB"*.
  - Its calm "task app" example: task created = *"Single mallet note (G4), soft attack, 120ms"*; completed = *"Two notes ascending (C4 → E4), 250ms total"*.
- **Conflicts:**
  - *"Play sounds AFTER visual feedback"* with a 200 ms delay, which contradicts Apple's causality rule.
  - A looping *"Payment Processing"* tone.
  - *"Pair all sounds with haptic"*.

**(E) Others:**
- **SoundWeaver** (`uaredumb/soundweaver`, 0★): web-only. Its one useful pointer is CC0 libraries (*"Kenney Interface Sounds, Google Material Product Sounds"*) and *"default to muted/reduced when prefers-reduced-motion"*.
- **`smolgroot/earcons`** (7★) and **`usespaceui/sounds`** (5★) are TS Web Audio libraries, not skills.
- **`curiositech/windags-skills`** (`sound-design-and-audio`) and **`ruminoob/sound-skill`** (0★) weren't evaluated in depth.
- **Software Mansion `react-native-audio-api`** sub-skill (already in the bundle you scouted). New facts: it's native, so not for Expo Go; *"Single AudioContext"*; *"Suspend when idle"*. iOS `ambient` category = *"Mixes with other apps, respects silent switch."*

### 3.2 Haptics (expo-haptics stays the API)

There's no RN haptics-design skill beyond Expo's table (first report). The design principles all trace back to Apple WWDC21 *Practice audio haptic design*.

- **CharlesWiltgen/Axiom → `axiom-media/skills/haptics.md`.** https://github.com/CharlesWiltgen/Axiom
  - **Trust:** 1,231★, MIT, very active, individual maintainer. A huge Swift plugin (2,126 files), so don't install it for RN.
  - **Useful:** Causality, Harmony, Utility; `prepare()` on touch-down to cut latency; *"A large object should feel heavy, sound low and resonant, and look substantial."*
- **johnrogers/claude-swift-engineering → `haptics/references/design-principles.md`.**
  - **Trust:** 233★, MIT.
  - *"Even 100ms delay breaks the illusion"*; *"When NOT to use haptics: Every single tap… Scrolling through lists"*; *"Test with haptics disabled - does the UI still work?"*
- **mae616/ai-template → `sensory-design`** (Japanese).
  - **Trust:** 9★, MIT.
  - *"UI音の長さは150〜350ms"* (UI sounds 150–350 ms); *"キークリックフィードバック: 10〜20ms"* (key-click haptics 10–20 ms); *"Less is More — 過剰な振動は不快で感覚の麻痺を招く"* (excess vibration is unpleasant and numbing); avoid "buzzy" vibration for UI operations.
- **Skip:** `mahdidavoodi7/react-native-pulsar-skill` and SWM `pulsar-haptics`. Both need the native Pulsar SDK.

### 3.3 Motion and micro-interactions (RN-relevant)

**(A) LottieFiles `motion-design`.** https://github.com/LottieFiles/motion-design-skill
- **Trust:** 2,533★, MIT, LottieFiles organization, pushed 2026-05-18.
- **Files:** 20 Markdown files, no scripts.
- **Install:** `npx skills add LottieFiles/motion-design-skill`.
- **Values worth keeping:**
  - **Ambient / idle:** *"Waiting/idle | 0.98-1.02 | 3000ms"*; *"Background element | 0.99-1.01 | 4000ms"*; *"Pulsing >±5% scale becomes attention-demanding"*; *"Ambient amplitude: 10-20% of primary motion"*.
  - **Shimmer:** *"1500-2500ms/sweep, Pause 2000-5000ms between sweeps"*.
  - **Checkmark success:** *"Container: scale 0.9→1.0 (200ms, ease-out-back, 5-10% overshoot); Checkmark: stroke draw (150ms, ease-out, 100ms delay); Total: 400-500ms"*.
  - **Overshoot budget:** *"Error 0%, Feedback 2-5%, Success 5-10%, Celebration 15-25%, Premium 0%"*.
  - **Stagger:** *"Micro cascade 20-40ms <200ms"*; *"Total stagger MUST stay <500ms"*.
  - **Mobile:** *"0.8x… Reduced (1-2 properties)… reduce stagger budgets by 30%; avoid parallax"*.
  - **Accessibility:** *"never auto-play loops"* under reduced motion; *"Pause controls for animations >5 seconds"*; *"Same interaction = same animation every time"*.
  - **Context:** *"Healthcare | Corporate/Calm | 300-600ms | Very low"* motion density; *"Mixing Archetypes: 90% primary… corporate dashboard borrows Playful for success state only."*
- **Conflicts (override them):**
  - *"Always three motion layers — primary + secondary + ambient"* (labelled CRITICAL).
  - *"Never opacity-only for important state changes"*.
  - *"Exit=ease-in"*.
  - Error shake ±10–15 px.
  - Confetti and particles.

**(B) Owl-Listener `interaction-design` / `design-systems`.** https://github.com/Owl-Listener/designer-skills
- **Trust:** 3,115★, MIT, pushed 2026-09-05, individual maintainer. The repo has Python and shell maintenance scripts (index/README generators); the skills themselves are Markdown.
- **motion-system tokens:** instant 50, fast 100, normal 200, moderate 300, slow 400, deliberate 600 ms. *"Don't create more tokens than you have distinct use cases. 4–6 values is usually enough."* *"Document what should NOT animate as clearly as what should."*
- **loading-states:** *"Under 100ms: no loading indicator needed; 100ms-1s: subtle indicator; 1-10s: clear loading state with progress if possible; Over 10s: detailed progress, time estimate, background option."*
- **interfaces-that-feel:**
  - *"Recovery space: after an error, give the user 300–600ms before the next prompt"*.
  - *"Success | Warm and brief — acknowledge, don't overdo it"*.
  - *"Loading | Present and calm — 'Getting your data' not 'Loading...'"*.
  - Reference apps include *Gentler Streak* and *How We Feel*.
- **peak-end-rule:** *"Never end on an administrative or transitional screen."*
- **onboarding-design:** *"Orient, don't educate"*, *"Defer collection"*.
- **Skip:** `zeigarnik-effect` and the `ease-spring (0.34, 1.56, 0.64, 1)` overshoot token.

**(C) Owl-Listener/inclusive-design-skills.** https://github.com/Owl-Listener/inclusive-design-skills
- **Trust:** 107★, MIT. Same marketplace as (B).
- **motion-sensitivity:** *"Flashing content faster than 3 times per second (seizure risk — this is a WCAG Level A requirement)"*; parallax and full-viewport zoom are triggers; it notes *"People with anxiety disorders (unexpected motion increases stress)"*.
- **focus-attention-design:** *"No autoplay audio or video"*; *"No flashing, blinking, or rapidly changing content"*; *"Animation only for functional feedback"*; *"Allow at least 20 seconds per required decision"*.
- WCAG 2.2.2 (Pause, Stop, Hide) applies to any idle loop longer than 5 s.

**(D) dylantarre/animation-principles.** https://github.com/dylantarre/animation-principles
- **Trust:** 129★, MIT, last push 2025-12-30. 144 small Markdown skills; copy only the ones you want.
- **calm-relaxation:** fades *"400-600ms"*; *"Breathing pulse | 4000-6000ms"*; *"cubic-bezier(0.4, 0, 0.6, 1)"*; squash *"Very subtle (2-5%)"*.
- **loading-states:** *"Show spinner after 200ms delay (avoid flash for fast loads); Minimum display: 500ms"*.
- **continuous-loops:** *"Test at 30 seconds - still pleasant?"*
- **feedback-indicators:** inline validation 150 ms; checkmark draw 400 ms; success toast auto-dismiss 4000 ms.
- **Conflict:** its 4–6 s breathing is right at Apple's *"near 0.2 Hz"* warning (§4). It also says *"Overshoot scale to 1.2"* for success.

**(E) enzomanuelmangano/skill ("reactiive").** https://github.com/enzomanuelmangano/skill
- **Trust:** 10★, **no license**, Markdown. The author is a known RN animation educator.
- *"My range: 0.95 - 1"* dampingRatio *"for professional UI"*.
- Spring tokens: `quick {dampingRatio:1, duration:200}`, `default {1, 300}`, `slow {1, 450}`, `soft {0.95, 350}`. *"Three spring configs for the whole app."*
- Transforms use `withSpring`; opacity and colours use `withTiming`.
- *"If you can't name the job, delete the animation."*
- **Conflicts:** pressto *"globalHandlers… onPress: () => Haptics.selectionAsync()"* (a haptic on every press); 50 ms list stagger everywhere; the "Magic Button" blur and gradient. Read it; don't vendor it.

**(F) draftbit/mobile-taste-skill.** https://github.com/draftbit/mobile-taste-skill
- **Trust:** 8★, Draftbit organization, license NOASSERTION.
- **Install:** `/plugin marketplace add draftbit/mobile-taste-skill`, then `/plugin install mobile-taste-skill@mobile-taste-skill`.
- **Best idea:** *"`MOTION_INTENSITY` … 1 = native transitions only, 10 = gesture-driven physics everywhere"*. That maps directly to Tranquilo ≈ 2 and Con detalles ≈ 5.
- **value-first-onboarding:**
  - *"every screen either collects an input that changes the app, or shows the real product"*.
  - *"Progress = thin bar in the header, not dots"*.
  - *"MOTION 4-7: option rows stagger in (first mount only, <= 400ms total)… Reduced motion: instant"*.
  - Permission priming before the system prompt.
- **Domain rules:** *"Health / fitness | … streak-guilt patterns"* and *"Productivity / tools | … celebration modals"* are listed under "avoid". *"Never [haptics] on plain taps or navigation."*
- **Conflict:** its code skeletons use `sharedValue.value` and `runOnJS`, against Expo/SWM conventions.

**(G) KaiChi888/ios-game-feel-design-skill.** https://github.com/KaiChi888/ios-game-feel-design-skill
- **Trust:** 2★, **no license**, SwiftUI.
- **Architecture worth copying in TypeScript:**
  - Define a **semantic event plus occurrence token** first, then map it across channels.
  - Feedback matrix: *"Outcome | Visual | Haptic | Sound | Timing"*.
  - *"Choose a single lead channel for the moment."*
  - *"Reserve the top of the ladder so it remains meaningful."*
  - Rhythm: *"tap -> immediate scale/haptic; 80-180ms later -> glow, badge pop…"*.
  - *"per-effect cooldowns"*.
  - *"Reduce Motion should produce a coherent alternate timeline… Never make haptics, sound, or particles the only way to distinguish success from failure."*
- **Conflicts:** streak rewards; camera shake (*"120-220ms… 4-12pt"*; *"avoid… finance, medical"*); confetti.

**(H) detaildotdesign/skill.** https://github.com/detaildotdesign/skill
- **Trust:** 68★, organization, **no license**.
- `motion.md` #15: *"Reduce animation for frequently used features… Reserve full motion for first-run or rare moments."*
- #22: one ambient lifecycle indicator that morphs through loading, active and complete.
- `easter-egg.md`: *"Embed a real detail where people look closely"* and *"Reward the explorer in overlooked corners"*. **Skip when:** *"The user is trying to recover from a serious failure."*
- **Idea for SpaceEase:** a static, quiet detail in the pixel window (for example, the sky matches the time of day). It's a delight that doesn't move.

**(I) gamedev-skills `game-feel`** (4,821★, Apache-2.0): engine-specific (Godot/Unity). Its only transferable line is *"add a 'reduce screen shake'/'reduce flashing' accessibility option."* Its core claim, *"5–8 tiny responses firing together"*, is the opposite of calm. Skip it.

### 3.4 Lottie, Rive and pixel sprites in React Native

- **Lottie:** `lottie-react-native` is in Expo Go (^7.5.0). Expo's own skill says *"Lottie — for illustration only, never for UI state"*.
  - `diffusionstudio/lottie` (5,632★, MIT, organization; 14 script files) generates Lottie JSON from text.
  - `freshtechbro/claudedesignskills → lottie-animations` (1,139★; 90 skills; 252 script-like files; last push 2025-11) targets `lottie-web` and `dotlottie-react`, i.e. the web.
  - Neither helps pixel art, which is SpaceEase's identity. Vector Lottie would be a second visual language beside the pixel scene (Expo: *"Never introduce a second system beside an existing one"*).
- **Rive:** every skill found is community-made (`BowTiedSwan/rive-skills` 27★ with no license, web/Luau; the "native-rive" listing on claudskills.com has no source repo). The Rive RN runtime **needs a dev build**. Skip it while plan B is Expo Go.
- **Pixel sprites:** no dedicated RN sprite skill exists. This recipe is synthesized from verified sources:
  1. **Frames come from `draw_icon.py`** (the source of truth). Render each frame at 32×32, then `upscale(img, k)` with `Image.NEAREST` to the exact display size times @2x/@3x. Pre-scaling is required, because expo-image has no nearest-neighbour prop (SDK 58 docs).
  2. **Frame economy** (local `pixel-art-mastery`): *"idle: 4 // Subtle breathing/movement"*; *"idleFrames: [0, 0, 1, 1]… idleFrameTime: 300"*; positions rounded to the integer grid; *"The best animations have fewer frames, not more."*
  3. **Playback option (a), Reanimated CSS animation:** a sprite strip inside an `overflow: 'hidden'` view, with `animationTimingFunction: steps(N)` and `animationName: { to: { transform: [{ translateX: -stripWidth }] } }`. Reanimated 4 supports `steps()` (SWM). It **ignores Reduce Motion**, so gate it yourself, and cap `animationIterationCount`.
  4. **Playback option (b), expo-image** with an animated WebP or APNG: `autoplay` defaults to `true`, so pass `autoplay={false}` when calm or reduced, and use `startAnimating()`/`stopAnimating()`.
  5. **Skia** (in Expo Go) can draw with nearest-neighbour sampling if you need runtime scaling. This is from my own knowledge of the Skia API, not verified in this pass.
  - The Aseprite tools (`with-pebbly/aseprite-ai-artist` 480★, MCP; `aigengame/aseprite-automation`) need the Aseprite app. You don't need them, because the Python script already authors the scene.

### 3.5 Retention, onboarding, habits and gamification

**(A) bixxter/app-growth-design → `skill/references/retention-gamification.md`.** https://github.com/bixxter/app-growth-design
- **Trust:** 3★, MIT. The `skill/` folder is Markdown (about 370 KB across 7 files), distilled from one creator's videos. The repo also ships `bin/install.mjs` and a video/subtitle pipeline (shell, Python, JS) (flagged), so copy only `skill/`.
- **Best evidence base found:**
  - §5: *"Prefer completion drive over loss aversion… streaks run on fear of losing what you built… one burns out, the other recharges itself"*; tie the closable loop *"to a real-world outcome"*.
  - §6: *"Ship competence feedback, not badge theater"*. A 2024 meta-analysis found gamification has *"minimal impact on competence (g = 0.277)"*.
  - §7: gamification depth is *"S-shaped… overload zone"*; *"provide adaptive controls that let users streamline secondary mechanics"*; Habitica: *"cognitive overload disguised as engagement"*.
  - §8: streaks shift *"from 'I want to do this' to 'I can't miss today'"*; it cites the proposed **EU Digital Fairness Act** wording *"'daily streaks' that penalise taking a break"* and the 2024 Nevada AG action against Snapchat.
  - Decision guide: *"IF your product depends on honest self-report (nutrition, mood, health, finances) THEN delete the shame mechanics — no breakable streaks, no red over-target numbers, no guilt pushes… Clean data becomes the moat"* (the MacroFactor case). **This fits SpaceEase exactly:** "¿Cuánto te molesta el entorno?" is honest self-report.
  - §21 peak-end: *"Ahead closes the session with a gentle 'come back tomorrow' nudge instead of guilt mechanics"*. Spotify Discover Weekly's predictable weekly delivery shows that *"the recurring, predictable delivery moment is the habit."*
- **Conflicts:**
  - §10–11 *"Variable reward magnitude"*, anticipation windows and *"50%-certainty"* reveals.
  - Loss-aversion streaks (Freecash).
  - Leaderboards and share cards.
  - Identity claims (*"You're a hardworking night owl"*), which break DESIGN §1 (*"La app habla del entorno, no de la persona"*).

**(B) omer-metin/skills-for-antigravity → `gamification-loops`.** https://github.com/omer-metin/skills-for-antigravity/tree/main/skills/gamification-loops
- **Trust:** 183★, Apache-2.0, pushed 2026-01-22. Markdown: `SKILL.md` plus `references/patterns.md`, `sharp_edges.md` and `validations.md`.
- **Install:** `npx -y skills add omer-metin/skills-for-antigravity --skill gamification-loops --agent claude-code` (command from a registry listing), or copy the folder.
- **Rules:**
  - *"Can user stop without penalty? Does user feel good after using? … Are we transparent about mechanics?"*
  - **Red-line mechanics:** *"Punishment for not engaging; FOMO for basic features; Hidden addiction mechanics; Infinite scrolling rewards; Guilt-based retention."*
  - **Overjustification:** *"External rewards can PERMANENTLY reduce intrinsic motivation"*. Safe rewards are *"INFORMATIONAL — Feedback on performance… Progress visibility"*.
  - **Streak protection:** *"Freeze… Grace period… Repair… Weekend pause"*.
- **Conflicts:** *"UNEXPECTED — Surprise bonuses"* (variable rewards); leaderboards.

**(C) tzn068/hooked-review.** https://github.com/tzn068/hooked-review
- **Trust:** 0★, MIT, Markdown.
- `references/ethics.md`: Nir Eyal's 2×2 (Facilitator, Peddler, Entertainer, **Dealer**).
- **Red lines:** *"Infinite variable rewards… Engineered dependence… Hidden mechanics… One-way manipulation… Addiction rent"*.
- *"look at the user's state when they leave."*
- Use it as a pre-ship review.

**(D) rastian/behavioral-design-skills → `references/ethics-checklist.md`.**
- **Trust:** 34★, **no license**. The repo also contains a 136 KB packaged `.skill` file and evals.
- *"The test: Would the user endorse this intervention if they understood exactly what it was doing and why?"*
- Five tests: benefit, transparency, autonomy, vulnerability, reversibility. Plus a dark-patterns list (confirmshaming, roach motel and so on).

**(E) Non-installable but on-point references for no-shame continuity:**
- **zakariaf/Hifz-Companion** `.claude/skills/domain-adab-and-religious-integrity/SKILL.md`. **Trust:** 1★, **GPL-3.0**; same author as the zakariaf a11y skill; project-specific. Quotes:
  - *"No streak-as-pressure, no broken-chain shame… Any continuity indicator is private, opt-in, and never punitive; the heat-map shows green receding to a muted neutral, never an alarming red scoreboard."*
  - *"extrinsic rewards measurably undermine intrinsic… motivation (Deci, Koestner & Ryan 1999, d ≈ −0.40)"*.
  - *"Hard news… leads with empathy, then a calm path, then the user's choice."*
  - *"Invite and inform; never command"*; *"no exclamation marks, no emoji in product copy"*; *"'your revision for today is ready'"*.
- **curiositech/port-daddy** `skills/sobriety-app-design`. **Trust:** 3★, NOASSERTION.
  - *"Offer the option to HIDE the counter. Some people find it triggering or reductive."*
  - *"'We're here when you're ready' not 'You broke your streak!'"*
- **tianze-hou/marvin** `prompts/tone.md` (1★, MIT, Chinese; an ADHD agent scaffold, *"no streaks, no shame"*):
  - Praise the concrete thing, not the person (*"拍实物不拍人"*).
  - Praise only with evidence (*"有据才拍"*).
  - Don't assert anything about empty days (*"可能是歇着，可能是做了没记——都正常"*: "maybe resting, maybe done but not logged — both normal").
  - On repeated misses, re-estimate; don't blame (*"是我的估算该校准了，不是你的问题"*: "it's my estimate that needs recalibrating, not your problem").
  - Compare only with the user's own history.
- **Onboarding:**
  - `coreyhaines31/marketingskills` `onboarding` (56.7k★, MIT): aha-moment, time-to-value and empty-state guidance is good. But it uses the *"Endowed Progress Effect — a checklist that opens at '20% done'… +40% completion"*, which is dishonest progress, so skip that part.
  - `sickn33 onboarding-psychologist` (part of a 2,687-skill mega-repo, 48.5k★): sound guardrails (*"If the product is high stakes -> optimize for confidence and reassurance, not streak pressure"*). Copy it; don't install the whole repo.
  - **Avoid `adamlyttleapps/claude-skill-app-onboarding-questionnaire`** (1,223★):
    - *"Brief pause (1-3 seconds) — even if nothing is actually loading"*.
    - *"suggest the user writes aspirational [testimonials]"*.
    - *"This creates the sunk cost that drives conversion at the paywall."*
- **curiositech adhd-design-expert** (in `curiositech/some_claude_skills`, 254★): its useful forgiving-recovery copy (*"You completed 6/7 days"*, *"'Life happens' acknowledgment"*) sits next to *"Celebrate Everything… Confetti… Streak counters"*. That shows ADHD and autistic preferences pulling in opposite directions, which is exactly why "Con detalles" must stay opt-in and granular. It also requests third-party MCP tools (21st magic, stability-ai, firecrawl).

### 3.6 UX writing ("delight" copy that stays plain)

- **content-designer/ux-writing-skill.** https://github.com/content-designer/ux-writing-skill
  - **Trust:** 248★, MIT, pushed 2026-05-26.
  - **Files:** `SKILL.md`, `references/`, `templates/` (onboarding, empty state, error). **Flagged:** `build-skill.sh`, GitHub workflows, an 18 MB demo `.mp4`, a `dist/` zip.
  - **Install:** `npx skills add content-designer/ux-writing-skill`.
  - **Rules:**
    - *"Use 40-60 characters per line maximum"*; *"7th grade reading level"*; *"active voice 85% of the time"*.
    - Success: *"Past tense, specific… `[Action] [result/benefit]`… 'Changes saved'"*.
    - Permission: *"Explain benefit before requesting permission"*.
    - Avoid *"Blame language ('invalid input')"*.
  - `cuellarfr/design-skills` (113★) bundles what looks like the same `ux-writing` skill (identical description).
- **Anthropic `design/skills/ux-copy`** (official, Apache-2.0). https://github.com/anthropics/knowledge-work-plugins/tree/main/design/skills/ux-copy
  - *"Clear… Concise… Consistent… Useful… Human"*.
  - Errors: *"What happened + Why + How to fix"*.
  - *"Success: Celebratory but not over the top"*.
  - Confirmation buttons are labelled with the action, never *"OK / Cancel"*.
  - Each output includes a *"Localization Notes"* section. That matters for es/en.
- There's no reliable Spanish UX-writing skill. `denipeduzzi/UX_Writing_denissepeduzzi` (3★, no license) and `thevenomsnake/humanization` (1★) are too thin.

---

## 4. Conflicts with a calm, neurodivergent-first design, and how to make them opt-in

| Guidance (source) | Why it conflicts | How to offer it in "Con detalles" (if at all) |
|---|---|---|
| *"Always three motion layers — primary + secondary + ambient"* (LottieFiles, CRITICAL) | Constant background motion is the top sensory complaint for autistic users and a distraction for ADHD users | Never as a default. In Con detalles, primary only plus at most one secondary beat (rule 4). Ambient motion only on the pixel scene, and auto-stopping (rule 7) |
| Breathing and floating loops at 3–6 s/cycle (LottieFiles, dylantarre) vs *"avoid… slow looping oscillations (near 0.2 Hz)"* (Emil apple-design) | 4–6 s breathing **is** 0.17–0.25 Hz, right where the vestibular warning sits | Use **discrete stepped frames with long rests** (a 2-frame twitch every 8–12 s) instead of continuous oscillation, on a small area only |
| Variable rewards, surprise bonuses, anticipation windows (bixxter §10–11, omer-metin "UNEXPECTED") | Unpredictability is aversive for many autistic users, and it's a slot-machine mechanic (hooked-review red line) | **Don't offer it.** Use a *predictable* weekly recap on a fixed day instead (rule 13) |
| Streaks, loss aversion, "streak in danger" (bixxter §9, Freecash, KaiChi888) | Shame and RSD; it corrupts honest self-report; EU DFA wording | **Don't offer streaks.** If you add any continuity view: private, opt-in, hideable, no reset-to-zero, and muted neutral rather than red (rule 11) |
| Leaderboards and share cards (bixxter, omer-metin) | Social comparison; privacy (DESIGN §8: the employer has no access) | Don't offer |
| Confetti, particles, camera shake, *"Celebrate everything"* (curiositech ADHD, LottieFiles, KaiChi888) | Flashing and motion risk (WCAG 2.3.1); sudden stimulation | Not offered. The single "signature" success is the pixel wave settling (rule 4) |
| Error shake ±10–15 px (LottieFiles), *"Shake a disabled button"* (detail.design) | *"Errores sin culpa ni alarma"* (DESIGN §2); vestibular | Never. Errors stay a static message plus colour **and** icon |
| Press squash on everything (`physics-active-state`, pressto), haptic on every press (pressto `globalHandlers`) | DESIGN §5 *"sin 'aplastar' el botón"*; haptic spam | Rows: background change (as now). In Con detalles buttons may use 0.98 scale at 100–120 ms. Haptics only on commits |
| Sound on navigation, hover, transitions ("whoosh"), looping "processing" tones (ui-sound-design, clawfu) | Uninvited sound; sensory load | Never. Only ≤ 3 sounds, all on user-initiated commits (rule 8) |
| `playsInSilentMode: true` (the expo-audio default) | Breaks the user's explicit silence | Always override to `false` (rule 9) |
| *"Endowed progress"* (corey), fake loading (adamlyttle), Zeigarnik pressure (Owl, userinterface-wiki) | Dishonest; DESIGN §2 *"Resultados honestos"* | Never. Progress bars show real steps only |
| Identity claims (*"You're a… night owl"*, bixxter §6) | DESIGN §1: talk about the environment, not the person | Rephrase as environment facts: *"Este espacio suele molestarte menos por la tarde."* |
| `easing-exit-ease-in` (userinterface-wiki), *"Exit=ease-in"* (LottieFiles) | Expo: *"Never `ease-in` on UI"*; DESIGN §5 | Keep ease-out exits, 20–30% shorter than entrances |
| *"If a neurotypical person finds it 'too much,' it's probably right for ADHD"* (curiositech) | Directly opposed to autistic sensory needs | This is the reason for **granular toggles**: Movimiento, Sonido, Vibración and Progreso are separate switches inside Con detalles |

---

## 5. Rules and recipes for "Con detalles" (a draft for a new DESIGN.md section)

Proposed structure: **Experiencia: Tranquila (default) / Con detalles**. Inside "Con detalles" there are four independent switches: **Movimiento**, **Sonido**, **Vibración** and **Progreso**.
- Switching to "Con detalles" turns on Movimiento only. Sound and haptics each need their own tap.
- iOS Reduce Motion (live), or the app's own "Solo fundidos" setting, always overrides Movimiento. It also mutes Sonido unless the user turned Sonido on explicitly after enabling Reduce Motion.
- Every detail has a static equivalent. Nothing new is communicated *only* by motion, sound or vibration.

1. **Frequency still gates everything.** Con detalles adds motion only to *rare* moments: finishing a trial, the first save, the weekly recap, the end of onboarding. Tabs, option picks and the keyboard stay unanimated. *Sources:* Expo/Emil frequency gate; detail.design #15; draftbit `MOTION_INTENSITY` (Tranquila ≈ 2, Con detalles ≈ 5).
2. **Selection feedback.** The option row changes background and icon immediately (as today). In Con detalles the background cross-fades over ≤ 150 ms with `EASE_OUT`, with no scale on rows; buttons may scale to 0.98 over 100–120 ms. With Vibración on, fire `selectionAsync()` only for stepped controls (the 5-point "¿Cuánto te molesta?" buttons), on press-in, once. *Sources:* Expo RECIPES "Press feedback" and haptics table; enzomanuelmangano (0.95–0.97 is the upper bound); DESIGN §5.
3. **Step-progress indicator.** A thin bar under the header, never dots; real steps only, no head start. The fill is an absolutely positioned child animated with `withTiming(…, { duration: 250, easing: EASE_IN_OUT })`; under reduced motion it jumps. Optionally, in Con detalles the bar's end cap can be a 2×2 "pixel" that steps (not slides) to the next cell, with `steps()`. *Sources:* Expo RECIPES tab indicator; draftbit value-first onboarding; corey "endowed progress" rejected.
4. **The signature success moment (one per product).** When a trial is saved, or when it *"Ayudó"*, the pixel monitor's wave **settles into a flat line**: 3–4 pre-rendered frames from `draw_icon.py` at about 120–150 ms each, under 600 ms in total, played once.
   - Lead channel: the visual. Supporting channels: `notificationAsync(Success)` on the frame where the line goes flat (same frame, Apple *Causality*), and, if Sonido is on, a soft two-note rise starting on that frame.
   - No overshoot above 5%, no confetti, no particles.
   - Under Reduce Motion: show the final flat-line frame plus text, and keep the haptic if Vibración is on.
   - *Sources:* jal-co *"signature moment"*; KaiChi888 *"single lead channel"* and *"coherent alternate timeline"*; LottieFiles overshoot budget (success 5–10%, capped lower here); Expo/Apple same-frame rule; `draw_icon.py`.
5. **Loading and scanning (photo or audio analysis).**
   - Under 100 ms: nothing.
   - Over 200 ms: an inline indicator, shown for at least 500 ms.
   - 1–10 s: words (*"Revisando la foto en el teléfono"*).
   - Over 10 s: real progress and a "Detener" button.
   - In Con detalles: a stepped pixel **scan line** sweeps the pixelated preview with `steps(8)` at about 1.2 s per pass, at most 3 passes, then stays static with the text (WCAG 2.2.2 and SWM *"cap iteration count"*).
   - No full-screen shimmer, no spinner blink.
   - *Sources:* Owl `loading-states`; dylantarre `loading-states`; SWM Reanimated CSS (no Reduce Motion support, so gate it manually); Expo native-slop #19.
6. **List and marker entrances (photo findings).** Only on first mount of content the user asked for, never inside FlatList rows. Each marker fades over 200 ms from `scale 0.97`, never 0, with a 30–40 ms stagger and a total of ≤ 300 ms (mobile budgets about 30% under web). The VoiceOver list is rendered without delay. *Sources:* Expo RECIPES list entrances; LottieFiles (micro cascade, total < 500 ms, mobile −30%); draftbit (≤ 400 ms total, first mount only).
7. **Idle animation of the pixel scene.** Off in Tranquila. In Con detalles:
   - A **stepped 2-frame "twitch"** on one small layer (a plant leaf moves 1 px on the 32 grid, or the screen wave flickers): about 300 ms per frame, then a rest of 8–12 s.
   - No continuous breathing near 0.2 Hz.
   - It stops after 5 s of activity, or offers a visible pause. It also pauses when the screen loses focus or the app is backgrounded.
   - Frames are pre-scaled with `Image.NEAREST` at integer factors and played either with `steps()` (Reanimated CSS) or as an animated WebP in expo-image with `autoplay={false}` when it shouldn't play.
   - *Sources:* pixel-art-mastery (`idleFrames [0,0,1,1]`, 300 ms; integer NEAREST); Emil apple-design §14 (0.2 Hz); LottieFiles (*"ambient… 10-20% of primary"*, *"pause controls for animations >5 s"*); impeccable (*"Any nonessential loop must stop when offscreen"*); WCAG 2.2.2 via Owl motion-sensitivity; expo-image docs (`autoplay` default `true`; no resampling prop).
8. **Sound palette: the "butler".** At most **3 sounds**, all user-initiated, in one key:
   - (a) **save/confirm:** a soft mallet click (filtered noise, about 1.2 kHz, 60 ms);
   - (b) **"ayudó"/success:** a two-note rise (for example a major third from about 520 Hz, 120 ms notes, 80 ms gap, triangle wave);
   - (c) **optional "settle"** earcon under the signature moment.
   - **Levels:** press about −27 dBFS peak, success ≤ −24 dBFS, nothing louder than −20 dBFS.
   - **Character:** fundamentals in about 300–900 Hz, low-pass filtered; no sustained energy in 2–5 kHz.
   - **Never** on navigation, selection, typing, scroll, launch or errors. Debounce ≥ 90 ms; throttle to one sound per 200 ms.
   - *Sources:* jal-co `ux-sound` (butler, ladder, ≤ 3 sounds, 2–5 kHz, 90 ms); ui-sound-design recipes (soft click, gentle ding, major-third success, "warmer" = sine/triangle with a lower cutoff); clawfu (tonal center, calm = soft attack and filtered, 200 ms throttle).
9. **Sound plumbing in Expo Go.**
   - Synthesize and A/B the sounds in `ui-sound-design`'s HTML preview on the PC, then export WAV (mono, 44.1 kHz, 16-bit, peak ≤ −1 dBFS).
   - Bundle them as assets and `preload()` them at module scope with expo-audio.
   - Call `setAudioModeAsync({ playsInSilentMode: false, interruptionMode: 'mixWithOthers' })`. The silent switch then mutes the app, and the user's music or white noise is never paused or ducked.
   - Read the mute flag before every play. Put the Sonido switch on the same screen where sound is first heard.
   - *Sources:* expo-audio SDK 58 docs (defaults `playsInSilentMode: true`, `interruptionMode: 'mixWithOthers'`; `preload` at module scope); SWM audio (`ambient` respects the silent switch); clawfu file spec; jal-co §6–7.
10. **Pairing sound and haptics.**
    - Same frame as the visual (*"Even 100 ms delay breaks the illusion"*).
    - One haptic per user action; never on entrances, scroll or navigation.
    - Match weight across channels: soft sound with `Light` impact; success sound with `notificationAsync(Success)`.
    - Errors: visual only by default; with Vibración on, at most `notificationAsync(Warning)` and no sound (DESIGN: *"sin alarma"*).
    - A secondary beat, if any, comes 80–180 ms after the primary.
    - Every channel must stand on its own when the others are off.
    - *Sources:* Apple Causality/Harmony/Utility via Emil apple-design §13, Axiom and johnrogers; Expo haptics rules; KaiChi888 matrix and rhythm; draftbit (*"Never on plain taps or navigation"*).
11. **Retention without streaks.**
    - The loop is the **trial itself**: a finite unit with an end (25 or 50 min, one adjustment).
    - No counters that reset. If **Progreso** is on, the app may show a private history ("Ajustes que probaste este mes") that can be hidden, never turns red, and **never penalizes a break**.
    - Pre-ship checks: *"Can the user stop without penalty?"* and the EU DFA test *"does it penalise taking a break?"*.
    - *Sources:* bixxter §5, §8 and the decision guide (honest self-report, so delete shame mechanics); omer-metin red lines; zakariaf Hifz (*"private, opt-in, never punitive… muted neutral, never… red"*); sobriety-app-design (*"Offer the option to HIDE the counter"*); DESIGN §6.
12. **Competence feedback, not badges.** The only "reward" is informational and about the environment: *"Lo probaste 3 veces aquí; ayudó en 2. Todavía no es seguro."* This is already DESIGN §2. In Con detalles it can arrive with the signature moment from rule 4. No XP, no badges, no levels, and no identity statements about the person. *Sources:* omer-metin (*"Rewards that don't crowd out: INFORMATIONAL"*); bixxter §6 (*"competence feedback, not badge theater"*); Deci, Koestner & Ryan 1999 via Hifz.
13. **Predictable cadence instead of variable rewards.** Offer an opt-in weekly recap on a **fixed day the user picks**: at most 3 items, revealed in a fixed order (stepped, one per beat, under Movimiento), with the same structure every week. No surprises and no "unlock". *Sources:* bixxter (Spotify Discover Weekly, *"the recurring, predictable delivery moment is the habit"*), with the variable-reward parts rejected; hooked-review (*"Infinite variable rewards"* is a red line); DESIGN §6 (reminders only when asked for).
14. **Peak-end without pressure.** Every trial ends on a calm completion screen, never on a settings or setup screen: *"Guardado. Puedes volver cuando quieras."* After a gap there is no "llevas N días sin…", only *"Tu próxima prueba está lista cuando quieras."* *Sources:* Owl `peak-end-rule` (*"Never end on an administrative or transitional screen"*); bixxter §21 (Ahead's *"gentle 'come back tomorrow'"*); sobriety (*"We're here when you're ready"*); DESIGN §6.
15. **Encouraging copy, still plain.**
    - Success is past tense and specific: *"Ajuste guardado"*, *"Prueba terminada"*.
    - Praise the thing, never the person, and only with evidence.
    - Empty or missed days: *"Puede que hayas descansado o que no lo hayas anotado. Las dos cosas están bien."*
    - Hard news order: empathy, then a calm path, then the user's choice.
    - Invitations, not commands: *"Tu prueba de hoy está lista"*; never "debes", "no olvides" or "no rompas".
    - No exclamation marks or emoji. In Con detalles the tone may be warmer, not louder.
    - *Sources:* content-designer `ux-writing` (`[Action] [result]`, 40–60 characters per line); Anthropic `ux-copy` (*"Celebratory but not over the top"*; localization notes); Marvin `tone.md` (*"拍实物不拍人"*, *"有据才拍"*, empty-day rule); Hifz (*"empathy, then a calm path, then the user's choice"*; no exclamation marks or emoji); Owl `interfaces-that-feel` (*"Success | Warm and brief"*).

**Bonus (motionless delight):** a real, verifiable detail in the pixel window, for example the sky tint following the device's time of day, rendered as a static frame. *Source:* detail.design easter-egg #4 (*"Embed a real detail where people look closely"*).

---

## 6. Override block for `apps/mobile/CLAUDE.md` (add to the one in the first report)

```md
## "Con detalles" mode (overrides any skill default; DESIGN.md is the source of truth)
- Two experiences: Tranquila (default) and Con detalles, with separate switches for Movimiento / Sonido /
  Vibración / Progreso. Sound and haptics are off until switched on individually. iOS Reduce Motion or the
  in-app "Solo fundidos" setting overrides Movimiento and mutes Sonido unless Sonido was explicitly enabled after it.
- Every detail has a static, text-or-icon equivalent. No information lives only in motion, sound or vibration.
- Con detalles never animates high-frequency UI (tabs, option picks, keyboard). Delight is only for: trial
  saved/finished, first save, end of onboarding, weekly recap.
- Signature moment = the pixel monitor wave settling flat (3–4 stepped frames from draw_icon.py, <600 ms, once).
  No confetti, particles, shake, parallax, overshoot >5%, or continuous loops near 0.2 Hz. Idle loops stop
  within 5 s or have a pause, and stop when offscreen or backgrounded.
- Pixel frames are pre-scaled with Image.NEAREST at integer factors (expo-image has no nearest-neighbour option).
  Reanimated CSS animations (including steps()) ignore Reduce Motion: gate them manually; cap iterations.
- Sound: max 3 bundled WAV/M4A sounds, user-initiated only, one key, ≤ −20 dBFS peak (press ≈ −27),
  fundamentals 300–900 Hz, low-passed, nothing sustained in 2–5 kHz, debounce ≥ 90 ms. expo-audio with
  setAudioModeAsync({ playsInSilentMode: false, interruptionMode: 'mixWithOthers' }). Never on navigation,
  selection, typing, scroll, launch or errors.
- Haptics: same frame as the visual, one per user action, never on entrances, scroll or navigation, never the only signal.
- No streaks, XP, badges, leaderboards, variable or surprise rewards, loss framing, fake progress or fake
  loading. History is private, opt-in, hideable, never red, never penalizes breaks.
- Do not install Rive, react-native-audio-api or Pulsar (they need a dev build; plan B is Expo Go).
```

---

## 7. Security and trust summary (new candidates)

| Candidate | Trust | Code / network it brings |
|---|---|---|
| jal-co `ux-sound` | 6★, MIT, individual | `scripts/transients.mjs`, `trim-to-transient.sh` (optional); the GENERATE route mentions a paid API (opt-in) |
| dannyjpwilliams `ui-sound-design` | 43★, MIT, individual | `tools/analyze-sound.mjs` (40 KB Node, zero-dependency, optional; ffmpeg for non-WAV input) |
| LottieFiles `motion-design` | 2.5k★, MIT, org | None (Markdown only) |
| Owl-Listener designer-skills / inclusive-design-skills | 3.1k★ / 107★, MIT | Skills are Markdown; repo-maintenance scripts (Python/shell) aren't run by the skills |
| content-designer `ux-writing` | 248★, MIT | `build-skill.sh`, CI workflows, 18 MB demo video, dist zip (not run by the skill) |
| Anthropic `ux-copy` | Official, Apache-2.0 | None if copied alone; the full `design` plugin adds 9 MCP connectors |
| omer-metin `gamification-loops` | 183★, Apache-2.0 | None |
| tzn068 `hooked-review` | 0★, MIT | None |
| bixxter `app-growth-design` | 3★, MIT | Repo has `bin/install.mjs` plus a video/subtitle pipeline; `skill/` is Markdown |
| draftbit `mobile-taste-skill` | 8★, org, license unclear | None; older Reanimated idioms |
| enzomanuelmangano / KaiChi888 / detaildotdesign / rastian | 10★ / 2★ / 68★ / 34★, **no license** | None; read-only use advised (no licence to redistribute) |
| zakariaf Hifz-Companion | 1★, **GPL-3.0** | Project-internal skill; quote ideas, don't copy |
| curiositech `adhd-design-expert` | 254★ repo, MIT | `allowed-tools` requests 21st-magic, stability-ai and firecrawl MCPs |
| clawfu | 150★, MIT, **archived** | References the `@clawfu/mcp-skills` MCP server |
| SoundWeaver | 0★, MIT | 1.26 MB inline base64, Python generator, `push_to_github.sh` |
| adamlyttleapps questionnaire onboarding | 1.2k★, MIT | None, but **dark-pattern content** |

Downloaded copies: `C:/Users/kiki7/AppData/Local/Temp/claude/c--Users-kiki7-OneDrive-Desktop-AIChallenge/f555c6c5-db13-4bc1-940e-7b29d63cf946/scratchpad/dl2/` (subfolders `sound/`, `haptics/`, `lottiefiles/`, `rn/`, `owl/`, `owl-incl/`, `dylan/`, `ret/`, `copy/`, `late/`, `swm-audio/`, `game/`).
