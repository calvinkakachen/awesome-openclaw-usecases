"""
Product type detector using Google Gemini Vision.
Classifies uploaded images into: COMPOSITE / HARDWARE / FABRIC / SOLID
"""

import base64
import json
import os
from pathlib import Path

import google.generativeai as genai
from PIL import Image


DETECTION_PROMPT = """
You are an Amazon product photography expert. Analyze the uploaded product image(s)
and return a JSON object with the following structure.

IMPORTANT: Return ONLY valid JSON, no markdown fences, no explanation.

{
  "product_type": "<COMPOSITE|HARDWARE|FABRIC|SOLID>",
  "confidence": "<high|medium|low>",
  "detection_reason": "<one sentence explanation>",
  "product_name": "<short descriptive name>",
  "category": "<home decor category, e.g. window film, curtain hook, curtain, vase>",
  "material": "<primary material, e.g. PVC film, zinc alloy, linen, ceramic>",
  "surface": "<surface quality: transparent|translucent|opaque|reflective|matte|glossy|fabric>",
  "color_palette": ["<hex1>", "<hex2>", "<hex3>"],
  "pattern": "<pattern description or 'none'>",
  "opacity_percent": <0-100, only relevant for films/translucent items, else null>,
  "dimensions_note": "<relative size note, e.g. small accessory ~3cm, large panel ~120x90cm>",
  "key_features": ["<feature1>", "<feature2>", "<feature3>"],
  "target_surface": "<what surface this product is applied to or used with, e.g. glass window, curtain rod, wall>",
  "lifestyle_rooms": ["<room1>", "<room2>", "<room3>"]
}

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


class ProductDetector:
    def __init__(self):
        api_key = os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("GOOGLE_API_KEY environment variable is not set")
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel("gemini-2.0-flash")

    async def analyze(self, image_paths: list[str]) -> dict:
        """Analyze product images and return structured profile dict."""
        parts = []

        for path in image_paths:
            img_bytes = Path(path).read_bytes()
            mime = _mime_type(path)
            parts.append({"mime_type": mime, "data": img_bytes})

        parts.append(DETECTION_PROMPT)

        response = self.model.generate_content(parts)
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
