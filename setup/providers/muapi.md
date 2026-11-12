# Provider: MuAPI (muapi CLI)

MuAPI is an aggregator for many image, video, audio and lip-sync models (Seedance, Kling, Veo, MiniMax and others) behind one key. Community skills (MIT): github.com/SamurAIGPT/Generative-Media-Skills.

## Install → Sign in → Verify

**Install** (one of):
```bash
npm install -g muapi-cli
pip install muapi-cli
npx muapi-cli --help        # run without installing
```

**Sign in:** the user gets a key from the MuAPI dashboard and runs `muapi auth configure` in their own terminal (interactive prompt). Scripts also read the `MUAPI_KEY` environment variable.

**Verify (free):**
```bash
muapi auth status
muapi models list --category video --output-json
```

## Rules
- **Model names change — list before use:** `muapi models list --category video --output-json`. Never invent a model name; copy it from the list.
- Check flags once per session: `muapi video generate --help`, `muapi video from-image --help`.
- Price: read it from the model list / dashboard for the confirmation card. If no price is shown, say "estimate unavailable" and still ask.
- Local files must be uploaded first: `muapi upload file ./frame.png --output-json` → use the returned URL.

## Commands
```bash
# Text-to-video, async: keep the request_id
muapi video generate '<prompt>' --model <model-from-list> --no-wait --output-json
# Image-to-video (confirm flag names with --help)
muapi video from-image --help
# Wait and download
muapi predict wait <request_id> --download ./takewright-output
# Re-fetch a result without re-running (no new charge)
muapi predict result <request_id>
# Images (for key frames)
muapi image generate '<prompt>' --model <model-from-list> --download ./takewright-output
```
Voiceover / music: MuAPI also offers audio models — check `muapi audio --help` and `muapi models list --output-json` for TTS or music models; use the same list → help → run pattern. If none fit, use another configured provider or the user's own recorded/licensed audio.

Add `--jq '<filter>'` with `--output-json` to extract one field (for example the request ID) if the shell lacks `jq`.

Model choice: pick the highest-quality video model in the list for finals, a fast/turbo variant for drafts. When a model fails repeatedly, choose another family from the list rather than re-rolling (`craft/troubleshoot.md`).

Errors: auth → `muapi auth configure`; unknown model → re-list models; result URL expired → `muapi predict wait <request_id>` again.
