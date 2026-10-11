#!/usr/bin/env python3
"""Verify the bilingual question bank's public routes, provenance and native UI."""
import argparse
from collections import Counter
import json
import os
from pathlib import Path
import re

from playwright.sync_api import expect, sync_playwright

from browser_check import no_overflow, screenshot, serve


ROOT = Path(__file__).resolve().parents[1]
SOURCE_ID = re.compile(r'^S\d+-(?:Q\d+|SC\d+)$')
HEADING_ID = re.compile(r'^(S\d+-(?:Q\d+|SC\d+))\b')
SAMPLE_GROUP = 'messaging-idempotent-consumer'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def route(baseurl, language, tail):
    prefix = 'vi/' if language == 'vi' else ''
    return baseurl.rstrip('/') + '/' + prefix + tail


def accessible(page, axe_path):
    page.add_script_tag(path=str(axe_path))
    result = page.evaluate("""async () => await axe.run(document, {
        runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice']}
    })""")
    failures = [
        {'id': item['id'], 'impact': item['impact'],
         'nodes': [node['target'] for node in item['nodes']]}
        for item in result['violations']
        if item['impact'] in ('serious', 'critical')
    ]
    assert not failures, f'Serious/critical accessibility violations at {page.url}: {json.dumps(failures)}'


def open_page(page, url, language):
    response = page.goto(url)
    assert response is not None and response.status == 200, f'Unreachable page: {url}'
    expect(page.locator('html')).to_have_attribute('lang', language)
    assert page.locator('main h1').count() == 1, f'Expected one content title: {url}'


def group_ids(page):
    return [value for value in page.locator('main [id]').evaluate_all(
        '(nodes) => nodes.map(node => node.id)') if SOURCE_ID.fullmatch(value)]


def question_heading_ids(page):
    headings = page.locator('main h3').all_text_contents()
    return [match[1] for text in headings if (match := HEADING_ID.match(text.strip()))]


