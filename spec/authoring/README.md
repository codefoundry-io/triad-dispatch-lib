# PRD and Spec authoring

[The common authoring rule](../reference/spec-authoring.md#R-PRD-SPEC) defines
the relationship: PRD intent → Spec behavior → rule/contract → case → owning unit.
[implementation-map.schema.json](implementation-map.schema.json) is the
machine-readable structure. [The Claude v2 bundle](maps/claude-host-v2.json)
connects the existing documents; it contains references, not a second copy of
their requirements or expected results.

[The shared development log](shared-dev-log.md) records what a host's
implementation reading found — in A, in B or in this specification — as rows
keyed by case id, so the host that must act can find it (`R-DEV-LOG`).

## Edit a bundle

1. Read current remote main and record its commit under
   [R-AUTHORING-SYNC](../reference/spec-authoring.md#R-AUTHORING-SYNC). Resolve
   every input from the same checkout. Preserve pinned historical evidence as
   history; a main URL alone does not pin an implementation input.
2. Write intent and acceptance in the PRD. Put behavior in the existing normative
   rule or Spec section and types in the contract. Keep observed vendor limits
   and unrun checks in their evidence records, linked from the handoff.
3. Put stable explicit Markdown anchors (`<a id="PRD-ROSTER"></a>`) on their own
   unindented lines outside code blocks and comments at the referenced sections.
   Add the PRD/Spec bundle under `authoring/maps/`. Reuse
   case IDs and unit keys from `cases/cases.json` and `units.json`.
4. Run the checks below. Review the meaning and adequacy of each requirement
   link separately; a valid link does not prove that its case tests the intent.

The current bundle groups the PRD's implementation requirements. Its acceptance
links identify evidence entry points; the PRD's Functional coverage map and the
canonical case corpus retain their fuller coverage descriptions. Historical
decision documents are not all registered as implementation bundles.

## Offline checks

With `requirements-dev.txt` available in the selected Python environment:

```sh
python3 tools/check_authoring.py
python3 -m pytest -q tests
```

The checker uses the existing JSON Schema Draft 2020-12 library and local
references only. It checks required structure, document ownership of section
references, unique requirement/document IDs, existing explicit anchors and
case/unit references, including the owning unit of each linked case.
Local references cannot traverse symlinks. It fetches no
web pages, executes no manifest commands and invokes no AI provider.

`status` records the author's document classification. Schema acceptance does
not grant approval, establish semantic completeness, report a test result or
change a host's adopted revision. No runtime wire/policy schema is replaced by
this authoring schema. Tests for host behavior remain in the owning host.

## AI entry maps

[AGENTS.md](../AGENTS.md), [CLAUDE.md](../CLAUDE.md) and
[GEMINI.md](../GEMINI.md) contain the same short links. The
[common source map](../reference/README.md) owns where guidance lives. Add or
change guidance there and in its canonical source; update the entry maps only
when their destinations change.
