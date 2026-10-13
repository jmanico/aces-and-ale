# Product Requirements

Version 1.0.0, specification approved 2026-10-13. This document owns product behavior and its [atomic requirement records](docs/requirements/). Security and privacy policy are exclusively in [SECURITY.md](SECURITY.md); presentation in [DESIGN.md](DESIGN.md); implementation contracts in [ARCHITECTURE.md](ARCHITECTURE.md). The user explicitly delegated all remaining decisions on 2026-10-13. These are approved defaults, not evidence of working software.

## Decision provenance

The original notes required eight players, supplied names, opponents, a match plan, a scoreboard, world/local rankings, statistics, merchandising and a beer garden. Original FR-1 through FR-8 IDs remain traceable below. Earlier human decisions allowed incomplete public drafts and restricted mutations to admins. Interview Q001–Q007 selected singles, single elimination, ranking-based pairings, an organizer-chosen external ranking list, manual entry and a relative order numbered 1–8. The final delegation resolves every remaining design choice in this baseline. [The decision register](docs/clarification-interview.json) retains the interview and the closure of all 51 topics. Historical source omissions are documented as omissions, never invented facts.

## Launch scope

One deployment serves one operator/club, with any number of tournaments and venues. All admins share tournament and commerce authority as defined in SECURITY; there are no tenant partitions or extra staff roles. Players, judges, trainers, press and spectators are audience categories, not additional grants. Players do not need accounts. Public reads work without login on web, iOS and Android; all three clients support the same admin workflows. Accounts exist for invited administrators only.

Launch includes singles knockout tournaments, game/set score entry, manual ranking snapshots, calculated tournament statistics, internal merchandise sales and internal beer-garden orders. It excludes doubles, groups, consolation games, self-registration, online payments, refunds/returns/reversals, shipping, customer profiles, ingredient inventory, bookings, loyalty, uploads, exports, push notifications, offline writes, automated ranking imports and background integration jobs. A platform's ordinary share-sheet may share an existing public HTTPS tournament link; there is no custom deep-link handler. Printing uses the browser's normal print operation and is not a separate export feature.

English, left-to-right, light mode, system fonts and the existing Aces & Ale name, logo and tagline are the approved launch defaults. The operating business, real domain, signing identities and contacts are deployment inputs with explicit validation in ARCHITECTURE; they are not fictitious values assigned by this specification. Budget planning ceiling is USD 500/month for hosting, with an alert at 80%; this is a chosen planning limit, not a price quote or authority to buy services. No calendar launch deadline is imposed.

## Tournament and participant records

A tournament has a server-generated UUID, version, state, name (1–80 characters), venue label (0–120), IANA time zone (default UTC), optional planned start instant, ranking-source name (0–120 in drafts; 1–120 before seeding), and one to eight named courts (1–40 characters, unique within that tournament; default `Court 1`). Dates use explicit ISO 8601 instants; the time zone controls display. No description, photo, source URL or free-form HTML is collected. Creation requires only a name; the initial state is `draft` and the initial roster is empty.

Names and short labels are trimmed, normalized to Unicode NFC, and measured in Unicode code points after normalization. Reject empty required text, control characters and bidirectional override/isolate controls; allow ordinary international letters, marks, spaces, punctuation and emoji. Participant display names have 1–80 characters. Do not impose ASCII, real-name or uniqueness rules. Render every value as text. Duplicated names are distinguished everywhere a choice is made by an eight-character suffix of the stable player UUID.

A player has a stable deployment-wide UUID and current display name. Participation has its own UUID, a player reference, a tournament-specific display-name snapshot and an optional seed. Publication attestation and erasure constraints follow SEC-DATA-01. The same player may join multiple tournaments but may appear only once in a tournament. An admin chooses an existing player or explicitly creates a new player; the app never merges identities by name. Editing the master name affects future assignments. Correcting a tournament display-name snapshot affects that tournament's views and results only; it does not rewrite another tournament. Privacy erasure is a separate SECURITY-owned operation.

