# JavaScript ES2026 Secure Coding Prompt

Apply to all ES2026 code, including adapters, generated code, and framework boundaries. Validate at every receiving browser, server, worker, extension, package, storage, and message boundary, including DOM attributes, URLs, and third-party data. Check deployed engines' host APIs; apply browser and DOM rules only in their host.

## Validation

- Validate runtime input regardless of JSDoc, editor hints, or TypeScript types. For security-sensitive commands, configuration, and protocol messages, use allowlisted schemas that reject unknown fields.
- Check primitive type, size, and encoding before normalization, then normalized syntax, range, and length.
- Keep raw input separate; pass only validated values downstream.
- Authorize every protected web operation and object server-side; browser checks and client roles grant nothing.

## Dynamic code

- Never give untrusted strings to `eval`, `Function`, string timers, or dynamic compilers. Dispatch selected operations through trusted function tables.
- Map untrusted `import()` specifiers through an exact allowlist.
- Keep code out of JSON, database fields, feature flags, templates, and editable config. Never deserialize functions or revive callbacks, classes, or proxy handlers.

## Objects

- Use `Object.create(null)` or `Map` for attacker keys. Reject `__proto__`, `prototype`, and `constructor` before recursive merges/assignments; test helpers for prototype pollution.
- Use `Object.hasOwn` for own-property checks controlling authorization or flow.
- Recursively protect shared security data or keep independent private copies: `Object.freeze()` and shallow copies leave nested objects mutable.

## DOM and HTML

- Put untrusted text in ordinary elements with `textContent` or equivalent, never in `script`/`style`.
- Encode for the actual HTML, attribute, URL, CSS, or JavaScript context; no escaper covers all.
- Sanitize before `innerHTML`, `outerHTML`, `insertAdjacentHTML`, `document.write`, `iframe.srcdoc`, `setHTMLUnsafe`, or `Range.createContextualFragment()`, even on detached elements. Live-document nodes can load resources/run handlers before insertion or after removal; fragment scripts run on insertion.
- Inspect markup/extract text in inert `new DOMParser().parseFromString(html, 'text/html')` or `document.implementation.createHTMLDocument('')` documents, never detached-element `innerHTML`. Sanitize before importing/adopting/moving nodes into the page.
- Enforce `Content-Security-Policy: require-trusted-types-for 'script'; trusted-types <policy-names>` where supported. Confine `createPolicy` to a small reviewed module; never expose a pass-through default policy. Trusted Types labels do not sanitize.
- Sanitize rich HTML with a maintained context-aware sanitizer such as `DOMPurify.sanitize`. Pass strings, not nodes with possibly queued handlers; use output only in its matching context. Never concatenate markup, change namespaces, or compile templates afterward.
- Allowlist dynamic element/attribute names per element/namespace; validate values separately. `setAttribute()` and allowed `href`/`src`/`style` names cannot secure values. DOMPurify neither validates CSS nor authorizes resource URLs.
- Keep security DOM references/configuration in module bindings, never `window`, `document`, or form properties supplied by untrusted `id`/`name` attributes.
- Trust only reviewed DOMPurify config/hooks. Select required `USE_PROFILES`; review `ADD_TAGS`, `ADD_ATTR`, `ADD_URI_SAFE_ATTR`, `CUSTOM_ELEMENT_HANDLING`, and `forceKeepAttr` bypasses. Forbid `IN_PLACE: true` and same-instance `sanitize()` in hooks/config callbacks, which can replace active config.
- If `DOMPurify.isSupported` is false in a browser or server DOM, reject rich HTML or render text; unchanged output is unsafe. Keep sanitizer and server DOM (e.g. jsdom) security-current; fail builds on either's open advisories.

## URLs and SSRF

