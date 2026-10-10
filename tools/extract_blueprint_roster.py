#!/usr/bin/env python3
"""Extract serialized BlueprintData scalar fields; no inferred availability."""
import argparse
import json
import re
import struct
from pathlib import Path
import UnityPy


def read_string(data, offset):
    length = struct.unpack_from('<I', data, offset)[0]
    if length > 512 or offset + 4 + length > len(data):
        raise ValueError('invalid string length')
    value = data[offset + 4:offset + 4 + length].decode('utf-8')
    return value, (offset + 4 + length + 3) & ~3


def extract(path):
    env = UnityPy.load(path)
    result = []
    for obj in env.objects:
        if obj.type.name != 'MonoBehaviour':
            continue
        raw = obj.get_raw_data()
        try:
            name, offset = read_string(raw, 28)
            if not re.fullmatch(r'BP[A-Z0-9_]+', name):
                continue
            offset += 4  # BlueprintData's serialized identifier prefix
            guid, offset = read_string(raw, offset)
            if struct.unpack_from('<I', raw, offset)[0] == 0:
                offset += 4
            faction, offset = read_string(raw, offset)
            tower, offset = read_string(raw, offset)
            cost, currency, rarity, available = struct.unpack_from('<qiiB', raw, offset)
        except (ValueError, struct.error, UnicodeDecodeError):
            continue
        result.append(dict(code=name, path_id=obj.path_id, guid=guid,
                           tower=tower, faction=faction, cost=cost, currency=currency,
                           rarity_index=rarity, available_in_bundles=bool(available)))
    return sorted(result, key=lambda row: row['code'])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('resources_assets')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    data = extract(args.resources_assets)
    output = json.dumps(data, indent=2) + '\n'
    if args.output:
        Path(args.output).write_text(output)
    else:
        print(output)
