# Design

Version 1.0.0. The user's2026-10-13 delegation approves the existing Aces & Ale identity and the defaults below. This owner defines presentation and accessibility, not business rules or grants. [REQUIREMENTS](REQUIREMENTS.md) owns behavior; [ARCHITECTURE](ARCHITECTURE.md) owns client/contracts; [SECURITY](SECURITY.md) owns disclosure and enforcement. **DES-01** is the complete-workflow presentation/accessibility requirement, formalized in [its requirement record](docs/requirements/DES-01.md).

## Brand and logo

Name: **Aces & Ale**. Tagline: **Eight players. Every match. Beyond the court.** Personality: calm, practical and welcoming; clear scores and readable controls take priority over decoration. Existing [logo.svg](logo.svg) is the approved generic tennis-ball mark; [README variant](docs/assets/readme-logo.svg) supplies its white clear-space canvas. No wordmark, mascot, stock photography, external fonts or additional brand assets are required. Original brand approval history was not supplied; this paragraph records the new delegated approval, not invented history.

Use the original square64×64 viewBox, minimum 24×24 CSSpx/native points, with clear space at least one quarter of displayed width on every side. Keep dark silhouette and white seams, on white or the light page background. Never stretch, rotate, crop, recolor, shadow or place over photographs/dark backgrounds. Meaningful logo has an accessible name; hide decorative duplicates from assistive technology. A header logo link navigates to the public tournament list and is named `Aces & Ale — tournaments`.

## Color palette

Light mode only; no theme toggle. Both platforms retain the light palette even when the OS is dark. Status always uses words/icons in addition to color; red/green never identifies players.

| Token | Value | Use |
| --- | --- | --- |
| primary | #1F2937 | Actions, links, focus, logo |
| secondary | #4B5563 | Supporting text/boundaries |
| background | #F9FAFB | Page background |
| surface | #FFFFFF | Cards/fields/inverse labels |
| text | #111827 | Main text and numbers |
| error | #B91C1C | Errors |
| success | #166534 | Confirmed success |

Approved text pairs: text/primary/secondary/error/success on surface or background, and surface on primary. Preserve contrast on hover/pressed/disabled states; indicate interaction with underline/boundary/wording rather than opacity alone. No gradients or motion decoration.

## Typography

Use system-ui, -apple-system, BlinkMacSystemFont, Segoe UI, sans-serif on web; platform system font on native. Weights400/600/700. Web base1rem follows user defaults (ordinarily16CSSpx); native base16sp/points with platform font scaling enabled, never clamp maximum size. Supporting14, body/controls16, section20, page/score32; native values map the same numeric sizes and text-scale preferences. Line heights1.5 for body/support,1.3 section,1.2 page/score. Tabular numerals when supported. Names wrap; full text always remains accessible. No automatic capitalization changes. Inline `bdi`/native direction isolation protects mixed-script names without accepting override control characters prohibited by REQUIREMENTS.

## Layout and spacing

Spacing4/8/12/16/24/32/48px (native density-independent points). Gap8 within related controls,16 within groups,24/32 between groups. Fluid max-width1200px, gutters16 below640,24 below1024,32 above; 4/8/12-column grids respectively. Native uses equivalent width classes in logical points and safe-area insets. Collapse to one logical reading order at narrow widths; no page-wide horizontal scrolling at 320CSSpx or200% zoom. An essential comparison table may scroll inside a labeled region with persistent row/column context. Support phone, tablet, desktop and ordinary large browser windows320–1920px; no separate TV/kiosk app. Test indoor and bright outdoor readability at normal device brightness, without promising sunlight hardware performance.

## Navigation and screens

Public landing is `/tournaments`; persistent destinations `Tournaments`, `Rankings`, `Sign in`. Signed-in admins additionally see `Players`, `Catalog`, `Menu`, `Accounts`, and their `Account`/`Sign out`. Revoked admins see only public destinations and own Account/Sign out. Native uses the same labels in a drawer opened by a named menu button; public Tournaments and Rankings are bottom tabs, detail screens push on the navigation stack. Web uses header links and responsive menu below640px; active destination has aria-current. Menu/modal focus returns to its trigger on close; navigation moves focus to the new page heading on web and announces the new native screen title.

