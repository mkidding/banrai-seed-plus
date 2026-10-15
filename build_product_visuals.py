import os
from PIL import Image, ImageEnhance, ImageOps, ImageDraw, ImageFilter, ImageFont

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PHOTO_DIR = os.path.join(BASE_DIR, "product_photos")
OUT_DIR = os.path.join(PHOTO_DIR, "processed")
os.makedirs(OUT_DIR, exist_ok=True)

# Pantone Palette Colors (RGB)
C_CANVAS = (244, 242, 237)      # #F4F2ED Cloud Dancer
C_WHITE = (251, 250, 247)       # #FBFAF7 Marshmallow
C_STONE = (236, 233, 225)       # #ECE9E1 Warm Sand
C_SAGE = (225, 232, 224)        # #E1E8E0 Soft Celadon
C_SLATE = (224, 231, 236)       # #E0E7EC Pale Mist
C_BORDER = (216, 212, 202)      # #D8D4CA Pumice Stone
C_BORDER_STR = (168, 164, 154)  # #A8A49A Warm Taupe
C_INK = (35, 38, 42)            # #23262A After Dark
C_SECOND = (96, 101, 108)       # #60656C Neutral Gray
C_MUTED = (142, 146, 152)       # #8E9298 Harbor Mist
C_SAGE_ACC = (88, 114, 92)      # #58725C Laurel Oak
C_SLATE_ACC = (78, 105, 122)    # #4E697A Porcelain Blue
C_LIME = (202, 251, 91)         # #CAFB5B Banrai Lime
C_LIME_BRD = (156, 204, 48)     # #9CCC30


