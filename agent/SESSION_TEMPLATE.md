---
layout: default
title: Interactive Session Template
---

# Interactive Session Template

An Interactive or Mock session needs a durable cursor in addition to the
generated lesson and its status. Save the following as
`learning/sessions/LESSON_ID.md`, or beside an independent profile under
`sessions/LESSON_ID.md`. Replace placeholders and quote the learner-local date.

```yaml
---
lesson_id: YYYY-MM-DD-topic-id
mode: interactive
stage: 1
updated_at: "YYYY-MM-DD"
next_action: await-learner-attempt
---
```

## Current unanswered prompt

Save the exact question or challenge the learner should answer next. Do not
include its withheld solution in this section.

## Attempts and feedback so far

Initially: no learner attempt. Later, append sanitized attempts, precise
feedback, remaining uncertainty and the next correction task. Distinguish an
observed answer from a hypothetical model answer. Do not infer a score from
silence or familiarity.

## Resume action

State what the agent should do on the next turn: await this answer, assess a
submitted attempt, reveal a worked example after the attempt, or ask the next
follow-up. Preserve the current lesson ID. A session note does not itself
complete a lesson or create a review event.

Write the note before ending each question/feedback turn and read it at the
start of the next session. Store only sanitized notes in this public repository;
Pages exclusion does not make committed material private. Private transcripts
belong outside the checkout.

[Daily skill](SKILL.md) · [Workflow](../docs/workflow.md)
