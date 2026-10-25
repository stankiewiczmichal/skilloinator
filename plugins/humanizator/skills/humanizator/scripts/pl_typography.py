#!/usr/bin/env python3
"""Apply mechanical Polish typography fixes to a text and print the result.

Fixes:
  "tekst" and “tekst”   -> „tekst”   (nested quotes inside „…” become ‚…’)
  słowo—słowo, słowo — słowo, słowo - słowo -> słowo – słowo  (--dash en, default)
                                             -> słowo — słowo  (--dash em)
  1914—1918             -> 1914–1918
  „tekst.”              -> „tekst”.
  Dodatkowo, / Ponadto, / Jednakże, at sentence start -> no comma
  --nbsp: non-breaking space after one-letter words (w, z, i, a, o, u) for typesetting

Code blocks, inline code and URLs are left untouched. Title Case headings are
only reported, because sentence case needs judgement about proper names.

Usage:
  python3 pl_typography.py FILE [--dash en|em] [--nbsp] [--report]
"""
import argparse
import re
import sys
from pathlib import Path

PROTECT_RE = re.compile(r"```.*?```|`[^`\n]*`|https?://\S+", re.S)
HEADING_RE = re.compile(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*$")


def fix_quotes(s):
    out, depth = [], 0
    for i, ch in enumerate(s):
        if ch in "\"“”„":
            prev = s[i - 1] if i else " "
            opening = ch in "“„" or (ch == "\"" and (prev.isspace() or prev in "([{–—-/"))
            if ch == "”" and depth == 0:
                opening = False
            if opening:
                out.append("„" if depth == 0 else "‚")
                depth += 1
            else:
                depth = max(depth - 1, 0)
                out.append("”" if depth == 0 else "’")
        else:
            out.append(ch)
    return "".join(out)


def fix_segment(s, dash, nbsp, counts):
    def sub(name, pattern, repl, text, flags=0):
        new, n = re.subn(pattern, repl, text, flags=flags)
        counts[name] = counts.get(name, 0) + n
        return new

    before = s
    s = fix_quotes(s)
    counts["quotes"] = counts.get("quotes", 0) + sum(a != b for a, b in zip(before, s))
    s = sub("number_ranges", r"(\d)\s*[—–]\s*(\d)", r"\1–\2", s)
    mark = "–" if dash == "en" else "—"
    s = sub("dashes", r"(?<=[^\W\d_])—(?=[^\W\d_])", f" {mark} ", s)
    other = "—-" if dash == "en" else "–-"
    s = sub("dashes", rf"(?<=\S) [{other}] (?=\S)", f" {mark} ", s)
    s = sub("period_after_quote", r"([^\s.,])([.,])([”’])", r"\1\3\2", s)
    s = sub("comma_after_adverb", r"(^|[.!?]\s+|\n)(Dodatkowo|Ponadto|Jednakże),\s", r"\1\2 ", s)
    if nbsp:
        s = sub("nbsp", r"(?<![^\s(„])([wzWZiIaAoOuU]) (?=\S)", "\\1\u00a0", s)
    return s


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text file, or - for stdin")
    ap.add_argument("--dash", default="en", choices=["en", "em"], help="dash used between words (default: en dash –)")
    ap.add_argument("--nbsp", action="store_true", help="add non-breaking spaces after one-letter words")
    ap.add_argument("--report", action="store_true", help="print a summary of changes to stderr")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else Path(a.file).read_text(encoding="utf-8")

    counts, out, last = {}, [], 0
    for m in PROTECT_RE.finditer(text):
        out.append(fix_segment(text[last:m.start()], a.dash, a.nbsp, counts))
        out.append(m.group(0))
        last = m.end()
    out.append(fix_segment(text[last:], a.dash, a.nbsp, counts))
    result = "".join(out)
    sys.stdout.write(result)

    if a.report:
        title_case = [h for h in HEADING_RE.findall(result)
                      if sum(w[0].isupper() for w in h.split()[1:] if len(w) > 3) >= 2]
        print("\n--- pl_typography report ---", file=sys.stderr)
        for k, v in counts.items():
            if v:
                print(f"  {k}: {v}", file=sys.stderr)
        for h in title_case:
            print(f"  Title Case heading, change to sentence case by hand: {h}", file=sys.stderr)


if __name__ == "__main__":
    main()
