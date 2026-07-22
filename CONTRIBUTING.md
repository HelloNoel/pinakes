# Contributing to pinakes

Thanks for your interest. This spec evolves through PRs. There are three
kinds of contributions worth distinguishing:

## Editorial

Typos, prose clarifications, and structural cleanup that don't change
*what* the spec says. Open a PR; no issue needed.

## Schema additions (non-breaking)

A new optional field, a new optional entry kind, a clarification of
previously-implementation-defined behavior. These do not bump the major
version; they land on the current version and are documented in
`CHANGELOG.md`.

PR checklist:

- [ ] Edit `SPEC.md` with the new field/kind, including required/optional
      and a worked example.
- [ ] Update `schema/pinakes.schema.json` (or `registry.schema.json`) so
      validators flag missing/wrong types.
- [ ] Add an entry to `CHANGELOG.md` under `[Unreleased]`.
- [ ] Add at least one example in `examples/` exercising the new field.

## Breaking changes

Anything that would cause an existing valid `pinakes.yaml` to be rejected
or interpreted differently. These bump the major version. Please open an
issue first — major bumps are expensive for downstream consumers, so we
want explicit alignment before drafting the PR.

## Discussion

Substantive design questions belong in an issue, not a PR comment. The
goal is to keep the *rationale* discoverable from the issue tracker, not
buried in PR review threads.

## Style

- Use RFC 2119 keywords (MUST, SHOULD, MAY) only for normative
  statements. Rationale and examples should be in plain prose.
- Examples are YAML, indented two spaces, with comments explaining
  non-obvious fields.
- Field tables are markdown pipe tables; required/optional column is
  centered.
