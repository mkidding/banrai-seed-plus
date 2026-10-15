import os
import math
from PIL import Image, ImageDraw, ImageFilter
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUT_DIR = "/Users/mklaw/Developer/klaw/Seed Plus Round"
BG_DIR = "/tmp/banrai_slide_bgs"
os.makedirs(BG_DIR, exist_ok=True)


def make_ambient_bg(filename, mode="dark", variant=0):
    """Generates a peacefully delightful, calm ambient 1920x1080 background inspired by banrai.ai."""
    w, h = 1920, 1080
    if mode == "dark":
        # Serene nocturnal twilight base (#0B101B)
        base = Image.new("RGBA", (w, h), (11, 16, 27, 255))
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)

        # Soft aurora orbs (lime #CAFB5B, mint #A8E6CF, lavender #C7B9FF)
        orbs = [
            # (cx, cy, radius, (r, g, b, max_alpha))
            (int(w * (0.82 if variant % 2 == 0 else 0.18)), int(h * 0.18), 520, (202, 251, 91, 22)),
            (int(w * (0.15 if variant % 2 == 0 else 0.85)), int(h * 0.82), 580, (168, 230, 207, 18)),
            (int(w * 0.52), int(h * (0.12 if variant % 3 == 0 else 0.88)), 620, (199, 185, 255, 16)),
        ]
        for cx, cy, rad, col in orbs:
            draw.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=col)

        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=160))
        img = Image.alpha_composite(base, overlay)

        # Add a few tiny, peaceful firefly/starlight dots like banrai.ai
        dots = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        d_draw = ImageDraw.Draw(dots)
        positions = [
            (180, 140, (202, 251, 91, 70), 3),
            (1720, 190, (168, 230, 207, 65), 3),
            (1640, 920, (199, 185, 255, 60), 3),
            (290, 910, (255, 255, 255, 45), 2),
            (980, 95, (202, 251, 91, 50), 2),
        ]
        for x, y, c, r in positions:
            d_draw.ellipse((x - r*3, y - r*3, x + r*3, y + r*3), fill=(c[0], c[1], c[2], 18))
            d_draw.ellipse((x - r, y - r, x + r, y + r), fill=c)
        img = Image.alpha_composite(img, dots)
    else:
        # Serene daylight/morning calm base (#F7F9F7)
        base = Image.new("RGBA", (w, h), (246, 248, 245, 255))
        overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        orbs = [
            (int(w * (0.82 if variant % 2 == 0 else 0.18)), int(h * 0.18), 520, (202, 251, 91, 55)),
            (int(w * (0.15 if variant % 2 == 0 else 0.85)), int(h * 0.82), 580, (168, 230, 207, 50)),
            (int(w * 0.52), int(h * (0.12 if variant % 3 == 0 else 0.88)), 620, (199, 185, 255, 42)),
        ]
        for cx, cy, rad, col in orbs:
            draw.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill=col)
        overlay = overlay.filter(ImageFilter.GaussianBlur(radius=150))
        img = Image.alpha_composite(base, overlay)

    path = os.path.join(BG_DIR, filename)
    img.convert("RGB").save(path, "PNG", optimize=True)
    return path


def get_palette(mode="dark"):
    if mode == "dark":
        return {
            "mode": "dark",
            "bg": RGBColor(11, 16, 27),
            "card_bg": RGBColor(19, 26, 41),
            "card_bg_alt": RGBColor(23, 32, 49),
            "card_border": RGBColor(42, 54, 79),
            "placeholder_bg": RGBColor(15, 21, 34),
            "placeholder_border": RGBColor(65, 85, 115),
            "text_primary": RGBColor(242, 245, 248),
            "text_secondary": RGBColor(162, 176, 196),
            "text_muted": RGBColor(108, 124, 148),
            "accent_lime": RGBColor(202, 251, 91),       # #CAFB5B (Banrai Primary)
            "accent_mint": RGBColor(168, 230, 207),      # #A8E6CF (Banrai Secondary)
            "accent_lavender": RGBColor(199, 185, 255),  # #C7B9FF (Banrai Tertiary)
            "accent_amber": RGBColor(253, 224, 141),     # Soft warm sunlight
            "pill_bg": RGBColor(26, 38, 34),
            "pill_text": RGBColor(202, 251, 91),
            "dark_text_on_lime": RGBColor(11, 16, 27),
        }
    else:
        return {
            "mode": "light",
            "bg": RGBColor(246, 248, 245),
            "card_bg": RGBColor(255, 255, 255),
            "card_bg_alt": RGBColor(240, 244, 239),
            "card_border": RGBColor(218, 226, 220),
            "placeholder_bg": RGBColor(237, 242, 238),
            "placeholder_border": RGBColor(176, 192, 182),
            "text_primary": RGBColor(17, 24, 34),
            "text_secondary": RGBColor(74, 88, 104),
            "text_muted": RGBColor(124, 138, 152),
            "accent_lime": RGBColor(92, 142, 18),        # Deeper botanical green for light mode text
            "accent_lime_fill": RGBColor(202, 251, 91),  # Original Banrai lime for badges/dots
            "accent_mint": RGBColor(38, 132, 102),
            "accent_lavender": RGBColor(106, 82, 186),
            "accent_amber": RGBColor(180, 118, 24),
            "pill_bg": RGBColor(230, 244, 200),
            "pill_text": RGBColor(54, 92, 10),
            "dark_text_on_lime": RGBColor(17, 24, 34),
        }


