from dataclasses import dataclass

@dataclass
class Chunk:
    id: str
    scheme: str
    section: str
    text: str
    source_url: str
    updated: str

@dataclass
class Hit:
    chunk: Chunk
    score: float
