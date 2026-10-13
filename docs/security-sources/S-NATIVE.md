# React Native 0.87 Secure Coding Prompt

Apply the React 19, TypeScript 7, and JavaScript ES2026 prompts first. These rules cover React Native 0.87 client trust, networking, storage, deep links, WebViews, native modules, permissions, logging, and release builds.

## Client trust and application data

- Treat the JavaScript bundle, device state, component state, and all client decisions as attacker controllable; React Native 0.87's default Strict TypeScript API improves compile-time API accuracy but adds no runtime trust boundary.
- Enforce authentication, authorization, price, entitlement, workflow, and integrity rules on trusted servers.
- Keep API secrets, private keys, administrative endpoints, and privileged business logic out of bundles and assets.
- Validate every server response, deep-link value, native-module result, persisted value, and push-notification payload at runtime.
- Clear user-scoped state, queries, caches, and files on logout, account switching, tenant switching, and credential revocation.

## Networking and authentication

- Use HTTPS for all remote traffic and keep platform certificate and hostname verification enabled.
- Keep iOS ATS enabled and `cleartextTrafficPermitted="false"` in Android Network Security Configuration; remove broad ATS exceptions and exclude development CAs from release trust anchors.
- Apply certificate pinning only with a reviewed rotation, backup-pin, expiry, and recovery design.
- Use short-lived tokens with server-side revocation and store refresh credentials in platform-protected storage.
- Use the system browser for OAuth authorization-code flows with PKCE (`S256`); do not collect identity-provider credentials inside an embedded WebView.
- Keep credentials out of URLs, analytics, crash reports, network logs, clipboard data, and screenshots.
- Bound requests, responses, redirects, retries, downloads, uploads, streaming, and offline queues.
- Enforce destination and cookie policies in native networking when required; browser CORS and `fetch` options `redirect: 'manual'` and `credentials: 'omit'` are not reliable cross-platform controls.

## Local storage and platform protection

- Store credentials and cryptographic keys in iOS Keychain through a maintained library; on Android, protect encryption keys with Keystore and store credential ciphertext separately.
- Treat AsyncStorage and ordinary files as untrusted plaintext storage and keep secrets out of them.
- Apply iOS data-protection and Android backup and extraction policies appropriate to sensitive files.
- Encrypt sensitive application data with platform-protected keys and authenticated encryption when storage is required.
- Minimize cached personal data and implement retention, deletion, migration, and device-compromise behavior explicitly.

## Deep links and WebViews

- Prefer verified iOS Universal Links or Android App Links; custom URL schemes have no centralized ownership and another installed app can claim the callback.
- Never place tokens, authorization codes without PKCE, or sensitive state in custom-scheme links, and validate scheme, host, path, parameters, and current flow correlation before dispatch.
- Require current authentication and confirmation before a deep link triggers a privileged or irreversible operation.
- Avoid WebViews for untrusted content; when required, restrict navigation, origins, file access, mixed content, and new windows.
- Disable JavaScript and bridge messaging in WebViews unless the feature requires them; validate message schemas and exact sender origins where trustworthy platform metadata is available. Navigation allowlisting and top-level URLs do not authenticate senders; expose Android `addJavascriptInterface` bridges only to trusted frame content.
- Never inject untrusted strings into WebView JavaScript or expose a general native bridge to web content.
- Treat `Linking.openURL()` as an outbound native capability: parse and allowlist the exact scheme and destination before invoking it, and require user confirmation for `tel:`, `sms:`, `mailto:`, custom schemes, or other URLs handled by installed applications; `canOpenURL()` tests availability, not safety.

## Native modules and permissions

- Expose narrow typed native-module methods and validate arguments again in native code.
- Keep filesystem, shell, intent, URL, clipboard, camera, microphone, location, and biometric capabilities behind explicit policy.
- Request platform permissions only at the point of need and handle denial without weakening security.
- Validate Android intents and iOS extension or URL inputs before dispatch and do not export components unnecessarily.
- Review third-party native modules for exported components, permissions, deep links, storage, network, and binary provenance.

## Logging and release builds

- Redact credentials, personal data, request bodies, server responses, and local paths from JavaScript and native logs.
- Disable development menus, remote debugging, packager access, debug certificates, and test endpoints in release builds.
- Sign release artifacts with protected keys and verify store, over-the-air update, and bundle integrity policies.
- Use the stable React Native 0.87 root API and documented setup entry points such as `react-native/setup-env`; deep imports into `react-native/Libraries/*` are type errors under the default Strict API, so do not restore them with path aliases or the `react-native-legacy-deep-imports` custom condition to bypass upgrade review.
- Test rooted or jailbroken environments, proxy interception, deep-link spoofing, WebView compromise, native bridge abuse, and backup extraction.
