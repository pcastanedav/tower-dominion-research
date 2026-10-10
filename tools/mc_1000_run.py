import json, statistics, sys
from mc_wave60 import simulate_run, WaveConfig
from mc_roster import load_blueprint_roster
roster=load_blueprint_roster()
cases=[('Baseline',{}),('Lions',{'red':True}),('Eleanor',{'eleanor':True}),('Tander',{'tander':True}),('Magel',{'magel':True})]
out={}
for saved in (False,True):
 for name,flags in cases:
  cfg=WaveConfig(**flags,tier1_amplifier_doctrine_from_wave1=saved)
  runs=[]
  for i in range(1,1001):
   state,h=simulate_run(roster,None,waves=103,seed=i,config=cfg)
   if len(h)!=103 or state.censored: raise RuntimeError((name,saved,i,len(h),state.censored))
   runs.append(h)
  data={str(w):{'mean':round(statistics.mean(h[w-1]['mc_owned'] for h in runs),3),**{'p_ge_'+str(t):round(100*statistics.mean(h[w-1]['mc_owned']>=t for h in runs),2) for t in (5,10,20)}} for w in (20,35,40,50,60,63,64,83,103)}
  out[('Saved Tier I' if saved else 'Natural')+' / '+name]=data
  print(('Saved Tier I' if saved else 'Natural'),name,'W63',data['63'],'W103',data['103'],flush=True)
with open('/tmp/td_mc_1000_results.json','w') as f:json.dump(out,f,indent=2)
