#!/usr/bin/env python3
"""Validate live specification links, traceability, templates and frozen evidence.

This is documentation validation. It never claims runtime conformance.
"""
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote
from render_requirements import outputs

ROOT = Path(__file__).resolve().parents[1]
errors = []
def check(condition, message):
    if not condition:
        errors.append(message)

def anchors(text):
    found = set()
    counts = {}
    for line in text.splitlines():
        if re.match(r'^#{1,6} ', line):
            value = re.sub(r'[^\w\- ]', '', re.sub(r'^#+ ', '', line).lower(), flags=re.UNICODE).replace(' ', '-')
            n = counts.get(value, 0)
            counts[value] = n + 1
            found.add(value + (f'-{n}' if n else ''))
    return found

owners = ['REQUIREMENTS.md','ARCHITECTURE.md','SECURITY.md','DESIGN.md']
for name in owners:
    text = (ROOT/name).read_text()
    check(not re.search(r'\b(TO BE DECIDED|UNKNOWN|ASSUMPTION|TBD|FIXME|TODO)\b', text), f'{name}: unresolved live marker')
    check('## Open Questions\n\nNone for' in text, f'{name}: no explicit closed question register')

live = [ROOT/name for name in owners+['AGENTS.md','README.md','REQUIREMENT_TEMPLATE.md']]
live += list((ROOT/'docs/requirements').glob('*.md'))
for p in live:
    text = p.read_text()
    for match in re.finditer(r'(?<!!)\[[^\]\n]*\]\(([^)]+)\)', text):
        dest = match[1].split(' "',1)[0].strip('<>')
        if re.match(r'^[a-z]+:', dest):
            continue
        path, _, fragment = dest.partition('#')
        target = (p.parent/unquote(path)).resolve() if path else p
        check(target.exists(), f'{p.relative_to(ROOT)}: missing link {dest}')
        if target.is_file() and fragment and target.suffix=='.md':
            check(unquote(fragment) in anchors(target.read_text()), f'{p.relative_to(ROOT)}: missing anchor {dest}')

records=json.loads((ROOT/'docs/requirement-catalog.json').read_text())
ids={r['id'] for r in records}
check(len(ids)==len(records), 'Duplicate atomic requirement ID')
req=(ROOT/'REQUIREMENTS.md').read_text()
for r in records:
    check(f"docs/requirements/{r['id']}.md" in req, f"Catalog link missing: {r['id']}")
    check(set(r['upstream'])<=ids, f"Unknown upstream ID: {r['id']}")
    check(r['section'] in anchors((ROOT/r['owner']).read_text()), f"Unknown owner section: {r['id']}")
    for sid in r['security']:
        check(sid in (ROOT/'SECURITY.md').read_text(), f"Unknown security ID: {sid}")

visiting=set(); done=set(); by_id={r['id']:r for r in records}
def visit(rid):
    if rid in visiting:
        errors.append('Requirement dependency cycle at '+rid);return
    if rid in done:return
    visiting.add(rid)
    for up in by_id[rid]['upstream']:
        if up in by_id:visit(up)
    visiting.remove(rid);done.add(rid)
for rid in by_id:visit(rid)

template=(ROOT/'REQUIREMENT_TEMPLATE.md').read_text()
headings=re.findall(r'^## (.+)$',template,re.M)
fields=re.findall(r'^- \*\*([^*]+)\*\*:',template,re.M)
for p, expected in outputs().items():
    check(p.exists(),f'Missing rendered record: {p.name}')
    if not p.exists():continue
    actual=p.read_text()
    check(actual==expected,f'Stale generated record: {p.name}; run scripts/render_requirements.py')
    check(re.findall(r'^## (.+)$',actual,re.M)==headings,f'Template heading mismatch: {p.name}')
    for field in fields:
        check(f'- **{field}**: ' in actual,f'Missing field {field}: {p.name}')
    check(len(re.findall(r'^\d+\. \*\*AC-\d+.*Given .+, when .+, then .+\.$',actual,re.M))==4,f'Incomplete Given/When/Then criteria: {p.name}')
    check(not re.search(r'\b(TO BE DECIDED|TBD)\b',actual),f'Unresolved record: {p.name}')

interview=json.loads((ROOT/'docs/clarification-interview.json').read_text())
check(interview['active_question'] is None,'Interview still has an active question')
check(len(interview['topics'])==51,'Audited topic count changed without review')
check(len(interview['completed_questions'])==7,'Explicit interview answer missing')
for t in interview['topics']:
    check(t['status']=='resolved' and t.get('resolution') and t.get('resolved_decision_refs'), 'Unresolved topic '+t['id'])
    for ref in t['resolved_decision_refs']:
        path,_,a=ref.partition('#');p=ROOT/path
        check(p.exists() and a in anchors(p.read_text()), 'Invalid decision reference '+ref)
manifest=json.loads((ROOT/'docs/security-sources/manifest.json').read_text())
for item in manifest:
    p=ROOT/item['snapshot']
    check(p.exists(),f'Missing source snapshot {p}')
    if p.exists():check(hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256'],'Frozen source changed: '+item['id'])
security=(ROOT/'SECURITY.md').read_text()
sids=set(re.findall(r'^\*\*(SEC-[A-Z]+-\d+)',security,re.M))
check(len(sids)==17,'Security control definition count differs from17')
check(sids<=set(re.findall(r'SEC-[A-Z]+-\d+',req)),'Security IDs missing from ALL scope')
check('DES-01' in ids,'Design requirement missing from ALL scope')
if errors:
    print('\n'.join('ERROR: '+e for e in errors));sys.exit(1)
print(f'PASS: {len(records)} complete records,17 security controls,51 closed topics, acyclic requirement dependencies, live links and frozen source hashes. Documentation checks only.')
