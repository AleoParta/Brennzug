#!/usr/bin/env python3
"""
Liest alle Bilder aus media/gallery/ und schreibt tabs/gallerie-data.js.
Nach jedem Hochladen neuer Bilder einmal ausführen:   python3 build_gallery.py
(im Hauptordner der Seite, dort wo index.html liegt)

Datum der Bilder (in dieser Reihenfolge):
1. WoW-Screenshots: aus dem Dateinamen  WoWScrnShot_MMTTJJ_HHMMSS.jpg
   (021520_125942 = 15.02.2020, 12:59:42)
2. Andere Dateinamen mit Datum, z. B.
   "Screenshot 2019-10-13 23.11.30.png"   (Windows/Snipping Tool, Steam, ...)
   "Screenshot_20200104-022740.png"       (Handy, Xbox Game Bar, ...)
   "2020-01-04.png" / "IMG_20200104_022740.jpg"
3. EXIF-Aufnahmedatum (nur mit  pip install pillow)
4. Dateidatum (das ältere aus Erstellungs- und Änderungsdatum)
"""
import json, os, re, sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
GALLERY = ROOT / "media" / "gallery"
OUT = ROOT / "tabs" / "gallerie-data.js"
EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif", ".bmp"}
WOW = re.compile(r"WoWScrnShot_(\d{2})(\d{2})(\d{2})_(\d{2})(\d{2})(\d{2})", re.I)
# JJJJ-MM-TT HH.MM.SS (Trenner zwischen den Teilen: - _ . : Leerzeichen oder T)
ISO_TIME = re.compile(r"(?<!\d)((?:19|20)\d{2})[-_.](\d{2})[-_.](\d{2})[T _.-]+(\d{2})[-_.:](\d{2})[-_.:](\d{2})(?!\d)")
# JJJJMMTT_HHMMSS (auch mit - oder Leerzeichen dazwischen)
COMPACT_TIME = re.compile(r"(?<!\d)((?:19|20)\d{2})(\d{2})(\d{2})[T _-](\d{2})(\d{2})(\d{2})(?!\d)")
# nur Datum: JJJJ-MM-TT
ISO_DATE = re.compile(r"(?<!\d)((?:19|20)\d{2})[-_.](\d{2})[-_.](\d{2})(?!\d)")


def _mk(y, mo, d, h=0, mi=0, s=0):
    try:
        dt = datetime(y, mo, d, h, mi, s)
    except ValueError:
        return None
    return dt if 2004 <= dt.year <= datetime.now().year + 1 else None


def name_date(name):
    """Datum aus dem Dateinamen lesen, sonst None."""
    m = WOW.search(name)
    if m:
        mo, d, y, h, mi, s = (int(x) for x in m.groups())
        r = _mk(2000 + y, mo, d, h, mi, s)
        if r:
            return r
    for rx in (ISO_TIME, COMPACT_TIME):
        m = rx.search(name)
        if m:
            r = _mk(*(int(x) for x in m.groups()))
            if r:
                return r
    m = ISO_DATE.search(name)
    if m:
        return _mk(*(int(x) for x in m.groups()))
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
    """Das ältere von Erstellungs- und Änderungsdatum.
    Beim Kopieren bekommt eine Datei ein neues Erstellungsdatum, das Änderungsdatum
    bleibt aber meist das Original. Deshalb nimmt man das frühere der beiden."""
    st = path.stat()
    ts = [st.st_mtime]
    if getattr(st, "st_birthtime", None):      # macOS
        ts.append(st.st_birthtime)
    if os.name == "nt":                        # Windows: ctime = Erstellungszeit
        ts.append(st.st_ctime)
    return datetime.fromtimestamp(min(ts))


def main():
    if not GALLERY.is_dir():
        sys.exit(f"Ordner nicht gefunden: {GALLERY}")
    images, skipped = [], []
    for p in sorted(GALLERY.iterdir()):
        if p.name.startswith("."):
            continue
        if p.is_dir():
            skipped.append(f"{p.name}/  (Unterordner werden nicht durchsucht)")
        elif p.suffix.lower() in EXT:
            d = name_date(p.name) or exif_date(p) or file_date(p)
            images.append({"file": p.name, "date": d.strftime("%Y-%m-%dT%H:%M:%S")})
        else:
            skipped.append(f"{p.name}  (Format {p.suffix or 'ohne Endung'} wird nicht unterstützt)")
    images.sort(key=lambda i: i["date"], reverse=True)

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text("window.GALLERY_DATA = " + json.dumps(images, ensure_ascii=False, indent=1) + ";\n",
                   encoding="utf-8")
    print(f"{len(images)} Bilder -> {OUT.relative_to(ROOT)}")
    if skipped:
        print(f"\n{len(skipped)} Eintrag/Einträge übersprungen:")
        for line in skipped:
            print("  -", line)


if __name__ == "__main__":
    main()
