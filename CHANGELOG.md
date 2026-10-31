# Changelog

All notable changes to the Pinakes specification are recorded here, including
revision compatibility and supporting-consumer requirements. See the
[versioning policy](SPEC.md#23-versioning).

## [Unreleased]

### 2026-10-30

- Add SHA-256 commit IDs and unambiguous prefixes in both indexes and registries.
  Retain existing SHA-1 semantics; validate pin length against the actual Git
  object format, not just the shared schema range.
- Require cached prefixes to retain their resolved commit. Permit missing-object
  acquisition at that fixed revision, including during a forced cache update.
- Clarify selective acquisition and bounded metadata prefetching without adding
  fields, entry kinds, or consumer-specific APIs.
- Align the versioning policy for revisions before and after finalization.
  Unknown fields, kinds, and versions remain errors.
- Compatibility: the format remains `version: 1` and existing SHA-1 documents
  remain valid. SHA-256 pins require a consumer implementing this revision.
  AIexandria development builds with this change support it; releases through
  v0.3.0 do not. Record the first supporting release number when published.

### 2026-10-29 — Documentation and validation

- Add an implementation guide and conformance checklist.
- Clarify how unknown fields and kinds make additions incompatible with v1.
- Publish canonical schema URLs and run shared validation in GitHub Actions.

## [1.0-draft] — 2026-06-04

Initial draft. Defines:

- Top-level shape (`version`, `name`, `description`, `command_policy`, `entries`)
- Four entry kinds: `doc`, `index`, `merge`, `command`
- Cross-repo `repo:` overrides with `branch` / `tag` / `commit` and submodule support
- Registry format mapping names to root indexes
- Intersect-only command policy chain with `{query}` argv substitution
- Auth resolution order (`token_env` → host map → SSH agent)
- Conformance requirements