FONT_MAIN = "Poppins"


def add_bg(slide, prs, bg_path):
    slide.shapes.add_picture(bg_path, 0, 0, width=prs.slide_width, height=prs.slide_height)


def add_textbox(slide, left, top, width, height, text, font_size=16, bold=False,
                color=RGBColor(255, 255, 255), align=PP_ALIGN.LEFT,
                line_spacing=1.25, font_name=FONT_MAIN, anchor=MSO_ANCHOR.TOP):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = align
    p.line_spacing = line_spacing
    p.font.name = font_name
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    return tb


def add_card(slide, left, top, width, height, fill_color, border_color=None, border_pt=1.0, radius=0.04):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    shape.adjustments[0] = radius
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_pt)
    else:
        shape.line.fill.background()
    return shape


def add_banrai_logo(slide, left, top, size="small", pal=None):
    """Draws the official Banrai wordmark + glowing lime circle from banrai.ai."""
    dot_color = pal.get("accent_lime_fill", pal["accent_lime"])
    if size == "hero":
        # Centered hero logo on Slide 1
        add_textbox(
            slide, left, top, 3.6, 1.1, "Banrai",
            font_size=64, bold=True, color=pal["text_primary"],
            align=PP_ALIGN.RIGHT
        )
        # Outer subtle halo circle
        halo = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(left + 3.72), Inches(top + 0.42), Inches(0.36), Inches(0.36)
        )
        halo.fill.solid()
        halo.fill.fore_color.rgb = pal["pill_bg"]
        halo.line.fill.background()

        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(left + 3.80), Inches(top + 0.50), Inches(0.20), Inches(0.20)
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = dot_color
        dot.line.fill.background()
    else:
        # Top-right or footer mini logo
        add_textbox(
            slide, left, top, 1.15, 0.35, "Banrai",
            font_size=15, bold=True, color=pal["text_secondary"],
            align=PP_ALIGN.RIGHT
        )
        dot = slide.shapes.add_shape(
            MSO_SHAPE.OVAL,
            Inches(left + 1.20), Inches(top + 0.12), Inches(0.09), Inches(0.09)
        )
        dot.fill.solid()
        dot.fill.fore_color.rgb = dot_color
        dot.line.fill.background()


def add_slide_header(slide, eyebrow, title, subtitle, pal, slide_num=None):
    """Consistent, calm, editorial slide header with generous whitespace."""
    # Eyebrow pill/label
    add_textbox(
        slide, 0.85, 0.55, 6.0, 0.3, eyebrow.upper(),
        font_size=10, bold=True, color=pal["accent_lime"],
        line_spacing=1.1
    )
    # Top-right logo & slide number
    add_banrai_logo(slide, 11.15, 0.50, size="small", pal=pal)
    if slide_num:
        add_textbox(
            slide, 11.8, 6.92, 0.7, 0.3, f"{slide_num:02d} / 09",
            font_size=9.5, bold=False, color=pal["text_muted"],
            align=PP_ALIGN.RIGHT
        )

    # Main Title
    add_textbox(
        slide, 0.85, 0.88, 10.8, 0.65, title,
        font_size=28, bold=True, color=pal["text_primary"],
        line_spacing=1.15
    )
    if subtitle:
        add_textbox(
            slide, 0.85, 1.48, 10.2, 0.45, subtitle,
            font_size=13.5, bold=False, color=pal["text_secondary"],
            line_spacing=1.3
        )


def add_image_placeholder(slide, left, top, width, height, label, sublabel, pal, accent_color=None):
    """Creates a clean, spacious, unmistakable image drop zone for product imagery."""
    border_col = accent_color if accent_color else pal["placeholder_border"]
    box = add_card(
        slide, left, top, width, height,
        fill_color=pal["placeholder_bg"],
        border_color=border_col,
        border_pt=1.25,
        radius=0.04
    )
    # Inner subtle frame corners / icon circle
    cx = left + width / 2.0
    cy = top + height / 2.0 - 0.22
    icon_circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL,
        Inches(cx - 0.28), Inches(cy - 0.28), Inches(0.56), Inches(0.56)
    )
    icon_circle.fill.solid()
    icon_circle.fill.fore_color.rgb = pal["card_bg_alt"]
    icon_circle.line.color.rgb = border_col
    icon_circle.line.width = Pt(1.0)

    add_textbox(
        slide, cx - 0.28, cy - 0.26, 0.56, 0.52, "✦",
        font_size=16, bold=True, color=border_col,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )

    add_textbox(
        slide, left + 0.3, cy + 0.38, width - 0.6, 0.35, label,
        font_size=12, bold=True, color=pal["text_primary"],
        align=PP_ALIGN.CENTER
    )
    add_textbox(
        slide, left + 0.3, cy + 0.68, width - 0.6, 0.4, sublabel,
        font_size=10, bold=False, color=pal["text_muted"],
        align=PP_ALIGN.CENTER
    )
    return box


