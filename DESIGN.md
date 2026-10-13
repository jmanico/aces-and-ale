## Required Design Inputs

- Brand personality: TO BE DECIDED
- Primary audience: Players, judges, admin, press, trainers, audience. Responsibilities and permissions: UNKNOWN.
- Platform targets (web / mobile / both): TO BE DECIDED
- Light / dark mode: TO BE DECIDED
- Existing brand assets: UNKNOWN

## Brand and Logo

Product name in the supplied requirements: UNKNOWN. Brand direction: TO BE DECIDED. The specifications below are neutral design defaults, not inferred brand preferences or additional product requirements.

`logo.svg` is a single generic tennis-ball mark: a dark circular silhouette with two white curved seams. It represents tennis only. It contains no lettering, mascot, external asset, gradient, or affiliation imagery. Naming and any future wordmark: TO BE DECIDED.

- Use the supplied 64 × 64 viewBox at its original square proportions, on `background` or `surface`.
- Minimum display box: 24 × 24 CSS pixels. Clear space: at least one quarter of the displayed box width outside the box on every side.
- Colors: `primary` #1F2937 and `surface` #FFFFFF. The SVG canvas is transparent; white seams are opaque.
- Do not stretch, rotate, crop, recolor, add shadows, place over photographs, or combine with an unapproved wordmark. Dark-background use: TO BE DECIDED.
- When meaningful, provide an accessible name describing the mark or its control's action. When adjacent text supplies the same meaning, hide the decorative mark from assistive technology. Do not make the mark a navigation control unless a destination is specified.

## Color Palette

Neutral light-surface defaults; final brand colors and supported modes: TO BE DECIDED.

| Token | Hex | Use |
| --- | --- | --- |
| `primary` | `#1F2937` | Main actions, links, focus indicator, logo silhouette |
| `secondary` | `#4B5563` | Supporting text and control boundaries |
| `background` | `#F9FAFB` | Page background |
| `surface` | `#FFFFFF` | Content surfaces, field interiors, inverse labels |
| `text` | `#111827` | Main text and numeric information |
| `error` | `#B91C1C` | Error text and indicators |
| `success` | `#166534` | Confirmed-success text and indicators |

Approved text/background pairs: `text`, `primary`, `secondary`, `error`, or `success` on `surface` or `background`; `surface` text on `primary`. All exceed 4.5:1. Do not use other text pairings without checking contrast. Use the same approved colors for hover, adding an underline or boundary change instead of reducing opacity. Communicate feedback through words as well as color. Red and green do not imply player identity, ranking position, or match outcome.

## Typography

Brand typography: UNKNOWN. Broader typography direction: TO BE DECIDED. Default family: `system-ui`, falling back to `-apple-system`, `BlinkMacSystemFont`, `"Segoe UI"`, then `sans-serif`. Native system fonts provide readable text without external font assets.

| Role | Size | Line height | Weight |
| --- | --- | --- | --- |
| Supporting text | 0.875rem | 1.5 | 400 |
| Body, controls | 1rem | 1.5 | 400; 600 for labels |
| Section heading | 1.25rem | 1.3 | 600 |
| Page heading | 2rem | 1.2 | 700 |
| Score emphasis | 2rem | 1.2 | 700 |

Reference size: 1rem equals the user's default text size, ordinarily 16 CSS pixels. Supported weights: 400, 600, 700. Use tabular numerals for scores and ranking values where available. Wrap long player names; do not use clipping as the only presentation. Preserve normal capitalization and user text-size preferences.

## Layout and Spacing

