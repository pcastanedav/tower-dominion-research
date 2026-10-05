import reinforcement_model as m
import random

def screen(rng,wave,removed,owned,placed,candidates):
    pool=m.dynamic_doctrine_pool_fast("Lions",wave,removed=removed,tb_owned=owned,placed_families=placed)
    k=sum(rng.random()<.29 for _ in range(candidates))
    doctrines=m.sample_doctrines(rng,pool,k)
    slots=doctrines+[None]*(candidates-len(doctrines))
    rng.shuffle(slots)
    return [slots[i:i+2] for i in range(0,candidates,2)]

def trial(others,candidates,seed,cleanup=False):
    rng=random.Random(seed); owned=set(); removed=set(); placed=set(range(others+1))
    for wave in range(1,36):
        cards=screen(rng,wave,removed,owned,placed,candidates)
        target=[i for i,c in enumerate(cards) if any(x and x.startswith("TB0D") for x in c)]
        if target:
            best=max(sum(bool(x and x.startswith("TB0D")) for x in cards[i]) for i in target)
            choice=rng.choice([i for i in target if sum(bool(x and x.startswith("TB0D")) for x in cards[i])==best])
        elif cleanup:
            scores=[]
            for i,c in enumerate(cards):
                score=sum(m.doctrine_weight_at_wave(x,wave) for x in c if x and not x.startswith("TB"))
                scores.append((score,i))
            best=max(v for v,i in scores)
            choice=rng.choice([i for v,i in scores if v==best])
        else:
            choice=rng.randrange(len(cards))
        for x in cards[choice]:
            if not x: continue
            if x.startswith("TB"): owned.add(x)
            else: removed.add(x)
        if "TB0D7" in owned:return wave
    return None

N=5000
for cleanup in (False,True):
    print("cleanup",cleanup,flush=True)
    for others in range(6):
        line=[]
        for candidates in (6,8):
            vals=[trial(others,candidates,seed+others*100000+candidates*1000000+int(cleanup)*10000000,cleanup) for seed in range(N)]
            w20=sum(v is not None and v<=20 for v in vals)/N
            w35=sum(v is not None for v in vals)/N
            line.append((w20,w35))
        b,t=line
        print(others,
              "base",f"{b[0]:.3%}",f"{b[1]:.3%}",
              "tander",f"{t[0]:.3%}",f"{t[1]:.3%}",
              "gain_pp",f"{(t[0]-b[0])*100:.2f}",f"{(t[1]-b[1])*100:.2f}",
              flush=True)
