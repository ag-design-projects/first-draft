---
name: first-draft
description: Turn uploaded research and brand guidelines into storyboard-first branded presentation drafts. Use when Codex needs to analyze research files, extract or reuse brand presentation rules, propose multiple narrative structures from consulting and design-storytelling frameworks, then generate editable decks for PowerPoint, Figma Slides, Google Slides-compatible import, or HTML/PDF.
---

# First Draft

## Overview

Use this skill to convert uploaded research into a branded presentation without jumping straight to slides. Always produce storyboard options first, let the user choose one or more narrative structures and output formats, then generate the requested artifacts.

## Workflow

1. Confirm inputs: research files, audience, presentation objective, deadline or length constraints, output formats, and whether the deck is for executive decision, sales, education, workshop, or readout.
2. Resolve brand source:
   - Run `scripts/brand_store.py list` to show retained brands.
   - Ask whether to use an existing brand, add a new uploaded brand guideline package, or delete an obsolete brand.
   - Store retained brand files in `sources/brands/<brand-slug>/` with the manifest maintained by `brand_store.py`.
   - Prefer the retained `editorial-research` brand when the user asks for the bundled neutralized presentation templates.
   - Use `sources/brands/editorial-research/templates/editorial-slides-template-light.pptx` or `sources/brands/editorial-research/templates/editorial-slides-template-dark.pptx` as the default PowerPoint template when no other template is selected.
3. Extract source notes:
   - Run `scripts/extract_research.py <files...> --out <project>/research-notes.json`.
   - Preserve source file names, page/slide numbers when available, claims, evidence, and gaps.
4. Read only the needed references:
   - `references/brand-extraction.md` when extracting brand rules.
   - `references/narrative-frameworks.md` when choosing story options.
   - `references/deck-spec.md` before generating artifacts.
5. Propose 2-4 storyboard options. Each option must include:
   - Narrative name and framework mix.
   - Best-fit use case and tradeoff.
   - 6-12 slide outline with action titles.
   - Template variant, `layout_id`, and image/visual placeholder for each slide.
   - Evidence map and known assumptions.
   - Cast-to-capacity check: if a beat exceeds every suitable layout, split it into multiple slides or move a quote/stat/image to its own slide.
6. Stop and ask the user to select one or more storyboards, template variants, and output formats.
7. Generate selected outputs:
   - PowerPoint: create a normalized deck spec JSON and run `scripts/render_pptx.py`.
     - Requires `python-pptx>=1.0.2`; install with `python -m pip install -r requirements.txt` if missing.
   - Google Slides-compatible: generate the same `.pptx` for import unless a true Google Slides connector is available.
   - HTML/PDF: run `scripts/render_html_deck.py`; tell the user to print/export the HTML to PDF if no browser automation is available.
   - Figma Slides: use the Figma deck generation tool when available. Pass a self-contained prompt with objectives, outline, style, palette, brand rules, and theme.
8. Validate before delivery: check slide count, brand token application, source mapping, action titles, text density, and output file readability.

## Narrative Rules

- Let the uploaded research choose the story. Do not force a favorite framework.
- Prefer a hybrid model: consulting frameworks for argument logic, and design-storytelling frameworks for audience journey, emotion, pacing, and visual experience.
- Use `$consulting` for business structure when the task involves strategy, market analysis, operations, finance, transformation, M&A, or executive recommendations.
- Use the book-inspired patterns in `references/narrative-frameworks.md` for narrative arc, persona, emotional journey, sensory pacing, attention, comprehension, and experience design.
- Make every slide title an action title that states the "so what", not a topic label.
- Never invent evidence. Mark unsupported claims as assumptions or open questions.

## Output Standards

- Decks must be editable, not screenshots of text.
- Use one idea per slide. Split dense content.
- Keep chart and table specs explicit enough that another agent can rebuild them.
- Maintain brand compliance for colors, typography, logo use, layout density, imagery, icons, and tone.
- Keep speaker notes or appendix notes for source citations when the visible slide would become cluttered.
- For Figma Slides, include all relevant context in the tool request because the tool does not retain chat history.
- Use Helvetica Neue as the default font family for the bundled neutralized templates. Do not use italic as the default style.
- Do not mention source-template brand names in generated assets, slide text, metadata, file names, or user-facing summaries.
- Build PowerPoint outputs from the selected template so the template layouts remain visible in PowerPoint Home > Layout.
- Do not use a blank slide layout when a relevant existing template layout is available. Blank layout is a last resort only.

## File Conventions

- Retained brands: `sources/brands/<brand-slug>/`
- Project working files: ask the user for a project folder, or create a timestamped folder under the current workspace.
- Deck spec: `deck-spec.json`
- PowerPoint output: `<deck-slug>.pptx`
- HTML output: `<deck-slug>.html`
