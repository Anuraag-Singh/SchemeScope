# SchemeScope — Facts-Only Mutual Fund FAQ

A small RAG-based FAQ assistant built for the NextLeap **AI System Design, LLMs & Prompt Engineering** milestone. The selected product context is **INDMoney**; the factual corpus is limited to **HDFC Mutual Fund** public sources.

**Live prototype:** https://schemescopegit-eoavutw2d6adgbv9fhyt5y.streamlit.app/

## What it does

SchemeScope answers factual questions about five HDFC schemes:

- HDFC Large Cap Fund
- HDFC Flexi Cap Fund
- HDFC ELSS - Tax Saver Fund
- HDFC Small Cap Fund
- HDFC Balanced Advantage Fund

Supported facts include expense ratio, exit load, minimum SIP/investment, ELSS lock-in, riskometer, benchmark and scheme objective. It refuses investment advice, rankings, return comparisons and PII.

Every accepted answer is capped at **3 sentences**, displays **one source link**, and shows **Last updated from sources:**.

## Architecture

```text
Question
  -> PII / advice guardrails
  -> local embedding
  -> Chroma similarity search
  -> evidence threshold
  -> OpenAI-compatible LLM (optional)
  -> <=3 sentence answer
  -> one allow-listed source
```

The vector index is built automatically the first time the application starts. There is no separate ingest command required for deployment.

If `LLM_API_KEY` is configured, the answer is generated from retrieved evidence using the configured OpenAI-compatible endpoint. If the key is absent or the provider is unavailable, the app uses a deterministic extractive fallback from the retrieved source chunk rather than inventing an answer. This makes the demo runnable while still demonstrating the LLM path when configured.

## Run locally

Python 3.11+ is recommended.

```bash
python -m venv .venv
# Windows
.venv\\Scripts\\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
copy .env.example .env        # Windows
# cp .env.example .env        # macOS/Linux
streamlit run app.py
```

Add an API key to `.env` for LLM generation:

```env
LLM_API_KEY=your_key_here
LLM_MODEL=gpt-4o-mini
LLM_BASE_URL=https://api.openai.com/v1
```

Never commit `.env` or an API key.

## Streamlit Community Cloud

1. Push this repository to GitHub.
2. Create a Streamlit Community Cloud app.
3. Set the main file to `app.py`.
4. Add these secrets in the Streamlit Secrets panel:

```toml
LLM_API_KEY = "your_key_here"
LLM_MODEL = "gpt-4o-mini"
LLM_BASE_URL = "https://api.openai.com/v1"
```

5. Deploy. On the first boot, the local embedding model downloads and Chroma builds its index from `documents/`. Subsequent questions reuse the cached index.

## Render

The repository includes `Procfile` and `render.yaml`.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

Set `LLM_API_KEY` as a Render secret/environment variable.

## Required milestone deliverables

- `deliverables/SOURCES.csv` — 16 official HDFC public URLs used for the corpus/reference set.
- `deliverables/sample_qa.md` — sample factual and refusal Q&A.
- `deliverables/disclaimer.md` — exact facts-only disclaimer used in the UI.
- `PROJECT.md` — product/system design summary.

## Source list

SchemeScope uses only official HDFC Mutual Fund public pages for its answer corpus. The complete source registry is also available in `deliverables/SOURCES.csv`.

