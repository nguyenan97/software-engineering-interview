#!/usr/bin/env python3
"""Generate/check shared lesson code from actual lab sources, with no translation copies."""
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = {
    'atomic-inbox-solution': ('solution.py', 'python'),
    'sql-server-setup': ('sql-server-setup.sql', 'sql'),
    'sql-server-procedure': ('sql-server-procedure.sql', 'sql'),
}


def render(check=False):
    for name, (source, language) in SOURCES.items():
        target = ROOT / '_includes/lab-code' / (name + '.md')
        expected = '```' + language + '\n' + (ROOT / 'labs/atomic-inbox' / source).read_text().rstrip() + '\n```\n'
        if check:
            if not target.is_file() or target.read_text() != expected:
                raise ValueError('Stale shared code: run python scripts/render_lesson_code.py')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(expected)
    print('Shared lesson code matches lab sources.' if check else 'Generated shared lesson code.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    try:
        render(parser.parse_args().check)
    except ValueError as exc:
        raise SystemExit(str(exc)) from exc
