from pathlib import Path
from schemescope.corpus import load_documents

def test_sources_are_official_hdfc():
    chunks=load_documents(Path(__file__).parents[1]/"documents")
    assert all("hdfcfund.com" in c.source_url for c in chunks)
    assert all("groww" not in c.source_url.lower() for c in chunks)
