import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(OUT_DIR, "product_photos", "processed")

# ==============================================================================
# PANTONE-INSPIRED CALM LIGHT PALETTE
# ==============================================================================
# Designed for effortless readability and calm visual hierarchy.
# Bright Banrai Lime (#CAFB5B) is strictly reserved for 1 key callout per slide.
PAL = {
    "bg_canvas": RGBColor(244, 242, 237),       # Pantone 11-4201 Cloud Dancer / Warm Alabaster (#F4F2ED)
    "card_white": RGBColor(251, 250, 247),      # Pantone Marshmallow / Soft Paper (#FBFAF7)
    "card_stone": RGBColor(236, 233, 225),      # Pantone 12-0104 Warm Sand / Travertine (#ECE9E1)
    "card_sage": RGBColor(225, 232, 224),       # Pantone Soft Celadon / Sage Tint (#E1E8E0)
    "card_slate": RGBColor(224, 231, 236),      # Pantone Pale Mist / Slate Tint (#E0E7EC)
    "border_subtle": RGBColor(216, 212, 202),   # Pantone Pumice Stone (#D8D4CA)
    "border_strong": RGBColor(168, 164, 154),   # Pantone Warm Taupe Border (#A8A49A)
    "ink_primary": RGBColor(35, 38, 42),        # Pantone 19-4007 After Dark / Charcoal (#23262A)
    "ink_secondary": RGBColor(96, 101, 108),    # Pantone 17-4402 Neutral Gray (#60656C)
    "ink_muted": RGBColor(142, 146, 152),       # Pantone Harbor Mist (#8E9298)
    "sage_accent": RGBColor(88, 114, 92),       # Pantone 17-0210 Laurel Oak (#58725C)
    "slate_accent": RGBColor(78, 105, 122),     # Pantone 17-4412 Porcelain Blue (#4E697A)
    "terracotta_muted": RGBColor(166, 112, 96), # Pantone Muted Clay (#A67060)
    # RESERVED FOR SINGLE HERO CALLOUT PER SLIDE + LOGO DOT ONLY:
    "callout_lime": RGBColor(202, 251, 91),     # Banrai Signature Lime (#CAFB5B)
    "callout_lime_border": RGBColor(156, 204, 48),
}

FONT_MAIN = "Poppins"


def set_slide_bg(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color


def add_box(slide, left, top, width, height, fill_color=None, border_color=None,
            border_pt=1.0, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.05):
    shape = slide.shapes.add_shape(shape_type, Inches(left), Inches(top), Inches(width), Inches(height))
    if shape_type == MSO_SHAPE.ROUNDED_RECTANGLE and len(shape.adjustments) > 0:
        shape.adjustments[0] = radius
    if fill_color:
        shape.fill.solid()
        shape.fill.fore_color.rgb = fill_color
    else:
        shape.fill.background()
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(border_pt)
    else:
        shape.line.fill.background()
    return shape


def add_text(slide, left, top, width, height, text, size=14, bold=False,
             color=PAL["ink_primary"], align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.2):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    tf.margin_left = Inches(0)
    tf.margin_right = Inches(0)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = line
        p.alignment = align
        p.line_spacing = line_spacing
        p.font.name = FONT_MAIN
        p.font.size = Pt(size)
        p.font.bold = bold
        p.font.color.rgb = color
    return tb


def add_logo(slide, left, top, hero=False):
    if hero:
        add_text(slide, left, top, 3.3, 1.0, "Banrai", size=60, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.RIGHT)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left + 3.40), Inches(top + 0.48), Inches(0.22), Inches(0.22))
        dot.fill.solid()
        dot.fill.fore_color.rgb = PAL["callout_lime"]
        dot.line.color.rgb = PAL["callout_lime_border"]
        dot.line.width = Pt(1.0)
    else:
        add_text(slide, left, top, 1.1, 0.35, "Banrai", size=14, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.RIGHT)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left + 1.15), Inches(top + 0.11), Inches(0.09), Inches(0.09))
        dot.fill.solid()
        dot.fill.fore_color.rgb = PAL["callout_lime"]
        dot.line.color.rgb = PAL["callout_lime_border"]
        dot.line.width = Pt(0.75)


def add_header(slide, section_label, title, slide_label, title_width=11.60):
    set_slide_bg(slide, PAL["bg_canvas"])
    # Calm section label
    add_text(slide, 0.9, 0.55, 6.0, 0.28, section_label.upper(), size=9.5, bold=True, color=PAL["sage_accent"])
    # Top-right logo
    add_logo(slide, 11.15, 0.50, hero=False)
    # Bottom-right slide counter
    add_text(slide, 11.3, 6.90, 1.15, 0.28, slide_label, size=9, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.RIGHT)
    # Crisp, editorial headline
    add_text(slide, 0.9, 0.88, title_width, 0.55, title, size=28, bold=True, color=PAL["ink_primary"], line_spacing=1.12)


