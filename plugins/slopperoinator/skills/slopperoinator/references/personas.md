# Slop recipes, personas and meme formats

## 1. Knobs (0–10)

| Knob | 0 | 5 | 10 |
|---|---|---|---|
| `lexicon` – style words | none | one per paragraph | every sentence: delve, tapestry, pivotal / kluczowy, kompleksowy, holistyczny |
| `triads` – rule of three | none | one per paragraph | every list of adjectives has three items |
| `neg_parallel` – "not X, it's Y" | none | one per text | every paragraph |
| `emoji` | none | one per section | bullets, openers, closers |
| `markdown` – headings, bold lead-ins, lists | prose | headings + one list | Title Case headings, bold lead-ins on every bullet |
| `sycophancy` | none | "Great question!" | "What a brilliant, visionary idea!" |
| `hedging` | none | one "It's important to note" | every claim hedged, both-sidesed |
| `offers` – closing offers of help | none | one closer | closer with three options + emoji |
| `dashes` | none | one per paragraph | em dash in every sentence (PL max: unspaced) |
| `significance` – inflated importance | none | one "plays a pivotal role" | everything is a testament, a paradigm shift and a game-changer |
| `persona` | neutral | – | one of the personas below |

Default for "max slop" / „10 na 10”: all knobs at 10, persona `gpt4o`.

## 2. Ten-out-of-ten templates

### English

```
Certainly! Great question — let's delve into it. 🚀

## Understanding The Rich Tapestry Of {TOPIC}

In today's fast-paced, ever-evolving digital landscape, {TOPIC} isn't just a trend — it's a paradigm shift.
It stands as a testament to innovation, resilience, and transformation.

### Key Benefits:
- **Enhanced Efficiency:** Streamlines workflows, fosters collaboration, and unlocks potential.
- **Seamless Integration:** From small startups to global enterprises, it plays a pivotal role.
- **Future-Proofing:** It's important to note that the journey is just beginning.

In conclusion, {TOPIC} underscores the intricate interplay between technology and humanity.

I hope this helps! Would you like me to create a detailed roadmap, a checklist, or a LinkedIn post? 😊
```

### Polish

```
Oczywiście! Świetne pytanie — zagłębmy się w temat. 🚀

## Kluczowa Rola {TEMAT} W Dzisiejszym Dynamicznym Świecie

W dzisiejszych czasach {TEMAT} to nie tylko trend — to prawdziwa rewolucja.
Warto zauważyć, że stanowi on fundament innowacyjnego, kompleksowego i holistycznego podejścia.

### Najważniejsze Korzyści:
- ✅ **Zwiększona efektywność:** usprawnia procesy, wspiera współpracę i otwiera drzwi do nowych możliwości.
- ✅ **Dedykowane rozwiązania:** od małych firm po globalne korporacje — odgrywa kluczową rolę.
- ✅ **Synergia:** to prawdziwy game-changer.

Podsumowując, {TEMAT} ma kluczowe znaczenie dla przyszłości. Mam nadzieję, że to pomoże!
Daj znać, jeśli chcesz, żebym przygotował szczegółowy plan działania. 😊
```

In Polish max mode the typography errors (Title Case, unspaced em dash, straight
"quotes", full stop inside the quote: "tekst.") are part of the joke. Inflect
{TEMAT} correctly (genitive after „Rola”); grammatical errors are not funny, AI
style is.

## 3. Polish slop kit

- Openers: „W dzisiejszych czasach…”, „W dzisiejszym dynamicznym świecie…”, „W erze
  cyfrowej…”, „W tym artykule przyjrzymy się…”, „Czy zastanawiałeś się kiedyś…”,
  „Nie sposób nie zauważyć, że…”.
- Fillers: „Warto zauważyć/podkreślić, że…”, „Należy zaznaczyć…”, „w kontekście…”,
  „Co więcej…”, „Co ciekawe…”, „Mając na uwadze powyższe…”.
- Inflated: „odgrywa kluczową rolę”, „ma kluczowe znaczenie”, „Kluczowym aspektem
  jest…”, „stanowi świadectwo”, „otwiera drzwi do…”.
