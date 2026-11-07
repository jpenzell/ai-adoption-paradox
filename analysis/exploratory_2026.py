"""Exploratory 2026-only cuts. Not pre-specified; descriptive only.

Writes outputs/sentiment_2026/exploratory_*.csv. Run after
sentiment_deep_dive.py --year 2026. Every table uses the primary 2026
current-user sample (complete on use, stance, trust) and the stance labels
harmonized to 2025 vocabulary.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from config import CSV_2026
from sentiment_deep_dive import STANCE_ORDER, wilson_interval
from survey_2026 import prepare_2026

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "sentiment_2026"
OUT.mkdir(parents=True, exist_ok=True)

AIWORK_COLUMNS = [
    "AIWorkCurrentlyUse",
    "AIWorkExpectMore",
    "AIWorkExpectLess",
    "AIWorkDoNotPlanToUse",
    "AIWorkNotInWorkflow",
]


def count_items(series):
    return series.fillna("").apply(lambda s: 0 if s == "" else len(s.split(";")))


def share_table(frame, flag_column, label):
    rows = []
    for stance in STANCE_ORDER:
        cell = frame[frame["AISent"] == stance]
        successes = int(cell[flag_column].sum())
        low, high = wilson_interval(successes, len(cell))
        rows.append(
            {
                "favorable_stance": stance,
                "n": len(cell),
                f"{label}_rate": successes / len(cell) if len(cell) else float("nan"),
                "ci_low": low,
                "ci_high": high,
            }
        )
    return pd.DataFrame(rows)


def main():
    raw = pd.read_csv(CSV_2026, low_memory=False)
    data = prepare_2026(raw)
    users = data[
        data["AIUsageScore"].ge(2) & data["AISent"].notna() & data["AIAcc"].notna()
    ].copy()

    # 1. Next-year expectations across workflow parts (AIWork matrix).
    answered = users[users[AIWORK_COLUMNS].notna().any(axis=1)].copy()
    for column in AIWORK_COLUMNS:
        answered[f"n_{column}"] = count_items(answered[column])
    answered["any_expect_less"] = answered["n_AIWorkExpectLess"].gt(0).astype(int)
    answered["any_expect_more"] = answered["n_AIWorkExpectMore"].gt(0).astype(int)
    expectations = (
        answered.groupby("AISent")
        .agg(
            n=("Daily", "size"),
            any_expect_less=("any_expect_less", "mean"),
            any_expect_more=("any_expect_more", "mean"),
            mean_parts_expect_less=("n_AIWorkExpectLess", "mean"),
            mean_parts_expect_more=("n_AIWorkExpectMore", "mean"),
            mean_parts_currently_use=("n_AIWorkCurrentlyUse", "mean"),
            mean_parts_do_not_plan=("n_AIWorkDoNotPlanToUse", "mean"),
        )
        .reindex(STANCE_ORDER)
        .reset_index()
        .rename(columns={"AISent": "favorable_stance"})
    )
    expectations.to_csv(OUT / "exploratory_next_year_expectations_by_stance.csv", index=False)
    daily_only = answered[answered["Daily"] == 1]
    share_table(daily_only, "any_expect_less", "any_expect_less").to_csv(
        OUT / "exploratory_daily_users_expect_less_by_stance.csv", index=False
    )

    # 2. Control over the information the AI uses (KnowAgentTrust).
    control = users[users["KnowAgentTrust"].notna()]
    pd.crosstab(control["AISent"], control["KnowAgentTrust"], normalize="index").reindex(
        STANCE_ORDER
    ).reset_index().rename(columns={"AISent": "favorable_stance"}).to_csv(
        OUT / "exploratory_information_control_by_stance.csv", index=False
    )

    # 3. What people do before using AI output (AIWorkNext, multi-select).
    verify = users[users["AIWorkNext"].notna()].copy()
    options = sorted({o for cell in verify["AIWorkNext"] for o in cell.split(";")})
    for option in options:
        verify[option] = verify["AIWorkNext"].str.contains(option, regex=False).astype(int)
    verify.groupby("AISent")[options].mean().reindex(STANCE_ORDER).reset_index().rename(
        columns={"AISent": "favorable_stance"}
    ).to_csv(OUT / "exploratory_verification_behavior_by_stance.csv", index=False)
    verify["n"] = 1
    verify.groupby("AISent")["n"].sum().reindex(STANCE_ORDER).rename("n").reset_index().to_csv(
        OUT / "exploratory_verification_behavior_n.csv", index=False
    )

    # 4. Job satisfaction (0-10) and complacency driver.
    sat = users[users["JobSat"].notna()].copy()
    sat["low_satisfaction_0_to_4"] = sat["JobSat"].le(4).astype(int)
    sat["high_satisfaction_9_to_10"] = sat["JobSat"].ge(9).astype(int)
    satisfaction = (
        sat.groupby("AISent")
        .agg(
            n=("JobSat", "size"),
            mean_job_satisfaction=("JobSat", "mean"),
            low_satisfaction_0_to_4=("low_satisfaction_0_to_4", "mean"),
            high_satisfaction_9_to_10=("high_satisfaction_9_to_10", "mean"),
        )
        .reindex(STANCE_ORDER)
        .reset_index()
        .rename(columns={"AISent": "favorable_stance"})
    )
    satisfaction.to_csv(OUT / "exploratory_job_satisfaction_by_stance.csv", index=False)
    complacent = users[users["JobSatComplacent"].notna()]
    pd.crosstab(
        complacent["AISent"], complacent["JobSatComplacent"], normalize="index"
    ).reindex(STANCE_ORDER).reset_index().rename(columns={"AISent": "favorable_stance"}).to_csv(
        OUT / "exploratory_complacency_driver_by_stance.csv", index=False
    )

    print(expectations.round(3).to_string())
    print(satisfaction.round(3).to_string())
    print(f"Outputs written to: {OUT}")


if __name__ == "__main__":
    main()
