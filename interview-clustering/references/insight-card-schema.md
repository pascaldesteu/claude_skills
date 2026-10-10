# Insight card schema

One card = one atomic piece of evidence from one interview. Small and specific beats broad: "Exports data to Excel every Friday to build the client report" rather than "Has reporting problems".

Write cards as a JSON array to `_synthesis/cards/<interview_id>.json`.

```json
{
  "id": "P03-07",
  "interview_id": "P03",
  "interview_type": "discovery",
  "participant": { "role": "Finance ops lead", "segment": "Mid-market" },
  "card_type": "workaround",
  "statement": "Rebuilds the monthly client report by hand in Excel because the tool's export drops custom fields.",
  "quote": "Every month I export everything and then spend half a day fixing it in Excel.",
  "location": "[14:32]",
  "evidence_level": "past_behavior",
  "intensity": 3,
  "research_questions": ["RQ2"],
  "tags": ["reporting", "export"]
}
```

## Fields

| Field | Required | Notes |
|---|---|---|
| `id` | yes | `<interview_id>-<nn>`, unique |
| `interview_id` | yes | Matches the transcript file name (`P03` → `transcripts/P03.txt`) |
| `interview_type` | yes | `discovery` or `stakeholder` |
| `participant` | yes | `role` and `segment`; use `"unknown"` rather than guessing |
| `card_type` | yes | See lists below |
| `statement` | yes | Researcher's paraphrase, one idea, specific, includes the *why* when known |
| `quote` | yes | **Verbatim** from the transcript, 1–3 sentences. Trim with `…` only between exact fragments. No quote → no card |
| `location` | no | Timestamp or line marker |
| `evidence_level` | yes | See below |
| `intensity` | yes | 1 = mentioned, 2 = clearly matters, 3 = strong emotion, cost, or effort spent |
| `research_questions` | no | RQ ids this card informs |
| `tags` | no | Free, lowercase; used as hints only — clustering must not just group by tag |

## `card_type`

Discovery / JTBD: `job`, `trigger`, `pain`, `workaround`, `desired_outcome`, `push`, `pull`, `anxiety`, `habit`, `current_solution`, `context`

Stakeholder / expert: `goal`, `constraint`, `decision_process`, `customer_assumption`, `market_insight`, `risk`, `metric`, `conflict`, `context`

## `evidence_level` (strongest → weakest)

- `observed_behavior` — seen or shown during the session (screen share, artifact shown)
- `past_behavior` — a specific thing they actually did ("last Tuesday I…")
- `opinion` — their view or preference about their own situation
- `speculation` — hypothetical or future ("I would probably use…", "it'd be nice if…")
- `hearsay` — about other people ("our customers want…", "users usually…")

Stakeholder statements about customers are almost always `hearsay` or `opinion` — that is expected and is what makes them hypotheses to test.
