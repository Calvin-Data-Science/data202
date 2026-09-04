---
name: gift-quiz-writer
description: Write a short retrieval/practice quiz as a GIFT-format .txt file, ready for Moodle import (Question bank > Import > GIFT format). Use when the user asks for a "retrieval quiz," "GIFT quiz," "Moodle quiz," or wants existing quiz questions converted to GIFT. Produces 5-8 questions by default, covering specified class content/readings, with full distractor feedback.
---

# GIFT-format retrieval quiz writer

Writes a low-stakes retrieval-practice quiz as a single `.txt` file in Moodle's
GIFT format. Works for any course — the content/topics come from what the
user points at (a reading, slides, a class session, a dataset); the format
and conventions below are course-agnostic.

## Before writing

Determine, from the user's request or by asking:
1. **Source content** — what the quiz should test (a reading, a class
   session's material, specific files/slides). Read the actual source
   material before writing questions — don't invent content.
2. **Question count** — default to **5–8 questions**. Only go outside that
   range if the user asks or the source content clearly needs more sections
   than 8 questions can cover well.
3. **Category / ID prefix** — a short label for `$CATEGORY:` and question
   IDs, e.g. `Week 03 / Retrieval 01` and `W03-R1`. If the user doesn't
   specify one, infer a reasonable one from filenames/folder structure
   (e.g. a `weeks/03/` folder → `Week 03`) or ask.
4. **Save location** — match existing project conventions if a quiz folder
   already exists (e.g. `weeks/NN/retrievalN.txt`); otherwise ask where to
   save it.

## File structure

```gift
// <Course/Week label> Retrieval Quiz — <short topic description> — GIFT format
// Import into Moodle: Question bank > Import > GIFT format
// <N> questions covering <what they cover, in 1-2 lines>

$CATEGORY: <Week/Unit label> / <Quiz label>

// ── Section 1: <Topic> ──────────────────────────────────────────────────────

::<ID>-Q1 <short question title>::
<Question stem text>{
=<correct answer> #Correct. <why this is right, tied to the concept>.
~<distractor 1> #<why this is wrong — name the specific misconception>.
~<distractor 2> #<why this is wrong>.
~<distractor 3> #<why this is wrong>.
}

// ── Section 2: <Topic> ──────────────────────────────────────────────────────

::<ID>-Q2 <short question title>::
...
```

Notes on the header comments:
- Line 1: quiz title + what it covers, ending "— GIFT format".
- Line 2: always include the literal Moodle import instruction, verbatim —
  it's the reminder the user relies on months later.
- Line 3+: a one-to-three-line summary of scope (what session/reading/pages
  it draws from), and question count.
- `$CATEGORY:` line needs a **blank line before and after** it (Moodle GIFT
  requirement).
- Use `// ── Section N: Title ──` comment dividers between topic groups so
  the file stays scannable — one section per sub-topic, not per question.
- Leave one blank line between questions.

## Question ID and title convention

`::<ID> <short title>::` — the title after the ID is optional in GIFT but
worth keeping; it's the label Moodle shows in the question bank list, and
future-you will thank present-you.

- ID pattern: `<WeekOrUnit>-<QuizLabel>-Q<n>`, e.g. `W03-R1-Q4`. Keep it
  short and grep-able. Reuse the same prefix across a whole quiz.
- If a question is a deliberate carry-over/review of an earlier quiz's
  question, say so in the title (`Q8 Review: <concept>`) and in the section
  comment, and reference which earlier quiz it came from in the feedback
  text — this is a good spaced-retrieval technique, use it when a concept
  from a prior session directly resurfaces in current material.

## Question types (GIFT syntax)

**Multiple choice** (the default; use for anything with plausible wrong answers):
```gift
::ID Title::
Question stem?{
=correct answer #Correct. Explanation.
~wrong answer 1 #Why this is wrong specifically.
~wrong answer 2 #Why this is wrong specifically.
~wrong answer 3 #Why this is wrong specifically.
}
```

**True/False** (use sparingly — good for one clear misconception per quiz, not the default):
```gift
::ID Title::
TRUE or FALSE: <statement>{
FALSE #Correct. <Explain what's actually true and why the statement is wrong>.
}
```

**Matching** (use for a set of 3+ terms mapped to definitions/categories):
```gift
::ID Title::Match each <thing> to its <property>.{
=Term A -> definition/category A
=Term B -> definition/category B
=Term C -> definition/category C
}
```
(Note: the question stem sits right after `::ID Title::` with no space
before the `{` opening the matching block — see how the intro sentence
attaches directly.)

**Short answer / wildcard** (rare — only for icebreakers or truly open prompts):
```gift
::ID::
Open-ended prompt? {=* #Feedback shown regardless of answer.}
```

Default to multiple choice for content questions. Use true/false only when
there's one crisp misconception worth testing directly. Use matching when
you have a clean list of term↔definition or category↔example pairs — it's
more efficient than several separate multiple-choice questions.

## Escaping — the actual rule (don't over-escape)

GIFT reserves exactly six characters: **`~ = # { } :`**. Escape one of
these with a backslash **only when it appears literally** in text and could
otherwise be parsed as GIFT syntax:

- Inside the answer block (between `{` and `}`) — stem or feedback text
  containing `=`, `~`, `#`, `{`, `}`, or `:` as literal characters (e.g.
  Python code with `==`, dict literals `{...}`, or slicing `x[::2]`) must
  have those characters escaped: `\=`, `\~`, `\#`, `\{`, `\}`, `\:`.
- In the **question stem before the opening `{`**, only `{` and `}` need
  escaping (they'd otherwise look like the start of the answer block).
  `=`, `~`, `#`, `:` do **not** need escaping there — the parser isn't
  looking for them yet.
- **Do not escape commas** — comma is not a GIFT reserved character.
  Escaping it is unnecessary and can leave a stray backslash in the
  rendered question in some parsers.
- When code contains a literal backslash-producing sequence of its own,
  escape gets nested rarely enough that it's easier to just re-read the
  rendered line once you're done and sanity-check it.

Examples from real code-based questions:
```gift
::ID::
Given label_map = \{'low': 0, 'medium': 1, 'high': 2\} and raw = ['high', 'low'], what does [label_map[r] for r in raw] produce?{
=[2, 0] #Correct. 'high' maps to 2 and 'low' maps to 0, in that order.
~[0, 2] #This would be the result for raw \= ['low', 'high'], not ['high', 'low'].
}
```
(`{`/`}` escaped even in the stem because they're literal dict braces;
`=` in the stem's `raw = [...]` is left unescaped since it's before the
answer block; `\=` inside the distractor's feedback IS escaped since that
text is inside `{ }`.)

```gift
~[x for x in range(10) if x % 2 \=\= 0] #Correct.
```
(`==` inside the answer block, both `=` escaped.)

## Writing good distractors and feedback

This is what makes retrieval quizzes worth running — always include it:

- **Every correct answer's feedback** starts with "Correct." then explains
  *why*, referencing the underlying concept (not just restating the answer).
- **Every distractor's feedback** names the *specific* misconception or
  mix-up it represents — which related-but-wrong concept, off-by-one error,
  or common confusion it corresponds to. Never just say "this is wrong";
  say what the student was probably thinking and why that's not it.
- Distractors should be plausible near-misses drawn from real confusions in
  the material (adjacent concepts, common code mistakes, reversed logic,
  off-by-one on indices/axes), not obviously-wrong filler.
- Keep stems concrete: reference actual variable/dataset/column names from
  the real source material rather than abstract placeholders — it's more
  memorable and tests applied understanding, not just terminology.

## Workflow

1. Read the actual source material the quiz is based on.
2. Draft 5–8 questions grouped into sections by sub-topic, in the order the
   material was presented.
3. Write correct-answer and distractor feedback for every question — no
   question ships without full feedback.
4. Escape only `~ = # { } :` where literal, per the rule above; leave
   commas alone.
5. Save as a `.txt` file at the location the user specified (or matching
   existing project convention).
6. Tell the user it's ready for **Moodle → Question bank → Import → GIFT
   format**, and mention the question count and what it covers.
