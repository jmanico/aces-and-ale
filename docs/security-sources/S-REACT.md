# React 19 Secure Coding Prompt

Apply the JavaScript ES2026 baseline first. These rules cover React 19.

## Rendering and HTML

- Render untrusted values as JSX text or inert string props such as `title`; string URL or HTML props still need validation or sanitization.
- Avoid `dangerouslySetInnerHTML`. For required rich HTML, sanitize once with a maintained allowlist sanitizer and pass it only as `{__html: sanitized}` at the reviewed sink; never concatenate after sanitizing or treat raw API responses as trusted markup.
- Keep untrusted values out of inline script/style text, event-handler strings, and raw SVG or MathML.
- Pass a per-response CSP nonce to server streaming via the `nonce` option; Trusted Types enforcement alone doesn't make `dangerouslySetInnerHTML` safe.
- Under `require-trusted-types-for 'script'`, check your minor: 19.3.0+ passes `TrustedHTML` and `TrustedScriptURL` to DOM attributes unconverted, while 19.0 through 19.2 stringify them. On those minors, test each attribute sink under enforcement; never fix violations with a pass-through default policy.

## URLs, props, and components

- Parse and allowlist URL schemes and origins before assigning user-derived navigation, image, iframe, or form targets.
- Never spread untrusted objects into DOM elements or privileged components, which can set unexpected attributes and handlers; map user-selected components and variants through an exact registry, not dynamic imports or property lookup.
- Keep secrets and authorization decisions out of client component props and public build-time variables; treat third-party escape hatches and HTML-rendering props as sinks.
- Keep `preinit` and `preinitModule` on server-controlled URLs: they fetch and execute scripts, and `preinit` with `as: 'style'` applies stylesheets, unlike `preload`, `preconnect`, and `prefetchDNS`, which only fetch or warm connections.

## Server Functions and Actions

- Every client-reachable `'use server'` function is a remotely callable endpoint whose arguments are fully client-controlled.
- Authenticate and reauthorize ownership, action, and tenant inside every Server Function, never trusting captured values, hidden inputs, bound arguments, or client state; validate form and serialized arguments, excluding role, owner, price, status, and server-generated fields.
- Configure the host framework's CSRF and origin checks for credentialed Server Function transports; React defines the contract, not an authorization boundary.
- Return only deliberate serializable data, without secrets, internal errors, or privileged object references.
- Keep secrets out of Server Function code and bundled helpers, reading keys and passwords at runtime from the environment or a secret store, so leaked Server Function source discloses none.

## State and browser trust

- Treat state, context, refs, local/session storage, URL state, and cached client data as attacker-controlled; client feature flags, hidden components, and route state aren't authorization.
- Prevent stale async responses overwriting newer identity, permission, or tenant state; clear user-specific caches and state on logout, account/tenant switch, and credential expiry.

## SSR, hydration, and caching

- Use request-scoped server state so module globals and shared caches can't leak data across users; include identity and tenant in every rendering and cache key for protected output.
- Never put raw request-derived text in `renderToPipeableStream`/`renderToReadableStream` `bootstrapScriptContent`; React's script-terminator escaping doesn't make it safe. Use a script-safe serializer escaping `<` in JSON state.
- Source `bootstrapScripts` and `bootstrapModules` only from a trusted build manifest: each string becomes an executable script URL, so request-, tenant-, or CMS-selected values can load attacker code even without `bootstrapScriptContent`.
- Keep credentials, secrets, internal fields, and other users' data out of hydration payloads and streamed markup.
- With multiple roots in one document, set a collision-resistant server `identifierPrefix` and pass the same prefix to `hydrateRoot`, never derived from attacker-controlled markup.
- Fix unexpected hydration mismatches instead of hiding them with `suppressHydrationWarning`; React doesn't guarantee mismatched attributes are repaired.

## Refs, errors, and dependencies

- Expose narrow `useImperativeHandle` handles, not DOM nodes or privileged internals; keep direct DOM writes behind a reviewed adapter that never feeds untrusted data to HTML-parsing sinks.
- Keep `onShellError`, `onError`, error-boundary output, and Server Function failures generic, logging opaque correlation data server-side, not stacks, raw responses, or secrets.
- Pin matching `react` and `react-dom` versions. Treat `react-server-dom-webpack`, `react-server-dom-turbopack`, and `react-server-dom-parcel` as internet-facing request decoders: with RSC enabled, servers accept Server Function requests even if you wrote none, so leave RSC off where unneeded. React has shipped every RSC security fix so far as a patch on each affected 19.x minor, so keep these packages on your minor's newest patch, moving minors when an advisory lists no fix for yours. Update framework-bundled copies via the framework's release; review renderer, build-tool, and component advisories together.
- Test dangerous markup, malicious props, Server Function authorization, cross-user SSR state, stale state, and dependency sinks.
