from mc_wave60 import simulate_run, WaveConfig
from collections import Counter
from statistics import mean,median
rows=[]
for seed in range(100):
 s,h=simulate_run(None,None,waves=83,seed=seed,config=WaveConfig(faction='Lions',red=True,package='salamander',attenuation_enabled=True))
 w40=h[39];end=h[-1]
 rows.append((seed,s.mc_owned,s.first_mc_wave,s.first_amplifier_wave,w40['mc_owned'],end['drafts_resolved'],end['mc_from_3a_this_wave'],end['blueprint_acquisitions'].get('BPCB21',0),end['censored']))
print('FIRST_MC',Counter(r[2] for r in rows).most_common(12))
print('FIRST_AMP',Counter(r[3] for r in rows).most_common(12))
print('MC_AT_40 mean median',mean(r[4] for r in rows),median(r[4] for r in rows))
print('DRAFTS mean median max',mean(r[5] for r in rows),median(r[5] for r in rows),max(r[5] for r in rows))
print('TOP_MC',sorted(rows,key=lambda r:-r[1])[:8])
print('BOTTOM_MC',sorted(rows,key=lambda r:r[1])[:8])
print('CENSORED',sum(r[8] for r in rows))
