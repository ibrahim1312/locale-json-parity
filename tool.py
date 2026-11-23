"""Audit two JSON locale files for missing keys, value type mismatches, and brace placeholder changes."""

import argparse
import json
from decimal import InvalidOperation
from pathlib import Path
import re
from collections import Counter


def main():
    parser = argparse.ArgumentParser(description='Audit two JSON locale files for missing keys, value type mismatches, and brace placeholder changes.')
    parser.add_argument("reference", type=Path)
    parser.add_argument("translation", type=Path)
    args = parser.parse_args()

    def unique_pairs(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f"Duplicate JSON key: {key!r}")
            result[key] = value
        return result

    def flatten(value, path=""):
        if isinstance(value, dict) and value:
            for key, child in value.items():
                escaped = key.replace("~", "~0").replace("/", "~1")
                yield from flatten(child, f"{path}/{escaped}")
        else:
            yield path, value

    def load(path):
        root = json.loads(path.read_text(encoding="utf-8-sig"), object_pairs_hook=unique_pairs)
        if not isinstance(root, dict):
            raise ValueError(f"{path}: expected a JSON object")
        if not root:
            return {}
        return dict(flatten(root))

    reference, translated = load(args.reference), load(args.translation)
    placeholder = re.compile(r"(?<!\{)\{(?:\{)?([A-Za-z_][\w.-]*)\}\}?(?!\})")
    types, placeholders = [], []
    for key in sorted(reference.keys() & translated.keys()):
        left, right = reference[key], translated[key]
        if type(left) is not type(right):
            types.append(key)
        elif isinstance(left, str) and Counter(placeholder.findall(left)) != Counter(placeholder.findall(right)):
            placeholders.append(key)
    report = {"missing": sorted(reference.keys() - translated.keys()),
              "extra": sorted(translated.keys() - reference.keys()),
              "type_mismatches": types, "placeholder_mismatches": placeholders}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, OverflowError, InvalidOperation, TypeError) as error:
        raise SystemExit(f"Error: {error}") from None
