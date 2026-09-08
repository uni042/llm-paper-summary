#!/usr/bin/env python3
"""Deterministic survey helpers. Local changes require verified GitHub publication."""
import argparse
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
STATE = 'survey-state/'

def read(path, default=None):
    p = ROOT / path
    return json.loads(p.read_text()) if p.exists() else default

def write(path, data):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(data, ensure_ascii=False, indent=2, default=str) + '\n'
    tmp = p.with_suffix(p.suffix + '.tmp')
    tmp.write_text(text)
    tmp.replace(p)

def timestamp(value):
    t = dt.datetime.fromisoformat(value.replace('Z', '+00:00'))
    if t.tzinfo is None:
        raise ValueError('Timezone is required')
    return t

def now():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def front(path):
    text = path.read_text()
    if not text.startswith('---\n'):
        return {}, text
    parts = text.split('---', 2)
    return yaml.safe_load(parts[1]) or {}, parts[2]

def norm_id(value):
    value = str(value).strip()
    if value.lower().startswith('arxiv:'):
        basic = re.sub(r'v\d+$', '', value.split(':', 1)[1])
        if not re.fullmatch(r'(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})', basic, re.I):
            raise ValueError('Invalid arXiv ID: ' + value)
        return 'arXiv:' + basic
    if value.lower().startswith(('doi:', 'https://doi.org/', 'http://doi.org/')):
        return 'DOI:' + re.sub(r'^(?:doi:|https?://doi.org/)', '', value, flags=re.I).lower()
    return value

def papers():
    old = read(STATE + 'paper-identity-index.json', {})
    moved = set(old.get('ignored_moved_stubs', []))
    records = []
    for p in sorted((ROOT / 'papers/inference').glob('*/*.md')):
        rel = p.relative_to(ROOT).as_posix()
        if p.name == 'README.md' or rel.removeprefix('papers/inference/') in moved:
            continue
        meta, body = front(p)
        cid = meta.get('canonical_id')
        if not cid:
            raise ValueError('Missing canonical_id: ' + rel)
        ids = [norm_id(cid)]
        for key, prefix in [('arxiv_id', 'arXiv:'), ('doi', 'DOI:'), ('openreview_id', 'OpenReview:')]:
            if meta.get(key):
                ids.append(norm_id(prefix + str(meta[key])))
        records.append({'canonical_id': norm_id(cid), 'path': rel,
                        'identifiers': sorted(set(ids)), 'title': meta.get('title', ''),
                        'summary': meta.get('summary', ''), 'lineage': p.parent.name,
                        'source_hash': hashlib.sha256(p.read_bytes()).hexdigest(),
                        'meta': meta})
    return records

def identity(records):
    result = {}
    aliases = {}
    for r in records:
        for key in r['identifiers']:
            if key in aliases and aliases[key] != r['canonical_id']:
                raise ValueError('Duplicate identifier: ' + key)
            aliases[key] = r['canonical_id']
        if r['canonical_id'] in result:
            raise ValueError('Duplicate paper: ' + r['canonical_id'])
        result[r['canonical_id']] = {k: v for k, v in r.items() if k in ('path', 'identifiers', 'source_hash')}
    old = read(STATE + 'paper-identity-index.json', {})
    return {'schema_version': 3, 'active_count': len(result), 'papers': result,
            'identifier_to_canonical': aliases,
            'ignored_moved_stubs': old.get('ignored_moved_stubs', [])}

def cell(value):
    if isinstance(value, (dict, list)):
        value = json.dumps(value, ensure_ascii=False, default=str)
    return str(value if value not in (None, '', []) else '未記録').replace('|', '\\|').replace('\n', ' ')

def put_text(path, text):
    p = ROOT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text)

