# Genre: explainer, education, market update, service intro

## Two routes
- **Built-in explainer** (fastest): providers with an explainer capability (e.g. ListenHub `explainer create`) generate narration + AI visuals from a topic, URL or text. Review the script first (`--skip-audio` or script-only mode), then render.
- **Composed explainer** (most control): write the script → voiceover (TTS or the user's voice) → one visual per idea (image or short image-to-video) → assemble with captions.

## Script rules
- One idea per 5–8 s; total 45–90 s for social, 2–3 min for YouTube.
- Hook with the question or the surprising number in the first sentence.
- Plain words; numbers from the user's sources only; cite sources in the caption or description.
- Narration pace: ~2.5 English words or ~4 Chinese characters per second — time the visuals to the voiceover, not the other way round.

## Visual rules
- Diagrams and charts: generate as images with an image model that renders text accurately, or build them as graphics in the edit. Never ask a video model to render numbers.
- Keep motion gentle (slow push, parallax) so viewers can read.
- Consistent Look Card across all visuals.

## Assembly
Voiceover first → place visuals to the narration → captions from the script (SRT) → light music bed ducked under the voice (`assembly/editing.md`).
