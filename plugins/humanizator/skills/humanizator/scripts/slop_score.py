#!/usr/bin/env python3
"""Measure the "AI smell" of an English or Polish text (0-100).

This is not an authorship detector. It counts statistical AI-isms: a weighted
lexicon, discourse and syntax templates, Markdown density, dash and Polish
typography habits, sentence-length rhythm and lack of concrete detail.

Usage:
  python3 slop_score.py FILE [--lang auto|en|pl] [--json] [--top N]
  cat text.md | python3 slop_score.py - --lang pl
"""
import argparse
import json
import math
import re
import statistics
import sys
import unicodedata
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Discourse and structural templates. Fixed phrases and single words live in
# lexicon/<lang>.json; patterns here are counted as "tmpl".
TEMPLATES = {
    "en": {
        "NEG_PARALLEL": (3, r"(?i)\b(?:isn'?t|aren'?t|is not|are not|it'?s not|this is not|that'?s not)\s+(?:just|only|merely|simply|about)\s+[^.;!?\n]{1,60}?(?:[,;:—–]|\s-)\s*(?:it'?s|they'?re|this is|but|rather)\b"),
        "NEG_PARALLEL_IT": (3, r"(?i)\b(?:it'?s|this is|that'?s) not\s+[^.;!?\n]{1,60}?(?:[,;:—–]|\s-)\s*(?:it'?s|this is|that'?s)\b"),
        "NEG_PARALLEL_2S": (3, r"(?i)\b(?:it|this|that)(?:'s| is) not (?:just )?[^.!?\n]{1,60}[.!?]\s+(?:it|this|that)(?:'s| is)\b"),
        "NOT_ONLY": (2, r"(?i)\bnot\s+(?:just|only|merely)\s+[^.\n]{1,60}?,?\s+but\s+(?:also\s+)?"),
        "FALSE_RANGE": (1.5, r"\b(?i:from)\s+(?:[a-z][\w-]*\s+){0,3}[a-z][\w-]*\s+to\s+(?:[a-z][\w-]*\s+){0,3}[a-z][\w-]*\b"),
        "TRIAD": (1, r"(?i)\b[a-z][\w-]*(?: [a-z][\w-]*)?, [a-z][\w-]*(?: [a-z][\w-]*)?,? (?:and|or) [a-z][\w-]*\b"),
        "OPENER_CHAT": (3, r"(?im)^\s*(?:certainly|absolutely|sure|great question|of course|ha)\s*[!,.—]"),
        "CLOSER_OFFER": (3, r"(?i)\b(?:I hope this helps|let me know if|feel free to|would you like me to|happy to help|if you want, I can|I'?d be happy to)\b"),
        "SUMMARY": (2, r"(?im)^\s*(?:in conclusion|in summary|ultimately|to sum up|all in all)\b"),
        "SYCOPHANCY": (3, r"(?i)\b(?:you'?re absolutely (?:right|correct)|great (?:question|point)|excellent (?:question|point)|what a (?:brilliant|great|fantastic) (?:idea|question))\b"),
        "AI_ARTIFACT": (6, r"(?i)\b(?:as an AI(?: language model)?|as a large language model|as of my (?:last|latest) (?:training|knowledge)(?: update| cutoff)?|I (?:cannot|can't) browse)\b"),
        "SHALL_WE": (2, r"(?i)\b(?:let'?s (?:dive|delve|explore|take a closer look)|here'?s (?:a|the) (?:breakdown|rundown))\b"),
    },
    "pl": {
        "NEG_PARALLEL": (3, r"(?i)\bto nie (?:tylko |jest |kolejn\w+ )?[^.;!?\n]{1,60}?\s*[,;:—–]\s*to\b"),
        "NEG_PARALLEL_2S": (3, r"\bTo nie [^.!?\n]{1,60}[.!?]\s+To\b"),
        "NOT_ONLY": (2, r"(?i)\bnie tylko\b[^.\n]{1,80}?\b(?:ale|lecz) (?:także|również|i|też)\b"),
        "FALSE_RANGE": (1.5, r"\b(?i:od)\s+(?:[a-ząćęłńóśźż]\w*\s+){0,3}[a-ząćęłńóśźż]\w*\s+(?:po|aż po)\s+(?:[a-ząćęłńóśźż]\w*\s+){0,3}[a-ząćęłńóśźż]\w*\b"),
        "TRIAD": (1, r"(?i)\b[a-ząćęłńóśźż]\w*, [a-ząćęłńóśźż]\w*,? (?:i|oraz|lub|albo) [a-ząćęłńóśźż]\w*\b"),
        "OPENER_CHAT": (3, r"(?im)^\s*(?:oczywiście|jasne|świetne pytanie|doskonałe pytanie|chętnie)\s*[!,.—]"),
        "CLOSER_OFFER": (3, r"(?i)\b(?:mam nadzieję, że (?:to|ten|te|moja)|daj (?:mi )?znać, jeśli|czy chcesz, (?:żebym|abym)|jeśli chcesz, (?:mogę|przygotuję)|chętnie pomogę|służę pomocą)\b"),
        "SUMMARY": (2, r"(?im)^\s*(?:podsumowując|reasumując|konkludując|na zakończenie|w podsumowaniu)\b"),
        "SYCOPHANCY": (3, r"(?i)\b(?:masz (?:absolutną |całkowitą )?rację|świetne pytanie|doskonałe pytanie|wspaniały pomysł|trafna uwaga)\b"),
        "AI_ARTIFACT": (6, r"(?i)\b(?:jako (?:model językowy(?: AI)?|sztuczna inteligencja|asystent AI)|według (?:mojej|stanu mojej) wiedzy na dzień|nie mam dostępu do internetu)\b"),
        "SHALL_WE": (2, r"(?i)\b(?:przyjrzyjmy się|przejdźmy do|oto (?:szczegółowe )?(?:zestawienie|omówienie))\b"),
    },
}

