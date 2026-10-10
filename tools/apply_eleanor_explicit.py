from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
p=root/'model/mc_wave60.py'
s=p.read_text()
s=s.replace('    eleanor: bool = False\n', '    eleanor: bool = False\n    eleanor_starting_mc_1a_equivalent: int = 10  # +2 Tier 2/3 rarity per equivalent MC 1A\n    eleanor_initial_tier23_dampening: bool = False  # explicit: no initial dampening\n')
s=s.replace("    if config.eleanor and (config.eleanor_cadence < 1 or config.eleanor_first_wave < 1):", "    if config.eleanor_starting_mc_1a_equivalent < 0:\n        raise ValueError('invalid Eleanor starting rarity bonus')\n    if config.eleanor and config.eleanor_initial_tier23_dampening:\n        raise ValueError('Eleanor initial Tier 2/3 dampening is not modeled or supported')\n    if config.eleanor and (config.eleanor_cadence < 1 or config.eleanor_first_wave < 1):")
s=s.replace("            extra_tier_weights={tier: (extra_tier_weights or {}).get(tier, 0) +", "            extra_tier_weights={tier: (extra_tier_weights or {}).get(tier, 0) +\n                                (2 * config.eleanor_starting_mc_1a_equivalent if config.eleanor and tier in (2, 3) else 0) +")
p.write_text(s)
for filename in ['chain-establishment-experiment.json','faction-establishment-experiment.json']:
 p=root/'docs/tasks/mission-control-chain'/filename
 obj=json.loads(p.read_text())
 for sc in obj['scenarios']:
  if sc['config'].get('eleanor'):
   sc['config']['eleanor_starting_mc_1a_equivalent']=10
   sc['config']['eleanor_initial_tier23_dampening']=False
   sc['config']['eleanor_first_wave']=2
   sc['config']['eleanor_cadence']=2
 p.write_text(json.dumps(obj,indent=2)+'\n')
print('Eleanor explicit settings applied')
