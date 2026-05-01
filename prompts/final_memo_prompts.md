# Prompt Notes for the Final Memo

This project uses two separate prompt records.

- `prompts/final_memo_prompts.md` documents the prompt logic that belongs to the final memo itself: how LLM assistance could be used in a later extension of the analysis, and how prompt use is framed for reproducibility.
- `prompts/prompt_recorded.md` records the prompts used during the actual course workflow, including drafting, revision, formatting, and follow-up requests made while preparing the assignment.

The core empirical pipeline in `code/analysis_final_memo_authentic.py` does **not** use an LLM to generate the reported numerical results. Data ingestion, cleaning, panel construction, keyword-based GRI calculation, and regression output all come from local code execution.

---

## 1. Role of LLM use in this project

LLM use in this project serves two limited purposes.

First, it supports memo drafting and revision during the course workflow. That record is preserved in `prompts/prompt_recorded.md`.

Second, it provides a documented template for a possible future extension of the text analysis. The memo currently uses a transparent keyword-based geopolitical rhetoric index (GRI v1). If the project is extended beyond this baseline, an LLM-assisted classifier could be used to build a richer GRI v2. That future-facing prompt logic is documented below.

---

## 2. Optional future extension: LLM-assisted GRI v2

A more context-sensitive version of the geopolitical rhetoric index could replace simple keyword matching with structured labels. One reproducible prompt template would be:

```
You are a senior defense-industry analyst. Given the U.S. federal contract or
subaward description below, return JSON only with the following keys:
{"mission_class": one of ["defense_cloud","intel_analytics",
"biometric_surveillance","civil_admin","other"],
 "geopolitical_salience": integer 0-3,
 "surveillance_semantics": boolean}

Description:
"""{{transaction_description}}"""
```

If used, this prompt would be applied to transaction descriptions one record at a time, with outputs cached by `contract_transaction_unique_key` or an equivalent transaction identifier. The coded outputs could then be aggregated to the firm--quarter level to create a richer text measure than GRI v1.

The motivation for this extension is straightforward: simple keyword matching can confuse ordinary IT-security language with national-security or defense-related content. A structured classifier would help reduce that ambiguity while keeping the coding logic explicit.

**Suggested governance rules for a future GRI v2 workflow:**

- fix the model version;
- set temperature to `0`;
- retain raw JSON outputs;
- store the prompt text alongside code hashes;
- validate a sample of labels by hand before aggregation.

---

## 3. Prompt use during memo preparation

The prompts that were actually used while preparing the assignment are documented in `prompts/prompt_recorded.md`. That file includes:

- the main drafting prompt for the memo;
- follow-up prompts used to align the draft with the course requirements;
- prompts related to equation formatting and LaTeX conversion;
- a note explaining that some prompts had to be reconstructed after an application reload.

This separation is intentional. `prompt_recorded.md` is the assignment workflow record, while this file explains how prompt use fits into the logic of the final memo.

---

## 4. No LLM use in the reported empirical results

All quoted obligation figures, descriptive summaries, and regression outputs in the memo come from local execution of `code/analysis_final_memo_authentic.py` on the bundled `data` files. In the current pipeline, no LLM is applied to raw federal transaction data.

This means the reported quantitative results are reproducible from the local code and source files alone. Any future LLM-assisted extension should be treated as an additional layer of text classification rather than as part of the current empirical baseline.
