# Editing (assembly)

`scripts/assemble.py` wraps ffmpeg so edits are repeatable and cheap in tokens. Run `python <skill-dir>/scripts/assemble.py <subcommand> -h` for every option. Needs ffmpeg + ffprobe on PATH.

## Typical finish (vertical social video)
```bash
# 1. Captions from the voiceover script (one caption per line), timed to the real voiceover
python scripts/assemble.py srt --text script.txt --out captions.srt --fit-to voiceover.mp3
# 2. Join approved takes + voice + music (ducked) + captions, normalized loudness
python scripts/assemble.py edit --clips s01.mp4 s02.mp4 s03.mp4 --out final_9x16.mp4 \
  --ratio 9:16 --xfade 0.4 --voice voiceover.mp3 --music bgm.mp3 --duck --subs captions.srt --fade 0.5 --hold-end auto
# 3. Other platforms
python scripts/assemble.py variants final_9x16.mp4 --ratios 1:1 16:9 --fit blur
# (Photos instead of AI clips? python scripts/assemble.py stills p1.jpg p2.jpg --duration 4)
# 4. Cover image
python scripts/assemble.py cover final_9x16.mp4 --at 2.0
```

## Subcommands
| Command | Use |
|---|---|
| `probe FILE` | width, height, duration, fps, size, audio; also `listenhub_meta` (`WxH:DUR:FPS:SIZE`) for reference-video flags |
| `frames FILE --count 5` | QC frames (`craft/qc.md`) |
| `stills IMG … --duration 4 --zoom 0.08` | photos → clips with a slow push-in (free; no AI). Real listings/products, storyboards, or a fallback when generation keeps failing. `--fit blur` keeps the whole photo; `--zoom 0` for static |
| `trim FILE --start 0.5 --end 4.8 --out cut.mp4` | remove a bad first/last moment instead of re-rendering |
| `srt --text script.txt --out c.srt` | timed captions: ~2.5 words/s Latin, ~4 chars/s CJK, ≥1.2 s each (`--wps`, `--cps`, `--min`, `--start`). **Always add `--fit-to voiceover.mp3` when a voiceover exists** — TTS speed varies, and this stretches/squeezes the captions to the real voice |
| `edit --clips … --out …` | normalize every clip to one size/fps, join (cut or crossfade), mix clip audio + voice + music, burn captions, fades, loudness |
| `variants FILE --ratios 1:1 16:9` | re-frame a finished edit (`--fit blur` keeps everything visible on a blurred background; `crop` fills; `pad` letterboxes) |
| `cover FILE --at 2.0` | JPG cover frame |

## `edit` options that matter
- `--ratio 9:16|16:9|1:1|4:5|3:4|4:3|21:9` or `--size 1080x1920`; `--fit crop|pad|blur` for clips that don't match.
- `--xfade 0.4` crossfade between clips (must be shorter than the shortest clip); 0 = hard cuts (best for fast social pacing).
- Audio: clips' own audio is kept (`--clip-volume`, or `--mute-clips`); `--voice` (+ `--voice-start`, `--voice-volume`); `--music` loops to length (`--music-volume 0.25` default) and `--duck` lowers it under the voice.
- `--loudness -14` (default, social platforms) · `-16` for podcasts/YouTube-quiet · `--no-loudnorm` to skip.
- Captions: `--subs file.srt` burns them in. Chinese/Japanese/Korean text auto-selects a CJK font (Windows: Microsoft YaHei; macOS: PingFang SC; Linux: Noto Sans CJK SC). Override with `--font`, `--font-size`, `--margin-v` (vertical safe margin).
- `--fade 0.5` fades picture and sound in/out at the very start and end.
- `--hold-end 2` freezes the last frame for 2 s — room for a title, price or call to action added later. `--hold-end auto` extends the ending just enough for the voiceover to finish (+0.5 s).
- If the voiceover is longer than the video, `edit` prints a **WARNING** and lists it under `warnings` in its JSON. Never ignore it: use `--hold-end auto`, add or lengthen shots, or shorten the script.
- Quality: `--crf 18` (lower = better/larger), `--preset medium` (use `veryfast` for quick previews).

## Editing craft
- Cut on action; hold the last shot for titles 1.5–2 s.
- Hard cuts for social energy; crossfades for calm, premium pieces.
- Put the strongest shot first (hook); keep each shot under ~4 s for social unless it is a slow premium piece.
- Time visuals to the voiceover: 2.5 words/s; captions match the voice exactly.
- Music: generated or licensed only; duck under voice; end on a musical resolution if possible.
- Titles, prices, logos and CTAs are added here (or in the user's editor), never generated.
- For advanced titles/graphics, export the clean edit and finish in the user's editor (CapCut, Premiere, DaVinci Resolve).
