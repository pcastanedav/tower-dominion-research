import reinforcement_model as m, random

def run(others,seed,waves=35):
    rng=random.Random(seed); owned=set(); removed=set()
    placed=set(range(others+1))
    for wave in range(1,waves+1):
        cards=m.dynamic_doctrine_screen(rng,'Lions',wave,removed=removed,tb_owned=owned,placed_families=placed)
        target_cards=[i for i,c in enumerate(cards) if any(x and x.startswith('TB0D') for x in c)]
        if target_cards:
            mx=max(sum(bool(x and x.startswith('TB0D')) for x in cards[i]) for i in target_cards)
            cand=[i for i in target_cards if sum(bool(x and x.startswith('TB0D')) for x in cards[i])==mx]
            i=rng.choice(cand)
        else:
            scores=[(sum(m.doctrine_weight_at_wave(x,wave) for x in c if x and not x.startswith('TB')),i) for i,c in enumerate(cards)]
            mx=max(x for x,_ in scores); cand=[i for x,i in scores if x==mx]; i=rng.choice(cand)
        for x in cards[i]:
            if not x: continue
            if x.startswith('TB'): owned.add(x)
            else: removed.add(x)
        if 'TB0D7' in owned: return wave
    return None

N=3000
for others in range(6):
    vals=[run(others,100000*others+i) for i in range(N)]
    hit=[x for x in vals if x is not None]
    print(others,'by35',f'{len(hit)/N:.2%}','mean_if_hit',f'{sum(hit)/len(hit):.2f}' if hit else '-','by20',f'{sum(x is not None and x<=20 for x in vals)/N:.2%}',flush=True)
