# Node.js 26 Secure Coding Prompt

Apply the JavaScript ES2026 baseline first. These rules target the Node.js 26 runtime, which is the Current release until it enters long-term support in October 2026 and which ships a broader permission model, a deprecated asynchronous loader API, and several runtime-deprecated crypto paths.

## Release line and upgrade posture

- Run the newest Node.js 26 release, including new minors, and redeploy when the Node.js project ships a 26.x security release; this Current line moves faster than an LTS line. Prefer a base image tag that follows the line, such as `node:26-slim` rebuilt with `docker build --pull`, or a digest an update bot keeps current, and when a Dockerfile or CI matrix needs an exact version you can't check on nodejs.org, leave a placeholder that fails the build rather than a version you remember.
- Check the runtime against Node.js security releases with `is-my-node-vulnerable`, installed as a locked dev dependency rather than fetched by a bare `npx` call, because `npm audit` covers packages, not Node.js itself.
- Treat Node.js 26 as Current until it becomes LTS in October 2026, and keep an LTS line available as a fallback for workloads that cannot absorb a semver-major change.
- Re-test on each 26.x minor before rollout, since a Current line still lands semver-minor runtime behavior that can change parsing, TLS, or module resolution.
- Test and ship the same image, or point every image and CI runner at one digest an update bot keeps current, so build and production run the same 26.x release; a line-following tag resolves to whatever is newest when each build pulls it. Verify the deployed `process.version`, because npm treats `engines` as advisory by default.
- Remove code that depends on interfaces deleted in 26.0.0, including `http.ServerResponse.prototype.writeHeader()` and the legacy `_stream_*` internal modules.

## Permission model

- Start production processes with `--permission` and grant only the capabilities the service needs; entry points have implicit read access, and the model does not sandbox malicious code.
- Omit `--allow-net` unless network access is required, and combine any network grant with an egress proxy or firewall because a granted process can still reach any reachable host.
- Pass one path per `--allow-fs-read` and `--allow-fs-write` flag, and never grant `*` on a process that handles untrusted input.
- Run `--permission-audit` only to discover the grants a workload needs; it reports violations through a diagnostics channel and lets execution continue, so it is not an enforcement mode.
- Call `process.permission.drop(scope[, reference])` after startup to shed unneeded capabilities irreversibly; only future checks are affected, so close or terminate already-open files, sockets, children, and workers separately.
- Check `process.permission.has()` before an optional privileged operation and still handle `ERR_ACCESS_DENIED` from that operation; the check does not reserve permission against a later drop.
- Understand the documented gaps: existing file descriptors bypass the model, symbolic links can resolve outside granted paths, and worker `execArgv` or `env` overrides can change its permission configuration.
- Add `--allow-inspector` deliberately or not at all, and isolate processes at the operating-system level because `process._debugProcess()` can force a debugger onto another process.
- Grant `--allow-openssl-store` only for a specific reviewed loader, since a STORE loader gets file and network authority that the other permission flags do not constrain.
- Audit each child's effective `execArgv` and `NODE_OPTIONS`: Node.js children can inherit startup permission flags, but runtime drops are not propagated and non-Node executables are not constrained by those flags.

## Startup configuration and environment

- Keep `--env-file` and `--env-file-if-exists` targets on deployment-controlled paths the application user cannot write, because those files are read before the permission model initializes and can carry `NODE_OPTIONS`.
- Validate required environment variables at startup for presence, type, length, and allowed values, and exit non-zero rather than starting in a degraded configuration.
- Never place secrets in command-line arguments, since `process.argv` and process listings can expose them.
- Load `node.config.json` or `--experimental-config-file` only from a trusted path, because a configuration file can set runtime flags that weaken the process.
- Freeze validated security configuration at startup so a later mutation of `process.env` cannot change an authorization, TLS, or limit decision.
- Do not silence security-relevant warnings with `--disable-warning` or `--no-warnings` in production; route deprecation and experimental warnings into monitoring instead.

