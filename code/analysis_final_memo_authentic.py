"""
Reproducible pipeline for Final_Memo_Authentic.md.
Loads USASpending extracts from ../data/, builds firm-quarter panel, estimates OLS.

Run from project root:
  python code/analysis_final_memo_authentic.py
"""
from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"

UEI_TO_FIRM = {
    "FSY4LVSBGWB7": "Palantir Technologies Inc.",
    "YT9GYGR24NW9": "C3.ai, Inc.",
    "YYRJSL45NMQ7": "C3.ai, Inc.",
    "NQEWN6C1LSU5": "Amazon Web Services (AWS), Inc.",
}
VALID_UEIS = set(UEI_TO_FIRM)

KW = ["defense", "security", "intelligence", "warfighting", "surveillance"]
KW_RE = re.compile("|".join(re.escape(k) for k in KW), re.I)

# Observed obligations above this threshold treated as reporting error (see memo).
MAX_PLAUSIBLE_OBLIGATION = 1e10


def calendar_quarter(s: pd.Series) -> pd.Series:
    return pd.to_datetime(s, errors="coerce").dt.to_period("Q")


def load_prime_contracts(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, low_memory=False)
    req = ["recipient_uei", "federal_action_obligation", "action_date", "transaction_description"]
    if not all(c in df.columns for c in req):
        return pd.DataFrame()
    out = df[req].copy()
    out["federal_action_obligation"] = pd.to_numeric(out["federal_action_obligation"], errors="coerce").fillna(0.0)
    out["transaction_description"] = out["transaction_description"].fillna("").astype(str)
    return out


def load_prime_assistance(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, low_memory=False)
    if "recipient_uei" not in df.columns or "federal_action_obligation" not in df.columns:
        return pd.DataFrame()
    if "transaction_description" not in df.columns:
        return pd.DataFrame()
    out = df[["recipient_uei", "federal_action_obligation", "action_date", "transaction_description"]].copy()
    out["federal_action_obligation"] = pd.to_numeric(out["federal_action_obligation"], errors="coerce").fillna(0.0)
    out["transaction_description"] = out["transaction_description"].fillna("").astype(str)
    return out


def load_subawards(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path, dtype=str, low_memory=False)
    req = ["subawardee_uei", "subaward_amount", "subaward_action_date", "subaward_description"]
    if not all(c in df.columns for c in req):
        return pd.DataFrame()
    out = df[req].copy()
    out = out.rename(
        columns={
            "subawardee_uei": "recipient_uei",
            "subaward_amount": "federal_action_obligation",
            "subaward_action_date": "action_date",
            "subaward_description": "transaction_description",
        }
    )
    out["federal_action_obligation"] = pd.to_numeric(out["federal_action_obligation"], errors="coerce").fillna(0.0)
    out["transaction_description"] = out["transaction_description"].fillna("").astype(str)
    return out


def ingest_all() -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for csv in sorted(DATA.rglob("*.csv")):
        name = csv.name.lower()
        if "prime" in name and "contract" in name:
            frames.append(load_prime_contracts(csv))
        elif "prime" in name and "assistance" in name:
            frames.append(load_prime_assistance(csv))
        elif "subaward" in name:
            frames.append(load_subawards(csv))
    tx = pd.concat([f for f in frames if not f.empty], ignore_index=True)
    tx = tx[tx["recipient_uei"].isin(VALID_UEIS)]
    obl = pd.to_numeric(tx["federal_action_obligation"], errors="coerce").fillna(0.0)
    tx = tx[obl <= MAX_PLAUSIBLE_OBLIGATION].copy()
    tx["firm"] = tx["recipient_uei"].map(UEI_TO_FIRM)
    tx["quarter"] = calendar_quarter(tx["action_date"])
    return tx.dropna(subset=["quarter"])


def main() -> None:
    tx = ingest_all()
    start = pd.Period("2019Q1", freq="Q")
    tx = tx[tx["quarter"] >= start]

    tx["gri_hit"] = tx["transaction_description"].str.contains(KW_RE, regex=True).astype(int)

    rev = (
        tx.groupby(["firm", "quarter"], observed=True)
        .agg(
            federal_obligation=("federal_action_obligation", "sum"),
            n_tx=("federal_action_obligation", "count"),
            gri_hits=("gri_hit", "sum"),
        )
        .reset_index()
    )
    rev["gri_rate"] = np.where(rev["n_tx"] > 0, rev["gri_hits"] / rev["n_tx"], 0.0)
    rev = rev.sort_values(["firm", "quarter"])
    rev["gri_lag1"] = rev.groupby("firm")["gri_rate"].shift(1)

    shock_start = pd.Period("2023Q3", freq="Q")
    rev["D"] = (rev["quarter"] >= shock_start).astype(float)

    reg = rev.dropna(subset=["gri_lag1"]).copy()
    reg["y_m"] = reg["federal_obligation"] / 1e6

    firm_dummies = pd.get_dummies(reg["firm"], drop_first=True, dtype=float)
    X = pd.concat([reg[["gri_lag1", "D"]].astype(float), firm_dummies], axis=1)
    X = sm.add_constant(X)
    y = reg["y_m"].astype(float)
    ols = sm.OLS(y, X).fit(cov_type="HC1")

    shock = shock_start
    summary_rows = []
    for f in sorted(reg["firm"].unique()):
        sub = rev[rev["firm"] == f]
        pre_m = sub[sub["quarter"] < shock]["federal_obligation"].mean() / 1e6
        post_m = sub[sub["quarter"] >= shock]["federal_obligation"].mean() / 1e6
        summary_rows.append((f, pre_m, post_m))

    print("Latest quarter:", rev["quarter"].max())
    print("Regression N:", len(reg))
    print("\nMean quarterly obligations ($M), pre vs post shock (post = 2023Q3+):")
    for f, pre_m, post_m in summary_rows:
        print(f"  {f}: pre {pre_m:.3f}, post {post_m:.3f}")
    print("\n", ols.summary().as_text())


if __name__ == "__main__":
    main()
