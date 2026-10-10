#!/usr/bin/env python3
"""Exercise English/Vietnamese daily learning in real Chromium, including fallbacks."""
import argparse
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import re
import threading
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright, expect

KEY = 'interview-practice:reading-place:v1'
LANGUAGE_KEY = 'interview-practice:language:v1'
STEPS = ['goal', 'predict', 'model', 'practice', 'verify', 'recall']
SAMPLE_LESSON_ID = '2026-10-08-messaging-idempotent-consumer'


@contextmanager
def serve(site, baseurl):
    class Handler(SimpleHTTPRequestHandler):
        def do_GET(self):
            path = urlsplit(self.path).path
            if path != baseurl and not path.startswith(baseurl + '/'):
                self.send_error(404)
                return
            self.path = self.path[len(baseurl):] or '/'
            super().do_GET()

        def log_message(self, *_):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(Handler, directory=str(site)))
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f'http://127.0.0.1:{server.server_port}{baseurl}/'
    finally:
        server.shutdown()
        thread.join()
        server.server_close()


def accessibility(page, axe_path):
    page.add_script_tag(path=str(axe_path))
    result = page.evaluate("""async () => await axe.run(document, {
        runOnly: {type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa', 'best-practice']}
    })""")
    failures = [{"id": v['id'], "impact": v['impact'], "nodes": [n['target'] for n in v['nodes']]} for v in result['violations']]
    assert not failures, f'Accessibility violations at {page.url}: {json.dumps(failures)}'


def no_overflow(page):
    assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1'), f'Horizontal page overflow at {page.url}'


def config(page):
    return json.loads(page.locator('#study-config').text_content())


def bookmark(page):
    return page.evaluate(f"JSON.parse(localStorage.getItem('{KEY}'))")


def screenshot(page, directory, name):
    if directory:
        directory.mkdir(parents=True, exist_ok=True)
        page.screenshot(path=str(directory / (name + '.png')), full_page=True)


def check_library(page, lessons, language):
    entries = page.locator('[data-logical-lesson]')
    ids = entries.evaluate_all('(nodes) => nodes.map(node => node.dataset.logicalLesson)')
    expected = {item['id']: item['routes'].get(language, item['routes']['en']) for item in lessons}
    assert len(ids) == len(expected) and set(ids) == set(expected), 'Library must list each logical lesson once'
    for entry in entries.all():
        expect(entry.locator('[data-public-lesson]')).to_have_attribute('href', expected[entry.get_attribute('data-logical-lesson')])