def add_pill_badge(slide, left, top, width, height, text, bg_color, text_color, border_color=None, font_size=9.5):
    pill = add_card(slide, left, top, width, height, fill_color=bg_color, border_color=border_color, border_pt=1.0, radius=0.5)
    add_textbox(
        slide, left + 0.08, top + 0.02, width - 0.16, height - 0.04, text,
        font_size=font_size, bold=True, color=text_color,
        align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE
    )
    return pill


def add_bullet_list(slide, left, top, width, height, items, pal, accent_color=None, font_size=12.5, spacing=10):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)

    dot_col = accent_color if accent_color else pal["accent_lime"]
    for idx, (lead, body) in enumerate(items):
        p = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
        p.space_after = Pt(spacing)
        p.line_spacing = 1.32

        r_dot = p.add_run()
        r_dot.text = "●  "
        r_dot.font.name = FONT_MAIN
        r_dot.font.size = Pt(font_size - 2)
        r_dot.font.color.rgb = dot_col

        if lead:
            r_lead = p.add_run()
            r_lead.text = lead + " "
            r_lead.font.name = FONT_MAIN
            r_lead.font.size = Pt(font_size)
            r_lead.font.bold = True
            r_lead.font.color.rgb = pal["text_primary"]

        r_body = p.add_run()
        r_body.text = body
        r_body.font.name = FONT_MAIN
        r_body.font.size = Pt(font_size)
        r_body.font.bold = False
        r_body.font.color.rgb = pal["text_secondary"]
    return tb


