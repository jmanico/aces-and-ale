# Agent Instructions

## Load Specifications Only When Needed

This file contains agent operating and authoring guidance. The domain documents are **not eager imports**. Read the relevant owner only when needed for the current task, and consult another owner when the task crosses its domain; do not automatically load every specification for unrelated work.

| Task or decision | Read its owner |
| --- | --- |
| Functional/nonfunctional behavior, business records, workflows, testable product acceptance criteria | [REQUIREMENTS.md](REQUIREMENTS.md) |
| Brand/logo, tokens, typography, layout, components and accessibility | [DESIGN.md](DESIGN.md) |
| Components, interfaces, data flows, trust-boundary topology, technology choices and rationale | [ARCHITECTURE.md](ARCHITECTURE.md) |
| Any security requirement, threat, posture, privacy/disclosure control, authorization or boundary enforcement | [SECURITY.md](SECURITY.md) |
| New GitHub issue or requirement authoring | [REQUIREMENT_TEMPLATE.md](REQUIREMENT_TEMPLATE.md) and the affected owner |

Security owns overlaps involving security policy. Put each rule in its owner; nonowners link rather than reauthor it. Preserve distinct facts, constraints, decisions, source provenance and caveats when relocating content. Architecture may place a control at a boundary but links to SECURITY for what the control enforces. Do not silently promote an assumption into a decision.

## Working Rules

- Every new GitHub issue MUST follow [REQUIREMENT_TEMPLATE.md](REQUIREMENT_TEMPLATE.md) so each issue is a structured, testable requirement.
- Do not invent workflow, tooling or process details; mark unresolved choices explicitly `TO BE DECIDED`. `UNKNOWN` may identify unavailable historical facts; `ASSUMPTION` labels unapproved proposals.
- Follow the affected owner's verification requirements, including [security verification](SECURITY.md#security-verification) when security-critical decisions or error paths are involved. Select checks appropriate to the change; do not claim implementation conformance from document review.
- Record setup/build/test/run/release guidance here when actually decided. Do not infer commands or review gates from template examples.

## Requirement Authoring

- Use one template per atomic, independently testable requirement; split compound behavior where outcomes are independently specifiable. Uppercase normative terms use BCP 14 semantics (RFC 2119 and RFC 8174); prefer `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT` and `MAY`.
- Replace bracketed placeholders. Use `N/A` only after evaluating nonapplicability and `TO BE DECIDED` for unresolved inputs.
- Each acceptance criterion MUST describe one independently testable observable pass/fail outcome, identifying preconditions, action and expected result within the statement's scope, without introducing new behavior. Use Given/When/Then or an equally explicit form.
- Include only standard mappings verified against the cited version; do not guess control IDs. Record evaluated nonapplicability as `N/A`, unassessed applicability/mapping as `TO BE DECIDED`.
- Template security/context/failure/reviewer fields reference owner policy; filling a field does not authorize a new control exception or approval gate. Security coverage and failure rules belong exclusively to [SECURITY.md](SECURITY.md).

## Development Workflow

These decisions were adopted under the user's 2026-10-13 delegation. This repository currently contains specifications and their validator; application commands below are the explicit contract to implement in the first relevant engineering issues, not commands falsely claimed to exist today.

### Checks available now

```sh
python3 scripts/check_specs.py
```

Python3.11+ standard library only. The GitHub workflow `spec-check` runs this on pull requests and main. Documentation-only changes require this check and owner consistency review; they do not claim application conformance. The original clone commands remain valid:

```sh
git clone https://github.com/jmanico/aces-and-ale.git
cd aces-and-ale
```

### Application setup and command contract

Support macOS and Linux development with the exact Node/pnpm versions in ARCHITECTURE; native iOS builds require macOS/Xcode compatible with the selected Expo SDK, Android uses the SDK version selected by that Expo release. Use Docker Compose for local PostgreSQL17.11. Workspace/package names are `@aces/web`, `@aces/mobile`, `@aces/api`, `@aces/domain`, `@aces/contracts`, `@aces/design`. Root scripts MUST expose these commands when implemented:

