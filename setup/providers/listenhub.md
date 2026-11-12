# Provider: ListenHub

ListenHub (by MarsWave) renders video (Seedance 2.5 / 2.0, HappyHorse, PixVerse), images (Gemini image models), TTS, voice cloning, music and explainer videos through one CLI. Official agent skills (MIT): github.com/marswaveai/skills.

## Install → Sign in → Verify

**Install** (needs Node.js 20+):
```bash
npm install -g @marswave/listenhub-cli@latest
```
Windows: if PowerShell says scripts are disabled, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, then install again.

**Sign in — two modes (both can be active):**
- **API key** (needed for PixVerse; good for automation; key from ListenHub → Settings → API Keys, paid plan): `listenhub openapi config set-key` — it **prompts** for the key; do not pass the key as an argument. Commands then use `listenhub openapi <group>`.
- **OAuth** (needed for music; richer video-edit audio options): `listenhub auth login` opens the browser. If the user signs in with Google, they must choose the Google account that owns their ListenHub plan. Commands use `listenhub <group>`.

**Verify (free):**
```bash
listenhub --version
listenhub openapi config show --json     # API-key mode
listenhub auth status --json             # OAuth mode
listenhub openapi video estimate --model doubao-seedance-2-fast --resolution 720p --duration 5 --json
```

`--help` is the source of truth: before the first use of a command in a session run `<prefix> <group> <action> --help` once; follow it if it differs from this file; if a needed flag is missing, update the CLI.

Windows/Git Bash: do not depend on `jq`; pass `--json` and read the output directly. Single-quote prompts. Download results with `curl -L -o`.

## Prefix per capability
`$V` = `listenhub openapi video` (API key) or `listenhub video` (OAuth). Same pattern for `image`, `tts`, `speakers`, `voice-clone`, `explainer`. **PixVerse is API-key only. Music is OAuth only.**

## Model chooser (video)

| Need | Model | Key limits |
|---|---|---|
| Best general quality, characters, multi-reference, edit/extend, draft → final | **Seedance 2.5** `doubao-seedance-2-5` | 4–30 s or `-1` auto; 480p/720p/1080p (draft 480p, final 1080p); ≤30 ref images, ≤10 ref videos (total ≤30 s), ≤10 ref audios (total ≤30 s, audio-only allowed); prompt ≤5000 chars |
| First + last frame transition | Seedance 2.0 `doubao-seedance-2-pro` / `doubao-seedance-2-fast` | 4–15 s; Pro 480p/720p/1080p, Fast 480p/720p; ratios 16:9, 9:16, 1:1, 4:3, 3:4, 21:9; prompt ≤3000 |
| ≤9 ref images with `[Image N]` syntax; edit an existing video | HappyHorse `happyhorse` (CLI default) | 3–15 s; 720p/1080p; ratios 16:9, 9:16, 1:1, 4:3, 3:4, 4:5, 5:4; prompt ≤2500 Chinese / ≤5000 other |
| Lip sync, mimic, restyle, fusion, multi-keyframe transition, auto ad (20/30/60 s) | **PixVerse** (API key) | 1–60 s; 360p–1080p; media must be public URLs or prior PixVerse task/video IDs |

Rules: Seedance 2.5 first/last frame, edit and extend need `--ratio adaptive`; edit needs `--duration -1`; frame mode cannot mix with reference mode. Remote image URLs on Seedance need `--reference-image-meta WIDTHxHEIGHT[:SIZE]`; reference video/audio need real `--reference-video-meta WIDTHxHEIGHT:DUR:FPS:SIZE` / `--reference-audio-meta DUR:SIZE` (measure with `python scripts/assemble.py probe <file>`; never invent). Video MP4/MOV ≤200 MB; audio WAV/MP3 ≤15 MB. Never send HappyHorse's `--audio-setting` to Seedance. Rate limit 5 requests/min.

## Commands

**Estimate / create / check**
```bash
$V estimate --model doubao-seedance-2-5 --resolution 720p --ratio 9:16 --duration 5 --json
$V create --model doubao-seedance-2-5 --prompt '...' --resolution 720p --ratio 9:16 --duration 5 --no-wait --json
$V get <taskId> --json       # status pending → generating → uploading → success | failed; fields videoUrl, seed, creditCharged
$V list --json
```
Poll `get` every ~15 s in the background; stop after ~20 min and tell the user to check later.

**Seedance 2.5 draft → final** (two separate charges; the final must not repeat prompt/assets/resolution/ratio/duration/seed/--draft)
```bash
$V create --model doubao-seedance-2-5 --prompt '...' --draft --resolution 480p --ratio 9:16 --duration 5 --request-id '<uuid>' --no-wait --json
$V estimate --model doubao-seedance-2-5 --draft-task-id '<draftTaskId>' --json
$V create --model doubao-seedance-2-5 --draft-task-id '<draftTaskId>' --request-id '<new-uuid>' --no-wait --json
```
Drafts expire after 14 days; finalize only a successful draft. A network retry reuses the same `--request-id`; a new ID is a new charge.

**Image-to-video**
```bash
$V create --model doubao-seedance-2-5 --prompt '...' --first-frame ./key.png --ratio adaptive --resolution 720p --duration 5 --no-wait --json
$V create --model doubao-seedance-2-pro --prompt '...' --first-frame ./a.png --last-frame ./b.png --resolution 720p --ratio 9:16 --duration 8 --no-wait --json
```

