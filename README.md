# EU AI Act Timing and U.S. Federal Procurement

### A Firm–Quarter Empirical Analysis (Research Design Memo)

**Author:** Hanning Zhou
**Date:** April 2026

---

## 📌 Overview

This repository contains the research design, data pipeline, and preliminary empirical analysis for examining:

> **How EU AI regulatory milestones (EU AI Act) relate to U.S. federal procurement flows to AI and cloud vendors.**

The project links **transatlantic regulatory timing** with **firm-level government revenue exposure**, using transaction-level procurement data and a simple text-based geopolitical signal.

---

## ❓ Research Question

How does the timing of EU AI Act legislative milestones relate to realized U.S. federal procurement obligations to selected AI/cloud vendors?

---

## 🧩 Research Design

This project implements a transparent, audit-friendly empirical pipeline:

* Construct a **firm–quarter panel (2019Q1–2025Q3)**

* Define a **post-EU AI Act milestone indicator (2023Q3+)**

* Aggregate U.S. federal procurement data (USASpending-style)

* Build a **Geopolitical Rhetoric Index (GRI)** using keyword matching

* Estimate:

* OLS with **firm fixed effects**

* **HC1 robust standard errors**

---

## 📊 Data

### Sources

* U.S. federal procurement transaction data (prime + sub-awards)
* EU AI Act legislative timeline (European Parliament milestone: June 2023)

### Sample

* 2,579 transactions
* 70 firm–quarter observations
* Firms:

  * AWS
  * Palantir
  * C3.ai

---

## ⚙️ Methodology

### Key Variables

* **Outcome (Y):** Quarterly obligations (USD, millions)
* **Treatment (D):** Post-2023Q2 indicator (EU AI Act milestone)
* **GRI:** Share of contracts containing geopolitical/security keywords

### Model

* Firm fixed effects regression
* Lagged GRI (t−1)
* Heteroskedasticity-robust inference

---

## 📈 Key Findings (Preliminary)

* Strong **post-2023Q2 increase** in procurement obligations
* Positive and statistically significant coefficient on post-period indicator
* **GRI has limited explanatory power** in current specification

⚠️ Results are **descriptive, not causal**, due to concurrent shifts in:

* U.S. defense cloud procurement (e.g., JWCC)
* Geopolitical and industrial policy changes

---

## 🗂️ Repository Structure

```bash
.
├── code/
│   └── analysis_final_memo_authentic.py
├── data/
│   └── (procurement extracts)
├── prompts/
│   └── final_memo_prompts.md
├── docs/
│   └── Final_Memo_Authentic.pdf
└── README.md
```

---

## 🔁 Reproducibility

To reproduce results:

```bash
python code/analysis_final_memo_authentic.py
```

Pipeline includes:

* Data ingestion and cleaning
* Firm-level aggregation
* GRI construction
* Regression estimation

No LLM is used in the current pipeline (GRI v1 = keyword-based).

---

## 🚀 Future Work

* Causal identification (triple-difference / staggered designs)
* Expanded firm coverage
* LLM-based **GRI v2** (structured text classification)
* Forecasting procurement flows
* Integration with firm financial exposure

---

## ⚖️ Interpretation

This project should be understood as:

> A **transparent empirical prototype** linking regulatory timelines to real economic activity, rather than a definitive causal estimate.

---

## 📎 Citation

If you reference this work, please cite the memo:

Zhou, H. (2026). *EU AI Regulation Timing and U.S. Federal Procurement*. Research Design Memo.

---

## 📬 Contact

For questions or collaboration:

* GitHub Issues
* Direct contact (if shared in application materials)
