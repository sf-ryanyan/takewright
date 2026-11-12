# Prompting

## Formula (video and image)
`[Subject] + [Action] + [Setting] + [Camera] + [Lighting] + [Style] + [Sound (video)] + [Constraints]`

- **Subject:** specific nouns, materials, colours ("a two-storey modern house with white board-and-batten siding").
- **Action:** one clear motion with a visible end state ("she sets the cup down; the steam keeps rising").
- **Setting:** place, time, weather, story moment.
- **Camera:** shot size + angle + **one** move — slow dolly in, push in, pull back, pan, tilt, orbit, crane up, lateral track, static tripod, handheld follow, top-down drone.
- **Lighting:** a physical source — golden hour, soft overcast, window light, warm practical lamps, blue hour, high key, low key.
- **Style:** a look that defines the shot (photoreal, 35 mm film look, anime, ink painting…) — not empty praise.
- **Sound:** always state it. No music → `Sound: no score, natural ambience only.` With music → mood + instruments. Name signature sounds (rain, footsteps, door click).
- **Constraints:** what must not change or appear ("no text, no watermark", "the room stays the same").

## Structure rules
- One main action and one camera move per shot.
- Clips ≥ 8 s: time slices — `0–3s: … / 3–6s: … / 6–10s: …` — one beat per slice.
- Realism: for photoreal people, props and materials add 1–2 small natural imperfections (worn edge, scuff, fabric crease, real skin texture). Too perfect reads as fake.
- Endings: finish on a calm hold ("the final frame holds for one second"). No explosions, blinding light or victory poses unless the brief needs them.
- No text, logos, prices, phone numbers or signs inside generated visuals — add typography in editing.
- No more than 2 people interacting per shot; avoid close-up hands doing fine tasks.
- Consistency across shots: reuse the same **Look Card** wording (palette, lens, light, era) and the same reference images.
- Respect each model's prompt-length limit (provider file). Never silently truncate.
- Image prompts: describe composition (wide angle, rule of thirds, eye level) and leave negative space where titles will go.
- Prompt language: English by default. Chinese-native models (Seedance/Jimeng) handle Chinese very well — use Chinese when the scene is Chinese or has Chinese dialogue.

## Anti-slop rewrite (run before every submission)
Empty praise words do not improve output; physical detail does.

| Weak | Stronger |
|---|---|
| cinematic, epic, beautiful, stunning | soft side backlight through tall windows, slow dolly-in, warm oak floor reflections |
| luxury, high-end, premium | 40% empty frame, travertine and walnut, a narrow warm light sweep, very slow camera |
| make it move naturally | the curtain drifts once in the breeze, sunlight slides across the floor, the final frame holds |
| dynamic, energetic | a fast lateral track beside the runner, footfalls on wet asphalt, motion blur on the background |
| 4K, ultra detailed, masterpiece, best quality | delete — set resolution with parameters |
| use this video as style | the reference video sets only the camera rhythm; do not copy its people or background |

Keep genre and style labels that define the look (noir, documentary, anime, ink painting). Do not replace the user's chosen style with a stock look.

## Example
Weak: "Beautiful cinematic luxury kitchen, 4K."
Strong: "Wide eye-level shot of a white-oak kitchen with a honed marble island, late-afternoon window light from the left. Slow lateral track right to left along the island. A ceramic bowl of lemons, a faint scratch on the brass faucet. Sound: no score, quiet room tone, distant birds. The layout stays exactly the same; no text, no people; final frame holds for one second."
