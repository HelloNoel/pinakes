# The pinakes specification

**Version:** 1 (draft)
**Status:** Draft. Subject to breaking change until version 1 is finalized.

This document defines the **pinakes** format: a YAML file (`pinakes.yaml`)
that describes a hierarchical, navigable view of a documentation corpus
hosted in one or more git repositories.

The intent is to let documentation authors publish a single, vendor-neutral
description of *which repositories an LLM is allowed to read*, *which documents
should be presented for navigation*, and *how it should drill into them*.
A repository referenced by a registry or entry is the read-access boundary;
`doc` entries curate navigation and are not a per-file allow-list. Any conforming
runtime (MCP server, library, agent harness, …) can act on that description
without coupling to a specific implementation.

The keywords MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY in this document
are to be interpreted as in [RFC 2119].

[RFC 2119]: https://datatracker.ietf.org/doc/html/rfc2119

---

## 1. Overview

A pinakes **index** is a YAML document containing a header, an optional
command policy, and an ordered list of **entries**. Each entry is one of
four kinds:

- `doc` — a leaf text file the consumer is allowed to read
- `index` — a child pinakes index (same repo or another)
- `merge` — inline another index's entries here
- `command` — a sandboxed shell command (RAG, ripgrep, custom retriever)

Indexes form a directed graph rooted at a single index file. Cycles MUST
be detected and rejected.

A **registry** maps names → root indexes; this is how a runtime knows
which indexes exist and where to fetch them from.

---

## 2. File format

### 2.1 Encoding

Indexes MUST be valid UTF-8 YAML 1.2. The conventional filename is
`pinakes.yaml`, but consumers MUST NOT rely on the filename — the path is
specified by whatever points at it (the registry, or a parent `index` /
`merge` entry).

### 2.2 Top-level shape

```yaml
version: 1                         # REQUIRED. Spec major version.
name: my-project                   # REQUIRED. Human-readable label.
description: "Internal docs"       # OPTIONAL. One-line summary for LLM consumption.

command_policy:                    # OPTIONAL. See §6.
  allow: '^rg .* docs/'
  timeout_secs: 10

entries:                           # REQUIRED. Ordered list. May be empty.
  - id: getting-started
    name: Getting started
    kind: doc
    path: docs/getting-started.md
```

A consumer that encounters an unknown top-level field MUST reject the
file. (This is intentionally strict: typos in author intent should fail
loudly rather than silently.)

### 2.3 Versioning

The top-level `version:` field is the spec major version. Version 1 of
the spec corresponds to `version: 1` in the file. Implementations MUST
reject any file whose `version:` they do not recognize.

Backwards-incompatible changes to the spec bump the major version.
Backwards-compatible additions (new optional fields, new entry kinds
behind a feature gate) keep the major version and are documented in
[`CHANGELOG.md`](./CHANGELOG.md).

---

## 3. Entries

Each entry is a YAML mapping with these common fields:

| Field | Type | Required | Notes |
| --- | --- | :---: | --- |
| `kind` | string | yes | One of `doc`, `index`, `merge`, `command`. |
| `id` | string | no | Stable identifier; auto-generated from `name` if omitted (see §3.1). |
| `name` | string | yes (except `merge`) | Human-readable label. |
| `description` | string | no | One-line summary the LLM uses to choose. |
| `repo` | object | no | Override the enclosing index's repo for this entry only (see §4). |

Kind-specific fields are defined in §3.2–3.5.

### 3.1 IDs and slugification

`id` MUST be unique among siblings within a single index level (after any
`merge` entries are flattened — see §3.4).

When `id` is omitted, consumers MUST derive it from `name` by:

1. Lowercasing each Unicode alphanumeric character.
2. Replacing every other character with `-`.
3. Trimming leading/trailing `-`.

Two entries that slugify to the same value at the same level constitute
a duplicate-id error.

### 3.2 `doc` entries

```yaml
- id: getting-started
  name: Getting started
  kind: doc
  description: "Install + first run"
  path: docs/getting-started.md
  repo: { ... }                    # OPTIONAL, see §4
```

| Field | Type | Required | Notes |
| --- | --- | :---: | --- |
| `path` | string | yes | Repo-relative path to a UTF-8 text file. |

Once a registry or entry references a repository, consumers MAY expose reads of
other UTF-8 files beneath that repository's checkout root. A `doc` entry is a
curated navigation leaf, not a file-access allow-list.

Consumers MUST canonicalize `path` and verify it stays within the entry's
repo root. Path-traversal attempts (`..`, absolute paths, symlink escapes)
MUST be rejected.

