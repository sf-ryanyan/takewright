# Director's pre-flight check

Run on every shot before estimating. Fix problems first; report the result in one line on the confirmation card. Most unusable takes are decided here, before any money is spent.

| Check | Pass rule | Fix |
|---|---|---|
| Event density | clip seconds ÷ beats ≥ 3 (a reaction or insert = ½ beat). 2–3 = risky; under 2 = split | Split into more clips or cut beats |
| Too empty | a long clip with one small action lets the model improvise | Shorten the clip or add one concrete beat |
| Camera | exactly one move with a start and an end ("slow push-in from the doorway to the window") | Remove extra moves; never "static" + "orbit" together |
| Conflicts | no contradicting style, light, time of day or speed | Keep one, delete the other |
| Reference roles | every asset has one job, named in plain words in the order passed (opening frame / character / location / camera rhythm / music) | Drop assets without a job |
| Image-to-video | prompt describes only what the image cannot show + preservation locks (`craft/image-to-video.md`) | Delete re-described static details |
| High-risk elements | fast hands, small text/signs/logos/screens, >2 people interacting, several simultaneous moves, product changing shape, crowds | Lock framing, simplify, move text to editing, or split |
| Dialogue time | ≤ ~2.5 English words or ~4 Chinese characters per second; one speaker per line; head mostly still | Shorten the line or lengthen the clip |
| Anti-slop | no empty praise words (`craft/prompting.md`) | Replace with light, material, action, sound |
| Sound | every video prompt states its sound | Add ambience, or "no score, natural ambience only" |
| Ending | calm, usable final hold; no effect pile-up | End on a one-second hold |
| Limits | duration, resolution, ratio, prompt length and reference counts within the chosen model's limits (provider file) | Adjust; never silently truncate a prompt |
| Rights & safety | no real public figures, protected characters, brands/logos, unconsented voices; no deceptive depiction of real products, places or people | Rewrite as original, honest content |

Notes
- Some platforms reject realistic human-face reference uploads. If rejected, switch to a text description, an illustrated reference, or a provider that allows it — do not retry the same upload.
- For multi-shot work also check continuity across shots: same character images, same Look Card wording, light direction, screen direction, props.
- If several checks fail, the shot is too ambitious: split it.