def check(args):
    with serve(args.site.resolve(), args.baseurl) as desk, sync_playwright() as p:
        launch = {'headless': True}
        if os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE'):
            launch['executable_path'] = os.environ['PLAYWRIGHT_CHROMIUM_EXECUTABLE']
        browser = p.chromium.launch(**launch)
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        context.grant_permissions(['clipboard-read', 'clipboard-write'])
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(desk)
        assert page.locator('.action-card').count() == 4
        expect(page.locator('[data-resume-status]')).to_contain_text('No browser reading place')
        manifest = config(page)
        ids = [item['id'] for item in manifest['lessons']]
        assert ids and len(ids) == len(set(ids)), 'Translation must not become another logical lesson'
        check_library(page, manifest['lessons'], 'en')
        # The published library can grow daily. Only lab-specific assertions use
        # the immutable sample; the desk's newest lesson may be a different topic.
        latest = manifest['lessons'][-1]
        expect(page.locator('[data-public-lesson]').first).to_have_attribute('href', latest['routes']['en'] + '#goal')
        logical = next(item for item in manifest['lessons'] if item['id'] == SAMPLE_LESSON_ID)
        origin = desk[:desk.index(args.baseurl)] if args.baseurl else desk.rstrip('/')
        lesson_url = logical['routes']['en']
        lesson = origin + lesson_url
        vi_lesson = origin + logical['routes']['vi']
        vi_desk = origin + manifest['routes']['vi']
        page.keyboard.press('Tab')
        expect(page.get_by_role('link', name='Skip to content')).to_be_focused()
        page.keyboard.press('Enter')
        assert page.evaluate('document.activeElement.id') == 'main-content'
        page.locator('[data-copy-prompt]').click()
        expect(page.locator('[data-copy-status]')).to_contain_text('Copied.')
        assert page.evaluate('navigator.clipboard.readText()') == 'Write today’s lesson in English.'
        screenshot(page, args.screenshots, 'desk-en-desktop')
        page.goto(lesson + '#goal')
        assert page.locator('h1').count() == 1
        assert page.locator('details[open]').count() == 0
        for step in STEPS:
            page.locator(f'[data-step="{step}"]').click()
            expect(page.locator(f'[data-step="{step}"]')).to_have_attribute('aria-current', 'step')
            assert bookmark(page)['step'] == step
        summary = page.locator('details[data-answer] summary').first
        summary.focus()
        page.keyboard.press('Enter')
        expect(page.locator('details[data-answer]').first).to_have_attribute('open', '')
        page.locator('[data-close-answers]').click()
        assert page.locator('details[data-answer][open]').count() == 0
        expect(page.locator('#recall-status')).to_contain_text('Answers closed')
        page.locator('[data-step="practice"]').click()
        with page.expect_download() as info:
            page.get_by_role('link', name='Download the runnable lab (.zip)').click()
        assert info.value.suggested_filename == 'atomic-inbox.zip'
        english_code = page.locator('.lesson-content pre code').all_text_contents()
        screenshot(page, args.screenshots, 'lesson-en-desktop')
        # Same logical lesson, fragment and existing bookmark schema across languages.
        page.locator('[data-locale-link="vi"]').focus()
        page.keyboard.press('Enter')
        expect(page).to_have_url(vi_lesson + '#practice')
        expect(page.locator('html')).to_have_attribute('lang', 'vi')
        saved = bookmark(page)
        assert saved['lessonId'] == logical['id'] and saved['step'] == 'practice'
        assert set(saved) == {'lessonId', 'path', 'step', 'updatedAt'}
        assert page.evaluate(f"localStorage.getItem('{LANGUAGE_KEY}')") == 'vi'
        assert page.locator('.lesson-content pre code').all_text_contents() == english_code
        assert page.locator('div[lang="en"] blockquote').count() == 2
        assert page.locator('details[open]').count() == 0
        page.reload()
        expect(page.locator('[data-step="practice"]')).to_have_attribute('aria-current', 'step')
        page.go_back()
        expect(page).to_have_url(lesson + '#practice')
        page.go_forward()
        expect(page).to_have_url(vi_lesson + '#practice')
        screenshot(page, args.screenshots, 'lesson-vi-desktop')
        page.locator('details[data-answer]').first.locator('summary').click()
        page.locator('[data-close-answers]').click()
        expect(page.locator('#recall-status')).to_contain_text('Đã đóng lời giải')
        # Remembered locale is offered; an explicit English URL is never redirected.
        page.goto(desk)
        expect(page).to_have_url(desk)
        expect(page.locator('html')).to_have_attribute('lang', 'en')
        expect(page.locator('[data-preference-link]')).to_have_attribute('href', manifest['routes']['vi'])
        expect(page.locator('[data-resume]')).to_have_attribute('href', logical['routes']['vi'] + '#practice')
        page.locator('[data-resume]').click()
        expect(page).to_have_url(vi_lesson + '#practice')
        page.goto(lesson + '#goal')
        page.locator('[data-step="verify"]').click()
        expect(page.locator('[data-preference-link]')).to_have_attribute('href', logical['routes']['vi'] + '#verify')
        page.locator('[data-preference-link]').click()
        expect(page).to_have_url(vi_lesson + '#verify')
        page.goto(vi_desk)
        assert page.locator('.action-card').count() == 4
        expect(page.locator('[data-public-lesson]').first).to_have_attribute('href', latest['routes'].get('vi', latest['routes']['en']) + '#goal')
        check_library(page, manifest['lessons'], 'vi')
        page.locator('[data-copy-prompt]').click()
        assert page.evaluate('navigator.clipboard.readText()') == 'Viết bài học hôm nay bằng tiếng Việt.'
        screenshot(page, args.screenshots, 'desk-vi-desktop')
        for language, home in (('en', desk), ('vi', vi_desk)):
            page.goto(home + 'lessons/')
            check_library(page, manifest['lessons'], language)
        # All paired entry points/guides: native switches and layout at three widths.
        pairs = ('', 'lessons/', 'practice/review/', 'practice/interview/',
                 'docs/workflow/', 'agent/INTERVIEW_METHOD/', 'curriculum/', 'README/')
        for width in (1440, 390, 320):
            page.set_viewport_size({'width': width, 'height': 1000 if width == 1440 else 844})
            for language, home, content in (('en', desk, lesson), ('vi', vi_desk, vi_lesson)):
                for path in [home + pair for pair in pairs] + [content]:
                    response = page.goto(path)
                    assert response.status == 200, path
                    expect(page.locator('html')).to_have_attribute('lang', language)
                    assert config(page)['locale'] == language
                    assert config(page)['routes'][language] == urlsplit(path).path
                    no_overflow(page)
                    accessibility(page, args.axe)
                page.goto(content)
                page.locator('details[data-answer]').first.locator('summary').click()
                no_overflow(page)
                accessibility(page, args.axe)
                if width == 390:
                    screenshot(page, args.screenshots, f'lesson-{language}-mobile')
                    page.goto(home)
                    screenshot(page, args.screenshots, f'desk-{language}-mobile')
        # A real untranslated domain keeps its own content and discloses English fallback.
        missing = desk + 'curriculum/domains/sql-data/'
        page.goto(missing)
        expect(page.locator('#translation-notice')).to_be_visible()
        link = page.locator('[data-locale-missing]')
        expect(link).to_have_attribute('href', urlsplit(missing).path + '#translation-notice')
        link.click()
        expect(page).to_have_url(missing + '#translation-notice')
        expect(page.locator('html')).to_have_attribute('lang', 'en')
        # Browser resume fallback when the requested variant is unavailable.
        # Alter only the served test response, leaving repository content/state untouched.
        def absent_variant(route):
            response = route.fetch()
            body = response.text()
            match = re.search(r'(<script type="application/json" id="study-config">)(.*?)(</script>)', body, re.S)
            changed = json.loads(match.group(2))
            saved_lesson = next(item for item in changed['lessons'] if item['id'] == SAMPLE_LESSON_ID)
            del saved_lesson['routes']['vi']
            body = body[:match.start(2)] + json.dumps(changed) + body[match.end(2):]
            route.fulfill(response=response, body=body)
        page.goto(desk)
        page.evaluate('(item) => localStorage.setItem("' + KEY + '", JSON.stringify(item))',
                      {'lessonId': logical['id'], 'path': lesson_url, 'step': 'verify'})
        page.route(desk, absent_variant)
        page.reload()
        expect(page.locator('[data-resume]')).to_have_attribute('href', lesson_url + '#verify')
        expect(page.locator('[data-resume-status]')).to_contain_text('opens its English version')
        page.unroute(desk, absent_variant)
        # Invalid preferences/bookmarks cannot route to unrelated pages or external sites.
        for bad in ('{broken', json.dumps({'lessonId': logical['id'], 'path': 'https://example.com' + lesson_url, 'step': 'practice'}),
                    json.dumps({'lessonId': logical['id'], 'path': '/unpublished', 'step': 'practice'}),
                    json.dumps({'lessonId': 'other-id', 'path': lesson_url, 'step': 'practice'})):
            page.evaluate('value => localStorage.setItem("' + KEY + '", value)', bad)
            page.reload()
            expect(page.locator('[data-resume]')).to_have_attribute('href', latest['routes']['en'] + '#goal')
        for invalid in ('fr', '{broken'):
            page.evaluate('value => localStorage.setItem("' + LANGUAGE_KEY + '", value)', invalid)
            page.reload()
            expect(page.locator('[data-preference-link]')).not_to_be_visible()
        page.goto(lesson + '#verify')
        page.locator('[data-locale-link="vi"]').click()
        page.locator('[data-clear-place]').click()
        assert page.evaluate(f"localStorage.getItem('{KEY}')") is None
        assert page.evaluate(f"localStorage.getItem('{LANGUAGE_KEY}')") == 'vi'
        assert not errors, errors
        context.close()
        # Blocked browser storage/clipboard: truthful local-language notices, working links.
        fallback = browser.new_context()
        fallback.add_init_script("""Object.defineProperty(window, 'localStorage', {get() {throw new Error('blocked')}});
            Object.defineProperty(navigator, 'clipboard', {value: {writeText: async () => {throw new Error('blocked')}}});""")
        fp = fallback.new_page()
        for language, home, content in (('en', desk, lesson), ('vi', vi_desk, vi_lesson)):
            fp.goto(content + '#practice')
            expect(fp.locator('#bookmark-status')).to_contain_text(config(fp)['messages']['bookmark_blocked'])
            expect(fp.locator('#locale-status')).to_contain_text(config(fp)['messages']['locale_blocked'])
            fp.goto(home)
            fp.locator('[data-copy-prompt]').click()
            expect(fp.locator('[data-copy-status]')).to_contain_text(config(fp)['messages']['copy_blocked'])
            target_language = 'vi' if language == 'en' else 'en'
            fp.locator(f'[data-locale-link="{target_language}"]').click()
            expect(fp.locator('html')).to_have_attribute('lang', target_language)
        fallback.close()
        # No JavaScript: visible prompts, disabled browser helpers, native language links/answers.
        plain = browser.new_context(java_script_enabled=False)
        pp = plain.new_page()
        for language, home, content in (('en', desk, lesson), ('vi', vi_desk, vi_lesson)):
            pp.goto(home)
            expect(pp.locator('[data-prompt]')).to_be_visible()
            expect(pp.locator('[data-copy-prompt]')).to_be_disabled()
            expect(pp.locator('noscript')).to_be_visible()
            pp.goto(content)
            pp.locator('details[data-answer]').first.locator('summary').click()
            expect(pp.locator('details[data-answer]').first).to_have_attribute('open', '')
            expect(pp.locator('#practice')).to_be_visible()
            expect(pp.locator('[data-clear-place]')).to_be_disabled()
            pp.locator(f'[data-locale-link="{"vi" if language == "en" else "en"}"]').click()
            expect(pp.locator('html')).to_have_attribute('lang', 'vi' if language == 'en' else 'en')
        plain.close()
        browser.close()
    print('Bilingual Chromium flow passed: shared identity/code, six steps, switching/reload/history, preferences/resume, missing translations, keyboard/downloads, blocked storage/clipboard, no-JS, 1440/390/320px and axe WCAG checks.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('_site'))
    parser.add_argument('--baseurl', default='/software-engineering-interview')
    parser.add_argument('--axe', type=Path, required=True)
    parser.add_argument('--screenshots', type=Path)
    check(parser.parse_args())
