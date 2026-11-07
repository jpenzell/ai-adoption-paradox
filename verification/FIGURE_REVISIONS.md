# Figure wording revisions

Completed 2026-11-07T08:54:45.336421+00:00 by Codex subagent /root/finish_figures.

Only two research figures and their plot-generation text were revised:

- `outputs/sentiment_2026/four_year_context.png`: replaced the directional title with a neutral description of separate survey samples. Added a title line stating that 2026 measures differ, retained the instrument-redesign marker, and clarified the classified-use-response denominator label. The caption states that sample and measurement changes limit trend interpretation and that the new trust question is omitted from the earlier accuracy-trust scale.
- `outputs/sentiment_2026/stance_gradient_2025_vs_2026.png`: replaced the claim that the floor rose with a neutral two-sample comparison title. The caption states that differences combine sample and measurement changes, names the distinct daily-use definitions, and limits the Wilson intervals to the observed sample. The caption was placed below the axis with reserved space to prevent overlap.

Both figures were regenerated with Matplotlib from the retained CSV files of the same names. The source script `analysis/sentiment_deep_dive.py` contains the matching title, legend, and annotation repairs for future runs. No model, table-generation code, counts, rates, intervals, or plotted values were changed. The original uploaded review ZIP remains untouched.

Verification: all 50 CSV/JSON output files retained identical SHA-256 hashes before and after these repairs. The edited analysis script passes Python syntax parsing. Both final PNGs were visually inspected; the titles, legends, captions, and interval marks are readable and not clipped. The cross-year caption spacing was corrected after the first rendering pass.

These are presentation repairs, not independent recomputation of historical data or model estimates. See the separate raw-data verification and model-rerun reports for those scopes.
