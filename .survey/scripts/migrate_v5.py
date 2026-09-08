"""One-time, repeatable metadata/state migration; never claims a new audit."""
import datetime as dt
import json
import re
import survey as s


def main():
    old = s.read(s.STATE + 'paper-identity-index.json')
    moved = set(old.get('ignored_moved_stubs', []))
    other = {v: k for k, v in old.get('other', {}).items()}
    for p in sorted((s.ROOT / 'papers/inference').glob('*/*.md')):
        rel = p.relative_to(s.ROOT / 'papers/inference').as_posix()
        if p.name == 'README.md' or rel in moved:
            continue
        meta, body = s.front(p)
        original = p.read_text()
        add = {}
        arxiv = re.search(r'(?<!\d)\d{4}\.\d{4,5}(?!\d)', p.name)
        if not arxiv:
            label = re.search(r'^- \*?\*?arXiv\*?\*?:\*?\*?\s*(\d{4}\.\d{4,5})', body, re.M)
            if label:
                arxiv = re.search(r'\d{4}\.\d{4,5}', label[1])
        cid = meta.get('canonical_id') or other.get(rel) or ('arXiv:' + arxiv[0] if arxiv else None)
        if not cid:
            raise ValueError('Unresolved identity: ' + rel)
        add['canonical_id'] = cid
        if arxiv:
            add['arxiv_id'] = arxiv[0]
        heading = re.search(r'^# (.+)$', body, re.M)
        summary = re.search(r'^> (.+)$', body, re.M) or re.search(r'^## 一文要約\s*\n+([^\n]+)', body, re.M)
        add.update(title=heading[1] if heading else None, summary=summary[1] if summary else None,
                   source='https://arxiv.org/abs/' + arxiv[0] if arxiv else None,
                   last_audited=None, audit_version=0, storage_targets=[], bottlenecks=[],
                   hardware_details=None, quality_effect=None, evidence_locations=[])
        fields = {k: v for k, v in add.items() if k not in meta}
        if not (meta.get('summary') or fields.get('summary')):
            raise ValueError('Summary needs explicit migration: ' + rel)
        lines = ''.join(k + ': ' + json.dumps(v, ensure_ascii=False) + '\n' for k, v in fields.items())
        if original.startswith('---\n'):
            p.write_text('---\n' + lines + original[4:])
        else:
            p.write_text('---\n' + lines + '---\n\n' + original)
    for p in (s.ROOT / s.STATE).rglob('*.json'):
        if p.name == 'exploration-state.json':
            continue
        obj = json.loads(p.read_text())
        if 'workflow_version' in obj:
            obj['workflow_version'] = 5
            s.write(p.relative_to(s.ROOT).as_posix(), obj)
    layout = s.read(s.STATE + 'state-layout.json')
    layout['paths'].update(retry_papers=s.STATE + 'retry-papers.json', leases=s.STATE + 'leases.json', runs_dir=s.STATE + 'runs/', status_page=s.STATE + 'STATUS.md')
    layout['migration']['to_workflow_version'] = 5
    s.write(s.STATE + 'state-layout.json', layout)
    rejected = s.read(s.STATE + 'rejected-papers.json')
    retry = s.read(s.STATE + 'retry-papers.json', {'schema_version': 1, 'items': []})
    for x in rejected['papers'][:]:
        if x.get('reason_code') != 'insufficient_primary_source':
            continue
        if not any(i['canonical_id'] == x['canonical_id'] for i in retry['items']):
            at = x['checked_at']
            retry['items'].append({'canonical_id': x['canonical_id'], 'title': x['title'], 'status': 'waiting',
                'first_attempt_at': at, 'last_attempt_at': at,
                'retry_after': (s.timestamp(at) + dt.timedelta(days=7)).isoformat(),
                'attempts': [{'at': at, 'sources': x.get('attempted_sources', []), 'error': x.get('retrieval_error')}],
                'migration_note': 'Earlier failures without individually recorded dates are not invented or counted.',
                'previous_rejection': x})
        rejected['papers'].remove(x)
    s.write(s.STATE + 'retry-papers.json', retry)
    s.write(s.STATE + 'rejected-papers.json', rejected)
    if not (s.ROOT / s.STATE / 'leases.json').exists():
        s.write(s.STATE + 'leases.json', {'schema_version': 1, 'items': {}})
    # Replace only the old generated paper list; preserve authored technical sections.
    for p in (s.ROOT / 'papers/inference').glob('*/README.md'):
        text = p.read_text()
        if '<!-- survey:auto:start -->' not in text:
            text = re.sub(r'^## 収録論文\n.*?(?=^## |\Z)', '', text, flags=re.S | re.M)
            p.write_text(text.rstrip() + '\n')
    s.render()
    s.validate()


if __name__ == '__main__':
    main()
