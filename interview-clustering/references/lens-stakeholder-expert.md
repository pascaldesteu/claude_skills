# Lens: Stakeholder / B2B expert interviews

**Interviewee:** an internal stakeholder (sales, support, leadership, CS), a partner, a buyer-side executive, or a domain expert speaking about the market, an organisation, or customers in general.
**Purpose:** capture constraints, organisational dynamics and expert knowledge — and make the stakeholder's beliefs about customers explicit so they can be tested against customer evidence.

## What to extract

1. **Goals** (`goal`) — business or organisational objectives they own or care about, with the metric if mentioned.
2. **Constraints** (`constraint`) — regulatory, security, procurement, integration, budget, technical or timeline limits. Include who imposes it.
3. **Decision process** (`decision_process`) — who initiates, evaluates, approves, pays and uses; buying triggers; approval steps; typical cycle length. In B2B this is often where adoption actually fails.
4. **Customer assumptions** (`customer_assumption`) — any claim about what customers need, do, or think. Record faithfully and *neutrally*; these become hypotheses in the report ("Sales believes customers churn because of price").
5. **Market insight** (`market_insight`) — competitors, trends, substitutes, pricing norms, industry practices.
6. **Risks** (`risk`) — what they fear could go wrong with the product, project or market.
7. **Metrics** (`metric`) — KPIs used to judge success, and current baselines.
8. **Conflicts** (`conflict`) — misalignment between teams, roles or incentives (e.g. "IT wants control, ops wants speed").
9. **Context** (`context`) — org structure, tooling, scale — only when it shapes other cards.

## Evidence rules

- Distinguish **first-hand** knowledge (their own role, their own decisions → `past_behavior` / `opinion`) from **second-hand** claims about customers or other teams (→ `hearsay`).
- An anecdote about a named customer account is stronger than a generalization; capture the anecdote as the quote and keep `evidence_level: hearsay`.
- Note the stakeholder's incentive in the statement when it plausibly colours the claim (e.g. a sales lead attributing lost deals to missing features).
- If the interview also contains the person's *own* use of a product or process, extract those parts with the discovery lens card types (`pain`, `workaround`, …) and `interview_type` still `stakeholder`.

## Pitfalls

- Don't treat seniority as evidence strength. A VP's opinion about users is still `hearsay`.
- Don't drop constraints because they aren't "insights" — in B2B they frequently decide what is feasible.
- Don't editorialize. Record the belief; the clustering step decides whether customer evidence supports it.
