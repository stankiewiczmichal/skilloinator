# AI-ism catalogue (EN + PL)

AI-isms are statistical patterns, not single forbidden words. Word lists age fast
("delve" and the em dash faded from newer models within a year). Structural
signals last longer: negative parallelism, triads, nominalisations, participle
clauses, missing specifics and Markdown layout. Fix those first.

Evidence levels: **A** peer-reviewed or controlled measurement, **B** vendor
documentation or a widely reported incident, **C** anecdote, **[H]** editorial
heuristic not yet measured on a corpus.

## 1. Taxonomy

| Level | Pattern | EN example | PL example | Durability | Fix |
|---|---|---|---|---|---|
| Lexical | "Style words" with high log-ratio | delve, intricate, tapestry, pivotal, underscore, landscape, foster, testament, enhance, crucial | kluczowy, kompleksowy, holistyczny, innowacyjny, synergia, transformacyjny | Low (rotate with model versions) | Plain word, or a fact instead of the adjective |
| Lexical | Polysyllables, nominalisations (1.5–2× human rate, A) | significant, increasingly, consequences, implementation | realizacja, implementacja, dokonanie analizy, w zakresie | High | Verb instead of noun: "przeanalizowaliśmy", not "dokonano analizy" |
| Phrase | Negative parallelism | It's not just X, it's Y | To nie tylko X – to Y; To nie kolejny kurs. To system. | High | One direct claim with a specific |
| Phrase | Rule of three | innovative, transformative, and groundbreaking | szybko, skutecznie i efektywnie | High | Keep one strong item or two; max 1 triad per 500 words |
| Phrase | False ranges | from intimate gatherings to global movements | od małych firm po globalne korporacje | Medium | Name the actual cases, or drop |
| Phrase | Inflated significance | stands as a testament, plays a vital role | stanowi świadectwo, odgrywa kluczową rolę | Medium | State the consequence (number, date, effect) or delete |
| Syntax | Participle clauses (2–5× human rate, A) | "…, leaning on his agility, dances…, evading…" | "…, podkreślając…, umożliwiając…" | High | Subordinate clause: bo / kiedy / więc / because / so |
| Syntax | Uniform sentence and paragraph length | — | — | High | Mix 3–6 word sentences with long ones; never 3 similar in a row |
| Structure | Markdown: headings, bold lead-ins in bullets, lists (Markdown alone gives 73.1% model attribution, A) | **Key Benefits:** … | **Kluczowe korzyści:** … | High in chat output | Prose paragraphs; lists only for genuinely enumerable content |
| Punctuation | Em dash, few commas, semicolons, almost no parentheses | — | pauza bez spacji (słowo—słowo) | Low/medium (Claude still over-uses dashes; GPT-5.x under-uses them) | Normal mix of commas, parentheses, semicolons |
| Typography | Title Case headings, wrong quotes for the language | How To Build A Brand | Jak Zbudować Markę; "tekst" | Medium | Sentence case; „…” in Polish |
| Discourse | Hedging, both-sidesing, summaries, offers of further help | It's important to note…; In conclusion…; Would you like me to… | Warto zauważyć…; Podsumowując…; Daj znać, jeśli… | Medium | Delete; take a position |
| Discourse | Sycophancy | You're absolutely right!; Great question! | Masz absolutną rację!; Świetne pytanie! | Version-dependent | Delete |
| Content | Generalities, no numbers, names or expert quotes | — | — | High | Add specifics **from the source only**; else mark `[DOPISZ KONKRET: …]` / `[ADD DETAIL: …]` |
| Chat artefacts | Refusals, knowledge cutoffs, preambles | As an AI language model…; As of my last training update… | Jako model językowy AI…; Oto… | High in pasted text | Delete |

## 2. English: phrases to remove or rewrite

Openers: "Certainly!", "Great question!", "Sure! Here's…", "In today's fast-paced
world/digital landscape…", "Let's dive in / delve into".

Hedges and fillers: "It's important to note that…", "It's worth noting…",
"Additionally,", "Moreover,", "Furthermore,", "Notably,".

Inflated significance: "stands as a testament to", "serves as a reminder",
"plays a vital/crucial/pivotal role", "underscores its importance",
"at the heart of", "the interplay between".

Promotional: "rich cultural heritage", "breathtaking", "stunning natural beauty",
"nestled", "vibrant", "bustling", "seamless", "game-changer", "paradigm shift",
"unlock the potential", "ever-evolving".

Closers: "In conclusion", "In summary", "Overall", "Ultimately", "I hope this helps",
"Let me know if…", "Feel free to…", "Would you like me to…", "If you want, I can…".

Fiction slop (Antislop, A): Elara, Kael, "voice barely above a whisper",
"heart hammered against her ribs", "a profound sense of", shimmered, flickered,
stammered, camaraderie, palpable.

## 3. Polish

### 3a. Openers and fillers

| Phrase | Category | Action |
|---|---|---|
| W dzisiejszych czasach…; W dzisiejszym dynamicznym świecie…; W erze cyfrowej… | opener | Delete; start with the point |
| W tym artykule przyjrzymy się…; Czy zastanawiałeś się kiedyś…; Wiele osób zadaje sobie pytanie… | opener | Delete |
| Nie sposób nie zauważyć, że… | opener | Delete |
| Warto zauważyć / zaznaczyć / podkreślić, że…; Należy zauważyć… | filler | Delete and rebuild the sentence (capital letter, syntax) |
| w kontekście… | filler | "w", "przy", "dla" |
| Kluczowym aspektem jest…; odgrywa kluczową rolę; ma kluczowe znaczenie | inflated | "jest ważny dla", "decyduje o", "wpływa na", or the fact |
| Co więcej…; Co ciekawe…; Mając na uwadze powyższe… | connector | Usually delete; "Poza tym", "Dlatego" |
| Na podstawie dostępnych danych… | hedge | Name the data, or delete |
| W skrócie… (mid-text) | summary | Delete |
| Podsumowując…; Reasumując…; Konkludując…; Mam nadzieję, że ten artykuł… | closer | Delete or merge into the last real sentence |
| Oto kilka… | list announcement | Start the list or the prose directly |
| Zagłębmy się w temat… | calque of "delve into" | Delete the sentence |

