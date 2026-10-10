"""High-value MC 3A draft outcomes; supports and offense equally counted."""
from statistics import mean
from mc_wave60 import WaveConfig, simulate_run

for target in range(10, 21):
    rows=[]
    for seed in range(100):
        state,history=simulate_run(None,None,waves=83,seed=seed,
            config=WaveConfig(faction='Lions',red=True,package='salamander',
                attenuation_enabled=True,mc_build_target=target,mc_reserve_target=3,
                mc_batch_size=2,mc_construction_policy='continuous'))
        outcomes=history[-1]['mc_draft_outcomes']
        offense=outcomes.get('hv_offense',0)
        support=outcomes.get('hv_support',0)
        other=outcomes.get('hv_other',0)
        mc=outcomes.get('mc_reinvestment',0)
        low=outcomes.get('low_value',0)
        empty=outcomes.get('empty',0)
        assert offense+support+other+mc+low+empty == state.drafts_resolved, (target,seed,outcomes,state.drafts_resolved)
        rows.append((state.drafts_resolved,offense,support,other,mc,low,empty,state.mc_built))
    print(target,*(round(mean(r[i] for r in rows),2) for i in (0,1,2,3,4,5,6,7)),
          'HV_TOTAL',round(mean(r[1]+r[2]+r[3] for r in rows),2),flush=True)
