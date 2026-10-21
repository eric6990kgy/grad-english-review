"""Builds the GitHub Pages site in docs/: index.html wrapped in the document skeleton the Artifact
publisher normally adds, plus bank.json (from export_bank.py).

Usage: python seed/build_site.py   (run from english-review/, after export_bank.py wrote docs/bank.json)
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HEAD = """<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"><style>
:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
body{margin:0;font:14px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}img{max-width:100%}[hidden]{display:none!important}
</style></head><body>"""
page = open(os.path.join(ROOT, "index.html"), encoding="utf-8").read()
os.makedirs(os.path.join(ROOT, "docs"), exist_ok=True)
with open(os.path.join(ROOT, "docs", "index.html"), "w", encoding="utf-8") as f:
    f.write(HEAD + page + "</body></html>\n")
open(os.path.join(ROOT, "docs", ".nojekyll"), "w").close()
print("docs/index.html written")
