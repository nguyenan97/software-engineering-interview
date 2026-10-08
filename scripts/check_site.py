#!/usr/bin/env python3
"""Check generated site links and ensure excluded learning state is absent."""
import argparse
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            self.ids.add(attrs["id"])
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])


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
    for excluded in ("learning", "scripts", "tests", "agent/LEARNING_STATE_TEMPLATE.json", "AGENTS.md", "requirements.txt", "work"):
        if (site / excluded).exists():
            errors.append(f"Excluded content published: {excluded}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"Validated links and anchors in {len(pages)} rendered pages; learning state and tooling excluded.")


if __name__ == "__main__":
    main()