## Child processes, addons, and FFI

- Spawn with `execFile` or `spawn` using an argument array and `shell` left false, and keep untrusted values out of the executable path, arguments, `cwd`, and `env`.
- Give each child an absolute executable path and a minimal explicit environment instead of inheriting the parent's environment and `PATH`.
- Constrain children with `timeout` and `killSignal`, set `maxBuffer` for `execFile` and cap `spawn` output while reading it, and drop privileges through `uid` and `gid` where supported; verify exit and enforce a final termination deadline because a signal may be ignored.
- Keep `--experimental-ffi` and `node:ffi` out of services that handle untrusted input, because an FFI call escapes both memory safety and the permission model's file and network checks.
- Grant `--allow-ffi` or `--allow-addons` only when required under `--permission`, and start with `--no-addons` when addons are unnecessary; `--force-context-aware` only rejects addons that are not context-aware.

## Filesystem and paths

- Resolve untrusted path fragments with `path.resolve` against a fixed root and reject any result that escapes that root.
- Use `O_NOFOLLOW` where supported for final-component symlinks, validate `fs.realpath` output against the fixed root, and keep parent directories unwritable by attackers; a separate path check does not prevent symlink races.
- Create files with a restrictive explicit mode and the `wx` flag or `O_WRONLY | O_CREAT | O_EXCL` instead of a separate existence check followed by an open.
- Use `fs.mkdtemp` for scratch space rather than predictable names in a shared temporary directory.
- Bound size, entry count, and nesting depth before reading, extracting, or serving uploaded files and archives.
- Map client-supplied names through an allowlist before using them as a stored filename, extension, or `Content-Disposition` value.

## HTTP server hardening

- Never enable `insecureHTTPParser` or `--insecure-http-parser`, and keep `httpValidation: 'strict'`; lenient parsing accepts mixed `Transfer-Encoding` and `Content-Length` framing, invalid header values, and bare `\n` separators, enabling request smuggling.
- Reduce `requestTimeout` to a positive value below its 300000 ms default and keep `headersTimeout` non-zero so a slow sender cannot occupy a connection.
- Give `server.timeout`, which defaults to 0, and `server.maxRequestsPerSocket`, which defaults to no limit, positive finite values on any internet-facing listener; explicitly destroy timed-out sockets when handling `'timeout'` events.
- Keep `maxHeadersCount` bounded, remembering that 0 disables the 2000-header limit instead of tightening it.
- Match `--max-http-header-size` and `maxHeadersCount` to the upstream proxy's header size and header-count limits, so the proxy rejects any request Node.js would truncate or refuse.
- Accept `X-Forwarded-For` and `Forwarded` only from enumerated proxy addresses, and rebuild client identity from the trusted hop.
- Reject control characters and newlines in any value copied into a response header, redirect location, or cookie.
- Send `Access-Control-*` headers only from handlers meant for cross-origin callers; use `*` only for public, uncredentialed responses, otherwise echo `Origin` only after an exact allowlist match, add `Vary: Origin`, and never reflect arbitrary or `null` origins with `Access-Control-Allow-Credentials: true`.
- For HTTP/2 listeners, bound `settings.maxConcurrentStreams`, `maxHeaderListPairs`, `maxSessionMemory`, and both `streamResetBurst` and `streamResetRate`; existing streams can exceed the memory admission limit. Enforce deadlines that close expired streams and destroy expired sessions.
- When one TLS server gives hostnames different client-certificate trust through `addContext()` or an `SNICallback`, make the default context at least as strict as any named one, check on each request that the `Host` header or HTTP/2 `:authority` matches `req.socket.servername` ignoring case, and authorize the peer certificate against that host's own policy. Don't trust the handshake to have picked the right context: hostname matching flaws have sent connections to the default context and its trust roots.

## Outbound requests, fetch, and TLS