### 3.3 `index` entries

```yaml
- id: api
  name: API reference
  kind: index
  description: "REST endpoints"
  path: docs/api/pinakes.yaml
  repo: { ... }                    # OPTIONAL
```

| Field | Type | Required | Notes |
| --- | --- | :---: | --- |
| `path` | string | yes | Repo-relative path to another `pinakes.yaml`. |

Following an `index` entry produces a new index level. Consumers SHOULD
NOT eagerly load child indexes — load on demand, when the consumer
actually descends into them.

### 3.4 `merge` entries

```yaml
- kind: merge
  path: docs/api/pinakes.yaml
  prefix: "api-"                   # OPTIONAL
  repo: { ... }                    # OPTIONAL
```

| Field | Type | Required | Notes |
| --- | --- | :---: | --- |
| `path` | string | yes | Repo-relative path to another `pinakes.yaml`. |
| `prefix` | string | no | String prepended to each merged entry's `id`. |

A `merge` entry is **flattened** at load time: the target index's entries
appear in this index's level as if written here. `merge` entries do not
themselves have an `id` or appear in a consumer's view of the parent.

If `prefix` is set, every merged entry's `id` becomes `prefix + original_id`.
This disambiguates when a parent merges multiple sibling indexes.

Cycle detection: implementations MUST track visited (repo URL, path)
pairs and refuse to follow a `merge` whose target is already on the
load stack.

### 3.5 `command` entries

```yaml
- id: search
  name: Full-text search
  kind: command
  description: "Substring search over docs/. Pass a query."
  argv: ["rg", "--max-count", "20", "{query}", "docs/"]
  success_exit_codes: [0, 1]       # OPTIONAL
  repo: { ... }                    # OPTIONAL
```

| Field | Type | Required | Notes |
| --- | --- | :---: | --- |
| `argv` | array of string | yes | Argv vector. The token `{query}` is substituted with caller input (see §6.1). |
| `success_exit_codes` | array of integer | no | Exit codes treated as success. Defaults to `[0]`. |

Commands MUST be executed under the policy chain defined in §6, with the
working directory set to the entry's repo root. They MUST be invoked
directly via the OS process API (e.g. `execve`); consumers MUST NOT
pass `argv` through a shell.

---

## 4. Cross-repository references

Any entry MAY include a `repo` object overriding the repository in which
its `path` (or `argv`'s working directory) is resolved:

```yaml
repo:
  url: https://example.com/org/repo.git    # REQUIRED
  branch: main                              # one of branch / tag / commit, OPTIONAL
  tag: v1.2.3
  commit: 0123abcd...
  token_env: PROJECT_TOKEN                  # OPTIONAL — see §7
  submodules: true                          # OPTIONAL, default true
```

| Field | Type | Required | Notes |
| --- | --- | :---: | --- |
| `url` | string | yes | Git URL. SSH (`git@host:org/repo.git`), HTTPS, and `file://` are valid. |
| `branch` | string | no | Branch name. Mutually exclusive with `tag` and `commit`. |
| `tag` | string | no | Tag name. |
| `commit` | string | no | Full SHA. **Pinned commits MUST never be auto-refreshed.** |
| `token_env` | string | no | Environment variable name to read an auth token from. |
| `submodules` | bool | no | Whether to recursively initialize submodules on clone. Default `true`. |

If `repo` is omitted, the entry uses the enclosing index's repo. If no
parent has a repo (e.g. a hand-written root index loaded from a local
file), the consumer SHOULD reject the index.

### 4.1 Path semantics

Within a single repo, all `path:` fields are **repo-root relative**.
When an entry has its own `repo:`, `path:` is relative to **that** repo's
root, not the parent's.

### 4.2 Refresh policy

Consumers MUST treat clones as long-lived caches. They SHOULD re-fetch
on a configurable interval (lazy, no background scheduler is required).

Pinned `commit:` refs are immutable and MUST NOT be re-fetched.

---

## 5. Registry

A **registry** is a separate file that maps names to top-level pinakes
indexes. It is consumer-side configuration; the spec defines the format
so registries are portable across implementations.

```yaml
indexes:
  rust-stdlib:
    description: "Rust standard library docs"
    repo:
      url: https://github.com/rust-lang/rust.git
      branch: master
    path: docs/pinakes.yaml
    refresh: 24h                             # OPTIONAL, see below

  internal:
    repo:
      url: git@github.example.com:platform/docs.git
      branch: main
      token_env: PLATFORM_DOCS_TOKEN
    path: pinakes.yaml
    refresh: never
```

| Registry-entry field | Type | Required | Notes |
| --- | --- | :---: | --- |
| `repo` | object | yes | Same shape as §4. |
| `path` | string | yes | Path to the root index inside that repo. |
| `description` | string | no | One-line summary the consumer may surface. |
| `refresh` | string | no | Either `never` or a duration string (`5m`, `1h`, `24h`, …). Overrides any consumer default. |

Registry **keys** are the names a consumer (or LLM) uses to address an
index. They MUST be unique within a registry.

---

## 6. Command policy

Commands run under a **policy chain**: a list of constraints accumulated
top-down from the root index to the leaf entry.

A `command_policy` block at any index level looks like:

```yaml
command_policy:
  allow: '^rg( -[A-Za-z]+)*( --[A-Za-z-]+(=[^ ]+)?)* [^;&|`$]+$'
  timeout_secs: 10
