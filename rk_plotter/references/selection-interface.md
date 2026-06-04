# Selection Interface: When Users Want to Choose

This skill exposes a selection interface for interactive visual choices. Use it when
the user says they want to choose, pick, compare, decide, list, browse, or select any
of these before plotting:

- figure type or image type;
- template or template family;
- mode within a template family;
- color scheme, palette, color family, or colormap;
- legend or colorbar plan;
- figure size or journal column width;
- map projection, extent, inset, coastline/border layer, or colorbar position;
- statistical display choices such as confidence interval, error bar, fit line,
  significance marks, reference line, panel labels, or value annotations.

## Required behavior

When triggered, stop before generating or editing the plotting script. Present the
complete available choices, then ask the user to choose. Do not infer silently and do
not start plotting until the user has selected or explicitly delegates the choice.

Recommended command:

```bash
python scripts/list_options.py --format markdown
```

If the user only wants a subset, pass one or more sections:

```bash
python scripts/list_options.py --section templates --section palettes --format markdown
```

## Template source boundary

All choices must come from this skill package:

- templates and modes: `references/template-index.md` plus `templates/*.py`;
- palette families and display plans: `scripts/list_options.py` built-in catalog;
- high-fidelity constraints: `references/high-fidelity-policy.md`;
- style and output rules: `references/style-contract.md`.

Never add plotting scripts from the current working directory to the choice list unless
the user explicitly asks to import them into the skill template library. Project scripts
are user material, not skill templates.

## Default question shape

Use concise grouped lists:

1. Figure/template options.
2. Palette/color-scheme options.
3. Legend/colorbar and statistical-display options when relevant.

Then ask for the minimum choices needed to proceed. If there are many templates, list all
template IDs and modes first, then recommend the nearest 2-3 based on the user's data or
scientific question.
