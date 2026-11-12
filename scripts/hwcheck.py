#!/usr/bin/env python3
"""Takewright hardware check: is this computer suitable for local AI video?

Usage: python hwcheck.py [--json] [--comfy http://127.0.0.1:8188]
Standard library only. Never fails hard: unknown values are reported as null.
"""
import argparse
import ctypes
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request


def run(cmd, timeout=10):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        if out.returncode == 0:
            return out.stdout.strip()
    except (OSError, subprocess.SubprocessError):
        pass
    return None


def ram_gb():
    system = platform.system()
    try:
        if system == "Linux":
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal:"):
                        return round(int(line.split()[1]) / 1024 / 1024, 1)
        elif system == "Darwin":
            val = run(["sysctl", "-n", "hw.memsize"])
            if val:
                return round(int(val) / 1024 ** 3, 1)
        elif system == "Windows":
            class MEMORYSTATUSEX(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                            ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                            ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                            ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                            ("sullAvailExtendedVirtual", ctypes.c_ulonglong)]
            stat = MEMORYSTATUSEX()
            stat.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
                return round(stat.ullTotalPhys / 1024 ** 3, 1)
    except Exception:
        pass
    return None


def find_nvidia_smi():
    exe = shutil.which("nvidia-smi")
    if exe:
        return exe
    if platform.system() == "Windows":  # older drivers install it outside PATH
        for base in (os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("SystemRoot", r"C:\Windows")):
            for sub in (r"NVIDIA Corporation\NVSMI\nvidia-smi.exe", r"System32\nvidia-smi.exe"):
                cand = os.path.join(base, sub)
                if os.path.isfile(cand):
                    return cand
    return None


def nvidia_gpus():
    exe = find_nvidia_smi()
    if not exe:
        return []
    out = run([exe, "--query-gpu=name,memory.total,driver_version,compute_cap",
               "--format=csv,noheader,nounits"])
    if out is None:  # older drivers do not know compute_cap
        out = run([exe, "--query-gpu=name,memory.total,driver_version",
                   "--format=csv,noheader,nounits"])
    gpus = []
    for line in (out or "").splitlines():
        parts = [p.strip() for p in line.split(",")]
        if len(parts) < 3:
            continue
        try:
            vram = round(float(parts[1]) / 1024, 1)
        except ValueError:
            vram = None
        cc = None
        if len(parts) > 3:
            try:
                cc = float(parts[3])
            except ValueError:
                cc = None
        gpus.append({"vendor": "NVIDIA", "name": parts[0], "vram_gb": vram,
                     "driver": parts[2], "compute_cap": cc})
    return gpus


def other_gpus():
    system = platform.system()
    names = []
    if system == "Windows":
        out = run(["powershell", "-NoProfile", "-Command",
                   "(Get-CimInstance Win32_VideoController).Name"], timeout=20)
        names = [n.strip() for n in (out or "").splitlines() if n.strip()]
    elif system == "Darwin":
        out = run(["system_profiler", "SPDisplaysDataType"], timeout=20)
        names = [l.split(":", 1)[1].strip() for l in (out or "").splitlines()
                 if "Chipset Model" in l]
    elif system == "Linux":
        out = run(["lspci"])
        names = [l.split(":", 2)[-1].strip() for l in (out or "").splitlines()
                 if "VGA" in l or "3D controller" in l]
    return [{"vendor": "other", "name": n, "vram_gb": None} for n in names]


def apple_silicon():
    return platform.system() == "Darwin" and platform.machine() in ("arm64", "aarch64")


def comfy_up(url):
    try:
        with urllib.request.urlopen(url.rstrip("/") + "/system_stats", timeout=3) as r:
            return r.status == 200
    except Exception:
        return False


def tier(gpus, mac_arm):
    if mac_arm:
        return "MAC", "Apple Silicon: cloud for video generation; local for images and editing."
    nv = [g for g in gpus if g.get("vendor") == "NVIDIA" and g.get("vram_gb")]
    if not nv:
        return "T0", "No usable NVIDIA GPU found: use cloud or manual for generation; edit locally with ffmpeg."
    best = max(nv, key=lambda g: g["vram_gb"])
    vram, cc = best["vram_gb"], best.get("compute_cap")
    if cc is not None and cc < 7.0:
        return "T0", (f"{best['name']} ({vram} GB) is an older architecture (compute {cc}); "
                      "video models will be very slow or unsupported. Cloud recommended; editing stays local.")
    if vram < 7.5:
        return "T0", f"{best['name']} has {vram} GB VRAM: too little for video models. Use cloud/manual."
    if vram < 11.5:
        return "T1", f"{best['name']} ({vram} GB): light models (LTX-Video, Wan 2.2 5B FP8 + offload) for drafts; cloud finals."
    if vram < 23.5:
        return "T2", f"{best['name']} ({vram} GB): Wan 2.x 14B (quantized on 12 GB), HunyuanVideo 1.5 with offload."
    return "T3", f"{best['name']} ({vram} GB): all mainstream open video models at full quality."


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--json", action="store_true", help="print JSON only")
    ap.add_argument("--comfy", default="http://127.0.0.1:8188", help="ComfyUI URL to probe")
    args = ap.parse_args()

    gpus = nvidia_gpus() or other_gpus()
    mac_arm = apple_silicon()
    disk_free = round(shutil.disk_usage(os.getcwd()).free / 1024 ** 3, 1)
    t, advice = tier(gpus, mac_arm)
    report = {
        "os": f"{platform.system()} {platform.release()}",
        "machine": platform.machine(),
        "cpu": platform.processor() or None,
        "cpu_cores": os.cpu_count(),
        "ram_gb": ram_gb(),
        "disk_free_gb_here": disk_free,
        "gpus": gpus,
        "apple_silicon": mac_arm,
        "python": platform.python_version(),
        "ffmpeg": bool(shutil.which("ffmpeg")),
        "ffprobe": bool(shutil.which("ffprobe")),
        "comfyui_running": comfy_up(args.comfy),
        "tier": t,
        "advice": advice,
        "warnings": [],
    }
    if report["ram_gb"] is not None and report["ram_gb"] < 32 and t in ("T1", "T2"):
        report["warnings"].append("Less than 32 GB RAM: model offloading may be slow or fail.")
    if disk_free < 50 and t != "T0":
        report["warnings"].append("Less than 50 GB free here: video models need 30-100 GB.")
    if not report["ffmpeg"]:
        report["warnings"].append("ffmpeg not found: needed for frame checks and editing.")

    if args.json:
        print(json.dumps(report, indent=2))
        return
    print("Takewright hardware check")
    print(f"  OS: {report['os']} ({report['machine']}), CPU cores: {report['cpu_cores']}, RAM: {report['ram_gb']} GB")
    print(f"  Free disk here: {disk_free} GB")
    if gpus:
        for g in gpus:
            extra = f", compute {g['compute_cap']}" if g.get("compute_cap") else ""
            vram = f"{g['vram_gb']} GB" if g.get("vram_gb") else "VRAM unknown"
            print(f"  GPU: {g['name']} ({vram}{extra})")
    else:
        print("  GPU: none detected")
    print(f"  ffmpeg: {'yes' if report['ffmpeg'] else 'no'} · ComfyUI running: {'yes' if report['comfyui_running'] else 'no'}")
    print(f"  Tier: {t} — {advice}")
    for w in report["warnings"]:
        print(f"  ! {w}")


if __name__ == "__main__":
    sys.exit(main())