- Parse with `URL` against a trusted base; validate protocol, host, port, and credentials. Allow remote `https:` only except narrowly documented protocols.
- Compare normalized origins/exact hosts, never substrings/prefixes/suffixes.
- Revalidate redirects; resolve relative targets against approved same-origin bases only.
- Prevent SSRF: check approved hostnames and actual connection IPv4/IPv6 addresses, including redirects. Block private/special-use ranges except authorized internal services; prevent a second DNS lookup bypassing checks.
- For server `fetch()` to caller-influenced URLs, set `redirect: 'manual'` or `'error'`: default `'follow'` allows 20 unchecked hops. Resolve `Location` against the current URL; recheck destinations/connection addresses, cap hops, and forward only destination-authorized headers/credentials.

## Structured data and queries

- Validate all `JSON.parse` output as untyped input. Bound bytes before parsing and depth, collections, and strings; use a bounded parser when limits must precede allocation. `JSON.parse()` has no structural limits.
- Reject duplicate/unexpected security fields; use a duplicate-reporting parser when components could disagree. `JSON.parse()` keeps the last value; revivers/byte limits cannot recover duplicates.
- Avoid untrusted JSON revivers unless every key/value is constrained. Never copy attacker properties onto prototypes to rebuild classes/privileged objects.
- Bind SQL values using driver placeholders or documented binding tagged templates. Never interpolate untrusted values through untagged templates, `+`, `concat()`, or `join()`, including raw/unsafe APIs.
- Server-allowlist SQL tables, columns, sort directions, and other structure; binding protects values, not identifiers/keywords.
- Construct ORM/document-database filters, sorts, projections, and updates from allowlisted fields/validated scalars, never request bodies. Reject objects/arrays where scalars belong and client `$`-prefixed keys, which act as query operators.

## Text and numbers

- Avoid ambiguous nested regex quantifiers/overlapping alternatives on untrusted text; bound its length before matching. Prefer linear-time parsers for complex grammars; test critical patterns with long inputs and adversarial near-matches.
- Never rely solely on client regex for authorization/integrity.
- Escape literal user text in trusted patterns with ES2025 `RegExp.escape()` or a reviewed specification-compatible polyfill, never replacements with different leading-character semantics.
- Use `Number.isSafeInteger` and bounds for money, indexes, allocations, quotas, and authorization; use `BigInt`/reviewed decimals beyond that range. Reject `NaN`, `Infinity`, implicit coercion, and partial parses.
- Generate tokens/opaque IDs with cryptographic randomness, never `Math.random`.
- Parse explicit date formats; compare normalized instants, never locale strings.

## Asynchrony and logs

- Await/return security promises, including validation, authorization, logging, cleanup. Handle task-boundary rejections; fail closed on prerequisite rejection/timeout.
- Pass deadlines/`AbortController` signals to cancellable calls, streams, and operations. Aborting cannot stop arbitrary promises/synchronous work or prove remote effects never occurred.
- Prevent stale responses from overwriting newer authorization, identity, or validated state; release locks, temporary secrets, and resources in `finally`.
- Give `console`/loggers untrusted values as arguments/structured fields, never format strings/templates. For log neutralization, escape CR, LF, and other controls in line-oriented values against forged entries/terminal output.

## Secrets and crypto

