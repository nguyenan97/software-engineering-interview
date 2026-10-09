#!/usr/bin/env python3
"""Check the built static daily-learning flow in real Chromium (test dependencies only)."""
import argparse
from contextlib import contextmanager
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import threading
from urllib.parse import urlsplit

from playwright.sync_api import sync_playwright, expect

KEY = 'interview-practice:reading-place:v1'
STEPS = ['goal', 'predict', 'model', 'practice', 'verify', 'recall']


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


def check(args):
    # Start the server for the complete browser session, including downloads.
    with serve(args.site.resolve(), args.baseurl) as desk, sync_playwright() as p:
        launch = {'headless': True}
        if os.environ.get('PLAYWRIGHT_CHROMIUM_EXECUTABLE'):
            launch['executable_path'] = os.environ['PLAYWRIGHT_CHROMIUM_EXECUTABLE']
        browser = p.chromium.launch(**launch)
        context = browser.new_context(viewport={'width': 1440, 'height': 1000}, reduced_motion='reduce')
        page = context.new_page()
        errors = []
        page.on('pageerror', lambda error: errors.append(str(error)))
        page.goto(desk)
        assert page.locator('.action-card').count() == 4
        expect(page.locator('[data-resume-status]')).to_contain_text('No browser reading place')
        lesson_url = page.locator('[data-public-lesson]').first.get_attribute('href').split('#')[0]
        lesson = desk.rstrip('/')[:-len(args.baseurl)] + lesson_url
        # Native keyboard access: skip link leads into the main landmark.
        page.keyboard.press('Tab')
        expect(page.get_by_role('link', name='Skip to content')).to_be_focused()
        page.keyboard.press('Enter')
        assert page.evaluate("document.activeElement.id") == 'main-content'
        accessibility(page, args.axe)
        if args.screenshots:
            args.screenshots.mkdir(parents=True, exist_ok=True)
            page.screenshot(path=str(args.screenshots / 'desk-desktop.png'), full_page=True)
        context.grant_permissions(['clipboard-read', 'clipboard-write'])
        page.locator('[data-copy-prompt]').click()
        expect(page.locator('[data-copy-status]')).to_contain_text('Copied.')
        assert page.evaluate('navigator.clipboard.readText()') == 'Viết bài học hôm nay.'
        page.goto(lesson + '#goal')
        assert page.locator('h1').count() == 1
        assert page.locator('details[open]').count() == 0
        for step in STEPS:
            page.locator(f'[data-step="{step}"]').click()
            expect(page.locator(f'[data-step="{step}"]')).to_have_attribute('aria-current', 'step')
            assert page.evaluate(f"JSON.parse(localStorage.getItem('{KEY}')).step") == step
        summary = page.locator('details[data-answer] summary').first
        summary.focus()
        page.keyboard.press('Enter')
        expect(page.locator('details[data-answer]').first).to_have_attribute('open', '')
        page.locator('[data-close-answers]').click()
        assert page.locator('details[data-answer][open]').count() == 0
        expect(page.locator('#recall-status')).to_contain_text('Answers closed')
        page.locator('[data-step="practice"]').click()
        accessibility(page, args.axe)
        with page.expect_download() as info:
            page.get_by_role('link', name='Download the runnable lab (.zip)').click()
        assert info.value.suggested_filename == 'atomic-inbox.zip'
        if args.screenshots:
            page.screenshot(path=str(args.screenshots / 'lesson-desktop.png'), full_page=True)
        page.goto(desk)
        expect(page.locator('[data-resume]')).to_have_attribute('href', lesson_url + '#practice')
        expect(page.locator('[data-resume-status]')).to_contain_text('not completion')
        page.locator('[data-resume]').click()
        assert page.url.endswith('#practice')
        page.locator('[data-clear-place]').click()
        assert page.evaluate(f"localStorage.getItem('{KEY}')") is None
        # Mobile flow and code/details: page stays within viewport; code may scroll internally.
        for width in (390, 320):
            page.set_viewport_size({'width': width, 'height': 844})
            for path in (desk, lesson, desk + 'practice/review/', desk + 'practice/interview/'):
                page.goto(path)
                no_overflow(page)
                accessibility(page, args.axe)
            page.goto(lesson)
            page.locator('details[data-answer]').first.locator('summary').click()
            no_overflow(page)
            accessibility(page, args.axe)
            if args.screenshots and width == 390:
                page.screenshot(path=str(args.screenshots / 'lesson-mobile.png'), full_page=True)
                page.goto(desk)
                page.screenshot(path=str(args.screenshots / 'desk-mobile.png'), full_page=True)
        # Bad/untrusted bookmarks cannot turn Continue into an external redirect.
        for bad in ('{broken', json.dumps({'lessonId': 'x', 'path': 'https://example.com/', 'step': 'practice'}), json.dumps({'lessonId': 'x', 'path': '/unpublished', 'step': 'practice'})):
            page.goto(desk)
            page.evaluate('value => localStorage.setItem("' + KEY + '", value)', bad)
            page.reload()
            expect(page.locator('[data-resume]')).to_have_attribute('href', lesson_url + '#goal')
        assert not errors, errors
        context.close()
        # Blocked storage and clipboard have visible truthful fallback messages.
        fallback = browser.new_context()
        fallback.add_init_script("""Object.defineProperty(window, 'localStorage', {get() {throw new Error('blocked')}});
            Object.defineProperty(navigator, 'clipboard', {value: {writeText: async () => {throw new Error('blocked')}}});""")
        fp = fallback.new_page()
        fp.goto(lesson + '#practice')
        expect(fp.locator('#bookmark-status')).to_contain_text('storage is unavailable')
        fp.goto(desk)
        fp.locator('[data-copy-prompt]').click()
        expect(fp.locator('[data-copy-status]')).to_contain_text('Select the prompt')
        fallback.close()
        # Static content/answers remain usable without JavaScript.
        plain = browser.new_context(java_script_enabled=False)
        pp = plain.new_page()
        pp.goto(desk)
        expect(pp.locator('[data-prompt]')).to_be_visible()
        pp.goto(lesson)
        pp.locator('details[data-answer]').first.locator('summary').click()
        expect(pp.locator('details[data-answer]').first).to_have_attribute('open', '')
        expect(pp.locator('#practice')).to_be_visible()
        plain.close()
        browser.close()
    print('Chromium flow passed: six steps, keyboard disclosures, downloads, resume, clipboard/storage fallbacks, no-JS reading, 1440/390/320px layouts and axe WCAG checks.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', type=Path, default=Path('_site'))
    parser.add_argument('--baseurl', default='/software-engineering-interview')
    parser.add_argument('--axe', type=Path, required=True)
    parser.add_argument('--screenshots', type=Path)
    check(parser.parse_args())
