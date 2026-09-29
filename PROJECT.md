# Project Summary

## Product context
INDMoney

## Problem
Retail mutual-fund users repeatedly ask support-style factual questions. The assistant should answer those questions from verified public sources without turning into an investment adviser.

## Scope
One AMC: HDFC Mutual Fund.

Five schemes: Large Cap, Flexi Cap, ELSS Tax Saver, Small Cap and Balanced Advantage.

## Model behavior
1. Detect PII and refuse before retrieval.
2. Detect advice/opinion/return-comparison intent and refuse before retrieval.
3. Embed the factual question locally.
4. Retrieve the nearest evidence from Chroma.
5. Refuse when the similarity score is below the configured evidence threshold.
6. Generate from retrieved evidence only when an LLM API key is available.
7. Otherwise use deterministic extractive fallback.
8. Display exactly one source URL from the retrieved metadata.
9. Keep the answer within three sentences.

## Why RAG
The corpus is deliberately small and controlled. Retrieval provides a traceable evidence block, while the generation layer turns that evidence into a concise natural-language answer.
