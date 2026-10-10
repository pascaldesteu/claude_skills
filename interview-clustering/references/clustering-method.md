# Clustering method

Input: `_synthesis/cards.jsonl` (verified cards). Output: `_synthesis/themes.json`.

## 1. Read everything first

Read all cards before forming any group. Note the total participants `N` per type (customers vs stakeholders) and per segment.

## 2. Bottom-up affinity grouping

- Group cards that point to the **same underlying problem or need**, even if the words differ ("I chase approvals over Slack" + "nobody knows who signed off" → approval visibility).
- Don't group by interview question, product area, or tag alone — those give topics, not insights.
- Start with small groups (3–8 cards), then merge only if a single insight statement honestly covers both.
- Prefer customer cards (`interview_type: discovery`) to define themes. Stakeholder cards attach to a theme as a separate "stakeholder view", or form their own themes about constraints, decision process or organisation.
- Aim for roughly 5–12 themes. More usually means insufficient merging; fewer usually means themes are vague.

## 3. Write insight statements

A theme title is a claim, not a label:

- Weak: "Reporting"
- Strong: "Finance leads rebuild client reports by hand every month because exports lose custom fields — costing about half a day each cycle."

Each theme records:

```json
{
  "id": "T03",
  "insight": "…",
  "so_what": "Why this matters for the decision / research question",
  "research_questions": ["RQ2"],
  "card_ids": ["P03-07", "P05-02", "S01-04"],
  "customer_participants": ["P03", "P05", "P08"],
  "stakeholder_participants": ["S01"],
  "segments": {"Mid-market": 3, "Enterprise": 0},
  "strength": "strong | moderate | weak",
  "stakeholder_alignment": "confirmed | contradicted | untested | n/a",
  "contradictions": ["P06-11"],
  "key_quotes": ["P03-07", "P05-02"]
}
```

## 4. Rate strength

Based on distinct **customer** participants and evidence quality, not card count:

- **strong** — ≥ 40% of customer participants (minimum 3), mostly `past_behavior`/`observed_behavior`, intensity 2–3.
- **moderate** — 2+ participants with concrete evidence, or many participants with mostly `opinion`.
- **weak** — 1 participant, or evidence is mostly `speculation`/`hearsay`. Keep it in the report as a signal worth investigating, never as a finding.

With small samples (N < 6), report `n/N` and avoid percentages.

## 5. Stakeholder vs customer reality

For every `customer_assumption` card, check whether customer evidence:

- **confirms** it (link the theme),
- **contradicts** it (high-value finding — surface it prominently),
- or leaves it **untested** (list as an open question for the next round).

## 6. Segment and contradiction scan

- For each theme, check whether it is concentrated in a segment. A theme that is strong in one segment and absent in another is often the most decision-relevant insight.
- Keep contradicting cards attached to the theme. Do not silently drop them.
- List outlier cards with high intensity that fit no theme — they may be early signals.

## Review checklist (for the evidence review agent)

For each theme, check:

1. Does the insight statement claim more than the cards show (scope, frequency, causality)?
2. Is the strength rating consistent with distinct customer participants and evidence levels?
3. Is any theme supported only by stakeholder `hearsay` but phrased as a customer finding?
4. Are there cards in the theme that actually describe a different problem?
5. Are contradicting cards missing from `contradictions`?
6. Are the key quotes the most representative, not just the most dramatic?
7. Is any important high-intensity card left out of all themes?

Return a list of concrete fixes: `{theme_id, issue, suggested_change}`.
