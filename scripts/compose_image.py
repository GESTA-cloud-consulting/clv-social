#!/usr/bin/env python3
"""Compone l'immagine di un post Chianti Luxury Villas: quadrato + logo bianco + claim opzionale.

Layout del logo (ricavato dal post di riferimento 2160x2160):
  centrato orizzontalmente, larghezza 16% del lato, margine inferiore 5.5% del lato.
  Logo bianco pieno, nessun effetto.

Claim (opzionale): Cinzel Bold (o Crimson Pro), bianco o colore brand, centrato,
sempre dentro la "safe zone" della griglia 3:4 di Instagram: il profilo mostra solo
il 75% centrale della larghezza di un post quadrato, quindi il testo sta nel 68% centrale.

Uso:
  python compose_image.py input.jpg output.jpg
      [--claim "Comfortable Interior Design"] [--claim-color white|verde|siena|siena-bruciata|giallo|#RRGGBB]
      [--claim-font cinzel|crimson] [--claim-position top|center] [--max-lines 3]
      [--focus 0.5] [--size 2160] [--safe-preview preview.jpg]
"""
import argparse, json
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
LOGO = ROOT / "assets" / "logo_bianco.png"
FONTS = {
    "cinzel": (ROOT / "assets" / "fonts" / "Cinzel[wght].ttf", b"Bold"),
    "crimson": (ROOT / "assets" / "fonts" / "CrimsonPro[wght].ttf", b"SemiBold"),
}
COLORS = {
    "white": "#FFFFFF", "bianco": "#FFFFFF",
    "verde": "#5C932D", "siena": "#B64A14", "siena-bruciata": "#6B3D3D", "giallo": "#FCD870",
}
LOGO_W, LOGO_BOTTOM = 0.16, 0.055
SAFE_W = 0.68            # larghezza utile del claim (dentro il 75% visibile in griglia 3:4)
CLAIM_TOP = 0.06         # margine superiore del claim (posizione "top")
CLAIM_MAX_H = 0.36       # altezza massima del blocco claim (posizione "top")


def square_crop(img, focus=0.5):
    w, h = img.size
    s = min(w, h)
    if w > h:
        l = int((w - s) * focus); return img.crop((l, 0, l + s, s))
    t = int((h - s) * focus); return img.crop((0, t, s, t + s))


def load_font(name, px):
    path, var = FONTS[name]
    f = ImageFont.truetype(str(path), px)
    try:
        f.set_variation_by_name(var)
    except Exception:
        pass
    return f


def wrap_options(words, max_lines):
    """Tutte le suddivisioni delle parole in 1..max_lines righe contigue."""
    n = len(words)
    def rec(start, lines_left):
        if start == n:
            yield []
            return
        if lines_left == 0:
            return
        for end in range(start + 1, n + 1):
            for rest in rec(end, lines_left - 1):
                yield [" ".join(words[start:end])] + rest
    yield from rec(0, max_lines)


def layout_claim(text, size, font_name, max_lines, max_h):
    """Sceglie a capo e corpo che massimizzano la dimensione restando nella safe zone."""
    words = text.split()
    max_w = size * SAFE_W
    best = None
    for lines in wrap_options(words, max_lines):
        lo, hi = 20, int(size * 0.14)
        while lo < hi:  # ricerca binaria del corpo massimo
            mid = (lo + hi + 1) // 2
            f = load_font(font_name, mid)
            widths = [f.getbbox(l)[2] - f.getbbox(l)[0] for l in lines]
            lh = int(mid * 1.08)
            if max(widths) <= max_w and lh * len(lines) <= max_h:
                lo = mid
            else:
                hi = mid - 1
        # preferisci corpo grande, poi meno righe, poi righe bilanciate
        score = (lo, -len(lines))
        if best is None or score > best[0]:
            best = (score, lines, lo)
    return best[1], best[2]


