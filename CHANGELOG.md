# Changelog

All notable changes to the Pinakes specification are recorded here, including
revision compatibility and supporting-consumer requirements. See the
[versioning policy](SPEC.md#23-versioning).

## [Unreleased]

### 2026-11-02

- Change the default for omitted `repo.submodules` to `false` in indexes and
  registries. Submodule initialization and refresh now require explicit `true`.
- Compatibility: `version: 1` and accepted syntax are unchanged, but references
  omitting this field change meaning. Existing indexes that rely on nested
  documentation must add `submodules: true` before adopting this revision.
  Explicit boolean values retain their meaning.
- Producers supporting consumers on both sides of this revision should emit an
  explicit boolean. Otherwise, state the required draft revision; format version
  alone does not identify the default.
- AIexandria v0.4.0 is the first release implementing this revision. Releases
  through v0.3.0 use the previous default. This revision does not finalize v1.

### 2026-10-30

- Add SHA-256 commit IDs and unambiguous prefixes in both indexes and
  registries. Retain existing SHA-1 semantics; validate pin length against the
  actual Git object format, not just the shared schema range.
- Require cached prefixes to retain their resolved commit. Permit missing-object
  acquisition at that fixed revision, including during a forced cache update.
- Clarify selective acquisition and bounded metadata prefetching without adding
  fields, entry kinds, or consumer-specific APIs.
- Align the versioning policy for revisions before and after finalization.
  Unknown fields, kinds, and versions remain errors.
- Compatibility: the format remains `version: 1` and existing SHA-1 documents
  remain valid. SHA-256 pins require a consumer implementing this revision.
  AIexandria v0.4.0 is the first release supporting this revision; releases
  through v0.3.0 do not support it.

### 2026-10-29 — Documentation and validation

- Add an implementation guide and conformance checklist.
- Clarify how unknown fields and kinds make additions incompatible with v1.
- Publish canonical schema URLs and run shared validation in GitHub Actions.

## [1.0-draft] — 2026-06-04

Initial draft. Defines:

- Top-level shape (`version`, `name`, `description`, `command_policy`,
  `entries`)
- Four entry kinds: `doc`, `index`, `merge`, `command`
- Cross-repo `repo:` overrides with `branch` / `tag` / `commit` and submodule
  support
- Registry format mapping names to root indexes
- Intersect-only command policy chain with `{query}` argv substitution
- Auth resolution order (`token_env` → host map → SSH agent)
- Conformance requirements
