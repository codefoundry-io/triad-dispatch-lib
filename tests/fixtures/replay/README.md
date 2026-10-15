# Synthetic raw replay corpus

These are authored contract examples, not recorded provider responses. The
`cases.json` manifest supplies expected invocation bindings and either `admit`
or the exact admission error code. Read each referenced payload as bytes. Several
`.json` files deliberately contain invalid JSON or schema-invalid data; do not
format, normalize, or load-and-reserialize them. `invalid-utf8.bin` deliberately
contains a non-UTF-8 byte. This corpus is language-neutral and can later be used
by consumer adapters or a different implementation.

Refused cases may include optional `diagnostics` fixture metadata: `missing` is
the expected canonical required name and `path` is the expected schema path as
a JSON array. Both source replay tests and the installed-wheel replay driver
check these values. `missing-root` and `missing-finding` are authored synthetic
examples of root and nested required failures. This metadata is not a wire-schema
field and does not extend the admitted verdict format.
