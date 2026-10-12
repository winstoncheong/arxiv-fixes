#!/usr/bin/env python3
"""Assemble the GitHub Pages site directory per plan.html section 5.

Merges freshly built PDFs (downloaded CI artifacts) with the previously
deployed PDFs fetched from the live site, so unchanged papers keep their
existing files. Copies the generated index pages plus per-directory
readme files. Nothing built ever flows back into git.

Fresh-artifact layout (from actions/download-artifact with pattern 'pdf-*'):
    <fresh>/pdf-<dirname>/<file>.pdf

Usage:
    python3 scripts/assemble_site.py --fresh _fresh --out public \
        --site-url https://winstoncheong.github.io/arxiv-fixes
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def paper_dirs():
    return sorted(p.parent for p in ROOT.glob("*/paper.json"))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--fresh", default="_fresh")
    ap.add_argument("--out", default="public")
    ap.add_argument("--site-url", required=True)
    ap.add_argument("--allow-missing", action="store_true",
                    help="warn instead of failing when a PDF is unavailable")
    args = ap.parse_args(argv)

    fresh = Path(args.fresh)
    out = Path(args.out)
    missing = []

    out.mkdir(parents=True, exist_ok=True)
    for name in ("index.html", "index.md"):
        src = ROOT / name
        if src.exists():
            (out / name).write_bytes(src.read_bytes())

    for d in paper_dirs():
        meta = json.loads((d / "paper.json").read_text(encoding="utf-8"))
        dest_dir = out / d.name
        dest_dir.mkdir(parents=True, exist_ok=True)
        for e in meta["entries"]:
            pdf = e["pdf"]
            candidate = fresh / f"pdf-{d.name}" / pdf
            dest = dest_dir / pdf
            if candidate.exists():
                dest.write_bytes(candidate.read_bytes())
                print(f"fresh: {d.name}/{pdf}")
            else:
                url = f"{args.site_url.rstrip('/')}/{d.name}/{pdf}"
                try:
                    with urllib.request.urlopen(url, timeout=60) as r:
                        dest.write_bytes(r.read())
                    print(f"fallback: {url}")
                except Exception as exc:
                    print(f"MISSING {d.name}/{pdf}: {exc}", file=sys.stderr)
                    missing.append(f"{d.name}/{pdf}")
        for readme in ("readme.md", "readme.html", "README.md"):
            src = d / readme
            if src.exists():
                (dest_dir / src.name).write_bytes(src.read_bytes())

    if missing and not args.allow_missing:
        print(f"{len(missing)} PDFs unavailable; aborting", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
