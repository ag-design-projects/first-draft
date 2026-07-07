# Brand Extraction

Use this reference when converting brand guidelines into presentation rules.

## Extract

- Brand identity: brand name, approved logo files, clear-space rules, prohibited treatments.
- Color system: primary, secondary, accent, neutral, semantic colors, contrast constraints, gradients only if explicitly allowed.
- Typography: font families, weights, hierarchy, case rules, line-height, fallback fonts.
- Template files: light/dark variants, master names, slide layout names, and layout capacity.
- Layout: slide size, margins, grid, title placement, footer/page numbers, section divider style, whitespace density.
- Imagery: photography style, illustration style, icon style, data visualization style, texture or motion rules.
- Charts: palette order, axis and label treatment, annotations, callouts, table styling.
- Voice: tone, vocabulary, capitalization, claim style, citation style.
- Accessibility: contrast, minimum type sizes, color-blind-safe chart choices.

## Normalize To Brand Tokens

Use this minimal shape in deck specs:

```json
{
  "brand": {
    "name": "Brand Name",
    "slug": "brand-name",
    "templates": {
      "light": "sources/brands/brand-name/templates/template-light.pptx",
      "dark": "sources/brands/brand-name/templates/template-dark.pptx"
    },
    "catalogs": {
      "light": "sources/brands/brand-name/layouts-light.json",
      "dark": "sources/brands/brand-name/layouts-dark.json"
    },
    "colors": {
      "primary": "#111111",
      "secondary": "#666666",
      "accent": "#0A66CC",
      "background": "#FFFFFF",
      "text": "#111111"
    },
    "fonts": {
      "heading": "Helvetica Neue",
      "body": "Helvetica Neue",
      "default_style": "regular"
    },
    "layout": {
      "ratio": "16:9",
      "margin": 0.55,
      "footer": true
    },
    "tone": ["clear", "executive", "evidence-led"]
  }
}
```

## Brand Compliance Checks

- Logo is never stretched, cropped, recolored, or placed on low-contrast backgrounds.
- Accent colors support hierarchy; they do not dominate the deck unless brand rules say so.
- Typography hierarchy is consistent across title, subtitle, body, charts, captions, and footers.
- Visual style matches the brand's stated category: corporate, editorial, product, investor, workshop, or creative.
- If a brand guideline is incomplete, state the gap and choose conservative defaults.
- For retained PowerPoint templates, run `scripts/sanitize_pptx.py` before storing them if they contain client/private naming that should not appear in generated output.
- For PowerPoint templates, run `scripts/catalog_layouts.py` and store both JSON and Markdown catalogs beside the brand.
- Mark blank layouts as fallback-only; storyboard options should prefer designed template layouts with real structure.
- For the bundled neutralized templates, Helvetica Neue regular is the default; remove inherited italic defaults.
- Do not preserve source-brand names in sanitized template text, metadata, filenames, or output summaries.
