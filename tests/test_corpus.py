from pathlib import Path
from schemescope.corpus import load_documents

def test_five_schemes_and_fifteen_sources():
    chunks=load_documents(Path(__file__).parents[1]/"documents")
    assert len({c.scheme for c in chunks}) >= 5
    assert len({c.source_url for c in chunks}) >= 15
