# Banrai Seed+ Deck — Strategy, Design Rationale & Historical Iteration Log

> **Purpose of this Document:** Serves as the central knowledge base and historical changelog for the Banrai Seed+ Investor Deck—capturing our strategic framing, visual design rules, layout audit standards, and iteration history (`v1` → `v2` → `v3`).

---

## 1. Strategic Framing: How We Hook Investors in 7 Core Slides + 3 Appendix Slides

When early-stage hardware + AI investors review a deck, they typically raise two immediate objections:
1. *"AI apps are a feature war dominated by OpenAI, Google, and Anthropic."*
2. *"Consumer hardware is slow, capital-intensive, and dies after Gen-1 unit sales."*

The Banrai narrative sequences your insights so that **every slide disarms a specific investor skepticism and builds toward an inevitable conclusion**:

```
[1. Cover: Joy, Not Chores] ──► [2. 2x2 Matrix: Fun AI vs Functional AI] ──► [3. SaaS Model: 100% Hard-Sub]
                                                                                       │
[7. Summary] ◄── [6. Joy Data Flywheel] ◄── [5. 5-SKU US Roadmap] ◄── [4. 1 Shared Core -> Dozens of SKUs]
```

---

## 2. Visual & Typography Standards ("Pantone Calm Editorial")

### Color Palette (Pantone-Inspired Light Theme)
| Role | Pantone Reference | Hex / RGB | Usage Rule |
| :--- | :--- | :--- | :--- |
| **Slide Canvas** | *Pantone 11-4201 Cloud Dancer* | `#F4F2ED` `(244, 242, 237)` | Warm alabaster paper background across all slides to eliminate eye strain. |
| **Primary Card** | *Pantone Marshmallow* | `#FBFAF7` `(251, 250, 247)` | Main elevated surface for diagrams and product cards. |
| **Secondary Card** | *Pantone 12-0104 Warm Sand* | `#ECE9E1` `(236, 233, 225)` | Neutral comparison boxes and image drop-zone frames. |
| **Botanical Tint** | *Pantone Soft Celadon* | `#E1E8E0` `(225, 232, 224)` | Calm secondary highlight for Banrai platform nodes. |
| **Mineral Tint** | *Pantone Pale Mist* | `#E0E7EC` `(224, 231, 236)` | Subtle pipeline / H1 2027 prototype badges. |
| **Primary Ink** | *Pantone 19-4007 After Dark* | `#23262A` `(35, 38, 42)` | Soft charcoal ink for headlines and primary labels. |
| **Secondary Ink** | *Pantone 17-4402 Neutral Gray* | `#60656C` `(96, 101, 108)` | Body copy and supporting descriptions. |
| **Botanical Accent** | *Pantone 17-0210 Laurel Oak* | `#58725C` `(88, 114, 92)` | Eyebrow headers, connector lines, and calm structural accents. |
| **Hero Callout** | *Banrai Signature Lime* | `#CAFB5B` `(202, 251, 91)` | **Strictly reserved for 1 hero callout per slide + the `Banrai.` logo dot.** |

### Layout & Typography Guardrails (Enforced via Automated Audit)
- **Font Family:** `Poppins` (installed locally in `~/Library/Fonts/Poppins-*.ttf` so PowerPoint and macOS QuickLook render true geometric metrics without fallback substitution).
- **Single-Line Lock (`word_wrap=False`):** All slide titles (`23pt` across `11.53in`), section eyebrows, stat headers, spoke labels, and badges have explicit single-line width budgets with a 12% PowerPoint kerning safety margin so a 1-line label **never** wraps onto 2 lines.
- **Native Vector Connectors:** Because `Poppins` lacks glyphs for Unicode arrows (`→`, `←`, `↑`, `↓`, `↺`), all flow diagrams use native PowerPoint vector connector bars and ovals (`add_connector_bar`) rather than Unicode arrow characters.

---

## 3. Slide-by-Slide Architecture (v3)

### Core Investor Deck (`01` – `07`)
1. **Slide 01 — Cover:** `Banrai.` wordmark + lime dot, *"Consumer AI Hardware Built for Joy, Not Chores"*, *"Make Humans Talk Again"*, and 3 summary pills (Hero Lime Callout: **`< 9 Mos · $150K–$200K`**).
2. **Slide 02 — Category Positioning (2×2 Matrix Graphic):** Visual quadrant plotting *Work & Tasks vs. Play & Daily Joy* and *Screen Chatbots vs. Tactile Hardware*, isolating **Banrai · "Fun AI"** (Hero Lime Callout) alongside 3 crisp essence cards.
3. **Slide 03 — Business Model (Dual Revenue Lifecycle Graphic):** Contrasts Traditional Hardware (`Day 1: Sell Box → Month 2–12: $0 Recurring → Year 2+: Push Gen-2`) with Banrai's **100% Hard-Subscription Flow** (`01 Unbox w/ Free Trial → 02 Monthly Subscription [Hero Lime Callout] → 03 Continuous SaaS LTV`).
4. **Slide 04 — Unfair Advantage (Hub-and-Spoke + Cost Bars):**
   - **Left:** **1 Unified AI + Billing Backend** (*Conversational Voice OS, Image & Story Engine, Subscription & Metering*) radiating via vector connectors to **6+ Hardware Spoke Nodes** (`01 Living Photo Frame` through `06–10+ New SKUs / Yr`).
   - **Right:** Horizontal bar comparisons for Time to Market (`< 9 Mos` vs. `18–24+ Mos`), All-In Launch Cost (**`$150K–$200K`** [Hero Lime Callout] vs. `$3M–$10M+`), and Unit Winner Threshold (`100K+ units` vs. `10M+ units`).
