#!/usr/bin/env python3
"""Mechanical check of the original-language passages against their sources.

For each passage in a data file, download every source URL it records,
strip the markup, and measure how much of the passage's original text
appears in the source, as the share of its three-word sequences found
there (within each stretch between omission marks), and as the share of its words found anywhere in the source (after removing accents, case and punctuation, and treating u/v and
i/j alike). A score near 1.0 means the text was copied faithfully from
that source; a low score means it needs a person to look.

    python3 tools/check_texts.py research/passages/data/c400.json [more files] [--cache DIR] [--out DIR]
"""
import argparse, hashlib, html, json, re, subprocess, sys, unicodedata
from pathlib import Path

def norm_tokens(text):
    text = html.unescape(text)
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower().replace("ς", "σ").replace("v", "u").replace("j", "i")
    text = re.sub(r"\(\s*[\divxl][\w.,\- ]{0,20}\)", " ", text)  # section markers like (92.1.4)
    return re.findall(r"[^\W\d_]+", text, flags=re.UNICODE)

def strip_markup(raw):
    raw = re.sub(r"(?s)<(script|style|teiHeader)\b.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<note\b.*?</note>", " ", raw)
    return re.sub(r"<[^>]+>", " ", raw)

def fetch(url, cache):
    key = cache / (hashlib.sha1(url.encode()).hexdigest() + ".txt")
    if key.exists():
        return key.read_text(encoding="utf-8", errors="replace")
    try:
        raw = subprocess.run(["curl", "-sL", "--max-time", "60", "-A", "Mozilla/5.0", url],
                             capture_output=True, timeout=90).stdout.decode("utf-8", "replace")
    except Exception:
        raw = ""
    text = strip_markup(raw)
    key.write_text(text, encoding="utf-8")
    return text

def grams(tokens, n=3):
    return {tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)}

def segment_grams(text, n=3):
    """Word sequences within each stretch of quoted text, not across an omission mark."""
    out = set()
    for seg in re.split(r"\.\.\.|…|\[|\]|/", text or ""):
        out |= grams(norm_tokens(seg), n)
    return out

def check(path, cache):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = []
    for p in data.get("passages", []):
        want = segment_grams(p.get("original", ""))
        words = {w for w in norm_tokens(p.get("original", "")) if len(w) > 2}
        best, best_words, best_url = 0.0, 0.0, None
        for url in p.get("source_urls") or []:
            if not want:
                break
            src = norm_tokens(fetch(url, cache))
            score = len(want & grams(src)) / len(want)
            wscore = len(words & set(src)) / len(words) if words else 0.0
            if (score, wscore) > (best, best_words):
                best, best_words, best_url = score, wscore, url
        rows.append({"id": p["id"], "status": p.get("status"), "language": p.get("language"),
                     "score": round(best, 3), "words": round(best_words, 3), "matched_url": best_url, "grams": len(want)})
    return rows

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--cache", default=".textcheck-cache")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    cache = Path(a.cache); cache.mkdir(parents=True, exist_ok=True)
    for f in a.files:
        rows = check(f, cache)
        name = Path(f).stem
        if a.out:
            Path(a.out).mkdir(parents=True, exist_ok=True)
            (Path(a.out) / f"{name}.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
        for r in rows:
            print(f"{name:22} {r['id'][:40]:40} {r['status']} seq {r['score']:.2f} words {r['words']:.2f}  {(r['matched_url'] or '-')[30:80]}")

if __name__ == "__main__":
    main()
