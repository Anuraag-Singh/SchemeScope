from .guardrails import classify, refusal
from .index import Index
from .answer import generate
from .config import THRESHOLD

class Pipeline:
    def __init__(self): self.index=Index()
    def ask(self,q):
        kind=classify(q)
        if kind!="factual": return {"text":refusal(kind),"refused":True,"source":None,"score":None}
        hits=self.index.search(q)
        if not hits or hits[0].score < THRESHOLD:
            return {"text":"I can’t verify that fact from the supported HDFC Mutual Fund sources in my corpus.","refused":True,"source":None,"score":hits[0].score if hits else None}
        h=hits[0]
        text, chosen = generate(q,hits)
        return {"text":text,"refused":False,"source":chosen.chunk.source_url,"scheme":chosen.chunk.scheme,"section":chosen.chunk.section,"updated":chosen.chunk.updated,"score":h.score}
