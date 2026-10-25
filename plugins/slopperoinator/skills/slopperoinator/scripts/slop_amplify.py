#!/usr/bin/env python3
"""Rule-based slop amplifier: inject AI-isms into a text until it reaches a target score.

Steps run in a fixed order (cheapest first) and the text is re-scored with
slop_score.py after each one, so the result lands near --target whatever model
wrote the draft.

Usage:
  python3 slop_amplify.py FILE [--lang auto|en|pl] [--target 85] [--persona NAME]
                          [--topic "remote work"] [--label] [--seed 1]
Personas: chatgpt35, gpt4o, gpt5, claude, gemini, grok, llama, fantasy, linkedin-pl
The amplified text goes to stdout, the step log to stderr.
"""
import argparse
import random
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from slop_score import detect_lang, score  # noqa: E402

SUBS = {
    "en": [
        (r"\bimportant\b", "crucial"), (r"\bkey\b", "pivotal"), (r"\bshows\b", "underscores"),
        (r"\bshow\b", "showcase"), (r"\blook at\b", "delve into"), (r"\bexplore\b", "delve into"),
        (r"\bimprove(s?)\b", r"enhance\1"), (r"\bimproved\b", "enhanced"), (r"\bmany\b", "a myriad of"),
        (r"\bcomplex\b", "intricate"), (r"\bcarefully\b", "meticulously"), (r"\barea\b", "realm"),
        (r"\buse(s?)\b", r"leverage\1"), (r"\bhelp(s?)\b", r"empower\1"), (r"\bsmooth\b", "seamless"),
        (r"\balso\b", "additionally"), (r"\bnew\b", "innovative"), (r"\bfull\b", "comprehensive"),
        (r"\bbig\b", "significant"), (r"\bencourage(s?)\b", r"foster\1"), (r"\bmarket\b", "landscape"),
    ],
    "pl": [
        (r"\bważn(y|a|e|ych|ym|ymi|ą|ej|ego)\b", r"kluczow\1"),
        (r"\bistotn(y|a|e|ych|ym|ymi|ą|ej|ego)\b", r"kluczow\1"),
        (r"\bpełn(y|a|e|ych|ym|ymi|ą|ej|ego)\b", r"kompleksow\1"),
        (r"\bcałościow(y|a|e|ych|ym|ymi|ą|ej|ego)\b", r"holistyczn\1"),
        (r"\bnowoczesn(y|a|e|ych|ym|ymi|ą|ej|ego)\b", r"innowacyjn\1"),
        (r"\bnow(y|a|e|ych|ym|ymi|ą|ej|ego)\b", r"innowacyjn\1"),
        (r"\bjest ważny dla\b", "odgrywa kluczową rolę w"),
        (r"\bPonadto\b", "Co więcej"), (r"\boferta dla\b", "oferta dedykowana dla"),
        (r"\bna podstawie\b", "w oparciu o"), (r"\bwspółpraca\b", "synergia"),
        (r"\brynek\b", "krajobraz rynku"),
    ],
}

PERSONAS = {
    "chatgpt35": {
        "en": ("As an AI language model, I don't have personal opinions, but here is an overview.",
               "It's important to note that results may vary. I hope this helps!"),
        "pl": ("Jako model językowy AI nie mam własnych opinii, ale oto przegląd tematu.",
               "Należy pamiętać, że wyniki mogą się różnić. Mam nadzieję, że to pomoże!"),
    },
    "gpt4o": {
        "en": ("Certainly! What a brilliant idea — let's dive in! 🚀",
               "I hope this helps! Would you like me to turn this into a checklist, a roadmap, or a LinkedIn post? 😊"),
        "pl": ("Oczywiście! Wspaniały pomysł — zagłębmy się w temat! 🚀",
               "Mam nadzieję, że to pomoże! Czy chcesz, żebym przygotował checklistę, plan działania albo post na LinkedIn? 😊"),
    },
    "gpt5": {
        "en": ("Short answer: yes — with caveats.",
               "If you want, I can turn this into a one-page brief (no goblins, I promise)."),
        "pl": ("Krótko: tak — z zastrzeżeniami.",
               "Jeśli chcesz, mogę zrobić z tego jednostronicowe podsumowanie (obiecuję: bez goblinów)."),
    },
    "claude": {
        "en": ("You're absolutely right! Based on the text, here's what stands out — clearly, concisely, and carefully.",
               "Let me know if you'd like me to adjust the tone, the length, or the structure."),
        "pl": ("Masz absolutną rację! Na podstawie tekstu widać kilka rzeczy — jasnych, konkretnych i ważnych.",
               "Daj znać, jeśli chcesz, żebym dopasował ton, długość albo strukturę."),
    },
    "gemini": {
        "en": ("Here's a *quick* overview.", "Let me know if you have any other questions!"),
        "pl": ("Oto *krótki* przegląd.", "Daj znać, jeśli masz jeszcze pytania!"),
    },
    "grok": {
        "en": ("Great question — and a rich, comprehensive one at that.",
               "Bottom line: it's not just hype — it's the future. Let me know if you want more."),
        "pl": ("Świetne pytanie — i to bogate, kompleksowe.",
               "Krótko: to nie tylko hype — to przyszłość. Daj znać, jeśli chcesz więcej."),
    },
    "llama": {
        "en": ("Sure! Here are some key points, including several important aspects such as context and impact.",
               "Let me know if you have any other questions!"),
        "pl": ("Jasne! Oto kilka kluczowych punktów, w tym ważne aspekty, takie jak kontekst i wpływ.",
               "Daj znać, jeśli masz jeszcze jakieś pytania!"),
    },
    "fantasy": {
        "en": ("Elara's voice was barely above a whisper, her heart hammering against her ribs.",
               "As the light shimmered and flickered, a profound sense of camaraderie settled over them, palpable."),
        "pl": ("Głos Elary był ledwie szeptem, a serce waliło jej o żebra.",
               "Gdy światło migotało i drżało, ogarnęło ich głębokie poczucie wspólnoty, niemal namacalne."),
    },
    "linkedin-pl": {
        "en": ("This isn't another course. It's a system.",
               "No fluff. No BS. Just results. Agree? 👇 #GrowthMindset #FutureOfWork"),
        "pl": ("To nie kolejny kurs. To system.",
               "Bez ściemy. Bez bullshitu. Tylko konkret. I szczerze? To działa. ✅ #RozwójOsobisty #PrzyszłośćPracy"),
    },
}
PERSONAS["default"] = PERSONAS["gpt4o"]