| # | Source | Purpose |
|---|---|---|
| 1 | [HDFC Large Cap Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct) | TER, minimum SIP, exit load, riskometer, benchmark |
| 2 | [HDFC Large Cap Fund — Regular](https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/regular) | Benchmark, minimum SIP, exit load |
| 3 | [HDFC Flexi Cap Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct) | TER, minimum SIP, exit load, riskometer, benchmark |
| 4 | [HDFC Flexi Cap Fund — Regular](https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/regular) | Benchmark, exit load |
| 5 | [HDFC ELSS Tax Saver Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct) | Lock-in, TER, minimum SIP, exit load, riskometer, benchmark |
| 6 | [HDFC ELSS Tax Saver Fund — Regular](https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/regular) | Lock-in, minimum, benchmark |
| 7 | [HDFC Small Cap Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund/direct) | Minimum SIP, exit load, riskometer, benchmark |
| 8 | [HDFC Small Cap Fund — Regular](https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund/regular) | Minimum, TER, exit load, benchmark |
| 9 | [HDFC Balanced Advantage Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-balanced-advantage-fund/direct) | Minimum SIP, exit load, riskometer, benchmark |
| 10 | [HDFC Balanced Advantage Fund — Regular](https://www.hdfcfund.com/explore/mutual-funds/hdfc-balanced-advantage-fund/regular) | Minimum, exit load, benchmark |
| 11 | [HDFC Mutual Fund — KIM index](https://www.hdfcfund.com/mutual-funds/fund-documents/kim) | Official KIM documents |
| 12 | [HDFC Mutual Fund — SID index](https://www.hdfcfund.com/mutual-funds/fund-documents/sid) | Official SID documents |
| 13 | [HDFC Mutual Fund — Scheme summary](https://www.hdfcfund.com/mutual-funds/fund-documents/scheme-summary) | Scheme objectives |
| 14 | [HDFC Mutual Fund — Factsheets](https://www.hdfcfund.com/mutual-funds/factsheets) | Monthly factsheets |
| 15 | [HDFC Mutual Fund — Investor FAQ](https://www.hdfcfund.com/services/faqs/subscription-related-faqs) | Official transaction/support information |
| 16 | [HDFC Mutual Fund — NAV and IDCW](https://www.hdfcfund.com/nav-and-idcw) | NAV publication reference |

## Sample Q&A

The following examples demonstrate the intended factual, citation-backed response style. The live application retrieves evidence from its local corpus and attaches one source link.

### 1. What is the expense ratio of HDFC Large Cap Fund?

The HDFC Large Cap Fund Direct Plan page lists TER as 1.03%.

**Source:** [HDFC Large Cap Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct)

### 2. What is the lock-in period for HDFC ELSS Tax Saver Fund?

The scheme has a statutory lock-in period of 3 years.

**Source:** [HDFC ELSS Tax Saver Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver-fund/direct)

### 3. What is the minimum SIP for HDFC Flexi Cap Fund?

The minimum SIP amount shown is ₹100.

**Source:** [HDFC Flexi Cap Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct)

### 4. What is the exit load of HDFC Balanced Advantage Fund?

Up to 15% of units from each purchase/switch-in may be redeemed without exit load. Redemption above that limit is subject to 1.00% exit load within 1 year; no exit load applies after 1 year.

**Source:** [HDFC Balanced Advantage Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-balanced-advantage-fund/direct)

### 5. What is the benchmark of HDFC Small Cap Fund?

The benchmark is the BSE 250 SmallCap Index (Total Returns Index).

**Source:** [HDFC Small Cap Fund — Direct](https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund/direct)

### 6. Which HDFC fund is better?

I’m a facts-only assistant, so I can’t recommend, rank, compare returns, or tell you whether to buy or sell a fund. I can provide the published facts for each supported scheme instead.

### 7. What is my PAN?

I can answer public scheme facts, but I can’t accept or process PAN, Aadhaar, OTP, account, phone, or email details.

## Disclaimer

> **Facts-only. No investment advice.**
>
> SchemeScope answers factual questions from a constrained corpus of public HDFC Mutual Fund pages. It does not recommend, rank, compare returns, or make investment decisions. Do not enter PAN, Aadhaar, OTP, account numbers, phone numbers, or email addresses.

## Source policy

The source registry contains only official HDFC Mutual Fund pages. No Groww, broker, blog or other third-party page is used as an answer source.

Source pages include the five selected scheme pages (Direct and Regular plan references) plus HDFC's official KIM, SID, scheme-summary, factsheet and investor-FAQ pages. The assistant only links to URLs present in its own corpus metadata.

## UI improvements / next steps

The current UI is intentionally lightweight and demo-focused. The next UI iteration could improve:

- **Mobile responsiveness:** tighten spacing and card layouts for smaller screens.
- **Conversation navigation:** add clearer conversation anchors and a more obvious way to jump between recent questions and answers.
- **Source previews:** show a compact source title/section preview before opening the official page.
- **Loading states:** provide a clearer progress state while retrieval and first-time index creation are running.
- **Accessibility:** improve keyboard navigation, focus states, contrast checks and screen-reader labels.
- **Scheme discovery:** add a simple scheme selector/filter so users can narrow questions to a supported scheme.
- **Empty/error states:** make unavailable evidence, temporary model failures and unsupported questions more visually distinct.

These are presentation and usability improvements; the facts-only guardrails and source restrictions remain the core product behavior.

## Known limits

- This is a factual FAQ prototype, not an investment-advice system.
- Facts can change as the AMC updates its pages; the corpus therefore carries a capture date.
- The app does not calculate or compare returns.
- The extractive fallback is intentionally conservative and may refuse or return only the retrieved source text when an LLM is unavailable.
- The first cloud boot can be slower because the embedding model is downloaded and the Chroma index is created.

## Assignment disclaimer

**Facts-only. No investment advice.**

Do not enter PAN, Aadhaar, OTP, account numbers, phone numbers or email addresses.
