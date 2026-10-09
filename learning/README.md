# Learning state

`state.json` is the authoritative history, validated against
[`state.schema.json`](state.schema.json). Lesson front matter is a delivery
snapshot; subsequent status and assessment changes belong in state.

## State transitions

`generated → in_progress → completed`, or `generated → completed` when a learner
submits their attempt directly. Delivery alone never means completion. A
completed lesson requires a nonempty learner-evidence file. Assessment remains
optional; unassessed score dimensions are `null`, never zero. A zero is an actual
assessment. The agent must read the evidence before scoring; the CLI checks file
existence and structure, not whether a learner's reasoning is correct.

Each lesson records identity, mode, objectives, fingerprint, delivery/completion
dates, source references, Markdown path, score, weaknesses, evidence paths and
review dates. Reviews live in a separate array and never increment lesson count.
Domain counts and weak-concept summaries are derived from those records rather
than maintained as competing copies.

## Commands

From the repository root, install `python -m pip install -r requirements.txt`.
Supply the learner's local date explicitly. The initial profile uses
`Asia/Bangkok`; change it if the learner requests another timezone.

```sh
python scripts/learning.py next --date 2026-10-08
python scripts/learning.py record --lesson lessons/2026-10-08-messaging-idempotent-consumer.md --date 2026-10-08
python scripts/learning.py start 2026-10-08-messaging-idempotent-consumer --date 2026-10-08
```

The example is already registered in the checked-in state, so rerunning its
`record` command correctly rejects duplicate delivery. The following commands
are examples to run **after** a real attempt; they are not initial state:

```sh
python scripts/learning.py complete 2026-10-08-messaging-idempotent-consumer --date 2026-10-09 --evidence /path/to/learner-attempt.md
python scripts/learning.py review 2026-10-08-messaging-idempotent-consumer --date 2026-10-10 --evidence /path/to/retrieval-attempt.md
```

Optional `--assessment /path/to/assessment.json` accepts:

```json
{
  "score": {
    "technical": 3,
    "reasoning": 3,
    "implementation": null,
    "operations": 2,
    "communication": 3
  },
  "weak_points": ["Explain inbox retention and replay safety more precisely."]
}
```

The example scores demonstrate format only. Record them only when supported by
the learner's actual attempt. Partial assessment uses `null` for unobserved
dimensions.

`next` is read-only. It excludes delivered topics, exact fingerprints and obvious
objective duplicates, requires completed prerequisites, and favors source-direct
topics and domain rotation. It returns due reviews and pending lessons alongside
its candidate. It does not perform semantic reasoning; the agent must compare
objectives and reject paraphrased repeats before creating a lesson.

If no candidate qualifies, resume pending prerequisites or add a source-grounded
topic with a distinct objective. Do not silently mark prerequisites completed.

## Review dates and missed reviews

Intervals D+1, D+3, D+7, D+14 and D+30 start at **actual completion**, not lesson
generation. They are adjustable curriculum defaults, not a universal optimal
schedule. A generated lesson has no active due dates. One review command consumes
the earliest due interval for that lesson; it does not mark every overdue review
done. The agent can discuss a revised schedule with the learner when needed.

## Persistence and recovery

Interactive/Mock cursors use `sessions/LESSON_ID.md` beside the state file. The
agent follows [`SESSION_TEMPLATE.md`](../agent/SESSION_TEMPLATE.md), saving the
current unanswered prompt, stage, sanitized attempt/feedback and next action
before each turn ends, then reading it on resume. The CLI `start` command only
changes status; it does not save a cursor or transcript. Initial question
delivery is generated, and the first actual attempt starts in-progress work.
Private profile notes stay beside that private state, outside this checkout.

Commands validate before writing and replace the state file atomically. Run one
writer at a time: atomic replacement is not multi-agent conflict resolution.
Re-read state before saving and review the diff. Keep lessons and their state
record in the same commit; finish with `python scripts/validate.py`. When updating
state manually, preserve evidence, IDs and completed history.

Use `--state /path/to/state.json` **before** the subcommand for an independent
profile initialized from [`LEARNING_STATE_TEMPLATE.json`](../agent/LEARNING_STATE_TEMPLATE.json).
Do not overwrite an existing learner history with the template.

Legacy schema v1 was a blank scaffold in this repository. Its template is replaced
with v2, not fabricated history. If an external profile has real v1 records, map
records individually: missing creation/status/evidence must be resolved, unknown
scores become `null`, and unproven completion stays pending. Back up that profile
and validate the migrated state before replacing it.

If filesystem writes are unavailable, return the complete lesson and proposed
state JSON/patch. State clearly that they have not been saved and request the
current state on a subsequent session. Never claim persistence from chat alone.

## Privacy

Pages excludes `learning/`, but this is a public GitHub repository. Committed
state, scores and evidence are still publicly readable on GitHub. Keep sensitive
attempts outside the repository, use a private local profile if needed, and
record only sanitized learning information in shared state. Paths themselves
must not expose private identities. Public example state contains no learner
performance.
