import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

OUT_DIR = "/Users/mklaw/Developer/klaw/Seed Plus Round"

# ==============================================================================
# PANTONE-INSPIRED CALM LIGHT PALETTE
# ==============================================================================
PAL = {
    "bg_canvas": RGBColor(244, 242, 237),       # Pantone 11-4201 Cloud Dancer (#F4F2ED)
    "card_white": RGBColor(251, 250, 247),      # Pantone Marshmallow (#FBFAF7)
    "card_stone": RGBColor(236, 233, 225),      # Pantone 12-0104 Warm Sand (#ECE9E1)
    "card_sage": RGBColor(225, 232, 224),       # Pantone Soft Celadon (#E1E8E0)
    "card_slate": RGBColor(224, 231, 236),      # Pantone Pale Mist (#E0E7EC)
    "border_subtle": RGBColor(216, 212, 202),   # Pantone Pumice Stone (#D8D4CA)
    "border_strong": RGBColor(168, 164, 154),   # Pantone Warm Taupe (#A8A49A)
    "ink_primary": RGBColor(35, 38, 42),        # Pantone 19-4007 After Dark (#23262A)
    "ink_secondary": RGBColor(96, 101, 108),    # Pantone 17-4402 Neutral Gray (#60656C)
    "ink_muted": RGBColor(142, 146, 152),       # Pantone Harbor Mist (#8E9298)
    "sage_accent": RGBColor(88, 114, 92),       # Pantone 17-0210 Laurel Oak (#58725C)
    "slate_accent": RGBColor(78, 105, 122),     # Pantone 17-4412 Porcelain Blue (#4E697A)
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


def add_connector_bar(slide, left, top, width, color):
    """Draws a clean horizontal connector bar with a center dot between flow cards."""
    add_box(slide, left, top, width, 0.025, fill_color=color, shape_type=MSO_SHAPE.RECTANGLE)
    dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left + width / 2.0 - 0.045), Inches(top - 0.032), Inches(0.09), Inches(0.09))
    dot.fill.solid()
    dot.fill.fore_color.rgb = color
    dot.line.fill.background()


def add_text(slide, left, top, width, height, text, size=14, bold=False,
             color=PAL["ink_primary"], align=PP_ALIGN.LEFT,
             anchor=MSO_ANCHOR.TOP, line_spacing=1.2, word_wrap=True):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = word_wrap
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
        add_text(slide, left, top, 3.3, 0.95, "Banrai", size=56, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.RIGHT, word_wrap=False)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left + 3.42), Inches(top + 0.45), Inches(0.20), Inches(0.20))
        dot.fill.solid()
        dot.fill.fore_color.rgb = PAL["callout_lime"]
        dot.line.color.rgb = PAL["callout_lime_border"]
        dot.line.width = Pt(1.0)
    else:
        add_text(slide, left, top, 1.1, 0.32, "Banrai", size=14, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.RIGHT, word_wrap=False)
        dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(left + 1.16), Inches(top + 0.11), Inches(0.09), Inches(0.09))
        dot.fill.solid()
        dot.fill.fore_color.rgb = PAL["callout_lime"]
        dot.line.color.rgb = PAL["callout_lime_border"]
        dot.line.width = Pt(0.75)


def add_header(slide, section_label, title, slide_label):
    set_slide_bg(slide, PAL["bg_canvas"])
    add_text(slide, 0.90, 0.50, 7.50, 0.26, section_label.upper(), size=9.5, bold=True, color=PAL["sage_accent"], word_wrap=False)
    add_logo(slide, 11.15, 0.48, hero=False)
    add_text(slide, 11.20, 6.95, 1.23, 0.28, slide_label, size=9, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.RIGHT, word_wrap=False)
    add_text(slide, 0.90, 0.84, 11.53, 0.52, title, size=23, bold=True, color=PAL["ink_primary"], line_spacing=1.1, word_wrap=False)


