# Synthetic raw replay corpus

These are authored contract examples, not recorded provider responses. The
`cases.json` manifest supplies expected invocation bindings and either `admit`
or the exact admission error code. Read each referenced payload as bytes. Several
`.json` files deliberately contain invalid JSON or schema-invalid data; do not
format, normalize, or load-and-reserialize them. `invalid-utf8.bin` deliberately
contains a non-UTF-8 byte. This corpus is language-neutral and can later be used
by consumer adapters or a different implementation.