def block(path, text):
    p = ROOT / path
    content = p.read_text()
    start, end = '<!-- survey:auto:start -->', '<!-- survey:auto:end -->'
    replacement = start + '\n' + text + '\n' + end
    if start in content:
        content = re.sub(re.escape(start) + r'.*?' + re.escape(end), lambda _: replacement, content, flags=re.S)
    else:
        content = content.rstrip() + '\n\n' + replacement + '\n'
    p.write_text(content)

def render():
    records = papers()
    write(STATE + 'paper-identity-index.json', identity(records))
    grouped = {}
    for r in records:
        grouped.setdefault(r['lineage'], []).append(r)
    for lineage, rows in grouped.items():
        rows.sort(key=lambda r: (str(r['meta'].get('published', '')), r['canonical_id']), reverse=True)
        lines = [f'## 自動生成の論文一覧（{len(rows)}本）', '', '| 論文 | 一文要約 |', '|---|---|']
        lines += [f"| [{cell(r['title'])}]({Path(r['path']).name}) | {cell(r['summary'])} |" for r in rows]
        block(f'papers/inference/{lineage}/README.md', '\n'.join(lines))
    overview = ['## 自動生成の収録状況', '', f'推論論文：**{len(records)}本**（移動案内を除く）。', '', '| 系統 | 本数 |', '|---|---:|']
    overview += [f'| [{k}]({k}/README.md) | {len(v)} |' for k, v in sorted(grouped.items())]
    block('papers/inference/README.md', '\n'.join(overview))
    # Keep existing authored descriptions, but update all their numerical summaries.
    for path in ['papers/inference/README.md', 'papers/README.md', 'README.md']:
        p = ROOT / path
        content = p.read_text()
        for lineage, rows in grouped.items():
            content = re.sub(r'(\]\((?:inference/)?' + re.escape(lineage) + r'/\) — )\d+本', lambda m: m[1] + str(len(rows)) + '本', content)
        if path == 'papers/inference/README.md':
            content = re.sub(r'収録論文: \*\*\d+本\*\*', f'収録論文: **{len(records)}本**', content)
        elif path == 'papers/README.md':
            training = len(list((ROOT / 'papers/training').glob('*/*.md'))) - len(list((ROOT / 'papers/training').glob('*/README.md')))
            content = re.sub(r'収録論文: \*\*\d+本\*\*', f'収録論文: **{len(records) + training}本**', content)
            content = re.sub(r'## Inference / 推論 — \d+本', f'## Inference / 推論 — {len(records)}本', content)
        else:
            training = len(list((ROOT / 'papers/training').glob('*/*.md'))) - len(list((ROOT / 'papers/training').glob('*/README.md')))
            content = re.sub(r'(\[Inference / 推論\]\(papers/inference/\) — \*\*)\d+本', lambda m: m[1] + str(len(records)) + '本', content)
            content = re.sub(r'現在の論文収録数: .*', f'現在の論文収録数: **{len(records)+training}本**（推論{len(records)}本 + 学習{training}本）', content)
        p.write_text(content)
    for path, prefix in [('papers/README.md', 'inference/'), ('README.md', 'papers/inference/')]:
        block(path, f'推論論文：**{len(records)}本**。 [全一覧]({prefix}README.md) ／ [研究比較]({prefix}comparison.md)')
    cols = [('summary', '一文要約'), ('topics', '主題'), ('storage_targets', '保存・転送対象'), ('bottlenecks', '改善対象'), ('hardware_evaluation', '評価方式'), ('hardware_details', '評価機器'), ('quality_effect', '品質への影響'), ('code', '実装'), ('evidence_locations', '主要結果の出典')]
    lines = ['# 推論研究の横断比較', '', '既存の明示属性だけを表示する。未記録は未確認であり、非対応・実装なしを意味しない。本文の数値から自動推測しない。', '', '| 論文 | ' + ' | '.join(v for _, v in cols) + ' |', '|---|' + '---|' * len(cols)]
    lines += ['| [' + cell(r['title']) + '](' + r['path'].removeprefix('papers/inference/') + ') | ' + ' | '.join(cell(r['meta'].get(k)) for k, _ in cols) + ' |' for r in records]
    put_text('papers/inference/comparison.md', '\n'.join(lines) + '\n')
    dashboard()

