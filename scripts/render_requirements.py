#!/usr/bin/env python3
"""Render full requirement records from the owner-controlled catalog."""
import json
import re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / 'docs/requirement-catalog.json'

def gwt(value):
    a,b,c=value.split(', ',2)
    return f'Given {a}, when {b}, then {c}.'

def render(r):
    rid = r['id']
    owner = f"[{r['owner']}#{r['section']}](../../{r['owner']}#{r['section']})"
    arc = f"{r['architecture']}; [ARCHITECTURE](../../ARCHITECTURE.md)"
    sec = ', '.join(r['security']) + '; [SECURITY](../../SECURITY.md)'
    design = f"[DESIGN — {r['design']}](../../DESIGN.md#{r['design']})"
    read = r.get('public', False)
    f = {
      'ID': rid, 'Title':r['title'], 'Version':'1.0.0', 'Status':'Approved',
      'Owner':'jmanico (repository owner)', 'Author':'Codex under explicit user delegation',
      'Last Updated':'2026-10-13', 'Priority':'High', 'Requirement Type':'Accessibility' if rid=='DES-01' else 'Functional' if not rid.startswith('FR-9.') else 'Nonfunctional',
      'Source / Parent':owner+'; 2026-10-13 delegated default decisions; original FR provenance retained in REQUIREMENTS.',
      'Statement':r['statement'], 'Rationale':r['title']+' with an observable, consistent result.',
      'Assumptions':'None beyond the explicitly required deployment inputs and supported platforms in ARCHITECTURE.',
      'Out of Scope':'All exclusions in REQUIREMENTS Launch scope; no new behavior beyond the cited owner section.',
      'Design Traceability':design, 'Architecture Traceability':arc, 'Security Traceability':sec,
      'Applies To':'Multiple — the server and supported web/iOS/Android surfaces for this behavior.',
      'Components':arc, 'Interfaces / Operations':r['title']+'; exact read/command names and closed field contracts in ARCHITECTURE Read catalog, Command catalog and Additional contract details.',
      'Actors':'Anonymous viewers and current administrators as granted by SEC-ACCESS-02.' if read else 'Current administrators, supported clients and the specifically granted runtime/maintenance/operator identities under SEC-ACCESS-02.',
      'Preconditions':'The cited owner’s record-state, version, platform and deployment preconditions hold.',
      'Data Classification':'Public projection only; source records retain their SECURITY classifications.' if read else 'Public/Internal/Restricted as individually classified by SEC-DATA-01; no implicit public grant.',
      'Personal or Regulated Data':'Display names/opaque identity references where involved; no payment credentials, health data or customer profiles. SECURITY owns minimization/erasure.',
      'Jurisdiction / Regulatory Scope':'Operator-supplied deployment jurisdictions and release attestation under SEC-DATA-01; no inferred statutory obligation or certification.',
      'Security Objectives':'Integrity, Authorization, Availability, Accountability and Privacy under the cited controls.',
      'Control Layers':'Architecture, Authorization, Input Validation, Business-Rule Validation, Data Protection, Logging and Monitoring.',
      'Threat References':'Project STRIDE T-3/T-4/T-5 (authority/projection), T-8–T-13 (integrity), T-17/T-24 (bounded secure failure), as applicable to the cited boundary; frozen assessment in SECURITY.',
      'Abuse / Misuse Case':'Tamper with fields, references, role claims, versions or replayed operations to obtain an unauthorized disclosure or inconsistent result.',
      'Trust Boundary':'B-WAPI/B-MAPI and B-DB; ARC-OPS work additionally crosses B-OPS. UI-only rendering remains untrusted.',
      'Untrusted Inputs or Assertions':'Request fields, response records, identifiers, versions, client role labels and dependency outcomes.',
      'Authoritative Enforcement Point':'ARC-API/domain transaction for business authority; ARC-OPS for defined maintenance, with client validation as an additional boundary.',
      'Independent Verification':'Server rechecks identity/grant, schemas and owner invariants; clients validate received projections before rendering.',
      'Zero Trust Relevance':'N/A — NIST SP800-207 is not an adopted architecture claim; see SECURITY Security verification.',
      'OWASP ASVS 5.0.0':'v5.0.0-8.2.3 (permitted projection fields)' if read else 'v5.0.0-8.3.1 (trusted enforcement); security dependencies retain their separately verified owner mappings.',
      'OWASP AISVS 1.0':'N/A — no AI component.', 'NIST SP 800-53 Rev. 5':'N/A — not an adopted compliance catalog for this project.',
      'NIST SP 800-207':'N/A — no Zero Trust architecture conformance claim.',
      'Regulatory':'N/A to this requirement’s control mapping; operator legal compatibility is an explicit deployment attestation, not a claimed regulation.',
      'Other':'WCAG2.2AA for presented workflows; BCP14 for normative terms. No invented criterion IDs.',
      'Mapping Basis':'Mappings checked against the versions linked in SECURITY; product-specific tennis/commerce rules have no independent standards control mapping.',
      'On Invalid Input':'Use the exact ARCHITECTURE 400/422/409 classification, identify permitted field errors, and preserve authoritative state; AC-02 supplies the specific boundary case.',
      'On Authentication Failure':'Public reads remain permitted; protected requests require401 AUTH_REQUIRED before lookup.' if read else '401 AUTH_REQUIRED/AUTH_FAILED as appropriate; no protected data or mutation.',
      'On Authorization Failure':'SEC-ACCESS-01/02: deny ungranted action, use 403 or indistinguishable404 for inaccessible object, no change/disclosure.',
      'On Security-Decision Failure':'SEC-FAIL-01: fail closed, safe error and no unauthorized side effect; no launch exception.',
      'On External Dependency Failure':'Safe 503 for unavailable authoritative dependency; client keeps permitted last data/input. If commit may have occurred, reconcile the same operation reference under FR-8.1.',
      'On System Error':'SEC-FAIL-01 and SEC-OPS-01: safe error, rollback where possible, distinguish uncertain commit from rejection.',
      'Logging / Audit':'SEC-OPS-01 sanitized action/opaque actor/target/time/request-operation/outcome/changed fields and reason hash; no bodies, secrets or unnecessary names.',
      'Alerting':'SEC-OPS-01 exact integrity/audit/health/abuse thresholds and configured operator destination; this requirement adds no new alert.',
      'Unit Tests':'Exercise owner boundary values and state transitions specific to '+r['title'].lower()+'.',
      'Integration Tests':'Exercise the cited request/projection or transaction with real PostgreSQL fixtures; race/replay/fault cases where a mutation exists.',
      'Security Tests':'Positive/negative grants and field allowlists; invalid inputs, inaccessible references and injected security-decision failure. Apply cited client controls.',
      'Compliance Tests / Evidence':'DES-01 workflow keyboard/screen-reader/contrast/reflow evidence for UI; SECURITY control evidence. No certification claim.',
      'Acceptance-Criteria Traceability':'; '.join(f'{rid}/AC-{i:02d} → implementation suite with the same case label' for i in range(1,5))+'. Tests are required, not yet run.',
      'Coverage Target':'Every criterion and all applicable security-critical decisions/error paths, including success and rejection; SECURITY Security verification. No arbitrary overall percentage.',
      'Required Test Environment':'Synthetic isolated _test Postgres, current/revoked/absent identities, stable clock, dependency failure simulator and supported browser/native environments for UI.',
      'Upstream Requirements':', '.join(r['upstream']) or 'None.',
      'Downstream Requirements':'See the complete catalog and implementation dependency graph; this field introduces no implicit execution dependency.',
      'External Dependencies':'Selected runtime/libraries, PostgreSQL and platform credential facilities when involved; AWS only for defined operational deployment.',
      'Dependency Assumptions':'Compatibility and real deployment inputs follow ARCHITECTURE; release tests must verify actual artifacts/platforms rather than assume them.',
      'Failure Impact':'This operation becomes unavailable or unresolved, without false success, unauthorized exposure or duplicate mutation.',
      'Constraints':owner+'; '+arc+'; selected versions and bounded contracts are mandatory.',
      'Prohibited Approaches':'Client-only authorization, unvalidated casts, raw record serialization, guessed product behavior, payment integration, silent overwrite and false timeout rollback.',
      'Implementation Guidance':'Keep this behavior bounded; split implementation issues at server/web/native or independent workflow boundaries while preserving this owner contract.',
      'AI Development Guidance':'[AGENTS](../../AGENTS.md) and the applicable frozen secure-coding sources linked from SECURITY; generated code is subject to the same checks.',
      'Required Human Review':'AGENTS Branches, review and merge: human owner review for production security-sensitive code/promotion; authorized specification review can be performed by the agent.',
      'Open Decisions':'None for coding; deployment facts and runtime verification have explicit contracts and are not claimed complete.'
    }
    template=(ROOT/'REQUIREMENT_TEMPLATE.md').read_text()
    headings=re.findall(r'^## (.+)$',template,re.M)
    groups={}
    for heading in headings:
        chunk=template.split('## '+heading+'\n',1)[1].split('\n## ',1)[0]
        groups[heading]=re.findall(r'^- \*\*([^*]+)\*\*:',chunk,re.M)
    out=['# '+rid+' — '+r['title'],'']
    for h in headings:
        out+=['## '+h,'']
        if h=='Acceptance Criteria':
            outcome=gwt(r['expected'])
            invalid=gwt(r['invalid'])
            auth='Given an anonymous viewer, when this public projection is read, then its approved data is returned and no protected fields are included.' if read else 'Given a missing or revoked required grant, when the protected action is called directly, then the specified 401/403/404 response occurs without protected effects or disclosure.'
            fail='Given an unavailable authoritative dependency, when this operation is attempted, then the safe failure/last-data or same-reference uncertain-outcome behavior applies without fabricated success or partial state.'
            for i,(label,value) in enumerate(zip(['Expected behavior','Invalid or boundary behavior','Unauthorized behavior','Dependency failure'],[outcome,invalid,auth,fail]),1):out.append(f'{i}. **AC-{i:02d} — {label}**: {value}')
        else:
            for key in groups[h]:out.append(f'- **{key}**: {f[key]}')
        out.append('')
    return '\n'.join(out)

def outputs():
    records=json.loads(CATALOG.read_text())
    return {ROOT/'docs/requirements'/f"{r['id']}.md":render(r) for r in records}

if __name__=='__main__':
    for p,content in outputs().items():p.write_text(content)
    print('Rendered',len(outputs()),'full requirement records.')