- Exclude secrets from source, client bundles, URLs, exceptions, analytics, and serialized state.
- Use Web Crypto/maintained platform crypto, never homemade primitives.
- Use authenticated encryption with unique nonces, and timing-safe comparisons for tags/secret-derived values where timing is observable.
- For password storage, use slow hashes with unique random salts of at least 16 bytes: Argon2id at least `m=19456` KiB, `t=2`, `p=1`; scrypt at least `N=2**17`, `r=8`, `p=1`; or bcrypt cost at least 10, rejecting over 72 UTF-8 bytes. With Web Crypto alone, use `crypto.subtle.deriveBits()` with `name: 'PBKDF2'`, `hash: 'SHA-256'`, and at least 600,000 `iterations`.
- Never lower costs for library/runtime ceilings: raise ceilings or use supporting maintained implementations/services.
- Forbid fast password hashes (`crypto.subtle.digest()`), missing/shared salts, and reversible encryption. A transmitted browser hash becomes the password. Store verifier algorithms/parameters; rehash at successful login when costs rise.
- For token verification, verify JWT/JWS signatures before trusting claims; allowlist algorithms, expected issuer/audience, and require expiry, e.g. `jose` `jwtVerify(token, key, { algorithms: ['ES256'], issuer, audience, requiredClaims: ['exp'] })`. Never authenticate/authorize/select tenants with `jsonwebtoken` `jwt.decode()` or `jose` `decodeJwt()`, which verify nothing.
- Resolve keys only from trusted issuer config. Never let `alg`, `jku`, `x5u`, `jwk`, or `kid` fetch/select keys or algorithms outside it. Distrust lookup `kid`; set small explicit clock tolerance.
- Base64/hex/text decoding provides no validation, encryption, or integrity.

## Storage and messages

- Keep session secrets/bearer credentials out of browser storage when `HttpOnly`, `Secure` cookies can hold them.
- Protect cookie-authenticated changes with server-validated CSRF tokens or strict origin checks. `HttpOnly`/`Secure` cannot stop CSRF; `SameSite` alone misses request contexts.
- For cross-window `postMessage`, exact-match `event.origin`, verify expected-window `event.source`, and validate schemas before dispatch. Send sensitive data only to exact target origins, never `*`.
- Exclude privileged data from caches/stores shared across users, origins, or trust levels. Structured cloning removes neither malicious values nor oversized payloads.

## Dependencies and builds

- Add/upgrade through package managers, e.g. `npm install <pkg>@<major>`; review locks.
- Check `npm view <pkg> versions` before writing versions. If unverifiable, report and use build-failing `<verify-version>` in `package.json`, never guesses. A `0.x` caret allows only that minor's patches; update minors explicitly.
- Never lower/remove/loosen ranges, `overrides`, `resolutions`, or locks to permit installation; report conflicts.
- Run `npm audit`, `pnpm audit`, or `yarn npm audit` after dependency changes, before enabling existing-package features, and in CI from generated projects' first commit; fail on high/critical findings. Apply advisory/project fixes before scanners catch up; remove workarounds once fixed releases deploy.
- After security upgrades, find transitives with `npm ls <pkg>`; raise with `npm update <pkg>`/`overrides`. Remove overrides when parent ranges admit fixes.
- Keep Dependabot/Renovate proposing manifest/lock updates. Preserve release-age windows; admit security fixes only by reviewed one-off install-command overrides, never `min-release-age-exclude` or shorter project-wide windows.
- Commit reviewed locks; use expected HTTPS registries with `npm ci`, `pnpm install --frozen-lockfile`, or `yarn install --immutable`. Fail on manifest/lock mismatches instead of rewriting.
- Review dependencies before running lifecycle scripts, including native-binary packages. On npm 11.18+, which closed `allowScripts` gaps, record root `package.json` `allowScripts` approvals with `npm install-scripts approve <pkg>`, keep the default `allow-scripts-pin=true`, and set `strict-allow-scripts=true`. Otherwise npm 11 runs unreviewed scripts with notice; npm 12 blocks them. Use `--ignore-scripts` if no builds are needed, never `--dangerously-allow-all-scripts` to silence warnings.
- Keep `allow-git=none`, `allow-remote=none` (npm 12 defaults; npm 11: `all`) except reviewed needs. With `min-release-age`, restrict `min-release-age-exclude` to owned public-registry scopes: exclusions skip the window and may resolve newest versions immediately.
- Exclude development diagnostics, secrets, fixtures, private modules from production bundles; protect source maps with private source/metadata in access-controlled debugging systems.
- Enforce CSP and Subresource Integrity for necessary external browser scripts. Review transitives, bundles, and generated assets before production promotion.
