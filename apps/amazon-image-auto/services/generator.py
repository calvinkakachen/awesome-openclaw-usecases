"""
Image generator using Google Imagen 3.
Orchestrates pipeline selection and streams progress events.
"""

import json
import os
from pathlib import Path
from typing import AsyncGenerator

from google import genai
from google.genai.types import GenerateImagesConfig

from services.pipelines.composite import CompositePipeline
from services.pipelines.fabric import FabricPipeline
from services.pipelines.hardware import HardwarePipeline
from services.pipelines.solid import SolidPipeline

PIPELINES = {
    "COMPOSITE": CompositePipeline,
    "HARDWARE": HardwarePipeline,
    "FABRIC": FabricPipeline,
    "SOLID": SolidPipeline,
}


class ImageGenerator:
    def __init__(self, api_key: str = ""):
        key = api_key.strip() or os.environ.get("GOOGLE_API_KEY", "")
        if not key:
            raise RuntimeError("GOOGLE_API_KEY not provided")
        self.client = genai.Client(api_key=key)

    async def generate(
        self, profile: dict, output_dir: Path
    ) -> AsyncGenerator[dict, None]:
        """
        Yields SSE-compatible event dicts:
          { type: "progress", step: str, total: int, current: int }
          { type: "image",    filename: str, url: str, label: str }
          { type: "done",     manifest: [...] }
          { type: "error",    message: str }
        """
        product_type = profile.get("product_type", "SOLID").upper()
        pipeline_cls = PIPELINES.get(product_type, SolidPipeline)
        pipeline = pipeline_cls(self.client, profile, output_dir)

        yield {
            "type": "detected",
            "product_type": product_type,
            "confidence": profile.get("confidence", "medium"),
            "reason": profile.get("detection_reason", ""),
            "product_name": profile.get("product_name", "Product"),
        }

        manifest = []
        tasks = pipeline.build_tasks()
        total = len(tasks)

        for i, task in enumerate(tasks, 1):
            yield {
                "type": "progress",
                "step": task["label"],
                "current": i,
                "total": total,
            }

            try:
                result = await self._generate_image(task["prompt"], output_dir, task["filename"])
                manifest.append({
                    "filename": task["filename"],
                    "url": f"/output/{output_dir.name}/{task['filename']}",
                    "label": task["label"],
                    "folder": task["folder"],
                    "dimensions": task.get("dimensions", "2000x2000"),
                    "amazon_use": task.get("amazon_use", ""),
                })
                yield {
                    "type": "image",
                    "filename": task["filename"],
                    "url": f"/output/{output_dir.name}/{task['filename']}",
                    "label": task["label"],
                    "folder": task["folder"],
                }
            except Exception as e:
                yield {"type": "image_error", "filename": task["filename"], "message": str(e)}

        # Write manifest
        manifest_data = {
            "product": profile.get("product_name", "Product"),
            "detected_type": product_type,
            "detection_confidence": profile.get("confidence", "medium"),
            "session_id": profile.get("session_id", ""),
            "files": manifest,
        }
        (output_dir / "image-manifest.json").write_text(
            json.dumps(manifest_data, ensure_ascii=False, indent=2)
        )

        yield {"type": "done", "manifest": manifest_data}

    async def _generate_image(self, prompt: str, output_dir: Path, filename: str) -> Path:
        subfolder = output_dir / Path(filename).parent
        subfolder.mkdir(parents=True, exist_ok=True)
        dest = output_dir / filename

        response = self.client.models.generate_images(
            model="imagen-3.0-generate-001",
            prompt=prompt,
            config=GenerateImagesConfig(
                number_of_images=1,
                output_mime_type="image/png",
                aspect_ratio="1:1",
            ),
        )

        if not response.generated_images:
            raise RuntimeError(f"Imagen 3 returned no image for: {filename}")

        dest.write_bytes(response.generated_images[0].image.image_bytes)
        return dest