**References (style / character consistency)**
```bash
$V create --model doubao-seedance-2-5 --prompt '...' --omni-reference-task-type reference --reference-image ./char.png --reference-image ./look.png --resolution 720p --ratio 9:16 --duration 8 --no-wait --json
$V create --model happyhorse --prompt '[Image 1] walks into the sunlit room' --reference-image ./ref1.png --resolution 1080p --ratio 9:16 --duration 5 --no-wait --json
```

**Edit / extend (Seedance 2.5)**
```bash
$V create --model doubao-seedance-2-5 --prompt 'Replace the sky with a clear sunset; keep everything else unchanged' --omni-reference-task-type edit --ratio adaptive --duration -1 --resolution 720p --reference-video ./in.mp4 --reference-video-meta 1080x1920:6:30:9000000 --no-wait --json
```
Extend: `--omni-reference-task-type extend --ratio adaptive` plus a supported output duration. Add `--no-generate-audio` (Seedance) only if the user wants silence.

**PixVerse** (`listenhub openapi video pixverse …`; uses `--quality` and `--aspect-ratio`)
```bash
P='listenhub openapi video pixverse'
$P estimate --capability text_to_video --model pixverse --quality 720p --duration 5 --json
$P generate --capability text_to_video --model pixverse --prompt '...' --quality 720p --aspect-ratio 9:16 --duration 5 --no-wait --json
$P generate --capability image_to_video --model pixverse --prompt '...' --image 'https://….png' --quality 720p --aspect-ratio 9:16 --duration 5 --no-wait --json
$P generate --capability lip_sync --source-video-id '<id>' --audio 'https://….mp3' --quality 720p --no-wait --json
# Lip sync from TTS: nested JSON only — do NOT use --lip-sync-* flags (known CLI bug) and do NOT also pass --audio
$P generate --capability lip_sync --source-task-id '<taskId>' --pixverse-json '{"tts":{"speakerId":"<speakerId>","content":"..."}}' --quality 720p --no-wait --json
# Auto ad: quality 720p/1080p only; duration 20/30/60 only; promo_mix needs ≥4 images
$P generate --capability agent --agent-type promo_mix --prompt '...' --image 'https://1' --image 'https://2' --image 'https://3' --image 'https://4' --quality 1080p --duration 30 --no-wait --json
```
Getting public URLs for PixVerse: reuse URLs returned by earlier tasks (`videoUrl` from `video get`, the image URL from `image create`) or a PixVerse task/video ID. If the user wants to use their own local file, ask where they want it hosted (their own storage/website); never upload a user's file to a random public host without explicit consent.

Other PixVerse rules: `mimic` = 1 image + 1 video (5–30 s), quality locked 720p. `fusion` refs go in `--pixverse-json '{"imageReferences":[{"type":"subject|background","imageUrl":"…","refName":"cat"}]}'` (1–8; no top-level `--image`; prompt uses `@refName`). `multi_transition` keyframes go in `--pixverse-json '{"multiTransition":[{"imageUrl":"…","duration":3,"prompt":"…"}]}'` (2–7; default 360p). `restyle` = `--source-video-id` (or `--source-task-id`) + `--restyle-id`. Lip-sync audio 5–60 s. For `agent` estimates add `--agent-type`.

**Image** (`gemini-3-pro-image` quality; `gemini-3.1-flash-image` faster/cheaper, adds 1:4, 4:1, 1:8, 8:1)
```bash
listenhub openapi image create --prompt '...' --model gemini-3-pro-image --lang en --aspect-ratio 9:16 --size 2K --json
# --reference ./style.png (repeatable); sizes 1K/2K/4K; ratios 16:9, 1:1, 9:16, 2:3, 3:2, 3:4, 4:3, 21:9
```

**Voiceover / TTS**
```bash
listenhub openapi speakers list --lang en --json      # fields: name, speakerId, gender, demoAudioUrl
listenhub openapi tts create --text '...' --mode direct --speaker '<name>' --lang en --json
listenhub openapi tts create --text 'A: ...\nB: ...' --mode smart --speaker '<n1>' --speaker '<n2>' --lang en --no-wait --json
```
Optional `--speed 0.5–2.0` (default 1.0). Long text: write to a file and pass `--text "$(cat file)"`.

**Voice clone** (consent required; confirming may cost credits beyond plan quota)
```bash
listenhub voice-clone create --file ./voice.m4a --lang en --json     # 1–6 clean recordings: repeat --file
listenhub voice-clone get <taskId> --json
listenhub voice-clone confirm --task-id <taskId> --name '<name>' --gender <male|female> --json   # --use-credits only after the user agrees
listenhub voice-clone speakers --json                                  # use with tts --speaker-id <id>
```
API-key users: `listenhub openapi voice-clone create --consent …` (check `--help`).

**Music** (OAuth; models auto / mureka-7.6 / mureka-8 / mureka-9 / mureka-o2)
```bash
listenhub music instrumental --prompt 'warm acoustic, light piano, 30s, no vocals' --json
listenhub music soundtrack --video ./final.mp4 --prompt 'calm, modern' --json     # or --image
```

**Explainer video**
```bash
listenhub openapi explainer create --query '...' --mode info --lang en --speaker '<name>' --aspect-ratio 9:16 --image-size 2K --timeout 600 --json
```

Exit codes: 0 ok · 1 error (show stderr) · 2 auth (re-login / `listenhub openapi config show`) · 3 timeout (check later with `get`).
