# Genre: product ad / e-commerce

## Best path
Real product photo → approved key frame (clean background, target ratio) → image-to-video in **Hold mode** with locks: "preserve product shape, logo and label exactly; no shape change". Text, price and CTA go in the edit, never in the generation.

## Shot menu (pick 3–6 for a 15–30 s ad)
| Shot | Prompt core |
|---|---|
| Hero reveal | product centred, slow push-in, narrow light sweep across the surface, dark or white seamless background |
| Material macro | 100 mm macro on texture, raking light moves slowly across |
| Rotation | product on a slow turntable, 90° turn, soft rim light, static camera |
| In use | hands or a person using it naturally, one action, product clearly visible, shallow focus |
| Lifestyle context | product in a real setting, wide 35 mm, warm window light |
| Packshot end | product static, centred, 40% empty space for title/CTA, final hold 1–2 s |

## Structure (15 s)
0–2 s hook (reveal or macro) → 2–9 s benefit shots (in use / context) → 9–13 s proof or detail → 13–15 s packshot hold for title and CTA.

Zero-cost option: `assemble.py stills` on product photos (slow push-in) for detail shots; spend credits only on the hero and in-use shots.

## Rules
- Never let the model redraw the logo or label in motion; keep them static and light around them.
- No transformations of the product unless it is clearly creative (and labelled as such).
- Claims and prices come from the user, added in editing.
- Fast route for a quick ad: providers with an "auto ad" capability (e.g. PixVerse agent via ListenHub) — then refine key shots.
