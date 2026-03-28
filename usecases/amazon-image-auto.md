# Amazon Image Auto

You have a physical product but no professional studio, no photographer, and no 3D artist. Shooting every angle, every lifestyle scene, and every Amazon A+ banner manually takes days and costs thousands. This workflow turns a handful of raw product photos into a full Amazon listing image suite — automatically.

Built for **home decor sellers** — window film, curtain hardware, blinds, and similar products that are notoriously hard to photograph: transparent materials, small hardware accessories, and products whose value only becomes clear when shown installed in a real room.

Upload photos from multiple angles. OpenClaw uses Google Gemini Vision to understand the product's geometry and surface details, then calls Google Imagen 3 to render it from any angle, drop it into real home scenes, and produce every image format Amazon requires.

## What It Does

- **3D Product Understanding**: Upload 3–8 photos of your product from different angles; Gemini Vision reconstructs a conceptual 3D model including material properties (transparency, reflectance, texture)
- **Angle-on-Demand Rendering**: Request any camera angle — front, 45°, overhead, installed-on-window — and Imagen 3 generates a photorealistic render
- **Home Scene Composition**: Place your product in curated interior environments (bedroom window, living room curtain rail, bathroom glass door) with natural daylight and realistic shadows
- **Amazon A+ Content Images**: Automatically produce the full A+ module set — hero image, infographic overlay, before/after comparison, lifestyle banner (2000×2000, 970×300, 970×600)
- **Batch Export**: All images exported at correct Amazon resolution and aspect ratio, ready for Seller Central upload

## Pain Point

Home decor sellers face a double challenge: the product itself is often invisible in photos (window film is transparent, curtain hooks are tiny) and the value is only apparent when the product is shown *in use* in a beautiful room. Hiring a photographer to shoot a film installed on five window types, in three lighting conditions, costs $1,500+. This workflow generates the same shot variety in under an hour.

## Skills & APIs You Need

- **Google Gemini Vision API** — multi-image product understanding (`gemini-2.0-flash` or `gemini-2.5-pro`)
- **Google Imagen 3 API** — photorealistic image generation (via Google AI Studio or Vertex AI)
- OpenClaw file skill — local image upload and export
- Optional: Google Cloud Storage skill for batch asset management