Drafts accept zero through eight distinct players. Roster addition/removal/replacement and seed edits are allowed only in drafts. A completed seed order is the permutation 1–8, where 1 is strongest. Empty seed fields are allowed in an incomplete draft; every supplied seed is an integer 1–8 and unique within that draft. Seed swaps are submitted as one roster update. Out-of-range, fractional or duplicate supplied seeds reject that update without change. The organizer resolves external-list ties or missing rankings by judgment when assigning the unique local order; the app does not interpret or verify the external list. The ranking-source name records provenance and does not trigger a lookup. Original outside-list rank numbers are not stored as seeding inputs.

Starting requires a draft with exactly eight distinct players, the complete seed permutation, a nonempty ranking-source name and a current generated seven-match plan. A schedule is optional. The transition and validation are atomic against concurrent roster/plan edits. After start, the roster, seeds, source and bracket are locked. No substitutions or redraws are supported after start.

Lifecycle: `draft → active → completed`; `draft/active → cancelled`. Completing the final completes the tournament and establishes its champion atomically. Cancellation requires a 1–240-character reason, cancels uncompleted matches and preserves already completed results/statistics; cancelled tournaments have no champion. Completed/cancelled tournaments cannot be restarted. Admins may archive completed/cancelled tournaments; archival is a read-only flag and removes them from default discovery without hiding their direct public URL. Only drafts with no retained order or sale records can be deleted; deletion removes their business records while sanitized audit metadata follows SECURITY retention. Active/completed/cancelled records cannot be deleted through normal tournament controls.

## Matches and match plan

The app generates the fixed bracket when an admin requests generation on a complete draft roster:

| Match key | Competitors | Feeds |
| --- | --- | --- |
| QF1 | Seed 1 vs seed 8 | SF1, side A |
| QF2 | Seed 4 vs seed 5 | SF1, side B |
| QF3 | Seed 3 vs seed 6 | SF2, side A |
| QF4 | Seed 2 vs seed 7 | SF2, side B |
| SF1 | Winner QF1 vs winner QF2 | F, side A |
| SF2 | Winner QF3 vs winner QF4 | F, side B |
| F | Winner SF1 vs winner SF2 | Champion |

Each match has a stable UUID, tournament reference, key, round, two side references, state, optional court/start/duration, version and score/result. Before competitors are known, the plan shows `Winner of QF1` and equivalent dependency labels, never invented names. Every match with known competitors has two distinct assigned players. No further seeding or randomization occurs. Regeneration in a draft replaces only the unplayed plan, creates new match UUIDs and resets its scheduling fields; a confirmation describes that effect. Roster or seed edits invalidate the generated draft plan, so start requires regeneration. Ranking-source or name-only edits do not change pairings.

Schedules are entered manually. A match may have no schedule or have all three of court, planned start and duration (15–360 whole minutes). Planned intervals must not overlap on a court or for any known shared competitor. A dependent match's planned start must be at or after its feeders' planned end when both are scheduled. Ambiguous/nonexistent local times require an explicit valid UTC offset; never guess daylight-saving transitions. A future opponent's possible collision is shown as a warning, not treated as a known player collision. Scheduled matches in draft/active tournaments may be rescheduled after tournament start; in-progress/completed matches cannot. These are reservations, not promises of actual match length.

Match states are `scheduled`, `in_progress`, `completed`, `cancelled`. An admin can start only a scheduled match in an active tournament with both competitors known and feeders complete. A competitor and an assigned court cannot be in two in-progress matches. Starting sets actual start time. Normal completion requires valid winning scores; exceptional completion follows the rules below. Completing a match advances its winner into the fixed next match atomically. There is no separate approval or manual advancement step.

## Scoring and corrections

All matches use best of three ordinary tie-break sets. A set ends 6–0 through 6–4, 7–5, or 7–6. At 6–6 play a tie-break to at least seven points with a two-point lead. Every set uses the same rule, including the third. Ordinary on-court games use advantage scoring; the app records games/sets, not individual ordinary-game points, server rotation or timers.

