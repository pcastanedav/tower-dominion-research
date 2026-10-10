from mc_wave60 import simulate_run,WaveConfig
from statistics import mean,median
from collections import Counter
rows=[]
for seed in range(100):
 s,h=simulate_run(None,None,waves=83,seed=seed,config=WaveConfig(faction='Lions',red=True,package='salamander',attenuation_enabled=True,amplifier_effect_enabled=False))
 e=h[-1]
 rows.append((s.mc_owned,e['blueprint_acquisitions'].get('BPCB21',0),s.first_mc_wave,s.first_amplifier_wave,h[39]['mc_owned'],e['drafts_resolved'],e['censored']))
print('RUNS',len(rows))
print('MC_W83 mean median min max',round(mean(x[0] for x in rows),2),median(x[0] for x in rows),min(x[0] for x in rows),max(x[0] for x in rows))
print('SALAMANDER_W83 mean median',round(mean(x[1] for x in rows),2),median(x[1] for x in rows))
print('MC_W40 mean median',round(mean(x[4] for x in rows),2),median(x[4] for x in rows))
print('DRAFTS mean median max',round(mean(x[5] for x in rows),2),median(x[5] for x in rows),max(x[5] for x in rows))
print('CENSORED',sum(x[6] for x in rows))
print('FIRST_MC_NONE',sum(x[2] is None for x in rows))
print('FIRST_AMP_NONE',sum(x[3] is None for x in rows))
print('FIRST_10',rows[:10])