EMOJI_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅]")
HEADING_RE = re.compile(r"(?m)^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$")
BOLD_LEADIN_RE = re.compile(r"(?m)^\s*(?:[-*•+]|\d+[.)])\s+(?:\S+\s+)?\*\*[^*\n]{1,60}\*\*:?")
BULLET_RE = re.compile(r"(?m)^\s*(?:[-*•+]|\d+[.)])\s+\S")
CODE_RE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
URL_RE = re.compile(r"https?://\S+")
ZERO_WIDTH_RE = re.compile("[\u200b-\u200f\u2060\ufeff]")

PL_TYPO = {
    "straight_quotes": (1, r"\"[^\"\n]{1,200}\""),
    "english_quotes": (1, r"“[^”\n]{1,200}”"),
    "period_inside_quote": (1, r"\w[.,][”\"](?=\s|$)"),
    "unspaced_em_dash": (2, r"[^\W\d_]—[^\W\d_]"),
    "comma_after_opening_adverb": (1, r"(?m)(?:^|[.!?]\s+)(?:Dodatkowo|Ponadto|Jednakże|Jednak|Natomiast|Również),"),
    "camelcase_hashtag": (0.5, r"#[A-ZĄĆĘŁŃÓŚŹŻ][a-ząćęłńóśźż]+[A-ZĄĆĘŁŃÓŚŹŻ]\w*"),
}

PL_MARKERS = set("i w nie się na że to jest z do jak o po co ale dla od czy są tak już jego jej przez ich także oraz".split())
EN_MARKERS = set("the and of to is that in it for with as was on are be this by not or have from".split())


def load_lexicon(lang):
    data = json.loads((HERE / "lexicon" / f"{lang}.json").read_text(encoding="utf-8"))
    return [(re.compile(e["pattern"], re.I), e["weight"], e["category"], e["pattern"]) for e in data["entries"]]


def detect_lang(text):
    words = re.findall(r"[^\W\d_]+", text.lower())
    pl = sum(w in PL_MARKERS for w in words) + 3 * len(re.findall("[ąćęłńśźż]", text.lower()))
    en = sum(w in EN_MARKERS for w in words)
    return "pl" if pl > en else "en"


def strip_code(text):
    return URL_RE.sub(" ", CODE_RE.sub(" ", text))


def split_sentences(text):
    body = HEADING_RE.sub("\n", text)
    body = re.sub(r"(?m)^\s*(?:[-*•+]|\d+[.)])\s+", "\n", body)
    body = re.sub(r"[*_]{1,3}", "", body)
    parts = re.split(r"(?<=[.!?…])\s+(?=[\"„“(«»A-ZĄĆĘŁŃÓŚŹŻ0-9])|\n{1,}", body)
    return [p.strip() for p in parts if len(re.findall(r"\w+", p)) >= 2]


