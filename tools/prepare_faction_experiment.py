from pathlib import Path
import json
p=Path('tools/run_mc_experiment.py')
s=p.read_text()
s=s.replace('from statistics import mean, stdev','from statistics import mean, stdev, median\nfrom mc_packages import BLUEPRINT_NAMES, SUPPORTS, PACKAGES')
s=s.replace("'hv_total', 'drafts_resolved')", "'hv_total', 'drafts_resolved', 'all_hv_offense', 'all_hv_support', 'all_hv_total')")
s=s.replace("'median': values[(n-1)//2]", "'median': median(values)")
s=s.replace("                    vals = (h['mc_owned']", "                    acquired = h['blueprint_acquisitions']\n                    package = config.package or 'salamander'\n                    offense = sum(q for code,q in acquired.items() if BLUEPRINT_NAMES.get(code, code) in PACKAGES[package])\n                    support = sum(q for code,q in acquired.items() if BLUEPRINT_NAMES.get(code, code) in SUPPORTS)\n                    vals = (h['mc_owned']")
s=s.replace("                            h['drafts_resolved'])", "                            h['drafts_resolved'], offense, support, offense + support)")
assert "h['drafts_resolved'], offense, support, offense + support)" in s
p.write_text(s)
base=json.loads(Path('docs/tasks/mission-control-chain/chain-establishment-experiment.json').read_text())
base['description']='Faction roster comparison with matched Baseline and Chain policies. Lions Red duplication only for Lions; other factions no invented commander bonuses.'
base['scenarios']=[]
base['comparisons']=[]
for faction in ('Iron Dragoons','Lions','Pargan Assault Group'):
    natural=f'{faction} / Natural'
    chain=f'{faction} / Chain'
    flags={'faction':faction,'red':faction=='Lions'}
    base['scenarios'].append({'name':natural,'config':flags})
    base['scenarios'].append({'name':chain,'config':{**flags,'package':'salamander','attenuation_enabled':True,'mc_build_target':40,'mc_reserve_target':3,'mc_batch_size':2,'mc_construction_policy':'continuous','mc_dynamic_selectivity':True}})
    base['comparisons'].append({'scenario':chain,'reference':natural})
base['defaults']={'tier3_wave':40}
Path('docs/tasks/mission-control-chain/faction-establishment-experiment.json').write_text(json.dumps(base,indent=2)+'\n')
print('Prepared six faction scenarios and common acquisition metrics')
