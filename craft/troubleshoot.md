# Troubleshooting & retake protocol

When a take is weak or unusable, diagnose before retrying. Never re-roll the same prompt blindly more than once; never retry a paid task without the user's OK. Treat causes as likely, not proven — models vary run to run.

## Diagnostic table
| Symptom | Likely cause | First repair |
|---|---|---|
| Face, product or building changes | Image-to-video prompt re-described static details, or too much motion | Remove static description; add preservation locks; reduce motion |
| Camera jumps or wobbles | Several moves, or no endpoint | One move with start and end; tripod / dolly wording |
| Generic, flat look | Empty style words, weak light | Physical light source, material, lens and grade (`craft/aesthetics.md`) |
| Nothing moves | Static prompt | One actor + verb + visible end state + time cue |
| Story garbled, lines wrong | Too many beats for the duration | Split into shorter clips; ≥3 s per beat |
| Model invents extra content | Long duration, little content | Shorten the clip or add one concrete beat |
| Warped hands | Fine hand action in frame | Simplify the action; keep hands out of focus or frame |
| Text, signs, logos garbled | Model asked to render text | Remove text from the prompt; add it in editing; keep real logos static |
| Bending or melting architecture | Orbit or fast camera around straight lines; extreme wide lens | Slow linear push or lateral move; "straight vertical lines"; 24–35 mm feel |
| Flicker or boiling textures | Busy fine patterns, low resolution, long clip | Simplify surfaces; raise resolution; shorten |
| Unwanted music | No sound line | "no score, natural ambience only" |
| Poor lip sync | Moving head or camera, long line, unassigned speaker | Lock framing, shorten the line, one speaker; use a lip-sync capability |
| Audio reference ignored | Competing audio in reference video; no visual beat mapped | Mute competing audio; tie one visible event to the beat |
| Character drifts between shots | No shared reference or Look Card | Reuse the same character images and Look Card wording in every shot |
| Continuation looks different | No anchor frame | Use the previous clip's last frame as the next first frame; change one variable |
| Wrong ratio or cropped subject | Ratio not set, or image ratio differs | Set ratio explicitly; generate the key frame in the target ratio |
| Task rejected or blocked | Real-person face, protected IP or brand, unsafe wording | Rewrite as original, safe description — no evasion tricks |
| HTTP 422 / invalid parameter | Field name or value not supported | Read the provider's schema / `--help`; fix the field |

## Retake protocol
1. Name the failed criterion and what is still good in the take.
2. Change **one** variable only: camera, light, motion, reference role, duration or model.
3. Prefer cheap repairs: edit/extend the good take, fix in editing (text, colour, sound, trim), or re-render only the failing shot as a draft.
4. Conservative retry pattern:
   `[reference role]. Preserve [identity/product/room] exactly. One visible action: [verb + result]. Camera: [one move]. Light: [physical source]. Sound: [cue]. Do not change: [locks].`
5. Same failure twice → escalate: split the shot, reduce characters, simplify hands and faces, switch mode (text → image-to-video), or try another model family. If the shot only needs gentle motion on a real photo, use `assemble.py stills` (free) instead of another paid take.
6. Log the cause and the fix in the prompt log.

## Repair in editing instead of re-rendering
| Problem | Edit fix (`assembly/editing.md`) |
|---|---|
| Bad last second | trim |
| Wrong ratio but subject fits | crop / blurred-background pad |
| Colour mismatch between shots | grade in an editor; regenerate only if the light direction is wrong |
| Missing or wrong text | remove from prompt; add captions/titles in the edit |
| Loudness or music issues | mix in the edit |