def build_deck(output_filename, mode="dark"):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    pal = get_palette(mode)

    bgs = [make_ambient_bg(f"bg_{mode}_{i}.png", mode=mode, variant=i) for i in range(9)]

    # =========================================================================
    # SLIDE 1: COVER / TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    add_bg(s1, prs, bgs[0])

    # Top pill badge
    add_pill_badge(
        s1, 4.76, 1.55, 3.8, 0.36,
        "✦  AI-NATIVE CONSUMER ECOSYSTEM",
        bg_color=pal["pill_bg"], text_color=pal["pill_text"],
        border_color=pal["accent_lime"], font_size=9.5
    )

    # Center Banrai Logo
    add_banrai_logo(s1, 4.45, 2.25, size="hero", pal=pal)

    # Main Headline & Counter-trend subheadline
    add_textbox(
        s1, 1.5, 3.55, 10.333, 0.75,
        "Building the World’s First “Fun AI”",
        font_size=34, bold=True, color=pal["text_primary"],
        align=PP_ALIGN.CENTER
    )
    add_textbox(
        s1, 2.1, 4.30, 9.133, 0.85,
        "Delightfully non-functional, AI-native consumer electronics for everyday joy.\nGuided by one quiet conviction: Make Humans Talk Again.",
        font_size=15, bold=False, color=pal["text_secondary"],
        align=PP_ALIGN.CENTER, line_spacing=1.45
    )

    # Bottom 3 subtle summary pills
    pills_s1 = [
        ("100% Subscription-Native", "SaaS economics on physical hardware"),
        ("< 9 Months · $150K–$200K", "Concept to first 1,000 US units"),
        ("6–10 Products / Year", "Multi-brand portfolio on one backend"),
    ]
    for i, (p_title, p_sub) in enumerate(pills_s1):
        x = 1.35 + i * 3.65
        add_card(s1, x, 5.65, 3.35, 1.05, fill_color=pal["card_bg"], border_color=pal["card_border"])
        add_textbox(s1, x + 0.22, 5.82, 2.9, 0.32, p_title, font_size=12, bold=True, color=pal["accent_lime"], align=PP_ALIGN.CENTER)
        add_textbox(s1, x + 0.22, 6.18, 2.9, 0.32, p_sub, font_size=10.5, bold=False, color=pal["text_secondary"], align=PP_ALIGN.CENTER)

    # =========================================================================
    # SLIDE 2: THE COUNTER-TREND THESIS (FUN AI VS FUNCTIONAL AI)
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    add_bg(s2, prs, bgs[1])
    add_slide_header(
        s2,
        eyebrow="01 · The Philosophy",
        title="Everyone Is Building Functional AI. We Build Fun AI.",
        subtitle="In a sense, we are building the most 'useless' AI in the world—because human life isn’t a productivity spreadsheet.",
        pal=pal, slide_num=2
    )

    # Left Card: The Industry Default (Functional AI)
    add_card(s2, 0.85, 2.20, 5.55, 3.65, fill_color=pal["card_bg"], border_color=pal["card_border"])
    add_pill_badge(s2, 1.20, 2.50, 2.35, 0.32, "THE INDUSTRY CROWD", bg_color=pal["card_bg_alt"], text_color=pal["text_muted"], font_size=9)
    add_textbox(s2, 1.20, 2.98, 4.8, 0.45, "Functional AI", font_size=22, bold=True, color=pal["text_secondary"])
    add_bullet_list(
        s2, 1.20, 3.55, 4.85, 2.0,
        [
            ("Task-Obsessed:", "Built to write emails, summarize meetings, and shave seconds off workflows."),
            ("Utility Mindset:", "Users only engage when they have a chore or work problem to solve."),
            ("Commoditized Race:", "Competing head-on with tech giants on raw benchmark utility."),
        ],
        pal=pal, accent_color=pal["text_muted"], font_size=12, spacing=12
    )

    # Right Card: The Banrai Counter-Trend (Fun AI)
    add_card(s2, 6.75, 2.20, 5.73, 3.65, fill_color=pal["card_bg_alt"], border_color=pal["accent_lime"], border_pt=1.5)
    add_pill_badge(s2, 7.10, 2.50, 2.20, 0.32, "✦  OUR CATEGORY", bg_color=pal["pill_bg"], text_color=pal["pill_text"], font_size=9)
    add_textbox(s2, 7.10, 2.98, 5.0, 0.45, "Fun AI (Delightfully “Useless”)", font_size=22, bold=True, color=pal["text_primary"])
    add_bullet_list(
        s2, 7.10, 3.55, 5.0, 2.0,
        [
            ("Joy & Curiosity First:", "Built for moments of wonder, play, storytelling, and emotional warmth."),
            ("Ambient Daily Presence:", "Lives across diverse brands & tactile form factors in everyday life."),
            ("Zero Utility Pressure:", "No tasks to optimize—just companions that spark smiles and dialogue."),
        ],
        pal=pal, accent_color=pal["accent_lime"], font_size=12, spacing=12
    )

    # Bottom Theme Banner: "Make Humans Talk Again"
    add_card(s2, 0.85, 6.05, 11.63, 0.82, fill_color=pal["card_bg"], border_color=pal["accent_mint"], border_pt=1.0)
    add_textbox(
        s2, 1.15, 6.18, 3.3, 0.32, "UNIFYING THEME ·",
        font_size=10, bold=True, color=pal["accent_mint"]
    )
    add_textbox(
        s2, 1.15, 6.40, 3.8, 0.35, "“Make Humans Talk Again”",
        font_size=14, bold=True, color=pal["text_primary"]
    )
    add_textbox(
        s2, 4.65, 6.20, 7.6, 0.55,
        "After a decade of passive smartphone scrolling, our unifying theme inspires active voice, curiosity, and conversation—while letting every product share a single conversational AI backend.",
        font_size=11.5, bold=False, color=pal["text_secondary"], line_spacing=1.28
    )

    # =========================================================================
    # SLIDE 3: BUSINESS MODEL — HARDWARE-ENABLED SAAS
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    add_bg(s3, prs, bgs[2])
    add_slide_header(
        s3,
        eyebrow="02 · Business Model",
        title="Hardware as the Vessel. SaaS as the Engine.",
        subtitle="Because our products are truly AI-native and consume live tokens, every device operates on a hard monthly subscription.",
        pal=pal, slide_num=3
    )

    # Top Comparison Strip: Traditional Hardware vs Banrai Model
    add_card(s3, 0.85, 2.15, 5.55, 1.95, fill_color=pal["card_bg"], border_color=pal["card_border"])
    add_textbox(s3, 1.15, 2.35, 5.0, 0.35, "Traditional Consumer Hardware", font_size=15, bold=True, color=pal["text_secondary"])
    add_bullet_list(
        s3, 1.15, 2.78, 5.0, 1.2,
        [
            ("One-Time Margin:", "Profit stops the day the box is sold."),
            ("Upgrade Treadmill:", "Forced to push Gen-2 hardware or chase new unit buyers to survive."),
        ],
        pal=pal, accent_color=pal["text_muted"], font_size=11.5, spacing=8
    )

    add_card(s3, 6.75, 2.15, 5.73, 1.95, fill_color=pal["card_bg_alt"], border_color=pal["accent_lime"], border_pt=1.5)
    add_textbox(s3, 7.05, 2.35, 5.1, 0.35, "Banrai Hard-Subscription Model", font_size=15, bold=True, color=pal["accent_lime"])
    add_bullet_list(
        s3, 7.05, 2.78, 5.1, 1.2,
        [
            ("No Free Tier:", "Real token consumption requires sustainable recurring revenue."),
            ("Pure SaaS Alignment:", "We win by delivering continuous daily delight that retains subscribers."),
        ],
        pal=pal, accent_color=pal["accent_lime"], font_size=11.5, spacing=8
    )

    # Bottom 3 Step Flow Cards
    steps_s3 = [
        ("01 · Tactile Entry", "Hardware + Bundled Months", "Every device ships with several complimentary months of subscription—eliminating friction at first touch.", pal["accent_lime"]),
        ("02 · Daily Habit", "Hard Monthly Subscription", "To keep the companion alive after the trial period, users subscribe monthly—aligning token costs with high-margin recurring revenue.", pal["accent_mint"]),
        ("03 · SaaS Compounding", "Continuous Value Delivery", "Instead of pushing hardware replacements, our backend continuously evolves stories, personalities, and experiences.", pal["accent_lavender"]),
    ]
    for i, (tag, head, desc, col) in enumerate(steps_s3):
        x = 0.85 + i * 3.94
        add_card(s3, x, 4.38, 3.75, 2.45, fill_color=pal["card_bg"], border_color=col, border_pt=1.1)
        add_textbox(s3, x + 0.28, 4.62, 3.2, 0.28, tag.upper(), font_size=9.5, bold=True, color=col)
        add_textbox(s3, x + 0.28, 4.95, 3.2, 0.38, head, font_size=15, bold=True, color=pal["text_primary"])
        add_textbox(s3, x + 0.28, 5.42, 3.2, 1.2, desc, font_size=11.5, bold=False, color=pal["text_secondary"], line_spacing=1.35)

    # =========================================================================
    # SLIDE 4: THE UNFAIR ADVANTAGE — UNIFIED BACKEND & RAPID HARDWARE ENGINE
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    add_bg(s4, prs, bgs[3])
    add_slide_header(
        s4,
        eyebrow="03 · Unfair Advantage & Unit Economics",
        title="Many Form Factors. One Unified AI & Subscription OS.",
        subtitle="Single-product hardware startups must sell 10M+ units to win. Our portfolio model wins at 100K+ units per line.",
        pal=pal, slide_num=4
    )

    # 4 Big Metric Cards across the top
    metrics = [
        ("< 9 Months", "Concept to 1,000 Units", "Total cycle from initial idea to first 1,000 units landing in the US.", pal["accent_lime"]),
        ("$150K–$200K", "All-In Launch CapEx", "Total R&D + tooling + COGS for the first 1,000 US units per product.", pal["accent_mint"]),
        ("100K+ Units", "Success Threshold", "Profitable scale per product line—no 10M-unit single-product gamble.", pal["accent_lavender"]),
        ("100% US Market", "Focused Go-To-Market", "Exclusively built and launched for US consumers with high subscription LTV.", pal["accent_amber"]),
    ]
    for i, (big_num, m_title, m_desc, col) in enumerate(metrics):
        x = 0.85 + i * 2.95
        add_card(s4, x, 2.15, 2.78, 2.30, fill_color=pal["card_bg"], border_color=pal["card_border"])
        add_textbox(s4, x + 0.22, 2.38, 2.34, 0.55, big_num, font_size=24, bold=True, color=col)
        add_textbox(s4, x + 0.22, 3.00, 2.34, 0.35, m_title, font_size=12.5, bold=True, color=pal["text_primary"])
        add_textbox(s4, x + 0.22, 3.38, 2.34, 0.90, m_desc, font_size=10.5, bold=False, color=pal["text_secondary"], line_spacing=1.3)

    # Architecture / Shared Backend Visual Diagram at Bottom
    add_card(s4, 0.85, 4.72, 11.63, 2.10, fill_color=pal["card_bg_alt"], border_color=pal["accent_lime"], border_pt=1.25)
    add_textbox(
        s4, 1.20, 4.95, 4.2, 0.35,
        "THE BANRAI SHARED CORE",
        font_size=10.5, bold=True, color=pal["accent_lime"]
    )
    add_textbox(
        s4, 1.20, 5.25, 4.4, 0.75,
        "Unified AI + Subscription Backend",
        font_size=20, bold=True, color=pal["text_primary"]
    )
    add_textbox(
        s4, 1.20, 5.75, 4.4, 0.85,
        "Reused across every brand & device—slashing engineering time, initial CapEx, and ongoing maintenance.",
        font_size=11.5, bold=False, color=pal["text_secondary"], line_spacing=1.32
    )

    # 3 Modules on the right of the architecture box
    modules = [
        ("Voice & Dialogue Engine", "Low-latency speech, memory & persona orchestration"),
        ("Generative Media Pipeline", "Live image, animation & story synthesis on tap"),
        ("Hard-Subscription Billing OS", "Unified token metering, trial bundling & recurring billing"),
    ]
    for i, (m_name, m_sub) in enumerate(modules):
        mx = 5.95 + i * 2.08
        add_card(s4, mx, 5.00, 1.95, 1.55, fill_color=pal["card_bg"], border_color=pal["card_border"])
        add_textbox(s4, mx + 0.16, 5.18, 1.63, 0.50, m_name, font_size=11.5, bold=True, color=pal["text_primary"], line_spacing=1.2)
        add_textbox(s4, mx + 0.16, 5.75, 1.63, 0.68, m_sub, font_size=9.5, bold=False, color=pal["text_secondary"], line_spacing=1.25)

    # =========================================================================
    # SLIDE 5: LAUNCHING DEC 2026 (FIRST 1,000 UNITS EACH IN US MARKET)
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    add_bg(s5, prs, bgs[4])
    add_slide_header(
        s5,
        eyebrow="04 · Launching December 2026 · 1,000 US Units Each",
        title="Wave 1 Products: On Schedule & Within Budget",
        subtitle="Our first two hardware lines hit the US market in Dec 2026 (1,000 units each), tracking at or below our $150K–$200K target.",
        pal=pal, slide_num=5
    )

    # Left Column: Product 1 — Living Photo Frame
    add_card(s5, 0.85, 2.12, 5.65, 4.75, fill_color=pal["card_bg"], border_color=pal["card_border"])
    add_image_placeholder(
        s5, 1.10, 2.32, 5.15, 2.45,
        "[ Product Image Placeholder · Magical Photo Frame ]",
        "Drop static or animated concept asset here (16:9 / 4:3)",
        pal=pal, accent_color=pal["accent_lime"]
    )
    add_pill_badge(s5, 1.10, 4.92, 1.95, 0.28, "DEC 2026 · 1,000 UNITS", bg_color=pal["pill_bg"], text_color=pal["pill_text"], font_size=8.5)
    add_textbox(s5, 1.10, 5.28, 5.15, 0.38, "Magical Living Photo Frame", font_size=17, bold=True, color=pal["text_primary"])
    add_bullet_list(
        s5, 1.10, 5.68, 5.15, 1.05,
        [
            ("Harry Potter-Style Portraits:", "Turns a single uploaded photo into living, context-aware animation bundles."),
            ("Presence & Weather Aware:", "Waves hello as you walk by—or opens an umbrella inside the photo when it rains outside."),
        ],
        pal=pal, accent_color=pal["accent_lime"], font_size=11, spacing=6
    )

    # Right Column: Product 2 — Pocket Interactive Bible
    add_card(s5, 6.83, 2.12, 5.65, 4.75, fill_color=pal["card_bg"], border_color=pal["card_border"])
    add_image_placeholder(
        s5, 7.08, 2.32, 5.15, 2.45,
        "[ Product Image Placeholder · Pocket Interactive Bible ]",
        "Drop E-Ink handheld hardware render / photo here",
        pal=pal, accent_color=pal["accent_mint"]
    )
    add_pill_badge(s5, 7.08, 4.92, 1.95, 0.28, "DEC 2026 · 1,000 UNITS", bg_color=pal["pill_bg"], text_color=pal["pill_text"], font_size=8.5)
    add_textbox(s5, 7.08, 5.28, 5.15, 0.38, "Pocket Interactive Bible", font_size=17, bold=True, color=pal["text_primary"])
    add_bullet_list(
        s5, 7.08, 5.68, 5.15, 1.05,
        [
            ("Standalone E-Ink + 4G:", "Dedicated, distraction-free sanctuary with built-in cellular connectivity."),
            ("Trusted Christian Companion:", "Never lectures; deepens faith and Scripture understanding through warm daily dialogue."),
        ],
        pal=pal, accent_color=pal["accent_mint"], font_size=11, spacing=6
    )

    # =========================================================================
    # SLIDE 6: H1 2027 PIPELINE (PART 1: DREAM PRINTER & VOICE WALKIE-TALKIE)
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    add_bg(s6, prs, bgs[5])
    add_slide_header(
        s6,
        eyebrow="05 · H1 2027 Pipeline · Currently in Prototyping",
        title="Wave 2: Capturing Morning Wonder & Voice Play",
        subtitle="Expanding into new daily rituals—from the moment you wake up to tactile, screen-free voice gaming.",
        pal=pal, slide_num=6
    )

    # Left Column: Product 3 — Dream Printer
    add_card(s6, 0.85, 2.12, 5.65, 4.75, fill_color=pal["card_bg"], border_color=pal["card_border"])
    add_image_placeholder(
        s6, 1.10, 2.32, 5.15, 2.45,
        "[ Product Image Placeholder · Dream Printer ]",
        "Drop bedside alarm-clock form factor & dream diary UI image here",
        pal=pal, accent_color=pal["accent_lavender"]
    )
    add_pill_badge(s6, 1.10, 4.92, 2.15, 0.28, "H1 2027 · PROTOTYPING", bg_color=pal["card_bg_alt"], text_color=pal["accent_lavender"], font_size=8.5)
    add_textbox(s6, 1.10, 5.28, 5.15, 0.38, "Dream Printer", font_size=17, bold=True, color=pal["text_primary"])
    add_bullet_list(
        s6, 1.10, 5.68, 5.15, 1.05,
        [
            ("One-Press Morning Ritual:", "Wake up, press a button, and speak your dream aloud; generates dream art + audio transcript."),
            ("Living Dream Diary:", "Co-weaves fragments into stories and surfaces hidden threads across past dreams."),
        ],
        pal=pal, accent_color=pal["accent_lavender"], font_size=11, spacing=6
    )

    # Right Column: Product 4 — Walkie-Talkie Voice Game
    add_card(s6, 6.83, 2.12, 5.65, 4.75, fill_color=pal["card_bg"], border_color=pal["card_border"])
    add_image_placeholder(
        s6, 7.08, 2.32, 5.15, 2.45,
        "[ Product Image Placeholder · Voice Adventure Walkie-Talkie ]",
        "Drop handheld walkie-talkie gaming hardware image here",
        pal=pal, accent_color=pal["accent_amber"]
    )
    add_pill_badge(s6, 7.08, 4.92, 2.15, 0.28, "H1 2027 · PROTOTYPING", bg_color=pal["card_bg_alt"], text_color=pal["accent_amber"], font_size=8.5)
    add_textbox(s6, 7.08, 5.28, 5.15, 0.38, "Tactile Voice Gaming Walkie-Talkie", font_size=17, bold=True, color=pal["text_primary"])
    add_bullet_list(
        s6, 7.08, 5.68, 5.15, 1.05,
        [
            ("A Stranded Friend on the Line:", "A live character trapped on an alien planet or escape room calls for your help."),
            ("100% Voice Co-Op:", "Calm them down, guide exploration, and solve unfolding incidents together to advance."),
        ],
        pal=pal, accent_color=pal["accent_amber"], font_size=11, spacing=6
    )

    # =========================================================================
    # SLIDE 7: H1 2027 PIPELINE (PART 2: E-INK CHILDREN'S DOODLE BOARD)
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    add_bg(s7, prs, bgs[6])
    add_slide_header(
        s7,
        eyebrow="06 · H1 2027 Pipeline · Currently in Prototyping",
        title="Wave 2 Spotlight: E-Ink Children’s Story Doodle Pad",
        subtitle="How children should experience AI—long before they even know what 'AI' means.",
        pal=pal, slide_num=7
    )

    # Spacious Split Layout: Left Story & Interaction Pillars, Right Large Visual Placeholder
    add_card(s7, 0.85, 2.15, 5.15, 4.70, fill_color=pal["card_bg"], border_color=pal["card_border"])
    add_pill_badge(s7, 1.15, 2.42, 2.25, 0.30, "H1 2027 · PROTOTYPING", bg_color=pal["pill_bg"], text_color=pal["pill_text"], font_size=8.5)
    add_textbox(s7, 1.15, 2.88, 4.55, 0.45, "Eye-Friendly E-Ink Doodle Pad", font_size=20, bold=True, color=pal["text_primary"])
    add_textbox(
        s7, 1.15, 3.38, 4.55, 0.65,
        "A calm, paper-like canvas that meets every child’s sketch or handwritten curiosity on their own terms.",
        font_size=12, bold=False, color=pal["text_secondary"], line_spacing=1.35
    )
    add_bullet_list(
        s7, 1.15, 4.18, 4.55, 2.45,
        [
            ("Doodle-to-Comic Co-Creation:", "Turns a child’s sketch into the opening scene of a multi-panel comic story—collaborating back and forth."),
            ("Visual Q&A by Drawing:", "Kids can jot down a question or draw what they’re wondering about and receive a gentle, illustrated answer."),
            ("Screen-Time Without Burnout:", "Glare-free E-Ink hardware built for open-ended imagination, not addictive video loops."),
        ],
        pal=pal, accent_color=pal["accent_mint"], font_size=11.5, spacing=10
    )

    # Right Extra-Large Image Placeholder
    add_image_placeholder(
        s7, 6.28, 2.15, 6.20, 4.70,
        "[ Hero Image Placeholder · E-Ink Kids’ Story Doodle Pad ]",
        "Drop large product photo + sample child doodle-to-comic interaction here",
        pal=pal, accent_color=pal["accent_mint"]
    )

    # =========================================================================
    # SLIDE 8: THE DATA MOAT & 6–10 PRODUCTS/YEAR FLYWHEEL
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    add_bg(s8, prs, bgs[7])
    add_slide_header(
        s8,
        eyebrow="07 · The Compounding Moat",
        title="Capturing the Data That Doesn’t Exist on the Internet",
        subtitle="Public web data teaches AI how to work. Only our hardware portfolio captures how humans play, wonder, and laugh.",
        pal=pal, slide_num=8
    )

    # 3 Connected Flywheel Columns
    flywheel = [
        (
            "STEP 01 · PORTFOLIO PACE",
            "6–10 New Products / Year",
            "Backed by a deep backlog of form factors, we launch 6–10 distinct Fun AI devices every year on our shared backend.",
            "Low $150K–$200K CapEx per bet",
            pal["accent_lime"]
        ),
        (
            "STEP 02 · PROPRIETARY SIGNALS",
            "Spontaneous Joy & Play Data",
            "We capture how people interact with AI when seeking happiness, stories, and companionship—signals absent from the open web.",
            "100% exclusive first-party telemetry",
            pal["accent_mint"]
        ),
        (
            "STEP 03 · COMPOUNDING LEAD",
            "The Only Real “Fun AI” Model",
            "Every conversation across every device makes our shared backend wittier, warmer, and more human—widening our moat daily.",
            "Higher retention & subscription LTV",
            pal["accent_lavender"]
        ),
    ]
    for i, (f_step, f_title, f_body, f_foot, col) in enumerate(flywheel):
        x = 0.85 + i * 3.94
        add_card(s8, x, 2.20, 3.75, 4.55, fill_color=pal["card_bg"], border_color=col, border_pt=1.2)
        add_textbox(s8, x + 0.30, 2.50, 3.15, 0.30, f_step, font_size=9.5, bold=True, color=col)
        add_textbox(s8, x + 0.30, 2.90, 3.15, 0.70, f_title, font_size=19, bold=True, color=pal["text_primary"], line_spacing=1.2)
        add_textbox(s8, x + 0.30, 3.75, 3.15, 1.65, f_body, font_size=12, bold=False, color=pal["text_secondary"], line_spacing=1.4)

        # Bottom highlight pill inside each card
        add_card(s8, x + 0.28, 5.85, 3.19, 0.55, fill_color=pal["card_bg_alt"], border_color=pal["card_border"])
        add_textbox(
            s8, x + 0.38, 5.98, 2.99, 0.30, f_foot,
            font_size=10.5, bold=True, color=col, align=PP_ALIGN.CENTER
        )

    # =========================================================================
    # SLIDE 9: CLOSING / SUMMARY SLIDE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    add_bg(s9, prs, bgs[8])
    add_slide_header(
        s9,
        eyebrow="08 · The Banrai Opportunity",
        title="Delightfully Useless. Commercially Unstoppable.",
        subtitle="A counter-trend consumer AI ecosystem built for recurring subscription scale.",
        pal=pal, slide_num=9
    )

    summary_cards = [
        ("White-Space Category", "Fun AI > Functional AI", "Owning daily consumer joy, imagination, and voice companionship while the rest of tech fights over enterprise tasks.", pal["accent_lime"]),
        ("Disciplined Hardware Engine", "$150K–$200K · < 9 Months", "1,000 US units launched in under 9 months per product—powered by a single reusable AI + subscription backend.", pal["accent_mint"]),
        ("Immediate US Traction", "2 Launching · 3 Prototyping", "Photo Frame & Pocket Bible shipping Dec 2026 (1K units each); Dream Printer, Walkie-Talkie & Doodle Pad in H1 2027.", pal["accent_lavender"]),
    ]
    for i, (s_tag, s_head, s_desc, col) in enumerate(summary_cards):
        x = 0.85 + i * 3.94
        add_card(s9, x, 2.15, 3.75, 2.85, fill_color=pal["card_bg"], border_color=pal["card_border"])
        add_textbox(s9, x + 0.28, 2.42, 3.2, 0.28, s_tag.upper(), font_size=9.5, bold=True, color=col)
        add_textbox(s9, x + 0.28, 2.78, 3.2, 0.45, s_head, font_size=16, bold=True, color=pal["text_primary"])
        add_textbox(s9, x + 0.28, 3.32, 3.2, 1.4, s_desc, font_size=11.5, bold=False, color=pal["text_secondary"], line_spacing=1.38)

    # Closing Banner
    add_card(s9, 0.85, 5.30, 11.63, 1.50, fill_color=pal["card_bg_alt"], border_color=pal["accent_lime"], border_pt=1.5)
    add_banrai_logo(s9, 1.15, 5.65, size="small", pal=pal)
    add_textbox(
        s9, 1.25, 6.08, 4.5, 0.38,
        "Make Humans Talk Again.",
        font_size=16, bold=True, color=pal["text_primary"]
    )
    add_textbox(
        s9, 6.20, 5.65, 5.9, 0.80,
        "banrai.ai   ·   hello@banrai.ai\nSeed+ Investor Presentation · US Consumer AI Ecosystem",
        font_size=12, bold=False, color=pal["text_secondary"],
        align=PP_ALIGN.RIGHT, line_spacing=1.45
    )

    out_path = os.path.join(OUT_DIR, output_filename)
    prs.save(out_path)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    build_deck("Banrai_Seed_Plus_Deck.pptx", mode="dark")
    build_deck("Banrai_Seed_Plus_Deck_Light.pptx", mode="light")