### 3b. Adjectives and nouns "without backing"

kluczowy, kompleksowy, holistyczny, innowacyjny, transformacyjny, rewolucyjny,
unikalny, synergia, dynamiczny, game-changer, przełomowy, bezprecedensowy.

Exception rule (Wolniewicz): an adjective with a specific next to it (number,
name, year) is fine. "Kluczowy" at most once per 1000 words.

### 3c. Calques from English

| Calque | English source | Natural Polish |
|---|---|---|
| oferta dedykowana (dla…) | dedicated to | oferta dla…, skierowana do… |
| odgrywa kluczową rolę | plays a key role | jest ważny, decyduje o… |
| Nie tylko… ale także… (overuse) | not only… but also | one sentence with a specific |
| stanowi świadectwo / jest testamentem [H] | stands as a testament | pokazuje, dowodzi |
| bogata mozaika / gobelin [H] | rich tapestry | delete |
| krajobraz (rynku, technologii) [H] | landscape | rynek, sytuacja |
| nawigować (przez zmiany) [H] | navigate | radzić sobie z… |
| adresować problem [H] | address an issue | zająć się problemem, rozwiązać |
| pozwala na + noun [H] | allows for | pozwala + infinitive |
| bazując na / w oparciu o (overuse) [H] | based on | na podstawie, według |
| mieć sens; robić różnicę; na koniec dnia [H] | make sense; make a difference; at the end of the day | być sensownym; zmieniać wiele; ostatecznie |
| many possessives: „zadbaj o swoje zdrowie i swoją rodzinę” [H] | your | „zadbaj o zdrowie i rodzinę” |
| dokonać analizy / przeprowadzić optymalizację [H] | nominalisation | przeanalizować / zoptymalizować |

### 3d. Chat artefacts and sycophancy

„Oczywiście!”, „Świetne pytanie!”, „Masz absolutną rację!”, „Mam nadzieję, że to
pomoże”, „Daj znać, jeśli…”, „Czy chcesz, żebym…”, „Jako model językowy AI…”.
Delete all of them.

### 3e. LinkedIn register

„To nie kolejny kurs. To system.”, „Bez ściemy. Bez bullshitu. Tylko konkret.”,
„I szczerze?”, CamelCase hashtags, ✅ and 🚀 as bullets.

## 4. Polish typography rules

| AI habit | Polish norm |
|---|---|
| Title Case headings („Jak Zbudować Silną Markę”) | Capital only at the start and for proper names; no full stop at the end |
| Straight "…" or English “…” quotes | „…”, nested ‚…’ or »…« |
| Full stop inside the closing quote: „tekst.” | After it: „tekst”. Same for commas |
| Unspaced em dash (słowo—słowo), Chicago style | Spaced dash; today usually the en dash „ – ”. One dash type per text (Poradnia PWN) |
| Dash in every other sentence | The dash is ~10% of Polish punctuation, but not in every sentence |
| Comma after an opening adverb („Dodatkowo, …”) | No comma |
| Oxford comma | No comma before „i” in a list |
| 12,500 / 3.5 | 12 500 / 3,5 |
| October 24, 2026 | 24 października 2026 r. |
| Number ranges 1914 - 1918 | 1914–1918 (en dash, no spaces) |
| One-letter words at line end | Non-breaking space after w, z, i, a, o, u (typesetting only) |
| „Ty” capitalised in every marketing sentence | Impersonal form or lower-case „ty”, per brand voice |
| American cultural references | Polish ones (złoty, Polish institutions, holidays) when the reader is Polish |

Also: avoid stacked possessive pronouns and „zostać” passives; prefer natural
theme → rheme word order over English order.

Note: the em dash is a legitimate Polish character, and Word, macOS, iOS and
WordPress insert dashes automatically. A single dash proves nothing; density and
missing spaces matter.

## 5. Model fingerprints (for diagnosis, not accusations)

| Model / version | Typical tics | Evidence |
|---|---|---|
| GPT-3.5 / early ChatGPT (2023) | "As an AI language model", "It's important to note", "In conclusion" | B |
| GPT-4 / Turbo (2023–24) | delve, underscore, intricate, meticulously | A |
| GPT-4o (2024–25) | "Certainly!", "Sure! Here's…", "such as", "overall", bold in every bullet, headings, camaraderie, palpable | A |
| GPT-4o (April 2025) | extreme sycophancy ("glazing"), rolled back | B |
| GPT-5.x (2025–26) | fewest em dashes, more triads than humans, goblins/gremlins tic | A/B |
| Claude 3.5 Sonnet | "according to the text", "based on", "appears to"; few bold/headings | A |
| Claude (Claude Code 2025) | "You're absolutely right!" | B |
| Claude (2026) | more em dashes than humans; triads, nominalisations, rare words | A |
| Gemini | italics for emphasis, short direct openings, simpler words; polysyllables (2026) | A |
| Grok | rich, expansive style close to ChatGPT | A |
| Llama / Gemma | "including", "such as", "Let me know if…"; Gemma fiction: Elara, shimmered | A |

Slop clusters within model families and differs between them. These profiles
date quickly; refresh them about every quarter.
