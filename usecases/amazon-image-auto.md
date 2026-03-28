# Amazon Image Auto

You have a physical product but no professional studio, no photographer, and no 3D artist. Shooting every angle, every lifestyle scene, and every Amazon A+ banner manually takes days and costs thousands. This workflow turns a handful of raw product photos into a full Amazon listing image suite — automatically.

Upload photos from multiple angles. OpenClaw uses Google Gemini Vision to understand the product's geometry and surface details, then calls Google Imagen 3 to render it from any angle, drop it into real lifestyle scenes, and produce every image format Amazon requires.

## What It Does

- **3D Product Understanding**: Upload 3–8 photos of your product from different angles; Gemini Vision reconstructs a conceptual 3D model from the visual geometry
- **Angle-on-Demand Rendering**: Request any camera angle — front, 45°, overhead, hero — and Imagen 3 generates a photorealistic render
- **Lifestyle Scene Composition**: Place your product in curated real-world environments (kitchen counter, desk setup, outdoor table, gym bag) with natural lighting and shadows
- **Amazon A+ Content Images**: Automatically produce the full A+ module set — hero image, infographic overlay, comparison chart background, lifestyle banner (1500×1500, 970×300, 2000×600)
- **Batch Export**: All images exported at correct Amazon resolution and aspect ratio, ready for Seller Central upload

## Pain Point

Amazon sellers know this pain: a product launch needs 7–10 main images + A+ content + variation shots. A studio shoot runs $500–2,000. A 3D render artist charges $200–800 per scene. This workflow cuts both to near zero — you need only your phone camera and an afternoon.

## Skills & APIs You Need

- **Google Gemini Vision API** — multi-image product understanding (`gemini-2.0-flash` or `gemini-2.5-pro`)
- **Google Imagen 3 API** — photorealistic image generation (via Google AI Studio or Vertex AI)
- OpenClaw file skill — local image upload and export
- Optional: Google Cloud Storage skill for batch asset management