- Spacing scale: 4, 8, 12, 16, 24, 32, 48 CSS pixels. Use 8 between related elements, 16 within groups, and 24 or 32 between groups.
- Use a fluid content area with a maximum width of 1200 CSS pixels. Basic grid: four columns below 640, eight from 640, twelve from 1024 CSS pixels; content may span the full grid.
- Responsive breakpoints: 640 and 1024 CSS pixels. Outer gutters: 16, 24, and 32 CSS pixels respectively. These are layout defaults, not commitments to a platform.
- Collapse independent regions into a single reading order when space is insufficient. Preserve the same logical reading and keyboard order across sizes.
- Keep scores adjacent to their corresponding player names. Label world and local ranking scope explicitly. Use aligned rows for comparisons, with descriptive headers where data is tabular.
- At 320 CSS pixels wide, reflow content without page-wide horizontal scrolling. Any essential two-dimensional table may scroll within a clearly identified region without losing access to its labels.
- Tournament structure, navigation, scoring subdivisions, and statistics presentation remain TO BE DECIDED where the requirements leave behavior open. Do not assume a knockout bracket, live updates, or role-specific dashboards.

## Components

Apply these conventions only where an interaction is supported by resolved requirements. They do not authorize new workflows.

- **Buttons:** Clear action labels; one visually dominant action per action group when applicable. Primary: `primary` fill with `surface` text. Secondary: `surface` fill with `primary` text and boundary. Use 4 CSS pixel corner radii and a default 44 × 44 CSS pixel minimum target. Explain unavailability in nearby text when needed; do not rely on faded text alone.
- **Inputs:** Persistent visible labels, helper text before entry, and an explicit required/optional indicator when the rule is known. Use `surface` interiors, `text` content, and `secondary` boundaries. Do not invent fields or validation rules. Placeholders never replace labels.
- **Links:** Underlined `primary` text with descriptive wording. Preserve a visible distinction from surrounding text without relying on color. Distinguish navigation from action controls consistently.
- **Focus:** Use a 2 CSS pixel `primary` outline separated by a 2 CSS pixel `surface` gap. Keep it visible on all sides, including within scrolling regions. Never remove focus indication or obscure the focused control.
- **Feedback:** Explain errors in text next to the relevant field, associate messages with that field, and preserve entered values. For multiple errors, provide a summary linking to affected fields. Announce relevant feedback without unexpectedly moving focus. Use success messages only after confirmed completion.
- **Data presentation:** Keep player names and scores unambiguously associated. Use meaningful table headers for comparable data. Represent unavailable values explicitly when that state is supported; never substitute zero. Empty-state wording and recovery actions depend on resolved requirements.

## Accessibility

- Target conformance: WCAG 2.2 AA. Verify complete implemented workflows, not just individual components.
- Require at least 4.5:1 text contrast, or 3:1 for large text: at least 24 CSS pixels regular or approximately 18.7 CSS pixels bold. Required control boundaries, meaningful graphics, and focus indicators must meet 3:1 against adjacent colors.
- Make every interaction keyboard-operable, with logical focus order, visible focus, and no keyboard traps. Focus must not be hidden by other content.
- Provide programmatic names, roles, states, labels, and heading structure. Expose data relationships to assistive technology. Do not use color, shape, or position as the sole instruction or status cue.
- Support 200% text resizing, reflow at 320 CSS pixels, and user text-spacing overrides without lost information or controls.
- Default to 44 × 44 CSS pixel interaction targets; meet WCAG's 24 × 24 CSS pixel minimum or its applicable spacing exceptions in compact layouts.
- Avoid nonessential motion. Respect reduced-motion preferences by removing decorative animation and smooth movement. If dynamic score updates are later required, avoid focus movement and excessive announcements; announcement behavior remains TO BE DECIDED.

## Open Questions

- **OQ-1** What product name should the requirements establish, and is a wordmark needed? The source requirements do not name the product.
- **OQ-2** What brand personality and approved brand assets should replace the neutral defaults?
- **OQ-3** Are the targets web, mobile, or both, and what viewing conditions and display sizes are essential?
- **OQ-4** Is light mode alone sufficient, or is dark mode required?
- **OQ-5** Which actor actions and permissions determine navigation, editable controls, and read-only views?
- **OQ-6** What tournament format, match-plan fields, score detail, statistics, and ranking data determine the information hierarchy and data layouts?
- **OQ-7** What merchandising and beer garden workflows need interfaces once their scope is defined?
- **OQ-8** Which languages, writing directions, and name-display conventions must the interface support?
- **OQ-9** What update frequency, unavailable-data behavior, and feedback rules apply to scores, rankings, statistics, and match plans?
