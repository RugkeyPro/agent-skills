# Quality Checklist

- The plot type matches the scientific question.
- Random data has been replaced before final delivery, or the figure is explicitly labeled as a template/demo.
- Axis labels include units and transformations.
- Legends and colorbars explain all encodings.
- Colors avoid `jet`, `rainbow`, and red-green-only contrast.
- Statistical annotations state the comparison or interval being shown.
- PNG, PDF, and SVG exports are present when final output is requested.
- SVG text remains editable because `svg.fonttype` is `none`.
- No `plt.show()` remains in production scripts; every figure is closed after saving.
