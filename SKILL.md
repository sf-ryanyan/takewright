---
name: takewright
description: Director-grade AI video production for any provider — cloud APIs (ListenHub, fal, MuAPI, others), local GPU (ComfyUI) or copy-paste prompts. Plans shots, runs pre-flight checks to prevent wasted renders, writes model-ready prompts with premium aesthetics, diagnoses failed takes, and edits clips into a finished video with ffmpeg. Use when the user wants to make, plan, fix, or edit an AI video, short video, ad, short drama, product or property video, image-to-video, voiceover or soundtrack, or asks to set up a video generation provider or local video model.
license: MIT
---

# Takewright

Takewright turns an idea into a finished video: plan → check → generate → review → edit. Claude is the director; a provider (cloud, local GPU or the user's own web app) renders.

Reply in the user's language. Prompts sent to models are English unless the model or scene needs another language (for example Chinese dialogue on a Chinese-native model).

## Priorities (in this order)

1. **First-pass quality.** A 废片 / unusable take wastes more money and time than anything else. Never trim technical rules or checks to save tokens.
2. **Credit and time saving.** Estimate before every paid task; image before video; draft before final; fix in editing before re-rendering.
3. **Token saving.** Read only the files the current step needs (map below). One confirmation card, not question-by-question.

Never lock the user in: every model and capability stays available; defaults are suggestions; explicit user parameters win (still estimate and confirm).

**Maintenance rule:** future edits may add or sharpen rules but must not remove model limits, command rules, quality checks or aesthetic guidance unless they are proven wrong or replaced by something better.

## File map — load on demand

| When | Read |
|---|---|
| No `.takewright/config.json` yet, or the user asks to set up / switch provider | `setup/wizard.md` (it routes to one provider or local file) |
| Generating with a provider | that provider's file in `setup/providers/` or `setup/local.md` (once per session) |
| Planning any shot | `craft/preflight.md` and `craft/prompting.md` |
| A reference image or photo is involved | `craft/image-to-video.md` |
| Look, style, lighting, "make it premium/cinematic" | `craft/aesthetics.md` |
| A take is weak, broken or rejected | `craft/troubleshoot.md` |
| Reviewing a take or delivering | `craft/qc.md` |
| Genre fits (only the one that matches) | `genres/product-ad.md`, `genres/architecture.md`, `genres/short-video.md`, `genres/short-drama.md`, `genres/explainer.md` |
| Joining clips, captions, music, aspect ratios, cover | `assembly/editing.md` (+ `scripts/assemble.py`) |

Paths are relative to this skill's folder. Scripts need Python 3.8+ and ffmpeg; run them as `python <skill-dir>/scripts/<name>.py` (on Windows try `python`, then `py`, then `python3`).

## Step 0 — Configuration (silent if already done)

Read the global config `~/.takewright/config.json` (Windows: `%USERPROFILE%\.takewright\config.json`), then a project config `./.takewright/config.json` if present (project values override global ones). If neither exists, run `setup/wizard.md`. The config never stores API keys.

## Workflow

### 1. Brief (ask only what matters)
Infer platform, ratio, length and genre from the request. Ask at most 1–2 questions in one message, only for things that change the result (for example: real photos available? brand rules? target platform?).

| Signal | Default suggestion |
|---|---|
| TikTok / Reels / Shorts / 抖音 / 小红书 | 9:16, shots of 3–8 s |
| YouTube / website hero / landscape | 16:9 |
| Feed post | 1:1 or 4:5 |
| User has photos of the subject | image-to-video (first frame) — best control |
| A person must say exact lines | lip-sync capable route (see provider file) |

### 2. Plan
For anything longer than one clip, write a shot list in the user's language:
`Shot 1 (0–5 s): picture / action / camera / light / sound`
Then an English prompt per shot (`craft/prompting.md`). One main action and one camera move per shot.

### 3. Pre-flight check
Run every shot through `craft/preflight.md`. Fix problems before estimating. Never skip this, even for a "quick test".

### 4. One confirmation card (before any credit or long local render)
Estimate every paid task (provider file says how), then show one card and wait for an explicit yes:

```
Ready to generate:
  Content: {one line} · {N} shots
  Plan: {image → image-to-video / draft → final / direct}
  Provider · model: {…}   Ratio: {…}   Resolution: {…}   Length: {s per shot}
  Inputs: {none / first frame / N reference images / reference video}
  Pre-flight: {passed / adjusted: …}
  Estimate: draft {x}, final {y}, total ≈ {z} {credits/$/minutes of GPU}
  Retake budget (multi-shot): ≈ {n} drafts per shot
  Generate? (any parameter can change)
```
Translate the card into the user's language. If an estimate is unavailable, say so and still ask. Never submit a paid task without this yes. Never auto-retry a paid task.

### 5. Generate (cheapest path to a good result)
- **Image-first** for key shots: generate the key frame as an image (cheap), approve it, then animate it.
- **Draft → final** where the model supports drafts or lower resolution: explore cheap, finalize only approved takes.
- **Direct** only for simple shots, quick tests, or when asked.
- **Free fallback:** real photos animated with a slow push-in (`assemble.py stills`) — no credits, no risk of invented details. Offer it for listings/products, tight budgets, or after two failed takes.
Submit long jobs asynchronously and poll in the background; respect provider rate limits; on timeout tell the user how to fetch the result later.

Budget reality (say once for multi-shot work): AI video is probabilistic — the same prompt gives different results. Plan about 2–3 drafts for a simple shot and more for complex motion.

### 6. Review
Download every result to `./takewright-output/{YYYY-MM-DD}/` with slug `{project}_{shot}_{ratio}_{draft|final}_v{n}`. Run `craft/qc.md` (frame extraction via `scripts/assemble.py frames`). Rate each take 好 Good / 可修 Fixable / 废片 Unusable. Unusable → `craft/troubleshoot.md` before any retry.

### 7. Edit and deliver
Assemble approved takes with `assembly/editing.md`: join, captions, voiceover, music, loudness, ratio variants, cover frame. Report file paths, settings, seeds and credits charged.

### 8. Log
Append one line per take to `./takewright-output/prompt-log.md`:
`| date | provider/model | ratio/res/dur | cost | prompt (short) | rating + cause/fix |`
At the start of a new task read only the last 20 lines to reuse what worked.

## Guardrails
- Estimate and confirm before spending; show totals for multi-shot plans.
- Never fabricate model IDs, flags, metadata, prices or results. If unsure, check the provider's `--help`, schema or docs.
- Keep API keys out of chat, files, logs and config. Use the provider's own login or environment variables.
- No real public figures' likeness or voice, no protected characters, brands or logos, no voice cloning without the owner's consent, no deceptive depictions of real places, products or people (for example, AI features added to a real listing).
- Rights: check model licences before commercial use, and use licensed or generated music.
