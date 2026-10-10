---
layout: default
title: Verification and Boundaries
---

# Verification and Boundaries

Run from the repository root. Content/state checks require the dependencies in `requirements.txt`.

```sh
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/package_labs.py --check
python scripts/render_lesson_code.py --check
python labs/atomic-inbox/verify.py --solution
```

The unit suite exercises selection → generated → attempt → completion → due review → evidence-backed adjustment in **temporary fixture profiles**. It checks duplicate objectives, incomplete prerequisites and rejection of unsupported progress. These tests do not create learner history in `learning/state.json`.

The lab checks the reference against happy path, replay, injected failure, missing account, conflicting identity and invalid amounts (five test methods). The starter intentionally fails exactly two transaction-boundary checks. Unit tests verify this teaching failure and the ZIP contents. Rebuild the download with `python scripts/package_labs.py` after lab edits.

## Jekyll and browser flow

CI uses the existing GitHub Pages Jekyll builder, then checks generated links, anchors and exclusions:

```sh
python scripts/check_site.py _site
```

Browser dependencies are for verification only. No framework, analytics, font service, test library or CDN script is added to the public UI.

```sh
python -m pip install -r requirements-browser.txt
python -m playwright install --with-deps chromium
npm install --prefix work/browser-checks --no-audit --no-fund axe-core@4.10.3
python tests/browser_check.py --site _site --axe work/browser-checks/node_modules/axe-core/axe.min.js
```

For an installed system Chromium, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE=/path/to/chromium`. Optional `--screenshots work/screenshots` captures the daily desk and lesson. The browser script serves the actual build locally at its configured base URL, so ordinary links and downloads are exercised.

The PR's site check uploads English and Vietnamese desktop/mobile screenshots as the `daily-learning-ui` artifact for review (retained for seven days).

CI also builds an isolated copy with a synthetic later bilingual lesson and runs the same browser checks. This catches fixed-size library assumptions, incorrect latest-lesson selection and resume accidentally opening the newest lesson instead of the saved one. The fixture is test-only; it neither changes repository state nor appears in the published site or UI screenshots.

Checks cover both locales: four daily actions, six-step navigation, same-lesson/step language switching, reload/back/forward, preferences/resume/clear, missing translations, identical rendered lab code, native keyboard answers, downloads and copied prompts. Invalid preferences/bookmarks, blocked storage/clipboard and no-JavaScript reading have explicit fallbacks. The rendered-site checker verifies self-canonical URLs, reciprocal hreflang, document languages and unique logical IDs. Axe runs WCAG 2 A/AA, WCAG 2.1 AA and best-practice rules on paired entry points, guides and lessons at 1440/390/320px, including an open worked solution. Automated checks do not constitute a complete accessibility audit or prove semantic translation quality; keyboard, visual and technical comparison supplement them.

## Guarantee boundaries

- The static desk shows published lessons. Personalized selection, durable session cursor, completion and review history require the repo agent. A browser bookmark is a reading step only.
- The portable SQLite lab proves its transaction invariant for the exercised sequential, in-memory cases. It does not test SQL Server locks, a broker, process crashes, concurrent workers or uncertain commits.
- SQL Server adaptation is retained in optional depth; its runtime execution remains unverified. Dated official documentation checks are separately recorded in the lesson.
- Tests use synthetic evidence in isolated temporary profiles. No learner score, completion or review is inferred from a successful test run.

[Daily workflow](workflow.md) · [Sample lesson](../lessons/2026-10-08-messaging-idempotent-consumer.md)