def add_image_placeholder(slide, left, top, width, height, title, subtitle):
    add_box(slide, left, top, width, height, fill_color=PAL["card_stone"], border_color=PAL["border_strong"], border_pt=1.25, radius=0.04)
    cx = left + width / 2.0
    cy = top + height / 2.0
    add_box(slide, cx - 0.24, cy - 0.54, 0.48, 0.48, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], shape_type=MSO_SHAPE.OVAL)
    add_text(slide, cx - 0.24, cy - 0.54, 0.48, 0.48, "+", size=16, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, word_wrap=False)
    add_text(slide, left + 0.20, cy + 0.08, width - 0.40, 0.30, title, size=10.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(slide, left + 0.20, cy + 0.42, width - 0.40, 0.30, subtitle, size=9.0, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER, word_wrap=False)


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

    add_box(s1, 0.75, 0.65, 11.833, 6.20, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_logo(s1, 4.70, 1.80, hero=True)

    add_text(
        s1, 1.20, 3.10, 10.933, 0.58,
        "Consumer AI Hardware Built for Joy, Not Chores.",
        size=26, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False
    )
    add_text(
        s1, 2.00, 3.76, 9.333, 0.40,
        "Make Humans Talk Again   ·   Seed+ Investor Presentation",
        size=13, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False
    )

    s1_stats = [
        ("100% Hard-Subscription", "SaaS recurring model", PAL["card_stone"], PAL["border_subtle"]),
        ("< 9 Mos  ·  $150K–$200K", "Concept to 1,000 US units", PAL["callout_lime"], PAL["callout_lime_border"]),
        ("6–10 Products / Year", "Powered by 1 shared backend", PAL["card_stone"], PAL["border_subtle"]),
    ]
    for i, (big, sub, bg_c, brd_c) in enumerate(s1_stats):
        x = 1.65 + i * 3.45
        add_box(s1, x, 4.90, 3.15, 1.15, fill_color=bg_c, border_color=brd_c, radius=0.08)
        add_text(s1, x + 0.12, 5.14, 2.91, 0.34, big, size=12.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
        add_text(s1, x + 0.12, 5.52, 2.91, 0.30, sub, size=10.0, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)

    # ==========================================================================
    # SLIDE 2: THE COUNTER-TREND — VISUAL POSITIONING GRAPHIC
    # ==========================================================================
    s2 = prs.slides.add_slide(blank)
    add_header(s2, "01 · Category Positioning", "Everyone Builds Functional AI. We Build Fun AI.", "02 / 07")

    # Left: Visual 2x2 Positioning Matrix Graphic
    add_box(s2, 0.90, 1.60, 6.80, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_text(s2, 1.20, 1.80, 3.50, 0.26, "CONSUMER AI LANDSCAPE", size=9.0, bold=True, color=PAL["ink_muted"], word_wrap=False)

    # Top & Bottom Axis Pills (using pure Poppins-safe text)
    add_text(s2, 3.10, 2.12, 2.40, 0.26, "TACTILE HARDWARE", size=9.0, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(s2, 3.10, 6.26, 2.40, 0.26, "SCREEN CHATBOTS", size=9.0, bold=True, color=PAL["ink_muted"], align=PP_ALIGN.CENTER, word_wrap=False)

    # Crosshair Lines (center at x=4.30, y=4.30)
    add_box(s2, 1.35, 4.30, 5.90, 0.02, fill_color=PAL["border_strong"], shape_type=MSO_SHAPE.RECTANGLE)
    add_box(s2, 4.30, 2.44, 0.02, 3.74, fill_color=PAL["border_strong"], shape_type=MSO_SHAPE.RECTANGLE)

    # Left/Right Axis Labels
    add_text(s2, 1.35, 4.02, 1.90, 0.24, "WORK & TASKS", size=8.5, bold=True, color=PAL["ink_muted"], word_wrap=False)
    add_text(s2, 5.35, 4.02, 1.90, 0.24, "PLAY & DAILY JOY", size=8.5, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.RIGHT, word_wrap=False)

    # Top-Left Quadrant: Utility Wearables
    add_box(s2, 1.40, 2.58, 2.60, 1.32, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.08)
    add_text(s2, 1.52, 2.82, 2.36, 0.30, "Utility Wearables", size=11.0, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(s2, 1.52, 3.18, 2.36, 0.30, "Phone replacement pins", size=9.5, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER, word_wrap=False)

    # Top-Right Quadrant: BANRAI (Single Bright Lime Hero Callout)
    add_box(s2, 4.55, 2.58, 2.70, 1.32, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], border_pt=1.5, radius=0.08)
    add_text(s2, 4.67, 2.76, 2.46, 0.32, "Banrai · “Fun AI”", size=12.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(s2, 4.67, 3.12, 2.46, 0.56, "Delightfully “useless” hardware\nfor daily joy & conversation", size=9.5, bold=False, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)

    # Bottom-Left Quadrant: Functional AI Crowd
    add_box(s2, 1.40, 4.68, 2.60, 1.32, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.08)
    add_text(s2, 1.52, 4.86, 2.36, 0.30, "Functional AI Crowd", size=11.0, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(s2, 1.52, 5.20, 2.36, 0.56, "Emails, coding, productivity\n(99% of VC & Big Tech)", size=9.5, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER)

    # Bottom-Right Quadrant: Screen Entertainment
    add_box(s2, 4.55, 4.68, 2.70, 1.32, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.08)
    add_text(s2, 4.67, 4.92, 2.46, 0.30, "Screen Companions", size=11.0, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(s2, 4.67, 5.26, 2.46, 0.30, "Phone-bound chat apps", size=9.5, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER, word_wrap=False)

    # Right Column: 3 Crisp Essence Cards
    essence_cards = [
        ("01 · Counter-Trend", "Delightfully “Useless”", "Zero task optimization. Built purely for curiosity, laughter, and warmth.", PAL["card_white"]),
        ("02 · Unifying Theme", "“Make Humans Talk Again”", "Replaces passive screen scrolling with active voice, stories, and imagination.", PAL["card_sage"]),
        ("03 · Multi-Brand Strategy", "Ambient in Every Room", "Different brands & form factors—from bedside clocks to living room frames.", PAL["card_white"]),
    ]
    for i, (tag, head, desc, bg_c) in enumerate(essence_cards):
        y = 1.60 + i * 1.75
        add_box(s2, 8.00, y, 4.43, 1.60, fill_color=bg_c, border_color=PAL["border_subtle"], radius=0.05)
        add_text(s2, 8.28, y + 0.20, 3.88, 0.24, tag.upper(), size=9.0, bold=True, color=PAL["sage_accent"], word_wrap=False)
        add_text(s2, 8.28, y + 0.48, 3.88, 0.34, head, size=14.0, bold=True, color=PAL["ink_primary"], word_wrap=False)
        add_text(s2, 8.28, y + 0.88, 3.88, 0.56, desc, size=10.0, bold=False, color=PAL["ink_secondary"])

    # ==========================================================================
    # SLIDE 3: BUSINESS MODEL — VISUAL REVENUE & LIFECYCLE DIAGRAM
    # ==========================================================================
    s3 = prs.slides.add_slide(blank)
    add_header(s3, "02 · Business Model", "Hardware Is the Vessel. SaaS Is the Engine.", "03 / 07")

    # Top: Traditional Hardware
    add_box(s3, 0.90, 1.65, 11.53, 2.05, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.04)
    add_text(s3, 1.25, 1.90, 3.25, 0.26, "TRADITIONAL HARDWARE", size=9.0, bold=True, color=PAL["ink_muted"], word_wrap=False)
    add_text(s3, 1.25, 2.20, 3.25, 0.36, "One-Time Unit Margin", size=15.5, bold=True, color=PAL["ink_secondary"], word_wrap=False)
    add_text(s3, 1.25, 2.64, 3.25, 0.72, "Profit stops at checkout.\nForced to push Gen-2 upgrades.", size=10.0, bold=False, color=PAL["ink_muted"])

    trad_steps = [
        ("Day 1: Sell Box", "One-off unit margin"),
        ("Month 2–12", "$0 recurring revenue"),
        ("Year 2+", "Push Gen-2 upgrade"),
    ]
    for i, (t_head, t_sub) in enumerate(trad_steps):
        tx = 4.70 + i * 2.52
        add_box(s3, tx, 2.02, 2.26, 1.30, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.06)
        add_text(s3, tx + 0.10, 2.32, 2.06, 0.30, t_head, size=11.0, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)
        add_text(s3, tx + 0.10, 2.70, 2.06, 0.30, t_sub, size=9.5, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER, word_wrap=False)
        if i < 2:
            add_connector_bar(s3, tx + 2.26, 2.66, 0.26, PAL["border_strong"])

    # Bottom: Banrai Hard-Subscription Model
    add_box(s3, 0.90, 3.95, 11.53, 2.75, fill_color=PAL["card_white"], border_color=PAL["sage_accent"], border_pt=1.5, radius=0.04)
    add_text(s3, 1.25, 4.25, 3.25, 0.26, "THE BANRAI MODEL", size=9.0, bold=True, color=PAL["sage_accent"], word_wrap=False)
    add_text(s3, 1.25, 4.55, 3.25, 0.38, "100% Hard-Subscription", size=15.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_text(s3, 1.25, 5.02, 3.25, 1.25, "Real AI costs tokens—so there is no free tier. Hardware unlocks SaaS-style recurring revenue.", size=10.0, bold=False, color=PAL["ink_secondary"])

    banrai_steps = [
        ("01 · Unbox", "Hardware + Free Trial", "Bundled free trial months\nfor instant unboxing magic", PAL["card_sage"], PAL["border_subtle"]),
        ("02 · Subscribe", "Monthly Subscription", "Mandatory monthly fee\nkeeps companion alive", PAL["callout_lime"], PAL["callout_lime_border"]),
        ("03 · Compound", "Continuous SaaS LTV", "Cloud evolves stories\nfor long-term retention", PAL["card_sage"], PAL["border_subtle"]),
    ]
    for i, (b_tag, b_head, b_sub, bg_c, brd_c) in enumerate(banrai_steps):
        bx = 4.70 + i * 2.52
        add_box(s3, bx, 4.25, 2.26, 2.15, fill_color=bg_c, border_color=brd_c, border_pt=1.25, radius=0.06)
        add_text(s3, bx + 0.10, 4.48, 2.06, 0.24, b_tag.upper(), size=8.5, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)
        add_text(s3, bx + 0.10, 4.80, 2.06, 0.32, b_head, size=11.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
        add_text(s3, bx + 0.10, 5.24, 2.06, 0.70, b_sub, size=9.0, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)
        if i < 2:
            add_connector_bar(s3, bx + 2.26, 5.31, 0.26, PAL["sage_accent"])

    # ==========================================================================
    # SLIDE 4: UNFAIR ADVANTAGE — HUB & SPOKE ARCHITECTURE + COST GRAPHIC
    # ==========================================================================
    s4 = prs.slides.add_slide(blank)
    add_header(s4, "03 · Unfair Advantage", "One Shared Backend Powers Dozens of Hardware Products.", "04 / 07")

    # LEFT SIDE: Visual Hub-and-Spoke Diagram
    add_box(s4, 0.90, 1.60, 6.75, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_text(s4, 1.20, 1.82, 5.80, 0.26, "REUSABLE PLATFORM ARCHITECTURE", size=9.0, bold=True, color=PAL["sage_accent"], word_wrap=False)

    # Central Hub Box
    add_box(s4, 1.20, 2.48, 2.40, 3.65, fill_color=PAL["card_sage"], border_color=PAL["sage_accent"], border_pt=1.5, radius=0.05)
    add_text(s4, 1.32, 2.72, 2.16, 0.26, "SHARED CORE", size=8.5, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(s4, 1.32, 3.04, 2.16, 0.65, "1 Unified AI +\nBilling Backend", size=13.5, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER)

    hub_pills = ["Conversational Voice OS", "Image & Story Engine", "Subscription & Metering"]
    for i, hp in enumerate(hub_pills):
        hy = 3.92 + i * 0.62
        add_box(s4, 1.34, hy, 2.12, 0.46, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.08)
        add_text(s4, 1.38, hy + 0.11, 2.04, 0.24, hp, size=8.5, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)

    # Connector lines + 6 Spoke Product Nodes
    spokes = [
        ("01 · Living Photo Frame", "Dec 2026"),
        ("02 · Pocket Bible", "Dec 2026"),
        ("03 · Dream Printer", "H1 2027"),
        ("04 · Voice Walkie-Talkie", "H1 2027"),
        ("05 · Kids’ Doodle Pad", "H1 2027"),
        ("06–10+ · New SKUs / Yr", "Pipeline"),
    ]
    for i, (s_name, s_date) in enumerate(spokes):
        sy = 2.32 + i * 0.68
        add_connector_bar(s4, 3.60, sy + 0.25, 0.55, PAL["sage_accent"])
        node_bg = PAL["card_stone"] if i < 5 else PAL["card_slate"]
        add_box(s4, 4.15, sy, 3.20, 0.52, fill_color=node_bg, border_color=PAL["border_subtle"], radius=0.08)
        add_text(s4, 4.30, sy + 0.14, 2.15, 0.26, s_name, size=9.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
        add_text(s4, 6.50, sy + 0.15, 0.72, 0.24, s_date, size=8.5, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.RIGHT, word_wrap=False)

    # RIGHT SIDE: Visual Cost & Speed Comparison Bars
    add_box(s4, 7.90, 1.60, 4.53, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_text(s4, 8.20, 1.82, 4.00, 0.26, "ECONOMICS PER HARDWARE LINE (US)", size=9.0, bold=True, color=PAL["ink_muted"], word_wrap=False)

    # Comparison 1: Time to Market
    add_text(s4, 8.20, 2.26, 3.95, 0.28, "Time to Market (First 1,000 US Units)", size=10.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_box(s4, 8.20, 2.60, 3.90, 0.36, fill_color=PAL["card_stone"], radius=0.1)
    add_text(s4, 8.34, 2.66, 3.60, 0.24, "Traditional Hardware:  18 – 24+ Months", size=9.0, bold=False, color=PAL["ink_secondary"], word_wrap=False)
    add_box(s4, 8.20, 3.04, 2.05, 0.38, fill_color=PAL["card_sage"], border_color=PAL["sage_accent"], radius=0.1)
    add_text(s4, 8.34, 3.11, 1.80, 0.24, "Banrai: < 9 Mos", size=9.5, bold=True, color=PAL["ink_primary"], word_wrap=False)

    # Comparison 2: All-In Launch Cost (BRIGHT LIME HERO CALLOUT)
    add_text(s4, 8.20, 3.68, 3.95, 0.28, "All-In Launch Cost (R&D + First 1,000 Units)", size=10.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_box(s4, 8.20, 4.02, 3.90, 0.36, fill_color=PAL["card_stone"], radius=0.1)
    add_text(s4, 8.34, 4.08, 3.60, 0.24, "Traditional Hardware:  $3M – $10M+", size=9.0, bold=False, color=PAL["ink_secondary"], word_wrap=False)
    add_box(s4, 8.20, 4.46, 2.50, 0.40, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], border_pt=1.5, radius=0.1)
    add_text(s4, 8.34, 4.54, 2.25, 0.26, "Banrai: $150K – $200K", size=10.0, bold=True, color=PAL["ink_primary"], word_wrap=False)

    # Comparison 3: Unit Threshold
    add_text(s4, 8.20, 5.14, 3.95, 0.28, "Unit Threshold for a Winner", size=10.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_box(s4, 8.20, 5.48, 3.90, 0.92, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.06)
    add_text(
        s4, 8.36, 5.62, 3.60, 0.65,
        "• Single-Product Co: Must sell 10M+ units\n• Banrai Portfolio: Profitable hit at 100K+ units",
        size=9.5, bold=True, color=PAL["ink_primary"], line_spacing=1.35, word_wrap=False
    )

    # ==========================================================================
    # SLIDE 5: PRODUCT PORTFOLIO & ROADMAP AT A GLANCE
    # ==========================================================================
    s5 = prs.slides.add_slide(blank)
    add_header(s5, "04 · Product Roadmap (US Market Exclusively)", "5 Products in Motion. 6–10 New Launches Every Year.", "05 / 07")

    # Timeline Header Bar (Single Bright Lime Hero Callout on Wave 1 Header)
    add_box(s5, 0.90, 1.60, 4.52, 0.42, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], radius=0.08)
    add_text(s5, 1.00, 1.69, 4.32, 0.26, "WAVE 1 · DEC 2026 (1,000 US UNITS EACH · ON BUDGET)", size=9.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)

    add_box(s5, 5.58, 1.60, 6.85, 0.42, fill_color=PAL["card_sage"], border_color=PAL["sage_accent"], radius=0.08)
    add_text(s5, 5.70, 1.69, 6.60, 0.26, "WAVE 2 · H1 2027 (CURRENTLY IN PROTOTYPING)", size=9.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)

    products_overview = [
        ("01", "Magical Living\nPhoto Frame", "Dec 2026", "Portraits wave hello & react to live local weather.", PAL["card_white"], PAL["border_strong"]),
        ("02", "Pocket\nBible", "Dec 2026", "Standalone E-Ink + 4G daily Christian companion.", PAL["card_white"], PAL["border_strong"]),
        ("03", "Dream\nPrinter", "H1 2027", "One-button morning dream art & connected diary.", PAL["card_white"], PAL["border_subtle"]),
        ("04", "Voice Gaming\nWalkie-Talkie", "H1 2027", "Co-op voice rescue with a stranded character.", PAL["card_white"], PAL["border_subtle"]),
        ("05", "Kids’ E-Ink\nDoodle Pad", "H1 2027", "Turns children’s sketches into interactive comics.", PAL["card_white"], PAL["border_subtle"]),
    ]
    for i, (num, p_name, p_date, p_hook, bg_c, brd_c) in enumerate(products_overview):
        px = 0.90 + i * 2.34
        add_box(s5, px, 2.18, 2.18, 3.55, fill_color=bg_c, border_color=brd_c, border_pt=1.0, radius=0.04)
        add_box(s5, px + 0.16, 2.34, 1.86, 1.30, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.06)
        add_text(s5, px + 0.20, 2.86, 1.78, 0.30, f"[ Photo {num} ]", size=9.5, bold=False, color=PAL["ink_muted"], align=PP_ALIGN.CENTER, word_wrap=False)
        add_text(s5, px + 0.18, 3.80, 1.82, 0.24, p_date.upper(), size=8.5, bold=True, color=PAL["sage_accent"], word_wrap=False)
        add_text(s5, px + 0.18, 4.06, 1.82, 0.62, p_name, size=12.0, bold=True, color=PAL["ink_primary"], line_spacing=1.15, word_wrap=False)
        add_text(s5, px + 0.18, 4.78, 1.82, 0.80, p_hook, size=9.5, bold=False, color=PAL["ink_secondary"], line_spacing=1.25)

    add_box(s5, 0.90, 5.92, 11.53, 0.72, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.05)
    add_text(
        s5, 1.20, 6.15, 6.40, 0.30,
        "Deep Backlog:  Launching 6–10 new Fun AI hardware products every year.",
        size=10.5, bold=True, color=PAL["ink_primary"], word_wrap=False
    )
    add_text(
        s5, 7.75, 6.15, 4.40, 0.30,
        "See Appendix (A1–A3) for full product visuals  >",
        size=10.0, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.RIGHT, word_wrap=False
    )

    # ==========================================================================
    # SLIDE 6: THE DATA MOAT — VISUAL FLYWHEEL DIAGRAM
    # ==========================================================================
    s6 = prs.slides.add_slide(blank)
    add_header(s6, "05 · Defensibility & Moat", "Capturing the Data That Doesn’t Exist on the Internet.", "06 / 07")

    # Top Contrast Strip
    add_box(s6, 0.90, 1.60, 5.60, 1.32, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.04)
    add_text(s6, 1.20, 1.80, 5.00, 0.24, "PUBLIC INTERNET DATA", size=9.0, bold=True, color=PAL["ink_muted"], word_wrap=False)
    add_text(s6, 1.20, 2.10, 5.00, 0.62, "Teaches AI how to work, code, and summarize.\nEvery competitor scrapes the exact same web.", size=10.5, bold=False, color=PAL["ink_secondary"], word_wrap=False)

    add_box(s6, 6.83, 1.60, 5.60, 1.32, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], border_pt=1.5, radius=0.04)
    add_text(s6, 7.13, 1.80, 5.00, 0.24, "BANRAI PROPRIETARY DATA", size=9.0, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_text(s6, 7.13, 2.10, 5.00, 0.62, "Captures how humans play, laugh, and wonder.\nZero public dataset exists—it must be earned live.", size=10.5, bold=True, color=PAL["ink_primary"], word_wrap=False)

    # Bottom Visual 4-Node Flywheel Diagram
    fly_nodes = [
        ("01 · Ship", "6–10 Products / Yr", "Ambient devices\nacross daily life", PAL["card_white"]),
        ("02 · Spark", "Spontaneous Play", "Users talk for joy,\nnot chores", PAL["card_sage"]),
        ("03 · Collect", "Exclusive Joy Data", "Un-scrapable\nemotional signals", PAL["card_white"]),
        ("04 · Evolve", "Smarter “Fun AI”", "Compounds retention\nacross all SKUs", PAL["card_sage"]),
    ]
    for i, (f_step, f_head, f_sub, bg_c) in enumerate(fly_nodes):
        fx = 0.90 + i * 2.98
        add_box(s6, fx, 3.30, 2.60, 2.55, fill_color=bg_c, border_color=PAL["border_strong"], radius=0.05)
        add_text(s6, fx + 0.15, 3.62, 2.30, 0.26, f_step.upper(), size=9.0, bold=True, color=PAL["sage_accent"], align=PP_ALIGN.CENTER, word_wrap=False)
        add_text(s6, fx + 0.12, 4.02, 2.36, 0.36, f_head, size=13.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
        add_text(s6, fx + 0.15, 4.55, 2.30, 0.75, f_sub, size=10.0, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)
        if i < 3:
            add_connector_bar(s6, fx + 2.60, 4.56, 0.38, PAL["sage_accent"])

    add_box(s6, 1.80, 6.08, 9.73, 0.48, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.08)
    add_text(s6, 2.00, 6.20, 9.33, 0.28, "CONTINUOUS COMPOUNDING FLYWHEEL ACROSS EVERY BRAND & HARDWARE LINE", size=9.5, bold=True, color=PAL["ink_secondary"], align=PP_ALIGN.CENTER, word_wrap=False)

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
        add_box(s7, px, 1.70, 3.65, 3.15, fill_color=bg_c, border_color=brd_c, border_pt=1.25, radius=0.04)
        add_text(s7, px + 0.20, 2.05, 3.25, 0.26, p_tag.upper(), size=9.0, bold=True, color=PAL["ink_secondary"], word_wrap=False)
        add_text(s7, px + 0.20, 2.45, 3.25, 0.38, p_head, size=13.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
        add_text(s7, px + 0.20, 3.05, 3.25, 1.30, p_desc, size=10.5, bold=False, color=PAL["ink_secondary"], line_spacing=1.35)

    # Calm Footer Callout Card
    add_box(s7, 0.90, 5.15, 11.53, 1.45, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.04)
    add_logo(s7, 1.20, 5.50, hero=False)
    add_text(s7, 1.30, 5.92, 4.50, 0.35, "Make Humans Talk Again.", size=13.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_text(s7, 6.20, 5.54, 5.85, 0.72, "banrai.ai   ·   hello@banrai.ai\nSeed+ Investor Presentation  ·  Product Appendix Follows  >", size=11.0, bold=False, color=PAL["ink_secondary"], align=PP_ALIGN.RIGHT, line_spacing=1.4, word_wrap=False)

    # ==========================================================================
    # APPENDIX A1: WAVE 1 PRODUCTS (DEC 2026) — GALLERY VIEW
    # ==========================================================================
    sa1 = prs.slides.add_slide(blank)
    add_header(sa1, "Appendix A1 · Wave 1 Product Gallery (Dec 2026)", "Shipping Dec 2026: 1,000 US Units Each (On Budget)", "A1 / A3")

    # Left: Magical Living Photo Frame
    add_box(sa1, 0.90, 1.60, 5.60, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_image_placeholder(sa1, 1.12, 1.80, 5.16, 3.20, "[ Drop Product Photo · Magical Living Photo Frame ]", "16:10 frame for hardware + animated portrait preview")
    add_box(sa1, 1.12, 5.18, 1.72, 0.28, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], radius=0.15)
    add_text(sa1, 1.16, 5.23, 1.64, 0.20, "DEC 2026 · 1K UNITS", size=8.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(sa1, 2.96, 5.16, 3.32, 0.32, "Magical Living Photo Frame", size=13.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_text(sa1, 1.12, 5.62, 5.16, 0.90, "• Harry Potter-style portraits that wave hello as you walk by.\n• Syncs with live local weather (opens an umbrella when it rains).", size=9.5, bold=False, color=PAL["ink_secondary"], line_spacing=1.35, word_wrap=False)

    # Right: Pocket Interactive Bible
    add_box(sa1, 6.83, 1.60, 5.60, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_image_placeholder(sa1, 7.05, 1.80, 5.16, 3.20, "[ Drop Product Photo · Pocket Interactive Bible ]", "16:10 frame for standalone E-Ink + 4G hardware")
    add_box(sa1, 7.05, 5.18, 1.72, 0.28, fill_color=PAL["card_sage"], border_color=PAL["sage_accent"], radius=0.15)
    add_text(sa1, 7.09, 5.23, 1.64, 0.20, "DEC 2026 · 1K UNITS", size=8.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(sa1, 8.89, 5.16, 3.32, 0.32, "Pocket Interactive Bible", size=13.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_text(sa1, 7.05, 5.62, 5.16, 0.90, "• Standalone E-Ink + 4G device for focused, distraction-free faith.\n• Warm Christian companion that deepens Scripture via daily talk.", size=9.5, bold=False, color=PAL["ink_secondary"], line_spacing=1.35, word_wrap=False)

    # ==========================================================================
    # APPENDIX A2: WAVE 2 PRODUCTS (H1 2027 PROTOTYPING) — GALLERY VIEW
    # ==========================================================================
    sa2 = prs.slides.add_slide(blank)
    add_header(sa2, "Appendix A2 · Wave 2 Product Gallery (H1 2027)", "Prototyping for H1 2027: Morning Rituals & Voice Gaming", "A2 / A3")

    # Left: Dream Printer
    add_box(sa2, 0.90, 1.60, 5.60, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_image_placeholder(sa2, 1.12, 1.80, 5.16, 3.20, "[ Drop Product Photo · Dream Printer ]", "Bedside alarm-clock hardware + visual dream diary UI")
    add_box(sa2, 1.12, 5.18, 1.80, 0.28, fill_color=PAL["card_slate"], border_color=PAL["slate_accent"], radius=0.15)
    add_text(sa2, 1.16, 5.23, 1.72, 0.20, "H1 2027 · PROTOTYPE", size=8.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(sa2, 3.04, 5.16, 3.24, 0.32, "Dream Printer", size=13.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_text(sa2, 1.12, 5.62, 5.16, 0.90, "• Press a button upon waking to record & illustrate your dream.\n• Builds a connected dream diary linking themes across prior nights.", size=9.5, bold=False, color=PAL["ink_secondary"], line_spacing=1.35, word_wrap=False)

    # Right: Voice Adventure Walkie-Talkie
    add_box(sa2, 6.83, 1.60, 5.60, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_image_placeholder(sa2, 7.05, 1.80, 5.16, 3.20, "[ Drop Product Photo · Voice Walkie-Talkie ]", "Tactile walkie-talkie gaming hardware")
    add_box(sa2, 7.05, 5.18, 1.80, 0.28, fill_color=PAL["card_slate"], border_color=PAL["slate_accent"], radius=0.15)
    add_text(sa2, 7.09, 5.23, 1.72, 0.20, "H1 2027 · PROTOTYPE", size=8.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)
    add_text(sa2, 8.97, 5.16, 3.24, 0.32, "Voice Gaming Walkie-Talkie", size=13.0, bold=True, color=PAL["ink_primary"], word_wrap=False)
    add_text(sa2, 7.05, 5.62, 5.16, 0.90, "• A character stranded on an alien planet or escape room calls you.\n• Calm them down, guide exploration, and solve live incidents by voice.", size=9.5, bold=False, color=PAL["ink_secondary"], line_spacing=1.35, word_wrap=False)

    # ==========================================================================
    # APPENDIX A3: WAVE 2 SPOTLIGHT — KIDS' E-INK DOODLE PAD
    # ==========================================================================
    sa3 = prs.slides.add_slide(blank)
    add_header(sa3, "Appendix A3 · Wave 2 Product Gallery (H1 2027)", "Prototyping for H1 2027: E-Ink Children’s Story Doodle Pad", "A3 / A3")

    # Left: Concise 3-pill summary card
    add_box(sa3, 0.90, 1.60, 4.55, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_box(sa3, 1.20, 1.88, 1.90, 0.28, fill_color=PAL["callout_lime"], border_color=PAL["callout_lime_border"], radius=0.15)
    add_text(sa3, 1.24, 1.93, 1.82, 0.20, "H1 2027 · PROTOTYPE", size=8.0, bold=True, color=PAL["ink_primary"], align=PP_ALIGN.CENTER, word_wrap=False)

    add_text(sa3, 1.20, 2.34, 3.95, 0.68, "Eye-Friendly E-Ink\nChildren’s Doodle Pad", size=18.0, bold=True, color=PAL["ink_primary"], line_spacing=1.18, word_wrap=False)
    add_text(sa3, 1.20, 3.12, 3.95, 0.52, "How kids should experience AI—long before they even know what AI is.", size=10.0, bold=False, color=PAL["ink_secondary"])

    kids_features = [
        ("01 · Sketch to Comic Story", "Extends any sketch into a comic story."),
        ("02 · Visual Curiosity Q&A", "Answers doodled or written questions."),
        ("03 · Calm E-Ink Screen", "Zero blue light or addictive feeds."),
    ]
    for i, (kf_head, kf_sub) in enumerate(kids_features):
        ky = 3.82 + i * 0.86
        add_box(sa3, 1.20, ky, 3.95, 0.72, fill_color=PAL["card_stone"], border_color=PAL["border_subtle"], radius=0.06)
        add_text(sa3, 1.38, ky + 0.12, 3.60, 0.24, kf_head, size=10.5, bold=True, color=PAL["ink_primary"], word_wrap=False)
        add_text(sa3, 1.38, ky + 0.38, 3.60, 0.24, kf_sub, size=9.5, bold=False, color=PAL["ink_secondary"], word_wrap=False)

    # Right: Giant Gallery Image Placeholder
    add_box(sa3, 5.70, 1.60, 6.73, 5.10, fill_color=PAL["card_white"], border_color=PAL["border_subtle"], radius=0.03)
    add_image_placeholder(sa3, 5.92, 1.82, 6.29, 4.66, "[ Hero Product Photo · E-Ink Children’s Story Doodle Pad ]", "Drop large hardware photo + child sketch-to-comic sequence here")

    prs.save(output_path)
    print(f"Saved Audited Pantone Light Deck: {output_path}")


if __name__ == "__main__":
    main_out = os.path.join(OUT_DIR, "Banrai_Seed_Plus_Deck.pptx")
    build_pantone_deck(main_out)
