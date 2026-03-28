"""
COMPOSITE pipeline — window film, wall decals, contact paper, stickers.
Strategy: extract pattern/texture from uploaded image, apply to glass/surface in scenes.
"""


class CompositePipeline:
    def __init__(self, client, profile: dict, output_dir):
        self.client = client
        self.p = profile
        self.output_dir = output_dir

    def build_tasks(self) -> list[dict]:
        name = self.p.get("product_name", "window film")
        pattern = self.p.get("pattern", "frosted pattern")
        color = self.p.get("color_palette", ["#FFFFFF"])[0]
        opacity = self.p.get("opacity_percent", 60)
        material = self.p.get("material", "PVC film")
        surface = self.p.get("target_surface", "glass window")
        rooms = self.p.get("lifestyle_rooms", ["living room", "bathroom", "office"])
        features = self.p.get("key_features", ["privacy", "UV blocking", "easy install"])

        room1 = rooms[0] if len(rooms) > 0 else "living room"
        room2 = rooms[1] if len(rooms) > 1 else "bathroom"
        room3 = rooms[2] if len(rooms) > 2 else "home office"

        style = (
            f"photorealistic product photography, professional Amazon listing image, "
            f"clean composition, commercial photography style"
        )
        film_desc = (
            f"{pattern} {name}, {material}, approximately {opacity}% opacity, "
            f"color {color}, applied to {surface}"
        )

        return [
            # ── White-background renders ──
            {
                "filename": "renders/01-flat-lay.png",
                "folder": "renders",
                "label": "平铺白底图",
                "dimensions": "2000x2000",
                "amazon_use": "Main listing image",
                "prompt": (
                    f"Product photo of {film_desc}. "
                    f"Flat lay on pure white background (#FFFFFF), "
                    f"film sheet neatly spread out, one corner slightly lifted to show it is a thin flexible film, "
                    f"pattern clearly visible across the entire sheet, "
                    f"soft even studio lighting, no harsh shadows, product fills 80% of frame. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/02-roll-view.png",
                "folder": "renders",
                "label": "卷装展示图",
                "dimensions": "2000x2000",
                "amazon_use": "Gallery image",
                "prompt": (
                    f"Product photo of {film_desc} shown partially unrolled. "
                    f"Pure white background, the roll is standing upright, "
                    f"film unfurling to the right showing the {pattern} pattern clearly, "
                    f"roll core visible at the top, "
                    f"soft studio lighting, product fills 75% of frame. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/03-pattern-closeup.png",
                "folder": "renders",
                "label": "花纹特写图",
                "dimensions": "2000x2000",
                "amazon_use": "Detail image",
                "prompt": (
                    f"Extreme macro close-up of {film_desc} pattern detail. "
                    f"Pure white background, film fills entire frame, "
                    f"pattern texture in sharp focus showing fine detail, "
                    f"color accuracy is critical: {color}, "
                    f"flat even lighting to show pattern without glare. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/04-edge-detail.png",
                "folder": "renders",
                "label": "边缘厚度图",
                "dimensions": "2000x2000",
                "amazon_use": "Detail image",
                "prompt": (
                    f"Close-up product photo showing the cut edge of {film_desc}. "
                    f"Pure white background, edge facing camera at slight angle to show thinness, "
                    f"film layer and backing layer visible, demonstrates easy-peel design, "
                    f"sharp focus on edge detail, macro photography style. "
                    f"{style}."
                ),
            },
            # ── Installed lifestyle scenes ──
            {
                "filename": "lifestyle/05-scene-living-room.png",
                "folder": "lifestyle",
                "label": f"客厅安装场景",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle image",
                "prompt": (
                    f"Photorealistic interior photo of a modern {room1}, "
                    f"large window with {film_desc} applied to the lower two-thirds of the glass, "
                    f"soft morning sunlight filtering through the {pattern} creating beautiful light patterns on the floor, "
                    f"the film maintains {opacity}% privacy while letting light through, "
                    f"stylish furniture partially visible, green plants, warm aspirational home atmosphere, "
                    f"the film texture and pattern must be accurate and realistic on the glass. "
                    f"Professional interior photography, golden hour natural light, "
                    f"sharp focus on the window with film installed. {style}."
                ),
            },
            {
                "filename": "lifestyle/06-scene-bathroom.png",
                "folder": "lifestyle",
                "label": f"卫生间安装场景",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle image",
                "prompt": (
                    f"Photorealistic interior photo of a clean modern {room2}, "
                    f"small window above sink with {film_desc} covering the full glass pane, "
                    f"natural daylight diffusing through the {pattern} film creating soft ambient light, "
                    f"white tile walls, minimalist design, plant on windowsill, "
                    f"film provides full privacy while keeping the room bright, "
                    f"the {pattern} pattern clearly visible on the glass surface. "
                    f"Professional interior photography style. {style}."
                ),
            },
            {
                "filename": "lifestyle/07-scene-office.png",
                "folder": "lifestyle",
                "label": "办公室安装场景",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle image",
                "prompt": (
                    f"Photorealistic interior photo of a modern {room3} or home office, "
                    f"glass partition or interior glass door with {film_desc} applied to the center panel, "
                    f"the {pattern} pattern centered on the glass, clear glass visible above and below the film, "
                    f"wooden desk and bookshelf visible through the clear sections, "
                    f"professional and clean atmosphere, window light from the side. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "lifestyle/08-before-after.png",
                "folder": "lifestyle",
                "label": "贴膜前后对比图",
                "dimensions": "2000x2000",
                "amazon_use": "A+ comparison image (highest converting)",
                "prompt": (
                    f"Split-image comparison photo, divided vertically down the center with a thin white line: "
                    f"LEFT HALF: plain clear glass window in a living room, "
                    f"bright outdoor scene visible through transparent glass, "
                    f"labeled 'Before' in clean sans-serif white text at top. "
                    f"RIGHT HALF: identical window and room, same lighting and angle, "
                    f"but {film_desc} applied to the glass, "
                    f"the {pattern} pattern visible on the glass, outdoor scene diffused by the film, "
                    f"labeled 'After' in clean sans-serif white text at top. "
                    f"Same room, same perspective, dramatic transformation effect, "
                    f"professional interior photography style. {style}."
                ),
            },
            # ── Amazon A+ content ──
            {
                "filename": "amazon-aplus/09-main-hero.png",
                "folder": "amazon-aplus",
                "label": "A+ 主图",
                "dimensions": "2000x2000",
                "amazon_use": "Amazon main listing image",
                "prompt": (
                    f"Amazon product listing hero image of {film_desc}. "
                    f"Pure white background (#FFFFFF), "
                    f"flat lay of the film sheet, fills 85% of the frame, "
                    f"pattern fully visible, slight 3D lift on corner showing it is a flexible film, "
                    f"perfect exposure, no shadows, no text, "
                    f"meets Amazon main image guidelines: white background, product centered. "
                    f"{style}."
                ),
            },
            {
                "filename": "amazon-aplus/10-infographic.png",
                "folder": "amazon-aplus",
                "label": "A+ 功能信息图",
                "dimensions": "970x600",
                "amazon_use": "A+ Module 1 — feature callout",
                "prompt": (
                    f"Amazon A+ content infographic for {name}. "
                    f"Clean white background, product image on the left half (flat lay of the film), "
                    f"right half shows 3 feature callout boxes arranged vertically: "
                    f"1) {features[0] if features else 'Privacy Protection'} with a simple icon, "
                    f"2) {features[1] if len(features) > 1 else 'UV Blocking'} with a simple icon, "
                    f"3) {features[2] if len(features) > 2 else 'Easy Installation'} with a simple icon, "
                    f"clean sans-serif typography, accent color {color}, "
                    f"professional e-commerce design, landscape orientation 970x600 pixels. "
                    f"{style}."
                ),
            },
            {
                "filename": "amazon-aplus/11-lifestyle-banner.png",
                "folder": "amazon-aplus",
                "label": "A+ 生活场景横幅",
                "dimensions": "970x300",
                "amazon_use": "A+ Module 2 — lifestyle banner",
                "prompt": (
                    f"Amazon A+ lifestyle banner image, wide landscape format (970x300 pixels ratio). "
                    f"Horizontal crop of a beautiful {room1} interior with {film_desc} on the window, "
                    f"film installed on glass in background, natural light filtering through {pattern}, "
                    f"left third of image is slightly lighter/empty for text overlay, "
                    f"warm aspirational home atmosphere, "
                    f"wide cinematic crop, no text in image. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/12-portrait-lifestyle.png",
                "folder": "amazon-aplus",
                "label": "A+ 竖版生活图",
                "dimensions": "300x400",
                "amazon_use": "A+ Module 3 — sidebar portrait",
                "prompt": (
                    f"Amazon A+ portrait lifestyle image (vertical 3:4 ratio). "
                    f"Close-up shot of {film_desc} installed on a {room2} window, "
                    f"natural light diffusing through {pattern} creating beautiful ambient glow, "
                    f"tight vertical crop focusing on the window and film, "
                    f"no people, clean and aspirational. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/13-brand-background.png",
                "folder": "amazon-aplus",
                "label": "A+ 品牌背景图",
                "dimensions": "970x600",
                "amazon_use": "A+ Module 4 — brand story background",
                "prompt": (
                    f"Abstract soft lifestyle background image for Amazon A+ brand story module. "
                    f"Wide landscape format (970x600 pixels ratio). "
                    f"Soft out-of-focus interior scene, warm natural light through a window, "
                    f"subtle {pattern} shadow pattern on a light wall from diffused sunlight through film, "
                    f"very light and airy, mostly white/cream tones with accent color {color}, "
                    f"no products visible, no text, "
                    f"serves as a text overlay background — needs clear readable areas. "
                    f"Professional lifestyle photography, bokeh effect, serene atmosphere. {style}."
                ),
            },
        ]