def dashboard():
    runtime = read(STATE + 'runtime.json', {})
    plan = read(runtime.get('current_plan_path', STATE + 'none'), {})
    lines = ['# サーベイの進捗', '', '保存された状態から生成。実行開始記録がない場合、未起動と記録保存失敗は区別できない。', '', f"対象期間：{plan.get('period_start', '未記録')} 〜 {plan.get('period_end', '未記録')}", '', '| 作業 | 完了 | 目標 | 未完了 |', '|---|---:|---:|---:|']
    for key, label, target in [('selected_papers', '精読', 'target'), ('selected_audits', '監査', 'audit_target')]:
        items = plan.get(key, [])
        done = sum(x.get('status') == 'completed' and x.get('reason_code') != 'insufficient_primary_source' for x in items)
        pending = sum(x.get('status') != 'completed' for x in items)
        lines.append(f'| {label} | {done} | {plan.get(target, 0)} | {pending} |')
    runs = [read(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT / STATE / 'runs').glob('*.json'))]
    runs.sort(key=lambda r: r.get('last_progress_at', r['started_at']), reverse=True)
    lines += ['', '## 直近の実行', '']
    for r in runs[:10]:
        lines.append(f"- {r['run_id']}：{r['status']}／{r.get('stage', '未記録')}／最終進捗 {r.get('last_progress_at')}／次：{r.get('next_action', '未記録')}")
    if not runs:
        lines.append('実行記録なし。過去の実行を推測して補完しない。')
    lines += ['', '## 次の選定済み対象', '']
    for key, label in [('selected_papers', '精読'), ('selected_audits', '監査')]:
        for item in plan.get(key, []):
            if item.get('status') != 'completed':
                lines.append(f"- {label}：{item.get('title', item['canonical_id'])}／{item.get('next_action', '一次資料を確認')}")
    lines += ['', '## 再確認・保守', '']
    for x in read(STATE + 'retry-papers.json', {'items': []})['items']:
        lines.append(f"- {x['canonical_id']}：{x['status']}／次回 {x.get('retry_after', 'なし')}")
    for filename in ['maintenance-queue.json', 'blockers.json']:
        data = read(STATE + filename, {})
        for x in data.get('items', data.get('blockers', [])):
            if x.get('status') == 'open':
                lines.append(f"- {cell(x.get('id'))}：{cell(x.get('next_action', x.get('problem')))}")
    put_text(STATE + 'STATUS.md', '\n'.join(lines) + '\n')

