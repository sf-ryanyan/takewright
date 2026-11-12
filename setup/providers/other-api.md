# Provider: any other API

Use for platforms without a dedicated file: official model APIs (for example ByteDance Volcengine Ark / BytePlus ModelArk for Seedance, Google's Gemini API for Veo, Kling, Runway), or routers (Replicate, OpenRouter, Kie.ai, PiAPI, Atlas Cloud and similar).

## Install → Sign in → Verify
1. Ask which platform. Open its **current official docs** (web search / fetch) — do not rely on memory for endpoints, model IDs or field names; they change often.
2. Prefer the platform's own CLI or SDK if it has one; otherwise plain HTTPS (curl or a short Python script with `urllib`).
3. Key: the user sets an environment variable in their own terminal (`setup/wizard.md` § Secrets). Scripts read it from the environment; never hard-code it.
4. Verify with the cheapest call available: account/balance, model list, or a price estimate. Save in config as `"other:<name>"` with the base URL and model ID used (no key).

## Universal async lifecycle
1. **Create** the task: model ID, prompt, duration, ratio/size, resolution, reference file URLs (upload first if needed).
2. **Store** task ID + provider + model ID + prompt version in the prompt log.
3. **Poll** status (or use the SDK's wait helper / webhook) every 10–20 s; stop after ~20 min and report.
4. **Retrieve** output URL(s) — and the last frame if the API offers it (useful for continuations).
5. **Download immediately**; many output URLs expire.
6. Cancel or delete tasks only via the documented endpoint.

## Request checklist
- One visible beat, one camera move, physical light, sound intent, constraints (`craft/preflight.md`).
- Mode explicit: text-to-video, image-to-video, first+last frame, reference, edit or extend.
- Reference roles explicit; each file has one job.
- Real-person faces, voices and portraits: authorization and platform policy checked; some platforms reject realistic face uploads.
- Price, duration limits, resolution, region and quotas checked with a date.
- Never merge field names across platforms (one platform's `aspect_ratio` may be another's `ratio`).

## Notes
- Official-surface access (for example Volcengine in mainland China) can require region-specific accounts or identity verification. Tell the user early.
- The workspace or corporate network may block some API hosts; if a request is refused at the network level, say so instead of retrying.
