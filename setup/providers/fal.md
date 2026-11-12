# Provider: fal.ai (genmedia CLI)

fal hosts 1,000+ image, video, audio and 3D endpoints (Seedance, Kling, Veo, Grok Imagine, HappyHorse and more) behind one key and one CLI, `genmedia`. Official community skills (MIT): github.com/fal-ai-community/skills.

## Install → Sign in → Verify

**Install**
```bash
curl https://genmedia.sh/install -fsS | bash      # macOS / Linux
irm https://genmedia.sh/install.ps1 | iex         # Windows PowerShell
```

**Sign in:** the user creates a key at fal.ai → dashboard → API keys, then runs `genmedia setup` in their own terminal (interactive; the key is saved encrypted locally) — or sets the environment variable `FAL_KEY` (see `setup/wizard.md`) and runs `genmedia setup --non-interactive --api-key "$FAL_KEY"`. Add `--no-save-key` to keep the key only in the environment.

**Verify (free):**
```bash
genmedia version
genmedia models --endpoint_id bytedance/seedance-2.0/text-to-video --json
genmedia pricing bytedance/seedance-2.0/text-to-video --json
```

## Rules that prevent failed jobs
1. Always pass `--json` when Claude reads the output.
2. **Never invent endpoint IDs.** Discover with `genmedia models "<query>" --json` or `genmedia models --category text-to-video --json`; verify with `genmedia models --endpoint_id <id> --json`.
3. **Read the schema before custom parameters:** `genmedia schema <endpoint_id> --json`. Field names differ per endpoint (`duration`, `aspect_ratio`, `resolution`, `image_url`, `generate_audio` …). Guessed fields fail with HTTP 422.
4. **Price before running:** `genmedia pricing <endpoint_id> --json` — this is the estimate for the confirmation card.
5. Local files must be uploaded first: `genmedia upload ./frame.png --json` → use the returned `url`.
6. Video is slow: submit with `--async`, poll with `genmedia status`, download with `--download`.
7. Save files with `--download`, not curl.

## Commands
```bash
# Submit (async) and remember request_id
genmedia run bytedance/seedance-2.0/image-to-video --prompt '...' --image_url '<uploaded url>' --duration 5 --aspect_ratio 9:16 --async --json
# Poll: status IN_QUEUE / IN_PROGRESS / COMPLETED / FAILED
genmedia status bytedance/seedance-2.0/image-to-video <request_id> --json
# Fetch + download when COMPLETED
genmedia status bytedance/seedance-2.0/image-to-video <request_id> --download './takewright-output/{request_id}_{index}.{ext}' --json
# Logs or cancel
genmedia status <endpoint_id> <request_id> --logs --json
genmedia status <endpoint_id> <request_id> --cancel
```
(The parameter names above are examples; confirm them with `genmedia schema` first.)

Smart routing for quick defaults (no endpoint): `genmedia run "a 5-second clip of …" --json` — the output's `routed` block shows the endpoint used. Prefer explicit endpoints for production so results are repeatable.

## Routing candidates (verify before use — catalog changes)
As published in fal's model-routing guidance (2026). Confirm each ID with `genmedia models --endpoint_id`.

| Role | Candidates |
|---|---|
| Highest-quality video | `bytedance/seedance-2.0/text-to-video`, `…/image-to-video`, `…/reference-to-video` |
| Faster Seedance | `bytedance/seedance-2.0/fast/text-to-video` (and `/fast/image-to-video`, `/fast/reference-to-video`) |
| Fast / low-cost drafts | `xai/grok-imagine-video/text-to-video`, `…/image-to-video`, `…/edit-video` |
| Multi-shot / element control | `fal-ai/kling-video/v3/pro/text-to-video`, `…/image-to-video` |
| Alternative | `alibaba/happy-horse/text-to-video`, `…/image-to-video` |
| Talking presenter / lip sync | `veed/fabric-1.0` (image + audio), `veed/fabric-1.0/text`, `fal-ai/creatify/aurora` |
| Premium still / key frame | `openai/gpt-image-2` (quality high), `fal-ai/nano-banana-pro`, `fal-ai/nano-banana-2` |
| Fast draft still | `fal-ai/flux-2/klein/9b` |
| Text inside an image must be correct | `openai/gpt-image-2`, then `fal-ai/nano-banana-pro` |

Draft → final on fal: draft with a fast/cheap endpoint or lower resolution, then final with the premium endpoint using the same approved key frame and prompt.

TTS and music: discover with `genmedia models "text to speech" --json` / `genmedia models "music generation" --json`, then schema + pricing as above.

Errors: 401/403 → key missing or wrong (`genmedia setup`); 422 → wrong field (read schema); FAILED with moderation → rewrite the prompt safely (`craft/troubleshoot.md`).