def validate():
    expected = identity(papers())
    actual = read(STATE + 'paper-identity-index.json', {})
    errors = []
    if expected != actual:
        errors.append('Identity index differs from paper metadata; run build')
    for r in papers():
        for key in ['canonical_id', 'title', 'summary', 'source', 'last_audited', 'audit_version']:
            if key not in r['meta']:
                errors.append(f"Missing {key}: {r['path']}")
        if r['meta'].get('audit_version') and not r['meta'].get('last_audited'):
            errors.append('Audit version without date: ' + r['path'])
    runtime = read(STATE + 'runtime.json', {})
    plan = read(runtime.get('current_plan_path', STATE + 'none'), {})
    if plan.get('plan_id') != runtime.get('current_plan_id'):
        errors.append('Runtime/plan ID mismatch')
    for side, key, target in [('research', 'selected_papers', 'target'), ('audit', 'selected_audits', 'audit_target')]:
        items = plan.get(key, [])
        ids = [x['canonical_id'] for x in items]
        if len(ids) != len(set(ids)) or len(items) > plan.get(target, 0):
            errors.append('Duplicate or over-target plan: ' + side)
        queue = read(STATE + f'queues/{side}.json', {'items': []})['items']
        assigned = [x['canonical_id'] for x in queue if x.get('plan_id') == plan.get('plan_id')]
        pending = [x['canonical_id'] for x in items if x.get('status') != 'completed']
        if sorted(assigned) != sorted(pending):
            errors.append('Queue/plan mismatch: ' + side)
        for item in items:
            if item.get('status') != 'completed':
                continue
            if item.get('reason_code') == 'insufficient_primary_source':
                retry_ids = [x['canonical_id'] for x in read(STATE + 'retry-papers.json', {'items': []})['items']]
                if item['canonical_id'] not in retry_ids:
                    errors.append('Unavailable source missing retry record')
            elif item.get('result') != 'not_selected' and item['canonical_id'] not in expected['papers']:
                errors.append('Completed paper missing artifact: ' + item['canonical_id'])
    history = read(STATE + 'daily-history.json', {})
    entries = history.get('entries', [])
    if isinstance(entries, list):
        ids = [x.get('plan_id') for x in entries]
        if len(ids) != len(set(ids)):
            errors.append('Daily history contains duplicate plan IDs')
    for item in read(STATE + 'retry-papers.json', {'items': []})['items']:
        if item['status'] == 'waiting' and timestamp(item['retry_after']) < timestamp(item['last_attempt_at']) + dt.timedelta(days=7):
            errors.append('Retry interval is shorter than seven days')
    rejected_ids = {x['canonical_id'] for x in read(STATE + 'rejected-papers.json', {'papers': []})['papers']}
    for item in read(STATE + 'rejected-papers.json', {'papers': []})['papers']:
        if item.get('reason_code') not in ('duplicate', 'out_of_scope', 'not_research', 'withdrawn_or_retracted'):
            errors.append('Unsupported permanent rejection: ' + item['canonical_id'])
        if not all(item.get(k) for k in ('evidence_url', 'checked_at', 'reopen_condition')):
            errors.append('Permanent rejection lacks evidence/reopening condition: ' + item['canonical_id'])
        if item.get('reason_code') == 'duplicate' and item.get('duplicate_of') not in expected['papers']:
            errors.append('Duplicate rejection lacks an active merge destination')
    retry_ids = {x['canonical_id'] for x in read(STATE + 'retry-papers.json', {'items': []})['items'] if x['status'] in ('waiting', 'dormant')}
    if rejected_ids & retry_ids:
        errors.append('Paper simultaneously permanently rejected and waiting for retrieval')
    for path in ['README.md', 'papers/README.md', 'papers/inference/README.md', 'papers/inference/comparison.md', STATE + 'STATUS.md']:
        p = ROOT / path
        for target in re.findall(r'\]\(([^)]+)\)', p.read_text()):
            if '://' not in target and not target.startswith('#') and not (p.parent / target.split('#')[0]).exists():
                errors.append('Broken local link: ' + path + ' -> ' + target)
    if errors:
        raise ValueError('\n'.join(errors))
    print(f"OK: {len(expected['papers'])} papers; index, metadata, plan, queue, retry state")

def lease(data, resource, run_id, at, action):
    current = data.setdefault('items', {}).get(resource)
    t = timestamp(at)
    active = current and timestamp(current['expires_at']) > t
    if action == 'acquire' and active and current['run_id'] != run_id:
        raise ValueError('Resource is claimed by another run')
    if action in ('renew', 'release') and (not active or current['run_id'] != run_id):
        raise ValueError('Lease expired or belongs to another run')
    if action == 'release':
        del data['items'][resource]
    else:
        data['items'][resource] = {'run_id': run_id, 'updated_at': at, 'expires_at': (t + dt.timedelta(minutes=45)).isoformat()}
    return data

