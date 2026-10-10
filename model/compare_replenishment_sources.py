from statistics import mean, median
from mc_wave60 import WaveConfig, simulate_run

for reserve, batch in [(2,2),(3,3),(3,2)]:
    for source in ('both','draft_only','reinforcement_only'):
        results=[]
        for seed in range(100):
            state,history=simulate_run(None,None,waves=83,seed=seed,
                config=WaveConfig(faction='Lions',red=True,package='salamander',
                    attenuation_enabled=True,mc_build_target=15,
                    mc_reserve_target=reserve,mc_batch_size=batch,
                    mc_replenish_source=source))
            established=next((h['wave'] for h in history if h['mc_established']),None)
            post=[h for h in history if established is not None and h['wave']>established]
            results.append((state.mc_built,state.mc_in_hand,
                history[-1]['blueprint_acquisitions'].get('BPCB21',0),
                sum(h['mc_selective_this_wave'] for h in post),len(post),
                sum(h['mc_draft_selective_this_wave'] for h in post),state.drafts_resolved))
        print('reserve',reserve,'batch',batch,'source',source,
              'built',round(mean(r[0] for r in results),2),
              'hand',round(mean(r[1] for r in results),2),
              'salamander',round(mean(r[2] for r in results),2),
              'median',median(r[2] for r in results),
              'reinforcement_selective_pct',round(100*sum(r[3] for r in results)/max(1,sum(r[4] for r in results)),1),
              'draft_selective_pct',round(100*sum(r[5] for r in results)/max(1,sum(r[4] for r in results)),1),
              'drafts',round(mean(r[6] for r in results),2),flush=True)
