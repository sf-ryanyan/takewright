# Setup wizard

Run once (or when the user asks to set up, switch or add a provider). Goal: a working, verified route and a saved config — without ever storing secrets.

## 1. Ask the route (one message, multiple choice)

> How do you want to generate video?
> 1. **Cloud platform** — I already have an account or credits (ListenHub, fal, MuAPI, or another)
> 2. **Local GPU** — run open models on my own computer
> 3. **Manual** — just give me prompts; I'll paste them into a web app (Jimeng/Dreamina, Kling, Hailuo, Higgsfield, Runway, Veo…)
> 4. **Hybrid** — local or cheap drafts, cloud finals
> 5. **Not sure** — check my computer and recommend

Use the multiple-choice question tool if available. Several cloud providers can be configured; one is the default.

## 2. Follow the route

| Answer | Do |
|---|---|
| Cloud | Ask which platform(s). Read only the matching file: `setup/providers/listenhub.md`, `setup/providers/fal.md`, `setup/providers/muapi.md`, or `setup/providers/other-api.md` for anything else. Follow its **Install → Sign in → Verify** steps. |
| Local | Read `setup/local.md`: run the hardware check, recommend a model tier, guide the install, verify with one test render. |
| Manual | Read `setup/providers/manual.md`. No install needed. |
| Hybrid | Do Local (or the cheaper cloud model) as the draft route and one Cloud provider as the final route. |
| Not sure | Run `python <skill-dir>/scripts/hwcheck.py` and show the result in plain words. Recommend: capable GPU (≥12 GB VRAM, modern architecture) → Local or Hybrid; otherwise Cloud if they have any account, else Manual. |

Always also check the two local tools every route needs (frame checks, editing, hardware check):
- **Python 3.8+**: try `python --version`, then `py --version` (Windows launcher), then `python3 --version`. Use whichever works for all script calls. Missing → Windows: `winget install Python.Python.3.12` (then open a new terminal); macOS: `brew install python`; Debian/Ubuntu: `sudo apt install python3`. On Windows, if `python` opens the Microsoft Store instead, install with winget and turn off the "App execution aliases" for python in Settings.
- **ffmpeg + ffprobe**: `ffmpeg -version`. Missing → Windows: `winget install Gyan.FFmpeg`; macOS: `brew install ffmpeg`; Debian/Ubuntu: `sudo apt install ffmpeg`. Open a new terminal after installing so PATH updates.

## 3. Secrets — hard rules

- Never ask the user to paste an API key into chat. Tell them where to paste it: the provider's own login/`setup` command, or an environment variable set in their own terminal.
- Never write keys into the config, the prompt log, scripts or command history you create.
- If a key is shown to you by accident, tell the user to rotate it.

Environment variable lines to give the user (replace NAME):
- Windows PowerShell (persistent): `setx NAME "value"` then open a new terminal
- macOS/Linux (bash/zsh): add `export NAME="value"` to `~/.zshrc` or `~/.bashrc`, then `source` it

## 4. Verify before saving

Each provider file ends with a **Verify** command that costs nothing (status, account or estimate call). Run it. Only save the config after it passes. If it fails, show the exact error and the provider file's fix — do not guess.

## 5. Save `.takewright/config.json`

Save **globally** by default at `~/.takewright/config.json` (Windows: `%USERPROFILE%\.takewright\config.json`) so setup happens once for every project. Only if the user wants different settings for one project, also save a project file at `./.takewright/config.json`; it overrides the global one key by key.

```json
{
  "version": 1,
  "route": "cloud | local | manual | hybrid",
  "default_provider": "listenhub | fal | muapi | other:<name> | local | manual",
  "draft_provider": "local | <provider> | null",
  "providers": {
    "listenhub": { "auth": "oauth | api-key", "verified": "YYYY-MM-DD" },
    "fal": { "verified": "YYYY-MM-DD" },
    "local": { "gpu": "…", "vram_gb": 0, "comfy_url": "http://127.0.0.1:8188", "workflows": { "t2v": "path/to/api.json", "i2v": "path/to/api.json" } }
  },
  "defaults": { "language": "auto", "ratio": "9:16", "budget_cap": null },
  "ffmpeg": true
}
```

Keep only the providers actually set up. `budget_cap` (optional) = the most the user allows per confirmation card; above it, ask again even after a yes.

## 6. Finish

Tell the user in two or three lines: route, default provider, what was verified, and how to change it later ("say: set up Takewright again" or edit the config).
