#!/usr/bin/env python3
"""Read-only repository-wide structural checks, with explicit coverage reporting."""
import argparse
import hashlib
import json
import re
import shutil
import tempfile
from pathlib import Path
from urllib.parse import unquote, urlsplit
import survey


def blob_hash(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def local_files(root):
    return {p.relative_to(root).as_posix(): p for p in root.rglob('*') if p.is_file()
            and not any(x in ('.git', '__pycache__', '.venv') for x in p.relative_to(root).parts)
            and not p.name.endswith(('.pyc', '.tmp'))}


def check(root, inventory):
    root = root.resolve()
    files = local_files(root)
    findings = []
    external = set()
    def issue(code, path, detail):
        findings.append({'code': code, 'path': path, 'detail': detail})
    if not inventory.get('source_commit') or not inventory.get('files'):
        issue('inventory_missing', '', 'A complete remote tree or tracked-file inventory with a source commit is required')
    expected = {x['path']: x['sha'] for x in inventory.get('files', [])}
    for path in expected:
        if path not in files:
            issue('missing_file', path, 'Present in repository inventory but unavailable locally')
    json_objects = {}
    scanned = []
    for name, path in sorted(files.items()):
        scanned.append(name)
        if path.suffix not in ('.md', '.json', '.yaml', '.yml'):
            continue
        try:
            text = path.read_text(encoding='utf-8')
        except UnicodeError:
            issue('invalid_encoding', name, 'Expected UTF-8 text')
            continue
        if path.suffix == '.json':
            try:
                json_objects[name] = json.loads(text)
            except ValueError as error:
                issue('invalid_json', name, str(error))
        if path.suffix in ('.yaml', '.yml') or (path.suffix == '.md' and text.startswith('---\n')):
            try:
                survey.yaml.safe_load(text if path.suffix != '.md' else text.split('---', 2)[1])
            except (ValueError, survey.yaml.YAMLError) as error:
                issue('invalid_yaml', name, str(error))
        if path.suffix != '.md':
            continue
        # Code examples are not live links. Inline and reference-style destinations are covered.
        prose = re.sub(r'^```.*?^```\s*$', '', text, flags=re.M | re.S)
        links = re.findall(r'!?\[[^\]\n]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', prose)
        links += re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', prose, re.M)
        for link in links:
            target = link.strip('<>')
            try:
                parsed = urlsplit(target)
            except ValueError:
                issue('invalid_link', name, target)
                continue
            if parsed.scheme or parsed.netloc:
                if parsed.scheme in ('http', 'https'):
                    external.add(target)
                continue
            if not parsed.path:
                continue  # Fragment anchors are not validated by this structural checker.
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root):
                issue('link_outside_repository', name, target)
            elif not destination.exists():
                issue('broken_local_link', name, target)
    def state_object(name):
        value = json_objects.get(name, {})
        if not isinstance(value, dict):
            issue('invalid_state_type', name, 'Expected a JSON object')
            return {}
        return value
    frozen = state_object('survey-state/frozen-training.json')
    if not frozen or not frozen.get('files'):
        issue('frozen_baseline_missing', 'survey-state/frozen-training.json', 'Cannot verify training freeze without a baseline')
    else:
        actual_training = {n for n in files if n.startswith('papers/training/')}
        for name, sha in frozen['files'].items():
            if name not in files or blob_hash(files[name]) != sha:
                issue('frozen_training_changed', name, 'Read-only baseline differs; do not rewrite automatically')
        for name in actual_training - set(frozen['files']):
            issue('frozen_training_added', name, 'Unreviewed addition in frozen training area')
    layout = state_object('survey-state/state-layout.json')
    for key, value in layout.get('paths', {}).items():
        if not (root / value).exists():
            issue('state_path_missing', 'survey-state/state-layout.json', f'{key}: {value}')
    history = state_object('survey-state/daily-history.json')
    entries = history.get('entries', [])
    if len({x.get('plan_id') for x in entries}) != len(entries):
        issue('duplicate_daily_close', 'survey-state/daily-history.json', 'Same plan closed more than once')
    for name, obj in json_objects.items():
        if name.startswith('survey-state/daily-plans/'):
            try:
                if survey.timestamp(obj['period_start']) >= survey.timestamp(obj['period_end']):
                    issue('invalid_plan_period', name, 'Period end must follow start')
                for side, target in [('selected_papers', 'target'), ('selected_audits', 'audit_target')]:
                    items = obj[side]
                    ids = [x['canonical_id'] for x in items]
                    if len(ids) != len(set(ids)) or len(items) > obj[target]:
                        issue('invalid_plan_items', name, side)
                    for item in items:
                        for artifact in item.get('artifact_paths', []):
                            if not (root / artifact).exists():
                                issue('missing_plan_artifact', name, artifact)
            except (KeyError, TypeError, ValueError) as error:
                issue('invalid_plan', name, str(error))
    previous = survey.ROOT
    try:
        survey.ROOT = root
        try:
            survey.validate()
        except (ValueError, KeyError, TypeError, AttributeError, OSError, survey.yaml.YAMLError) as error:
            issue('survey_invariant', 'survey-state/', str(error))
        # Regenerate in an isolated copy; inspection must not rewrite the repository.
        with tempfile.TemporaryDirectory() as tmp:
            copy = Path(tmp) / 'repository'
            shutil.copytree(root, copy, ignore=shutil.ignore_patterns('.git', '__pycache__', '.venv'))
            survey.ROOT = copy
            try:
                survey.render()
                for name, path in local_files(copy).items():
                    if name not in files or path.read_bytes() != files[name].read_bytes():
                        issue('stale_generated_file', name, 'Regeneration changes this file')
            except (ValueError, KeyError, TypeError, AttributeError, OSError, survey.yaml.YAMLError) as error:
                issue('generation_failed', 'scripts/survey.py', str(error))
    finally:
        survey.ROOT = previous
    return {'schema_version': 1, 'source_commit': inventory.get('source_commit'),
            'checked_at': survey.now(), 'status': 'passed' if not findings else 'issues_found',
            'scope': 'repository-wide structural consistency',
            'inventory_file_count': len(expected), 'checked_file_count': len(scanned),
            'missing_files': sorted(set(expected) - set(files)),
            'working_changes': sorted(n for n, p in files.items() if n not in expected or blob_hash(p) != expected[n]),
            'checks': ['inventory_coverage', 'all_json_yaml', 'markdown_file_links', 'frozen_training',
                       'state_paths', 'all_daily_plans', 'current_survey_invariants', 'derived_file_regeneration'],
            'not_checked': ['External URL reachability', 'Fragment anchors', 'Scientific validity / full paper audits',
                            'Scheduler startup guarantees', 'Runtime execution of arbitrary repository code'],
            'external_url_count': len(external), 'findings': findings}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=survey.ROOT)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    result = check(args.root, json.loads(args.inventory.read_text()))
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'checked_files': result['checked_file_count'], 'findings': len(result['findings'])}))
    raise SystemExit(0 if result['status'] == 'passed' else 1)


if __name__ == '__main__':
    main()