def add_image_placeholder(slide, left, top, width, height, title, subtitle):
    add_box(slide, left, top, width, height, fill_color=PAL["card_stone"], border_color=PAL["border_strong"], border_pt=1.25, radius=0.04)
    cx = left + width / 2.0
    cy = top + height / 2.0
    # Minimal camera / frame icon badge
    add_box(slide, cx - 0.26, cy - 0.48, 0.52, 0.52, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], shape_type=MSO_SHAPE.OVAL)
    add_text(slide, cx - 0.26, cy - 0.48, 0.52, 0.52, "＋", size=16, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(slide, left + 0.3, cy + 0.14, width - 0.6, 0.32, title, size=11.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
    add_text(slide, left + 0.3, cy + 0.42, width - 0.6, 0.32, subtitle, size=9.5, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER)


def add_product_image(slide, left, top, width, height, img_filename, radius=0.04):
    add_box(slide, left - 0.02, top - 0.02, width + 0.04, height + 0.04,
            fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], border_pt=1.0, radius=radius)
    img_path = os.path.join(IMG_DIR, img_filename)
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(left), Inches(top), width=Inches(width), height=Inches(height))


def build_pantone_deck(output_path):
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    # ==========================================================================
    # SLIDE 1: COVER — CALM, SPACIOUS, MINIMAL
    # ==========================================================================
    s1 = prs.slides.add_slide(blank)
    set_slide_bg(s1, PAL["bg_canvas"])

    # Soft architectural frame card
    add_box(s1, 0.75, 0.65, 11.833, 6.20, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)

    # Logo centered
    add_logo(s1, 4.70, 1.85, hero=True)

    # Crisp 1-line thesis + quiet mission
    add_text(
        s1, 1.5, 3.15, 10.333, 0.65,
        "Consumer AI Hardware Built for Joy, Not Chores.",
        size=28, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER
    )
    add_text(
        s1, 2.5, 3.82, 8.333, 0.45,
        "Make Humans Talk Again  ·  Seed+ Investor Presentation",
        size=13, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER
    )

    # 3 Minimal Stat Pills at bottom — only middle/key one uses bright lime callout
    s1_stats = [
        ("100% Hard-Subscription", "SaaS recurring model", PAL["card_stone"], PAL["border_subtle"]),
        ("< 9 Mos  ·  $150K–$200K Each", "Concept to 1,000 US units", PAL["callout_lime"], PAL["callout_lime_border"]),
        ("6–10 Products / Year", "Powered by 1 shared backend", PAL["card_stone"], PAL["border_subtle"]),
    ]
    for i, (big, sub, bg_c, brd_c) in enumerate(s1_stats):
        x = 1.65 + i * 3.45
        add_box(s1, x, 4.95, 3.15, 1.15, fill_color=bg_c, border_color=brd_c, radius=0.08)
        add_text(s1, x + 0.08, 5.18, 2.99, 0.35, big, size=12.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
        add_text(s1, x + 0.15, 5.55, 2.85, 0.30, sub, size=10.5, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)

    # ==========================================================================
    # SLIDE 2: THE COUNTER-TREND — VISUAL POSITIONING GRAPHIC
    # ==========================================================================
    s2 = prs.slides.add_slide(blank)
    add_header(s2, "01 · Category Positioning", "Everyone Builds Functional AI. We Build Fun AI.", "02 / 07")

    # Left: Visual 2x2 Positioning Matrix Graphic
    add_box(s2, 0.90, 1.75, 6.80, 4.90, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_text(s2, 1.25, 2.00, 6.10, 0.30, "CONSUMER AI LANDSCAPE", size=9.5, bold=True, color=PAL["ink_muted"])

    # Horizontal & Vertical Axes inside the matrix card
    # Horizontal bar (Work/Tasks <---> Joy/Play)
    add_box(s2, 1.50, 4.30, 5.60, 0.03, fill_color=PAL["border_strong"], shape_type=MSO_SHAPE.RECTANGLE)
    # Vertical bar (Screen Apps <---> Tactile Hardware)
    add_box(s2, 4.30, 2.45, 0.03, 3.70, fill_color=PAL["border_strong"], shape_type=MSO_SHAPE.RECTANGLE)

    # Axis Labels
    add_text(s2, 1.45, 4.40, 1.8, 0.28, "← Work & Tasks", size=9.5, bold=True, color=PAL["ink_muted"])
    add_text(s2, 5.30, 4.40, 1.8, 0.28, "Play & Daily Joy →", size=9.5, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.RIGHT)
    add_text(s2, 3.40, 2.15, 1.8, 0.28, "↑ Tactile Hardware", size=9.5, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)
    add_text(s2, 3.40, 6.22, 1.8, 0.28, "↓ Screen Chatbots", size=9.5, bold=True, color=PAL["ink_muted"], align=PP_ALIGN.CENTER)

    # Bottom-Left Quadrant: Crowded Red Ocean
    add_box(s2, 1.65, 4.75, 2.35, 1.20, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.08)
    add_text(s2, 1.80, 4.92, 2.05, 0.30, "Functional AI Crowd", size=11, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)
    add_text(s2, 1.80, 5.25, 2.05, 0.50, "Emails, coding, productivity\n(99% of VC & Big Tech)", size=9.5, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER)

    # Top-Left Quadrant: Generic AI Pins
    add_box(s2, 1.65, 2.75, 2.35, 1.20, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.08)
    add_text(s2, 1.80, 2.95, 2.05, 0.30, "Utility Wearables", size=11, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)
    add_text(s2, 1.80, 3.28, 2.05, 0.50, "Trying to replace the smartphone", size=9.5, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER)

    # Top-Right Quadrant: BANRAI (Single Bright Lime Hero Callout!)
    add_box(s2, 4.60, 2.65, 2.45, 1.40, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], border_pt=1.5, radius=0.08)
    add_text(s2, 4.75, 2.85, 2.15, 0.35, "Banrai · “Fun AI”", size=13, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
    add_text(s2, 4.75, 3.22, 2.15, 0.65, "Delightfully “useless” hardware for daily joy & conversation", size=10, bold=False, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)

    # Right Column: 3 Crisp Essence Cards
    essence_cards = [
        ("01 · Counter-Trend", "Delightfully “Useless”", "Zero task optimization. Built purely for curiosity, laughter, and warmth.", PAL["card_white"]),
        ("02 · Unifying Theme", "“Make Humans Talk Again”", "Replaces passive screen scrolling with active voice, stories, and imagination.", PAL["card_sage"]),
        ("03 · Multi-Brand Strategy", "Ambient in Every Room", "Different brands & form factors—from bedside clocks to living room frames.", PAL["card_white"]),
    ]
    for i, (tag, head, desc, bg_c) in enumerate(essence_cards):
        y = 1.75 + i * 1.68
        add_box(s2, 8.00, y, 4.43, 1.50, fill_color=bg_c, border_color=PAL["border_subtle"], radius=0.05)
        add_text(s2, 8.28, y + 0.20, 3.9, 0.25, tag.upper(), size=9, bold=True, color=PAL["sage_accent"])
        add_text(s2, 8.28, y + 0.46, 3.9, 0.35, head, size=15, bold=True, color=PAL["ink_primary"])
        add_text(s2, 8.28, y + 0.85, 3.9, 0.50, desc, size=10.5, bold=False, color=PAL["ink_secondary"])

    # ==========================================================================
    # SLIDE 3: BUSINESS MODEL — VISUAL REVENUE & LIFECYCLE DIAGRAM
    # ==========================================================================
    s3 = prs.slides.add_slide(blank)
    add_header(s3, "02 · Business Model", "Hardware Is the Vessel. SaaS Is the Engine.", "03 / 07")

    # Top: Traditional Hardware (Muted Visual Track)
    add_box(s3, 0.90, 1.80, 11.53, 1.95, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.04)
    add_text(s3, 1.25, 2.02, 3.2, 0.28, "TRADITIONAL HARDWARE", size=9.5, bold=True, color=PAL["ink_muted"])
    add_text(s3, 1.25, 2.30, 3.2, 0.40, "One-Time Unit Margin", size=17, bold=True, color=PAL["ink_secondary"])
    add_text(s3, 1.25, 2.75, 3.2, 0.65, "Profit stops at checkout. Forced to push Gen-2 upgrades to survive.", size=10.5, bold=False, color=PAL["ink_muted"])

    # Visual Timeline Blocks for Traditional Hardware
    trad_steps = [
        ("Day 1: Sell Box", "One-off hardware margin"),
        ("Month 2–12", "$0 recurring revenue"),
        ("Year 2+", "Beg user to buy Gen-2"),
    ]
    for i, (t_head, t_sub) in enumerate(trad_steps):
        tx = 4.75 + i * 2.50
        add_box(s3, tx, 2.18, 2.25, 1.20, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.06)
        add_text(s3, tx + 0.15, 2.42, 1.95, 0.30, t_head, size=11.5, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)
        add_text(s3, tx + 0.15, 2.78, 1.95, 0.40, t_sub, size=10, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER)
        if i < 2:
            add_text(s3, tx + 2.25, 2.60, 0.25, 0.30, "→", size=14, bold=True, color=PAL["ink_muted"], align=PP_ALIGN.CENTER)

    # Bottom: Banrai Hard-Subscription Model (Visual SaaS Flow)
    add_box(s3, 0.90, 4.05, 11.53, 2.60, fill_color=PAL["card_white"], border_color=PAL["sage_accent"], border_pt=1.5, radius=0.04)
    add_text(s3, 1.25, 4.32, 3.2, 0.28, "THE BANRAI MODEL", size=9.5, bold=True, color=PAL["sage_accent"])
    add_text(s3, 1.25, 4.60, 3.2, 0.45, "100% Hard-Subscription", size=19, bold=True, color=PAL["ink_primary"])
    add_text(s3, 1.25, 5.37, 3.2, 1.10, "Real AI costs tokens—so there is no free tier. Hardware unlocks high-margin, SaaS-style recurring revenue.", size=10.5, bold=False, color=PAL["ink_secondary"])

    banrai_steps = [
        ("01 · Unbox", "Hardware + Free Months", "Ships with bundled trial months for instant magic", PAL["card_sage"], PAL["border_subtle"]),
        ("02 · Subscribe", "Mandatory Monthly Fee", "Hard subscription keeps the AI companion alive", PAL["callout_lime"], PAL["callout_lime_border"]),
        ("03 · Compound", "Continuous SaaS Value", "Cloud updates stories & memory—growing LTV", PAL["card_sage"], PAL["border_subtle"]),
    ]
    for i, (b_tag, b_head, b_sub, bg_c, brd_c) in enumerate(banrai_steps):
        bx = 4.75 + i * 2.50
        add_box(s3, bx, 4.35, 2.25, 2.00, fill_color=bg_c, border_color=brd_c, border_pt=1.25, radius=0.06)
        add_text(s3, bx + 0.15, 4.58, 1.95, 0.25, b_tag.upper(), size=9, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)
        add_text(s3, bx + 0.15, 4.88, 1.95, 0.45, b_head, size=12, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
        add_text(s3, bx + 0.15, 5.42, 1.95, 0.70, b_sub, size=9.5, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)
        if i < 2:
            add_text(s3, bx + 2.25, 5.15, 0.25, 0.30, "→", size=14, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.CENTER)

    # ==========================================================================
    # SLIDE 4: UNFAIR ADVANTAGE — HUB & SPOKE ARCHITECTURE + COST GRAPHIC
    # ==========================================================================
    s4 = prs.slides.add_slide(blank)
    add_header(s4, "03 · Unfair Advantage", "One Shared Backend Powers Dozens of Hardware Products.", "04 / 07", title_width=11.94)

    # LEFT SIDE: Visual Hub-and-Spoke Diagram (1 Backend -> Many Hardware Form Factors)
    add_box(s4, 0.90, 1.75, 6.75, 4.95, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_text(s4, 1.20, 1.98, 6.15, 0.28, "REUSABLE PLATFORM ARCHITECTURE", size=9.5, bold=True, color=PAL["sage_accent"])

    # Central Hub Box (Left-Center of diagram)
    add_box(s4, 1.25, 2.65, 2.45, 3.45, fill_color=PAL["card_sage"], border_color=PAL["sage_accent"], border_pt=1.5, radius=0.05)
    add_text(s4, 1.40, 2.90, 2.15, 0.30, "SHARED CORE", size=9, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.CENTER)
    add_text(s4, 1.40, 3.20, 2.15, 0.65, "1 Unified AI +\nBilling Backend", size=15, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)

    hub_pills = ["Conversational Voice OS", "Image & Story Engine", "Subscription & Metering"]
    for i, hp in enumerate(hub_pills):
        hy = 4.10 + i * 0.58
        add_box(s4, 1.42, hy, 2.11, 0.44, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.08)
        add_text(s4, 1.48, hy + 0.10, 1.99, 0.26, hp, size=9.5, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)

    # Connector lines + 6 Spoke Product Nodes on the right of the Hub
    spokes = [
        ("01 · Living Photo Frame", "Dec 2026"),
        ("02 · Pocket Interactive Bible", "Dec 2026"),
        ("03 · Dream Printer", "H1 2027"),
        ("04 · Voice Walkie-Talkie", "H1 2027"),
        ("05 · Kids’ E-Ink Doodle Pad", "H1 2027"),
        ("06–10+ · New Launches / Yr", "Ongoing Pipeline"),
    ]
    for i, (s_name, s_date) in enumerate(spokes):
        sy = 2.45 + i * 0.65
        # Horizontal connector line from Hub to Spoke
        add_box(s4, 3.70, sy + 0.24, 0.65, 0.02, fill_color=PAL["sage_accent"], shape_type=MSO_SHAPE.RECTANGLE)
        # Spoke Node
        is_last = (i == 5)
        node_bg = PAL["card_stone"] if not is_last else PAL["card_slate"]
        add_box(s4, 4.35, sy, 2.95, 0.50, fill_color=node_bg, border_color=PAL["border_subtle"], radius=0.08)
        add_text(s4, 4.50, sy + 0.13, 1.95, 0.26, s_name, size=10, bold=True, color=PAL["ink_primary"])
        add_text(s4, 6.30, sy + 0.14, 0.88, 0.24, s_date, size=8.5, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.RIGHT)

    # RIGHT SIDE: Visual Cost & Speed Comparison Bars
    add_box(s4, 7.90, 1.75, 4.53, 4.95, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_text(s4, 8.20, 1.98, 3.95, 0.28, "ECONOMICS PER HARDWARE LINE (US MARKET)", size=9.5, bold=True, color=PAL["ink_muted"])

    # Comparison 1: Time to First 1,000 US Units
    add_text(s4, 8.20, 2.40, 3.95, 0.28, "Time to Market (First 1,000 Units)", size=11, bold=True, color=PAL["ink_primary"])
    add_box(s4, 8.20, 2.74, 3.85, 0.34, fill_color=PAL["card_stone"], shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    add_text(s4, 8.32, 2.80, 3.60, 0.24, "Traditional Hardware:  18 – 24+ Months", size=9.5, bold=False, color=PAL["ink_secondary"])
    # Banrai Short Bar
    add_box(s4, 8.20, 3.16, 1.85, 0.36, fill_color=PAL["card_sage"], border_color=PAL["sage_accent"], shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    add_text(s4, 8.32, 3.22, 1.65, 0.24, "Banrai: < 9 Mos", size=10, bold=True, color=PAL["ink_primary"])

    # Comparison 2: Total CapEx to Launch 1,000 US Units (BRIGHT LIME HERO CALLOUT!)
    add_text(s4, 8.20, 3.78, 3.95, 0.28, "All-In Launch Cost (R&D + First 1,000 Units)", size=11, bold=True, color=PAL["ink_primary"])
    add_box(s4, 8.20, 4.12, 3.85, 0.34, fill_color=PAL["card_stone"], shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    add_text(s4, 8.32, 4.18, 3.60, 0.24, "Traditional Hardware:  $3M – $10M+", size=9.5, bold=False, color=PAL["ink_secondary"])
    # Banrai Callout Bar
    add_box(s4, 8.20, 4.54, 2.35, 0.40, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], border_pt=1.5, shape_type=MSO_SHAPE.ROUNDED_RECTANGLE, radius=0.1)
    add_text(s4, 8.32, 4.61, 2.15, 0.26, "Banrai: $150K – $200K", size=10.5, bold=True, color=PAL["ink_primary"])

    # Comparison 3: Units Needed for a "Hit"
    add_text(s4, 8.20, 5.20, 3.95, 0.28, "Unit Threshold for a Winner", size=11, bold=True, color=PAL["ink_primary"])
    add_box(s4, 8.20, 5.54, 3.85, 0.85, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.06)
    add_text(
        s4, 8.38, 5.68, 3.50, 0.60,
        "Single-Product Co: Must sell 10M+ units\nBanrai Portfolio: Profitable hit at 100K+ units",
        size=10.5, bold=True, color=PAL["ink_primary"], line_spacing=1.35
    )

    # ==========================================================================
    # SLIDE 5: PRODUCT PORTFOLIO & ROADMAP AT A GLANCE (CONSOLIDATED!)
    # ==========================================================================
    s5 = prs.slides.add_slide(blank)
    add_header(s5, "04 · Product Roadmap (US Market Exclusively)", "5 Products in Motion. 6–10 New Launches Every Year.", "05 / 07")

    # Timeline Header Bar
    add_box(s5, 0.90, 1.75, 4.45, 0.42, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], radius=0.08)
    add_text(s5, 1.05, 1.84, 4.15, 0.26, "WAVE 1 · DEC 2026 (1,000 US UNITS EACH · ON BUDGET)", size=9.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)

    add_box(s5, 5.55, 1.75, 6.88, 0.42, fill_color=PAL["card_sage"], border_color=PAL["sage_accent"], radius=0.08)
    add_text(s5, 5.70, 1.84, 6.58, 0.26, "WAVE 2 · H1 2027 (CURRENTLY IN PROTOTYPING)", size=9.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)

    # 5 Clean Visual Product Cards in a 5-Column Strip
    products_overview = [
        ("01", "Magical Living\nPhoto Frame", "Dec 2026", "Portraits wave hello & react to live local weather", PAL["card_white"], PAL["callout_lime_border"], "s5_01_photoframe.png"),
        ("02", "Pocket Interactive\nBible", "Dec 2026", "Standalone E-Ink + 4G daily Christian companion", PAL["card_white"], PAL["callout_lime_border"], "s5_02_bible.png"),
        ("03", "Dream\nPrinter", "H1 2027", "One-button morning dream art & connected diary", PAL["card_white"], PAL["border_subtle"], "s5_03_dreamprinter.png"),
        ("04", "Voice Gaming\nWalkie-Talkie", "H1 2027", "Co-op voice rescue with a stranded character", PAL["card_white"], PAL["border_subtle"], "s5_04_mayday.png"),
        ("05", "Kids’ E-Ink\nDoodle Pad", "H1 2027", "Turns children’s sketches into interactive comics", PAL["card_white"], PAL["border_subtle"], "s5_05_doodleboard.png"),
    ]
    for i, (num, p_name, p_date, p_hook, bg_c, brd_c, p_img) in enumerate(products_overview):
        px = 0.90 + i * 2.34
        add_box(s5, px, 2.32, 2.18, 3.45, fill_color=bg_c, border_color=brd_c, border_pt=1.25, radius=0.04)
        # Curated & color-graded product thumbnail inside each card
        add_product_image(s5, px + 0.16, 2.48, 1.86, 1.35, p_img, radius=0.05)
        # Product Title & 1-sentence essence
        add_text(s5, px + 0.18, 3.98, 1.82, 0.24, p_date.upper(), size=8.5, bold=True, color=PAL["sage_accent"])
        add_text(s5, px + 0.18, 4.22, 1.82, 0.60, p_name, size=13, bold=True, color=PAL["ink_primary"], line_spacing=1.15)
        add_text(s5, px + 0.18, 4.90, 1.82, 0.75, p_hook, size=9.5, bold=False, color=PAL["ink_secondary"], line_spacing=1.25)

    # Bottom Backlog Strip + Pointer to Appendix
    add_box(s5, 0.90, 5.95, 11.53, 0.72, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.05)
    add_text(
        s5, 1.20, 6.18, 7.20, 0.30,
        "Deep Backlog:  Launching 6–10 new Fun AI hardware products every year.",
        size=11.5, bold=True, color=PAL["ink_primary"]
    )
    add_text(
        s5, 8.20, 6.19, 3.95, 0.30,
        "See Appendix (A1–A3) for full product visuals →",
        size=10.5, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.RIGHT
    )

    # ==========================================================================
    # SLIDE 6: THE DATA MOAT — VISUAL FLYWHEEL DIAGRAM
    # ==========================================================================
    s6 = prs.slides.add_slide(blank)
    add_header(s6, "05 · Defensibility & Moat", "Capturing the Data That Doesn’t Exist on the Internet.", "06 / 07", title_width=11.02)

    # Top Contrast Strip: Public Web Data vs Banrai Data
    add_box(s6, 0.90, 1.75, 5.60, 1.25, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.04)
    add_text(s6, 1.20, 1.95, 5.0, 0.25, "PUBLIC INTERNET DATA", size=9, bold=True, color=PAL["ink_muted"])
    add_text(s6, 1.20, 2.22, 5.0, 0.55, "Teaches AI how to work, code, and summarize.\nEvery competitor scrapes the exact same web.", size=11, bold=False, color=PAL["ink_secondary"])

    add_box(s6, 6.83, 1.75, 5.60, 1.25, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], border_pt=1.5, radius=0.04)
    add_text(s6, 7.13, 1.95, 5.0, 0.25, "BANRAI PROPRIETARY DATA", size=9, bold=True, color=PAL["ink_primary"])
    add_text(s6, 7.13, 2.22, 5.0, 0.55, "Captures how humans play, laugh, and wonder.\nZero public dataset exists—it must be earned live.", size=11, bold=True, color=PAL["ink_primary"])

    # Bottom Visual 4-Node Flywheel Diagram
    fly_nodes = [
        ("01 · Ship", "6–10 Products / Yr", "Ambient devices across daily life", PAL["card_white"]),
        ("02 · Spark", "Spontaneous Play", "Users talk for joy, not chores", PAL["card_sage"]),
        ("03 · Collect", "Exclusive Joy Data", "Un-scrapable emotional signals", PAL["card_white"]),
        ("04 · Evolve", "Smarter “Fun AI”", "Compounds retention across all SKUs", PAL["card_sage"]),
    ]
    for i, (f_step, f_head, f_sub, bg_c) in enumerate(fly_nodes):
        fx = 0.90 + i * 2.98
        add_box(s6, fx, 3.45, 2.60, 2.45, fill_color=bg_c, border_color=PAL["border_strong"], radius=0.05)
        add_text(s6, fx + 0.20, 3.75, 2.20, 0.26, f_step.upper(), size=9.5, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.CENTER)
        add_text(s6, fx + 0.20, 4.15, 2.20, 0.45, f_head, size=15, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
        add_text(s6, fx + 0.20, 4.70, 2.20, 0.70, f_sub, size=10.5, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)
        if i < 3:
            add_text(s6, fx + 2.60, 4.45, 0.38, 0.35, "→", size=18, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.CENTER)

    # Feedback loop bar under the 4 nodes
    add_box(s6, 1.80, 6.12, 9.73, 0.45, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.08)
    add_text(s6, 2.00, 6.22, 9.33, 0.28, "↺   Continuous Compounding Loop Across Every Brand & Hardware Line", size=10.5, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER)

    # ==========================================================================
    # SLIDE 7: CLOSING SUMMARY — MINIMAL & MEMORABLE
    # ==========================================================================
    s7 = prs.slides.add_slide(blank)
    add_header(s7, "06 · Summary", "Delightfully “Useless.” Commercially Unstoppable.", "07 / 07")

    pillars = [
        ("Category of One", "Fun AI > Functional AI", "Owning daily consumer joy & voice while the rest of tech fights over spreadsheets.", PAL["card_white"], PAL["border_subtle"]),
        ("Asymmetric Hardware Math", "< 9 Mos  ·  $150K–$200K", "1 shared AI + SaaS backend powers 6–10 US hardware launches per year.", PAL["callout_lime"], PAL["callout_lime_border"]),
        ("Compounding Data Moat", "2 Launching · 3 Prototyping", "2,000 US units shipping Dec 2026; building the only dataset of human play.", PAL["card_white"], PAL["border_subtle"]),
    ]
    for i, (p_tag, p_head, p_desc, bg_c, brd_c) in enumerate(pillars):
        px = 0.90 + i * 3.94
        add_box(s7, px, 1.85, 3.65, 3.10, fill_color=bg_c, border_color=brd_c, border_pt=1.25, radius=0.04)
        add_text(s7, px + 0.30, 2.18, 3.05, 0.26, p_tag.upper(), size=9.5, bold=True, color=PAL["ink_secondary"])
        add_text(s7, px + 0.30, 2.55, 3.05, 0.55, p_head, size=18, bold=True, color=PAL["ink_primary"])
        add_text(s7, px + 0.30, 3.25, 3.05, 1.20, p_desc, size=11.5, bold=False, color=PAL["ink_secondary"], line_spacing=1.35)

    # Calm Footer Callout Card
    add_box(s7, 0.90, 5.25, 11.53, 1.40, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.04)
    add_logo(s7, 0.87, 5.58, hero=False)
    add_text(s7, 1.30, 5.98, 4.5, 0.35, "Make Humans Talk Again.", size=14, bold=True, color=PAL["ink_primary"])
    add_text(s7, 6.48, 5.98, 5.55, 0.25, "Appendix Follows →", size=11.5, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.RIGHT, line_spacing=1.4)

    # ==========================================================================
    # APPENDIX A1: WAVE 1 PRODUCTS (DEC 2026) — GALLERY VIEW
    # ==========================================================================
    sa1 = prs.slides.add_slide(blank)
    add_header(sa1, "Appendix A1 · Wave 1 Product Gallery (Dec 2026)", "Shipping Dec 2026: 1,000 US Units Each (On Budget)", "A1 / A3")

    # Left: Magical Living Photo Frame (Huge Image Space + 2 Short Lines)
    add_box(sa1, 0.90, 1.72, 5.60, 5.00, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_product_image(sa1, 1.12, 1.92, 5.16, 3.30, "a1_photoframe_collage.png", radius=0.03)
    add_box(sa1, 1.12, 5.38, 1.75, 0.28, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], radius=0.15)
    add_text(sa1, 1.18, 5.42, 1.63, 0.22, "DEC 2026 · 1K UNITS", size=8.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
    add_text(sa1, 3.00, 5.36, 3.30, 0.32, "Magical Living Photo Frame", size=15, bold=True, color=PAL["ink_primary"])
    add_text(sa1, 1.12, 5.80, 5.16, 0.69, "• Harry Potter-style living portraits that wave hello as you walk by.\n• Syncs with live local weather (pulls out an umbrella when it rains outside).", size=10.0, bold=False, color=PAL["ink_secondary"], line_spacing=1.35)

    # Right: Pocket Interactive Bible
    add_box(sa1, 6.83, 1.72, 5.60, 5.00, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_product_image(sa1, 7.05, 1.92, 5.16, 3.30, "a1_bible_preview.png", radius=0.03)
    add_box(sa1, 7.05, 5.38, 1.75, 0.28, fill_color=PAL["card_sage"], border_color=PAL["sage_accent"], radius=0.15)
    add_text(sa1, 7.11, 5.42, 1.63, 0.22, "DEC 2026 · 1K UNITS", size=8.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
    add_text(sa1, 8.93, 5.36, 3.30, 0.32, "Pocket Interactive Bible", size=15, bold=True, color=PAL["ink_primary"])
    add_text(sa1, 7.05, 5.80, 5.16, 0.66, "• Standalone E-Ink + 4G cellular device for focused, distraction-free faith.\n• Warm Christian companion that deepens Scripture understanding via daily talk.", size=10.0, bold=False, color=PAL["ink_secondary"], line_spacing=1.35)

    # ==========================================================================
    # APPENDIX A2: WAVE 2 PRODUCTS (H1 2027 PROTOTYPING) — GALLERY VIEW
    # ==========================================================================
    sa2 = prs.slides.add_slide(blank)
    add_header(sa2, "Appendix A2 · Wave 2 Product Gallery (H1 2027)", "Prototyping for H1 2027: Morning Rituals & Voice Gaming", "A2 / A3", title_width=11.49)

    # Left: Dream Printer
    add_box(sa2, 0.90, 1.72, 5.60, 5.00, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_product_image(sa2, 1.12, 1.92, 5.16, 3.30, "a2_dreamprinter_collage.png", radius=0.03)
    add_box(sa2, 1.12, 5.38, 1.85, 0.28, fill_color=PAL["card_slate"], border_color=PAL["slate_accent"], radius=0.15)
    add_text(sa2, 1.18, 5.42, 1.73, 0.22, "H1 2027 · PROTOTYPE", size=8.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
    add_text(sa2, 3.10, 5.36, 3.20, 0.32, "Dream Printer", size=15, bold=True, color=PAL["ink_primary"])
    add_text(sa2, 1.12, 5.80, 5.16, 0.62, "• Press a button upon waking to speak your dream; generates dream art + transcript.\n• Builds a connected dream diary linking recurring themes across prior nights.", size=9.0, bold=False, color=PAL["ink_secondary"], line_spacing=1.35)

    # Right: Voice Adventure Walkie-Talkie
    add_box(sa2, 6.83, 1.72, 5.60, 5.00, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_product_image(sa2, 7.05, 1.92, 5.16, 3.30, "a2_mayday_collage.png", radius=0.03)
    add_box(sa2, 7.05, 5.38, 1.85, 0.28, fill_color=PAL["card_slate"], border_color=PAL["slate_accent"], radius=0.15)
    add_text(sa2, 7.11, 5.42, 1.73, 0.22, "H1 2027 · PROTOTYPE", size=8.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)
    add_text(sa2, 9.03, 5.36, 3.20, 0.32, "Voice Gaming Walkie-Talkie", size=15, bold=True, color=PAL["ink_primary"])
    add_text(sa2, 7.05, 5.80, 5.16, 0.39, "• A character stranded on an alien planet or escape room calls for your help.\n• Calm them down, guide exploration, and solve live incidents by voice.", size=9.0, bold=False, color=PAL["ink_secondary"], line_spacing=1.35)

    # ==========================================================================
    # APPENDIX A3: WAVE 2 SPOTLIGHT — KIDS' E-INK DOODLE PAD
    # ==========================================================================
    sa3 = prs.slides.add_slide(blank)
    add_header(sa3, "Appendix A3 · Wave 2 Product Gallery (H1 2027)", "Prototyping for H1 2027: E-Ink Children’s Story Doodle Pad", "A3 / A3", title_width=11.55)

    # Left: Concise 3-pill summary card
    add_box(sa3, 0.90, 1.72, 4.45, 5.00, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_box(sa3, 1.20, 2.02, 1.95, 0.30, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], radius=0.15)
    add_text(sa3, 1.26, 2.07, 1.83, 0.22, "H1 2027 · PROTOTYPE", size=8.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)

    add_text(sa3, 1.20, 2.50, 3.85, 0.65, "Eye-Friendly E-Ink\nChildren’s Doodle Pad", size=20, bold=True, color=PAL["ink_primary"], line_spacing=1.18)
    add_text(sa3, 1.20, 3.28, 3.85, 0.55, "How kids should experience AI—long before they even know what AI is.", size=11, bold=False, color=PAL["ink_secondary"])

    kids_features = [
        ("Doodle → Comic Story", "Extends any child’s sketch into a back-and-forth comic adventure."),
        ("Visual Q&A", "Answers handwritten or doodled questions in a child-friendly way."),
        ("Calm E-Ink Screen", "Zero blue light or addictive feeds—pure creative agency."),
    ]
    for i, (kf_head, kf_sub) in enumerate(kids_features):
        ky = 4.00 + i * 0.82
        add_box(sa3, 1.20, ky, 3.85, 0.70, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.06)
        add_text(sa3, 1.38, ky + 0.10, 3.50, 0.24, kf_head, size=10.5, bold=True, color=PAL["ink_primary"])
        add_text(sa3, 1.38, ky + 0.35, 3.50, 0.35, kf_sub, size=9.0, bold=False, color=PAL["ink_secondary"])

    # Right: Giant Gallery Image Collage (60%+ of slide width)
    add_box(sa3, 5.60, 1.72, 6.83, 5.00, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_product_image(sa3, 5.85, 1.95, 6.33, 4.54, "a3_doodleboard_collage.png", radius=0.03)

    prs.save(output_path)
    print(f"Saved Pantone Light Deck: {output_path}")


if __name__ == "__main__":
    main_out = os.path.join(OUT_DIR, "Banrai_Seed_Plus_Deck.pptx")
    build_pantone_deck(main_out)