- Adjectives: kluczowy, kompleksowy, holistyczny, innowacyjny, transformacyjny,
  rewolucyjny, unikalny, synergia, dynamiczny, game-changer, przełomowy.
- Calques: „oferta dedykowana dla…”, „krajobraz rynku”, „nawigować przez zmiany”,
  „adresować problem”, „robi różnicę”, „na koniec dnia”, „w oparciu o”, „dokonać
  analizy”, „bogata mozaika”, „zagłębmy się”.
- Closers: „Podsumowując…”, „Reasumując…”, „Mam nadzieję, że ten artykuł…”,
  „Daj znać, jeśli…”, „Czy chcesz, żebym…”.

## 4. English slop kit

- Style words: delve, underscore, showcase, intricate, meticulous, pivotal, realm,
  tapestry, testament, landscape, foster, enhance, crucial, comprehensive,
  seamless, robust, leverage, holistic, synergy, transformative, groundbreaking,
  multifaceted, myriad, plethora, beacon, vibrant, bustling.
- Phrases: "In today's fast-paced world", "navigate the complexities", "unlock the
  full potential", "paradigm shift", "game-changer", "ever-evolving", "embark on a
  journey", "the interplay between", "at the heart of".
- Significance: "stands as a testament to", "serves as a reminder", "plays a
  pivotal role", "underscores its importance".
- Hedges: "It's important to note that", "It's worth noting".
- Closers: "In conclusion", "Overall", "I hope this helps!", "Let me know if…",
  "Would you like me to…", "Feel free to…".
- Fiction: Elara, Kael, "voice barely above a whisper", "heart hammered against her
  ribs", "a profound sense of", shimmered, flickered, stammered, camaraderie,
  palpable.

## 5. Model personas

Evidence level in brackets: **A** measured, **B** documented incident, **C** anecdote.

| Persona (`--persona`) | Tics |
|---|---|
| `chatgpt35` – "ChatGPT 3.5" | "As an AI language model, I cannot…", "It's important to note…", "In conclusion…", refusals and knowledge-cutoff disclaimers in the middle of the text (B) |
| `gpt4o` – "GPT-4o glazer" | "Certainly!", "What a brilliant idea!", bold on every bullet, headings, emoji, an em dash in every sentence, "camaraderie", "palpable" (A/B) |
| `gpt5` – "GPT-5.x" | terse, "Short answer: …", "If you want, I can…" (C); hardly any em dashes, more triads; an occasional goblin or gremlin in an unrelated context (B, 2026 meme) |
| `claude` – "Claude" | "You're absolutely right!" after every correction, "Based on the text…", "appears to", em dashes, triads, nominalisations (A/B) |
| `gemini` – "Gemini" | *italics* for emphasis, short direct opening, simpler words ("sugar", not "glucose") (A) |
| `grok` – "Grok" | rich, expansive style close to ChatGPT (A); "edgy" tone (C) |
| `llama` – "Llama/Gemma" | "including", "such as", "Let me know if you have any other questions!" (A) |
| `fantasy` – "Fantasy slop" | Elara, "voice barely above a whisper", "heart hammered against her ribs", "a profound sense of…", shimmered, flickered (A, Antislop) |
| `linkedin-pl` – "LinkedIn PL" | „To nie kolejny kurs. To system.”, „Bez ściemy. Bez bullshitu. Tylko konkret.”, „I szczerze?”, CamelCase hashtags, ✅ (practitioner lists) |

Personas are caricatures of a model's style, not of a person. Persona profiles date
quickly; the GPT-5.x one is partly anecdotal.

## 6. Meme formats

- "As an AI language model" pasted by mistake into a product review, a paper or a
  Wikipedia article.
- "You're absolutely right!" (the GitHub issue, the absolutelyright.lol counter,
  the "You Are Absolutely Right" music video).
- "Ha—great question!"
- The em dash joke: „pauza, więc pisał ChatGPT”.
- "delve" as the traitor word.
- The goblin ban in GPT-5.5 prompts.
- A corporate post with emoji bullets and "game-changer".