def check(args):
    inventory = read(ROOT / '_data/question_bank/inventory.json')
    labels = read(ROOT / '_data/question_bank/labels.json')
    canonical = {item['question_id']: item for item in inventory['canonical_questions']}
    units = {item['source_id']: item for item in inventory['source_units']}
    groups = sorted({item['group_id'] for item in canonical.values()})
    sample_questions = sorted(qid for qid, item in canonical.items() if item['group_id'] == SAMPLE_GROUP)
    assert sample_questions, 'The sample group must have a source-backed question'
    sample_id = sample_questions[0]
    sample_alias = next((sid for sid in canonical[sample_id]['source_ids'] if sid != sample_id), sample_id)

    with serve(args.site.resolve(), args.baseurl) as home, sync_playwright() as playwright:
        origin = home[:home.index(args.baseurl)] if args.baseurl else home.rstrip('/')
        launch = {'headless': True}
        executable = str(args.browser) if args.browser else os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE')
        if executable:
            launch['executable_path'] = executable
        browser = playwright.chromium.launch(**launch)
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))

        # Every route and anchor is derived from the authoritative inventory.
        # Source aliases are navigation targets, never additional questions.
        for language in ('en', 'vi'):
            index_path = route(args.baseurl, language, 'questions/')
            open_page(page, origin + index_path, language)
            group_links = page.locator('main h3 a').evaluate_all('(nodes) => nodes.map(node => node.getAttribute("href"))')
            expected_links = [route(args.baseurl, language, f'questions/groups/{gid}/') for gid in groups]
            assert Counter(group_links) == Counter(expected_links), f'Missing or repeated group entry: {language}'
            assert page.locator('main h2').count() >= len(labels['domains']), 'Domain browsing must remain visible'
            no_overflow(page)
            accessible(page, args.axe)

            all_anchors, all_headings = [], []
            for gid in groups:
                expected_questions = sorted(qid for qid, item in canonical.items() if item['group_id'] == gid)
                expected_ids = sorted(sid for qid in expected_questions for sid in canonical[qid]['source_ids'])
                group_path = route(args.baseurl, language, f'questions/groups/{gid}/')
                for width in (1440, 390, 320):
                    page.set_viewport_size({'width': width, 'height': 1000 if width == 1440 else 844})
                    open_page(page, origin + group_path, language)
                    assert page.locator('details[open]').count() == 0, f'Guidance must start closed: {page.url}'
                    no_overflow(page)
                    if width == 1440:
                        anchors = group_ids(page)
                        headings = question_heading_ids(page)
                        assert Counter(anchors) == Counter(expected_ids), f'Wrong source-anchor coverage: {language}/{gid}'
                        assert Counter(headings) == Counter(expected_questions), f'Aliases became questions or questions missing: {language}/{gid}'
                        assert page.locator('details.question-original').count() == len(expected_questions)
                        assert page.locator('details.question-guidance').count() == len(expected_questions)
                        all_anchors.extend(anchors)
                        all_headings.extend(headings)
                        for sid in expected_ids:
                            source_path, _, anchor = units[sid]['source_ref'].partition('#')
                            source_href = route(args.baseurl, 'en', source_path.removesuffix('.md') + '/') + '#' + anchor
                            assert page.locator(f'main a[href="{source_href}"]').count() >= 1, f'Missing original-source link: {sid}'
                    if gid == SAMPLE_GROUP:
                        accessible(page, args.axe)
                        screenshot(page, args.screenshots, f'questions-{language}-{width}-closed')
                    # Expand all material to catch long translations and source
                    # wording, not only the first short disclosure. Native user
                    # interaction is checked separately with JavaScript disabled.
                    page.locator('details').evaluate_all('(nodes) => nodes.forEach(node => {node.open = true})')
                    no_overflow(page)
                    if gid == SAMPLE_GROUP:
                        accessible(page, args.axe)
                        screenshot(page, args.screenshots, f'questions-{language}-{width}-expanded')
            assert Counter(all_anchors) == Counter({sid: 1 for sid in units}), f'Each source ID must occur exactly once per locale: {language}'
            assert Counter(all_headings) == Counter({qid: 1 for qid in canonical}), f'Each canonical question needs one heading: {language}'

            # Coverage-table links retain the source alias hash on the canonical
            # home. Both members of a merge must navigate to the same group.
            open_page(page, origin + route(args.baseurl, language, 'questions/coverage/'), language)
            mapping_rows = page.locator('main details tbody tr').evaluate_all("""(rows) => rows.map(row => {
                const links = row.querySelectorAll('a');
                return {source: links[0]?.textContent.trim(), sourceHref: links[0]?.getAttribute('href'),
                    canonical: links[1]?.textContent.trim(), destination: links[1]?.getAttribute('href')};
            })""")
            assert Counter(row['source'] for row in mapping_rows) == Counter({sid: 1 for sid in units}), f'Coverage mapping must include every source unit: {language}'
            for row in mapping_rows:
                sid = row['source']
                unit = units[sid]
                qid = unit['canonical_id']
                expected = route(args.baseurl, language, f'questions/groups/{canonical[qid]["group_id"]}/') + '#' + sid
                assert row['canonical'] == qid and row['destination'] == expected, f'Incorrect alias destination: {sid}'
                source_path, _, anchor = unit['source_ref'].partition('#')
                expected_source = route(args.baseurl, 'en', source_path.removesuffix('.md') + '/') + '#' + anchor
                assert row['sourceHref'] == expected_source, f'Incorrect source provenance link: {sid}'

            for width in (1440, 390, 320):
                page.set_viewport_size({'width': width, 'height': 1000 if width == 1440 else 844})
                open_page(page, origin + index_path, language)
                no_overflow(page)
                accessible(page, args.axe)
                screenshot(page, args.screenshots, f'questions-index-{language}-{width}')

        # Check the original source routes and all referenced anchors as rendered,
        # including unnumbered scenarios. This catches source-link regressions
        # without following hundreds of duplicate links individually.
        source_paths = sorted({unit['source_ref'].partition('#')[0] for unit in units.values()})
        for source_path in source_paths:
            source_url = origin + route(args.baseurl, 'en', source_path.removesuffix('.md') + '/')
            open_page(page, source_url, 'en')
            anchors = page.locator('[id]').evaluate_all('(nodes) => nodes.map(node => node.id)')
            needed = [unit['source_ref'].partition('#')[2] for unit in units.values() if unit['source_ref'].partition('#')[0] == source_path]
            for anchor in needed:
                assert anchors.count(anchor) == 1, f'Original source anchor missing or repeated: {source_path}#{anchor}'

        # Uppercase stable source IDs survive both directions of the live locale
        # switch, including an alias of a merged canonical question.
        for fragment in dict.fromkeys((sample_id, sample_alias)):
            en_url = origin + route(args.baseurl, 'en', f'questions/groups/{SAMPLE_GROUP}/') + '#' + fragment
            vi_url = origin + route(args.baseurl, 'vi', f'questions/groups/{SAMPLE_GROUP}/') + '#' + fragment
            page.goto(en_url)
            page.locator('[data-locale-link="vi"]').click()
            expect(page).to_have_url(vi_url)
            assert page.locator(f'[id="{fragment}"]').count() == 1
            page.locator('[data-locale-link="en"]').click()
            expect(page).to_have_url(en_url)
        assert not errors, f'Question-bank JavaScript errors: {errors}'
        context.close()

        # Native details are usable without scripts. Questions stay visible;
        # source wording and editorial guidance can be opened independently.
        plain = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
        native = plain.new_page()
        for language in ('en', 'vi'):
            url = origin + route(args.baseurl, language, f'questions/groups/{SAMPLE_GROUP}/')
            open_page(native, url, language)
            assert native.locator('details[open]').count() == 0
            assert sample_id in question_heading_ids(native)
            heading = native.get_by_role('heading', level=3, name=re.compile(r'^' + re.escape(sample_id) + r'\b'))
            expect(heading).to_be_visible()
            expect(heading.locator('xpath=following-sibling::p[normalize-space()][1]')).to_be_visible()
            original = heading.locator('xpath=following-sibling::details[contains(@class, "question-original")][1]')
            guidance = heading.locator('xpath=following-sibling::details[contains(@class, "question-guidance")][1]')
            expect(original.locator('summary')).to_have_text(labels[language]['original'])
            expect(guidance.locator('summary')).to_have_text(labels[language]['guidance'])
            expect(original.locator('blockquote').first).not_to_be_visible()
            original.locator('summary').click()
            expect(original).to_have_attribute('open', '')
            expect(original.locator('blockquote').first).to_be_visible()
            assert guidance.get_attribute('open') is None
            guidance.locator('summary').click()
            expect(guidance).to_have_attribute('open', '')
            expect(guidance).to_contain_text(labels[language]['intent'])
            expect(guidance).to_contain_text(labels[language]['followups'])
            assert 1 <= guidance.locator('ul').last.locator('li').count() <= 2, 'Added follow-ups must be present under their label'
            no_overflow(native)
            screenshot(native, args.screenshots, f'questions-{language}-no-js')
            original.locator('summary').click()
            guidance.locator('summary').click()
            assert native.locator('details[open]').count() == 0
            alternate = 'vi' if language == 'en' else 'en'
            native.locator(f'[data-locale-link="{alternate}"]').click()
            expect(native.locator('html')).to_have_attribute('lang', alternate)
        plain.close()
        browser.close()

    print(f'Question-bank browser checks passed: {len(groups)} groups and {len(canonical)} canonical headings/'
          f'{len(units)} unique source anchors per locale; provenance and alias links, native no-JS disclosures, '
          'uppercase locale-switch hashes, 1440/390/320px closed/expanded layout, and serious/critical axe checks.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('_site'))
    parser.add_argument('--baseurl', default='/software-engineering-interview')
    parser.add_argument('--axe', type=Path, required=True)
    parser.add_argument('--screenshots', type=Path)
    parser.add_argument('--browser', type=Path, help='Chromium executable; otherwise uses PLAYWRIGHT_CHROMIUM_EXECUTABLE or Playwright default')
    check(parser.parse_args())
