import reinforcement_model as m, random

def run(others,seed,cleanup,waves=35):
    rng=random.Random(seed); owned=set(); removed=set(); placed=set(range(others+1))
    for wave in range(1,waves+1):
        cards=m.dynamic_doctrine_screen(rng,'Lions',wave,removed=removed,tb_owned=owned,placed_families=placed)
        tc=[i for i,c in enumerate(cards) if any(x and x.startswith('TB0D') for x in c)]
        if tc:
            mx=max(sum(bool(x and x.startswith('TB0D')) for x in cards[i]) for i in tc)
            cand=[i for i in tc if sum(bool(x and x.startswith('TB0D')) for x in cards[i])==mx]; i=rng.choice(cand)
        elif cleanup:
            scores=[(sum(m.doctrine_weight_at_wave(x,wave) for x in c if x and not x.startswith('TB')),i) for i,c in enumerate(cards)]
            mx=max(v for v,_ in scores); i=rng.choice([i for v,i in scores if v==mx])
        else:
            i=rng.randrange(len(cards))
        for x in cards[i]:
            if not x: continue
            if x.startswith('TB'): owned.add(x)
            else: removed.add(x)
        if 'TB0D7' in owned:return wave
    return None

N=5000
for cleanup in (False,True):
    print('CLEANUP',cleanup)
    for others in range(6):
        vals=[run(others,1000000*int(cleanup)+100000*others+i,cleanup) for i in range(N)]
        print(others,
              f'W20={sum(x is not None and x<=20 for x in vals)/N:.3%}',
              f'W35={sum(x is not None for x in vals)/N:.3%}')
