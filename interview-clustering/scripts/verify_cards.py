#!/usr/bin/env python3
"""Validate insight cards, verify quotes against transcripts, and merge into one JSONL.

Usage:
    python3 verify_cards.py --cards _synthesis/cards --transcripts _synthesis/transcripts \
        --out _synthesis/cards.jsonl

Each cards file is `<interview_id>.json` (a JSON array of cards); its transcript is
`<interview_id>.txt`. Every card gets a `quote_check` field: exact | approximate | missing.
Standard library only.
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from pathlib import Path

REQUIRED = ["id", "interview_id", "interview_type", "participant", "card_type",
            "statement", "quote", "evidence_level", "intensity"]
INTERVIEW_TYPES = {"discovery", "stakeholder"}
CARD_TYPES = {
    # discovery / JTBD
    "job", "trigger", "pain", "workaround", "desired_outcome", "push", "pull",
    "anxiety", "habit", "current_solution", "context",
    # stakeholder / expert
    "goal", "constraint", "decision_process", "customer_assumption",
    "market_insight", "risk", "metric", "conflict",
}
EVIDENCE_LEVELS = {"observed_behavior", "past_behavior", "opinion", "speculation", "hearsay"}
APPROX_THRESHOLD = 0.85


def normalize(text):
    text = text.lower().replace("’", "'").replace("‘", "'")
    text = re.sub(r"\[\d{1,2}:\d{2}(?::\d{2})?\]", " ", text)  # timestamps
    text = re.sub(r"[^\w\s']", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def check_quote(quote, transcript_norm):
    # Ellipses mark trimmed quotes: every fragment must appear.
    fragments = [normalize(f) for f in re.split(r"\.\.\.|…", quote)]
    fragments = [f for f in fragments if f]
    if not fragments:
        return "missing"
    if all(f in transcript_norm for f in fragments):
        return "exact"
    worst = 1.0
    for f in fragments:
        if f in transcript_norm:
            continue
        m = SequenceMatcher(None, transcript_norm, f, autojunk=False)
        match = m.find_longest_match(0, len(transcript_norm), 0, len(f))
        # Compare the fragment to the transcript window around the longest common block.
        start = max(0, match.a - match.b)
        window = transcript_norm[start:start + len(f) + 20]
        worst = min(worst, SequenceMatcher(None, window, f).ratio())
    return "approximate" if worst >= APPROX_THRESHOLD else "missing"


def validate(card):
    problems = [f"missing field '{k}'" for k in REQUIRED if k not in card or card[k] in ("", None)]
    if card.get("interview_type") and card["interview_type"] not in INTERVIEW_TYPES:
        problems.append(f"unknown interview_type '{card['interview_type']}'")
    if card.get("card_type") and card["card_type"] not in CARD_TYPES:
        problems.append(f"unknown card_type '{card['card_type']}'")
    if card.get("evidence_level") and card["evidence_level"] not in EVIDENCE_LEVELS:
        problems.append(f"unknown evidence_level '{card['evidence_level']}'")
    if "intensity" in card and card["intensity"] not in (1, 2, 3):
        problems.append("intensity must be 1, 2 or 3")
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cards", required=True, type=Path)
    ap.add_argument("--transcripts", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args()

    merged, issues, seen_ids = [], [], set()
    checks = Counter()
    per_interview = defaultdict(Counter)

    card_files = sorted(args.cards.glob("*.json"))
    if not card_files:
        sys.exit(f"No card files found in {args.cards}")

    for path in card_files:
        interview_id = path.stem
        transcript_path = args.transcripts / f"{interview_id}.txt"
        transcript_norm = normalize(transcript_path.read_text(encoding="utf-8", errors="replace")) \
            if transcript_path.exists() else None
        if transcript_norm is None:
            issues.append(f"{interview_id}: transcript {transcript_path} not found")
        try:
            cards = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            issues.append(f"{path.name}: invalid JSON ({e})")
            continue
        if not isinstance(cards, list):
            issues.append(f"{path.name}: expected a JSON array of cards")
            continue

        for card in cards:
            cid = card.get("id", "?")
            for p in validate(card):
                issues.append(f"{cid}: {p}")
            if cid in seen_ids:
                issues.append(f"{cid}: duplicate id")
            seen_ids.add(cid)
            if card.get("interview_id") not in (None, interview_id):
                issues.append(f"{cid}: interview_id '{card['interview_id']}' differs from file '{interview_id}'")

            status = check_quote(card.get("quote", ""), transcript_norm) if transcript_norm else "missing"
            card["quote_check"] = status
            checks[status] += 1
            per_interview[interview_id][status] += 1
            if status == "missing":
                issues.append(f"{cid}: quote not found in transcript")
            merged.append(card)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with args.out.open("w", encoding="utf-8") as f:
        for card in merged:
            f.write(json.dumps(card, ensure_ascii=False) + "\n")

    participants = {(c.get("interview_id"), c.get("interview_type")) for c in merged}
    by_type = Counter(t for _, t in participants)
    print(f"Merged {len(merged)} cards from {len(card_files)} interviews -> {args.out}")
    print(f"Participants: " + ", ".join(f"{t}={n}" for t, n in sorted(by_type.items())))
    print(f"Quotes: exact={checks['exact']} approximate={checks['approximate']} missing={checks['missing']}")
    for iid in sorted(per_interview):
        c = per_interview[iid]
        print(f"  {iid}: {sum(c.values())} cards ({c['missing']} missing quotes)")
    if issues:
        print(f"\n{len(issues)} issue(s):")
        for i in issues:
            print(f"  - {i}")
        sys.exit(1)


if __name__ == "__main__":
    main()
