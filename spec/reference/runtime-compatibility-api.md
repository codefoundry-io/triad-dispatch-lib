# Common runtime compatibility API

This additive dev6 API implements the deterministic portion of
[R-SHARED-RUNTIME-COMPAT](review-rules.md#R-SHARED-RUNTIME-COMPAT) and C81-C83.
It performs no filesystem, provider, environment, installation or native-agent
operation. The consuming host authenticates artifacts, measures capabilities,
verifies the declared consumer corpus and preserves its transaction boundary.

## Trust boundary

A runtime descriptor is the host's declaration of combinations it has verified
for an exact artifact. Its supported binding IDs are not discovered from a
package version or an installer marker. The host must authenticate the descriptor
and every referenced artifact and compatibility record before calling these
functions. Computing a digest, parsing a descriptor or passing this API does not
establish authenticity or prove that an unexecuted consumer test passed.

The consumer's baseline and library digests are provenance pins, not semver
ranges. Its context digest covers its caller-owned adapter/default/configuration,
classifier/authentication/permission and toolkit/receipt binding contract as
measured by the host. Keep secrets out of descriptors. Changing any such context
creates a different consumer binding requiring new compatibility evidence.

## Immutable descriptions

`validate_consumer_binding(document: dict) -> ConsumerBinding` accepts exactly:

| Field | Meaning |
| --- | --- |
| `schema` | Literal `triad-consumer-binding.v1` |
| `consumer` | Host-owned consumer identifier |
| `baseline_digest` | Immutable supported consumer baseline identity |
| `library_digest` | Adopted library artifact identity |
| `adapter` | Host-owned adapter contract identifier |
| `capabilities` | Required capability identifiers; may be empty |
| `commands` | Nonempty set of required command basenames |
| `context_digest` | Immutable caller context identity |

Digests are lowercase SHA-256 strings of exactly 64 hexadecimal characters.
Identifiers/capabilities match `[a-z][a-z0-9._:-]{0,127}`; command basenames match
`[A-Za-z0-9][A-Za-z0-9_.-]{0,127}`. Collections in input documents are lists with
no duplicate entries. Unknown fields and unsupported schema versions refuse.
These consumer/adapter identifiers do not extend canonical roster host literals.

The returned frozen record has the same fields, sorted tuple collections, and
`binding_id`: SHA-256 of UTF-8 canonical JSON of the validated document, with
sorted keys, compact separators, ASCII escaping and sorted set-valued lists.
Input field/list order therefore does not select a consumer or change identity.
No `binding_id` field is accepted in the input document.

`validate_runtime_descriptor(document: dict) -> RuntimeDescriptor` accepts
exactly `schema`, `artifact_digest`, `commands`, `capabilities` and
`supported_bindings`. Schema is `triad-runtime-compat.v1`; `artifact_digest`
identifies the host-verified runtime artifact. Commands and capabilities use the
same identifier rules. Commands and supported binding IDs are nonempty unique
lists; capabilities may be empty. The returned record has sorted tuple fields.

Dataclass constructors themselves do not validate. Public operations revalidate
records, including the consumer's computed binding ID, before making decisions.
They never mutate supplied documents or return mutable collection aliases.

## Compatibility and selection

```python
check_consumer_compatibility(runtime, binding) -> None
select_consumer_binding(runtime, bindings, *, explicit_binding, legacy_binding)
```

Compatibility requires the exact binding ID in `runtime.supported_bindings`
and every required command/capability in the runtime's declared sets. An equal
library version, similar host name or available `--help` output is insufficient.
Hosts must also check actual capabilities and provenance; this operation checks
the supplied declaration, not the workstation.

Selection validates the whole binding inventory and rejects duplicate IDs.
When `explicit_binding` is present, only that exact ID may be selected. An empty,
malformed or unknown explicit ID refuses; it never falls back. Otherwise only
the supplied established `legacy_binding` may be selected. If both selectors
are absent, selection refuses even when the inventory has a single member.
After selection the compatibility check must pass. A newly installed consumer
cannot become the legacy default merely through list or installation order.

The returned record preserves the chosen consumer's context. The host executes
its actual adapter; this API neither substitutes a native child with a CLI nor
changes defaults, environment, classifiers or receipt paths.

## Conservative retention

```python
plan_runtime_retention(
    artifacts, *, consumer_references, active_references, dependencies_known
) -> RuntimeRetention
```

Inputs are finite list/tuple digest inventories and a strict boolean. Duplicate
artifact IDs or a reference absent from the artifact inventory refuse; repeated
references are harmless. With known dependencies, `retain` is the sorted union
of consumer and active references, `remove` contains only unreferenced artifacts,
and `diagnostic` is `references_preserved`. With unknown dependencies, every
artifact is retained, nothing is removable and the diagnostic is
`dependencies_unknown`.

This is a pure decision over a host-supplied observation. A caller must not treat
it as a lock, permission grant, fresh process inventory or deletion primitive.
Recheck references and provenance under the host's existing publication/removal
transaction. Unknown active use requires conservative retention.

## Refusals and evidence

`RuntimeCompatibilityError` is a `ValueError` with stable `.code` and fixed,
value-free text. Codes are `invalid_descriptor`, `invalid_binding`,
`unsupported_schema`, `invalid_selector`, `missing_context`, `unknown_binding`,
`ambiguous_binding`, `unsupported_binding`, `command_mismatch`,
`capability_mismatch`, `invalid_inventory` and `incomplete_inventory`.

The library suite and installed public consumer driver exercise these operations.
They do not certify any host launcher, caller adapter, upgrade, transaction or
running invocation. Host/platform C81-C83 results remain separately recorded in
the canonical cases and host adoption records.
