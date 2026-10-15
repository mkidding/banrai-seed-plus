# Banrai Seed+ Deck — Strategy, Narrative Arc & Design Rationale (v2 · Pantone Edition)

> **Purpose of this Document:** Captures the strategic thinking, investor narrative architecture, and visual design decisions used to transform the founder's brain dump into a crisp **7-slide core investor deck + 3-slide visual Product Appendix**.

---

## 1. Key Evolution in v2 (Addressing Founder Feedback)

1. **Pantone-Inspired Calm Light Theme (Easy on the Eyes)**
   - Replaced the dark/high-contrast neon theme with a warm, tactile **Pantone-inspired editorial palette**:
     - **Canvas:** *Pantone 11-4201 Cloud Dancer* (`#F4F2ED`) — warm alabaster paper that eliminates eye strain.
     - **Cards & Surfaces:** *Pantone Marshmallow* (`#FBFAF7`), *Pantone 12-0104 Warm Sand* (`#ECE9E1`), *Pantone Soft Celadon* (`#E1E8E0`), and *Pantone Pale Mist* (`#E0E7EC`).
     - **Typography Ink:** *Pantone 19-4007 After Dark* (`#23262A`) and *Pantone 17-4402 Neutral Gray* (`#60656C`).
   - **Disciplined Accent Usage:** Bright Banrai Lime (`#CAFB5B`) is **strictly reserved for a single high-conviction callout per slide** (plus the signature dot in the `Banrai.` logo).

2. **Visual Graphics Over Text Walls**
   - Cut word count per slide by **~55%**, replacing multi-sentence bullet lists with **four custom vector diagrams**:
     - **Slide 2 (2×2 Category Matrix Graphic):** Plots *Work & Tasks $\leftrightarrow$ Play & Daily Joy* against *Screen Chatbots $\leftrightarrow$ Tactile Hardware*, visually isolating **Banrai · "Fun AI"** in the open top-right quadrant.
     - **Slide 3 (Revenue Lifecycle Flow Graphic):** Visually contrasts Traditional Hardware's dead-end one-off margin (`Day 1 Sale → $0 Recurring → Push Gen-2`) with Banrai's **100% Hard-Subscription SaaS Flow** (`Unbox w/ Bundled Trial → Mandatory Monthly Fee → Continuous Cloud LTV`).
     - **Slide 4 (Hub-and-Spoke Shared Backend + Cost Comparison Bars):** Visually demonstrates how **1 Unified AI + Billing Backend** powers **dozens of hardware lines** (`01` through `06–10+/yr`), paired with horizontal bar charts comparing Traditional Hardware (`18–24+ mos`, `$3M–$10M+`, needs `10M+ units`) vs. Banrai (`< 9 mos`, **`$150K–$200K`**, wins at `100K+ units`).
     - **Slide 6 (4-Step Data Flywheel Graphic):** Shows the compounding loop (`Ship 6–10/yr → Spark Play → Collect Un-Scrapable Joy Data → Evolve Smarter Fun AI`).

3. **Core Pitch (Slides 01–07) Separated from Product Gallery Appendix (Slides A1–A3)**
   - Instead of spending nearly half the main deck on product descriptions, **Slide 5** now presents a crisp **5-Column Product Roadmap at a Glance** (*Wave 1 Dec 2026 + Wave 2 H1 2027 + 6–10/yr backlog*).
   - All detailed product descriptions and oversized product photo drop-zones now live in a dedicated **3-slide Product Appendix (`A1`–`A3`)**, giving both the main strategic narrative and the product photography room to breathe.

---

## 2. Slide-by-Slide Architecture (7 Core + 3 Appendix)

### Main Deck (01 – 07)
| Slide | Title | Visual Graphic / Hero Callout |
| :--- | :--- | :--- |
| **01** | **Banrai — Consumer AI Hardware Built for Joy, Not Chores** | Minimal architectural frame + 3 stat pills (Lime callout on **`< 9 Mos · $150K–$200K Each`**). |
| **02** | **Everyone Builds Functional AI. We Build Fun AI.** | **2×2 Positioning Matrix** + 3 crisp essence cards (*Delightfully "Useless"*, *"Make Humans Talk Again"*, *Ambient in Every Room*). |
| **03** | **Hardware Is the Vessel. SaaS Is the Engine.** | **Dual Lifecycle Flow Diagram** contrasting one-off hardware sales vs. Banrai's hard monthly subscription (Lime callout on **Mandatory Monthly Fee**). |
| **04** | **One Shared Backend Powers Dozens of Hardware Products.** | **Hub-and-Spoke Platform Diagram** (left) + **Time/Cost Comparison Bars** (right, Lime callout on **`Banrai: $150K – $200K`**). |
| **05** | **5 Products in Motion. 6–10 New Launches Every Year.** | **5-Column Visual Roadmap** with curated hardware thumbnails grouping Wave 1 (Dec 2026, 1K US units each, Lime header) and Wave 2 (H1 2027 Prototyping). |
| **06** | **Capturing the Data That Doesn't Exist on the Internet.** | **Public Web vs. Banrai Data Contrast** (Lime callout) + **4-Node Compounding Flywheel Diagram**. |
| **07** | **Delightfully "Useless." Commercially Unstoppable.** | **3 Executive Summary Pillars** + clean aligned footer (`Make Humans Talk Again.` / `Appendix Follows →`). |

