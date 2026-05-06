# SVG Header Set

This folder contains a small set of scalable SVG headers for the manuscript.

Files:
- `manuscript-title.svg` — large manuscript title banner (editable text, color variables).
- `act-header.svg` — act-level header for "ACT I", "ACT II", etc.
- `chapter-header.svg` — chapter number + title layout.
- `scene-header.svg` — compact ribbon-style scene header.
- `section-divider.svg` — thin decorative divider with center ornament.
- `subheader.svg` — small italic subheader with dot ornament.

Quick customization:
- Open any `.svg` in a text editor and edit the visible text nodes (e.g. "Chain Weapon Story", "ACT I").
- Change colors by editing the CSS variables near the top (e.g. `--accent`, `--fg`).
- SVGs are sized with `viewBox` so they scale cleanly; adjust `width`/`height` attributes if you need fixed pixel sizes.

If you want additional variants (dark/light, ornate, minimal) or exports as PNG/PDF at specific sizes, tell me which styles and sizes to generate.