A score has an ordered list of zero through three sets. Games are integers 0–7. Completed sets precede the sole optional incomplete set. Incomplete game pairs have both values 0–6 and cannot already satisfy a completed-set condition; 6–6 remains incomplete. Once a player wins two sets, no further set is accepted. A 7–6 set requires tie-break points: either winner 7 and loser 0–5, or winner n and loser n−2 for n ≥ 8; both are integers at most 999. Other sets have no tie-break fields. The set and tie-break winners must agree. A complete normal result has exactly one player with two set wins. Winner/loser are derived server-side, not accepted as an alternative to valid scores.

Game/set updates are saved explicitly and may correct an earlier entry. Rejected updates preserve the stored score. No scores are fabricated for missing games. Before play, the scoreboard says `Not started`; a started match without games says `In progress — no score yet`; unavailable data says `Unavailable`, not zero. The tournament scoreboard includes all seven matches grouped by round, their status, competitors/placeholders, set scores, winner and exceptional-result label. Statistics appear in a separate table on the same tournament page.

A walkover completes an unstarted match when one named player is unavailable; the other wins, with no set score. Retirement completes an in-progress match with the opponent as winner and preserves the valid partial score. Both require an explicit unavailable/retiring player and a 1–240-character reason. They count as a completed win/loss under FR-5.1 and are labeled in views. If both players cannot continue, cancel the tournament; no bye, invented winner or replacement is created. Withdrawal from an active tournament is represented by a walkover/retirement at that player's next/current match; there is no separate roster substitution.

A completed result may be corrected with a 1–240-character reason. If the winner stays the same, downstream results remain. A changed winner is allowed only if every dependent match is still scheduled; update those participant references atomically. If any descendant is in progress/completed, reject the change with `DOWNSTREAM_STARTED`; do not erase later play. Correcting the final winner changes the champion of the still-completed tournament. No reopening flow is introduced. Cancelled or archived tournaments reject score changes. Concurrent edits use the expected record version: the second stale write receives `VERSION_CONFLICT`, preserves its draft input and offers reload; there is no silent last-write-wins.

## World and local rankings

These are published snapshots of player positions entered by an admin, separate from tournament seed numbers and from calculated statistics. `World` means the supplied source's worldwide ranking list; `Local` means the deployment's operator/club named by `LOCAL_SCOPE_NAME`. Neither label asserts that this app is an official ranking authority. Each scope has one current snapshot containing a source name (1–120), source as-of date, and zero through 500 entries referring to registered player UUIDs with integer position 1–1,000,000. A snapshot cannot repeat a player; equal positions are permitted, displayed as tied and ordered by normalized display name then UUID. Players missing from the list show `Unranked` where a ranking is requested; no rank is calculated from match wins.

Admins replace a complete snapshot atomically; individual edits are implemented by editing that snapshot and saving its replacement with the expected version. An empty snapshot is a deliberate unpublished/empty state, not deletion of player identity. Public views show scope, operator label for local, source, as-of date, positions and permitted player display names. At more than 30 days old a snapshot is labeled `Out of date`; it remains visible until replaced. Changes appear on the next successful read/poll. A source/as-of date in the future is rejected. There are no ranking APIs, scrapers or imports at launch. Seeding provenance is entered separately and does not automatically consume either published snapshot.

## Tournament statistics

For each assigned participant, completed matches played = wins + losses; include normal, walkover and retirement outcomes once per winning/losing participant. Scheduled, in-progress and cancelled matches contribute nothing. Win percentage = wins / played × 100 rounded half-up to one decimal. Zero played means counts 0 and percentage unavailable. Derive from current results on each read, so corrections remove the prior contribution. Statistics cover one tournament only. No cross-tournament ranking formula is introduced.

## Merchandise, beer garden and money

A deployment has one catalog and one menu shared by its tournaments. Every sale/order records one tournament reference for reporting; commerce is allowed for draft, active and completed tournaments until archived, and rejected for cancelled/archived/deleted tournaments. Existing orders in a tournament must be completed or cancelled before cancelling or archiving it. Merchandise has reference, name (1–120), integer unit-price minor units (0–100,000,000), currency, stock (0–1,000,000) and active flag. A menu item has the same fields except stock. Only EUR and USD are accepted, both with two decimal places; EUR is the form default, chosen as a product default rather than inferred from the operator's location. No conversion occurs.

