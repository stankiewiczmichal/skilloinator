---
name: slopperoinator
description: Use when the user wants deliberately AI-sounding text in English or Polish - "slop", "max slop", "make it sound like ChatGPT/Claude/Gemini", "parody of AI writing", "napisz jak ChatGPT", "zaslopuj", "tekst 10 na 10 AI", LinkedIn-bro parodies, or examples of AI-isms for training, workshops or testing a detector or humanizer. Generates or converts text with controllable slop density (knobs 0-10), model personas and a rule-based amplifier that injects AI-isms until a shared scoring engine reaches a target score. Parody only; no impersonation of real people.
---

# Slopperoinator

You produce **slop on purpose**: text full of AI-isms, at a density the user
controls. Typical uses: parody and humour, workshop and training material
("spot the AI-ism"), test data for a detector or for the `humanizator` skill,
and before/after examples.

AI-isms are statistical patterns. The funniest and most recognisable slop combines
the lexicon (delve, tapestry, kluczowy, holistyczny) with structure: "not X, it's
Y", triads, inflated significance, bold lead-ins, Title Case headings, emoji
bullets, sycophantic openers and offers of more help.

## Files

- `scripts/slop_score.py` – the scoring engine shared with `humanizator`
  (0–100 "AI-smell" score with matches).
- `scripts/lexicon/en.json`, `scripts/lexicon/pl.json` – weighted lexicons; mine
  them for vocabulary.
- `scripts/slop_amplify.py` – rule-based amplifier that injects AI-isms step by
  step until the score reaches `--target`.
- `references/personas.md` – knobs, the ten-out-of-ten templates (EN/PL), slop
  kits, model personas and meme formats. Read it on the first use in a
  conversation.

Run scripts from this skill's directory. If you cannot run Python, write the slop
by hand from the reference and say that the score is estimated.

## Workflow

### 1. Settings

Take from the request, or use defaults without asking:

| Setting | Default |
|---|---|
| language | the language of the request |
| mode | `generate` (new text on a topic) or `convert` (slop up a given text) |
| target score | 85/100 ("max slop", „10 na 10” → 95) |
| knobs (see `references/personas.md` §1) | all at the level implied by the target; "max" = all 10 |
| persona | `gpt4o`; or the model the user names |
| genre | blog post; or LinkedIn post, e-mail, product description, essay, fiction |
| length | 150–300 words |

### 2. Write the draft

Write the slop yourself, following the persona and knobs:

- Start from the ten-out-of-ten template in `references/personas.md` §2 when the
  target is high, and adapt it to the topic and genre. Do not paste the template
  verbatim every time: vary which tics you use, so the parody stays fresh.
- In `convert` mode keep the facts and the order of the source and add the slop
  around and inside it (style words, hedges, triads, inflated significance,
  Markdown, persona opener and closer).
- For Polish, keep the grammar correct (inflect the topic, agree genders). The
  typography errors of AI (Title Case, unspaced em dash, "straight quotes") are
  part of the joke in max mode; grammar errors are not.
- Lower knobs mean fewer tics, not worse writing: at 3/10 the text should read
  like a plausible, mildly over-polished assistant answer.

### 3. Measure and amplify

Save the draft to your scratch space and score it:

```
python3 scripts/slop_score.py draft.md
```

If the score is below the target, either add more slop by hand (look at which
subscores are low: `lex`, `tmpl`, `md`, `dash`, `typo_pl`, `rhythm`, `vague`) or
run the amplifier:

```
python3 scripts/slop_amplify.py draft.md --target 85 --persona gpt4o --topic "remote work" > slop.md
```

The amplifier makes the result predictable whatever model wrote the draft, but its
injections are mechanical. Read the output and smooth anything that breaks the
grammar or the joke. For Polish, pass `--topic` in the nominative („praca zdalna”).

If the score overshoots a low target, remove tics until it fits. Report the final
score.

### 4. Deliver

Return the slop text and one line with its score and persona. If the user wants
the text for teaching or testing, also offer a short annotated list of the
AI-isms used (from the `slop_score.py` matches), or a clean version made with the
`humanizator` skill for a before/after pair.

## Ethics

- **Parody, not impersonation.** Personas imitate a *model's* style. Do not write
  slop in the name of a real, identifiable person, do not imitate a specific
  author or brand so that it could be taken as theirs, and do not produce fake
  reviews, testimonials or news meant to be taken as genuine.
- **Label it when it leaves the chat.** If the text goes into a file, a post or
  any public place, add a footer: `_AI parody. Generated on purpose._` /
  `_Parodia AI. Wygenerowane celowo._` (`slop_amplify.py --label`). Skip the
  label only for test data the user clearly keeps internal, and say so.
- **Not for framing people.** Do not generate slop to plant in someone else's work
  or to "prove" that a person used AI. A high score is a style measurement, not
  evidence of authorship.
- **Not for gaming detectors.** If the user needs test data for a detector, slop
  is fine; tuning text to evade a specific detector is out of scope (see the
  `humanizator` skill for the reasons).
