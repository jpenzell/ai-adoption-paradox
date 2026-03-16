# Data Access

The Stack Overflow Developer Survey data is publicly available but not included in this repository due to file size.

## Download Instructions

1. Go to https://survey.stackoverflow.co/datasets
2. Download the annual survey results for 2023, 2024, and 2025
3. Extract the CSV files and place them inside the repo at:

```
data/2023/survey_results_public.csv
data/2024/survey_results_public.csv
data/2025/survey_results_public.csv
```

These paths match what `analysis/config.py` expects. Run from the repo root.

## Verify Your Downloads

After downloading, verify your files match the CSVs used in this analysis using the SHA-256 checksums in `docs/DENOMINATORS.md`.

On macOS/Linux:
```bash
shasum -a 256 data/2025/survey_results_public.csv | cut -c1-16
# Should output: 2d1f65308877282e
```

On Windows (PowerShell):
```powershell
(Get-FileHash data\2025\survey_results_public.csv -Algorithm SHA256).Hash.Substring(0,16).ToLower()
# Should output: 2d1f65308877282e
```

If your hashes don't match, Stack Overflow may have released an updated version of the CSV. The analysis should still run correctly, but minor count differences are expected.