Entered prices are the final amount charged per unit. No tax, discount, tip or change calculator exists. The operator handles taxation, payment collection and any receipt outside this recording tool. A zero-price item is a permitted free item. Quantities are whole numbers 1–999. Names need not be unique; references disambiguate them. An item can be renamed/repriced or marked inactive; inactive items cannot be used in new sales/orders, but existing snapshots remain. There is no physical deletion of referenced items.

An admin's stock adjustment is a signed nonzero whole number whose result remains 0–1,000,000, with a required reason (1–240). Stock can also be initialized when creating the item. Every adjustment has an operation reference and is idempotent. A merchandise sale contains one item and quantity, snapshots server-side price/currency, and decrements stock in the same transaction. Insufficient stock rejects both effects. A basket spanning multiple merchandise items is out of scope.

A beer-garden order has one to 50 distinct menu-item lines, quantities, one currency, creation time and a per-tournament display number assigned monotonically without promising gapless numbering. Duplicate menu-item lines and mixed currencies are rejected. Snapshot prices at creation; do not decrement merchandise stock or track beer/ingredient stock. Lines are fixed thereafter: cancel and create a new order to change them. Open orders appear oldest-first, with reference, display number, time, lines and total. `open → completed` creates exactly one sale; `open → cancelled` creates none. Same-state retries return the established result; changing a terminal state or reopening is rejected. Deactivating a menu item does not prevent completion of an already open order.

Reports default to the selected tournament and its full lifetime. Optional from/to instants use inclusive from, exclusive to; to must exceed from, maximum range 366 days. Report merchandise units per item and sale totals, and beer-garden completed-sale totals, separately per currency. No revenue from open/cancelled orders. Sum integer minor units and return totals as decimal integer strings to avoid numeric overflow. Sale/order totals cannot exceed 9,000,000,000,000 minor units. Refunds, returns and reversals stay excluded: mistakes in terminal sales are reconciled outside the app; historical sales are not silently edited or deleted.

## Reads, writes and failures

All mutations use a client-generated UUID operation reference and expected aggregate version where applicable. Identical reference/action/content retries return the committed result without another effect; changed action/content with that reference is rejected. Rejected operations have no partial business state. If a response is lost, show `Outcome unknown — checking` and resolve the same operation reference; never generate a fresh reference merely because a response timed out. A missing operation reference on lookup means `not_recorded`, not proof that an in-flight request was rejected; retry the same command/reference. Reference history follows SECURITY retention and is not a public object.

Public discovery lists nonarchived tournaments, newest created first with UUID tie-break, filtering by state and case-insensitive name prefix (1–80 characters). Page size defaults 20, maximum 100, using cursor pagination. Public player search/directory is excluded; player selection is admin-only. Direct links can retrieve archived tournaments during retention. Rankings list by rank/name/UUID. Commerce read order is created time descending unless the open-order queue specifies oldest-first.

Clients fetch on entering/returning to a screen and poll visible tournament/order screens every five seconds with up to one second jitter; ranking/catalog screens every 30 seconds. Stop polling when hidden/backgrounded. A mutation's successful response updates cached aggregate state immediately unless its version is older than the cached version; replay must never roll a view backward. Sale/order acknowledgements invalidate affected read queries and fetch them immediately. One failed read keeps the last visible data with `Last updated` and `Connection lost`; after 15 seconds the tournament view is labeled stale. First-load failure shows a retry action. No background/offline command queue or persisted form cache exists. A form stays in memory while its screen remains open; leaving a dirty form requires confirmation. Disable mutation submission while known offline; public last-loaded data can remain in memory and is explicitly stale. Retry transient GET failures at most twice (1s, then 2s); mutation transport retries use the same operation reference, at most twice, then manual retry/status lookup.

## Capacity and operations acceptance

