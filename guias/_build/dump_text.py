# -*- coding: utf-8 -*-
"""Gera um .txt legível (sem marcação) do conteúdo de um guia, para revisão. Uso: python dump_text.py ml"""
import sys, os, importlib, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.stdout.reconfigure(encoding="utf-8")
k = sys.argv[1]
c = importlib.import_module("content_" + k)

def flat(x, out, ind=""):
    if isinstance(x, str):
        out.append(ind + x)
    elif isinstance(x, (list, tuple)):
        for y in x:
            flat(y, out, ind + "  ")
    elif isinstance(x, dict):
        t = x.get("t")
        if t == "h1":
            out.append("\n##### " + x["text"] + (" — " + x["intro"] if x.get("intro") else ""))
        elif t == "h2":
            out.append("\n## " + x["text"])
        elif t == "h3":
            out.append("### " + x["text"])
        elif t in ("p", "formula"):
            out.append(x["text"])
        elif t in ("bullets", "numbered"):
            for i in x["items"]:
                flat(i, out, "  • ")
        elif t == "box":
            out.append(f"[{x['kind'].upper()}] {x['title'] or ''}")
            for i in x["items"]:
                flat(i, out, "    ")
        elif t == "table":
            if x["headers"]:
                out.append("  | " + " | ".join(x["headers"]))
            for r in x["rows"]:
                cells = []
                for cell in r:
                    cells.append(" / ".join(cell) if isinstance(cell, list) else str(cell))
                out.append("  | " + " | ".join(cells))
        elif t == "code":
            out.append("  <code>")
            out += ["    " + l for l in x["text"].split("\n")]
        elif t == "ex":
            out.append("\n--- EXERCÍCIOS ---")
            for i, q in enumerate(x["items"], 1):
                out.append(f"Q{i}. {q['q']}")
                for o in (q.get("opts") or []):
                    out.append("     ( ) " + o)
                if q.get("table"):
                    out.append("     tabela: " + str(q["table"]))
                out.append("   R:")
                a = q["a"]
                flat(a if isinstance(a, list) else [a], out, "     ")
        elif t in ("space", "pagebreak"):
            pass
    elif x is not None:
        out.append(str(x))

out = []
for b in c.C:
    flat(b, out)
text = "\n".join(out)
text = re.sub(r"\*\*", "", text)
path = os.path.join(os.environ.get("DUMP_DIR", "."), f"dump_{k}.txt")
open(path, "w", encoding="utf-8").write(text)
print(path, len(text))
