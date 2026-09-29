"""Build stores.json from a folder of store documents (one <doc id>.json per store).

Usage: python3 sync.py <docs dir> [stores.json]
Only stores whose Naver info is filled in (status "ok") are published.
"""
import json, os, sys, glob
from datetime import datetime, timezone

src = sys.argv[1]
out = sys.argv[2] if len(sys.argv) > 2 else os.path.join(os.path.dirname(os.path.abspath(__file__)), "stores.json")

stores = []
for f in sorted(glob.glob(os.path.join(src, "*.json"))):
    with open(f, encoding="utf-8") as fh:
        d = json.load(fh)
    if d.get("status") != "ok" or not d.get("naver"):
        continue
    stores.append({
        "doc": os.path.splitext(os.path.basename(f))[0],
        "name": d.get("name", ""),
        "status": "ok",
        "addedAt": d.get("addedAt", ""),
        "memo": d.get("memo", ""),
        "naver": d["naver"],
    })

new_body = json.dumps(stores, ensure_ascii=False, sort_keys=True)
try:
    with open(out, encoding="utf-8") as fh:
        old = json.load(fh)
    if json.dumps(old.get("stores", []), ensure_ascii=False, sort_keys=True) == new_body:
        print("unchanged", len(stores))
        sys.exit(0)
except (FileNotFoundError, ValueError):
    pass

with open(out, "w", encoding="utf-8", newline="\n") as fh:
    json.dump({"updatedAt": datetime.now(timezone.utc).isoformat(timespec="seconds"), "stores": stores},
              fh, ensure_ascii=False, indent=1)
print("updated", len(stores))