5. **Slide 05 — Product Roadmap at a Glance (5-Column Visual Strip):** Consolidates all 5 products into a single roadmap slide—**Wave 1 · Dec 2026 (1,000 US Units Each · On Budget)** [Hero Lime Callout] and **Wave 2 · H1 2027 (Prototyping)**—plus a pointer to the Product Appendix.
6. **Slide 06 — Defensibility & Data Moat (4-Node Flywheel Graphic):** Contrasts Public Internet Data with **Banrai Proprietary Joy Data** [Hero Lime Callout], followed by the 4-stage compounding loop (`01 Ship → 02 Spark → 03 Collect → 04 Evolve`).
7. **Slide 07 — Closing Summary:** 3 executive pillars (*Fun AI > Functional AI*, **`< 9 Mos · $150K–$200K`** [Hero Lime Callout], *2 Launching · 3 Prototyping*) + closing contact banner (`banrai.ai · hello@banrai.ai`).

### Product Gallery Appendix (`A1` – `A3`)
- **Appendix A1 (Wave 1 · Dec 2026):** Side-by-side large `16:10` image drop-zones + 2 concise bullets each for **Magical Living Photo Frame** and **Pocket Interactive Bible**.
- **Appendix A2 (Wave 2 · H1 2027 Prototyping):** Side-by-side large `16:10` image drop-zones + 2 concise bullets each for **Dream Printer** and **Voice Gaming Walkie-Talkie**.
- **Appendix A3 (Wave 2 Spotlight · H1 2027 Prototyping):** Split hero gallery (`6.29in × 4.66in` image drop-zone on the right) + 3 concise feature cards on the left for the **Eye-Friendly E-Ink Children’s Doodle Pad**.

---

## 4. Historical Iteration Log (Changelog)

### `v1` — Initial 9-Slide Draft (`commit e3c9560`)
- Translated the founder's raw brain dump into `Founder_Brain_Dump_Structured.md` and created a 9-slide deck in both Dark (`Banrai_Seed_Plus_Deck.pptx`) and Light (`Banrai_Seed_Plus_Deck_Light.pptx`) themes plus an HTML preview.
- **Feedback received:** Dark theme with multiple bright accents was hard on the eyes; slides were too text-heavy; product descriptions took up 3 of the 9 main slides and crowded the narrative.

### `v2` — Pantone Calm Light Theme, Visual Diagrams & Product Appendix (`commit ee59c42`)
- Switched exclusively to a **Pantone-inspired warm light palette** (`#F4F2ED` Cloud Dancer base) and restricted bright Banrai Lime (`#CAFB5B`) to **1 hero callout per slide**.
- Replaced text walls with 4 visual diagrams (2×2 positioning matrix, hardware vs. SaaS lifecycle flow, hub-and-spoke shared backend + cost comparison bars, and 4-node data flywheel).
- Consolidated products into 1 roadmap slide in the 7-slide core deck and moved individual product deep-dives into a 3-slide **Product Gallery Appendix (`A1`–`A3`)**.
- **Feedback received:** Much better direction, but several 1-line headings/labels wrapped onto 2 lines in PowerPoint and caused overlapping text.

### `v3` — Full Geometry, Font & Line-Wrap Audit (`Current`)
- **Root-Cause Diagnosis:**
  1. `Poppins` was not installed in `~/Library/Fonts` on the local Mac, causing PowerPoint/QuickLook to substitute a wider fallback font.
  2. Several narrow cards (`1.82in–3.20in` wide) had font sizes (`13pt–19pt`) that wrapped single-line titles onto 2 lines (`"100% Hard-Subscription"`, `"2 Launching · 3 Prototyping"`, `"Magical Living Photo Frame"`, `"Voice Gaming Walkie-Talkie"`), overflowing vertically into the text box below.
  3. On Slide 4's spoke nodes and Slide 5's bottom bar, left-aligned and right-aligned text boxes had overlapping horizontal coordinates (`l + w > right_box.l`).
  4. `Poppins` lacked glyphs for Unicode arrows (`→`, `←`, `↑`, `↓`, `↺`) and fullwidth `＋`.
- **Fixes Applied & Verified:**
  - Installed `Poppins` (`Light`, `Regular`, `Medium`, `SemiBold`, `Bold`) directly into `~/Library/Fonts`.
  - Built an automated bounding-box & TrueType text-width audit script to verify every slide with a 12% PowerPoint kerning safety margin.
  - Resized and locked all single-line headings/labels (`word_wrap=False`) and separated all horizontal/vertical bounding boxes so **zero unintended line wraps, height overflows, or box overlaps exist across all 10 slides**.
  - Replaced all unsupported Unicode arrows with native PowerPoint vector connector bars + center dots (`add_connector_bar`).
