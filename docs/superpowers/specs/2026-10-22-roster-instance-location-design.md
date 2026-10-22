# Roster instance location design

Status: draft for the required project design review. A fresh builder check
found no important unanswered question. No runtime implementation or release is
included. The preceding documentation review encountered an invalid AGY 1.4.5
terminal object with extra `toolAction`/`toolSummary` fields; its host-owned
producer/format issue must be resolved before relying on another formal round.

The owner selected issue #9's optional location improvement after the October 22 library triage. The existing library rejects invalid rosters correctly, but the same invalid field in entries 0 and 3 produces identical public diagnostics. A caller cannot locate the entry from the schema path alone.

Add `RosterError.instance_path: tuple[str | int, ...] | None`. It is `None` on direct construction and on non-schema refusals. For the existing first selected schema error, copy `tuple(validation_error.absolute_path)`. The empty tuple means the evaluated document root; `None` means location is unavailable. The existing `.document` says whether the location is in defaults, the override, or the resolved roster. Resolved indices refer to the final merged order, not the source override order. For a bad timeout in the fourth entry the value is `('legs', 3, 'timeout_s')`.

The [official jsonschema 4.26.0 error documentation](https://python-jsonschema.readthedocs.io/en/stable/errors/#jsonschema.exceptions.ValidationError.absolute_path), accessed 2026-10-22, defines `absolute_path` relative to the original validated instance and permits an empty root path. This matches the locked dependency and avoids inventing a location parser.

Preserve constructor signature, error codes, messages, `.args`, `.path` (schema path), `.missing`, `.document`, validation ordering, admission decisions, and copy/nonmutation behavior. Do not search child errors or run a second validation. Required and aggregate errors point to the containing instance: for a missing Google adapter, `('legs', index)` accompanies the existing `.missing` result, including `None` for an `anyOf` winner.

The current verified canonical roster schema uses only fixed object properties and array indices; every object rejects additional properties. Thus copied instance paths contain canonical field names and integer indices, not values, entry names, or unknown-key spelling. An additional-properties failure points at its containing object. Test these concrete guarantees at root, entry and adapter levels. Keep exception-context/traceback limitations documented. This is a roster-only API; no arbitrary caller schema or general JSON Pointer API is introduced. A future schema extension with dynamic object keys must reassess this guarantee. No speculative schema walker or duplicate property-name catalogue is needed for the current contract.

This implementation choice is the leader's bounded call: expose a tuple rather than a formatted pointer, so hosts can format it independently. The source of truth stays in `spec/reference/library-api.md`. No schema IDs, acceptance semantics, schema bytes, provider integration, host formatting, installation, or release automation change. Issues #17, #21 and #5 remain separate decisions.

Verification must distinguish indices 0 and 3 in defaults and override errors; check final merged positions, standalone validation and selection; cover root `()`, both Google route-block vectors, unknown properties, non-schema `None`, and input nonmutation. Existing compatibility checks must remain green. Run the complete library suite, spec/authoring checks, API compatibility and package rebuild/smoke checks, then exact-head CI on the declared macOS/Ubuntu Python matrix. Use the project's formal review profile before implementation admission. A release candidate needs a new version and its own publication approval; neither docs review nor the enhancement PR publishes it.

This is one small functional unit: approximately 2-5 production lines added, no production deletions, 2 source files; roughly 60-100 test lines and a short API documentation update. The public property and actual canonical-schema invariant are the review boundary, not a broader diagnostic redesign.
