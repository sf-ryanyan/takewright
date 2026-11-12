# Local GPU route (ComfyUI + open models)

Goal: an honest recommendation (local, hybrid or cloud), then a working local install verified by one test render.

## 1. Hardware check
Run `python <skill-dir>/scripts/hwcheck.py` (add `--json` for machine-readable output). It reports OS, CPU, RAM, free disk, NVIDIA GPU name / VRAM / compute capability (via `nvidia-smi`), Apple Silicon, ffmpeg, and whether ComfyUI answers on `http://127.0.0.1:8188`. It also prints a tier. Explain the result in plain words.

## 2. Recommend by tier (open-model landscape as of 2026 — re-check before installing)

| Tier | Hardware | Recommendation |
|---|---|---|
| **T0** | No NVIDIA GPU, <8 GB VRAM, or an old architecture (compute capability below 7.0, e.g. GTX 10-series) | Local video generation not recommended — too slow or won't fit. Use cloud or manual for generation; keep **editing local** (ffmpeg). |
| **T1** | 8 GB VRAM, modern GPU | Light models only: **LTX-Video** (fast, lower fine detail) or **Wan 2.2 TI2V-5B** in FP8 with ComfyUI offloading (~5 s at 720p). Good for drafts; finals usually on cloud (hybrid). |
| **T2** | 12–16 GB VRAM | **Wan 2.x 14B** (quantized/GGUF on 12 GB; comfortable on 16 GB), **HunyuanVideo 1.5** with offloading (~14 GB minimum). Local drafts and many finals. |
| **T3** | 24 GB+ VRAM | All mainstream open models: Wan 2.2 14B, HunyuanVideo 1.5 at full quality, LTX-2.x with native audio. Local can handle finals. |
| **Mac** | Apple Silicon | ComfyUI runs, but video models are slow and some nodes are CUDA-only. Recommend cloud for video, local for images/editing. |

Also needs: 32 GB+ system RAM recommended for offloading; 30–100 GB free disk for models; NVIDIA driver up to date.

Licences differ — tell the user before commercial use: Wan 2.2 is Apache 2.0; HunyuanVideo's licence excludes some regions (EU, UK, South Korea) and has conditions; LTX models have their own licence terms. Link the model card and let the user decide.

## 3. Cost/time analysis (show before installing)
Give a short table for the user's tier: time per 5-second draft (rough), electricity/noise, setup effort, quality vs. their cloud option. Recommend one of:
- **Local** — strong GPU and high volume.
- **Hybrid** (most common) — local drafts to iterate free, cloud finals for quality.
- **Cloud/manual** — T0, low volume, or no time for setup.
Let the user choose; do not install anything without a yes.

## 4. Install ComfyUI (only after yes)
- **Windows:** ComfyUI Desktop installer (comfy.org) or the portable package; **manual/portable** installs serve on port 8188. The Desktop app may use a different port — read it from the app's server settings/log and save it to config.
- **macOS:** ComfyUI Desktop.
- **Linux:** `git clone https://github.com/comfyanonymous/ComfyUI` → install its requirements in a venv → `python main.py --port 8188`.
- Keep the server on `127.0.0.1` (default). Do not expose it on a network: the API has no authentication.

Models and workflows: open ComfyUI's **workflow templates** (video section) and pick the template for the chosen model; ComfyUI offers to download the required model files. Run the template once in the UI to confirm it works.

## 5. Connect Takewright to ComfyUI
1. In ComfyUI: **File → Export Workflow (API)** (older versions: enable Dev Mode, then "Save (API Format)"). Save as `workflows/t2v_api.json` (and `i2v_api.json` for image-to-video). The normal save format will not work with the API.
2. Open the JSON and note the node IDs for: positive prompt (`CLIPTextEncode` or the model's text node), seed, width/height/length, input image (`LoadImage`).
3. Test:
```bash
python <skill-dir>/scripts/comfy.py check --server http://127.0.0.1:8188
python <skill-dir>/scripts/comfy.py run --workflow workflows/t2v_api.json --set 6.text="a calm lake at sunrise, slow push-in" --set 3.seed=42 --out ./takewright-output
```
For image-to-video, upload the frame first and set the LoadImage node:
```bash
python <skill-dir>/scripts/comfy.py upload ./key.png --server http://127.0.0.1:8188     # prints the stored name
python <skill-dir>/scripts/comfy.py run --workflow workflows/i2v_api.json --set 52.image=key.png --set 6.text="..." --out ./takewright-output
```
`--set NODE.INPUT=VALUE` accepts numbers, true/false, or text (prefix `str:` to force text, e.g. `--set 6.text=str:2026`). Node IDs are examples — use the IDs from the user's JSON.
4. Save `comfy_url` and workflow paths (absolute paths) to `~/.takewright/config.json`.

## Local generation rules
- Estimate = expected GPU minutes (from the first test render), shown on the confirmation card.
- One job at a time; close other GPU-heavy apps. Out-of-memory → lower resolution/length, enable offloading/quantized model, or move the shot to cloud.
- Seeds are reproducible locally: log them; re-use for near-identical retakes.
- Same craft rules as cloud: pre-flight, image-first, QC, troubleshoot.
