from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]/'docs/tasks/mission-control-chain'
base=json.loads((root/'chain-establishment-experiment.json').read_text())
chains=[s for s in base['scenarios'] if s['name'].startswith('Chain /')]
packages=['howitzer','cannon','howitzer_cannon','sphd_rampart','sphd_retribution','sphd_fortress']
scenarios=[]
for package in packages:
 for original in chains:
  if package=='sphd_fortress' and original['name']!='Chain / Lions':
   continue
  config=dict(original['config']);config['package']=package
  scenarios.append({'name':package+' / '+original['name'].removeprefix('Chain / '),'config':config})
base['description']='Additional offensive package comparisons; building 1 and 2 tracked separately; fortress restricted to Lions/Red.'
base['scenarios']=scenarios
base['comparisons']=[]
path=root/'package-establishment-experiment.json'
path.write_text(json.dumps(base,indent=2)+'\n')
print(len(scenarios),'scenarios',path)
