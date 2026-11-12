#!/usr/bin/env python3
"""Takewright editing tool (ffmpeg wrapper). Standard library only.

Subcommands
  probe    FILE                         -> JSON: size, duration, fps, audio, ListenHub meta string
  frames   FILE [--count 5]             -> evenly spaced JPG frames for QC
  trim     FILE --start S --end E --out OUT
  srt      --text script.txt --out captions.srt [--start 0] [--wps 2.5] [--cps 4]
  stills   IMG [IMG ...] [--duration 4] [--zoom 0.08]   -> photo clips with a slow push-in
  edit     --clips a.mp4 b.mp4 ... --out final.mp4 [options]   -> joined, captioned, mixed video
  variants FILE --ratios 9:16 1:1 16:9 [--fit blur|crop|pad]
  cover    FILE [--at 1.0] [--out cover.jpg]

Run any subcommand with -h for its options.
"""
import argparse
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

RATIO_SIZES = {
    "9:16": (1080, 1920), "16:9": (1920, 1080), "1:1": (1080, 1080),
    "4:5": (1080, 1350), "3:4": (1080, 1440), "4:3": (1440, 1080), "21:9": (2560, 1080),
}
CJK_RE = re.compile(r"[　-〿぀-ヿ㐀-䶿一-鿿가-힯＀-￯]")


# ---------- helpers ----------
def need(tool):
    if not shutil.which(tool):
        sys.exit(f"{tool} not found. Install ffmpeg (Windows: winget install Gyan.FFmpeg; "
                 f"macOS: brew install ffmpeg; Linux: sudo apt install ffmpeg).")


def run(cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")
    if proc.returncode != 0:
        tail = "\n".join(proc.stderr.strip().splitlines()[-15:])
        sys.exit(f"ffmpeg failed:\n  {' '.join(cmd)}\n{tail}")
    return proc.stdout


def probe(path):
    need("ffprobe")
    if not os.path.isfile(path):
        sys.exit(f"File not found: {path}")
    out = run(["ffprobe", "-v", "error", "-show_entries",
               "stream=codec_type,width,height,r_frame_rate:format=duration,size",
               "-of", "json", path])
    data = json.loads(out)
    v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), None)
    a = any(s.get("codec_type") == "audio" for s in data.get("streams", []))
    fmt = data.get("format", {})
    dur = float(fmt.get("duration") or 0)
    fps = None
    if v and v.get("r_frame_rate") and v["r_frame_rate"] != "0/0":
        n, d = v["r_frame_rate"].split("/")
        fps = round(float(n) / float(d), 3) if float(d) else None
    info = {"path": path, "width": v and v.get("width"), "height": v and v.get("height"),
            "duration": round(dur, 3), "fps": fps, "size_bytes": int(fmt.get("size") or 0),
            "has_video": v is not None, "has_audio": a}
    if v:
        info["listenhub_meta"] = (f"{info['width']}x{info['height']}:{round(dur, 2)}:"
                                  f"{round(fps or 0)}:{info['size_bytes']}")
    return info


def size_for(ratio, size=None):
    if size:
        m = re.fullmatch(r"(\d+)x(\d+)", size)
        if not m:
            sys.exit("--size must look like 1080x1920")
        w, h = int(m.group(1)), int(m.group(2))
    elif ratio in RATIO_SIZES:
        w, h = RATIO_SIZES[ratio]
    else:
        sys.exit(f"Unknown ratio {ratio}. Use one of {', '.join(RATIO_SIZES)} or --size WxH")
    return w - w % 2, h - h % 2


