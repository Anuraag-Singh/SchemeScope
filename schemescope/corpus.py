from pathlib import Path
import re
from .models import Chunk

FRONT = re.compile(r"^---\n(.*?)\n---\n", re.S)

def load_documents(folder: Path):
    chunks=[]
    for path in sorted(folder.glob("*.md")):
        raw=path.read_text(encoding="utf-8")
        m=FRONT.match(raw)
        meta={}
        body=raw
        if m:
            for line in m.group(1).splitlines():
                if ":" in line:
                    k,v=line.split(":",1); meta[k.strip()]=v.strip()
            body=raw[m.end():]
        parts=re.split(r"(?=^## )", body, flags=re.M)
        for i,p in enumerate(parts):
            p=p.strip()
            if not p: continue
            heading=p.splitlines()[0].lstrip("# ").strip()
            text=" ".join(x.strip() for x in p.splitlines()[1:] if x.strip())
            if text:
                chunks.append(Chunk(f"{path.stem}-{i}", meta.get("scheme", path.stem), heading, text, meta["source_url"], meta.get("updated","2026-09-29")))
    return chunks
