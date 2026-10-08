#!/usr/bin/env python3
"""检查 Markdown 相对链接是否存在（外部链接与锚点不校验）。"""
import os
import re
import sys

LINK = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
SKIP_PREFIX = ("http://", "https://", "mailto:", "#", "tel:")

missing = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if d not in {".git", "node_modules"}]
    for name in files:
        if not name.endswith(".md"):
            continue
        path = os.path.join(root, name)
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
        for raw in LINK.findall(text):
            target = raw.split("#", 1)[0].strip()
            if not target or target.startswith(SKIP_PREFIX):
                continue
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            resolved = os.path.normpath(os.path.join(os.path.dirname(path), target))
            if not os.path.exists(resolved):
                missing.append(f"{path}: {raw}")

if missing:
    print("broken relative links:")
    for item in missing:
        print("  " + item)
    sys.exit(1)

print("all relative links resolve")