def retry_failure(data, cid, at, sources, error):
    items = data.setdefault('items', [])
    item = next((x for x in items if x['canonical_id'] == cid), None)
    if item and item['status'] == 'dormant':
        raise ValueError('Dormant: require a new source/version or explicit request before reopening')
    if item and timestamp(at) < timestamp(item['retry_after']):
        raise ValueError('Retry is not due')
    if not item:
        item = {'canonical_id': cid, 'first_attempt_at': at, 'attempts': []}
        items.append(item)
    item['attempts'].append({'at': at, 'sources': sources, 'error': error})
    item['last_attempt_at'] = at
    dormant = len(item['attempts']) >= 5 and timestamp(at) >= timestamp(item['first_attempt_at']) + dt.timedelta(days=28)
    item['status'] = 'dormant' if dormant else 'waiting'
    item['retry_after'] = None if dormant else (timestamp(at) + dt.timedelta(days=7)).isoformat()
    return data

def route(plan, scheduled_at, boundary):
    slot, start = timestamp(scheduled_at), timestamp(boundary)
    if not start <= slot < start + dt.timedelta(days=1):
        raise ValueError('Boundary must contain the scheduled slot')
    if plan.get('period_start') and timestamp(plan['period_start']) > start:
        return 'stale_slot'
    if not plan.get('period_start') or timestamp(plan['period_start']) != start or plan.get('status') not in ('ready', 'in_progress', 'completed'):
        return 'recover_planning'
    return 'reading'

def select_mode(scheduled_at, nightly_hour, morning_hour, morning_minute, planning_hour, planning_minute):
    slot = timestamp(scheduled_at)
    # Nightly owns the entire configured hour; it cannot fall through into reading/planning.
    if slot.hour == nightly_hour:
        return 'nightly'
    if (slot.hour, slot.minute) == (morning_hour, morning_minute):
        return 'morning'
    if (slot.hour, slot.minute) == (planning_hour, planning_minute):
        return 'planning'
    return 'reading'

def closing_result(plan, history):
    """Pure result; caller publishes history + next plan + queues atomically."""
    existing = next((x for x in history.get('entries', []) if x['plan_id'] == plan['plan_id']), None)
    if existing:
        return existing
    result = {'plan_id': plan['plan_id']}
    for key, target_key, name in [('selected_papers', 'target', 'research'), ('selected_audits', 'audit_target', 'audit')]:
        target, items = plan[target_key], plan[key]
        if target < 1:
            raise ValueError('Target must be positive')
        pending = [x['canonical_id'] for x in items if x.get('status') != 'completed']
        unavailable = [x for x in items if x.get('reason_code') == 'insufficient_primary_source']
        if pending:
            next_target, reason = max(1, target - 1), 'unfinished'
        elif len(items) == target and not unavailable:
            next_target, reason = target + 1, 'all_read' if name == 'research' else 'all_audited'
        else:
            next_target, reason = target, 'source_unavailable_or_candidate_shortfall'
        result[name] = {'target': target, 'next_target': next_target, 'reason': reason, 'carry_ids': pending}
    return result

