from pathlib import Path
p=Path(__file__).resolve().parent/'run_mc_experiment.py'
s=p.read_text()
s=s.replace("'all_hv_total')", "'all_hv_total', 'offense_building_1', 'offense_building_2', 'complete_sets', 'has_all_required', 'has_only_one_required')")
s=s.replace("                    vals = (h['mc_owned']", "                    names = PACKAGES[package]\n                    counts = [sum(q for code,q in acquired.items() if BLUEPRINT_NAMES.get(code, code) == target) for target in names]\n                    first = counts[0]\n                    second = counts[1] if len(counts) > 1 else 0\n                    complete = min(counts)\n                    has_all = int(all(counts))\n                    only_one = int(len(counts) == 2 and sum(c > 0 for c in counts) == 1)\n                    vals = (h['mc_owned']")
s=s.replace("h['drafts_resolved'], offense, support, offense + support)", "h['drafts_resolved'], offense, support, offense + support, first, second, complete, has_all, only_one)")
s=s.replace("    payload = {'configuration': spec", "    package_labels = {case['name']: list(PACKAGES[case.get('config', {}).get('package') or common.get('package') or 'salamander']) for case in cases}\n    payload = {'package_building_labels': package_labels, 'configuration': spec")
p.write_text(s)
print('Added individual building counts and completion metrics')
