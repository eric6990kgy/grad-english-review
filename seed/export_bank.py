"""Writes bank.json for the standalone (GitHub Pages) build from an ArtifactData export of the `bank` collection.

Usage: python export_bank.py <dir containing bank/*.json> <output bank.json>
Only the shared question bank is exported; nothing under data/users/ (progress, essays) is included.
"""
import glob, json, os, sys, time

src, out = sys.argv[1], sys.argv[2]
packs = []
for f in sorted(glob.glob(os.path.join(src, "bank", "*.json"))):
    data = json.load(open(f, encoding="utf-8"))
    packs.append({"id": os.path.basename(f)[:-5], **data})
packs.sort(key=lambda p: (p.get("createdAt", 0), p["id"]))
with open(out, "w", encoding="utf-8") as fh:
    json.dump({"exportedAt": int(time.time() * 1000), "packs": packs}, fh, ensure_ascii=False, separators=(",", ":"))
count = lambda t: sum(1 for p in packs for i in p["items"] if i.get("type") == t)
print(f"packs={len(packs)} vocab={count('vocab')} mc={count('mc')} passages={count('passage')} prompts={count('prompt')}")