def line_of(text, pos):
    return text.count("\n", 0, pos) + 1


def snippet(text, start, end, pad=30):
    s = text[max(0, start - pad):min(len(text), end + pad)].replace("\n", " ")
    return ("…" if start > pad else "") + s + ("…" if end + pad < len(text) else "")


def is_title_case(heading):
    words = re.findall(r"[^\W\d_]+", heading)
    if len(words) < 3:
        return False
    rest = [w for w in words[1:] if len(w) > 3 or w[0].isupper()]
    if len(rest) < 2:
        return False
    return sum(w[0].isupper() for w in rest) / len(rest) >= 0.75


def saturate(x, scale):
    return 1 - math.exp(-max(0.0, x) / scale)


def score(text, lang="auto"):
    # Layer 0: hidden characters are a red flag of "detector evasion" tools, not of style.
    zero_width = len(ZERO_WIDTH_RE.findall(text))
    text = unicodedata.normalize("NFKC", ZERO_WIDTH_RE.sub("", text))
    if lang == "auto":
        lang = detect_lang(text)
    clean = strip_code(text)
    words = re.findall(r"[^\W\d_][\w'’-]*", clean)
    n_words = max(len(words), 1)
    per_k = 1000 / n_words
    matches = []

    def hit(kind, name, weight, m):
        matches.append({
            "kind": kind, "name": name, "weight": weight, "line": line_of(clean, m.start()),
            "text": m.group(0).strip(), "context": snippet(clean, m.start(), m.end()),
        })

    lex_sum = 0.0
    for rx, w, cat, pat in load_lexicon(lang):
        for m in rx.finditer(clean):
            lex_sum += w
            hit("lexicon", cat, w, m)

    tmpl_sum = 0.0
    for name, (w, pat) in TEMPLATES[lang].items():
        for m in re.finditer(pat, clean):
            tmpl_sum += w
            hit("template", name, w, m)

    headings = HEADING_RE.findall(clean)
    title_case = [h for h in headings if is_title_case(h)]
    for h in title_case:
        tmpl_sum += 0.5 if lang == "en" else 0
    bold_leadins = len(BOLD_LEADIN_RE.findall(clean))
    bullets = len(BULLET_RE.findall(clean))
    emoji = len(EMOJI_RE.findall(clean))
    paragraphs = max(len([b for b in re.split(r"\n\s*\n", clean) if b.strip()]), 1)
    md_ratio = (len(headings) + 2 * bold_leadins + bullets + emoji) / paragraphs

    em_dashes = clean.count("—")
    unspaced = len(re.findall(r"[^\W\d_]—[^\W\d_]", clean))
    dash_per_k = (em_dashes + (2 * unspaced if lang == "pl" else 0)) * per_k

    typo_sum = 0.0
    typo_counts = {}
    if lang == "pl":
        for name, (w, pat) in PL_TYPO.items():
            found = list(re.finditer(pat, clean))
            typo_counts[name] = len(found)
            for m in found:
                typo_sum += w
                hit("typography", name, w, m)
        typo_counts["title_case_headings"] = len(title_case)
        typo_sum += 2 * len(title_case)

    sentences = split_sentences(clean)
    lens = [len(re.findall(r"\w+", s)) for s in sentences]
    cv = statistics.pstdev(lens) / statistics.mean(lens) if len(lens) >= 3 else None
    tau = 0.55
    rhythm = max(0.0, tau - cv) / tau if cv is not None else 0.0
    flat_runs = sum(
        1 for i in range(len(lens) - 2)
        if max(lens[i:i + 3]) <= 1.25 * min(lens[i:i + 3])
    )
    starts = [re.findall(r"\w+", s)[0].lower() for s in sentences if re.findall(r"\w+", s)]
    anaphora = sum(1 for a, b in zip(starts, starts[1:]) if a == b)

    def concrete(s):
        if re.search(r"\d", s) or re.search(r"[„\"“«»]", s):
            return True
        toks = re.findall(r"[^\W\d_]+", s)
        return any(t[0].isupper() and len(t) > 1 for t in toks[1:])

    vague_ratio = 1 - sum(concrete(s) for s in sentences) / len(sentences) if sentences else 0.0

    sub = {
        "lex": saturate(lex_sum * per_k, 25),
        "tmpl": saturate(tmpl_sum * per_k, 12),
        "md": saturate(md_ratio, 1.2),
        "dash": saturate(dash_per_k, 10),
        "typo_pl": saturate(typo_sum * per_k, 6) if lang == "pl" else 0.0,
        "rhythm": rhythm,
        "vague": max(0.0, vague_ratio - 0.3) / 0.7,
    }
    weights = {"lex": 0.35, "tmpl": 0.25, "md": 0.15, "dash": 0.05, "typo_pl": 0.10, "rhythm": 0.05, "vague": 0.05}
    if lang != "pl":
        # Redistribute the Polish typography weight so EN scores use the same 0-100 range.
        weights = {k: (0 if k == "typo_pl" else v / 0.9) for k, v in weights.items()}
    total = round(100 * sum(weights[k] * sub[k] for k in sub))
    verdict = "human-like" if total <= 20 else "mixed" if total <= 50 else "AI-smell"

    return {
        "lang": lang,
        "score": total,
        "verdict": verdict,
        "words": len(words),
        "reliable": len(words) >= 80,
        "subscores": {k: round(v, 3) for k, v in sub.items()},
        "diagnostics": {
            "lexicon_points_per_1000w": round(lex_sum * per_k, 1),
            "template_points_per_1000w": round(tmpl_sum * per_k, 1),
            "headings": len(headings),
            "title_case_headings": len(title_case),
            "bold_leadins": bold_leadins,
            "bullets": bullets,
            "emoji": emoji,
            "paragraphs": paragraphs,
            "em_dashes": em_dashes,
            "unspaced_em_dashes": unspaced,
            "pl_typography": typo_counts,
            "sentences": len(sentences),
            "sentence_len_mean": round(statistics.mean(lens), 1) if lens else 0,
            "sentence_len_cv": round(cv, 3) if cv is not None else None,
            "flat_runs_of_3": flat_runs,
            "repeated_sentence_starts": anaphora,
            "vague_sentence_ratio": round(vague_ratio, 3),
            "commas_per_sentence": round(clean.count(",") / max(len(sentences), 1), 2),
            "parentheses": clean.count("("),
            "semicolons": clean.count(";"),
            "zero_width_chars_removed": zero_width,
        },
        "matches": sorted(matches, key=lambda m: (-m["weight"], m["line"])),
    }


