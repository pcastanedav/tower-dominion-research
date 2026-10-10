from statistics import mean, median
from mc_wave60 import WaveConfig, simulate_run

for policy in ('threshold','draft_replenish','preserve'):
    rows=[]
    for seed in range(100):
        state,hist=simulate_run(None,None,waves=83,seed=seed,
            config=WaveConfig(faction='Lions',red=True,package='salamander',
                attenuation_enabled=True,mc_build_target=15,mc_reserve_target=3,
                mc_batch_size=3,mc_construction_policy=policy))
        established=next((h['wave'] for h in hist if h['mc_established']),None)
        post=[h for h in hist if established is not None and h['wave']>established]
        builds=[h['mc_built']-hist[h['wave']-2]['mc_built'] for h in post]
        rows.append((state.mc_built,state.mc_in_hand,
            hist[-1]['blueprint_acquisitions'].get('BPCB21',0),
            state.drafts_resolved,sum(h['mc_selective_this_wave'] for h in post),len(post),
            sum(x>0 for x in builds),sum(x for x in builds),
            sum(h['mc_in_hand']==0 for h in post),
            sum(h['mc_from_3a_this_wave'] for h in post)))
    print(policy,
        'built',round(mean(r[0] for r in rows),2),
        'reserve',round(mean(r[1] for r in rows),2),
        'salamander',round(mean(r[2] for r in rows),2),
        'median',median(r[2] for r in rows),
        'drafts',round(mean(r[3] for r in rows),2),
        'selective_pct',round(100*sum(r[4] for r in rows)/max(1,sum(r[5] for r in rows)),1),
        'build_events',sum(r[6] for r in rows),
        'post_established_built',sum(r[7] for r in rows),
        'zero_reserve_pct',round(100*sum(r[8] for r in rows)/max(1,sum(r[5] for r in rows)),1),
        'mc_from_drafts',sum(r[9] for r in rows),flush=True)
