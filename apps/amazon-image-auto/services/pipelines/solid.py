"""
SOLID pipeline — general rigid 3D home decor products (vases, candles, storage boxes, etc).
Strategy: multi-angle 3D renders + home lifestyle scenes.
"""


class SolidPipeline:
    def __init__(self, client, profile: dict, output_dir):
        self.client = client
        self.p = profile
        self.output_dir = output_dir

    def build_tasks(self) -> list[dict]:
        name = self.p.get("product_name", "home decor product")
        material = self.p.get("material", "ceramic")
        surface = self.p.get("surface", "matte")
        color = self.p.get("color_palette", ["#FFFFFF"])[0]
        pattern = self.p.get("pattern", "none")
        rooms = self.p.get("lifestyle_rooms", ["living room", "bedroom", "kitchen"])
        features = self.p.get("key_features", ["elegant design", "durable", "versatile"])
        dim = self.p.get("dimensions_note", "medium sized")

        room1 = rooms[0] if len(rooms) > 0 else "living room"
        room2 = rooms[1] if len(rooms) > 1 else "bedroom"

        style = (
            "photorealistic product photography, professional Amazon listing image, "
            "commercial photography style, sharp detail"
        )
        product_desc = (
            f"{name}, {material}, {surface} surface, color {color}"
            + (f", {pattern} pattern" if pattern and pattern != "none" else "")
            + f", {dim}"
        )

        return [
            {
                "filename": "renders/01-front.png",
                "folder": "renders",
                "label": "正面白底图",
                "dimensions": "2000x2000",
                "amazon_use": "Main listing image",
                "prompt": (
                    f"Product photo of {product_desc}. "
                    f"Front-facing, pure white background (#FFFFFF), "
                    f"product centered, fills 80% of frame, "
                    f"soft studio lighting from upper-left, subtle drop shadow at base. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/02-hero-45.png",
                "folder": "renders",
                "label": "45度英雄图",
                "dimensions": "2000x2000",
                "amazon_use": "Gallery hero",
                "prompt": (
                    f"Product photo of {product_desc}. "
                    f"45-degree front-right hero angle, pure white background (#FFFFFF), "
                    f"shows front, side, and top simultaneously, "
                    f"fills 80% of frame, subtle drop shadow. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/03-three-quarter.png",
                "folder": "renders",
                "label": "3/4俯视图",
                "dimensions": "2000x2000",
                "amazon_use": "Gallery image",
                "prompt": (
                    f"Product photo of {product_desc}. "
                    f"3/4 perspective from slightly above-left, pure white background, "
                    f"shows full depth, width, and top surface of the product. "
                    f"{style}."
                ),
            },
            {
                "filename": "renders/04-detail.png",
                "folder": "renders",
                "label": "材质细节特写",
                "dimensions": "2000x2000",
                "amazon_use": "Detail image",
                "prompt": (
                    f"Close-up macro detail photo of {product_desc}. "
                    f"White background, surface texture and {surface} finish in sharp focus, "
                    f"highlights the key selling point: material quality. "
                    f"{style}."
                ),
            },
            {
                "filename": "lifestyle/05-primary-scene.png",
                "folder": "lifestyle",
                "label": f"{room1}生活场景",
                "dimensions": "2000x2000",
                "amazon_use": "Primary lifestyle",
                "prompt": (
                    f"Photorealistic interior photo of a stylish {room1} with {product_desc} "
                    f"as a focal point in the scene. "
                    f"Product naturally placed on shelf, table, or counter appropriate to {room1}, "
                    f"complementary home decor around it (plants, books, candles), "
                    f"warm natural light, aspirational home atmosphere. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "lifestyle/06-secondary-scene.png",
                "folder": "lifestyle",
                "label": f"{room2}生活场景",
                "dimensions": "2000x2000",
                "amazon_use": "Lifestyle variation",
                "prompt": (
                    f"Photorealistic interior photo of a cozy {room2} featuring {product_desc}. "
                    f"Different styling and mood from primary scene, "
                    f"warm evening light or golden hour, "
                    f"magazine-quality home decor composition. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "lifestyle/07-styled-flatlay.png",
                "folder": "lifestyle",
                "label": "平铺场景图",
                "dimensions": "2000x2000",
                "amazon_use": "Styled flat lay",
                "prompt": (
                    f"Styled flat lay photo of {product_desc} with complementary props on a "
                    f"light wood or marble surface. "
                    f"Overhead shot, product is the hero with supporting elements (flowers, fabric, books), "
                    f"warm natural daylight from the side. "
                    f"Professional lifestyle flat lay photography. {style}."
                ),
            },
            {
                "filename": "lifestyle/08-in-use.png",
                "folder": "lifestyle",
                "label": "使用中场景图",
                "dimensions": "2000x2000",
                "amazon_use": "In-use demonstration",
                "prompt": (
                    f"Photorealistic photo showing {product_desc} in active use in a {room1}. "
                    f"Shows the product fulfilling its purpose, "
                    f"aspirational lifestyle context, no people needed, "
                    f"warm inviting atmosphere. "
                    f"Professional interior photography. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/09-main-hero.png",
                "folder": "amazon-aplus",
                "label": "A+ 主图",
                "dimensions": "2000x2000",
                "amazon_use": "Amazon main listing image",
                "prompt": (
                    f"Amazon main listing image of {product_desc}. "
                    f"Pure white background (#FFFFFF), product fills 85% of frame, "
                    f"front-facing or slight 45-degree angle, "
                    f"perfect exposure, no shadows, no text. {style}."
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
                    f"Product hero image on left, white background, "
                    f"3 feature callouts on right: "
                    f"1) {features[0] if features else 'Premium Quality'}, "
                    f"2) {features[1] if len(features) > 1 else 'Elegant Design'}, "
                    f"3) {features[2] if len(features) > 2 else 'Versatile Use'}, "
                    f"accent color {color}, clean sans-serif design. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/11-lifestyle-banner.png",
                "folder": "amazon-aplus",
                "label": "A+ 横幅图",
                "dimensions": "970x300",
                "amazon_use": "A+ Module 2 banner",
                "prompt": (
                    f"Wide A+ banner (970x300 ratio), horizontal crop of {room1} scene "
                    f"with {product_desc} prominent, warm natural light, "
                    f"left third open for text, no text in image. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/12-portrait.png",
                "folder": "amazon-aplus",
                "label": "A+ 竖版图",
                "dimensions": "300x400",
                "amazon_use": "A+ Module 3 portrait",
                "prompt": (
                    f"Vertical portrait A+ image (3:4 ratio) of {product_desc}, "
                    f"lifestyle context in {room2}, warm light, no text. {style}."
                ),
            },
            {
                "filename": "amazon-aplus/13-brand-background.png",
                "folder": "amazon-aplus",
                "label": "A+ 品牌背景图",
                "dimensions": "970x600",
                "amazon_use": "A+ Module 4 brand story",
                "prompt": (
                    f"Soft abstract background for Amazon A+ brand story, 970x600 ratio. "
                    f"Out-of-focus {material} texture or interior atmosphere with accent color {color}, "
                    f"light and airy, for text overlay use, no products, no text. {style}."
                ),
            },
        ]
