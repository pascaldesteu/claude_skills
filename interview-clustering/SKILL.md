---
name: interview-clustering
description: Synthesize a set of customer, user or stakeholder interviews for a product discovery project into clustered themes, evidence-backed insights and opportunities. Uses type-specialized extraction agents (discovery/JTBD, stakeholder/B2B expert) feeding a single cross-interview clustering pass and an evidence review. Use whenever someone shares several interview transcripts, notes or recordings' text and asks to cluster, synthesize, affinity-map, find themes, extract insights or summarize "what customers said", even if they don't say "clustering".
---

# Interview Clustering

Turn a batch of interviews into a traceable insight report a product team can act on.

The design principle: **specialize extraction, centralize clustering.** Each interview type needs a different lens to pull out the right evidence, but themes must be formed across *all* interviews at once — otherwise they fragment along interview type instead of customer problem.

```
transcripts ─► 1 Intake & classify ─► 2 Extract (1 agent / interview, type lens) ─► insight cards
                                                                                        │
            report ◄─ 6 Write ◄─ 5 Evidence review ◄─ 4 Cluster (single pass) ◄─ 3 Verify quotes
```

## 0. Frame the study (before reading transcripts)

Collect, from the conversation or a brief the user provides:

- **Project goal and research questions** (RQ1, RQ2…). Clustering without them produces generic themes.
- **Segments** that matter (e.g. role, company size, plan, persona).
- **Decision the research should inform** (e.g. "which problem to build for in Q1").

If research questions are missing, ask once, in a single short question, and offer to infer draft RQs from the transcripts instead. Do not block on segments; infer them from transcripts if absent.

## 1. Intake & classify

1. Create a working folder `_synthesis/` next to the transcripts (or in the location the user specifies) with `transcripts/`, `cards/`.
2. Convert every input to plain text in `_synthesis/transcripts/<ID>.txt` (docx → use pandoc or python-docx; pdf → pdftotext; vtt/srt → strip timestamps but keep them as `[mm:ss]` markers). Keep line structure so quotes can be located.
3. **Pseudonymize**: assign IDs `P01, P02…` for customers and `S01, S02…` for stakeholders/experts. Replace participant names in outputs; keep the mapping only in `_synthesis/participants.md`, and tell the user that file contains personal data.
4. Classify each interview:
   - `discovery` — a customer/user talking about their own work, problems and behaviour.
   - `stakeholder` — an internal stakeholder, partner, buyer-side executive or domain expert talking about the market, organisation or customers *in general*.
   - If an interview mixes both (common in B2B), classify by its dominant mode and let the extractor apply both lenses.
5. Write `_synthesis/participants.md`: ID, type, role, segment, date, source file. Show it to the user as a compact table and continue unless something is clearly wrong.

## 2. Extract insight cards — one agent per interview

Spawn one subagent per interview, in parallel (batches of ~8 if there are many). Each agent receives:

- the transcript path,
- the research questions and segments from step 0,
- the lens for its type: `references/lens-discovery-jtbd.md` or `references/lens-stakeholder-expert.md`,
- the card format: `references/insight-card-schema.md`.

Prompt template for each agent:

> You are extracting evidence from one interview for a product discovery synthesis. Read `<lens file>` and `references/insight-card-schema.md`, then read the transcript `<path>` fully. Research questions: `<RQs>`. Produce insight cards following the schema and write them as a JSON array to `_synthesis/cards/<ID>.json`. Quotes must be copied verbatim from the transcript. Do not cluster or generalize across interviews — stay within this one. Return only a 3-line summary: card count, the 2 strongest signals, and anything surprising.

Why one agent per interview: each gets the full transcript in a fresh context, so detail isn't lost to summarization, and the type lens stays focused.

If subagents are unavailable, do the same extraction sequentially, one interview at a time, writing each card file before moving on.

## 3. Verify quotes

Run:

```bash
python3 scripts/verify_cards.py --cards _synthesis/cards --transcripts _synthesis/transcripts --out _synthesis/cards.jsonl
```

It validates the schema, checks every quote against its transcript (`exact` / `approximate` / `missing`) and merges all cards. Fix or drop cards with `missing` quotes before clustering — an insight with a fabricated quote destroys trust in the whole report.

## 4. Cluster — single pass across all interviews

Done by you (the orchestrator) or one dedicated agent with all cards in context. Follow `references/clustering-method.md`. In short:

1. Bottom-up affinity grouping of cards by underlying customer problem, not by interview type or by the question asked.
2. Name each theme as an **insight statement** (a claim with a "because"), not a topic label.
3. Count **distinct participants**, not cards. Report `n/N` and segment breakdown.
4. Keep stakeholder cards as a separate evidence class: they are hypotheses *about* customers, not customer evidence. Show where stakeholder beliefs are confirmed, contradicted or untested by customer interviews.
5. Keep contradictions and outliers visible.

Write `_synthesis/themes.json` (theme id, insight statement, card ids, participant ids) so the report stays traceable.

## 5. Evidence review

Spawn one reviewer agent (fresh context) with `themes.json`, `cards.jsonl` and `references/clustering-method.md` § "Review checklist". Its job is adversarial: find themes whose statement overreaches the evidence, single-participant themes presented as patterns, missed contradictions, and cards misattributed to a theme. Apply its fixes or note why not.

## 6. Write the report

Fill `assets/report-template.md` and save it as `_synthesis/insights-report.md` (or the path the user asked for). Rules:

- Lead with the 3–5 insights that matter most for the decision from step 0.
- Every insight carries strength (`n/N` participants, evidence level) and 1–3 verbatim quotes with participant IDs.
- Use participant IDs only — never real names — in the report.
- Separate what was **heard** (insights) from what we **recommend** (opportunities) and what we **still don't know** (open questions).

Finish by giving the user the report path and a 4–6 line summary in chat: top insights, the weakest-evidenced area, and the suggested next research step.

## Adding a new interview type

Create `references/lens-<type>.md` following the structure of the existing lenses (purpose, what to extract, card types, evidence rules, pitfalls), add its card types to `references/insight-card-schema.md`, and add the classification rule in step 1. Clustering and reporting need no change.