def get_font(size, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def color_grade_hardware(img, brightness=1.06, contrast=1.08, saturation=0.95, cool_shift=6):
    """Normalizes indoor warm/yellow cast, lifts shadows, and balances saturation for Pantone palette."""
    img = img.convert("RGB")
    if cool_shift != 0:
        r, g, b = img.split()
        r = r.point(lambda i: max(0, min(255, i - cool_shift)))
        b = b.point(lambda i: max(0, min(255, i + cool_shift)))
        img = Image.merge("RGB", (r, g, b))
    if brightness != 1.0:
        img = ImageEnhance.Brightness(img).enhance(brightness)
    if contrast != 1.0:
        img = ImageEnhance.Contrast(img).enhance(contrast)
    if saturation != 1.0:
        img = ImageEnhance.Color(img).enhance(saturation)
    return img


def crop_fill(img, target_w, target_h, centering=(0.5, 0.5)):
    return ImageOps.fit(img, (target_w, target_h), method=Image.Resampling.LANCZOS, centering=centering)


def make_rounded_card(img, radius=24, border_color=C_BORDER, border_width=2):
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, w - 1, h - 1), radius=radius, fill=255)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    out.paste(img.convert("RGBA"), (0, 0), mask)
    if border_width > 0 and border_color:
        b_draw = ImageDraw.Draw(out)
        b_draw.rounded_rectangle(
            (border_width // 2, border_width // 2, w - 1 - border_width // 2, h - 1 - border_width // 2),
            radius=radius,
            outline=border_color + (255,),
            width=border_width,
        )
    return out


def paste_with_shadow(canvas, card_rgba, x, y, radius=24, shadow_offset=(0, 8), blur=14, shadow_alpha=28):
    w, h = card_rgba.size
    pad = blur * 2
    sh = Image.new("RGBA", (w + pad * 2, h + pad * 2), (0, 0, 0, 0))
    sh_draw = ImageDraw.Draw(sh)
    sh_draw.rounded_rectangle(
        (pad, pad, pad + w - 1, pad + h - 1),
        radius=radius,
        fill=(35, 38, 42, shadow_alpha),
    )
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    canvas.alpha_composite(sh, (x - pad + shadow_offset[0], y - pad + shadow_offset[1]))
    canvas.alpha_composite(card_rgba, (x, y))


def draw_pill_badge(canvas, x, y, text, bg_color=C_WHITE, border_color=C_BORDER, text_color=C_INK, font_size=20):
    draw = ImageDraw.Draw(canvas)
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pw, ph = tw + 28, th + 16
    pill = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    pdraw = ImageDraw.Draw(pill)
    pdraw.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=ph // 2, fill=bg_color + (242,), outline=border_color + (255,), width=2)
    pdraw.text((14, 7 - bbox[1]), text, font=font, fill=text_color + (255,))
    canvas.alpha_composite(pill, (x, y))


# ==============================================================================
# 1. MAGICAL LIVING PHOTO FRAME (FUREMU)
# ==============================================================================
def build_photoframe():
    pf1 = Image.open(os.path.join(PHOTO_DIR, "photoframe_1.jpg"))
    pf2 = Image.open(os.path.join(PHOTO_DIR, "photoframe_2.jpg"))
    pf3 = Image.open(os.path.join(PHOTO_DIR, "photoframe_3.jpg"))

    pf1_g = color_grade_hardware(pf1, brightness=1.08, contrast=1.07, saturation=0.94, cool_shift=8)
    pf2_g = color_grade_hardware(pf2, brightness=1.06, contrast=1.06, saturation=0.92, cool_shift=8)
    pf3_g = color_grade_hardware(pf3, brightness=1.08, contrast=1.08, saturation=0.92, cool_shift=6)

    w1, h1 = pf1_g.size
    pf1_crop = pf1_g.crop((int(w1 * 0.08), int(h1 * 0.11), int(w1 * 0.92), int(h1 * 0.89)))

    # Slide 5 Thumbnail (1100 x 800): 2-angle portrait framing so full tall bezel is visible
    s5_canvas = Image.new("RGBA", (1100, 800), C_STONE + (255,))
    left_img = crop_fill(pf1_crop, 630, 744, centering=(0.5, 0.48))
    right_img = crop_fill(pf2_g.crop((int(w1 * 0.18), int(h1 * 0.02), int(w1 * 0.88), int(h1 * 0.92))), 388, 744, centering=(0.55, 0.5))
    paste_with_shadow(s5_canvas, make_rounded_card(left_img, radius=22), 28, 28, radius=22)
    paste_with_shadow(s5_canvas, make_rounded_card(right_img, radius=22), 682, 28, radius=22)
    s5_canvas.convert("RGB").save(os.path.join(OUT_DIR, "s5_01_photoframe.png"), quality=95)

    # Appendix A1 Collage (1564 x 1000)
    a1_canvas = Image.new("RGBA", (1564, 1000), C_STONE + (255,))
    hero_card = make_rounded_card(crop_fill(pf1_crop, 880, 928, centering=(0.5, 0.5)), radius=28)
    side_top = make_rounded_card(
        crop_fill(pf2_g.crop((int(w1 * 0.15), int(h1 * 0.02), int(w1 * 0.88), int(h1 * 0.92))), 588, 448, centering=(0.55, 0.45)),
        radius=24,
    )
    side_bot = make_rounded_card(
        crop_fill(pf3_g.crop((int(w1 * 0.14), int(h1 * 0.05), int(w1 * 0.92), int(h1 * 0.90))), 588, 448, centering=(0.5, 0.52)),
        radius=24,
    )
    paste_with_shadow(a1_canvas, hero_card, 36, 36, radius=28)
    paste_with_shadow(a1_canvas, side_top, 940, 36, radius=24)
    paste_with_shadow(a1_canvas, side_bot, 940, 516, radius=24)

    draw_pill_badge(a1_canvas, 60, 60, "LIVE PORTRAIT + WEATHER SYNC", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_INK, font_size=19)
    draw_pill_badge(a1_canvas, 962, 58, "ANODIZED GOLD BEZEL", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_SECOND, font_size=17)
    draw_pill_badge(a1_canvas, 962, 538, "KICKSTAND · FUREMU EDITION", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_SECOND, font_size=17)
    a1_canvas.convert("RGB").save(os.path.join(OUT_DIR, "a1_photoframe_collage.png"), quality=95)


# ==============================================================================
# 2. POCKET INTERACTIVE BIBLE (VERSICLE — E-INK + 4G HARDWARE)
# ==============================================================================
def build_bible_visual():
    pb1 = Image.open(os.path.join(PHOTO_DIR, "pocketbible_1.jpg"))
    pb2 = Image.open(os.path.join(PHOTO_DIR, "pocketbible_2.jpg"))

    # Cool the warm concrete cast, lift E-Ink paper whites and gold anodized frame contrast
    pb1_g = color_grade_hardware(pb1, brightness=1.12, contrast=1.10, saturation=0.95, cool_shift=8)
    pb2_g = color_grade_hardware(pb2, brightness=1.12, contrast=1.10, saturation=0.95, cool_shift=8)

    w1, h1 = pb1_g.size
    pb1_crop = pb1_g.crop((int(w1 * 0.12), int(h1 * 0.08), int(w1 * 0.90), int(h1 * 0.90)))

    w2, h2 = pb2_g.size
    pb2_crop = pb2_g.crop((int(w2 * 0.10), int(h2 * 0.08), int(w2 * 0.92), int(h2 * 0.90)))

    # Slide 5 Thumbnail (1100 x 800): Clean single hero hardware shot of Pocket Interactive Bible
    s5_canvas = Image.new("RGBA", (1100, 800), C_STONE + (255,))
    s5_hero = crop_fill(pb1_crop, 1044, 744, centering=(0.5, 0.48))
    paste_with_shadow(s5_canvas, make_rounded_card(s5_hero, radius=22), 28, 28, radius=22)
    s5_canvas.convert("RGB").save(os.path.join(OUT_DIR, "s5_02_bible.png"), quality=95)

    # Appendix A1 Collage (1564 x 1000): Symmetrical 3-card bento layout matching Photo Frame on Slide A1
    a1_canvas = Image.new("RGBA", (1564, 1000), C_STONE + (255,))
    # Left Hero: Full hardware view of pb1_g (using full height so all 4 corners of the device fit inside 880x928)
    left_card = make_rounded_card(crop_fill(pb1_g, 880, 928, centering=(0.52, 0.5)), radius=28)
    # Top-Right: Full uncropped 4:3 view of pb2_crop showing VERSICLE backplate & gold buttons
    top_right = make_rounded_card(crop_fill(pb2_crop, 588, 448, centering=(0.5, 0.5)), radius=24)
    # Bottom-Right: Close-up detail of E-Ink Scripture + "Hold to talk" + tactile side buttons
    pb1_macro = pb1_g.crop((int(w1 * 0.20), int(h1 * 0.18), int(w1 * 0.82), int(h1 * 0.78)))
    bot_right = make_rounded_card(crop_fill(pb1_macro, 588, 448, centering=(0.5, 0.5)), radius=24)

    paste_with_shadow(a1_canvas, left_card, 36, 36, radius=28)
    paste_with_shadow(a1_canvas, top_right, 940, 36, radius=24)
    paste_with_shadow(a1_canvas, bot_right, 940, 516, radius=24)

    draw_pill_badge(a1_canvas, 60, 60, "STANDALONE E-INK + 4G COMPANION", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_INK, font_size=19)
    draw_pill_badge(a1_canvas, 962, 58, "VERSICLE · ANODIZED GOLD & GLASS", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_SECOND, font_size=17)
    draw_pill_badge(a1_canvas, 962, 538, "“HOLD TO TALK” DAILY SCRIPTURE", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_SECOND, font_size=17)

    a1_canvas.convert("RGB").save(os.path.join(OUT_DIR, "a1_bible_preview.png"), quality=95)


# ==============================================================================
# 3. DREAM PRINTER (HARDWARE + GENERATED DREAM ARTWORK UI)
# ==============================================================================
def build_dreamprinter():
    dp1 = Image.open(os.path.join(PHOTO_DIR, "dreamprinter_1.jpg"))
    dp2 = Image.open(os.path.join(PHOTO_DIR, "dreamprinter_2.png")).convert("RGB")

    dp1_g = color_grade_hardware(dp1, brightness=1.10, contrast=1.08, saturation=0.96, cool_shift=10)
    w1, h1 = dp1_g.size
    dp1_crop = dp1_g.crop((int(w1 * 0.19), int(h1 * 0.02), int(w1 * 0.85), int(h1 * 0.90)))

    # Slide 5 Thumbnail (1100 x 800)
    s5_canvas = Image.new("RGBA", (1100, 800), C_STONE + (255,))
    s5_hero = crop_fill(dp1_crop, 1044, 744, centering=(0.5, 0.48))
    paste_with_shadow(s5_canvas, make_rounded_card(s5_hero, radius=22), 28, 28, radius=22)
    s5_canvas.convert("RGB").save(os.path.join(OUT_DIR, "s5_03_dreamprinter.png"), quality=95)

    # Appendix A2 Collage (1564 x 1000)
    a2_canvas = Image.new("RGBA", (1564, 1000), C_STONE + (255,))
    left_hw = make_rounded_card(crop_fill(dp1_crop, 820, 928, centering=(0.5, 0.48)), radius=28)
    paste_with_shadow(a2_canvas, left_hw, 36, 36, radius=28)

    line_art = dp2.crop((55, 162, 385, 405))
    hires_art = dp2.crop((465, 135, 860, 431))

    tr_card = Image.new("RGBA", (636, 448), (255, 255, 255, 255))
    la_fit = ImageOps.contain(line_art, (560, 340), method=Image.Resampling.LANCZOS)
    tr_card.paste(la_fit.convert("RGBA"), ((636 - la_fit.width) // 2, 82))
    paste_with_shadow(a2_canvas, make_rounded_card(tr_card, radius=24), 892, 36, radius=24)

    br_card = make_rounded_card(crop_fill(hires_art, 636, 448, centering=(0.5, 0.5)), radius=24)
    paste_with_shadow(a2_canvas, br_card, 892, 516, radius=24)

    draw_pill_badge(a2_canvas, 60, 60, "BEDSIDE HARDWARE · E-INK + THERMAL", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_INK, font_size=18)
    draw_pill_badge(a2_canvas, 914, 52, "1 · INSTANT THERMAL SKETCH", bg_color=C_STONE, border_color=C_BORDER, text_color=C_INK, font_size=16)
    draw_pill_badge(a2_canvas, 914, 538, "2 · HIGH-RES CLOUD DREAM DIARY", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_INK, font_size=16)

    a2_canvas.convert("RGB").save(os.path.join(OUT_DIR, "a2_dreamprinter_collage.png"), quality=95)


# ==============================================================================
# 4. VOICE GAMING WALKIE-TALKIE (MAYDAY — 3-ACT RESCUE COLLAGE)
# ==============================================================================
def build_mayday():
    m1 = Image.open(os.path.join(PHOTO_DIR, "mayday_1.png"))
    m2 = Image.open(os.path.join(PHOTO_DIR, "mayday_2.png"))
    m3 = Image.open(os.path.join(PHOTO_DIR, "mayday_3.png"))

    m1_g = color_grade_hardware(m1, brightness=1.08, contrast=1.12, saturation=1.02, cool_shift=10)
    m2_g = color_grade_hardware(m2, brightness=1.06, contrast=1.10, saturation=1.02, cool_shift=10)
    m3_g = color_grade_hardware(m3, brightness=1.08, contrast=1.12, saturation=1.02, cool_shift=10)

    # Full hardware unit crop of m2 (558x776)
    m2_unit = m2_g.crop((24, 110, 552, 650))
    # Include generous top black bezel on m1_scr and m3_scr so pill badge never overlaps top screen text
    m1_scr = m1_g.crop((102, 222, 466, 548))
    m3_scr = m3_g.crop((62, 105, 456, 462))

    # Slide 5 Thumbnail (1100 x 800): Clean single hero hardware view (m2_unit) so 100% of screen & casing is legible
    s5_canvas = Image.new("RGBA", (1100, 800), C_STONE + (255,))
    s5_hero = crop_fill(m2_unit, 1044, 744, centering=(0.5, 0.48))
    paste_with_shadow(s5_canvas, make_rounded_card(s5_hero, radius=22), 28, 28, radius=22)
    s5_canvas.convert("RGB").save(os.path.join(OUT_DIR, "s5_04_mayday.png"), quality=95)

    # Appendix A2 Collage (1564 x 1000)
    a2_canvas = Image.new("RGBA", (1564, 1000), C_STONE + (255,))
    hero_card = make_rounded_card(crop_fill(m2_unit, 850, 928, centering=(0.5, 0.5)), radius=28)
    top_right = make_rounded_card(crop_fill(m1_scr, 606, 448, centering=(0.5, 0.5)), radius=24)
    bot_right = make_rounded_card(crop_fill(m3_scr, 606, 448, centering=(0.5, 0.5)), radius=24)

    paste_with_shadow(a2_canvas, hero_card, 36, 36, radius=28)
    paste_with_shadow(a2_canvas, top_right, 922, 36, radius=24)
    paste_with_shadow(a2_canvas, bot_right, 922, 516, radius=24)

    draw_pill_badge(a2_canvas, 60, 60, "LIVE VOICE COMMS · BIO & AUDIO WAVEFORM", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_INK, font_size=18)
    draw_pill_badge(a2_canvas, 944, 52, "ACT 1 · TRAVERSE ALIEN STORM", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_INK, font_size=16)
    draw_pill_badge(a2_canvas, 944, 532, "ACT 3 · MISSION RESCUE COMPLETE", bg_color=C_LIME, border_color=C_LIME_BRD, text_color=C_INK, font_size=16)

    a2_canvas.convert("RGB").save(os.path.join(OUT_DIR, "a2_mayday_collage.png"), quality=95)


# ==============================================================================
# 5. KIDS' E-INK DOODLE PAD (HARDWARE RENDER + SKETCH -> 4-PANEL COMIC)
# ==============================================================================
def build_doodleboard():
    db1 = Image.open(os.path.join(PHOTO_DIR, "doodleboard_1.png")).convert("RGB")
    db2 = Image.open(os.path.join(PHOTO_DIR, "doodleboard_2.png")).convert("RGB")
    db3 = Image.open(os.path.join(PHOTO_DIR, "doodleboard_3.png")).convert("RGB")

    # Subtle color grade on db3 so it harmonizes with the other studio hardware photos
    db3_g = color_grade_hardware(db3, brightness=1.03, contrast=1.04, saturation=0.96, cool_shift=3)
    w3, h3 = db3_g.size
    db3_crop = db3_g.crop((int(w3 * 0.12), int(h3 * 0.10), int(w3 * 0.90), int(h3 * 0.90)))

    db1_sketch = db1.crop((28, 95, 1258, 845))
    db2_comic = db2.crop((194, 348, 594, 644))

    # Slide 5 Thumbnail (1100 x 800): Clean single hero hardware view (db3) so all 5 Slide 5 cards feature physical hardware!
    s5_canvas = Image.new("RGBA", (1100, 800), C_STONE + (255,))
    s5_hero = crop_fill(db3_crop, 1044, 744, centering=(0.5, 0.5))
    paste_with_shadow(s5_canvas, make_rounded_card(s5_hero, radius=22), 28, 28, radius=22)
    s5_canvas.convert("RGB").save(os.path.join(OUT_DIR, "s5_05_doodleboard.png"), quality=95)

    # Appendix A3 Hero Spotlight Collage (1673 x 1200)
    # Top-Left: Physical E-Ink Hardware Render (db3), Top-Right: Child's Sketch Input (db1), Bottom: 4-Panel AI Comic Adventure (db2)
    a3_canvas = Image.new("RGBA", (1673, 1200), C_STONE + (255,))

    # Top-Left Card: Physical E-Ink Doodle Pad Hardware (920 x 520)
    tl_hw = make_rounded_card(crop_fill(db3_crop, 920, 520, centering=(0.5, 0.52)), radius=26)
    paste_with_shadow(a3_canvas, tl_hw, 36, 36, radius=26)
    draw_pill_badge(a3_canvas, 60, 56, "01 · E-INK HARDWARE · STYLUS + SMILEY AI BUTTON", bg_color=C_WHITE, border_color=C_BORDER, text_color=C_INK, font_size=17)

    # Top-Right Card: Child's Raw Sketch Input (653 x 520)
    tr_card = Image.new("RGBA", (653, 520), (255, 255, 255, 255))
    sk_fit = ImageOps.contain(db1_sketch, (605, 405), method=Image.Resampling.LANCZOS)
    tr_card.paste(sk_fit.convert("RGBA"), ((653 - sk_fit.width) // 2, 92))
    paste_with_shadow(a3_canvas, make_rounded_card(tr_card, radius=26), 984, 36, radius=26)
    draw_pill_badge(a3_canvas, 1008, 56, "02 · CHILD’S RAW SKETCH", bg_color=C_STONE, border_color=C_BORDER, text_color=C_INK, font_size=17)

    # Bottom Hero Card: 4-Panel Comic Strip Sequence at UNCROPPED native 4:3 landscape aspect ratio!
    p1 = db2_comic.crop((2, 2, 196, 145))
    p2 = db2_comic.crop((204, 2, 398, 145))
    p3 = db2_comic.crop((2, 151, 196, 294))
    p4 = db2_comic.crop((204, 151, 398, 294))

    bot_card = Image.new("RGBA", (1601, 574), C_WHITE + (255,))
    bdraw = ImageDraw.Draw(bot_card)
    f_cap = get_font(18, bold=True)
    f_sub = get_font(16, bold=False)
    captions = [
        ("01 · Set Sail", "Sam hops onto the shiny red boat"),
        ("02 · Sea Birds", "Three friendly birds swoop down"),
        ("03 · Yellow Flag", "Waving high in the warm sun"),
        ("04 · Magic Ocean", "Sailing far into the sparkling sea"),
    ]
    for idx, (pan, (cap_title, cap_sub)) in enumerate(zip([p1, p2, p3, p4], captions)):
        px = 28 + idx * 392
        py = 104
        # Native aspect ratio 194:143 -> 368 x 272 (zero cropping!)
        pan_resized = pan.resize((368, 272), Image.Resampling.LANCZOS)
        pan_card = make_rounded_card(pan_resized, radius=16, border_color=C_INK, border_width=3)
        bot_card.alpha_composite(pan_card, (px, py))
        bdraw.text((px + 6, py + 292), cap_title, font=f_cap, fill=C_INK + (255,))
        bdraw.text((px + 6, py + 320), cap_sub, font=f_sub, fill=C_SECOND + (255,))

    paste_with_shadow(a3_canvas, make_rounded_card(bot_card, radius=28), 36, 590, radius=28)
    draw_pill_badge(
        a3_canvas, 62, 612,
        "03 · GENERATED 4-PANEL COMIC ADVENTURE (CO-CREATED WITH CHILD)",
        bg_color=C_LIME, border_color=C_LIME_BRD, text_color=C_INK, font_size=18
    )

    a3_canvas.convert("RGB").save(os.path.join(OUT_DIR, "a3_doodleboard_collage.png"), quality=95)


if __name__ == "__main__":
    build_photoframe()
    build_bible_visual()
    build_dreamprinter()
    build_mayday()
    build_doodleboard()
    print("All product visuals refined successfully in:", OUT_DIR)