def fit_filter(w, h, fit, inp="0:v", out="v"):
    if fit == "crop":
        return (f"[{inp}]scale={w}:{h}:force_original_aspect_ratio=increase,"
                f"crop={w}:{h},setsar=1[{out}]")
    if fit == "pad":
        return (f"[{inp}]scale={w}:{h}:force_original_aspect_ratio=decrease,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:color=black,setsar=1[{out}]")
    # blur: blurred, zoomed copy behind the whole frame
    return (f"[{inp}]split=2[bgs][fgs];"
            f"[bgs]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},"
            f"boxblur=luma_radius=40:luma_power=2,eq=brightness=-0.08[bg];"
            f"[fgs]scale={w}:{h}:force_original_aspect_ratio=decrease[fg];"
            f"[bg][fg]overlay=(W-w)/2:(H-h)/2,setsar=1[{out}]")


def enc_args(preset, crf):
    return ["-c:v", "libx264", "-preset", preset, "-crf", str(crf), "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", "-movflags", "+faststart"]


def default_cjk_font():
    system = platform.system()
    if system == "Windows":
        return "Microsoft YaHei"
    if system == "Darwin":
        return "PingFang SC"
    return "Noto Sans CJK SC"


# ---------- subcommands ----------
def cmd_probe(a):
    print(json.dumps(probe(a.file), indent=2))


def cmd_frames(a):
    need("ffmpeg")
    info = probe(a.file)
    d = info["duration"]
    if d <= 0:
        sys.exit("Could not read duration.")
    n = max(1, a.count)
    times = [d * 0.5] if n == 1 else [d * (0.02 + 0.93 * i / (n - 1)) for i in range(n)]
    outdir = a.outdir or os.path.dirname(os.path.abspath(a.file))
    os.makedirs(outdir, exist_ok=True)
    stem = os.path.splitext(os.path.basename(a.file))[0]
    files = []
    for i, t in enumerate(times):
        dest = os.path.join(outdir, f"{stem}_qc{i + 1}_{t:.1f}s.jpg")
        run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", a.file,
             "-frames:v", "1", "-q:v", "2", dest])
        files.append(dest)
    print(json.dumps({"frames": files}, indent=2))


