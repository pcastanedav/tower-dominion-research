import reinforcement_model as m, random

def choose_normal(cards,rng,wave,state,cleanup):
    target=[i for i,c in enumerate(cards) if any(x and x.startswith("TB0D") for x in c)]
    if target:
        best=max(sum(bool(x and x.startswith("TB0D")) for x in cards[i]) for i in target)
        return rng.choice([i for i in target if sum(bool(x and x.startswith("TB0D")) for x in cards[i])==best])
    if cleanup:
        weights=dict(m.state_doctrine_pool(state,wave))
        scores=[sum(weights.get(x,0) for x in c if x and not x.startswith("TB")) for c in cards]
        best=max(scores); return rng.choice([i for i,v in enumerate(scores) if v==best])
    return rng.randrange(len(cards))

def take_many(xs,state,rng,wave,cleanup):
    events=[]
    for x in xs:
        if x: events.extend(m.acquire_doctrine(state,x,rng,wave,"aggressive" if cleanup else "none"))
    return events

def trial(others,mode,seed,cleanup=False,starts=None):
    rng=random.Random(seed); state=m.DoctrineRunState(faction="Lions")
    starts=starts if starts is not None else [1]*others
    for wave in range(1,36):
        state.placed_families={0}|{j for j,start in enumerate(starts,1) if wave>=start}
        candidates=8 if mode=="tander" else 6
        cards=m.dynamic_doctrine_screen(
            rng,"Lions",wave,removed=state.ordinary_owned,tb_owned=state.tb_owned,
            tb_mult=state.tb_mult,placed_families=state.placed_families,
            card_count=candidates//2,t2_bonus=state.t2_bonus,placed_towers=state.placed_towers)
        take_many(cards[choose_normal(cards,rng,wave,state,cleanup)],state,rng,wave,cleanup)
        if "TB0D7" in state.tb_owned:return wave
        if mode=="magel" and m.magel_draft_due(wave):
            draft=m.state_doctrine_draft(rng,state,wave,3)
            target=[x for x in draft if x.startswith("TB0D")]
            if target:pick=rng.choice(target)
            elif cleanup:
                weights=dict(m.state_doctrine_pool(state,wave)); pick=max(draft,key=lambda x:weights.get(x,0))
            else:pick=rng.choice(draft)
            take_many([pick],state,rng,wave,cleanup)
            if "TB0D7" in state.tb_owned:return wave
    return None

def summarize(vals):
    n=len(vals); hit=[x for x in vals if x is not None]
    return (sum(x is not None and x<=20 for x in vals)/n,len(hit)/n,sum(hit)/len(hit) if hit else None)

if __name__=="__main__":
    N=int(__import__("os").environ.get("N","5000"))
    for cleanup in (False,True):
        print("CLEANUP",cleanup,flush=True)
        for others in range(6):
            row=[]
            for mode in ("base","tander","magel"):
                vals=[trial(others,mode,i+others*100000+{"base":1,"tander":2,"magel":3}[mode]*1000000+int(cleanup)*10000000,cleanup) for i in range(N)]
                row.append((mode,summarize(vals)))
            print(others,*[f"{mode} W20={v[0]:.3%} W35={v[1]:.3%}" for mode,v in row],flush=True)
    schedules={"desired_only":[],"one_early":[1],"one_late":[10],"two_early":[1,4],"two_late":[10,15],"three_early":[1,4,9],"three_late":[10,15,20]}
    print("TIMING",flush=True)
    for name,starts in schedules.items():
        vals=[trial(len(starts),"base",20000000+i,False,starts) for i in range(N)]
        v=summarize(vals); print(name,f"W20={v[0]:.3%}",f"W35={v[1]:.3%}",flush=True)