> **API Access**: Both Gemini and Imagen 3 are available through [Google AI Studio](https://aistudio.google.com) (free tier available) or [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview) (pay-per-use).

## How to Set It Up

### Step 1: Prepare Your Source Images

The input requirements differ by product type:

**Window Film**
You only need **one flat design image** of the film pattern itself — no multi-angle shooting required. The AI will handle applying it to glass surfaces.

```
Required: film-pattern.jpg
  - Flat lay of the film on a white/light surface
  - Or a scan/digital file of the pattern
  - Shows the full repeat pattern, colors, and opacity level

Optional extras:
  - film-edge-detail.jpg (close-up of film edge/cut edge)
  - film-backlit.jpg (film held up to a light source, shows translucency)
```

**Curtain Hooks / Curtain Hardware**
Shoot from multiple angles since these are 3D objects:

```
Recommended set (5–6 photos):
  - Front face (flat-on, white background)
  - 45° hero angle
  - Side profile
  - Installed close-up (hook already on curtain rod, if possible)
  - Detail of clasp/finish (matte, brushed gold, chrome, etc.)
  - Scale reference (next to a coin or ruler)
```

Plain background preferred (white wall, gray card) but not required — Gemini removes it automatically.

### Step 2: Analyze the Product

**For Window Film:**

```text
I'm uploading the flat design image of my window film: film-pattern.jpg

Analyze this film image using Gemini Vision and extract:
1. Pattern description (geometric, floral, frosted, one-way privacy, etc.)
2. Opacity level (fully frosted / semi-transparent / light diffusion only)
3. Color palette and tint (hex codes)
4. Texture character (smooth, sandblasted look, holographic, etc.)
5. Recommended use case (privacy, UV blocking, decorative, office partition)

Save as product-profile.json. I will use this to generate window installation scenes.

Photo attached: [film-pattern.jpg]
```

**For Curtain Hooks / Hardware:**

```text
I'm uploading 5 photos of my curtain hooks from different angles.
Analyze all of them together using Gemini Vision and extract:

1. Shape and mechanism (clip-on, eyelet, pin-hook, ring, etc.)
2. Material and finish (brushed gold, matte black, chrome, plastic, etc.)
3. Color palette (hex codes)
4. Size estimate (small/medium/large relative to curtain rod)
5. Key selling feature (smooth glide, decorative cap, rust-proof, etc.)

Save as product-profile.json.

Photos attached: [front.jpg, angle.jpg, side.jpg, installed.jpg, detail.jpg]
```

### Step 3: Generate Product White-Background Renders

**Window Film — flat lay renders:**

```text
Using film-pattern.jpg and product-profile.json, generate white-background product renders with Imagen 3:

1. Flat lay — film sheet neatly laid on pure white surface, slight curl on one corner to show it's a film
2. Roll view — film partially unrolled, showing the pattern clearly
3. Close-up detail — macro shot of the film texture/pattern, 50% of frame
4. Edge detail — cut edge of film showing thinness, white background

For each image:
- Resolution: 2000×2000 px
- Background: pure white (#FFFFFF)
- Lighting: even, flat soft-box lighting (no harsh shadows — film needs to show pattern clearly)
- Style: clean Amazon product photo

Save to /product-renders/ folder.
```

**Curtain Hooks — 3D renders:**

```text
Using product-profile.json, generate white-background renders with Imagen 3:

1. Hero angle (45° front-right, eye level, 3–5 hooks arranged in a slight fan)
2. Single hook straight-on (fills 70% of frame)
3. Side profile showing hook depth and clasp mechanism
4. Lifestyle-adjacent: hooks already on a curtain rod, white background, curtain fabric partially visible

For each image:
- Resolution: 2000×2000 px
- Background: pure white (#FFFFFF)
- Lighting: soft studio light, slight specular highlight on metal finish
- Shadow: subtle drop shadow

Save to /product-renders/ folder.
```

### Step 4: Generate Home Scene Lifestyle Images

**Window Film — installed-on-glass scenes (core workflow):**

```text
I have my window film design: film-pattern.jpg
Generate photorealistic scenes showing this film already applied to glass windows.

The film texture and pattern from film-pattern.jpg must be accurately rendered on the glass surface.
Show the film's light-filtering / privacy effect realistically.

Scene 1: Bright living room, large floor-to-ceiling window, film covers lower 2/3 of glass,
          soft morning sunlight filtering through the film pattern, modern interior, blurred sofa in foreground

Scene 2: Bathroom window, frosted privacy film on small window above sink,
          natural daylight coming through, clean white tile walls, plant on windowsill

Scene 3: Home office / study, glass partition or door with decorative film,
          film pattern centered on glass, wooden desk and bookshelf visible through clear top section

Scene 4: Before/after split image — left half shows plain clear glass window, right half shows same window
          with film applied, same room, same lighting, dramatic transformation effect

For each scene:
- Resolution: 2000×2000 px
- Film pattern must match film-pattern.jpg exactly (color, opacity, repeat)
- Photorealistic interior photography style
- Warm, aspirational home atmosphere

Save to /lifestyle-scenes/ folder.
```

**Curtain Hooks — installed in room scenes:**

```text
Using product-profile.json, generate lifestyle scenes of the curtain hooks installed in real rooms.

Scene 1: Master bedroom — hooks on a curtain rod with linen curtains, soft morning backlight,
          hooks clearly visible, bed partially in frame, warm cozy atmosphere

Scene 2: Living room — floor-length velvet curtains hung on hooks, golden hour light,
          hooks at eye level, parquet floor visible, plant in corner

Scene 3: Close-up hero — 5 hooks on rod with curtain fabric draped through them,
          out-of-focus background, hooks sharp and detailed, showing the finish and mechanism

Scene 4: Dining room / kitchen window — café curtains on hooks, natural daylight,
          herb plants and wooden cutting board in background, bright airy feel

For each scene:
- Resolution: 2000×2000 px
- Hooks must match finish from product-profile.json (color, material, size)
- Photorealistic interior photography style

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

## Full Automation Prompts (One-Shot)

### Window Film — Full Run

```text
Amazon Image Auto — Window Film

Product: [film product name, e.g. "Frosted Hexagon Privacy Window Film"]
Source image: film-pattern.jpg
Product profile: product-profile.json

Generate the complete Amazon image suite:

WHITE BACKGROUND RENDERS (4 images):
- Flat sheet on white surface, corner slightly curled
- Partially unrolled roll showing pattern
- Macro close-up of pattern texture
- Cut edge detail showing film thinness

INSTALLED LIFESTYLE SCENES (4 images):
- Living room floor-to-ceiling window, film on lower 2/3, morning light
- Bathroom privacy window, full coverage, clean white tile
- Home office glass partition, film centered
- Before/after split: clear glass vs film-applied, same room

AMAZON A+ SET (5 images per spec):
- 2000×2000 main hero (flat lay on white)
- 970×600 feature infographic (UV% + privacy + easy install callouts)
- 970×300 lifestyle banner (living room scene, horizontal crop)
- 300×400 portrait (bathroom scene)
- 970×600 brand story (soft abstract room background)

Use film-pattern.jpg as the exact texture reference for all glass scenes.
Export to /output/[product-name]/ → renders/, lifestyle/, amazon-aplus/
Generate image-manifest.json with all file names, dimensions, and intended use.
```

### Curtain Hooks / Hardware — Full Run

```text
Amazon Image Auto — Curtain Hardware

Product: [hook product name, e.g. "Brushed Gold C-Ring Curtain Hooks, Set of 10"]
Product profile: product-profile.json

Generate the complete Amazon image suite:

WHITE BACKGROUND RENDERS (4 images):
- 5 hooks fanned out, 45° hero angle
- Single hook front-on, fills 70% of frame
- Side profile showing depth and clasp
- 5 hooks on curtain rod, white background, fabric edge visible

INSTALLED LIFESTYLE SCENES (4 images):
- Master bedroom: linen curtains on rod with hooks, soft morning backlight
- Living room: floor-length velvet curtains, golden hour light
- Macro hero: hooks on rod with draped fabric, sharp detail, blurred background
- Dining / kitchen: café curtains, bright natural light, airy feel

AMAZON A+ SET (5 images per spec):
- 2000×2000 main hero (fan arrangement, white background)
- 970×600 feature infographic (material + finish + load capacity callouts)
- 970×300 lifestyle banner (bedroom scene, horizontal crop)
- 300×400 portrait (macro hero close-up)
- 970×600 brand story (soft curtain fabric abstract background)

Export to /output/[product-name]/ → renders/, lifestyle/, amazon-aplus/
Generate image-manifest.json with all file names, dimensions, and intended use.
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

## Real World Examples

### Window Film Example

```text
Seller uploads: geometric hexagon frosted film pattern image (film-pattern.jpg)

OpenClaw → Gemini Vision:
"Semi-transparent frosted film with repeating hexagon geometric pattern.
Opacity: ~60% light transmission. Slight bluish-white tint.
Pattern repeat: ~8cm hexagon. Effect: privacy + decorative, diffused light."

→ Imagen 3 generates:
- 4 flat-lay white background renders (flat sheet, rolled, close-up, edge)
- Scene 1: Living room floor-to-ceiling window with film on lower half, morning sun
  diffusing through hexagon pattern → warm, privacy-protected look
- Scene 2: Bathroom window with full frosted coverage → clean, modern privacy
- Scene 3: Home office glass partition with film pattern on center panel
- Scene 4: Before/after split → clear glass vs. film-applied, same room
- Full A+ set with infographic showing UV blocking % and installation steps

Total generation time: ~30 minutes
Cost: ~$0.50 in API calls
vs. Hiring photographer + room staging: $1,200+ and 3-day shoot
```

### Curtain Hook Example

```text
Seller uploads: 5 photos of brushed gold C-ring curtain hooks

OpenClaw → Gemini Vision:
"C-ring style curtain hook. Brushed gold finish, matte sheen.
Ring diameter ~3.5cm. Smooth glide surface on inside of ring.
Material: zinc alloy. Color: #B8960C warm brushed gold."

→ Imagen 3 generates:
- 4 white-background renders (fan arrangement, single close-up, side profile, on-rod preview)
- Scene 1: Master bedroom, linen curtains on gold hooks, morning backlight
- Scene 2: Living room, floor-length velvet curtains, hooks at eye level
- Scene 3: Macro close-up hero, 5 hooks on rod, blurred fabric background
- Scene 4: Dining area, café curtains, bright window light

Total generation time: ~20 minutes
Cost: ~$0.35 in API calls
```

## Key Insights

- **Window film: one design image is enough.** Unlike solid products, you don't need multiple angles — the AI computes light transmission and installs the texture on glass geometry automatically.
- **The "before/after" scene sells the product.** For window film, the split-image showing a plain window vs. the film-applied result is consistently the highest-converting A+ image. Always generate this.
- **For small hardware (curtain hooks), scale context is everything.** Always include a scene with the hooks already on a rod with fabric — buyers can't judge size from a white-background shot alone.
- **Save your product-profile.json.** Once generated, you can spin up infinite variations — new room styles, seasonal scenes, different curtain colors — without re-uploading photos.
- **Batch your scene requests.** Imagen 3 generation takes ~30–60 seconds per image; queuing all scenes in one prompt minimizes back-and-forth.
- **White background renders first, always.** Amazon requires a pure white background for the main image. Generate this first; it's the highest-stakes output.

## Limitations & Workarounds

| Limitation | Workaround |
|-----------|-----------|
| Window film pattern doesn't render accurately on glass | Add "tile the exact pattern from the reference image across the glass surface" to prompt; increase pattern description detail in product-profile.json |
| Film opacity looks wrong (too opaque or too transparent) | Specify exact light transmission percentage in prompt: "60% light passes through, diffused, not frosted completely" |
| Curtain hooks too small to see detail in lifestyle scenes | Generate a dedicated close-up macro scene + use the lifestyle scene only for context shots |
| Metal finish (gold/chrome) looks flat or wrong color | Add "brushed [metal type] with directional grain highlights, warm specular reflection" to the render prompt |
| Products with fine text/brand labels | Generate base render, then manually composite label in Photoshop |
| Imagen 3 API regional availability | Use VPN or Vertex AI endpoint if AI Studio is unavailable in your region |

## Related Links

- [Google AI Studio — Imagen 3](https://aistudio.google.com)
- [Google Vertex AI — Image Generation](https://cloud.google.com/vertex-ai/generative-ai/docs/image/overview)
- [Amazon Seller Central Image Requirements](https://sellercentral.amazon.com/help/hub/reference/G1881)
- [Amazon A+ Content Guidelines](https://sellercentral.amazon.com/help/hub/reference/G202102730)
