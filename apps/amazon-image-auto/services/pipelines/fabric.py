"""
FABRIC pipeline — curtains, drapes, blinds, pillow covers, table runners, throws.
Strategy: fabric draping simulation + room scenes showing product in natural use.
"""


class FabricPipeline:
    def __init__(self, client, profile: dict, output_dir):
        self.client = client
        self.p = profile
        self.output_dir = output_dir

    def build_tasks(self) -> list[dict]:
        name = self.p.get("product_name", "curtain")
        material = self.p.get("material", "polyester fabric")
        color = self.p.get("color_palette", ["#F5F5DC"])[0]
        pattern = self.p.get("pattern", "solid color")
        opacity = self.p.get("opacity_percent", 50)
        rooms = self.p.get("lifestyle_rooms", ["bedroom", "living room", "dining room"])
        features = self.p.get("key_features", ["light filtering", "soft drape", "easy care"])

        weight = "sheer" if opacity and opacity > 70 else ("blackout" if opacity and opacity < 20 else "medium weight")
        room1 = rooms[0] if len(rooms) > 0 else "bedroom"
        room2 = rooms[1] if len(rooms) > 1 else "living room"

        style = (
            "photorealistic product photography, professional Amazon listing image, "
            "commercial photography style"
        )
        fabric_desc = f"{pattern} {name}, {material}, {color} color, {weight}"
        drape_hint = f"realistic {weight} fabric draping with natural folds and gravity-appropriate hang"

        return [
            {
                "filename": "renders/01-flat-lay.png",
                "folder": "renders",
                "label": "面料平铺图",
                "dimensions": "2000x2000",
                "amazon_use": "Main listing image",
                "prompt": (
                    f"Product photo of {fabric_desc} laid flat on pure white background. "
                    f"Fabric neatly spread showing full {pattern} pattern and color {color}, "
                    f"texture and weave visible in sharp detail, "
                    f"soft even studio lighting, fills 80% of frame. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/02-folded-packaged.png",
                "folder": "renders",
                "label": "折叠包装图",
                "dimensions": "2000x2000",
                "amazon_use": "Gallery image",
                "prompt": (
                    f"Product photo of {fabric_desc} neatly folded as packaged, pure white background. "
                    f"Crisp folds visible, fabric {color} color consistent, "
                    f"shows as-delivered state, "
                    f"soft studio lighting, product centered. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/03-texture-detail.png",
                "folder": "renders",
                "label": "面料质感特写",
                "dimensions": "2000x2000",
                "amazon_use": "Texture detail",
                "prompt": (
                    f"Macro close-up of {fabric_desc} texture. "
                    f"White background, fabric fills entire frame, "
                    f"weave structure clearly visible, {pattern} pattern in sharp focus, "
                    f"color {color} accurate, slight sheen if applicable. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/04-backlit-opacity.png",
                "folder": "renders",
                "label": "透光效果图",
                "dimensions": "2000x2000",
                "amazon_use": "Opacity demonstration",
                "prompt": (
                    f"Product photo demonstrating light transmission of {fabric_desc}. "
                    f"Fabric panel hung against a bright window or light source, "
                    f"backlit to show how much light passes through ({opacity}% opacity), "
                    f"natural draping with {drape_hint}, "
                    f"demonstrates {weight} quality clearly. "
                    f"{style}."
                ),
            },
            {
                "filename": "lifestyle/05-primary-room.png",
                "folder": "lifestyle",
                "label": f"{room1}安装场景",
                "dimensions": "2000x2000",
                "amazon_use": "Primary lifestyle image",
                "prompt": (
                    f"Photorealistic interior photo of a stylish {room1}, "
                    f"{fabric_desc} hanging on a window curtain rod, "
                    f"{drape_hint}, natural folds and pleats, "
                    f"color {color} accurate, {pattern} pattern visible, "
                    f"soft natural light, aspirational home decor, "
                    f"room furniture softly visible in background. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "lifestyle/06-secondary-room.png",
                "folder": "lifestyle",
                "label": f"{room2}安装场景",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle variation",
                "prompt": (
                    f"Photorealistic interior photo of a modern {room2}, "
                    f"{fabric_desc} as floor-length curtains on a rod, "
                    f"{drape_hint}, "
                    f"golden hour afternoon light partially visible behind curtain, "
                    f"elegant and cozy atmosphere. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "lifestyle/07-window-detail.png",
                "folder": "lifestyle",
                "label": "窗口采光细节图",
                "dimensions": "2000x2000",
                "amazon_use": "Light filtering detail",
                "prompt": (
                    f"Close-up interior shot of {fabric_desc} hanging in front of a window. "
                    f"Natural daylight filtering through the {weight} fabric, "
                    f"fabric folds and drape in sharp focus, "
                    f"light quality shown clearly — demonstrates filtering effect. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "lifestyle/08-styled-scene.png",
                "folder": "lifestyle",
                "label": "生活方式场景图",
                "dimensions": "2000x2000",
                "amazon_use": "Aspirational lifestyle",
                "prompt": (
                    f"Aspirational lifestyle photo featuring {fabric_desc} as part of a fully styled {room1} interior. "
                    f"Product is a natural part of the scene, not the sole focus, "
                    f"complementary home decor elements (plants, cushions, furniture) in view, "
                    f"warm natural light, magazine-style interior design. "
                    f"Professional editorial interior photography. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/09-main-hero.png",
                "folder": "amazon-aplus",
                "label": "A+ 主图",
                "dimensions": "2000x2000",
                "amazon_use": "Amazon main listing image",
                "prompt": (
                    f"Amazon main listing hero image of {fabric_desc}. "
                    f"Pure white background (#FFFFFF), fabric panel hanging or neatly folded, "
                    f"fills 85% of frame, color {color} accurate, pattern clearly visible. "
                    f"No shadows, no text. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/10-infographic.png",
                "folder": "amazon-aplus",
                "label": "A+ 功能信息图",
                "dimensions": "970x600",
                "amazon_use": "A+ Module 1",
                "prompt": (
                    f"Amazon A+ infographic for {name}, landscape 970x600 format. "
                    f"Fabric texture detail on left half, white background, "
                    f"right half with 3 feature callouts: "
                    f"1) {features[0] if features else 'Light Filtering'}, "
                    f"2) {features[1] if len(features) > 1 else 'Soft Drape'}, "
                    f"3) {features[2] if len(features) > 2 else 'Easy Care'}, "
                    f"accent color {color}, clean typography. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/11-lifestyle-banner.png",
                "folder": "amazon-aplus",
                "label": "A+ 横幅图",
                "dimensions": "970x300",
                "amazon_use": "A+ Module 2 banner",
                "prompt": (
                    f"Wide landscape A+ banner (970x300 ratio), horizontal crop of {room1} "
                    f"with {fabric_desc} at window, warm natural light, "
                    f"left third lighter for text, no text in image. "
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
                    f"Vertical portrait (3:4 ratio) A+ image, "
                    f"close-up of {fabric_desc} draped at window, "
                    f"natural backlight showing fabric quality and drape, no text. "
                    f"Professional photography. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/13-brand-background.png",
                "folder": "amazon-aplus",
                "label": "A+ 品牌背景图",
                "dimensions": "970x600",
                "amazon_use": "A+ Module 4 brand story",
                "prompt": (
                    f"Soft abstract background for Amazon A+ brand story, landscape 970x600 ratio. "
                    f"Out-of-focus soft fabric texture with color {color}, "
                    f"gentle bokeh, warm light, clean and airy, "
                    f"serves as text overlay background. "
                    f"No products, no text. Professional photography. {style}."
                ),
            },
        ]