- Parse an outbound destination with `URL` and check protocol, host, port, and credentials before issuing the request, then re-check the address after every redirect.
- Set `redirect: 'error'` or handle redirects manually for `fetch` calls to user-supplied URLs so a redirect cannot walk into an internal network.
- Attach an `AbortSignal` deadline to every `fetch` and `http.request`, and set socket and idle timeouts so a stalled upstream cannot pin a handler.
- Configure `http.Agent` with `maxSockets` and `maxTotalSockets`; for a fetch dispatcher, use the installed Undici version's `connections` and `connectTimeout` options, and bound total concurrent and queued requests.
- Give each client certificate and each server-identity policy, such as a custom `servername`, `ca`, or `checkServerIdentity`, its own `https.Agent` rather than letting one agent, the default global agent included, share its connection pool and TLS session cache across them, and pass a saved TLS `session` to `tls.connect()`, `https.request()`, or `http2.connect()` only for the host and `servername` it came from. A resumed session isn't checked against a certificate again, and flaws in Node's reuse checks have let one identity's connection or session serve another.
- Never set `rejectUnauthorized: false` or `NODE_TLS_REJECT_UNAUTHORIZED=0`, in application code, build scripts, or health checks.
- Keep the default TLS minimum version and OpenSSL security level, and do not append `@SECLEVEL=0` to a cipher string to make a legacy peer work.
- Replace `checkServerIdentity` only for a documented private PKI, and return an `Error` from the replacement whenever the identity does not match.

## Streams, buffers, and limits

- Allocate with `Buffer.alloc` and never hand out memory from `Buffer.allocUnsafe` or `allocUnsafeSlow` before overwriting every byte.
- Route bodies and file content through `stream.pipeline` with an explicit byte cap instead of accumulating them in one buffer.
- Limit decompressed output independently of compressed input in `zlib` and web streams, and abort when the expansion ratio exceeds what you allow.
- Respect write backpressure and `drain` so a slow consumer cannot build an unbounded in-memory queue.
- Clean up streams, temporary files, and database handles from a `finally` path, including when the client aborts mid-request.
- Set `--max-old-space-size` and a container memory limit so a memory spike terminates the process instead of degrading the host.

## Cryptography and secrets

- Generate keys, tokens, and salts with `crypto.randomBytes`, `crypto.randomInt`, or `crypto.webcrypto.getRandomValues`.
- Compare secrets with `crypto.timingSafeEqual` on equal-length buffers, hashing both sides first when lengths can differ.
- Pass `authTagLength: 16` for AES-GCM; Node.js 26 already rejects shorter tags without an explicit `authTagLength`, so never lower it based on untrusted input.
- For authenticated decryption, do not release or act on `decipher.update()` output until `decipher.final()` succeeds, or on decipher stream output until successful completion; discard all output on failure.
- Use Web Crypto for non-extractable `CryptoKey` values; convert an extractable key with `KeyObject.from()` only when native crypto interoperability is required, because conversion discards Web Crypto usage and algorithm restrictions and direct `CryptoKey` arguments are runtime-deprecated in 26.
- Derive password verifiers with `crypto.scrypt` or `crypto.pbkdf2` at reviewed parameters instead of a plain digest.
- Enable `--secure-heap=n` with a sufficiently large power-of-two size for selected OpenSSL allocations; it is unavailable on Windows and does not protect JavaScript memory, so still hold secrets in overwritable buffers rather than long-lived strings.

## Modules, loaders, and type stripping

- Replace `module.register()` with `module.registerHooks()`, since the asynchronous loader entry point is runtime-deprecated as DEP0205 in Node.js 26.
- Treat a customization hook as privileged code: register hooks only from modules you own and review any dependency that installs one.
- Restrict `NODE_OPTIONS`, `--require`, and `--import` preloads to deployment-controlled values, because a preload executes before your first line of code.
- Install production dependencies with `npm ci` against a committed lockfile, and use `--ignore-scripts` for trees you have not reviewed.
- Declare `exports` in `package.json` to restrict package-name subpath imports, but enforce privileges separately because absolute-path imports can still load internal modules.
- Keep TypeScript sources to erasable syntax because `--experimental-transform-types` was removed in 26.0.0, and never treat a stripped type annotation as runtime validation.

