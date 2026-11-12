# Provider: manual (copy-paste prompts)

No API, no install. Takewright plans, checks and writes the prompts; the user pastes them into a web app, downloads the results, and Takewright reviews and edits them.

## Prompt pack format (one block per shot)

```
SHOT 2 · 0:05–0:10 · 9:16 · 5 s · image-to-video
Upload: photo_living_room.jpg as the first frame
Prompt (EN): …
Prompt (ZH, for Chinese-native apps): …
Settings: 720p draft first; audio on/off; seed if available
Check after render: walls stay straight, no new furniture, ends on a calm hold
```

Always include: platform-ready prompt, settings, what to upload and in which role, and the 2–3 QC points that matter for that shot. Keep each pack readable on a phone.

## Platform notes (re-check current limits in the app)
- **Jimeng / Dreamina (ByteDance, Seedance):** Chinese prompts work very well. Reference files are named in the prompt by role — for example `@图片1 作为首帧`, `参考 @视频1 的运镜` (Jimeng's `@` syntax) — and every uploaded file needs a stated job. Realistic human-face uploads may be blocked. Time-sliced prompts (`0–3秒：…`) help longer clips.
- **Kling:** needs explicit motion; strict wording filter — remove brand/IP names first.
- **Hailuo (MiniMax):** short, concrete prompts; one action per clip.
- **Higgsfield:** good camera-move presets; keep the prompt to subject + action + light and choose the camera preset in the UI.
- **Runway:** concise descriptive prompts; use its reference/keyframe features for consistency.
- **Veo (Google):** English preferred; describe sound and dialogue explicitly.

## After the user renders
Ask them to drop the downloaded files into `./takewright-output/{date}/`, then run QC (`craft/qc.md`) and editing (`assembly/editing.md`) exactly as with an API route. Log prompts and ratings the same way so the next pack improves.