def cleanup(at):
    cutoff = timestamp(at) - dt.timedelta(hours=24)
    removed = []
    for p in (ROOT / STATE / 'runs').glob('*.json'):
        r = json.loads(p.read_text())
        # A running record is retained even if its last progress is very old.
        if r.get('status') in ('completed', 'partial', 'failed') and r.get('finished_at') and timestamp(r['finished_at']) < cutoff:
            p.unlink()
            removed.append(p.relative_to(ROOT).as_posix())
    print(json.dumps(removed, ensure_ascii=False))
    return removed

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--root', type=Path)
    s = p.add_subparsers(dest='cmd', required=True)
    for cmd in ['build', 'validate', 'dashboard']:
        s.add_parser(cmd)
    a = s.add_parser('cleanup')
    a.add_argument('--at')
    s.add_parser('closing-result')
    a = s.add_parser('lease')
    a.add_argument('action', choices=['acquire', 'renew', 'release'])
    a.add_argument('--resource', required=True)
    a.add_argument('--run-id', required=True)
    a.add_argument('--at', default=None)
    a = s.add_parser('run')
    a.add_argument('action', choices=['start', 'progress', 'finish'])
    for flag in ['run-id', 'stage', 'next-action']:
        a.add_argument('--' + flag, required=True)
    a.add_argument('--at')
    a.add_argument('--scheduled-at')
    a.add_argument('--mode')
    a.add_argument('--status', choices=['completed', 'partial', 'failed'])
    a.add_argument('--verified-commit')
    a = s.add_parser('retry-failure')
    a.add_argument('--id', required=True)
    a.add_argument('--at')
    a.add_argument('--source', action='append', required=True)
    a.add_argument('--error', required=True)
    a = s.add_parser('due')
    a.add_argument('--at')
    a = s.add_parser('route')
    a.add_argument('--scheduled-at', required=True)
    a.add_argument('--period-start', required=True)
    a = s.add_parser('select-mode')
    a.add_argument('--scheduled-at', required=True)
    for field in ['nightly-hour', 'morning-hour', 'planning-hour']:
        a.add_argument('--' + field, type=int, choices=range(24), required=True)
    for field in ['morning-minute', 'planning-minute']:
        a.add_argument('--' + field, type=int, choices=range(60), required=True)
    args = p.parse_args()
    global ROOT
    if args.root:
        ROOT = args.root.resolve()
    if args.cmd == 'build':
        render()
    elif args.cmd == 'validate':
        validate()
    elif args.cmd == 'dashboard':
        dashboard()
    elif args.cmd == 'cleanup':
        cleanup(args.at or now())
        dashboard()
    elif args.cmd == 'closing-result':
        runtime = read(STATE + 'runtime.json', {})
        print(json.dumps(closing_result(read(runtime['current_plan_path']), read(STATE + 'daily-history.json', {'entries': []})), ensure_ascii=False, indent=2))
    elif args.cmd == 'lease':
        write(STATE + 'leases.json', lease(read(STATE + 'leases.json', {'schema_version': 1, 'items': {}}), args.resource, args.run_id, args.at or now(), args.action))
        print('LOCAL ONLY: publish without force; verify remote ownership before working')
    elif args.cmd == 'retry-failure':
        write(STATE + 'retry-papers.json', retry_failure(read(STATE + 'retry-papers.json', {'schema_version': 1, 'items': []}), norm_id(args.id), args.at or now(), args.source, args.error))
    elif args.cmd == 'due':
        at = timestamp(args.at or now())
        print(json.dumps([x for x in read(STATE + 'retry-papers.json', {'items': []})['items'] if x['status'] == 'waiting' and timestamp(x['retry_after']) <= at], ensure_ascii=False))
    elif args.cmd == 'route':
        runtime = read(STATE + 'runtime.json', {})
        print(route(read(runtime.get('current_plan_path', STATE + 'none'), {}), args.scheduled_at, args.period_start))
    elif args.cmd == 'select-mode':
        print(select_mode(args.scheduled_at, args.nightly_hour, args.morning_hour, args.morning_minute, args.planning_hour, args.planning_minute))
    elif args.cmd == 'run':
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,100}', args.run_id):
            raise ValueError('Unsafe run ID')
        path = STATE + f'runs/{args.run_id}.json'
        r = read(path)
        at = args.at or now()
        timestamp(at)
        if args.action == 'start':
            if r or not args.scheduled_at or not args.mode:
                raise ValueError('Start requires a new ID, scheduled-at and mode')
            timestamp(args.scheduled_at)
            r = {'run_id': args.run_id, 'started_at': at, 'scheduled_at': args.scheduled_at, 'mode': args.mode, 'status': 'running', 'workflow_version': 6}
        elif not r or r['status'] != 'running':
            raise ValueError('No active run')
        r.update(last_progress_at=at, stage=args.stage, next_action=args.next_action)
        if args.verified_commit:
            r['verified_commit'] = args.verified_commit
        if args.action == 'finish':
            if not args.status:
                raise ValueError('Finish requires status')
            r.update(status=args.status, finished_at=at)
        write(path, r)
        dashboard()

if __name__ == '__main__':
    main()