> **API Access**: Both Gemini and Imagen 3 are available through [Google AI Studio](https://aistudio.google.com) (free tier available) or [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview) (pay-per-use).

## How to Set It Up

### Step 1: Prepare Your Product Photos

Shoot your product with your phone. You need at least 3 angles for reliable reconstruction:

```
Minimum set (3 photos):
- Front face
- Side profile (45° angle)
- Top-down / overhead

Recommended set (6–8 photos):
- Front, back, left side, right side
- 45° hero angle (most used for Amazon main image)
- Detail close-up (texture, ports, labels)
- Bottom / base (if relevant)
```

Plain background preferred (white wall, gray card) but not required — Gemini removes it automatically.

### Step 2: Upload and Analyze the Product

```text
I'm going to upload 6 photos of my product from different angles.
Analyze all of them together using Gemini Vision and extract:

1. Product shape and 3D geometry description
2. Surface material and texture (matte, glossy, fabric, metal, etc.)
3. Color palette (exact hex codes if possible)
4. Key product features and unique visual elements
5. Approximate dimensions ratio (height:width:depth)

Save this analysis as product-profile.json. I'll use it to generate images next.

Photos attached: [front.jpg, back.jpg, side-left.jpg, side-right.jpg, top.jpg, detail.jpg]
```

### Step 3: Generate Product Renders at Any Angle

```text
Using the product-profile.json I just created, generate the following product renders with Imagen 3:

1. Hero angle (45° front-right, eye level, pure white background)
2. Front face straight-on (white background, product centered)
3. 3/4 perspective view from above-left
4. Close-up detail shot highlighting [material/key feature]

For each image:
- Resolution: 2000×2000 px
- Background: pure white (#FFFFFF)
- Lighting: soft studio light from upper-left
- Shadow: subtle drop shadow at base
- Style: Amazon product photo, professional commercial photography

Save all renders to /product-renders/ folder.
```

### Step 4: Generate Lifestyle Scene Images

```text
Take my product from product-profile.json and place it into the following real lifestyle scenes using Imagen 3.
The product must look naturally integrated — correct scale, realistic shadows, proper perspective.

Scene 1: Modern kitchen counter, morning light, coffee and plants in background
Scene 2: Clean office desk with MacBook, notebook, and soft window light
Scene 3: Living room coffee table, cozy evening ambiance, warm lighting
Scene 4: Outdoor patio table, natural daylight, blurred garden background

For each scene:
- Resolution: 2000×2000 px
- Product in lower-right or center of frame (rule of thirds)
- Photorealistic style, not illustrated
- Target audience: premium home/lifestyle buyers

Save to /lifestyle-scenes/ folder.
```

### Step 5: Generate Amazon A+ Content Images

```text
Generate the full Amazon A+ content image set for my product using Imagen 3.
Use the product renders from /product-renders/ and lifestyle scenes from /lifestyle-scenes/.

Required outputs:

1. Main listing hero image
   - Size: 2000×2000 px (square)
   - White background, product fills 85% of frame
   - No text overlay

2. Feature infographic (Module 1 — comparison or feature callout)
   - Size: 970×600 px
   - Product on left, 3 key feature callouts on right
   - Clean sans-serif font, brand color from product palette
   - White/light gray background

3. Lifestyle banner (Module 2 — full-width scene)
   - Size: 970×300 px
   - Horizontal lifestyle crop from Scene 1 or 2
   - Product prominent, text area on left third

4. Secondary lifestyle (Module 3)
   - Size: 300×400 px (portrait)
   - Single lifestyle scene, product in use

5. Brand story background (Module 4)
   - Size: 970×600 px
   - Abstract lifestyle background, no product, text placeholder overlay

Export all as PNG to /amazon-aplus/ folder.
```

### Step 6: Batch Quality Check and Export

```text
Review all generated images in /product-renders/, /lifestyle-scenes/, and /amazon-aplus/.

For each image, verify:
- Correct dimensions (flag any that don't match spec)
- Product clearly visible and not distorted
- Background is appropriate (white for renders, scene for lifestyle)
- No artifacts, blurring, or AI-generation glitches

Create a QC report: image-qc-report.md
List: ✅ passed, ⚠️ needs regeneration, ❌ failed

For any flagged images, regenerate with adjusted prompt parameters.
```

## Full Automation Prompt (One-Shot)

For repeat use once you have a product profile:

```text
Amazon Image Auto — Full Run

Product: [product name]
Product profile: product-profile.json

Generate the complete Amazon image suite:
1. 4 white-background product renders (front, 45° hero, 3/4, detail)
2. 4 lifestyle scenes (kitchen, office, living room, outdoor)
3. Full A+ content set (5 images, correct Amazon dimensions)

Use Gemini Vision to maintain product accuracy across all generations.
Export everything to /output/[product-name]/ with subfolders:
  renders/, lifestyle/, amazon-aplus/

Generate image-manifest.json listing all files with dimensions and intended use.
```

## Amazon Image Specifications Reference

| Image Type | Dimensions | Format | Use |
|------------|-----------|--------|-----|
| Main listing image | 2000×2000 | JPEG/PNG | Primary product image |
| Additional images | 2000×2000 | JPEG/PNG | Gallery images 2–9 |
| A+ hero | 970×600 | JPEG/PNG | A+ Module comparison |
| A+ banner | 970×300 | JPEG/PNG | A+ full-width module |
| A+ portrait | 300×400 | JPEG/PNG | A+ sidebar image |
| A+ brand story | 970×600 | JPEG/PNG | Brand story module |

## Real World Example

```text
Seller: 6 photos of a stainless steel water bottle uploaded.

OpenClaw → Gemini Vision:
"Cylindrical product, 26cm tall, 7cm diameter. Brushed stainless finish,
matte navy blue powder coat on lower half. Bamboo screw cap.
Brand logo embossed on center. Color palette: #1B2A4A, #8B9DA7, #C4A882."

→ Imagen 3 generates:
- 4 clean white-background renders in 8 minutes
- 4 lifestyle scenes (product on kitchen counter with morning coffee,
  on gym bag, on office desk, on hiking trail rock)
- Full A+ set in correct dimensions

Total generation time: ~25 minutes
Cost: ~$0.40 in API calls
vs. Studio shoot: $800 + 2-week turnaround
```

## Key Insights

- **Angle diversity matters more than photo quality.** 3 blurry angles beat 1 perfect studio shot for Gemini's 3D understanding.
- **Save your product-profile.json.** Once generated, you can spin up infinite variations — seasonal scenes, color variants, bundle shots — without re-uploading photos.
- **Batch your scene requests.** Imagen 3 generation takes ~30–60 seconds per image; queuing all 10+ images in one prompt minimizes back-and-forth.
- **White background renders first, always.** Amazon requires a pure white background for the main image. Generate this first; it's the highest-stakes output.
- **Use the QC step.** AI image generation can introduce subtle distortions. The 5-minute QC check saves you from uploading broken images to Seller Central.

## Limitations & Workarounds

| Limitation | Workaround |
|-----------|-----------|
| Complex transparent/reflective products (glass bottles, mirrors) | Use 8+ photos, add "handle reflections carefully" to prompt |
| Very small products (jewelry, tiny components) | Include a scale reference object in one upload photo |
| Products with fine text/labels | Generate base render, then manually composite label in Photoshop |
| Imagen 3 API regional availability | Use VPN or Vertex AI endpoint if AI Studio is unavailable in your region |

## Related Links

- [Google AI Studio — Imagen 3](https://aistudio.google.com)
- [Google Vertex AI — Image Generation](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)
- [Amazon Seller Central Image Requirements](https://sellercentral.amazon.com/help/hub/reference/G1881)
- [Amazon A+ Content Guidelines](https://sellercentral.amazon.com/help/hub/reference/G202102730)