def draw_claim(canvas, text, color, font_name, position, max_lines):
    size = canvas.width
    max_h = size * (CLAIM_MAX_H if position == "top" else 0.5)
    lines, px = layout_claim(text, size, font_name, max_lines, max_h)
    f = load_font(font_name, px)
    lh = int(px * 1.08)
    block_h = lh * len(lines)
    y = size * CLAIM_TOP if position == "top" else (size - block_h) / 2 - size * 0.05
    d = ImageDraw.Draw(canvas)
    boxes = []
    for i, line in enumerate(lines):
        bb = f.getbbox(line)
        w = bb[2] - bb[0]
        x = (size - w) / 2 - bb[0]
        ly = y + i * lh
        d.text((x, ly), line, font=f, fill=color)
        boxes.append([round(x + bb[0]), round(ly + bb[1]), round(x + bb[2]), round(ly + bb[3])])
    return {"lines": lines, "font_px": px, "boxes": boxes}


def compose(src, dst, claim=None, claim_color="white", claim_font="cinzel",
            claim_position="top", max_lines=3, focus=0.5, size=2160, safe_preview=None):
    img = ImageOps.exif_transpose(Image.open(src))
    icc = img.info.get("icc_profile")
    if icc:  # converte in sRGB: i social mostrano solo sRGB, evita colori spenti
        try:
            from PIL import ImageCms
            import io
            img = ImageCms.profileToProfile(img.convert("RGB"), ImageCms.ImageCmsProfile(io.BytesIO(icc)),
                                            ImageCms.createProfile("sRGB"), outputMode="RGB")
        except Exception:
            pass
    img = img.convert("RGB")
    sq = square_crop(img, focus)
    warnings = []
    if sq.width < size:  # mai ingrandire: si perderebbe nitidezza
        size = sq.width
        warnings.append(f"Foto più piccola di 2160px: mantenuto il lato originale {size}px (nessun ingrandimento).")
    if size < 1080:
        warnings.append("Attenzione: lato < 1080px, qualità insufficiente per Instagram.")
    canvas = (sq.resize((size, size), Image.LANCZOS) if sq.width != size else sq).convert("RGBA")
    info = {"output": str(dst), "size": size, "warnings": warnings}

    if claim:
        color = COLORS.get(claim_color.lower(), claim_color)
        info["claim"] = draw_claim(canvas, claim, color, claim_font, claim_position, max_lines)

    mark = Image.open(LOGO).convert("RGBA")
    lw = round(size * LOGO_W); lh = round(mark.height * lw / mark.width)
    mark = mark.resize((lw, lh), Image.LANCZOS)
    x, y = (size - lw) // 2, size - round(size * LOGO_BOTTOM) - lh
    canvas.alpha_composite(mark, (x, y))
    info["logo_box"] = [x, y, x + lw, y + lh]

    out = canvas.convert("RGB")
    Path(dst).parent.mkdir(parents=True, exist_ok=True)
    # JPEG alta qualità: q92, nessun sottocampionamento colore (4:4:4), progressivo.
    # I metadati EXIF (incluso il GPS della proprietà) non vengono copiati.
    out.save(dst, "JPEG", quality=92, subsampling=0, optimize=True, progressive=True)

    if safe_preview:  # come appare nella griglia 3:4 del profilo Instagram
        vis = int(size * 0.75); l = (size - vis) // 2
        out.crop((l, 0, l + vis, size)).resize((540, 720), Image.LANCZOS).save(safe_preview, quality=88)
        info["safe_preview"] = str(safe_preview)
    return info


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("src"); p.add_argument("dst")
    p.add_argument("--claim"); p.add_argument("--claim-color", default="white")
    p.add_argument("--claim-font", default="cinzel", choices=list(FONTS))
    p.add_argument("--claim-position", default="top", choices=["top", "center"])
    p.add_argument("--max-lines", type=int, default=3)
    p.add_argument("--focus", type=float, default=0.5)
    p.add_argument("--size", type=int, default=2160)
    p.add_argument("--safe-preview")
    a = p.parse_args()
    print(json.dumps(compose(a.src, a.dst, a.claim, a.claim_color, a.claim_font, a.claim_position,
                             a.max_lines, a.focus, a.size, a.safe_preview), ensure_ascii=False))
