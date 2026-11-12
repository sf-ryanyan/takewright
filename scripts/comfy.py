#!/usr/bin/env python3
"""Takewright ComfyUI runner: queue an API-format workflow, wait, download outputs.

Usage:
  python comfy.py check  [--server URL]
  python comfy.py upload IMAGE [--server URL]
  python comfy.py run --workflow wf_api.json [--set NODE.INPUT=VALUE ...] [--out DIR]
                      [--server URL] [--timeout SECONDS]

The workflow must be exported with "File -> Export Workflow (API)".
Standard library only.
"""
import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid

DEFAULT_SERVER = "http://127.0.0.1:8188"


def http(method, url, data=None, headers=None, timeout=30):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def get_json(url, timeout=30):
    return json.loads(http("GET", url, timeout=timeout).decode("utf-8"))


def parse_value(raw):
    if raw.startswith("str:"):  # force text, e.g. --set 6.text=str:2026
        return raw[4:]
    low = raw.lower()
    if low in ("true", "false"):
        return low == "true"
    for cast in (int, float):
        try:
            return cast(raw)
        except ValueError:
            pass
    return raw


def apply_sets(workflow, sets):
    for item in sets:
        if "=" not in item or "." not in item.split("=", 1)[0]:
            sys.exit(f"Bad --set '{item}'. Use NODE.INPUT=VALUE, e.g. 6.text=\"a lake\"")
        key, raw = item.split("=", 1)
        node, field = key.split(".", 1)
        if node not in workflow:
            sys.exit(f"Node '{node}' not in workflow. Available: {', '.join(sorted(workflow))}")
        if "inputs" not in workflow[node]:
            sys.exit(f"Node '{node}' has no inputs. Is this an API-format export?")
        workflow[node]["inputs"][field] = parse_value(raw)
    return workflow


def looks_like_api_format(wf):
    return isinstance(wf, dict) and wf and all(
        isinstance(v, dict) and "class_type" in v for v in wf.values())


def cmd_check(args):
    try:
        stats = get_json(args.server.rstrip("/") + "/system_stats", timeout=5)
    except (urllib.error.URLError, OSError) as e:
        sys.exit(f"ComfyUI not reachable at {args.server}: {e}. Start ComfyUI or fix the port.")
    devices = stats.get("devices", [])
    print(json.dumps({"ok": True, "server": args.server,
                      "comfyui": stats.get("system", {}).get("comfyui_version"),
                      "devices": [{"name": d.get("name"),
                                   "vram_total_gb": round(d.get("vram_total", 0) / 1024 ** 3, 1)}
                                  for d in devices]}, indent=2))


def cmd_upload(args):
    path = args.image
    if not os.path.isfile(path):
        sys.exit(f"File not found: {path}")
    boundary = uuid.uuid4().hex
    name = os.path.basename(path)
    ctype = mimetypes.guess_type(name)[0] or "application/octet-stream"
    with open(path, "rb") as f:
        content = f.read()
    body = b"".join([
        f"--{boundary}\r\n".encode(),
        f'Content-Disposition: form-data; name="image"; filename="{name}"\r\n'.encode(),
        f"Content-Type: {ctype}\r\n\r\n".encode(), content, b"\r\n",
        f"--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="overwrite"\r\n\r\ntrue\r\n',
        f"--{boundary}--\r\n".encode(),
    ])
    res = json.loads(http("POST", args.server.rstrip("/") + "/upload/image", data=body,
                          headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}))
    stored = res.get("name", name)
    if res.get("subfolder"):
        stored = f"{res['subfolder']}/{stored}"
    print(json.dumps({"ok": True, "image": stored}, indent=2))


def collect_files(outputs):
    """Unique output files; skip 'temp' previews when real outputs exist."""
    seen, files = set(), []
    for node_out in outputs.values():
        for items in node_out.values():
            if isinstance(items, list):
                for it in items:
                    if isinstance(it, dict) and it.get("filename"):
                        key = (it["filename"], it.get("subfolder", ""), it.get("type", "output"))
                        if key not in seen:
                            seen.add(key)
                            files.append(it)
    real = [f for f in files if f.get("type", "output") != "temp"]
    return real or files


def cmd_run(args):
    with open(args.workflow, encoding="utf-8") as f:
        wf = json.load(f)
    if not looks_like_api_format(wf):
        sys.exit("This is not an API-format workflow. In ComfyUI use File -> Export Workflow (API).")
    wf = apply_sets(wf, args.set or [])
    server = args.server.rstrip("/")
    payload = json.dumps({"prompt": wf, "client_id": uuid.uuid4().hex}).encode()
    try:
        res = json.loads(http("POST", server + "/prompt", data=payload,
                              headers={"Content-Type": "application/json"}))
    except urllib.error.HTTPError as e:
        sys.exit(f"ComfyUI rejected the workflow (HTTP {e.code}): {e.read().decode('utf-8', 'replace')[:2000]}")
    except (urllib.error.URLError, OSError) as e:
        sys.exit(f"ComfyUI not reachable at {server}: {e}")
    if res.get("node_errors"):
        sys.exit("Node errors: " + json.dumps(res["node_errors"])[:2000])
    pid = res["prompt_id"]
    print(f"queued prompt_id={pid}", file=sys.stderr)

    deadline = time.time() + args.timeout
    entry = None
    while time.time() < deadline:
        hist = get_json(f"{server}/history/{pid}")
        if pid in hist:
            entry = hist[pid]
            status = entry.get("status", {})
            if status.get("completed") or status.get("status_str") in ("success", "error"):
                break
        time.sleep(args.poll)
    if entry is None:
        sys.exit(f"Timed out after {args.timeout}s. Check later: {server}/history/{pid}")
    status = entry.get("status", {})
    if status.get("status_str") == "error":
        sys.exit("Generation failed: " + json.dumps(status.get("messages", []))[:2000])

    os.makedirs(args.out, exist_ok=True)
    saved = []
    for it in collect_files(entry.get("outputs", {})):
        q = urllib.parse.urlencode({"filename": it["filename"], "subfolder": it.get("subfolder", ""),
                                    "type": it.get("type", "output")})
        data = http("GET", f"{server}/view?{q}", timeout=300)
        dest = os.path.join(args.out, it["filename"])
        base, ext = os.path.splitext(dest)
        n = 2
        while os.path.exists(dest):
            dest = f"{base}-{n}{ext}"
            n += 1
        with open(dest, "wb") as f:
            f.write(data)
        saved.append(dest)
    print(json.dumps({"ok": True, "prompt_id": pid, "files": saved}, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Run ComfyUI workflows for Takewright")
    ap.add_argument("--server", default=DEFAULT_SERVER)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    up = sub.add_parser("upload")
    up.add_argument("image")
    rn = sub.add_parser("run")
    rn.add_argument("--workflow", required=True)
    rn.add_argument("--set", action="append", metavar="NODE.INPUT=VALUE")
    rn.add_argument("--out", default="./takewright-output")
    rn.add_argument("--timeout", type=int, default=3600)
    rn.add_argument("--poll", type=float, default=3.0)
    for p in (up, rn, sub.choices["check"]):
        p.add_argument("--server", default=argparse.SUPPRESS)
    args = ap.parse_args()
    {"check": cmd_check, "upload": cmd_upload, "run": cmd_run}[args.cmd](args)


if __name__ == "__main__":
    main()
