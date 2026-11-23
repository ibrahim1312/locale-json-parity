# Locale JSON Parity

Audit two JSON locale files for missing keys, value type mismatches, and brace placeholder changes.

## Quick start

Requires Python 3.11 or later. Uses the standard library and runs locally.

```bash
python3 tool.py en.json fr.json
```

Output is formatted JSON on standard output. Invalid inputs report an error on standard error and exit with status 1. Run the tool with --help for all arguments.

Paths use JSON Pointer escaping. Nested objects are traversed. Arrays are treated as leaf values. This checks named brace placeholders in strings and does not parse ICU MessageFormat.

## Example input

**en.json**

```
{"text":"Hi {{name}}","bye":"Bye","count":2}
```

**fr.json**

```
{"text":"Salut {prenom}","more":"Plus","count":"2"}
```

## Example output

```json
{
  "missing": [
    "/bye"
  ],
  "extra": [
    "/more"
  ],
  "type_mismatches": [
    "/count"
  ],
  "placeholder_mismatches": [
    "/text"
  ]
}
```

## License

[MIT](LICENSE).
