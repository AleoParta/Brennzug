#!/usr/bin/env python3
"""
Liest alle Bilder aus media/gallery/ und schreibt tabs/gallerie-data.js.
Nach jedem Hochladen neuer Bilder einmal ausführen:   python3 build_gallery.py
(im Hauptordner der Seite, dort wo index.html liegt)

Datum der Bilder (in dieser Reihenfolge):
1. WoW-Screenshots: aus dem Dateinamen  WoWScrnShot_MMTTJJ_HHMMSS.jpg
   (021520_125942 = 15.02.2020, 12:59:42)
2. sonst: Aufnahmedatum aus den EXIF-Daten (nur mit  pip install pillow)
3. sonst: Erstellungsdatum der Datei
"""
import json, os, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GALLERY = ROOT / "media" / "gallery"
OUT = ROOT / "tabs" / "gallerie-data.js"
EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".bmp"}
WOW = re.compile(r"WoWScrnShot_(\d{2})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", re.I)


def wow_date(name):
    m = WOW.search(name)
    if not m:
        return None
    mo, d, y, h, mi, s = (int(x) for x in m.groups())
    try:
        return datetime(2000 + y, mo, d, h, mi, s)
    except ValueError:
        return None


def exif_date(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            ex = im.getexif()
            raw = ex.get_ifd(0x8769).get(0x9003) or ex.get(0x0132)  # DateTimeOriginal / DateTime
            if raw:
                return datetime.strptime(str(raw).strip(), "%Y:%m:%d %H:%M:%S")
    except Exception:
        pass
    return None


def file_date(path):
    st = path.stat()
    ts = getattr(st, "st_birthtime", None)           # macOS
    if ts is None:
        ts = st.st_ctime if os.name == "nt" else st.st_mtime  # Windows: Erstellung, Linux: Änderung
    return datetime.fromtimestamp(ts)


def main():
    if not GALLERY.is_dir():
        sys.exit(f"Ordner nicht gefunden: {GALLERY}")
    images = []
    for p in GALLERY.iterdir():
        if p.is_file() and p.suffix.lower() in EXT:
            d = wow_date(p.name) or exif_date(p) or file_date(p)
            images.append({"file": p.name, "date": d.strftime("%Y-%m-%dT%H:%M:%S")})
    images.sort(key=lambda i: i["date"], reverse=True)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("window.GALLERY_DATA = " + json.dumps(images, ensure_ascii=False, indent=1) + ";\n",
                   encoding="utf-8")
    print(f"{len(images)} Bilder -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
