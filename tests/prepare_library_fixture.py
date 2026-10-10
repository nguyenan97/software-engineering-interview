#!/usr/bin/env python3
"""Copy the site and add a synthetic later lesson, without recording learner history."""
import argparse
from pathlib import Path
import shutil


def prepare(source, destination):
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(
        '.git', '_site', 'work', '.venv', '__pycache__'))
    identity = '2099-01-01-library-regression-fixture'
    shared = f'''lesson_id: {identity}
topic_id: library-regression-fixture
translation_key: {identity}
'''
    body = '\n'.join(f'## {step}\n{{: #{step} }}\n\nSynthetic test content.\n'
                     for step in ('goal', 'predict', 'model', 'practice', 'verify', 'recall'))
    for language, directory in (('en', 'lessons'), ('vi', 'vi/lessons')):
        header = f'---\nlayout: lesson\nlocale: {language}\n' + shared
        if language == 'en':
            header += '''created_at: '2099-01-01'
level: foundation
duration_minutes: 40
practice_minutes: 28
status: generated
'''
        else:
            header += f'canonical_lesson: lessons/{identity}.md\n'
        title = 'Later lesson regression fixture' if language == 'en' else 'Bài giả lập để kiểm tra danh sách'
        header += f'title: {title}\nprimary_objective: Synthetic fixture, not learner history.\n'
        header += 'prerequisites_note: Test-only artifact.\n---\n'
        (destination / directory / (identity + '.md')).write_text(header + body, encoding='utf-8')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path('.'))
    parser.add_argument('--destination', type=Path, required=True)
    args = parser.parse_args()
    prepare(args.source.resolve(), args.destination.resolve())