| Command | Defined behavior |
| --- | --- |
| `pnpm install --frozen-lockfile --ignore-scripts` | Install reviewed locked packages without lifecycle execution; fail mismatch |
| `pnpm rebuild` | Run only committed, reviewed onlyBuiltDependencies allowlist; unknown lifecycle scripts remain disabled |
| `pnpm db:up` / `pnpm db:down` | Start/stop local Postgres Compose service; down preserves volume; destructive reset requires explicit separate operator action |
| `pnpm db:migrate` | Apply/checksum ordered SQL migrations using migration credentials; no production default |
| `pnpm db:seed` | Synthetic fixtures only, reject DB names outside _dev/_test |
| `pnpm dev` | Start API8080 and Vite5173 with same-origin dev proxy; local .env.example contains nonsecret placeholders and required-field explanations |
| `pnpm dev:mobile` | Start Expo development build tooling against configured staging HTTPS API |
| `pnpm build` | Type-check then build all workspace packages and web/API artifacts; native signed builds are separate |
| `pnpm lint` / `pnpm format:check` / `pnpm typecheck` | ESLint, Prettier check, full-project tsc noEmit respectively |
| `pnpm test` | Vitest domain/unit suites |
| `pnpm test:integration` | Vitest with isolated real Postgres test DB, transactions/concurrency/fault injection |
| `pnpm test:web` | Playwright supported browsers, accessibility fixtures and passkey virtual-authenticator tests |
| `pnpm test:native:ios` / `pnpm test:native:android` | Platform UI/integration harness; device passkey checks and accessibility evidence also required |
| `pnpm test:load` | Seed published capacity fixture and exercise REQUIREMENTS profile60min; record latency/5xx/visibility evidence |
| `pnpm start` / `pnpm worker` | Production compiled API / elected maintenance worker entry points |
| `pnpm operator` | Protected operator CLI for bootstrap, invitation revoke, break-glass and recovery; never a public endpoint |
| `pnpm audit --json` | Dependency advisory evidence; high/critical applicable findings block promotion per SECURITY |
| `pnpm release:staging` / `pnpm release:production` | Invoke environment-scoped GitHub deployment workflow with immutable image/native artifact digests and release evidence reference |
| `pnpm restore:verify` | Isolated backup restore, erasure replay and measured RPO/RTO verification; no serving production traffic |

Do not put real secrets in examples or pass them as CLI arguments. Select secrets by environment identity/secret store. Scripts and .env.example must be implemented with their owning feature, not presumed present. Do not introduce alternate commands or tools without updating this table and the affected owner.

### Branches, review and merge

Use `docs/short-description`, `feat/short-description`, `fix/short-description` or `chore/short-description`; conventional commit prefixes docs/feat/fix/chore/test. One coherent PR references requirements/issues, describes changed behavior and actual validation. Squash merge to main after applicable CI passes, no direct pushes to main. Repository owner jmanico is initial product/release/security policy owner. Agent-authored reversible documentation may be reviewed/merged by the agent when the user explicitly authorizes it, as in this session. Production security-sensitive implementation and production promotion require recorded human owner review; this release gate does not block the currently authorized specification PR or issue creation. No additional reviewer/staff roles are implied.

Every security decision/error path needs positive/negative coverage under SECURITY; ordinary code has no arbitrary percentage gate. Test only relevant changes, with broader release suites at promotion. Each user-visible feature includes web/native accessibility evidence in its own scope. Track status Approved for specifications, Implemented only after code exists, Verified only with evidence. Bump patch for editorial corrections, minor for backward-compatible requirements, major for incompatible contracts.

### Release and deployment

GitHub Actions CI runs spec-check plus typecheck/lint/format/unit/integration/web checks for affected implementation. Native build/test gates run for native changes on compatible macOS/Android runners. Build immutable OCI images, generate SBOM/advisory/script/lock/test evidence and sign provenance through GitHub OIDC; pin action SHAs and build-image digests when creating the actual workflow after verifying their releases. These supply-chain pins are artifact identity, not additional product scope.

Main deploys to staging after CI. Production is an explicit environment promotion by jmanico with recorded SECURITY review, real ARCHITECTURE deployment inputs, backup/restore evidence and smoke checks; this specification task does not deploy software. Apply compatible migrations first using migration role, deploy immutable API/worker image via ECS rolling update with automatic failed-deploy rollback, then smoke public read/admin ceremony/business mutation/operation lookup. Keep previous image/migration-compatible schema for seven days; rollback application image without destructive reverse migrations. Failed irreversible data migration requires tested restore/forward repair, not an invented automatic downgrade.

Native releases use local CI-generated Expo prebuild projects, Xcode archive/App Store Connect for iOS and Gradle signed AAB/Play Console for Android; protected signing credentials and separate staging/prod bundle/package IDs. Distribute staging via TestFlight/internal testing, production via store review. API remains compatible with the previous native release for at least 90 days; incompatible API evolution uses a new versioned route. Human release evidence names exact tested devices/browsers, signing fingerprints, runtime/dependency versions and artifact digests. Actual accounts/domains/contact/legal facts are required deploy inputs, never fabricated defaults.
