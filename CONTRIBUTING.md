# Contributing to Pinakes

Keep SPEC.md normative and implementation-independent. Include schema changes,
examples, fixtures, and a changelog entry when a proposal affects conformance.
Use RFC 2119 keywords only for requirements; separate rationale from requirements.

Editorial clarifications can retain the format version when they do not change
accepted inputs or meaning. Version 1 rejects unknown fields and entry kinds:
adding an optional field or kind is therefore not compatible with existing v1
consumers and requires a new major format version. Open an issue to discuss such
changes before updating the specification.

For a behavioral proposal, describe its effect on existing consumers and producers,
update both normative prose and affected schemas, and add positive and negative
fixtures. Run python tests/validate.py with tests/requirements.txt installed.
See [the implementation guide](IMPLEMENTING.md) for the runtime checks that schema
validation cannot provide.

AIexandria defaults, MCP tools, search ranking, and user setup belong in its own
repository unless they introduce a requirement shared by Pinakes consumers.
