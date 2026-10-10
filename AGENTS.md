# Repository instructions

For daily lessons, follow [Daily Interview Mastery](agent/SKILL.md). Read the
catalog, source prompts, and `learning/state.json` before selecting a topic.
Support English and Vietnamese teaching using the shared localization workflow
in docs/localization.md. Explicit language requests override the optional
profile preference; otherwise default to English. Interview model answers stay
English by default. Language variants share one lesson ID and state record.
User instructions take precedence.

Select the topic autonomously when asked for a new lesson. Generated lessons are
already delivered content, not evidence of learning. Never infer completion,
scores, experience, or benchmark results. Reviews are separate from new lessons.
Use [Interview Method](agent/INTERVIEW_METHOD.md) for concise, accurate answers
and honest follow-up bridges; prepare for deeper questions rather than evading
them.

Save public, generic lessons in `lessons/`. Keep learner evidence free of names,
employer/customer details, secrets, or confidential incidents. Learning state
and evidence are excluded from the public Pages build, but **committing them to
this public repository still makes them public on GitHub**. Keep sensitive
evidence outside the checkout and omit it from commits.

Run `python scripts/validate.py` and
`python -m unittest discover -s tests -v` after curriculum/state/tool changes.
Keep original source URLs stable and preserve source provenance. Do not claim
that code, labs, or external behavior were tested unless they were actually
checked. Inspect `git diff` before committing.
