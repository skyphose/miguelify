#!/usr/bin/env python3
"""Package miguelify-pro as a standalone skill zip for Claude settings / Cowork.

Usage:  build_pro_bundle.py [OUT_DIR]      default OUT_DIR: dist/ in the repo

Writes OUT_DIR/miguelify-pro.zip with one top-level folder, miguelify-pro/, holding
SKILL.md, the linter and the reference files it reads. The file list is explicit:
references/private.md and the extracted corpus never go in, whatever is on disk.
The zip is rebuilt from scratch every run.
"""
import os
import sys
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAME = "miguelify-pro"
FILES = [
    ("pro/SKILL.md", "SKILL.md"),
    ("tools/voicecheck.py", "tools/voicecheck.py"),
    ("references/ai-tells.md", "references/ai-tells.md"),
    ("references/voice.md", "references/voice.md"),
    ("references/surfaces.md", "references/surfaces.md"),
    ("references/profile.json", "references/profile.json"),
    ("references/jargon.txt", "references/jargon.txt"),
    ("LICENSE", "LICENSE"),
]
NEVER = ("private", "corpus")


def main(argv):
    out_dir = os.path.abspath(argv[0]) if argv else os.path.join(ROOT, "dist")
    os.makedirs(out_dir, exist_ok=True)
    out = os.path.join(out_dir, f"{NAME}.zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for src, dst in FILES:
            if any(word in dst for word in NEVER):
                raise SystemExit(f"refusing to bundle {dst}")
            zf.write(os.path.join(ROOT, src), f"{NAME}/{dst}")
    with zipfile.ZipFile(out) as zf:
        names = zf.namelist()
    print(out)
    for n in names:
        print("  " + n)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
