#!/usr/bin/env python3
"""Repository-wide structural consistency checks for the current v10 layout."""
import argparse
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlsplit
import yaml


def blob_hash(path):
    data = path.read_bytes()
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def local_files(root):
    return {
        p.relative_to(root).as_posix(): p
        for p in root.rglob('*')
        if p.is_file()
        and not any(x in ('.git', '__pycache__', '.venv') for x in p.relative_to(root).parts)
        and not p.name.endswith(('.pyc', '.tmp'))
    }


def frontmatter(path):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return {}, text
    parts = text.split('---', 2)
    return yaml.safe_load(parts[1]) or {}, parts[2]


def check(root, inventory):
    root = root.resolve()
    files = local_files(root)
    findings = []
    external = set()

    def issue(code, path, detail):
        findings.append({'code': code, 'path': path, 'detail': detail})

    expected = {x['path']: x['sha'] for x in inventory.get('files', [])}
    if not inventory.get('source_commit') or not expected:
        issue('inventory_missing', '', 'A complete tracked-file inventory is required')
    for path in expected:
        if path not in files:
            issue('missing_file', path, 'Present in inventory but unavailable locally')

    json_objects = {}
    canonical_ids = {}
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
                yaml.safe_load(text if path.suffix != '.md' else text.split('---', 2)[1])
            except (ValueError, yaml.YAMLError) as error:
                issue('invalid_yaml', name, str(error))

        if path.suffix != '.md':
            continue

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
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root):
                issue('link_outside_repository', name, target)
            elif not destination.exists():
                issue('broken_local_link', name, target)

        if name.startswith('papers/inference/') and path.name != 'README.md':
            meta, body = frontmatter(path)
            # A moved stub is navigation, not an active paper artifact.
            if body.lstrip().startswith('# Moved') or text.lstrip().startswith('# Moved'):
                continue
            cid = meta.get('canonical_id')
            if not cid:
                issue('paper_missing_canonical_id', name, 'Active inference paper requires canonical_id')
            elif cid in canonical_ids:
                issue('duplicate_canonical_id', name, f'Also used by {canonical_ids[cid]}')
            else:
                canonical_ids[cid] = name
            for key in ('title', 'summary', 'source', 'last_audited', 'audit_version'):
                if key not in meta:
                    issue('paper_missing_metadata', name, key)

    frozen_name = '.survey/survey-state/frozen-training.json'
    frozen = json_objects.get(frozen_name, {})
    if not isinstance(frozen, dict) or not frozen.get('files'):
        issue('frozen_baseline_missing', frozen_name, 'Cannot verify training freeze without a baseline')
    else:
        actual_training = {n for n in files if n.startswith('papers/training/')}
        baseline = frozen['files']
        for name, sha in baseline.items():
            if name not in files:
                issue('frozen_training_missing', name, 'Baseline file is missing')
            elif blob_hash(files[name]) != sha:
                issue('frozen_training_changed', name, 'Read-only baseline differs; do not rewrite automatically')
        for name in actual_training - set(baseline):
            issue('frozen_training_added', name, 'Unreviewed addition in frozen training area')

    layout_name = '.survey/survey-state/state-layout.json'
    layout = json_objects.get(layout_name, {})
    if isinstance(layout, dict):
        for key, value in layout.get('paths', {}).items():
            if not (root / value).exists():
                issue('state_path_missing', layout_name, f'{key}: {value}')

    maintenance_name = '.survey/work-queue/maintenance-cycle.json'
    maintenance = json_objects.get(maintenance_name, {})
    if isinstance(maintenance, dict):
        cadence = maintenance.get('cadence_runs')
        count = maintenance.get('runs_since_maintenance')
        if cadence != 24:
            issue('maintenance_cadence', maintenance_name, f'Expected cadence_runs=24, got {cadence!r}')
        if not isinstance(count, int) or count < 0 or count >= 24:
            issue('maintenance_counter', maintenance_name, f'Invalid runs_since_maintenance={count!r}')

    return {
        'schema_version': 2,
        'source_commit': inventory.get('source_commit'),
        'checked_at': __import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),
        'status': 'passed' if not findings else 'issues_found',
        'scope': 'repository-wide structural consistency',
        'inventory_file_count': len(expected),
        'checked_file_count': len(scanned),
        'missing_files': sorted(set(expected) - set(files)),
        'working_changes': sorted(n for n, p in files.items() if n not in expected or blob_hash(p) != expected[n]),
        'checks': [
            'inventory_coverage', 'all_json_yaml', 'markdown_file_links', 'frozen_training',
            'state_paths', 'paper_metadata_and_identity', 'maintenance_cycle'
        ],
        'not_checked': [
            'External URL reachability', 'Fragment anchors', 'Scientific validity / full paper audits',
            'Scheduler startup guarantees', 'Runtime execution of arbitrary repository code'
        ],
        'external_url_count': len(external),
        'findings': findings,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('.'))
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
