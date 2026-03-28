import asyncio
import json
import os
import uuid
from pathlib import Path

from fastapi import FastAPI, File, Form, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
from starlette.responses import StreamingResponse

from services.detector import ProductDetector
from services.generator import ImageGenerator

app = FastAPI(title="Amazon Image Auto", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
OUTPUT_DIR = Path("output")
UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

app.mount("/output", StaticFiles(directory="output"), name="output")
app.mount("/static", StaticFiles(directory="static"), name="static")


def _resolve_key(request_key: str | None) -> str:
    """Use key from request first, fall back to environment variable."""
    key = (request_key or "").strip() or os.environ.get("GOOGLE_API_KEY", "")
    if not key:
        raise HTTPException(
            status_code=400,
            detail="Google API Key 未提供。请在页面输入框中填写，或设置 GOOGLE_API_KEY 环境变量。",
        )
    return key


@app.get("/")
async def index():
    return FileResponse("static/index.html")


@app.post("/api/analyze")
async def analyze(
    files: list[UploadFile] = File(...),
    api_key: str = Form(default=""),
):
    """Upload product images → Gemini Vision detects type and extracts profile."""
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded")

    key = _resolve_key(api_key)

    session_id = str(uuid.uuid4())[:8]
    session_upload_dir = UPLOAD_DIR / session_id
    session_upload_dir.mkdir(exist_ok=True)

    saved_paths = []
    for f in files:
        if not f.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail=f"{f.filename} is not an image")
        dest = session_upload_dir / f.filename
        dest.write_bytes(await f.read())
        saved_paths.append(str(dest))

    detector = ProductDetector(api_key=key)
    profile = await detector.analyze(saved_paths)
    profile["session_id"] = session_id

    profile_path = session_upload_dir / "product-profile.json"
    profile_path.write_text(json.dumps(profile, ensure_ascii=False, indent=2))

    return JSONResponse(profile)


@app.get("/api/generate/{session_id}")
async def generate(
    session_id: str,
    api_key: str = Query(default=""),
):
    """Stream image generation progress via SSE."""
    profile_path = UPLOAD_DIR / session_id / "product-profile.json"
    if not profile_path.exists():
        raise HTTPException(status_code=404, detail="Session not found. Run /api/analyze first.")

    key = _resolve_key(api_key)
    profile = json.loads(profile_path.read_text())
    output_dir = OUTPUT_DIR / session_id
    output_dir.mkdir(exist_ok=True)

    generator = ImageGenerator(api_key=key)

    async def event_stream():
        try:
            async for event in generator.generate(profile, output_dir):
                yield f"data: {json.dumps(event)}\n\n"
                await asyncio.sleep(0)
        except Exception as e:
            yield f"data: {json.dumps({'type': 'error', 'message': str(e)})}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.get("/api/results/{session_id}")
async def results(session_id: str):
    """Return all generated images for a session."""
    output_dir = OUTPUT_DIR / session_id
    if not output_dir.exists():
        raise HTTPException(status_code=404, detail="No results for this session")

    manifest_path = output_dir / "image-manifest.json"
    if manifest_path.exists():
        return JSONResponse(json.loads(manifest_path.read_text()))

    files = []
    for f in sorted(output_dir.glob("**/*.png")):
        files.append({"filename": f.name, "url": f"/output/{session_id}/{f.name}", "folder": f.parent.name})
    return JSONResponse({"files": files})


@app.get("/api/download/{session_id}")
async def download(session_id: str):
    """Download all results as a zip archive."""
    import tempfile
    import zipfile

    output_dir = OUTPUT_DIR / session_id
    if not output_dir.exists():
        raise HTTPException(status_code=404, detail="No results for this session")

    tmp = tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in output_dir.glob("**/*.png"):
            zf.write(f, arcname=f.relative_to(output_dir))
        manifest = output_dir / "image-manifest.json"
        if manifest.exists():
            zf.write(manifest, arcname="image-manifest.json")
    tmp.close()

    return FileResponse(
        tmp.name,
        media_type="application/zip",
        filename=f"amazon-images-{session_id}.zip",
    )
