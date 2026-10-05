import reinforcement_model as m
import random

def normal_screen(rng,wave,removed,owned,placed,candidates=6):
    pool=m.dynamic_doctrine_pool_fast("Lions",wave,removed=removed,tb_owned=owned,placed_families=placed)
    k=sum(rng.random()<.29 for _ in range(candidates))
    ds=m.sample_doctrines(rng,pool,k)
    slots=ds+[None]*(candidates-len(ds)); rng.shuffle(slots)
    return [slots[i:i+2] for i in range(0,candidates,2)]

def choose(cards,rng,wave,cleanup):
    target=[i for i,c in enumerate(cards) if any(x and x.startswith("TB0D") for x in c)]
    if target:
        best=max(sum(bool(x and x.startswith("TB0D")) for x in cards[i]) for i in target)
        return rng.choice([i for i in target if sum(bool(x and x.startswith("TB0D")) for x in cards[i])==best])
    if cleanup:
        scores=[sum(m.doctrine_weight_at_wave(x,wave) for x in c if x and not x.startswith("TB")) for c in cards]
        best=max(scores); return rng.choice([i for i,v in enumerate(scores) if v==best])
    return rng.randrange(len(cards))

def take(card,owned,removed):
    for x in card:
        if not x: continue
        if x.startswith("TB"): owned.add(x)
        else: removed.add(x)

def magel_draft(rng,wave,removed,owned,placed):
    pool=m.dynamic_doctrine_pool_fast("Lions",wave,removed=removed,tb_owned=owned,placed_families=placed)
    # Same weighted doctrine selector, proposed without replacement: 3 doctrine identities.
    return m.sample_doctrines(rng,pool,3)

def trial(others,mode,seed,cleanup=False):
    rng=random.Random(seed); owned=set(); removed=set(); placed=set(range(others+1))
    for wave in range(1,36):
        candidates=8 if mode=="tander" else 6
        cards=normal_screen(rng,wave,removed,owned,placed,candidates)
        take(cards[choose(cards,rng,wave,cleanup)],owned,removed)
        if "TB0D7" in owned: return wave
        if mode=="magel" and wave%2==0:
            draft=magel_draft(rng,wave,removed,owned,placed)
            target=[x for x in draft if x.startswith("TB0D")]
            if target:
                # Any desired-family node advances the target; choose one at random if >1.
                pick=rng.choice(target)
            elif cleanup:
                pick=max(draft,key=lambda x:m.doctrine_weight_at_wave(x,wave))
            else:
                pick=rng.choice(draft)
            take([pick],owned,removed)
            if "TB0D7" in owned: return wave
    return None

N=5000
for cleanup in (False,True):
 print("cleanup",cleanup,flush=True)
 for others in range(6):
  vals={}
  for mode in ("base","tander","magel"):
   arr=[trial(others,mode,i+others*100000+{"base":1,"tander":2,"magel":3}[mode]*1000000+int(cleanup)*10000000,cleanup) for i in range(N)]
   vals[mode]=(sum(v is not None and v<=20 for v in arr)/N,sum(v is not None for v in arr)/N)
  print(others,*[f"{mode} {vals[mode][0]:.3%}/{vals[mode][1]:.3%}" for mode in ("base","tander","magel")],flush=True)
