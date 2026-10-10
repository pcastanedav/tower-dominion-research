from mc_wave60 import WaveConfig,simulate_run
from statistics import mean,median
for label,built,reserve in [('A',None,0),('B',15,5),('C',20,6)]:
 results=[]
 for seed in range(100):
  state,h=simulate_run(None,None,waves=83,seed=seed,config=WaveConfig(faction='Lions',red=True,package='salamander',attenuation_enabled=True,mc_build_target=built,mc_reserve_target=reserve))
  last=h[-1]
  results.append((state.mc_built,state.mc_in_hand,last['blueprint_acquisitions'].get('BPCB21',0),state.drafts_resolved,state.censored))
 print(label,'built',round(mean(r[0] for r in results),2),'reserve',round(mean(r[1] for r in results),2),'salamander',round(mean(r[2] for r in results),2),'median',median(r[2] for r in results),'drafts',round(mean(r[3] for r in results),2),'censored',sum(r[4] for r in results))