def cmd_trim(a):
    need("ffmpeg")
    if a.end <= a.start:
        sys.exit("--end must be greater than --start")
    info = probe(a.file)
    cmd = ["ffmpeg", "-y", "-v", "error", "-ss", str(a.start), "-to", str(a.end), "-i", a.file]
    cmd += ["-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf), "-pix_fmt", "yuv420p"]
    cmd += (["-c:a", "aac", "-b:a", "192k"] if info["has_audio"] else ["-an"])
    run(cmd + ["-movflags", "+faststart", a.out])
    print(json.dumps(probe(a.out), indent=2))


def fmt_ts(sec):
    ms = int(round(sec * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def cmd_srt(a):
    with open(a.text, encoding="utf-8") as f:
        lines = [l.strip() for l in f if l.strip()]
    if not lines:
        sys.exit("Script is empty.")
    t = a.start
    cues = []
    for line in lines:
        cjk = len(CJK_RE.findall(line))
        words = len(re.sub(CJK_RE, " ", line).split())
        dur = max(a.min, cjk / a.cps + words / a.wps)
        cues.append([t, t + dur, line])
        t += dur + a.gap
    fitted = None
    if a.fit_to:
        # Scale every cue so the captions end with the real voiceover (TTS speed varies).
        voice_dur = probe(a.fit_to)["duration"]
        span, target = cues[-1][1] - a.start, voice_dur - 0.15 - a.start
        if span > 0 and target > 0:
            k = target / span
            for c in cues:
                c[0] = a.start + (c[0] - a.start) * k
                c[1] = a.start + (c[1] - a.start) * k
            fitted = round(voice_dur, 3)
    out = [f"{i}\n{fmt_ts(c[0])} --> {fmt_ts(c[1])}\n{c[2]}\n" for i, c in enumerate(cues, 1)]
    with open(a.out, "w", encoding="utf-8") as f:
        f.write("\n".join(out))
    print(json.dumps({"srt": a.out, "lines": len(lines), "total_seconds": round(cues[-1][1], 2),
                      "fitted_to_voice_seconds": fitted}, indent=2))


IMAGE_EXT = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff")


def cmd_stills(a):
    """Photos -> short clips with a slow push-in (free fallback; ideal for real photos)."""
    need("ffmpeg")
    w, h = size_for(a.ratio, a.size)
    frames = max(2, int(round(a.duration * a.fps)))
    zmax = 1.0 + a.zoom
    inc = (zmax - 1.0) / frames
    os.makedirs(a.outdir, exist_ok=True)
    made = []
    for i, img in enumerate(a.images, 1):
        if not os.path.isfile(img):
            sys.exit(f"File not found: {img}")
        if not img.lower().endswith(IMAGE_EXT):
            sys.exit(f"Not an image ({', '.join(IMAGE_EXT)}): {img}")
        stem = os.path.splitext(os.path.basename(img))[0]
        dest = os.path.join(a.outdir, f"{i:02d}_{stem}.mp4")
        # Render the fitted frame at 2x first so the slow zoom does not jitter.
        zoom = "1" if a.zoom <= 0 else f"min(zoom+{inc:.6f},{zmax:.4f})"
        graph = (fit_filter(w * 2, h * 2, a.fit, "0:v", "c") +
                 f";[c]zoompan=z='{zoom}':d={frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                 f":s={w}x{h}:fps={a.fps},format=yuv420p[v]")
        run(["ffmpeg", "-y", "-v", "error", "-i", img,
             "-f", "lavfi", "-i", "anullsrc=channel_layout=stereo:sample_rate=48000",
             "-filter_complex", graph, "-map", "[v]", "-map", "1:a",
             "-frames:v", str(frames), "-t", f"{frames / a.fps:.3f}"] + enc_args(a.preset, 18) + [dest])
        made.append(dest)
    print(json.dumps({"clips": made, "seconds_each": round(frames / a.fps, 3),
                      "next": "pass these clips to: assemble.py edit --clips ..."}, indent=2))


def normalize_clip(src, dst, w, h, fps, fit, mute, preset):
    info = probe(src)
    if not info["has_video"]:
        sys.exit(f"No video stream in {src}")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", src]
    use_silence = mute or not info["has_audio"]
    if use_silence:
        cmd += ["-f", "lavfi", "-t", str(info["duration"]),
                "-i", "anullsrc=channel_layout=stereo:sample_rate=48000"]
    vf = fit_filter(w, h, fit, "0:v", "vfit") + f";[vfit]fps={fps},format=yuv420p[v]"
    if use_silence:
        af = "[1:a]aresample=48000,aformat=channel_layouts=stereo[a]"
    else:
        af = "[0:a]aresample=48000,aformat=channel_layouts=stereo[a]"
    cmd += ["-filter_complex", vf + ";" + af, "-map", "[v]", "-map", "[a]",
            "-t", str(info["duration"])] + enc_args(preset, 16) + [dst]
    run(cmd)
    return probe(dst)["duration"]


def join_clips(norm, durs, xfade, tmp, preset):
    joined = os.path.join(tmp, "joined.mp4")
    if xfade <= 0 or len(norm) == 1:
        lst = os.path.join(tmp, "list.txt")
        with open(lst, "w", encoding="utf-8") as f:
            for p in norm:
                safe = p.replace("\\", "/").replace("'", "'\\''")  # forward slashes work on Windows too
                f.write("file '" + safe + "'\n")
        run(["ffmpeg", "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
             "-c", "copy", "-movflags", "+faststart", joined])
        return joined
    shortest = min(durs)
    if xfade >= shortest:
        sys.exit(f"--xfade {xfade}s must be shorter than the shortest clip ({shortest:.2f}s)")
    cmd = ["ffmpeg", "-y", "-v", "error"]
    for p in norm:
        cmd += ["-i", p]
    parts, vprev, aprev, length = [], "0:v", "0:a", durs[0]
    for i in range(1, len(norm)):
        vout, aout = f"v{i}", f"a{i}"
        offset = length - xfade
        parts.append(f"[{vprev}][{i}:v]xfade=transition=fade:duration={xfade}:offset={offset:.3f}[{vout}]")
        parts.append(f"[{aprev}][{i}:a]acrossfade=d={xfade}[{aout}]")
        vprev, aprev, length = vout, aout, length + durs[i] - xfade
    cmd += ["-filter_complex", ";".join(parts), "-map", f"[{vprev}]", "-map", f"[{aprev}]"]
    run(cmd + enc_args(preset, 16) + [joined])
    return joined


def cmd_edit(a):
    need("ffmpeg")
    need("ffprobe")
    w, h = size_for(a.ratio, a.size)
    for p in a.clips + [x for x in (a.voice, a.music, a.subs) if x]:
        if not os.path.isfile(p):
            sys.exit(f"File not found: {p}")
    out = os.path.abspath(a.out)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="takewright_") as tmp:
        norm, durs = [], []
        for i, clip in enumerate(a.clips):
            dst = os.path.join(tmp, f"n{i:03d}.mp4")
            durs.append(normalize_clip(os.path.abspath(clip), dst, w, h, a.fps, a.fit, a.mute_clips, "veryfast"))
            norm.append(dst)
        joined = join_clips(norm, durs, a.xfade, tmp, "veryfast")
        video_len = probe(joined)["duration"]
        voice_end = (a.voice_start + probe(os.path.abspath(a.voice))["duration"]) if a.voice else 0.0
        if str(a.hold_end).lower() == "auto":
            hold = max(0.0, voice_end - video_len + 0.5) if a.voice else 0.0
        else:
            try:
                hold = max(0.0, float(a.hold_end))
            except ValueError:
                sys.exit("--hold-end must be a number of seconds or 'auto'")
        total = video_len + hold  # final length incl. held last frame
        warnings = []
        if a.voice and voice_end > total + 0.05:
            warnings.append(f"Voiceover ends at {voice_end:.1f}s but the video is {total:.1f}s: the last "
                            f"{voice_end - total:.1f}s of voice is cut. Use --hold-end auto, or add/lengthen shots.")

        cmd = ["ffmpeg", "-y", "-v", "error", "-i", joined]
        idx = 1
        vchain = "0:v"  # plain stream specifier when no video filters are applied
        vfilters = []
        if hold > 0:  # freeze the last frame so titles/CTA have room
            vfilters.append(f"tpad=stop_mode=clone:stop_duration={hold:.3f}")
        if a.subs:
            shutil.copyfile(a.subs, os.path.join(tmp, "subs.srt"))
            with open(a.subs, encoding="utf-8", errors="replace") as f:
                has_cjk = bool(CJK_RE.search(f.read()))
            font = a.font or (default_cjk_font() if has_cjk else "Arial")
            fsize = a.font_size or (11 if h > w else 16)
            margin = a.margin_v or (60 if h > w else 22)
            style = (f"FontName={font},FontSize={fsize},PrimaryColour=&H00FFFFFF,"
                     f"OutlineColour=&H00000000,BorderStyle=1,Outline=1.2,Shadow=0,MarginV={margin}")
            vfilters.append(f"subtitles=subs.srt:force_style='{style}'")
        if a.fade > 0:
            vfilters.append(f"fade=t=in:st=0:d={a.fade}")
            vfilters.append(f"fade=t=out:st={max(0.0, total - a.fade):.3f}:d={a.fade}")
        graph = []
        if vfilters:
            graph.append(f"[0:v]{','.join(vfilters)}[vout]")
            vchain = "[vout]"

        pad = f",apad=pad_dur={hold:.3f}" if hold > 0 else ""
        mix_inputs = [f"[0:a]volume={a.clip_volume}{pad}[base]"]
        labels = ["[base]"]
        voice_label = None
        if a.voice:
            cmd += ["-i", os.path.abspath(a.voice)]
            mix_inputs.append(f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,"
                              f"adelay={int(a.voice_start * 1000)}:all=1,volume={a.voice_volume},apad[voice]")
            idx += 1
            if a.music and a.duck:
                mix_inputs.append("[voice]asplit=2[voice1][voicesc]")
                labels.append("[voice1]")
                voice_label = "[voicesc]"
            else:
                labels.append("[voice]")
        if a.music:
            cmd += ["-stream_loop", "-1", "-i", os.path.abspath(a.music)]
            music = (f"[{idx}:a]aresample=48000,aformat=channel_layouts=stereo,"
                     f"atrim=duration={total:.3f},volume={a.music_volume}")
            idx += 1
            if voice_label:
                mix_inputs.append(music + "[mus]")
                mix_inputs.append(f"[mus]{voice_label}sidechaincompress=threshold=0.03:ratio=8:"
                                  f"attack=20:release=400[musd]")
                labels.append("[musd]")
            else:
                mix_inputs.append(music + "[musd]")
                labels.append("[musd]")
        n = len(labels)
        afilters = []
        if n > 1:
            mix = (f"{''.join(labels)}amix=inputs={n}:duration=first:dropout_transition=0,"
                   f"volume={n}")
        else:
            mix = "[base]anull"
        afilters.append(mix)
        if a.loudness is not None:
            afilters.append(f"loudnorm=I={a.loudness}:TP=-1.5:LRA=11,aresample=48000")
        if a.fade > 0:
            afilters.append(f"afade=t=in:st=0:d={a.fade}")
            afilters.append(f"afade=t=out:st={max(0.0, total - a.fade):.3f}:d={a.fade}")
        graph += mix_inputs
        graph.append(",".join(afilters) + "[aout]")
        cmd += ["-filter_complex", ";".join(graph), "-map", vchain, "-map", "[aout]",
                "-t", f"{total:.3f}"] + enc_args(a.preset, a.crf) + [out]
        run(cmd, cwd=tmp)
    result = probe(out)
    result["held_end_seconds"] = round(hold, 3)
    result["warnings"] = warnings
    for w_ in warnings:
        print("WARNING: " + w_, file=sys.stderr)
    print(json.dumps(result, indent=2))


def cmd_variants(a):
    need("ffmpeg")
    info = probe(a.file)
    stem, ext = os.path.splitext(os.path.abspath(a.file))
    results = []
    for r in a.ratios:
        w, h = size_for(r)
        dest = f"{stem}_{r.replace(':', 'x')}{ext or '.mp4'}"
        cmd = ["ffmpeg", "-y", "-v", "error", "-i", a.file, "-filter_complex",
               fit_filter(w, h, a.fit, "0:v", "v"), "-map", "[v]"]
        if info["has_audio"]:
            cmd += ["-map", "0:a", "-c:a", "copy"]
        cmd += ["-c:v", "libx264", "-preset", a.preset, "-crf", str(a.crf), "-pix_fmt", "yuv420p",
                "-movflags", "+faststart", dest]
        run(cmd)
        results.append(dest)
    print(json.dumps({"variants": results}, indent=2))


def cmd_cover(a):
    need("ffmpeg")
    info = probe(a.file)
    t = min(max(0.0, a.at), max(0.0, info["duration"] - 0.05))
    dest = a.out or os.path.splitext(a.file)[0] + "_cover.jpg"
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{t:.3f}", "-i", a.file, "-frames:v", "1",
         "-q:v", "2", dest])
    print(json.dumps({"cover": dest, "at": round(t, 3)}, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Takewright editing tool (ffmpeg)")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("probe", help="file info + ListenHub meta string")
    p.add_argument("file")
    p.set_defaults(fn=cmd_probe)

    p = sub.add_parser("frames", help="QC frames")
    p.add_argument("file")
    p.add_argument("--count", type=int, default=5)
    p.add_argument("--outdir")
    p.set_defaults(fn=cmd_frames)

    p = sub.add_parser("trim", help="cut a clip (re-encodes for frame accuracy)")
    p.add_argument("file")
    p.add_argument("--start", type=float, required=True)
    p.add_argument("--end", type=float, required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--preset", default="medium")
    p.add_argument("--crf", type=int, default=18)
    p.set_defaults(fn=cmd_trim)

    p = sub.add_parser("srt", help="captions from a script (one caption per line)")
    p.add_argument("--text", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--start", type=float, default=0.0)
    p.add_argument("--wps", type=float, default=2.5, help="words per second (Latin text)")
    p.add_argument("--cps", type=float, default=4.0, help="characters per second (CJK text)")
    p.add_argument("--min", type=float, default=1.2, help="minimum seconds per caption")
    p.add_argument("--gap", type=float, default=0.1)
    p.add_argument("--fit-to", help="voiceover file: stretch/squeeze timings to its real length")
    p.set_defaults(fn=cmd_srt)

    p = sub.add_parser("edit", help="join clips + captions + voice + music")
    p.add_argument("--clips", nargs="+", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--ratio", default="9:16")
    p.add_argument("--size", help="exact WxH, overrides --ratio")
    p.add_argument("--fit", choices=["crop", "pad", "blur"], default="crop")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--xfade", type=float, default=0.0, help="crossfade seconds between clips")
    p.add_argument("--mute-clips", action="store_true", help="drop the clips' own audio")
    p.add_argument("--clip-volume", type=float, default=1.0)
    p.add_argument("--voice")
    p.add_argument("--voice-start", type=float, default=0.0)
    p.add_argument("--voice-volume", type=float, default=1.0)
    p.add_argument("--music")
    p.add_argument("--music-volume", type=float, default=0.25)
    p.add_argument("--duck", action="store_true", help="lower music under the voice")
    p.add_argument("--subs", help="SRT file to burn in")
    p.add_argument("--font")
    p.add_argument("--font-size", type=int)
    p.add_argument("--margin-v", type=int)
    p.add_argument("--fade", type=float, default=0.0, help="fade in/out seconds at start and end")
    p.add_argument("--hold-end", default="0", help="freeze the last frame N seconds (title/CTA room); 'auto' = extend to fit the voiceover")
    p.add_argument("--loudness", type=float, default=-14.0, help="target LUFS; use --no-loudnorm to skip")
    p.add_argument("--no-loudnorm", dest="loudness", action="store_const", const=None)
    p.add_argument("--preset", default="medium")
    p.add_argument("--crf", type=int, default=18)
    p.set_defaults(fn=cmd_edit)

    p = sub.add_parser("stills", help="photos -> clips with a slow push-in")
    p.add_argument("images", nargs="+")
    p.add_argument("--outdir", default="./takewright-output/stills")
    p.add_argument("--duration", type=float, default=4.0, help="seconds per photo")
    p.add_argument("--zoom", type=float, default=0.08, help="push-in amount (0 = static)")
    p.add_argument("--ratio", default="9:16")
    p.add_argument("--size")
    p.add_argument("--fit", choices=["crop", "pad", "blur"], default="blur")
    p.add_argument("--fps", type=int, default=30)
    p.add_argument("--preset", default="medium")
    p.set_defaults(fn=cmd_stills)

    p = sub.add_parser("variants", help="other aspect ratios from one edit")
    p.add_argument("file")
    p.add_argument("--ratios", nargs="+", required=True)
    p.add_argument("--fit", choices=["crop", "pad", "blur"], default="blur")
    p.add_argument("--preset", default="medium")
    p.add_argument("--crf", type=int, default=18)
    p.set_defaults(fn=cmd_variants)

    p = sub.add_parser("cover", help="cover image from a frame")
    p.add_argument("file")
    p.add_argument("--at", type=float, default=1.0)
    p.add_argument("--out")
    p.set_defaults(fn=cmd_cover)

    a = ap.parse_args()
    a.fn(a)


if __name__ == "__main__":
    main()