## Time, URLs, and legacy APIs

- Parse and compare instants with `Temporal`, which is enabled by default in Node.js 26, instead of relying on `Date` string coercion for expiry or replay checks.
- Use the `URL` constructor rather than `url.parse()`; DEP0169 is an application deprecation, and DEP0170's acceptance of nonnumeric ports was removed in Node.js 25.
- Replace `buffer.slice()` with `subarray()` for an intentional shared view, or use `Buffer.from(buffer.subarray(start, end))` for an independent copy.
- Migrate off `Buffer()` and `new Buffer()` entirely in application code in favor of `Buffer.alloc` and `Buffer.from`.
- Run `--throw-deprecation` in test environments so a runtime deprecation in a security-relevant path fails the build rather than a log line.

## Local data with node:sqlite

- Treat `node:sqlite` as a release candidate on this line and re-test after each minor upgrade, since its API is still moving.
- Bind values with `?`, `:name`, `$name`, or `@name` parameters using a prepared statement's `run`, `get`, `all`, or `iterate` method, and never interpolate request data into SQL text.
- With a `database.createTagStore()` tag store, finish each `iterate()` iterator or stop it with `return()` before running the same query text through that store again, and don't share a store with code you don't trust. The store reuses one prepared statement per query text, and a stale iterator has re-run another caller's write.
- Leave `allowExtension` at its default of false, because `enableLoadExtension(true)` cannot enable extension loading when the database was constructed with that setting.
- Disable bare named parameters with `setAllowBareNamedParameters(false)` when the binding object is built from request data.
- Open database files from a fixed application directory within the required filesystem grants, and enforce OS permissions because SQL-level file operations such as `ATTACH DATABASE` are not constrained by `--allow-fs-write`.

## Isolation and dynamic execution

- Do not treat `node:vm` as a sandbox; `--disallow-code-generation-from-strings` does not even cover the `vm` module.
- Execute untrusted code in a separate operating-system process with its own user, filesystem view, and memory and CPU limits.
- Validate `workerData` and worker messages against a strict schema, and terminate a worker that exceeds its time budget.
- Set `resourceLimits` on every `Worker`, accounting for `--max-old-space-size` overriding `maxOldGenerationSizeMb`; these limits exclude external memory such as `ArrayBuffer`s and do not prevent a process-wide out-of-memory abort.
- Never derive a worker entry point, child executable, or dynamic import specifier from request data.
- Apply `--frozen-intrinsics` only after confirming your preloads run first, since it freezes the root context and can break libraries that patch built-ins.

## Diagnostics, inspector, and logging

- Keep `--inspect` and `--experimental-network-inspection` out of production, and bind the inspector to loopback when debugging because the port grants code execution.
- Treat diagnostic reports, heap snapshots, and core dumps as secrets, since they capture environment variables and in-memory credentials.
- Handle `unhandledRejection` and `uncaughtException` by writing a sanitized record and exiting instead of continuing to serve requests.
- Redact `authorization`, `cookie`, `set-cookie`, token-bearing query parameters, and proxy URL credentials, including any that show up in proxy connection errors, before request data or errors reach logs or traces.
- Return generic error bodies to clients and keep stack traces, module paths, and runtime version details in access-controlled telemetry.

## Deployment and operations

- Run as a dedicated non-root user with a read-only root filesystem and a writable mount only where the workload requires one.
- Terminate TLS at a maintained reverse proxy and keep its header, body, and timeout limits aligned with the Node.js server configuration.
- Ship immutable images built with `npm ci --omit=dev`, and rebuild to take a runtime patch instead of mutating a running host.
- Handle `SIGTERM` by refusing new connections, draining in-flight work against a deadline, and closing database, file, and socket handles.
- Expose readiness and liveness endpoints that reveal no configuration, dependency inventory, or stack detail.
