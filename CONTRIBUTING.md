# Contributing to Pinakes

Keep SPEC.md normative and implementation-independent. Include schema changes,
examples, fixtures, and a changelog entry when a proposal affects conformance.
Use RFC 2119 keywords only for requirements; separate rationale from requirements.

Follow the [versioning policy](SPEC.md#23-versioning) and discuss substantive
changes before updating the specification. Record the dated revision,
accepted-input changes, producer/consumer compatibility, and supporting-consumer
requirements in the [changelog](CHANGELOG.md). Preserve existing valid inputs
where possible.

For a behavioral proposal, describe its effect on existing consumers and producers,
update both normative prose and affected schemas, and add positive and negative
fixtures. Run python tests/validate.py with tests/requirements.txt installed.
See [the implementation guide](IMPLEMENTING.md) for the runtime checks that schema
validation cannot provide.

AIexandria defaults, MCP tools, search ranking, and user setup belong in its own
repository unless they introduce a requirement shared by Pinakes consumers.