```

| Field | Type | Required | Notes |
| --- | --- | :---: | --- |
| `allow` | string (regex) | no | A POSIX-extended regex. |
| `timeout_secs` | integer | no | Wall-clock seconds. |

### 6.1 Allow regex (intersect-only)

The flattened `argv` (joined by single spaces) MUST match every `allow`
regex on the chain — root and every parent down to the entry. **Children
narrow but never widen.** An empty chain (no `allow` anywhere) means
**deny all**.

`{query}` substitution happens **before** the regex check: the
post-substitution argv is what gets matched. This is intentional — a
malicious query can't bypass the allowlist.

`{query}` is substituted **into argv elements**, never via a shell.
Implementations MUST NOT invoke a shell to expand it.

### 6.2 Timeout

The chain's effective timeout is the **deepest non-null** `timeout_secs`
on the chain (a child's value takes precedence over the parent's). If no
level sets a timeout, implementations SHOULD apply a sane default
(reference implementation: 30 seconds).

### 6.3 Exit codes

By default, exit code `0` is success and any other code is failure. An
entry MAY set `success_exit_codes: [0, 1]` (e.g. for grep-family tools
where exit 1 means "no matches").

### 6.4 Output

Implementations SHOULD truncate command stdout to a reasonable cap
(reference implementation: 256 KiB). The truncation point and behavior
(suffix, error, …) is implementation-defined; this is not part of the
spec because it depends on the consumer's transport.

---

## 7. Authentication

A consumer fetching repos MUST resolve credentials in the following
order, stopping at the first match:

1. The entry's `repo.token_env` (if set, must be present in the
   environment; absence is an error, not a fallback).
2. A consumer-side host map (typically a separate config file)
   keyed by the URL's host. SSH URLs (`git@host:org/repo.git`)
   parse `host` from the part before `:`.
3. SSH agent (for `git@` URLs only).

`file://` URLs require no auth and MUST skip resolution entirely.

The host map's exact file location and shape is consumer-side
configuration and not normative. A reference shape:

```yaml
hosts:
  github.com:
    token_env: GITHUB_TOKEN
  gitlab.example.com:
    token_env: GITLAB_TOKEN
    username: oauth2
```

Submodule remotes MUST be authenticated against the same host map.

---

## 8. Conformance

A **conforming consumer** MUST:

- Reject indexes whose `version:` it does not recognize.
- Reject indexes with unknown top-level or entry-level fields.
- Detect `merge`/`index` cycles.
- Enforce path-traversal protection on all `path:` fields.
- Enforce the intersect-only command policy chain.
- Treat pinned `commit:` refs as immutable.
- Skip auth resolution for `file://` URLs.

A conforming consumer MAY:

- Skip support for `command` entries entirely (in which case it MUST
  surface them as inert metadata, not omit them).
- Cache parsed indexes in memory between requests.
- Apply per-implementation defaults (timeouts, output caps, refresh
  intervals) that this spec leaves unspecified.

A conforming consumer MUST NOT:

- Execute `command` entries via a shell.
- Auto-refresh pinned `commit:` refs.
- Allow children to widen any parent's `allow` regex.

A test corpus for conformance lives at [`examples/`](./examples/). It is
informative, not normative — implementations are free to add their own
fixtures.

---

## 9. Open questions

The following are deliberately unspecified in version 1 and are candidates
for a future revision:

- **Internationalization.** `name` and `description` are single strings.
  A future version may add a localized form.
- **Schema evolution.** No `extends:` mechanism for sharing common
  definitions across indexes; `merge` is a coarser tool.
- **Telemetry / observability.** No spec-mandated logging or metrics.
- **Signing.** No mechanism for a consumer to verify an index hasn't
  been tampered with in transit.

Feedback on any of these is welcome — open an issue or PR.