def render(r, top):
    d = r["diagnostics"]
    out = [
        f"AI-smell score: {r['score']}/100 ({r['verdict']}) · lang={r['lang']} · {r['words']} words"
        + ("" if r["reliable"] else " · SHORT TEXT, low reliability"),
        "Subscores (0-1): " + ", ".join(f"{k}={v}" for k, v in r["subscores"].items()),
        f"Rhythm: {d['sentences']} sentences, mean {d['sentence_len_mean']} words, CV {d['sentence_len_cv']}, "
        f"{d['flat_runs_of_3']} flat runs of 3, {d['repeated_sentence_starts']} repeated starts",
        f"Markdown: {d['headings']} headings ({d['title_case_headings']} Title Case), {d['bold_leadins']} bold lead-ins, "
        f"{d['bullets']} bullets, {d['emoji']} emoji · em dashes {d['em_dashes']} ({d['unspaced_em_dashes']} unspaced)",
        f"Concreteness: {round(100 * d['vague_sentence_ratio'])}% sentences without numbers, names or quotes",
    ]
    if d["zero_width_chars_removed"]:
        out.append(f"WARNING: {d['zero_width_chars_removed']} zero-width characters found and ignored")
    if r["lang"] == "pl" and d["pl_typography"]:
        out.append("PL typography: " + ", ".join(f"{k}={v}" for k, v in d["pl_typography"].items() if v))
    out.append(f"\nTop matches ({min(top, len(r['matches']))} of {len(r['matches'])}):")
    for m in r["matches"][:top]:
        out.append(f"  L{m['line']:<4} [{m['kind']}:{m['name']} w={m['weight']}] {m['text']!r}  — {m['context']}")
    out.append("\nThis measures style, not authorship. Do not use it as evidence that a person used AI.")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text file, or - for stdin")
    ap.add_argument("--lang", default="auto", choices=["auto", "en", "pl"])
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    ap.add_argument("--top", type=int, default=25, help="how many matches to list")
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else Path(a.file).read_text(encoding="utf-8")
    r = score(text, a.lang)
    print(json.dumps(r, ensure_ascii=False, indent=2) if a.json else render(r, a.top))


if __name__ == "__main__":
    main()
