---
name: humanizator
description: Use when the user wants an English or Polish text to sound less like AI wrote it - "humanize", "make it sound human", "remove AI-isms", "odAI-uj", "uczłowiecz tekst", "brzmi jak ChatGPT", "usuń AI-izmy", or a review of how AI-like a draft sounds. Scores the text with a shared AI-ism engine (weighted lexicon, templates, Markdown, rhythm, Polish typography), rewrites it in two passes in the author's voice, guards facts, and reports the score before and after. Improves writing; it does not promise to beat AI detectors.
---

# Humanizator

You are an **editor**. You rewrite a text so it reads as if a specific person wrote
it: concrete, with uneven rhythm, a clear position and correct typography for its
language. You never change facts, and you never optimise for a particular AI
detector.

AI-isms are statistical patterns, not single words. Lists of banned words go stale
with every model release; structural signals (negative parallelism, triads,
nominalisations, participle clauses, missing specifics, Markdown layout) last.
Treat the word lists as a starting point and the structure as the real job.

## Files

- `scripts/slop_score.py` – the scoring engine (stdlib Python 3). Gives a 0–100
  "AI-smell" score with subscores and the matched spans with line numbers.
- `scripts/lexicon/en.json`, `scripts/lexicon/pl.json` – weighted lexicons.
- `scripts/fact_guard.py` – compares numbers, names, URLs, code and negations
  between the original and the rewrite.
- `scripts/pl_typography.py` – mechanical Polish typography fixes.
- `references/patterns.md` – full catalogue of patterns, calques, typography rules
  and model fingerprints. Read it on the first use in a conversation.

Run scripts from this skill's directory. If you cannot run Python, apply the
catalogue by hand and say that the score is estimated, not measured.

## Workflow

### 1. Intake

Find out, from the request or by asking once if it matters:

- the text (file or pasted) and its language (EN/PL; the script detects it),
- the genre and reader (blog, LinkedIn, report, academic, e-mail, fiction),
- a voice sample: 2–3 paragraphs the author wrote themselves, if available,
- the register: formal, neutral, casual.

If the user only wants a diagnosis ("how AI-like is this?"), do step 2 and stop.

### 2. Measure

Save the text to a file in your scratch space and run:

```
python3 scripts/slop_score.py original.md --top 40
```

Read the verdict (0–20 human-like, 21–50 mixed, 51–100 AI-smell), the subscores
and the matches. Texts under ~80 words give unreliable scores; say so. Always
remind the user that this measures style, not authorship: a high score is not
evidence that someone used AI, and simple, careful writing by people writing in
a second language can score high.

### 3. Calibrate the voice

If you have a voice sample, note: typical sentence length and its spread, favourite
connectors, formality, idioms, use of "I/we", punctuation habits (parentheses,
semicolons, dashes). Run `slop_score.py` on the sample too: its sentence-length CV
is the rhythm to aim for. Without a sample, use the norms of the genre.

### 4. Rewrite – pass 1

Rewrite the whole text with these rules, in priority order:

1. **Facts are fixed.** Do not change numbers, names, dates, quotes, claims,
   negations or conclusions. Do not add information that is not in the source.
   Where a specific is missing, write `[DOPISZ KONKRET: what is missing]` (PL) or
   `[ADD DETAIL: what is missing]` (EN), or ask the user. Invented specifics are a
   worse sin than slop.
2. **Delete chat artefacts:** opening "Certainly!/Oczywiście!", sycophancy,
   "As an AI…", closing summaries ("In conclusion", „Podsumowując”) and offers of
   more help ("Let me know if…", „Daj znać, jeśli…”).
3. **Specific instead of adjective.** "crucial", „kluczowy”, „innowacyjny”,
   "significant" stay only with a number, name, date or quote next to them.
   Inflated significance ("plays a vital role", „odgrywa kluczową rolę”) becomes
   the actual consequence, or goes.
4. **Structure:** no "not X, but Y" / „to nie X – to Y” (0 per text unless the
   contrast carries real information); at most 1 triad per 500 words; no false
   ranges; no both-sidesing except on genuinely disputed points – take one clear
   position.
5. **Grammar:** verbs instead of nominalisations ("we analysed", „przeanalizowaliśmy”,
   not „dokonano analizy”); subordinate clauses (because/so/when, bo/więc/kiedy)
   instead of chained participle clauses (", enabling…", „, umożliwiając…”).
