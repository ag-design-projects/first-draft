# Deck Spec

Use this schema as the normalized handoff between research, storyboard, and renderers.

```json
{
  "title": "Deck title",
  "subtitle": "Optional subtitle",
  "audience": "Who will see this",
  "objective": "Decision or outcome the deck should drive",
  "output_targets": ["pptx", "html"],
  "brand": {
    "name": "Brand",
    "slug": "editorial-research",
    "theme": "light",
    "template": "sources/brands/editorial-research/templates/editorial-slides-template-light.pptx",
    "layout_catalog": "sources/brands/editorial-research/layouts-light.json",
    "colors": {
      "primary": "#111111",
      "secondary": "#666666",
      "accent": "#0A66CC",
      "background": "#FFFFFF",
      "text": "#111111"
    },
    "fonts": {
      "heading": "Aptos Display",
      "body": "Aptos"
    }
  },
  "narrative": {
    "name": "Executive recommendation",
    "frameworks": ["SCQ", "Pyramid Principle", "Narrative arc"],
    "rationale": "Why this structure fits the research"
  },
  "slides": [
    {
      "title": "Action title with the so what",
      "role": "cover | agenda | section | insight | chart | roadmap | recommendation | appendix | closing",
      "layout_id": "slideLayout1",
      "body": ["Concise bullet or paragraph"],
      "visual": {
        "type": "none | metric | chart | table | timeline | image | quote | diagram",
        "description": "What the visual should show"
      },
      "image": {
        "description": "Labeled image placeholder, or none - typographic",
        "source": "uploaded image, generated image, stock search, or none"
      },
      "evidence": [
        {
          "source": "research.pdf",
          "locator": "page 4",
          "claim": "Claim supported by the source"
        }
      ],
      "notes": "Speaker or builder notes"
    }
  ],
  "assumptions": ["Items not directly proven by uploaded research"],
  "gaps": ["Questions the user may need to answer"]
}
```

## Required Quality Bar

- Every non-cover slide needs a source-backed claim or an explicit assumption.
- Use action titles, not labels like "Market Overview".
- Keep body text short enough to fit a real slide.
- Give visuals a clear purpose and enough detail to build.
- Put source detail in notes when visible citations would crowd the slide.
- Every slide should carry a `layout_id` from the selected brand catalog before rendering.
- Pick a nonblank existing template layout whenever possible. Use a blank layout only when no relevant designed layout exists.
- Never overfill a layout. If the content exceeds the catalog capacity, split the slide.
- Use plain high-contrast text backgrounds unless the chosen template layout is explicitly designed for full-bleed imagery.
- Left-align body text. Avoid centered body copy except for cover, divider, quote, or closing slides.
- Use brand-token colors only.
- Use ASCII hyphens only; do not use em dashes or en dashes.
- For bundled neutralized templates, use Helvetica Neue regular by default and avoid italic unless explicitly requested.
- Do not mention source-template brand names anywhere in generated output.
