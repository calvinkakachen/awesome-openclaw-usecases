"""
Product type detector using Google Gemini Vision.
Classifies uploaded images into: COMPOSITE / HARDWARE / FABRIC / SOLID
Uses the new google-genai SDK (same as generator.py).
"""

import json
import os
from pathlib import Path
from typing import List

from google import genai
from google.genai import types


DETECTION_PROMPT = """
You are an Amazon product photography expert. Analyze the uploaded product image(s)
and return a JSON object with the following structure.

IMPORTANT: Return ONLY valid JSON, no markdown fences, no explanation.

{
  "product_type": "<COMPOSITE|HARDWARE|FABRIC|SOLID>",
  "confidence": "<high|medium|low>",
  "detection_reason": "<one sentence explanation>",
  "product_name": "<short descriptive name in English, e.g. Diamond Geometric Stained Glass Window Film>",
  "category": "<home decor category, e.g. window film, curtain hook, curtain, vase>",
  "material": "<primary material, e.g. PVC film, zinc alloy, linen, ceramic>",
  "surface": "<surface quality: transparent|translucent|opaque|reflective|matte|glossy|fabric>",
  "color_palette": ["<hex1>", "<hex2>", "<hex3>"],
  "pattern": "<VERY DETAILED pattern description, this will be used verbatim in image generation prompts>",
  "pattern_detail": "<exhaustive visual description of the exact pattern seen in the uploaded image>",
  "opacity_percent": <0-100, only relevant for films/translucent items, else null>,
  "dimensions_note": "<relative size note, e.g. small accessory ~3cm, large panel ~120x90cm>",
  "key_features": ["<feature1>", "<feature2>", "<feature3>"],
  "target_surface": "<what surface this product is applied to or used with, e.g. glass window, curtain rod, wall>",
  "lifestyle_rooms": ["<room1>", "<room2>", "<room3>"]
}

CRITICAL — "pattern" and "pattern_detail" field rules:
Describe the EXACT visual pattern you see in the uploaded product image(s) in as much detail as possible.
This description will be directly injected into Imagen 3 prompts to recreate the pattern.
Be extremely specific about:
- Geometric shapes (diamond, hexagon, square, circular, irregular, etc.)
- Arrangement (grid, tessellated, random, radial, repeating, overlapping, etc.)
- Color distribution (which colors appear where, gradients, borders between shapes)
- Line style (thick lead lines, thin lines, no lines, black outlines, colored outlines)
- Overall visual style (stained glass, frosted, etched, mosaic, floral, abstract, etc.)
- Scale of the pattern (fine/small repeat, large/bold repeat)
- Any unique visual elements (center medallion, border pattern, mixed shapes)

Example of a GOOD "pattern" value:
"diamond geometric stained glass design with repeating diamond shapes in blue, green, amber, and clear panels, separated by thick dark lead lines, arranged in a symmetrical grid pattern, each diamond approximately 8cm, classic cathedral stained glass style"

Example of a BAD "pattern" value (too vague):
"colorful geometric pattern"

PRODUCT TYPE RULES:
- COMPOSITE: flat, thin, designed to be applied/stuck onto another surface.
  Examples: window film, frosted film, privacy film, wall decal, contact paper, vinyl sticker.
- HARDWARE: small rigid 3D accessory, typically sold in sets, part of a larger installation.
  Examples: curtain hooks, rings, clips, brackets, handles, knobs, rods.
- FABRIC: soft flexible textile product.
  Examples: curtains, drapes, blinds, pillow covers, table runners, throws.
- SOLID: standalone rigid 3D product that doesn't fit above.
  Examples: candles, vases, storage boxes, decorative objects, lamps.

If confidence is "low", set product_type to your best guess and explain in detection_reason.
"""

DEFAULT_MODEL = "gemini-2.5-flash"


class ProductDetector:
    def __init__(self, api_key: str = "", model: str = ""):
        key = api_key.strip() or os.environ.get("GOOGLE_API_KEY", "")
        if not key:
            raise RuntimeError("GOOGLE_API_KEY not provided")
        self.client = genai.Client(api_key=key)
        self.model = (model.strip() or os.environ.get("GEMINI_MODEL", "") or DEFAULT_MODEL)

    async def analyze(self, image_paths: List[str]) -> dict:
        """Analyze product images and return structured profile dict."""
        contents: List[types.Part] = []

        for path in image_paths:
            img_bytes = Path(path).read_bytes()
            mime = _mime_type(path)
            contents.append(types.Part.from_bytes(data=img_bytes, mime_type=mime))

        contents.append(types.Part.from_text(text=DETECTION_PROMPT))

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
        )
        raw = response.text.strip()

        # Strip markdown fences if model adds them anyway
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        raw = raw.strip()

        try:
            profile = json.loads(raw)
        except json.JSONDecodeError:
            # Fallback: extract JSON block
            start = raw.find("{")
            end = raw.rfind("}") + 1
            profile = json.loads(raw[start:end])

        profile["source_images"] = image_paths
        return profile


def _mime_type(path: str) -> str:
    ext = Path(path).suffix.lower()
    return {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".webp": "image/webp",
    }.get(ext, "image/jpeg")
