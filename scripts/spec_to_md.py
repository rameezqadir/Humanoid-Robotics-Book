import yaml
from pathlib import Path

specs_dir = Path("specs")
out_docs = Path("docs-site/docs")
out_docs.mkdir(parents=True, exist_ok=True)

for f in specs_dir.rglob("*.yaml"):
    s = yaml.safe_load(f.read_text())
    md = f"# {s.get('title','Untitled')}

"
    md += s.get('quarter_scope','') + "\n\n" if s.get('quarter_scope') else ""
    if 'modules' in s:
        for m in s['modules']:
            md += f"## {m['title']}\n\n"
            for obj in m.get('objectives', []):
                md += f"- {obj}\n"
            md += "\n"
    out_file = out_docs / (f.stem + ".md")
    out_file.write_text(md)
    print("Wrote", out_file)