| Route / native screen | Contents and authorized actions |
| --- | --- |
| `/tournaments` | Search name prefix, state filter, newest-first cards, explicit empty state, `Load more`; admin `Create tournament` |
| `/tournaments/:id` | Name/state/venue/time zone, public Overview, Match plan, Scoreboard, Statistics tabs; admin `Manage`, `Commerce`; public direct archived banner |
| `/tournaments/new`, `/tournaments/:id/manage` | Metadata, court names, ranking source, roster slots1–8 and seed fields; select/create player, name correction, generate/replace plan, start/cancel/archive/delete according to state |
| `/tournaments/:id/matches/:matchId` | Read-only competitors/status/score and schedule; admin schedule, start, set-score entry, complete, walkover/retirement and completed-result correction forms when allowed |
| `/rankings` | World/Local tabs, source/as-of/local label, tied positions and stale banner; admin `Edit snapshot` opens full bounded editor with add/remove player rows, position and publication metadata |
| `/players` | Admin search/select/create player; master-name edit, fresh-proof `Erase personal data` action with consequences; no public directory |
| `/catalog`, `/menu` | Admin item cards/table, active filter, create/edit/retire; catalog stock and `Adjust stock` with reason |
| `/tournaments/:id/commerce` | Admin merchandise sale form, beer order creation and open queue, sales history and reports; explicit selected tournament/context and currency |
| `/orders/:id` | Admin fixed lines, display number/time/state/total; open-only complete/cancel; terminal outcome and retry/reconciliation feedback |
| `/signin`, `/enroll` | Passkey sign-in; enrollment invitation pasted into a field, display-name notice from invitation, credential label, native/browser ceremony, optional second-device encouragement |
| `/account` | Own credential labels/times, Add passkey, Rename, Remove, Sign out; expired/revoked session notice |
| `/accounts` | Admin list/status, invite (show token once with copy button), revoke/disable/account erasure with fresh passkey proof and reason; last-admin guard explanation |

No unsupported workflow is added by this screen inventory. Native screen names map to these paths but do not register custom deep-link handlers. Header/footer includes operator privacy notice and security contact from the public deployment projection. Account-free players have no profile/login screen.

## Tournament and score presentation

Roster editor shows count `N of 8 players`, required source and seed helper `1 is strongest; use each number once`. Do not label seeds as actual external ranking positions. Existing names plus shortUUID suffix disambiguate choices; an admin explicitly chooses existing versus new identity. Show required public-name attestation at roster assignment under SECURITY, warning that names are public immediately, including drafts. Seed swaps save the full roster atomically. Locked fields show why and remain readable. Generate/replace confirmation states that replacement resets schedules; start summarizes eight assigned players and current plan.

Match plan uses three labeled round sections, four/two/one match cards in canonical QF1/QF2/QF3/QF4/SF1/SF2/F order, collapsing to a vertical list on small screens. Connector lines are optional decoration and never the sole representation of progression. Each card includes exact feeder labels until players are known, court and local planned time/duration or `Not scheduled`, status and a match link. Schedule errors identify the conflicting court/player/match; uncertain future-player overlap is a warning. Date/time forms show tournament time zone and explicit UTC offset where needed; ambiguous local choices offer both valid offsets, nonexistent times reject without silent shifting.

Scoreboard groups all matches by round. Display two named competitor rows per match with set columns and winner/status words; do not use color alone. Editing exposes game fields per ordered set and tie-break fields only at 7–6. `Save score` and `Complete match` are distinct actions. Walkover/retirement require unavailable player plus internal reason; public views show the outcome label but never the reason. Result-correction form displays existing result, corrected result and downstream-change impact before save; a blocked change explains `A later match has already started`. Statistics shows participant, played, wins, losses and win percentage; unavailable percentage is an em dash with accessible label `No completed matches`.

Rankings show scope/source/as-of visibly above ordered rows. Ties use `Tied` text; missing is `Unranked`, empty snapshot `No rankings published`, stale `Out of date`. Source labels are inert text, not links or a claim of official status. Snapshot editor identifies duplicates and preserves draft values on conflict.

## Commerce presentation

Always show selected tournament, currency code, quantity and per-unit/line/total amounts. No payment-card fields, checkout/payment success wording, refund button or implied tax calculation. Sale button is `Record sale`; order completion is `Record completed order`. Confirmation means the record committed, not that money was collected. Catalog/menu edit helpers explain that prior snapshots remain unchanged. Stock adjustments show current stock, signed change, resulting stock and required reason; reject zero/range errors inline.

Order editor permits 1–50 distinct items, fixed lines after create, one currency. Open queue oldest-first shows display number/time/total plus Open link; completion/cancellation actions belong to the order detail. Reports show time filter (or All time), inclusive/exclusive boundary helper, currency-separated totals and merchandise item quantities. Terminal sale mistake guidance says `Recorded sales cannot be reversed here. Reconcile the mistake outside the app.` Never claim a timed-out write failed; use the shared outcome-unknown state.

## Components and feedback

