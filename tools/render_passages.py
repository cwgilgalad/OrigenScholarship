#!/usr/bin/env python3
"""Render the source-text files in research/passages/ from their JSON data.

Each cluster of passages lives in research/passages/data/<cluster>.json, and
research/passages/data/index.json says which files to write, in what order,
with what title and opening paragraph. The Markdown is generated, so edit the
JSON (or index.json) and run:

    python3 tools/render_passages.py

The original-language text, edition and English rendering are copied exactly
as they stand in the data. Nothing here rewrites them.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PASSAGES = ROOT / "research" / "passages"
DATA = PASSAGES / "data"

STATUS = {
    "V": "checked against an edition or a scan of one",
    "S": "checked against a scholar's quotation of it",
    "R": "not yet checked against the text",
    "C": "corrected during checking",
}
READING_STATUS = {
    "V": "read in the scholar's own words",
    "S": "from a reliable report of the scholar's view",
    "R": "standard attribution, not yet checked",
}
SECTION_MARK = re.compile(r"\s+(?=\((?:[IVXL]+\.|\d)[\w.,\-– ]{0,20}\)\s)")


def paragraphs(text):
    """Break a long quotation at its own section markers, e.g. '(92.2.1)'."""
    text = (text or "").strip()
    parts = SECTION_MARK.split(text)
    return [p.strip() for p in parts if p.strip()]


def quote(text):
    paras = paragraphs(text)
    return "\n>\n".join("> " + p for p in paras)


def link_list(urls):
    urls = [u for u in (urls or []) if u]
    if not urls:
        return ""
    if len(urls) == 1:
        return f"[source]({urls[0]})"
    return ", ".join(f"[source {i}]({u})" for i, u in enumerate(urls, 1))


def render_passage(n, p):
    out = [f"### {n}. {p['title'].strip()}", ""]
    meta = [f"**Source:** {p['author_work_ref'].strip()}"]
    if p.get("date"):
        meta.append(f"**Date:** {p['date'].strip()}")
    out.append(" · ".join(meta) + "  ")
    st = p.get("status", "R")
    corrected = " It was corrected during checking." if p.get("corrected") else ""
    out.append(f"**How far it was checked:** {st}, {STATUS.get(st, '')}.{corrected}")
    out.append("")
    if p.get("why_it_matters"):
        out += [p["why_it_matters"].strip(), ""]
    lang = (p.get("language") or "Original").strip()
    out += [f"**{lang}**", "", quote(p.get("original")), ""]
    out += [f"**English** ({p.get('english_source', '').strip()})", "", quote(p.get("english")), ""]
    out.append(f"**Edition:** {p.get('edition', '').strip()}  ")
    checked = p.get("checked_against", "").strip()
    links = link_list(p.get("source_urls"))
    out.append(f"**Checked against:** {checked}" + (f" ({links})" if links else ""))
    out.append("")
    if p.get("textual_notes"):
        out += [f"**About the text:** {p['textual_notes'].strip()}", ""]
    readings = p.get("readings") or []
    if readings:
        out += ["**How scholars read it**", ""]
        for r in readings:
            line = f"- **{r['scholar'].strip()}**, {r['work'].strip()}. {r['position'].strip()}"
            tail = [f"*{r['side'].strip()}*"] if r.get("side") else []
            tail.append(READING_STATUS.get(r.get("status", "R"), ""))
            if r.get("source_url"):
                tail.append(f"[source]({r['source_url']})")
            out.append(line + " (" + "; ".join(t for t in tail if t) + ")")
        out.append("")
    return "\n".join(out)


def render_file(entry, data):
    out = [f"# {entry['title']}", ""]
    if entry.get("lead"):
        out += [entry["lead"].strip(), ""]
    if data.get("summary"):
        out += ["## What these texts show", "", data["summary"].strip(), ""]
    passages = data.get("passages") or []
    out += ["## The passages", ""]
    for i, p in enumerate(passages, 1):
        out.append(f"{i}. [{p['title'].strip()}](#{anchor(i, p['title'])})")
    out.append("")
    for i, p in enumerate(passages, 1):
        out += [render_passage(i, p), ""]
    others = data.get("other_findings") or []
    if others:
        out += ["## Other things the check turned up", ""]
        for f in others:
            out.append(f"- {f['claim'].strip()} *Source:* {f['source'].strip()} ({READING_STATUS.get(f.get('status','R'),'').replace('the scholar', 'the source')})")
        out.append("")
    gaps = [g for g in (data.get("unverified") or []) if g]
    problems = (data.get("problems") or "").strip()
    if gaps or problems:
        out += ["## What couldn't be checked", ""]
        if problems:
            out += [problems, ""]
        for g in gaps:
            out.append(f"- {g.strip()}")
        out.append("")
    out += [f"[Back to the list of source texts](README.md)", ""]
    return "\n".join(out)


def anchor(i, title):
    # GitHub's heading slug: lower-case, drop punctuation except hyphens and spaces, spaces to hyphens
    s = f"{i}. {title}".strip().lower()
    s = re.sub(r"[^\w\- ]", "", s, flags=re.UNICODE)
    return s.replace(" ", "-")


def main():
    index = json.loads((DATA / "index.json").read_text(encoding="utf-8"))
    rows = []
    for entry in index["files"]:
        path = DATA / f"{entry['cluster']}.json"
        if not path.exists():
            print(f"skip {entry['cluster']}: no data yet", file=sys.stderr)
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        (PASSAGES / entry["file"]).write_text(render_file(entry, data), encoding="utf-8")
        n = len(data.get("passages") or [])
        rows.append((entry, n))
        print(f"wrote {entry['file']} ({n} passages)")
    readme = [f"# {index['title']}", "", index["lead"].strip(), ""]
    for part in index["parts"]:
        readme += [f"## {part['title']}", ""]
        if part.get("lead"):
            readme += [part["lead"].strip(), ""]
        readme += ["| File | What's in it | Passages |", "|---|---|---|"]
        for entry, n in rows:
            if entry["part"] == part["id"]:
                readme.append(f"| [{entry['title']}]({entry['file']}) | {entry['blurb']} | {n} |")
        readme.append("")
    readme += [index["how_to_read"].strip(), ""]
    total = sum(n for _, n in rows)
    readme += [f"*{total} passages in {len(rows)} files. This page and the files it lists are generated by `tools/render_passages.py` from `data/`.*", ""]
    (PASSAGES / "README.md").write_text("\n".join(readme), encoding="utf-8")
    print(f"wrote README.md ({total} passages)")


if __name__ == "__main__":
    main()
