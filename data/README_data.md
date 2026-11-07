# Data Access

The Stack Overflow Developer Survey data is publicly available but not included in this repository due to file size.

## Download Instructions

From the research root, run `python3 analysis/fetch_data.py`. This uses the Python standard library and verifies package-specified hashes before installing files. URLs and hashes below are inherited from the package; current source availability and provenance must be checked separately.


Stack Overflow now distributes the public CSVs from the GitHub archive at
https://github.com/StackExchange/Survey under `packages/archive/<year>/`
(Git LFS). The older survey.stackoverflow.co/datasets zips are no longer served.

File names differ by year:

| Year | Results file in the archive | Schema file |
|---|---|---|
| 2026 | `survey_results_public.csv` | `survey_results_schema.csv` |
| 2023, 2024, 2025 | `results.csv` | `schema.csv` |

Place them inside the repo as:

```
data/2026/survey_results_public.csv
data/2025/survey_results_public.csv
data/2024/survey_results_public.csv
data/2023/survey_results_public.csv
```

These paths match what `analysis/config.py` expects. Run from the repo root.

## Verify Your Downloads

`python analysis/verify_data.py` checks every file. Expected SHA-256:

| Year | SHA-256 | Rows |
|---|---|---|
| 2026 | `ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c` | 30,903 |
| 2025 | `2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa` | 49,191 |
| 2024 | `7f2c2dbf6989d00b80a7351de4bb3af4b52b21cc52d5c947891bbc4f4e5cbe49` | 65,437 |
| 2023 | `828874a3cf0fa1bbb4c3da6a87e5822b8563bbc04b21f9869479480dbcff410c` | 89,184 |

If a hash does not match, stop and resolve the discrepancy. Do not silently substitute changed data or presume differences will be minor. The downloader preserves existing mismatched files by default.
