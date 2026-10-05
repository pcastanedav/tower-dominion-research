import reinforcement_model as m
import random

schedules = {
    "desired_only": [],
    "one_early": [1],
    "one_late": [10],
    "two_early": [1,4],
    "two_late": [10,15],
    "three_early": [1,4,9],
    "three_late": [10,15,20],
}

def trial(starts, seed):
    rng = random.Random(seed)
    owned = set()
    removed = set()
    for wave in range(1,36):
        placed = {0}
        for j,start in enumerate(starts,1):
            if wave >= start:
                placed.add(j)
        cards = m.dynamic_doctrine_screen(rng,"Lions",wave,removed=removed,tb_owned=owned,placed_families=placed)
        target = [i for i,c in enumerate(cards) if any(x and x.startswith("TB0D") for x in c)]
        if target:
            best = max(sum(bool(x and x.startswith("TB0D")) for x in cards[i]) for i in target)
            choices = [i for i in target if sum(bool(x and x.startswith("TB0D")) for x in cards[i]) == best]
            choice = rng.choice(choices)
        else:
            choice = rng.randrange(len(cards))
        for x in cards[choice]:
            if not x:
                continue
            if x.startswith("TB"):
                owned.add(x)
            else:
                removed.add(x)
        if "TB0D7" in owned:
            return wave
    return None

N=3000
for name,starts in schedules.items():
    vals=[trial(starts,i) for i in range(N)]
    w20=sum(v is not None and v<=20 for v in vals)/N
    w35=sum(v is not None for v in vals)/N
    print(name, "W20", round(w20,4), "W35", round(w35,4), flush=True)
