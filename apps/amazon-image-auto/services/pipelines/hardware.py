"""
HARDWARE pipeline — curtain hooks, rings, clips, brackets, handles, knobs.
Strategy: 3D renders at multiple angles + installed context scenes.
"""


class HardwarePipeline:
    def __init__(self, client, profile: dict, output_dir):
        self.client = client
        self.p = profile
        self.output_dir = output_dir

    def build_tasks(self) -> list[dict]:
        name = self.p.get("product_name", "curtain hook")
        material = self.p.get("material", "metal")
        surface = self.p.get("surface", "matte")
        color = self.p.get("color_palette", ["#C0A060"])[0]
        rooms = self.p.get("lifestyle_rooms", ["bedroom", "living room", "dining room"])
        features = self.p.get("key_features", ["durable", "smooth glide", "decorative"])

        room1 = rooms[0] if len(rooms) > 0 else "bedroom"
        room2 = rooms[1] if len(rooms) > 1 else "living room"
        room3 = rooms[2] if len(rooms) > 2 else "dining room"

        finish_desc = f"{surface} {material} finish, color {color}"
        style = (
            "photorealistic product photography, professional Amazon listing image, "
            "commercial photography style, sharp focus"
        )
        metal_hint = (
            f"accurate {surface} metal rendering with directional grain highlights, "
            f"realistic specular reflection on {material}"
        )

        return [
            # ── White-background renders ──
            {
                "filename": "renders/01-hero-fan.png",
                "folder": "renders",
                "label": "多件展示图",
                "dimensions": "2000x2000",
                "amazon_use": "Main listing image",
                "prompt": (
                    f"Product photo of 5 {name}s arranged in a slight fan/arc layout on pure white background (#FFFFFF). "
                    f"{finish_desc}, {metal_hint}, "
                    f"45-degree hero angle, even soft studio lighting, "
                    f"subtle drop shadow at base, product fills 75% of frame, "
                    f"shows the full set as sold, every detail sharp. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/02-single-front.png",
                "folder": "renders",
                "label": "单件正面图",
                "dimensions": "2000x2000",
                "amazon_use": "Gallery image",
                "prompt": (
                    f"Product photo of a single {name}, front-facing, pure white background (#FFFFFF). "
                    f"{finish_desc}, {metal_hint}, "
                    f"product centered and fills 70% of frame, "
                    f"straight-on view showing the front face and mechanism clearly, "
                    f"soft studio lighting, subtle drop shadow. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/03-side-profile.png",
                "folder": "renders",
                "label": "侧面深度图",
                "dimensions": "2000x2000",
                "amazon_use": "Detail image",
                "prompt": (
                    f"Product photo of a single {name} shown from the side profile, pure white background (#FFFFFF). "
                    f"{finish_desc}, {metal_hint}, "
                    f"side view reveals depth, hook curve, and clasp/mechanism detail, "
                    f"product centered at 90-degree side angle, fills 60% of frame, "
                    f"sharp focus on mechanism detail. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/04-on-rod-white.png",
                "folder": "renders",
                "label": "安装状态白底图",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle-adjacent detail",
                "prompt": (
                    f"Product photo of 3 {name}s already installed on a curtain rod, white background (#FFFFFF). "
                    f"{finish_desc}, "
                    f"rod shown horizontally across the upper part of the frame, "
                    f"hooks hanging from rod with a small section of curtain fabric visible at edge, "
                    f"demonstrates how the product is used, "
                    f"clean studio lighting, shows scale and installation method. "
                    f"{style}."
                ),
            },
            # ── Lifestyle scenes ──
            {
                "filename": "lifestyle/05-bedroom-scene.png",
                "folder": "lifestyle",
                "label": "主卧生活场景",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle image",
                "prompt": (
                    f"Photorealistic interior photo of a stylish {room1}, "
                    f"{name}s with {finish_desc} installed on a curtain rod above the bed, "
                    f"linen or cotton curtains draped through the hooks, "
                    f"soft morning backlight coming through the window behind the curtains, "
                    f"hooks visible and in sharp focus at mid-frame, "
                    f"bed partially in foreground, warm cozy atmosphere, "
                    f"aspirational home decor style. "
                    f"Professional interior photography with natural light. {style}."
                ),
            },
            {
                "filename": "lifestyle/06-living-room-scene.png",
                "folder": "lifestyle",
                "label": "客厅生活场景",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle image",
                "prompt": (
                    f"Photorealistic interior photo of a modern {room2}, "
                    f"floor-length curtains hanging on {name}s with {finish_desc} on a ceiling-mounted rod, "
                    f"hooks visible at upper portion of frame, curtains with elegant drape, "
                    f"golden hour afternoon light, parquet floor visible, "
                    f"sofa and plant in soft background focus. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "lifestyle/07-macro-hero.png",
                "folder": "lifestyle",
                "label": "特写英雄图",
                "dimensions": "2000x2000",
                "amazon_use": "Hero detail lifestyle",
                "prompt": (
                    f"Macro hero shot: 4-5 {name}s with {finish_desc} on a curtain rod in sharp foreground focus, "
                    f"curtain fabric draped elegantly through/over the hooks, "
                    f"room interior softly blurred in background (bokeh), "
                    f"hooks fill center of frame, every surface detail and finish visible, "
                    f"{metal_hint}, "
                    f"dramatic product hero lighting. "
                    f"Professional product photography with shallow depth of field. {style}."
                ),
            },
            {
                "filename": "lifestyle/08-dining-scene.png",
                "folder": "lifestyle",
                "label": "餐厅生活场景",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle variation",
                "prompt": (
                    f"Photorealistic interior photo of a bright {room3} or kitchen, "
                    f"café-style short curtains hanging on {name}s with {finish_desc}, "
                    f"hooks on a small rod above a window, "
                    f"natural daylight streaming in, herb plants on windowsill, "
                    f"wooden cutting board and simple decor in background, "
                    f"airy and fresh atmosphere. "
                    f"Professional interior photography. {style}."
                ),
            },
            # ── Amazon A+ ──
            {
                "filename": "amazon-aplus/09-main-hero.png",
                "folder": "amazon-aplus",
                "label": "A+ 主图",
                "dimensions": "2000x2000",
                "amazon_use": "Amazon main listing image",
                "prompt": (
                    f"Amazon main listing image of {name}s, 5 units in fan arrangement, "
                    f"pure white background (#FFFFFF), {finish_desc}, {metal_hint}, "
                    f"product fills 85% of frame, perfect exposure, no shadows, no text, "
                    f"meets Amazon white background requirement. "
                    f"{style}."
                ),
            },
            {
                "filename": "amazon-aplus/10-infographic.png",
                "folder": "amazon-aplus",
                "label": "A+ 功能信息图",
                "dimensions": "970x600",
                "amazon_use": "A+ Module 1",
                "prompt": (
                    f"Amazon A+ infographic for {name}s, landscape 970x600 format. "
                    f"Product photo of single {name} with {finish_desc} on the left half, "
                    f"right half has 3 feature callout labels: "
                    f"1) {features[0] if features else 'Premium Material'}, "
                    f"2) {features[1] if len(features) > 1 else 'Smooth Glide'}, "
                    f"3) {features[2] if len(features) > 2 else 'Easy Install'}, "
                    f"clean white background, sans-serif font, accent color {color}, "
                    f"professional e-commerce design. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/11-lifestyle-banner.png",
                "folder": "amazon-aplus",
                "label": "A+ 横幅图",
                "dimensions": "970x300",
                "amazon_use": "A+ Module 2 banner",
                "prompt": (
                    f"Wide landscape banner (970x300 ratio) for Amazon A+, "
                    f"horizontal crop of {room1} interior with {name}s and curtains installed, "
                    f"warm natural light, hooks visible in the scene, "
                    f"left third of image slightly lighter for text overlay, "
                    f"no text in image, wide cinematic composition. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/12-portrait.png",
                "folder": "amazon-aplus",
                "label": "A+ 竖版图",
                "dimensions": "300x400",
                "amazon_use": "A+ Module 3 portrait",
                "prompt": (
                    f"Vertical portrait format (3:4 ratio) for Amazon A+. "
                    f"Close-up of {name}s with {finish_desc} on curtain rod with draped fabric, "
                    f"macro focus on hook detail, background blurred, "
                    f"warm aspirational atmosphere, no text. "
                    f"Professional product photography. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/13-brand-background.png",
                "folder": "amazon-aplus",
                "label": "A+ 品牌背景图",
                "dimensions": "970x600",
                "amazon_use": "A+ Module 4 brand story",
                "prompt": (
                    f"Abstract soft background image for Amazon A+ brand story, landscape 970x600 ratio. "
                    f"Soft out-of-focus interior scene, window light through curtains, "
                    f"subtle warm tones and fabric texture in background, "
                    f"accent color {color} as subtle accent, "
                    f"no products, no text, light and airy, "
                    f"serves as text overlay background with clear readable areas. "
                    f"Professional lifestyle photography, bokeh, serene. {style}."
                ),
            },
        ]
