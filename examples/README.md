# Examples

These files are illustrative, not normative. Each one exercises a specific
slice of the spec.

| File | Demonstrates |
| --- | --- |
| [`minimal.pinakes.yaml`](./minimal.pinakes.yaml) | Smallest valid index — header + one `doc` entry |
| [`hierarchical.pinakes.yaml`](./hierarchical.pinakes.yaml) | Nested `index` entry, sibling `doc` entries |
| [`cross-repo.pinakes.yaml`](./cross-repo.pinakes.yaml) | Per-entry `repo:` blocks reaching into upstream repos |
| [`merge.pinakes.yaml`](./merge.pinakes.yaml) | `merge` entries with `prefix:` for deduplication |
| [`command-search.pinakes.yaml`](./command-search.pinakes.yaml) | Sandboxed ripgrep `command` entry with `command_policy` |
| [`registry.yaml`](./registry.yaml) | Consumer-side registry config |

Validate any of them against the JSON Schema:

```sh
# pip install check-jsonschema
check-jsonschema --schemafile ../schema/pinakes.schema.json minimal.pinakes.yaml
```
