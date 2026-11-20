#!/usr/bin/env python3
"""Render a Mermaid .mmd file to PNG (doubles as a syntax check).

Usage: python3 render_mermaid.py diagram.mmd [--out-dir DIR] [--keep-source]

On success the source .mmd is deleted (the Mermaid lives in the companion .md),
unless --keep-source is given. On failure it is kept so it can be fixed.

Tries `mmdc`, then `npx -y @mermaid-js/mermaid-cli`. If neither works,
writes a self-contained HTML page that renders the diagram in a browser.
Exit code 0 = rendered (or HTML fallback written), 1 = Mermaid syntax/render error.
"""
import argparse
import html
import shutil
import subprocess
import sys
from pathlib import Path


def find_cli():
    if shutil.which("mmdc"):
        return ["mmdc"]
    if shutil.which("npx"):
        return ["npx", "-y", "@mermaid-js/mermaid-cli"]
    return None


def render(cli, src, out):
    cmd = cli + ["-i", str(src), "-o", str(out), "-b", "white"]
    if out.suffix == ".png":
        cmd += ["-s", "2"]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=180)


def html_fallback(src, out_dir):
    page = out_dir / (src.stem + ".html")
    page.write_text(
        "<!DOCTYPE html><html><head><meta charset='utf-8'><title>"
        + html.escape(src.stem)
        + "</title></head><body style='background:#fff'>"
        + "<pre class='mermaid'>" + html.escape(src.read_text()) + "</pre>"
        + "<script type='module'>import mermaid from "
        + "'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';"
        + "mermaid.initialize({startOnLoad:true});</script></body></html>"
    )
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mmd")
    ap.add_argument("--out-dir")
    ap.add_argument("--keep-source", action="store_true")
    a = ap.parse_args()
    src = Path(a.mmd).resolve()
    out_dir = Path(a.out_dir).resolve() if a.out_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)

    cli = find_cli()
    if cli:
        ok = True
        for ext in (".png",):
            out = out_dir / (src.stem + ext)
            try:
                r = render(cli, src, out)
            except subprocess.TimeoutExpired:
                r = None
            if r is None or r.returncode != 0 or not out.exists():
                err = (r.stderr or r.stdout) if r else "timed out"
                if "Parse error" in err or "Syntax error" in err or "Lexical error" in err:
                    lines = []
                    for ln in err.strip().splitlines():
                        if ln.strip().startswith(("at ", "Parser.")):
                            break
                        lines.append(ln)
                    print("MERMAID SYNTAX ERROR:\n" + "\n".join(lines[-12:]))
                    sys.exit(1)
                print(f"render to {ext} failed: {err.strip()[-800:]}")
                ok = False
                break
            print(f"wrote {out}")
        if ok:
            if not a.keep_source:
                src.unlink()
                print(f"removed {src}")
            return
    page = html_fallback(src, out_dir)
    print(f"mermaid-cli unavailable; wrote browser-rendered fallback {page}")
    print("Note: this fallback does NOT validate syntax.")
    if not a.keep_source:
        src.unlink()
        print(f"removed {src}")


if __name__ == "__main__":
    main()
