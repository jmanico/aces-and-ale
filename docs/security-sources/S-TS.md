# TypeScript 7 Secure Coding Prompt

Apply the JavaScript ES2026 baseline first. These rules cover TypeScript 7.0.x. The native compiler adopts 6.0's changed defaults, rejects removed options, and has no compiler API; review effective configuration when migrating from 5.x or 6.x.

## Compiler checks

- Keep `strict` (7.0 default `true`) and every strict-family check on in production; an older config still setting `false` opts out.
- Before release, require a full-project type check with `noCheck: false` and `checkJs` for included JavaScript. An emit stage may use `noCheck`, but emitted files don't prove checking passed: the compiler emits despite type errors.
- Enable `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `useUnknownInCatchVariables` (narrow caught values before reading properties or exposing details), `noImplicitOverride`, `noFallthroughCasesInSwitch`, and `noImplicitReturns`.

## Trust boundaries

- Type parsed JSON, request bodies, environment variables, storage values, and SDK responses as `unknown` at entry points; narrow them with runtime schemas or type guards checking every security-relevant property and rejecting unknown keys that could enable mass assignment, policy bypass, or version confusion.
- Never use type assertions, including doubles like `value as unknown as TrustedType`, to make untrusted data an authenticated identity, authorization decision, validated command, or other incompatible security type.
- Keep validated branded types distinct from raw strings for identifiers, URLs, paths, secrets, and tenant-scoped keys.
- Prohibit `any` at trust boundaries, containing unavoidable `any` in a small reviewed adapter; avoid non-null assertions on request, configuration, lookup, or async values.
- Never suppress errors with `@ts-ignore` or file-level `@ts-nocheck`; use a narrowly explained `@ts-expect-error` only for a tested, unavoidable incompatibility. Audit ambient declarations and module augmentation, which can claim guarantees the implementation lacks.

## Object models

- Use closed discriminated unions for commands, rejecting unsupported variants at runtime, and narrow literal unions for privilege levels and security states.
- `readonly`, `Readonly<T>`, and `as const` neither freeze objects nor stop alias mutation; apply the baseline's runtime protection to security configuration and validated data.
- Use JavaScript `#name` fields or closures for runtime privacy; `private` and `protected` are compile-time only.
- Avoid optional security-switch booleans when `undefined`, `false`, and inherited defaults differ. Separate public DTOs from persistence entities and privileged models.
- Constrain generic keys to exact allowed properties when selecting fields for update, serialization, or authorization, never `keyof any` maps for attacker-selected assignment; preserve tenant and owner types through generic repositories.
- Use `satisfies` for configuration shape, plus `as const` and a compatible readonly target when allowlists must keep literal types; `satisfies` alone doesn't prevent widening. Test mapped and conditional types against runtime behavior.

## Modules

- Keep `types` at its 7.0 default `[]` and list needed ambient packages. `types: ["*"]` includes every visible `@types` package; restricting `types` neither blocks imported declarations nor guarantees declared globals exist.
- Pair `module`/`moduleResolution` with the production runtime, enable `verbatimModuleSyntax`, and fail builds when imports resolve differently from the emitted package graph. 7.0 removes `moduleResolution: node`, `node10`, and `classic` and `amd`, `umd`, `system`, and `none` modules; re-test resolution after migrating.
- Set `target` and `lib` for the deployed runtime; declarations install no polyfills, and `paths` aliases don't rewrite emitted specifiers.
- Keep `noUncheckedSideEffectImports` at its 7.0 default `true`, and verify asset imports in the real build: ambient wildcard declarations can hide missing files.
- `esModuleInterop`, `allowSyntheticDefaultImports`, and `alwaysStrict` can't be `false` in 7.0; remove sloppy-mode and namespace-import assumptions.
- Write import attributes with `with`, e.g. `with { type: 'json' }`; `assert` is a 7.0 compile error. Keep them on JSON and other non-JavaScript imports so the host stops a swapped response running as script. `module: nodenext` rejects an ECMAScript-module JSON import without `type: 'json'`; bundler settings accept it.

## Builds

- Build security-sensitive entry points with the reviewed project configuration. `--ignoreConfig` skips `tsconfig.json` and its checks, keeping only defaults and explicit flags; use it only when those are reviewed.
- Run `tsc` on untrusted projects in an isolated filesystem with external CPU, memory, and time limits: configuration can redirect reads and writes, diagnostics can expose local files, and `--build --clean` can delete files named by configuration or `.tsbuildinfo`.
- Never publish declarations exposing secrets, privileged fields, or unsupported guarantees; keep test helpers, development entry points, and internal modules out of exports; inspect emitted JavaScript and source maps.
- Pin the TypeScript 7 compiler and type packages. Enable `erasableSyntaxOnly` for native type stripping (rejecting enums, runtime namespaces, and parameter properties), and keep a separate type-check gate: stripping doesn't check types and Node.js ignores `tsconfig.json`.
- Treat `@typescript/typescript6` as a reviewed build dependency where linters, codemods, template checkers, or plugins need the old compiler API, verifying which package and executable each tool loads, including npm aliases. It adds no 7.0 API or framework-tool compatibility.
- Re-check tools analyzing JavaScript with TypeScript: 7.0 drops closure-style JSDoc, special `@enum` handling, bare `?` types, and values standing in for types, so old rules and codemods can silently stop matching.
- Reproduce release diagnostics with consistent `--checkers` and `--singleThreaded`; tune `--builders` for resources, which shouldn't change results.
