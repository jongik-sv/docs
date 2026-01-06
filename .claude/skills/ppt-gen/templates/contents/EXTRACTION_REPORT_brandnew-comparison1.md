# Content Template Extraction Report

**Template ID:** brandnew-comparison1  
**Extraction Date:** 2026-01-07  
**Status:** SUCCESS ✓

---

## Source Information

| Field | Value |
|-------|-------|
| **Source File** | brandnew.pptx |
| **Slide Index** | 7 (slide 8, 0-based) |
| **Source Aspect Ratio** | 16:9 |
| **Dimensions** | 1920x1080 px |

---

## Design Intent

- **Primary Intent:** `comparison-2col-image`
- **Secondary Intents:** 
  - `comparison-2col`
  - `grid-2col`
  - `image-layout`
- **Quality Score:** 8.5/10.0
- **Visual Balance:** Symmetric
- **Information Density:** Medium

---

## Extracted Content

### Shapes (6 total)

#### Left Column Group
| ID | Name | Type | Position | Size |
|----|------|------|----------|------|
| shape-0 | Left Background Panel | rectangle | (1.1%, 8.4%) | 47.7% × 75.8% |
| shape-2 | Left Content Area | rectangle | (3.9%, 14.5%) | 42.6% × 46.7% |
| shape-4 | Left Title | textbox | (16.1%, 67.3%) | 18.2% × 9.0% |

#### Right Column Group
| ID | Name | Type | Position | Size |
|----|------|------|----------|------|
| shape-1 | Right Background Panel | rectangle | (51.2%, 8.4%) | 47.5% × 75.8% |
| shape-3 | Right Content Area | rectangle | (53.5%, 14.5%) | 42.6% × 46.7% |
| shape-5 | Right Title | textbox | (65.8%, 67.3%) | 18.2% × 9.0% |

### Groups (3 total)

1. **comparison-left** - Left panel assembly
   - Members: shape-0, shape-2, shape-4
   - Bounding box: 1.1% × 8.4% → 47.7% × 75.8%

2. **comparison-right** - Right panel assembly
   - Members: shape-1, shape-3, shape-5
   - Bounding box: 51.2% × 8.4% → 47.5% × 75.8%

3. **comparison-full** - Complete comparison layout
   - Members: all 6 shapes
   - Bounding box: 0% × 0% → 100% × 100%

---

## Spacing & Alignment

### Global Gaps
- **Column Gap:** 3.3% (between left and right panels)
- **Row Gap:** 5.8% (between background and content area)

### Spatial Relationships
- Left and right panels: **adjacent-horizontal** with 3.3% gap, **top-aligned**
- Content areas: **adjacent-horizontal** with 6.9% gap, **top-aligned**
- Title boxes: **adjacent-horizontal** with 29.4% gap, **center-aligned**

---

## Theme Colors

| Semantic | Usage |
|----------|-------|
| **accent** | Background panels (shape-0, shape-1) |
| **light** | Content area backgrounds (shape-2, shape-3) |
| **dark_text** | Title text (shape-4, shape-5) |

---

## Zone Detection Summary

### Content Zone
- **Top Boundary:** 20% (0% of content zone)
- **Bottom Boundary:** 95% (75% of content zone)
- **Left Boundary:** 3% (0% of content zone)
- **Right Boundary:** 97% (100% of content zone)

### Title/Footer Exclusion
- **Top Excluded:** 0% - 20% (placeholder & section title)
- **Bottom Excluded:** 95% - 100% (footer area)

---

## Output Files

### YAML Template
**Path:** `.claude/skills/ppt-gen/templates/contents/templates/brandnew-comparison1.yaml`  
**Size:** 5,678 bytes  
**Schema Version:** 2.0

### Thumbnail
**Path:** `.claude/skills/ppt-gen/templates/contents/thumbnails/brandnew-comparison1.png`  
**Size:** 1,689 bytes  
**Format:** PNG (320×180 px)

---

## Reusability

### Recommended Use Cases
- A vs B comparisons
- Before/After layouts
- Feature comparisons
- Side-by-side product comparisons
- Two-column image galleries

### Keywords
- 비교 (comparison)
- 2열 (two-column)
- 대조 (contrast)
- 좌우 (left-right)
- 이미지 비교 (image comparison)

---

## Validation

- ✓ All shapes extracted within content zone
- ✓ Zone filtering applied (title/footer excluded)
- ✓ Aspect ratios calculated for all shapes
- ✓ Semantic colors mapped from theme
- ✓ Spatial relationships documented
- ✓ Groups logically organized
- ✓ YAML schema v2.0 compliant
- ✓ Thumbnail generated

---

**Template Ready for Use:** YES  
**Next Steps:** The template can be used to generate similar comparison layouts in PowerPoint using the provided geometry, styling, and grouping information.
