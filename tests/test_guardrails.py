from schemescope.guardrails import classify

def test_pii(): assert classify("What is my PAN ABCDE1234F?") == "pii"
def test_advice(): assert classify("Which fund is better for me?") == "advice"
def test_fact(): assert classify("What is the exit load?") == "factual"
