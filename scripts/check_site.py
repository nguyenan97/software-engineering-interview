#!/usr/bin/env python3
"""Check generated site links and ensure excluded learning state is absent."""
import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
        self.lang = None
        self.canonical = None
        self.alternates = {}
        self.description = None
        self.title = ''
        self.config_text = ''
        self.in_config = False
        self.in_title = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'meta' and attrs.get('name') == 'description':
            self.description = attrs.get('content')
        if tag == 'title':
            self.in_title = True
        if tag == 'script' and attrs.get('id') == 'study-config':
            self.in_config = True
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonical = attrs.get('href')
        if tag == 'link' and attrs.get('rel') == 'alternate' and attrs.get('hreflang'):
            self.alternates[attrs['hreflang']] = attrs.get('href')
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_config:
            self.config_text += data

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        if tag == 'script':
            self.in_config = False


def check_locales(site, pages, baseurl, errors):
    """Check rendered routing, reciprocal SEO and logical IDs, not Markdown claims."""
    def target(url):
        path = unquote(urlsplit(url).path)
        if baseurl and not (path == baseurl or path.startswith(baseurl + '/')):
            raise ValueError('Locale route is outside the configured site: ' + url)
        path = path[len(baseurl):] if baseurl else path
        resolved = (site / path.lstrip('/')).resolve()
        if resolved.is_dir():
            resolved /= 'index.html'
        if resolved not in pages:
            raise ValueError('Locale route is not a rendered page: ' + url)
        return resolved

    for path, page in pages.items():
        if not page.config_text:
            continue
        try:
            config = json.loads(page.config_text)
            if page.lang != config['locale'] or page.lang not in config['supportedLocales']:
                raise ValueError('Document language differs from runtime locale')
            if not page.title.strip() or not page.description:
                raise ValueError('Localized page title/description is missing')
            if not page.canonical or target(page.canonical) != path:
                raise ValueError('Page must have its own canonical URL')
            for language, route in config['routes'].items():
                peer = pages[target(route)]
                if peer.lang != language:
                    raise ValueError('Counterpart route has the wrong document language')
                if page.alternates:
                    if page.alternates.get(language) != peer.canonical:
                        raise ValueError('hreflang does not reference the actual counterpart canonical URL')
                    if peer.alternates.get(page.lang) != page.canonical:
                        raise ValueError('hreflang is not reciprocal')
            if page.alternates and page.alternates.get('x-default') != pages[target(config['routes']['en'])].canonical:
                raise ValueError('x-default must reference the matching English page')
            identities = [item['id'] for item in config['lessons']]
            if len(identities) != len(set(identities)):
                raise ValueError('Locale variants were counted as duplicate logical lessons')
            for item in config['lessons']:
                if 'en' not in item['routes']:
                    raise ValueError('Logical lesson has no English canonical route')
                for language, route in item['routes'].items():
                    if pages[target(route)].lang != language:
                        raise ValueError('Lesson locale mapping has the wrong language')
        except (ValueError, KeyError, TypeError) as exc:
            errors.append(f'{path.relative_to(site)}: {exc}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("site", type=Path)
    parser.add_argument("--baseurl", default="/software-engineering-interview")
    args = parser.parse_args()
    site = args.site.resolve()
    if not (site / "index.html").is_file():
        raise SystemExit("Built site index.html is missing")
    pages = {}
    for path in site.rglob("*.html"):
        page = Page()
        page.feed(path.read_text(encoding="utf-8"))
        pages[path] = page
    errors = []
    check_locales(site, pages, args.baseurl, errors)
    for path, page in pages.items():
        for link in page.links:
            parts = urlsplit(link)
            if parts.scheme or parts.netloc:
                continue
            address = unquote(parts.path)
            if address.startswith("/"):
                if args.baseurl and not (address == args.baseurl or address.startswith(args.baseurl + "/")):
                    errors.append(f"Unexpected site-root URL {link} in {path.relative_to(site)}")
                    continue
                address = address[len(args.baseurl):] if args.baseurl else address
                target = site / address.lstrip("/")
            elif address:
                target = path.parent / address
            else:
                target = path
            target = target.resolve()
            if target.is_dir():
                target /= "index.html"
            if not target.is_file():
                errors.append(f"Missing {link} in {path.relative_to(site)}")
            elif parts.fragment and target in pages and unquote(parts.fragment) not in pages[target].ids:
                errors.append(f"Missing anchor {link} in {path.relative_to(site)}")
    for excluded in ("learning", "scripts", "tests", "agent/LEARNING_STATE_TEMPLATE.json", "AGENTS.md", "requirements.txt", "requirements-browser.txt", "work"):
        if (site / excluded).exists():
            errors.append(f"Excluded content published: {excluded}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated links, anchors, locale manifests and reciprocal metadata in {len(pages)} rendered pages; learning state and tooling excluded.")


if __name__ == "__main__":
    main()
