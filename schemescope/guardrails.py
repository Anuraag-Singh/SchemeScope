import re

PII = re.compile(r"\b(?:[A-Z]{5}[0-9]{4}[A-Z]|\d{12}|\d{10}|\bOTP\b|one[- ]time password|account number|bank account|phone number|mobile number|email address)\b", re.I)
ADVICE = re.compile(r"\b(?:should i|should we|buy|sell|switch|invest in|better|best|recommend|recommendation|which fund|portfolio|allocate|return comparison|compare returns|highest return|will it outperform)\b", re.I)

def classify(q: str) -> str:
    if PII.search(q): return "pii"
    if ADVICE.search(q): return "advice"
    return "factual"

def refusal(kind: str) -> str:
    if kind == "pii":
        return "I can answer public scheme facts, but I can’t accept or process PAN, Aadhaar, OTP, account, phone, or email details."
    return "I’m a facts-only assistant, so I can’t recommend, rank, compare returns, or tell you whether to buy or sell a fund. I can provide the scheme’s published facts instead."