Buttons use explicit action labels,4px radius,44×44 minimum target on both platforms, primary fill/secondary outline. Inputs have persistent labels, required/optional wording, helper text, appropriate native keyboard and associated errors; placeholders are examples only. Links are underlined primary text. Web focus is2px primary outline plus2px surface gap, fully visible. Native uses platform focus indicators and accessibility labels/roles/states; do not replace native text entry with gesture-only widgets. Destructive actions (delete, cancel, archive, retire, erasure, credential removal, grant revoke/disable) show a named confirmation dialog describing the exact effect and Cancel default; a confirmation does not create an extra server approval requirement.

| State | Presentation / action |
| --- | --- |
| Initial loading | `Loading…` status and noninteractive skeleton, no fabricated scores/zero totals |
| Empty | Explain entity-specific absence: `No tournaments yet`, `No players assigned`, `Generate the match plan`, `No rankings published`, `No open orders`, `No recorded sales`; show only permitted next action |
| Incomplete match | `Not started`, feeder labels, or `In progress — no score yet` per REQUIREMENTS |
| Read failure | Last data + Connection lost/Last updated; initial failure has Retry; never silently replace data with empty rows |
| Stale | Tournament data older than 15s after failure labeled Stale; rankings >30days use Out of date |
| Pending mutation | Preserve form, disable duplicate submit, `Saving…`; success only on committed acknowledgement |
| Unknown outcome | `Outcome unknown — checking`; look up/retry same reference, manual `Check again`, no new mutation reference |
| Version conflict | Preserve entered fields, explain another admin changed data, `Reload latest`; do not automatically resubmit against a newer version |
| Offline | Explicit banner; loaded data read-only and stale, mutations disabled, no queued writes |
| Auth cancelled/unsupported/lost | Neutral cancellation retry, supported-device guidance, optional second-device advice; lost-all-passkeys explains new-account contact process under SECURITY |

Web uses polite live regions for save/status/score updates, assertive only blocking form errors; native uses accessibility announcements with the same messages. Coalesce polled score changes into at most one announcement every 5s, identify changed match/result, never reread the entire scoreboard or steal focus. Loading/polling does not shift keyboard focus. Error summary links to individual fields; first submit error focuses summary, asynchronous updates preserve focus. Dirty form navigation uses Continue editing/Discard changes. Modals have named heading, focus containment, Escape/back cancellation and return focus. Motion is limited to immediate state changes; honor reduced-motion without essential animation.

## Formatting and accessibility

English LTR UI. Use Intl with en-GB for dates/numbers, display tournament local date/time using24-hour time plus zone abbreviation/UTC offset; as-of ranking dates are calendar dates, not time-zone converted. Money always shows currency code and two decimal digits (for example EUR12.50); parse typed prices as decimal text into integer minor units, never binary floating-point arithmetic. Percentages show one decimal; use words/screen-reader labels for empty values.

DES-01 MUST meet WCAG2.2AA for complete supported web workflows and equivalent native accessibility outcomes:4.5:1 ordinary text,3:1 large text/meaningful nontext boundaries, keyboard operation, no traps, unobscured focus, programmatic names/roles/states, correct headings/table associations, text scaling/reflow, no color-only information, visible error/recovery feedback and accessible authentication. Passkeys must not require memorization/puzzles. Target44px controls exceeds the minimum touch-target baseline. Accessibility evidence includes automated axe-core checks in browser tests (versions pinned in ARCHITECTURE), keyboard/manual320px+200%/400% zoom, VoiceOver/Safari, NVDA/Firefox, VoiceOver/iOS and TalkBack/Android, largest supported native text setting, contrast measurements and reduced-motion checks. Each feature includes its own accessibility cases; automated scans alone do not establish conformance. [WCAG2.2](https://www.w3.org/TR/WCAG22/) is the normative web standard; actual device/browser versions are captured at release.

## Resolved design questions

D01–D09: existing name/tagline/mark approved; neutral palette/system fonts final; light-only;320–1920px/points and native mapping; explicit public/admin navigation; seeded round/score/statistics layouts; catalog/orders/reports; English formatting; all loading/empty/stale/error/pending/unknown/auth states above. No separate dark assets, exports or unapproved dashboard behavior.

## Open Questions

None for coding. Preserve owner constraints when adapting layouts to each platform.

An enrollment response lost after key creation leads to a fresh passkey sign-in and then operation-status reconciliation. The UI never promises that a lost token can be recovered from logs or replay. If an invitation was created but its one-time token response is lost, show its invitation ID and explain that the operator must revoke it before issuing another. These are the recovery contracts in ARCHITECTURE, not alternative authentication paths.
