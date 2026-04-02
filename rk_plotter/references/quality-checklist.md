# Quality Checklist — rk_plotter

Use this checklist before finalizing any figure script or exported image.

## A. Scientific Fit

- [ ] The figure answers a clearly stated scientific question
- [ ] The chosen chart type matches the task: comparison, trend, relationship, composition, distribution, or space
- [ ] Variables, units, transformations, and reference periods are explicit
- [ ] If the figure supports a claim, the annotation and uncertainty display match the underlying analysis

## B. Data Integrity

- [ ] Missing values, zeros, censored values, and outliers are handled deliberately
- [ ] Aggregation level is correct and not silently mixed across panels
- [ ] Group ordering is scientifically meaningful rather than arbitrary
- [ ] Shared axes or shared color scales are truly comparable across panels

## C. Visual Clarity

- [ ] The main pattern is visible within 3–5 seconds
- [ ] The figure is not overloaded with redundant encodings
- [ ] Labels are readable and unclipped
- [ ] Legends, colorbars, and annotations do not cover important data
- [ ] Font sizes, line widths, and marker sizes are consistent

## D. Statistical Honesty

- [ ] Error bars or ribbons are defined clearly (`SD`, `SE`, `CI`, credible interval, etc.)
- [ ] Raw observations are shown when hiding them would mislead interpretation
- [ ] Significance stars are not used as the sole scientific takeaway
- [ ] Multiple-comparison issues are addressed when many tests are shown
- [ ] Model fits are not presented as causal evidence unless the design supports it

## E. Color and Accessibility

- [ ] Palette choice matches variable type: categorical, sequential, diverging, or cyclic
- [ ] Adjacent categories remain distinguishable in grayscale or for color-vision deficiency
- [ ] No `jet`, `rainbow`, or red-green-only contrast is used
- [ ] Map colorbars and legends include interpretable labels and units

## F. Layout and Export

- [ ] Panel labels and subplot titles are consistent
- [ ] Multi-panel spacing is balanced
- [ ] SVG and PNG exports both render correctly
- [ ] Vector text remains editable where expected
- [ ] `plt.close(fig)` or equivalent cleanup is present in script workflows

## G. Final Sanity Checks

- [ ] The figure would still be understandable without the caption
- [ ] The caption would not need to apologize for the figure design
- [ ] A reviewer could reproduce the figure from the script and data paths
- [ ] The filename and output directory follow repository conventions
