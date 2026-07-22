# pinakes

A specification for **pinakes indexes** — a YAML format for describing how
an LLM should navigate a documentation corpus hosted in one or more git
repositories.

The goal is interoperability: a single index file should drive any
conforming server, library, or model harness without modification. A
docs author writes one `pinakes.yaml`; tooling from different vendors can
all consume it.

## Status

**Draft, version 1.** Backwards-incompatible changes require bumping the
top-level `version:` field. The spec is versioned independently of any
implementation.

## What's in this repo

| Path | Contents |
| ---- | -------- |
| [`SPEC.md`](./SPEC.md) | The normative specification |
| [`schema/pinakes.schema.json`](./schema/pinakes.schema.json) | JSON Schema for `pinakes.yaml` files |
| [`schema/registry.schema.json`](./schema/registry.schema.json) | JSON Schema for registry config files |
| [`examples/`](./examples/) | Annotated example index files |
| [`CHANGELOG.md`](./CHANGELOG.md) | Spec version history |

## Reference implementation

[AIexandria](https://codeberg.org/HelloNoel/AIexandria) is a Rust MCP server
that implements this spec. It is one implementation among (eventually)
many; nothing in this spec depends on it.

## Contributing

This spec evolves through PRs against `SPEC.md` plus a corresponding
schema update. Substantive changes need a CHANGELOG entry and rationale
in the PR description. See [`CONTRIBUTING.md`](./CONTRIBUTING.md).

## License

[Apache-2.0](./LICENSE).