HEDGE = {"en": "It's important to note that ", "pl": "Warto zauważyć, że "}
OPENER_WORLD = {
    "en": "In today's fast-paced, ever-evolving digital landscape, {t} isn't just a trend — it's a paradigm shift.",
    "pl": "W dzisiejszym dynamicznym świecie {t} to nie tylko trend — to prawdziwa rewolucja.",
}
SIGNIFICANCE = {
    "en": "It stands as a testament to innovation, resilience, and transformation.",
    "pl": "Stanowi świadectwo innowacyjnego, kompleksowego i holistycznego podejścia.",
}
RANGE = {
    "en": "From small startups to global enterprises, {t} plays a pivotal role.",
    "pl": "Od małych firm po globalne korporacje — {t} odgrywa kluczową rolę.",
}
SUMMARY = {
    "en": "In conclusion, {t} underscores the intricate interplay between technology and humanity.",
    "pl": "Podsumowując, {t} ma kluczowe znaczenie dla przyszłości.",
}
HEADING = {"en": "## Understanding The Rich Tapestry Of {T}", "pl": "## {T}: Kluczowa Rola W Dzisiejszym Dynamicznym Świecie"}
EMOJI = ["🚀", "✨", "💡", "✅", "🔥", "🌟"]
EMOJI_END_RE = re.compile("[\U0001F300-\U0001FAFF☀-➿⭐✅]\\s*$")
DASH_BEFORE = {
    "en": r"(?<=\w), (?=(?:which|but|and|so|while|making|enabling|ensuring)\b)",
    "pl": r"(?<=\w), (?=(?:a|ale|bo|więc|który|która|które|co|dzięki|umożliwiając|sprawiając)\b)",
}


def title(s):
    return " ".join(w[:1].upper() + w[1:] for w in s.split())


def lower_first(s):
    return s[:1].lower() + s[1:] if s[:1].isupper() and not s[:2].isupper() else s


class Draft:
    """The draft as named blocks, so injected slop lands in a plausible place."""

    def __init__(self, text):
        self.opener, self.intro, self.summary, self.closer = "", "", "", ""
        self.heading = ""
        self.blocks = [b.strip("\n") for b in re.split(r"\n\s*\n", text.strip()) if b.strip()]
        self.bullets = ""

    def render(self):
        parts = [self.opener, self.heading, self.intro, *self.blocks, self.bullets, self.summary, self.closer]
        return "\n\n".join(p for p in parts if p) + "\n"

    def prose(self):
        """Indexes of body blocks that are plain paragraphs."""
        return [i for i, b in enumerate(self.blocks) if not b.lstrip().startswith(("#", "-", "*", "|", ">", "```", "1."))]


def step_subs(d, lang, rng, topic, persona):
    for pat, rep in SUBS[lang]:
        d.blocks = [re.sub(pat, rep, b, count=2) for b in d.blocks]


def step_persona(d, lang, rng, topic, persona):
    d.opener, d.closer = PERSONAS[persona][lang]


def step_world(d, lang, rng, topic, persona):
    d.intro = f"{OPENER_WORLD[lang].format(t=topic)} {SIGNIFICANCE[lang]}"


