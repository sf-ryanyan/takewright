# Quality check (QC)

## Extract frames
```bash
python <skill-dir>/scripts/assemble.py frames take.mp4 --count 5
```
Writes evenly spaced JPG frames next to the take (0%, 25%, 50%, 75%, ~95% for 5). Look at them. Use 3 frames for clips under 8 s, 5 for longer. If frames cannot be extracted, ask the user to watch the take.

## Checklist (per take)
1. Ratio and framing correct; subject not cropped; space left for captions (safe area).
2. Faces, hands, products and architecture stable — no warping, bending walls, extra fingers.
3. No unwanted text, logos, watermarks or garbled signs.
4. Identity and look match the references and earlier shots (wardrobe, props, light direction).
5. One clean camera move; no jumps.
6. Clean opening and a holdable ending (usable for a cut).
7. Sound matches the plan (no surprise music; dialogue in sync).
8. Honest: the take does not show features the real product/place does not have.

Rate: **Good** · **Fixable** (→ retake protocol or edit fix) · **Unusable** (→ `craft/troubleshoot.md` before any retry). In Chinese: 好 / 可修 / 废片.

## Delivery checklist (final video)
| Area | Check |
|---|---|
| Picture | resolution, ratio, fps consistent; no flicker or banding |
| Text | captions spelled correctly, inside the safe area, correct script variant (简体/繁體) |
| Audio | voice clear; music under voice; loudness about −14 LUFS for social |
| Continuity | wardrobe, props, screen direction, light direction |
| Rights | music, voice, likeness, logos and model licences clear |
| Versions | 9:16 / 16:9 / 1:1 as needed; cover image |
| Metadata | prompts, seeds, model IDs and costs logged |

## Naming
`{project}_{shot}_{ratio}_{draft|final}_v{n}.mp4` — e.g. `oakst_s01_9x16_draft_v1.mp4`; final edit `{project}_{ratio}_{lang}_final.mp4`.
