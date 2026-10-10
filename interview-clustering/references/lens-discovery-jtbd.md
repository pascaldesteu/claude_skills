# Lens: Discovery / Jobs-to-be-Done interviews

**Interviewee:** a customer or user talking about their own work, problems and behaviour.
**Purpose:** understand what progress they're trying to make, what gets in the way, and how they cope today.

## What to extract

1. **Job** (`job`) — the progress they're trying to make, in their context. Phrase the statement as *"When [situation], they want to [motivation], so they can [outcome]."* Include functional, emotional ("feel in control") and social ("look competent to my boss") dimensions when present.
2. **Trigger / struggling moment** (`trigger`) — the event that made the problem urgent or made them start looking for a solution. These are often the most actionable cards.
3. **Pains** (`pain`) — friction, failure, cost, risk. Capture the *consequence* (time lost, errors, stress, money) in the statement.
4. **Workarounds** (`workaround`) — spreadsheets, manual steps, duct-taped tools, people they ask. A workaround is strong evidence: they already pay with effort.
5. **Current solution** (`current_solution`) — what they use or hired, and why they chose it.
6. **Desired outcome** (`desired_outcome`) — how they'd measure success, ideally in their words ("close the month in 2 days instead of 5").
7. **Forces of progress:**
   - `push` — what's wrong with the current situation that pushes them to change
   - `pull` — what attracts them to a new solution
   - `anxiety` — fears about switching (cost, migration, risk, learning curve)
   - `habit` — what keeps them doing it the current way
8. **Context** (`context`) — team size, tools, frequency, who else is involved. Only when it matters for interpreting other cards.

## Evidence rules

- Prefer what they **did** over what they **say they would do**. Mark future/hypothetical statements `speculation`, and don't let them drive intensity above 1 unless there is supporting past behaviour.
- Feature requests ("you should add X") are a `desired_outcome` or `pull` card — record the underlying need in the statement; quote the request.
- **Intensity 3** requires a signal: money spent, time spent, workaround built, strong emotion, or escalation to a manager.
- If the interviewer asked a leading question ("Wouldn't it be great if…") and the participant just agreed, lower `evidence_level` to `speculation` and say so in the statement.

## Pitfalls

- Don't summarize the interview — extract discrete cards. A 45-min interview usually yields 15–40 cards.
- Don't merge two pains into one card because they appear in the same answer.
- Don't generalize beyond this participant ("users struggle with…"). Clustering happens later.
