"""Asset-backed normal-bundle Blueprint roster for MC probability modeling."""
import json
from pathlib import Path
from mc_weights import BlueprintEntry

RARITY = {1: (100, 0), 2: (-3, 1), 3: (-8, 1)}


def load_blueprint_roster(path=None, faction=None):
    if path is None:
        path = Path(__file__).resolve().parents[1] / 'maps' / 'blueprints.json'
    data = json.loads(Path(path).read_text())
    codes = [row['code'] for row in data]
    if len(codes) != len(set(codes)):
        raise ValueError('duplicate Blueprint codes in asset roster')
    result = []
    for row in data:
        if not row['available_in_bundles']:
            continue
        if faction is not None and row['faction'] not in ('0', faction):
            continue
        rarity = row['rarity_index']
        if rarity not in RARITY:
            raise ValueError('unknown rarity index')
        base, increment = RARITY[rarity]
        result.append(BlueprintEntry(row['code'], rarity, base, increment))
    return result


def blueprint_identity(code):
    return 'MC' if code == 'BPSB07' else code