### Product Gallery Appendix (A1 – A3)
| Slide | Title | Focus & Image Layout |
| :--- | :--- | :--- |
| **A1** | **Shipping Dec 2026: 1,000 US Units Each (On Budget)** | Symmetrical 3-card bento hardware collages + 2 concise lines each for **Magical Living Photo Frame (Furemu)** & **Pocket Interactive Bible (Versicle)**. |
| **A2** | **Prototyping for H1 2027: Morning Rituals & Voice Gaming** | Side-by-side hardware + UI collages + 2 single-line bullets each for **Dream Printer** & **Voice Gaming Walkie-Talkie (Mayday)**. |
| **A3** | **Prototyping for H1 2027: E-Ink Children's Story Doodle Pad** | Hero spotlight collage (60%+ width combining physical E-Ink hardware render, child's raw sketch, and 4-panel AI comic story) + 3 concise feature pills. |

---

## 3. Product Media Curation, Color Grading & Alignment Pipeline (v3)

### Automated Studio Processing (`build_product_visuals.py`)
Raw hardware photos and UI screenshots in `product_photos/` are automatically curated, color-graded (cooling indoor warm/yellow casts, lifting E-Ink paper whites, normalizing saturation), and composited onto Pantone Warm Sand (`#ECE9E1`) and Marshmallow (`#FBFAF7`) studio cards in `product_photos/processed/`:

1. **01 · Magical Living Photo Frame (`photoframe_1.jpg` – `photoframe_3.jpg`)**
   - `s5_01_photoframe.png` (`1100×800`): 2-angle portrait framing preserving the full brushed gold bezel.
   - `a1_photoframe_collage.png` (`1564×1000`): 3-card bento collage combining the live weather-synced front portrait (`photoframe_1.jpg`), gold bezel profile (`photoframe_2.jpg`), and kickstand + Furemu backplate (`photoframe_3.jpg`).
2. **02 · Pocket Interactive Bible (`pocketbible_1.jpg` – `pocketbible_2.jpg`)**
   - `s5_02_bible.png` (`1100×800`): Hero hardware shot of the Versicle E-Ink Scripture display (`Psalm 56:3` + `"Hold to talk"`).
   - `a1_bible_preview.png` (`1564×1000`): Symmetrical 3-card bento collage showing the full standalone E-Ink + 4G device (`pocketbible_1.jpg`) on the left, the gold & matte glass `VERSICLE` backplate + tactile talk buttons (`pocketbible_2.jpg`) on the top-right, and a macro Scripture screen detail on the bottom-right.
3. **03 · Dream Printer (`dreamprinter_1.jpg` & `dreamprinter_2.png`)**
   - `s5_03_dreamprinter.png` (`1100×800`): Hero hardware shot of the bedside cube + thermal dream slip.
   - `a2_dreamprinter_collage.png` (`1564×1000`): Combines the physical bedside hardware (`dreamprinter_1.jpg`) on the left with the `320×240` thermal sketch and `1344×1008` cloud dream diary art (`dreamprinter_2.png`) stacked on the right.
4. **04 · Voice Gaming Walkie-Talkie (`mayday_1.png` – `mayday_3.png`)**
   - `s5_04_mayday.png` (`1100×800`): Uncropped square hardware unit showing active voice comms with Nova Reyes (`mayday_2.png`).
   - `a2_mayday_collage.png` (`1564×1000`): 3-state narrative rescue collage pairing full hardware (`mayday_2.png`) on the left with Act 1 alien storm (`mayday_1.png`) and Act 3 mission rescue (`mayday_3.png`) on the right.
5. **05 · Kids' E-Ink Doodle Pad (`doodleboard_1.png` – `doodleboard_3.png`)**
   - `s5_05_doodleboard.png` (`1100×800`): Studio hardware render (`doodleboard_3.png`) featuring the sky-blue E-Ink pad, docked stylus, and orange smiley AI button—ensuring all 5 thumbnails on Slide 5 showcase physical hardware.
   - `a3_doodleboard_collage.png` (`1673×1200`): Full-story spotlight combining the physical hardware render (`doodleboard_3.png`, top-left), the child's raw sailboat sketch (`doodleboard_1.png`, top-right), and all 4 generated comic book panels (`doodleboard_2.png`, bottom strip) at native 4:3 aspect ratio.

### Cross-Format Alignment (`generate_banrai_deck.py` & `Banrai_Seed_Plus_Deck.html`)
- **Exact Aspect-Ratio Matching**: Every processed PNG matches its target PowerPoint box aspect ratio (`1.86"×1.35"`, `5.16"×3.30"`, and `6.33"×4.54"`), preventing distortion.
- **Typography & Layout Sync**: Synchronized single-line `28pt` slide titles, Slide 1's `< 9 Mos · $150K–$200K Each` callout, Slide 3/7 spacing, and single-line bullet font sizes (`10pt` on A1, `9pt` on A2/A3) across both `.pptx` and `.html`.

### Regenerating the Deck
```bash
python build_product_visuals.py
python generate_banrai_deck.py
```