def step_heading(d, lang, rng, topic, persona):
    d.blocks = [re.sub(r"(?m)^(#{1,6})\s+(.+)$", lambda m: f"{m.group(1)} {title(m.group(2))}", b) for b in d.blocks]
    if not any(b.lstrip().startswith("#") for b in d.blocks):
        d.heading = HEADING[lang].format(T=title(topic))


def step_hedge(d, lang, rng, topic, persona):
    for i in d.prose()[1::2]:
        b = d.blocks[i]
        first = re.split(r"(?<=[.!?])\s", b, maxsplit=1)[0]
        if not first.endswith("?"):
            d.blocks[i] = HEDGE[lang] + lower_first(b)


def step_bullets(d, lang, rng, topic, persona):
    def bold(m):
        body = m.group(2)
        head, sep, rest = body.partition(": ")
        if not sep:
            words = body.split()
            head, rest = " ".join(words[:2]), " ".join(words[2:])
        return f"{m.group(1)}✅ **{title(head.strip('*'))}:** {rest}"

    had_list = False
    for i, b in enumerate(d.blocks):
        if re.search(r"(?m)^\s*[-*•]\s", b):
            had_list = True
            d.blocks[i] = re.sub(r"(?m)^(\s*[-*•]\s+)(?!✅)(.+)$", bold, b)
    if not had_list:
        label = {"en": "### Key Benefits:", "pl": "### Najważniejsze Korzyści:"}[lang]
        items = {
            "en": ["- ✅ **Enhanced Efficiency:** streamlines workflows, fosters collaboration, and unlocks potential.",
                   "- ✅ **Seamless Integration:** " + lower_first(RANGE["en"].format(t=topic)),
                   "- ✅ **Future-Proofing:** it's a true game-changer."],
            "pl": ["- ✅ **Zwiększona efektywność:** usprawnia procesy, wspiera współpracę i otwiera drzwi do nowych możliwości.",
                   "- ✅ **Dedykowane rozwiązania:** " + lower_first(RANGE["pl"].format(t=topic)),
                   "- ✅ **Synergia:** to prawdziwy game-changer."],
        }[lang]
        d.bullets = label + "\n" + "\n".join(items)


def step_summary(d, lang, rng, topic, persona):
    d.summary = SUMMARY[lang].format(t=topic)


def step_dashes(d, lang, rng, topic, persona):
    for i in d.prose():
        d.blocks[i] = re.sub(DASH_BEFORE[lang], " — ", d.blocks[i])


def step_emoji(d, lang, rng, topic, persona):
    for i in d.prose():
        if not EMOJI_END_RE.search(d.blocks[i]) and rng.random() < 0.6:
            d.blocks[i] = d.blocks[i].rstrip() + " " + rng.choice(EMOJI)


STEPS = [
    ("lexical substitutions", step_subs),
    ("persona opener and closer", step_persona),
    ("'in today's world' opener + inflated significance", step_world),
    ("Title Case headings", step_heading),
    ("hedges", step_hedge),
    ("bold lead-in bullets with ✅", step_bullets),
    ("summary paragraph", step_summary),
    ("em dashes", step_dashes),
    ("emoji", step_emoji),
]


def guess_topic(text, lang):
    m = re.search(r"(?m)^#{1,6}\s+(.+)$", text)
    if m:
        return m.group(1).strip().lower()
    return {"en": "this topic", "pl": "ten temat"}[lang]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", help="text file, or - for stdin")
    ap.add_argument("--lang", default="auto", choices=["auto", "en", "pl"])
    ap.add_argument("--target", type=int, default=85, help="stop once the score reaches this (0-100)")
    ap.add_argument("--persona", default="default", choices=sorted(PERSONAS))
    ap.add_argument("--topic", help="topic phrase for injected sentences (PL: use a form that fits after 'to'/'Rola')")
    ap.add_argument("--label", action="store_true", help="append a parody footer")
    ap.add_argument("--seed", type=int, default=1)
    a = ap.parse_args()
    text = sys.stdin.read() if a.file == "-" else Path(a.file).read_text(encoding="utf-8")
    lang = detect_lang(text) if a.lang == "auto" else a.lang
    topic = a.topic or guess_topic(text, lang)
    rng = random.Random(a.seed)

    current = score(text, lang)["score"]
    print(f"start: {current}/100 (target {a.target})", file=sys.stderr)
    draft = Draft(text)
    for name, fn in STEPS:
        if current >= a.target:
            break
        fn(draft, lang, rng, topic, a.persona)
        text = draft.render()
        current = score(text, lang)["score"]
        print(f"  + {name}: {current}/100", file=sys.stderr)
    if current < a.target:
        print(f"target not reached; the draft needs more slop from the model (now {current})", file=sys.stderr)
    if a.label:
        text = text.rstrip() + "\n\n---\n" + {"en": "_AI parody. Generated on purpose._", "pl": "_Parodia AI. Wygenerowane celowo._"}[lang] + "\n"
    sys.stdout.write(text)


if __name__ == "__main__":
    main()
