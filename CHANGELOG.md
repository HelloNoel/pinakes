# Changelog

All notable changes to the pinakes specification are documented here.
The spec follows [Semantic Versioning](https://semver.org/) at the spec
level: the major version (the value of the `version:` field in a pinakes
file) is bumped on backwards-incompatible changes; minor revisions add
optional fields without breaking existing files.

## [Unreleased]

## [1.0-draft] — 2026-06-04

Initial draft. Defines:

- Top-level shape (`version`, `name`, `description`, `command_policy`, `entries`)
- Four entry kinds: `doc`, `index`, `merge`, `command`
- Cross-repo `repo:` overrides with `branch` / `tag` / `commit` and submodule support
- Registry format mapping names to root indexes
- Intersect-only command policy chain with `{query}` argv substitution
- Auth resolution order (`token_env` → host map → SSH agent)
- Conformance requirements

This version is **draft** until at least one independent implementation
exists alongside the reference implementation. Breaking changes may still
land before `1.0` is finalized.
