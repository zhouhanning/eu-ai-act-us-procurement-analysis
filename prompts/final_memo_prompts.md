# LLM and Analysis Prompts — Final Memo (Authentic)

Course rubric requires that where large language models (LLMs) are used, **prompts are attached**. This project’s **proof-of-concept regression and keyword-based GRI** are implemented in **`code/analysis_final_memo_authentic.py`** without an LLM. The prompts below document (1) optional **next-step** LLM use for a richer political-risk text index, and (2) the **memo drafting** assistant thread (high level) used to align the write-up with the assignment.

---

## 1. Optional prototype: LLM-assisted “GRI v2” (future work)

If you replace keyword hits with structured labels, a reproducible prompt template is:

```
You are a senior defense-industry analyst. Given the US federal contract or subaward
description below, answer in JSON only with keys:
{"mission_class": one of ["defense_cloud","intel_analytics","biometric_surveillance","civil_admin","other"],
 "geopolitical_salience": integer 0-3,
 "surveillance_semantics": boolean}.

Description:
"""{{transaction_description}}"""
```

Batch this over all lines, cache results by `contract_transaction_unique_key` or equivalent, then aggregate **geopolitical_salience** or **surveillance_semantics** rate by (firm, quarter). This addresses **polysemy** (“security” in IT vs national security) that weakens keyword GRI v1.

**Model governance:** Fix model version, temperature `0`, and retain raw JSON outputs alongside code hashes for audit.

---

## 2. Memo revision prompt (course rubric alignment)

Prompt used to align **`Final_Memo_Authentic.md`** with the assignment (paraphrased):

```
Revise the final memo so it explicitly states the political risk question
(political/social factor → economic outcome); summarizes existing approaches
in the literature or policy practice; states their limits; presents our design
as a prototype that addresses those limits; retains preliminary empirical
results as proof-of-concept; adds next steps; and references attached code and
prompt files.
```

---

## 3. No LLM on raw federal data

For compliance and reproducibility, **Personally Identifiable Information** in extracts was not sent to external APIs. All quoted obligation figures and regression outputs come from **local execution** of `analysis_final_memo_authentic.py` on the **`/data`** CSV files.
