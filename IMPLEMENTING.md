# Implementing Pinakes v1

Read [SPEC.md](SPEC.md) for normative requirements. The schemas validate document
shape; consumers must also implement Git resolution, safe paths, composition,
command execution, and credential handling. User setup instructions for the
reference implementation live in [AIexandria](https://github.com/HelloNoel/aiexandria).

## Suggested implementation order

1. Parse YAML without silently discarding duplicate mapping keys. Reject unknown
   fields, unknown versions/kinds, explicit nulls, invalid IDs, and conflicting refs.
2. Resolve a registry root to a repository revision. Keep repository identity,
   revision, submodule options, and authentication context explicit.
3. Resolve doc/index/merge/command entries. Paths are repository-root relative;
   validate both lexical traversal and resolved symlinks. Detect cycles across
   both lazy index navigation and merges. Check IDs after merge prefixes apply.
4. Carry inherited repository selection, refresh settings, and command policies
   across every route. Pinned commits are immutable. Do not treat cached routes
   as permanent authorization decisions.
5. Expand the query argument template and execute argv directly. Intersect every
   inherited allow restriction; apply the deepest supplied timeout. Check accepted
   exit codes and manage output pipes and descendant processes through timeout.
6. Resolve credentials, including submodules, under the documented host rules.
   Missing explicitly configured credentials are errors. Do not resolve auth for
   file URLs. Resolve relative submodule remotes against their parent first.

## Conformance checklist

| Area | Minimum verification |
| --- | --- |
| Parsing | Both schemas, duplicate keys, nulls, unknown fields/kinds/versions |
| References | Branch/tag/commit selection, abbreviated SHA-1 pins, immutable pins |
| Paths | Absolute/traversal rejection, symlink containment, repository-root semantics |
| Composition | Merge prefixes, duplicate IDs, cycles spanning index and merge edges |
| Policy | All ancestor restrictions retained; expanded argv matching; accepted exit codes |
| Processes | Deadline covers execution and output collection; descendants cannot hang calls |
| Credentials | Explicit missing token fails; local URLs skip auth; submodules use resolved hosts |
| Caching | Correct repository/ref/options identity; failed acquisition does not publish a partial clone |

Run the shared schema cases and examples:

~~~sh
python -m pip install -r tests/requirements.txt
python tests/validate.py
~~~

The fixtures in tests/validation.json cover schema-level cases, not complete
runtime conformance. Add runtime tests for the behaviors above. Passing a JSON
Schema validator alone is not a conformance claim.

## Discovery and implementation-specific features

Pinakes v1 provides names, descriptions, hierarchical indexes, and command query
guidance. A consumer can use these for global metadata discovery without new
fields or a shared content-query language. Command entries retain their own
semantics. Search syntax translation, ranking, source IDs, pagination, response
budgets, refresh deadlines, and MCP APIs are consumer choices.

Unknown fields and kinds are rejected in v1, so adding even an optional field or
kind requires a deliberate format-version change. New behavior based on existing
metadata can remain an implementation feature. SHA-256 commit pins also need
future spec/schema evolution; v1 commit syntax describes SHA-1.