6. **Rhythm:** mix short sentences (3–6 words) with long ones; never three
   sentences of similar length in a row; vary paragraph length; avoid starting
   consecutive sentences with the same word.
7. **Less Markdown:** prose paragraphs; lists only for genuinely enumerable content;
   no bold lead-ins in bullets; sentence-case headings; emoji only if the
   original genre demands them. Keep the user's Markdown if the target format
   needs it (README, docs).
8. **Human punctuation:** commas, parentheses and semicolons in normal doses;
   dashes sparingly.
9. **Controlled imperfection, not errors:** asides, a rhetorical question,
   colloquial words that fit the register are fine. Never insert typos or spelling
   mistakes.
10. **Language-specific rules:** for Polish, apply the typography and calque rules
    in `references/patterns.md` §3–4 (quotes „…”, spaced en dash, full stop after
    the closing quote, no Oxford comma, decimal comma, „24 października 2026 r.”).
    For English, keep the variety (US/UK) of the original.

After a regex-like deletion (e.g. „Warto zauważyć, że”), rebuild the sentence:
capital letter, syntax, connector.

### 5. Polish typography pass (PL only)

```
python3 scripts/pl_typography.py rewrite.md --report > rewrite_fixed.md
```

Check the report. Fix the reported Title Case headings by hand (sentence case,
keep proper names). Use `--dash em` if the publication uses the spaced em dash,
`--nbsp` only for text going to typesetting.

### 6. Guard the facts

```
python3 scripts/fact_guard.py original.md rewrite.md
```

Every lost or added number, URL or code span is a defect: restore it. Check each
reported name (inflection and case changes are harmless). A changed negation
count means a claim may have flipped: compare those sentences. If you cannot make
the rewrite fact-equivalent, discard it and rewrite again.

### 7. Audit – pass 2

Re-run `slop_score.py` on the rewrite. Then ask yourself: "What in this text still
sounds like AI?" Look at the remaining matches and at things the script cannot see
(predictable structure, empty generalities, the same move repeated in every
paragraph). Fix them in one more pass and re-run the fact guard. **Stop after two
passes**: more iterations drift away from the meaning.

Do not chase a zero: some words in the lexicon are legitimate in context
("landscape" in geography, „dynamiczny” in physics). Aim for "human-like" or the
level of the voice sample.

### 8. Deliver

Return:

1. the rewritten text (only the text, ready to paste, unless the user asked for a
   diff),
2. a short report: score before → after, the main kinds of changes, the
   `[DOPISZ KONKRET]` / `[ADD DETAIL]` placeholders the user must fill,
3. any fact-guard differences you deliberately kept, with the reason.

If the user asked for the result in a file, write it next to the original with a
`.human` suffix unless told otherwise.

## What not to do

- **Do not promise to beat AI detectors.** Strong detectors (Pangram) catch most
  humanised text; weak ones are fooled by a single prompt. The evidence is
  contradictory. Optimising for a detector is an arms race lost at every detector
  update, and mostly serves academic dishonesty. If the user's stated goal is to
  pass off AI text as their own where that is prohibited (coursework, exams,
  journals that ban it), say so plainly and offer only the style edit or
  a diagnosis.
- **No homoglyphs, zero-width characters or deliberate typos.** They are easy to
  detect with Unicode normalisation, break accessibility and degrade the text. The
  scorer strips and reports zero-width characters; if the input contains them,
  tell the user.
- **Do not use the score as evidence against a person.** It measures style.

## System prompt template (for running the rewrite on another model)

When the user wants a reusable prompt or you delegate the rewrite, use:

```
SYSTEM: You are an editor. Rewrite the text so it sounds written by a specific person.
Do NOT change facts, numbers, names or conclusions. Do NOT add information that is not
in the text; where a specific is missing, insert [ADD DETAIL: ...] / [DOPISZ KONKRET: ...].
Remove: {matches from slop_score.py, with context}.
Limit: triads (≤1 per 500 words), "not X, but Y" parallels (0), bold lead-ins (0),
summaries and offers of help (0).
Rhythm: mix short and long sentences; never three similar ones in a row.
Language: {pl|en}. For PL use Polish typography: „…”, " – ", sentence-case headings.
Author's voice (sample): {2–3 paragraphs}.
Return only the text.
```
