---
layout: default
title: Practice the Interview
locale: en
translation_key: interview
---

# Practice the interview

Answer the question first. Explain the mechanism, then show a failure case and the condition that would change your choice.

{% include prompt-box.html kind='interview' %}

## Practice now — five minutes

**Question:** “How would you stop a retried message from crediting an account twice?”

1. Speak for 30 seconds: direct answer → mechanism → boundary.
2. Extend to 90 seconds with one concrete failure timeline and a validation plan.
3. Defend: “Why not save the processed marker in its own transaction?”
4. Defend: “Does this also guarantee exactly one external payment?”

After answering fully, you may offer: “If the handler also publishes an event, the related boundary is the transactional outbox.” Prepare that topic before offering the bridge. Deeper questions are an opportunity to show reasoning, not something the method promises to prevent.

[Open the model answers](../lessons/2026-10-08-messaging-idempotent-consumer.md#recall) only after an attempt. Record your actual words; polished examples are not evidence of your performance.

[Back to the daily desk](../index.md) · [Interview method](../agent/INTERVIEW_METHOD.md)
