import os
from pptx import Presentation
from PIL import Image, ImageDraw, ImageFont

PPTX_PATH = "/Users/mklaw/Developer/klaw/Seed Plus Round/Banrai_Seed_Plus_Deck.pptx"
RENDER_DIR = "/tmp/slide_renders"
os.makedirs(RENDER_DIR, exist_ok=True)

FONT_REG = os.path.expanduser("~/Library/Fonts/Poppins-Regular.ttf")
FONT_BOLD = os.path.expanduser("~/Library/Fonts/Poppins-Bold.ttf")

prs = Presentation(PPTX_PATH)
W_IN = prs.slide_width.inches
H_IN = prs.slide_height.inches
DPI = 144  # 144 px per inch -> 1920 x 1080
PPT_WIDTH_SAFETY = 1.12  # PowerPoint renders Poppins ~10-12% wider than raw FreeType


def get_font(pt_size, bold=False):
    px_size = max(10, int(round(pt_size * (DPI / 72.0))))
    return ImageFont.truetype(FONT_BOLD if bold else FONT_REG, px_size)


def wrap_line(text, font, max_px_w):
    if not text:
        return [""]
    words = text.split(" ")
    lines = []
    cur = words[0]
    for w in words[1:]:
        test = cur + " " + w
        bbox = font.getbbox(test)
        tw = (bbox[2] - bbox[0]) * PPT_WIDTH_SAFETY
        if tw <= max_px_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


print("=== FULL PPTX LAYOUT & TEXT AUDIT ===")
for s_idx, slide in enumerate(prs.slides, start=1):
    print(f"\n--- SLIDE {s_idx:02d} ---")
    img = Image.new("RGB", (int(W_IN * DPI), int(H_IN * DPI)), (244, 242, 237))
    draw = ImageDraw.Draw(img)

    text_records = []

    for sh_idx, shape in enumerate(slide.shapes):
        l_in = shape.left.inches
        t_in = shape.top.inches
        w_in = shape.width.inches
        h_in = shape.height.inches

        x0, y0 = int(l_in * DPI), int(t_in * DPI)
        x1, y1 = int((l_in + w_in) * DPI), int((t_in + h_in) * DPI)

        # Draw shape fill/outline if not a pure textbox
        if not shape.has_text_frame or (shape.has_text_frame and shape.text_frame.text.strip() == ""):
            fill_rgb = (251, 250, 247)
            try:
                if shape.fill.type == 1:
                    c = shape.fill.fore_color.rgb
                    fill_rgb = (c[0], c[1], c[2])
            except Exception:
                pass
            line_rgb = None
            try:
                if shape.line and shape.line.fill.type == 1:
                    lc = shape.line.color.rgb
                    line_rgb = (lc[0], lc[1], lc[2])
            except Exception:
                pass
            draw.rounded_rectangle([x0, y0, x1, y1], radius=8, fill=fill_rgb, outline=line_rgb, width=2)

        if shape.has_text_frame and shape.text_frame.text.strip():
            tf = shape.text_frame
            raw_text = tf.text.strip()
            p0 = tf.paragraphs[0]
            pt_size = p0.font.size.pt if p0.font.size else 14
            bold = bool(p0.font.bold)
            font = get_font(pt_size, bold=bold)
            line_sp = p0.line_spacing if p0.line_spacing else 1.2
            color = (35, 38, 42)
            try:
                if p0.font.color and p0.font.color.rgb:
                    rc = p0.font.color.rgb
                    color = (rc[0], rc[1], rc[2])
            except Exception:
                pass

            max_px_w = max(10, x1 - x0)
            all_wrapped = []
            unintended_wraps = []
            for para in tf.paragraphs:
                p_txt = para.text
                w_lines = wrap_line(p_txt, font, max_px_w)
                if len(w_lines) > 1 and len(p_txt) < 42:
                    unintended_wraps.append((p_txt, w_lines))
                all_wrapped.extend(w_lines)

            px_line_h = (pt_size * (DPI / 72.0)) * line_sp
            total_text_h_px = len(all_wrapped) * px_line_h
            actual_h_in = total_text_h_px / DPI

            # Render text on audit image
            cy = y0
            for wl in all_wrapped:
                draw.text((x0, int(cy)), wl, font=font, fill=color)
                cy += px_line_h
            # Draw faint cyan bounding box of actual rendered text
            draw.rectangle([x0, y0, x1, int(y0 + total_text_h_px)], outline=(180, 120, 120), width=1)

            if unintended_wraps:
                for orig, wls in unintended_wraps:
                    print(f"  [WRAP WARNING] '{orig}' (w={w_in:.2f}in, pt={pt_size}) wrapped into {len(wls)} lines: {wls}")

            if actual_h_in > h_in * 1.08:
                print(f"  [HEIGHT OVERFLOW] '{raw_text[:45]}...' needs {actual_h_in:.2f}in height, box is only {h_in:.2f}in (lines={len(all_wrapped)})")

            text_records.append({
                "text": raw_text.replace("\n", " / "),
                "l": l_in,
                "t": t_in,
                "r": l_in + w_in,
                "b_box": t_in + h_in,
                "b_actual": t_in + max(h_in, actual_h_in),
                "pt": pt_size,
                "lines": len(all_wrapped),
            })

    # Check pairwise overlaps between text boxes
    for i in range(len(text_records)):
        for j in range(i + 1, len(text_records)):
            a = text_records[i]
            b = text_records[j]
            # Check horizontal overlap
            h_overlap = min(a["r"], b["r"]) - max(a["l"], b["l"])
            v_overlap = min(a["b_actual"], b["b_actual"]) - max(a["t"], b["t"])
            if h_overlap > 0.08 and v_overlap > 0.04:
                print(f"  [OVERLAP] '{a['text'][:35]}' (t={a['t']:.2f}..{a['b_actual']:.2f}, l={a['l']:.2f}..{a['r']:.2f}) "
                      f"OVERLAPS WITH '{b['text'][:35]}' (t={b['t']:.2f}..{b['b_actual']:.2f}, l={b['l']:.2f}..{b['r']:.2f}) by v={v_overlap:.2f}in")

    out_png = os.path.join(RENDER_DIR, f"slide_{s_idx:02d}.png")
    img.save(out_png)
