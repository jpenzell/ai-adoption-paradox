"""2026 Stack Overflow survey intake: column mapping to the v3.1.0 contract.

The 2026 survey redesigned all three core items used by the v3.1.0 analysis.
This module documents the mapping decisions in code; the rationale and the
pre-specified replication criteria are in docs/INTAKE_DECISIONS_2026.md.

Nothing here is applied to the 2025 run, which stays byte-identical.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

TOOL_TYPES = [
    "AI coding assistants or coding agents",
    "General-purpose AI chat tools",
    "AI agents or automated workflows",
    "Internal AI tools built by my company",
]
NO_USE = "I don’t use AI tools"  # curly apostrophe as shipped in the CSV
FREQ_COLUMNS = ["AIFreq_1", "AIFreq_2", "AIFreq_3", "AIFreq_4"]
FREQ_RANK = {"Daily": 4, "Weekly": 3, "Monthly or Infrequent": 2}

# Position-based harmonization of the six 2026 attitude options onto the
# six 2025 stance labels. Wording differs; see INTAKE_DECISIONS_2026.md.
STANCE_2026_TO_2025 = {
    "Very favorable": "Very favorable",
    "Somewhat favorable": "Favorable",
    "Neutral": "Indifferent",
    "Somewhat unfavorable": "Unfavorable",
    "Very unfavorable": "Very unfavorable",
    "Not sure": "Unsure",
}

# 2026 trust item is a reliance-scope question, not an accuracy Likert.
# This ordering is for display only; the models treat it as nominal.
TRUST_ORDER_2026 = [
    "I do not trust it for most work tasks",
    "I trust it for low-risk work tasks only",
    "I trust it when I can easily verify the output",
    "I trust it for many tasks, but not important work decisions",
    "I trust it for many tasks, including important work decisions",
    "Not sure / I do not use AI tools",
]
TRUST_SHORT_2026 = {
    "I do not trust it for most work tasks": "Not for most tasks",
    "I trust it for low-risk work tasks only": "Low-risk tasks only",
    "I trust it when I can easily verify the output": "When I can verify",
    "I trust it for many tasks, but not important work decisions": "Many tasks, not key decisions",
    "I trust it for many tasks, including important work decisions": "Incl. key decisions",
    "Not sure / I do not use AI tools": "Not sure",
}

HEAVY_DAILY = {"4+ hours/day"}


def classify_use(select_value):
    """Return (is_user, is_nonuser, contradictory) for a 2026 AISelect cell."""
    if pd.isna(select_value):
        return (False, False, False)
    text = str(select_value)
    has_tool = any(tool in text for tool in TOOL_TYPES)
    says_no = NO_USE in text
    return (has_tool and not says_no, says_no and not has_tool, has_tool and says_no)


def usage_score_2026(row):
    """4 = daily on any tool type, 3 = weekly max, 2 = monthly max, 0 = non-user."""
    is_user, is_nonuser, contradictory = classify_use(row["AISelect"])
    if contradictory:
        return np.nan  # excluded from the primary sample; see sensitivity note
    if is_nonuser:
        return 0.0
    if not is_user:
        return np.nan
    ranks = [FREQ_RANK.get(row[c], np.nan) for c in FREQ_COLUMNS]
    ranks = [r for r in ranks if not np.isnan(r)]
    if not ranks:
        return np.nan  # selected a tool type but answered no frequency item
    return float(max(ranks))


def work_mode_2026(value):
    text = "" if pd.isna(value) else str(value)
    if text == "Remote":
        return "Remote"
    if text == "In-person":
        return "In-person"
    if text.startswith("Hybrid"):
        return "Hybrid"
    if text.startswith("Your choice"):
        return "Flexible"
    return "Unknown"


def prepare_2026(raw: pd.DataFrame) -> pd.DataFrame:
    data = raw.copy()
    data["AIUsageScore"] = data.apply(usage_score_2026, axis=1)
    data["AISentimentRaw"] = data["AISentiment"]
    data["AISent"] = data["AISentiment"].map(STANCE_2026_TO_2025)
    data["AIAcc"] = data["AITrust"]  # column name kept so model specs match
    data["Daily"] = data["AIUsageScore"].eq(4).astype(int)
    data["CodingAssistantDaily"] = data["AIFreq_1"].eq("Daily").astype(int)
    data["HeavyDaily"] = data["AIDaily"].isin(HEAVY_DAILY).astype(int)
    data["Professional"] = data["CodeMain"].eq(
        "I create code as a primary part of my job"
    )
    data["DevType"] = data["Role"]
    data["RemoteWork"] = data["WorkSetting"]
    data["WorkMode"] = data["WorkSetting"].apply(work_mode_2026)
    return data


def contradictory_count(raw: pd.DataFrame) -> int:
    return int(sum(classify_use(v)[2] for v in raw["AISelect"]))
