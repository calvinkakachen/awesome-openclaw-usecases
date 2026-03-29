"""
COMPOSITE pipeline — window film, wall decals, contact paper, stickers.
Strategy: extract pattern/texture from uploaded image, apply to glass/surface in scenes.

7-image Amazon listing suite optimized for CTR + conversion.
"""


# ── Global prompt rules appended to EVERY image ──
GLOBAL_RULES = """
Use the EXACT original window film pattern from the reference, preserve 100% identical pattern, texture, color placement, and line structure. Do NOT redesign, simplify, recolor, or alter the pattern in any way.

Ultra-realistic product photography, natural lighting, high-end Amazon listing style, clean composition, sharp details.

Image size: 2000x2000 px, square format, high resolution, RGB, optimized for Amazon product listing.

No distortion, no extra patterns, no AI-generated variation on the film design.

Highly realistic, looks like professional product photography, not AI-generated.
"""


class CompositePipeline:
    def __init__(self, client, profile: dict, output_dir):
        self.client = client
        self.p = profile
        self.output_dir = output_dir

    def build_tasks(self) -> list[dict]:
        pattern = self.p.get("pattern", "diamond geometric stained glass design")
        color = self.p.get("color_palette", ["#FFFFFF"])[0]
        name = self.p.get("product_name", "decorative window film")
        material = self.p.get("material", "PVC film")
        opacity = self.p.get("opacity_percent", 60)
        features = self.p.get("key_features", ["privacy protection", "light filtering", "static cling"])

        feat1 = features[0] if len(features) > 0 else "Privacy Protection"
        feat2 = features[1] if len(features) > 1 else "Light Filtering"
        feat3 = features[2] if len(features) > 2 else "No Glue Static Cling"

        # Dynamically replace pattern description in all prompts
        pattern_ref = f"{pattern} {name}"

        return [
            # ━━━━ 图1：主图（白底）— CTR ━━━━
            {
                "filename": "renders/01-main-hero-white.png",
                "folder": "renders",
                "label": "主图（白底）",
                "dimensions": "2000x2000",
                "amazon_use": "Main listing image — CTR",
                "prompt": f"""
A premium product image of a decorative stained glass window film roll ({pattern_ref}), partially unrolled to show the full pattern.

Pure white background (#FFFFFF), no environment, no props.

The film is slightly curled to show thickness and flexibility, with subtle soft shadow underneath for depth.

Camera angle: 45-degree front angle, slightly elevated perspective.

Lighting: soft studio lighting, evenly diffused, no harsh shadows, bright and clean.

The colorful {pattern} pattern must be clearly visible and sharp.

No text, no watermark, no borders.

Amazon compliant main image, product fills around 85% of the frame.

{GLOBAL_RULES}
""".strip(),
            },
            # ━━━━ 图2：厨房场景图 — 第一视觉 ━━━━
            {
                "filename": "lifestyle/02-kitchen-scene.png",
                "folder": "lifestyle",
                "label": "厨房场景图",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle — kitchen scene, first visual impact",
                "prompt": f"""
A bright modern American kitchen interior with a large window above a sink.

The window is covered with the {pattern_ref} window film (exact original pattern preserved).

Scene elements:
- white cabinets
- marble or quartz countertop
- chrome faucet
- small green plant
- bowl of lemons

Lighting: strong natural sunlight coming through the window, creating colorful light diffusion from the film.

Camera angle: straight-on front view, eye level.

Mood: clean, fresh, modern American home.

No text or minimal text.

Focus on how the film enhances the kitchen with vibrant colors and soft light.

{GLOBAL_RULES}
""".strip(),
            },
            # ━━━━ 图3：对比图（Before / After）— 转化核心 ━━━━
            {
                "filename": "lifestyle/03-before-after.png",
                "folder": "lifestyle",
                "label": "贴膜前后对比图",
                "dimensions": "2000x2000",
                "amazon_use": "Before/After comparison — core conversion image",
                "prompt": f"""
Split-screen window comparison image.

Left side (BEFORE):
- clear glass window
- visible outdoor scene (neighbor / yard visible)
- label: "BEFORE: No Privacy"

Right side (AFTER):
- same window with {pattern_ref} film applied
- outside view blurred / obscured by the {pattern} film pattern
- label: "AFTER: Daytime Privacy Protection"

Lighting: same natural daylight on both sides.

Camera: straight-on, perfectly aligned.

Text style:
- clean sans-serif font
- bold headings
- high contrast

Ensure the film pattern is EXACT and unchanged from the original {pattern} design.

Emphasize privacy effect clearly.

{GLOBAL_RULES}
""".strip(),
            },
            # ━━━━ 图4：卖点图（3合1）— 快速说服 ━━━━
            {
                "filename": "amazon-aplus/04-benefits-infographic.png",
                "folder": "amazon-aplus",
                "label": "三大卖点信息图",
                "dimensions": "2000x2000",
                "amazon_use": "Feature infographic — quick persuasion",
                "prompt": f"""
A clean infographic-style product benefit image.

Layout: horizontal or grid layout with 3 icons.

Three key features:

1. {feat1}
   Blocks unwanted views

2. {feat2}
   Softens sunlight

3. {feat3}
   No residue, reusable

Icons: minimal, modern, blue or neutral tones.

Background: light grey or soft white.

Include small product close-up showing real {pattern_ref} texture.

Lighting: soft, commercial style.

Font: modern Amazon style (Montserrat / Open Sans)

Keep design clean and professional.

{GLOBAL_RULES}
""".strip(),
            },
            # ━━━━ 图5：安装步骤图（三步骤）— 降低退货 ━━━━
            {
                "filename": "amazon-aplus/05-installation-steps.png",
                "folder": "amazon-aplus",
                "label": "三步安装指南",
                "dimensions": "2000x2000",
                "amazon_use": "Installation steps — reduce returns",
                "prompt": f"""
Step-by-step installation visual for {pattern_ref}.

3 panels layout:

Step 1:
Hand spraying water on glass
Text: "Clean & Spray"

Step 2:
Peeling backing film
Text: "Peel Backing"

Step 3:
Using squeegee to smooth film on window
Text: "Apply & Smooth"

Close-up shots, real human hands.

Visible water droplets for realism.

Lighting: natural daylight, slightly warm.

Camera: close-up macro style.

Background: real window glass.

Film pattern ({pattern}) must remain identical to original.

{GLOBAL_RULES}
""".strip(),
            },
            # ━━━━ 图6：浴室场景 — 隐私场景强化 ━━━━
            {
                "filename": "lifestyle/06-bathroom-scene.png",
                "folder": "lifestyle",
                "label": "浴室隐私场景",
                "dimensions": "2000x2000",
                "amazon_use": "Bathroom privacy scene",
                "prompt": f"""
A modern bathroom interior with a bathtub and a window.

Window covered with the {pattern_ref} window film (exact original pattern preserved).

Scene elements:
- bathtub
- towel
- minimal decor
- clean tiles

Lighting: soft natural light through the film, creating soft colorful ambient glow.

Mood: privacy, calm, relaxing.

Camera: slightly angled front view.

Focus: strong privacy effect + soft colorful light diffusion through the {pattern} film.

No text or minimal text: "Perfect for Privacy"

{GLOBAL_RULES}
""".strip(),
            },
            # ━━━━ 图7：客厅 / 卧室场景 — 情绪价值 ━━━━
            {
                "filename": "lifestyle/07-living-room-scene.png",
                "folder": "lifestyle",
                "label": "客厅/卧室氛围图",
                "dimensions": "2000x2000",
                "amazon_use": "Living room / bedroom lifestyle — emotional value",
                "prompt": f"""
A cozy American living room or bedroom.

Window with {pattern_ref} stained glass film applied (exact original pattern preserved).

Scene elements:
- sofa or bed
- wooden furniture
- warm decor
- plants

Lighting: golden hour sunlight coming through the film, creating colorful reflections and light patterns on the floor and walls.

Camera: slightly wide angle.

Mood: warm, cozy, lifestyle-driven.

Optional text:
"Adds Style & Color to Any Room"

Ensure the {pattern} film pattern is unchanged and clearly visible on the window.

{GLOBAL_RULES}
""".strip(),
            },
        ]