The launch target is 250 concurrent public viewers, 25 simultaneously signed-in admins, 10 active tournaments, and a fixture of 10,000 historical tournaments/80,000 participations/100,000 sales. Under that fixture and 50 public reads plus five mutations per second for 60 minutes, API p95 ≤ 300 ms for reads and ≤ 500 ms for mutations, p99 ≤ 1.5 s, fewer than 0.1% unexpected 5xx, and committed score visibility within seven seconds on a healthy foreground client. Measurements include application and database time in the hosting region, excluding the user's network. Initial infrastructure/limits are design settings pending load-test evidence, not measured capacity claims.

Monthly target availability is 99.5% for public reads and admin operations, counting planned downtime. Recovery targets: at most five minutes of committed-data loss and restore within 60 minutes. Quarterly restore drills must replay privacy erasures before serving restored data. A maintenance worker performs session/invitation expiry, retention, audit export/integrity checks and backups/restore coordination; there are no business emails or notifications. Operational alerts belong to SECURITY, not participant communications.

## Atomic requirement catalog

Each linked record is a populated copy of REQUIREMENT_TEMPLATE.md with observable positive, invalid, unauthorized and failure criteria. The domain rules above supply exact values; records and implementation issues must not substitute alternate policies. Legacy FR-1.1 draft creation is traced additionally to FR-1.3/1.4, and FR-6.1 stock adjustments additionally to FR-6.5 after atomic decomposition.

| ID | Capability | Atomic requirement |
| --- | --- | --- |
| FR-1.1 | TOUR | [Start a complete eight-player tournament](docs/requirements/FR-1.1.md) |
| FR-1.2 | TOUR | [Display supplied participant names](docs/requirements/FR-1.2.md) |
| FR-1.3 | TOUR | [Create an empty public tournament draft](docs/requirements/FR-1.3.md) |
| FR-1.4 | TOUR | [Replace the draft roster and seeds atomically](docs/requirements/FR-1.4.md) |
| FR-1.5 | TOUR | [Cancel an unfinished tournament](docs/requirements/FR-1.5.md) |
| FR-1.6 | TOUR | [Archive completed or cancelled tournaments](docs/requirements/FR-1.6.md) |
| FR-1.7 | TOUR | [Maintain explicit player identities](docs/requirements/FR-1.7.md) |
| FR-1.8 | TOUR | [Correct a tournament name snapshot](docs/requirements/FR-1.8.md) |
| FR-1.9 | TOUR | [Edit tournament metadata](docs/requirements/FR-1.9.md) |
| FR-1.10 | TOUR | [Delete an eligible draft](docs/requirements/FR-1.10.md) |
| FR-2.1 | PLAN | [Read the complete match plan](docs/requirements/FR-2.1.md) |
| FR-2.2 | PLAN | [Generate the fixed seeded bracket](docs/requirements/FR-2.2.md) |
| FR-2.3 | PLAN | [Schedule a match without known conflicts](docs/requirements/FR-2.3.md) |
| FR-3.1 | SCORE | [Read the tournament scoreboard](docs/requirements/FR-3.1.md) |
| FR-3.2 | SCORE | [Save an in-progress game/set score](docs/requirements/FR-3.2.md) |
| FR-3.3 | SCORE | [Start an eligible match](docs/requirements/FR-3.3.md) |
| FR-3.4 | SCORE | [Validate best-of-three set scores](docs/requirements/FR-3.4.md) |
| FR-3.5 | SCORE | [Record a walkover or retirement](docs/requirements/FR-3.5.md) |
| FR-3.6 | SCORE | [Complete and advance a normal result](docs/requirements/FR-3.6.md) |
| FR-3.7 | SCORE | [Correct a completed result safely](docs/requirements/FR-3.7.md) |
| FR-4.1 | RANK | [Read world ranking snapshots](docs/requirements/FR-4.1.md) |
| FR-4.2 | RANK | [Read local ranking snapshots](docs/requirements/FR-4.2.md) |
| FR-4.3 | RANK | [Replace a ranking snapshot atomically](docs/requirements/FR-4.3.md) |
| FR-5.1 | STATS | [Derive current tournament statistics](docs/requirements/FR-5.1.md) |
| FR-6.1 | MERCH | [Maintain merchandise catalog records](docs/requirements/FR-6.1.md) |
| FR-6.2 | MERCH | [Record one stock-backed merchandise sale](docs/requirements/FR-6.2.md) |
| FR-6.3 | MERCH | [Report retained merchandise sales](docs/requirements/FR-6.3.md) |
| FR-6.4 | MERCH | [Retire merchandise from new sales](docs/requirements/FR-6.4.md) |
| FR-6.5 | MERCH | [Adjust stock with an accountable delta](docs/requirements/FR-6.5.md) |
| FR-7.1 | BEER | [Maintain menu items and retirement](docs/requirements/FR-7.1.md) |
| FR-7.2 | BEER | [Create a fixed beer-garden order](docs/requirements/FR-7.2.md) |
| FR-7.3 | BEER | [Resolve an order into one terminal outcome](docs/requirements/FR-7.3.md) |
| FR-7.4 | BEER | [Report completed beer-garden sales](docs/requirements/FR-7.4.md) |
| FR-7.5 | BEER | [Read the open order queue](docs/requirements/FR-7.5.md) |
| FR-8.1 | COMM | [Reconcile stable mutation outcomes](docs/requirements/FR-8.1.md) |
| FR-8.2 | COMM | [Represent money without payment processing](docs/requirements/FR-8.2.md) |
| FR-9.1 | TOUR | [Discover public tournaments by cursor](docs/requirements/FR-9.1.md) |
| FR-9.2 | CORE | [Deliver platform parity](docs/requirements/FR-9.2.md) |
| FR-9.3 | CORE | [Refresh views and preserve uncertainty safely](docs/requirements/FR-9.3.md) |
| FR-9.4 | OPS | [Meet the bounded launch capacity profile](docs/requirements/FR-9.4.md) |
| FR-9.5 | OPS | [Recover within defined loss and time targets](docs/requirements/FR-9.5.md) |
| FR-9.6 | OPS | [Run bounded maintenance jobs](docs/requirements/FR-9.6.md) |
| FR-9.7 | OPS | [Measure monthly service availability](docs/requirements/FR-9.7.md) |
| DES-01 | CORE | [Accessible complete launch workflows](docs/requirements/DES-01.md) |

