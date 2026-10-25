#!/usr/bin/env python3
"""Compare facts in an original text and its rewrite.

Checks numbers, proper names, URLs, code spans and negations. A rewrite that
loses or adds a number or a name, or changes the number of negations, must be
reviewed before it is accepted. Placeholders like [DOPISZ KONKRET: ...] or
[ADD DETAIL: ...] are ignored.

Usage:
  python3 fact_guard.py ORIGINAL REWRITE [--lang auto|en|pl] [--json]
Exit code: 0 = nothing lost or added, 1 = differences to review.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

PLACEHOLDER_RE = re.compile(r"\[(?:DOPISZ KONKRET|ADD DETAIL|ADD SPECIFIC)[^\]]*\]", re.I)
CODE_RE = re.compile(r"```.*?```|`[^`\n]+`", re.S)
URL_RE = re.compile(r"https?://[^\s)>\]]+")
NUMBER_RE = re.compile(r"\d(?:[\d   ,.']*\d)?")
NEGATIONS = {
    "en": r"\b(?:not|no|never|none|nobody|nothing|neither|nor|without|cannot)\b|n't\b",
    "pl": r"\b(?:nie|nigdy|żaden|żadna|żadne|żadnych|nikt|nic|bez|ani)\b",
}
# Capitalised words that are not names when they open a sentence or a heading.
COMMON_CAPS = set(
    "The A An This That These Those It In On At For And But Or If When While We I You They He She Our My "
    "W Na Z Do I A To Ten Ta Te Jak Co Czy Nie Gdy Kiedy Jeśli Oraz Ale My Ja Ty Oni One Ich Nasz Nasza".split()
)


def norm_number(tok):
    return re.sub(r"[^\d]", "", tok)


def names(text, lang):
    found = []
    for sent in re.split(r"(?<=[.!?…:])\s+|\n+", text):
        toks = re.findall(r"[^\W\d_][\w'’-]*", sent)
        for i, t in enumerate(toks):
            if not t[0].isupper() or t in COMMON_CAPS:
                continue
            if i == 0 and not (len(t) > 1 and t.isupper()):
                continue  # sentence-initial capital: not evidence of a name
            # Polish inflects names (Warszawa/Warszawie), so compare a stem.
            found.append(t[:5].lower() if lang == "pl" and len(t) > 5 else t.lower())
    return Counter(found)


def extract(text, lang):
    text = PLACEHOLDER_RE.sub(" ", text)
    code = Counter(m.strip() for m in CODE_RE.findall(text))
    text = CODE_RE.sub(" ", text)
    urls = Counter(URL_RE.findall(text))
    text = URL_RE.sub(" ", text)
    numbers = Counter(n for n in (norm_number(t) for t in NUMBER_RE.findall(text)) if n)
    return {
        "numbers": numbers,
        "names": names(text, lang),
        "urls": urls,
        "code": code,
        "negations": len(re.findall(NEGATIONS[lang], text, re.I)),
    }


def diff(a, b):
    return {"lost": sorted((a - b).elements()), "added": sorted((b - a).elements())}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("original")
    ap.add_argument("rewrite")
    ap.add_argument("--lang", default="auto", choices=["auto", "en", "pl"])
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    orig = Path(a.original).read_text(encoding="utf-8")
    new = Path(a.rewrite).read_text(encoding="utf-8")
    lang = a.lang
    if lang == "auto":
        lang = "pl" if len(re.findall("[ąćęłńśźż]", orig.lower())) > 3 else "en"
    x, y = extract(orig, lang), extract(new, lang)
    report = {k: diff(x[k], y[k]) for k in ("numbers", "names", "urls", "code")}
    # A name only changed case (Title Case heading -> sentence case) if it still appears in lower case.
    report["names"]["lost"] = sorted({n for n in report["names"]["lost"] if n not in new.lower()})
    report["names"]["added"] = sorted({n for n in report["names"]["added"] if n not in orig.lower()})
    report["negations"] = {"original": x["negations"], "rewrite": y["negations"]}
    report["placeholders_added"] = len(PLACEHOLDER_RE.findall(new)) - len(PLACEHOLDER_RE.findall(orig))
    problems = any(report[k]["lost"] or report[k]["added"] for k in ("numbers", "names", "urls", "code"))
    problems = problems or x["negations"] != y["negations"]
    report["ok"] = not problems

    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print("Fact guard: " + ("OK, no facts lost or added" if report["ok"] else "REVIEW the differences below"))
        for k in ("numbers", "names", "urls", "code"):
            if report[k]["lost"]:
                print(f"  {k} lost:  {', '.join(report[k]['lost'])}")
            if report[k]["added"]:
                print(f"  {k} added: {', '.join(report[k]['added'])}")
        if x["negations"] != y["negations"]:
            print(f"  negations: {x['negations']} -> {y['negations']} (check that no claim flipped)")
        if report["placeholders_added"] > 0:
            print(f"  {report['placeholders_added']} placeholder(s) for missing specifics added")
        print("Names are matched heuristically; a lost name may be a harmless rewording. Check each one.")
    sys.exit(0 if report["ok"] else 1)


if __name__ == "__main__":
    main()