Security requirements in scope (owned only by SECURITY): SEC-AUTH-01, SEC-AUTH-02, SEC-AUTH-03, SEC-AUTH-04, SEC-ACCESS-01, SEC-ACCESS-02, SEC-INPUT-01, SEC-DATA-01, SEC-DATA-02, SEC-SESSION-01, SEC-TRANSPORT-01, SEC-WEB-01, SEC-MOBILE-01, SEC-RUNTIME-01, SEC-OPS-01, SEC-SUPPLY-01, SEC-FAIL-01. Design requirement in scope: DES-01 in DESIGN.md. These IDs are included in `Scope: ALL` for implementation planning; the owner documents define their acceptance obligations.

## Resolved question register

OQ-1/2: singles, fixed eight-player single elimination. OQ-3: tournament fields above. OQ-4: capped drafts and explicit lifecycle. OQ-5: UUID identity, normalized names and separate name snapshots. OQ-8: manually assigned 1–8 seeds, named outside source, generated fixed bracket and optional manual schedule. OQ-9: versioned edits with downstream-result protection. OQ-10/11: best-of-three tie-break sets, game/set entry, exceptional outcomes and bounded polling. OQ-13/14: separately entered world/local snapshots. OQ-17: no external business-data integration. OQ-18: explicit empty/stale/unavailable states and future-round labels. OQ-19: capacity/recovery targets above. Original OQ-6/7/20 remain owned by SECURITY and are resolved there. Original OQ-12/15/16 remain covered by statistics/commerce rules above.

## Open Questions

None for the launch coding baseline. Runtime configuration and release evidence have explicit contracts in ARCHITECTURE, SECURITY and AGENTS; their eventual values/evidence are not assertions that deployment or implementation already exists. Future scope changes require an owner-document change rather than an undocumented implementation choice.
