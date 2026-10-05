import random, math
from collections import Counter
OUTER=[('supply',10),('recon',4),('bp',57),('doctrine',29)]
Q={'supply':[(100,64),(200,35),(500,1)],'recon':[(25,64),(50,35),(75,1)]}
def pick_weighted(items,rng):
 t=sum(w for _,w in items); x=rng.random()*t
 for v,w in items:
  x-=w
  if x<0:return v
 return items[-1][0]
def doctrine_draw(pool,rng):
 # pool is mutable list [identity,weight]; proposal consumes identity for this screen
 t=sum(w for _,w in pool); x=rng.random()*t
 for i,(v,w) in enumerate(pool):
  x-=w
  if x<0:
   pool.pop(i); return v
 return pool.pop()[0]
def bp_draw(pool,rng): return pick_weighted(pool,rng)
def item(rng,dpool,bpool):
 typ=pick_weighted(OUTER,rng)
 if typ in Q:return (typ,pick_weighted(Q[typ],rng),None,None)
 if typ=='bp':return (typ,1,bp_draw(bpool,rng),None)
 return (typ,1,None,doctrine_draw(dpool,rng))
def same_card(a,b): return sorted(a,key=repr)==sorted(b,key=repr)
def generate(rng,dweights,bweights):
 # faithfully preserve proposed doctrines across regeneration; rollback doctrines on discarded duplicate card
 while True:
  dpool=[[k,w] for k,w in dweights]
  items=[item(rng,dpool,bweights) for _ in range(6)]
  rng.shuffle(items); cards=[items[i:i+2] for i in range(0,6,2)]
  dup=None
  for i in range(len(cards)-1,0,-1):
   for j in range(i):
    if same_card(cards[i],cards[j]): dup=i; break
   if dup is not None: break
  if dup is None:return cards,False
  # approximate game regeneration by restarting entire candidate set; track frequency only.
  # exact local-card regeneration will be implemented after measuring whether correction matters.
  return cards,True
def wave_weights(faction,w,tb_families=0,tb_mult=3):
 counts={'Iron':(39,42,26),'Lions':(38,37,24),'Pargan':(34,38,19)}[faction]
 r2=max(0,-10+2*(w-1)); r3=max(0,-20+2*(w-1))
 pool=[]
 for tier,(n,wt) in enumerate(zip(counts,(100,r2,r3)),1):
  for i in range(n): pool.append((f'T{tier}_{i}',wt))
 # overwrite known deployment identities within counts: one target T1, second target T1; T2 pair
 pool[0]=('ATT_I',100); pool[1]=('AMP_I',100)
 off=counts[0]
 if counts[1]>=2: pool[off]=('ATT_II',r2); pool[off+1]=('AMP_II',r2)
 pool=[x for x in pool if x[1]>0]
 for f in range(tb_families):
  pool += [(f'TB{f}A',100*tb_mult),(f'TB{f}B',100*tb_mult)]
 return pool
if __name__=='__main__':
 rng=random.Random(123456); bp=[(f'BP{i}',1) for i in range(11)] # W1 faction pool T1 count for Iron/Pargan; duplicate rate sensitivity small
 N=300000; dup=0; hist=Counter(); hit=Counter()
 for _ in range(N):
  cards,isdup=generate(rng,wave_weights('Lions',1),bp); dup+=isdup
  ds=[x[3] for c in cards for x in c if x[0]=='doctrine']; hist[len(ds)]+=1
  hit['amp']+=('AMP_I' in ds); hit['either']+=bool({'AMP_I','ATT_I'}&set(ds))
 print('N',N,'duplicate_initial_cardsets',dup,dup/N)
 print('doctrine_hist',{k:hist[k]/N for k in range(7)})
 print('amp',hit['amp']/N,'either',hit['either']/N)

def sample_doctrines(rng,pool,k):
    pool=list(pool); out=[]; total=sum(w for _,w in pool)
    for _ in range(min(k,len(pool))):
        x=rng.random()*total
        for i,(name,w) in enumerate(pool):
            x-=w
            if x<0:
                out.append(name); total-=w; pool.pop(i); break
    return out

def simulate_target_offer(faction,w,target_names,tb_families=0,tb_mult=3,n=100000,seed=1,removed=()):
    rng=random.Random(seed); pool=[x for x in wave_weights(faction,w,tb_families,tb_mult) if x[0] not in set(removed)]
    targets=set(target_names); hits=0
    for _ in range(n):
        k=sum(rng.random()<.29 for _ in range(6))
        if targets.intersection(sample_doctrines(rng,pool,k)): hits+=1
    return hits/n

def deployment_targets(w):
    x=['AMP_I','ATT_I']
    if w>=7:x += ['AMP_II','ATT_II']
    return x

def removal_snapshot(faction,w,remove_t1=0,remove_t2=0,remove_t3=0,tb_families=0,tb_mult=3):
    pool=wave_weights(faction,w,tb_families,tb_mult); protected={'AMP_I','ATT_I','AMP_II','ATT_II'}; removed=[]
    quotas={1:remove_t1,2:remove_t2,3:remove_t3}
    for tier in (1,2,3):
        prefix=f'T{tier}_'
        for name,wt in pool:
            if quotas[tier]<=0: break
            if name.startswith(prefix) and name not in protected:
                removed.append(name); quotas[tier]-=1
    return removed

# Current-build TB-family classification. A placed type outside TB_FAMILIES does not
# admit the standard seven-node building-doctrine chain.
TB_FAMILIES = frozenset([
 'CB01','CB02','CB03','CB04','CB05','CB06','CB07','CB08','CB09','CB10','CB11',
 'CB13','CB14','CB15','CB16','CB17','CB18','CB19','CB20','CB21','F101'
])
DOCTRINE_FREE_BUNDLE_BUILDINGS = {
 'CB12':3, 'F102':2, 'F201':3, 'F202':3, 'F301':2, 'F302':1,
 'SB01':2, 'SB02':3, 'SB04':3, 'SB06':1, 'SB07':3,
}

def admits_tb_family(tower_type):
    return tower_type in TB_FAMILIES

def doctrine_screen(rng, faction, wave, removed=(), tb_families=0, tb_mult=3, card_count=3):
    """Doctrine identities on a normal reinforcement, grouped into 2-item cards.
    Baseline is 3 cards; Tander uses 4. Doctrine proposals are unique."""
    pool=[x for x in wave_weights(faction,wave,tb_families,tb_mult) if x[0] not in set(removed)]
    candidates=card_count*2
    k=sum(rng.random()<.29 for _ in range(candidates))
    doctrines=sample_doctrines(rng,pool,k)
    slots=doctrines+[None]*(candidates-len(doctrines))
    rng.shuffle(slots)
    return [slots[i:i+2] for i in range(0,candidates,2)]

def choose_doctrine_card(cards, policy, rng, targets=()):
    """Return doctrine(s) permanently removed by choosing one card.
    This isolates doctrine-cleaning preference from the value of non-doctrine rewards."""
    targets=set(targets)
    scored=[]
    for i,c in enumerate(cards):
        ds=[x for x in c if x is not None]
        target=sum(x in targets for x in ds)
        ordinary=sum(x not in targets and not x.startswith('TB') for x in ds)
        tb=sum(x.startswith('TB') for x in ds)
        if policy=='aggressive':
            score=(target, ordinary, len(ds), -tb)
        elif policy=='moderate':
            score=(target, ordinary>0, len(ds), -tb)
        elif policy=='none':
            score=(target, 0, 0, 0)
        else: raise ValueError(policy)
        scored.append((score,i))
    best=max(x[0] for x in scored)
    choices=[i for s,i in scored if s==best]
    chosen=rng.choice(choices)
    return [x for x in cards[chosen] if x is not None], chosen

def run_doctrine_policy(faction='Lions', waves=35, policy='aggressive',
                        family_schedule=None, tb_multiplier_schedule=None, seed=1):
    """Sequential doctrine-only policy experiment.
    family_schedule(w)->active doctrine-bearing families.
    tb_multiplier_schedule(w)->current TB multiplier."""
    rng=random.Random(seed); removed=set(); first_target=None; history=[]
    family_schedule=family_schedule or (lambda w: 1)
    tb_multiplier_schedule=tb_multiplier_schedule or (lambda w: 3)
    for w in range(1,waves+1):
        fam=family_schedule(w); mult=tb_multiplier_schedule(w)
        cards=doctrine_screen(rng,faction,w,removed,fam,mult)
        targets=[x for x in deployment_targets(w) if x not in removed]
        taken,_=choose_doctrine_card(cards,policy,rng,targets)
        target_taken=[x for x in taken if x in targets]
        if target_taken and first_target is None:first_target=w
        removed.update(taken)
        history.append((w,fam,mult,cards,taken,len(removed)))
    return {'first_target_wave':first_target,'removed':removed,'history':history}

def policy_monte_carlo(n=10000, **kwargs):
    hits=0; first=[]; removed=[]
    for seed in range(n):
        r=run_doctrine_policy(seed=seed,**kwargs)
        if r['first_target_wave'] is not None:
            hits+=1; first.append(r['first_target_wave'])
        removed.append(len(r['removed']))
    return {'acquired_by_end':hits/n,
            'mean_first_wave':sum(first)/len(first) if first else None,
            'mean_removed':sum(removed)/n}

# Cache immutable base pools used by sequential experiments.
_WAVE_POOL_CACHE={}
def cached_wave_weights(faction,w,tb_families=0,tb_mult=3):
    key=(faction,w,tb_families,tb_mult)
    if key not in _WAVE_POOL_CACHE:
        _WAVE_POOL_CACHE[key]=tuple(wave_weights(*key))
    return _WAVE_POOL_CACHE[key]

def doctrine_screen_fast(rng, faction, wave, removed=(), tb_families=0, tb_mult=3):
    rem=removed if isinstance(removed,set) else set(removed)
    pool=[x for x in cached_wave_weights(faction,wave,tb_families,tb_mult) if x[0] not in rem]
    k=sum(rng.random()<.29 for _ in range(6))
    doctrines=sample_doctrines(rng,pool,k)
    slots=doctrines+[None]*(6-len(doctrines)); rng.shuffle(slots)
    return [slots[0:2],slots[2:4],slots[4:6]]

def run_doctrine_policy_fast(faction='Lions',waves=35,policy='aggressive',
                             family_schedule=None,tb_multiplier_schedule=None,seed=1):
    rng=random.Random(seed); removed=set(); first_target=None; checkpoints={}
    family_schedule=family_schedule or (lambda w:1)
    tb_multiplier_schedule=tb_multiplier_schedule or (lambda w:3)
    for w in range(1,waves+1):
        fam=family_schedule(w); mult=tb_multiplier_schedule(w)
        cards=doctrine_screen_fast(rng,faction,w,removed,fam,mult)
        targets=[x for x in deployment_targets(w) if x not in removed]
        taken,_=choose_doctrine_card(cards,policy,rng,targets)
        target_taken=[x for x in taken if x in targets]
        if target_taken and first_target is None:first_target=w
        removed.update(taken)
        if w in (5,7,10,15,20,25,35):
            checkpoints[w]=(first_target is not None,len(removed))
    return first_target,len(removed),checkpoints

def policy_monte_carlo_fast(n=10000,**kwargs):
    first=[]; removed=[]; cp={w:0 for w in (5,7,10,15,20,25,35)}
    for seed in range(n):
        fw,nrem,cps=run_doctrine_policy_fast(seed=seed,**kwargs)
        if fw is not None:first.append(fw)
        removed.append(nrem)
        for w,(hit,_) in cps.items(): cp[w]+=hit
    return {'acquired_by_end':len(first)/n,
            'mean_first_wave':sum(first)/len(first) if first else None,
            'mean_removed':sum(removed)/n,
            'checkpoints':{w:v/n for w,v in cp.items()}}

def doctrine_tier(name):
    if name in ('AMP_I','ATT_I') or name.startswith('T1_'): return 1
    if name in ('AMP_II','ATT_II') or name.startswith('T2_'): return 2
    if name.startswith('T3_'): return 3
    return 0

def doctrine_weight_at_wave(name,w,tb_mult=3):
    tier=doctrine_tier(name)
    if tier==1:return 100
    if tier==2:return max(0,-10+2*(w-1))
    if tier==3:return max(0,-20+2*(w-1))
    if name.startswith('TB'):return 100*tb_mult
    return 0

def choose_doctrine_card_v2(cards,policy,rng,targets=(),wave=1,tb_mult=3):
    targets=set(targets)
    if any(any(x in targets for x in c if x) for c in cards):
        cand=[i for i,c in enumerate(cards) if any(x in targets for x in c if x)]
        return [x for x in cards[rng.choice(cand)] if x],cand
    ordinary_weight=[]
    for i,c in enumerate(cards):
        wt=sum(doctrine_weight_at_wave(x,wave,tb_mult) for x in c if x and not x.startswith('TB'))
        ordinary_weight.append((wt,i))
    if policy=='aggressive':
        best=max(w for w,_ in ordinary_weight)
        cand=[i for w,i in ordinary_weight if w==best]
    elif policy=='moderate':
        # Value pool cleanup, but only prioritize it on roughly half of otherwise
        # target-free decisions. Remaining choices represent immediate reward utility.
        if rng.random()<0.5 and max(w for w,_ in ordinary_weight)>0:
            best=max(w for w,_ in ordinary_weight); cand=[i for w,i in ordinary_weight if w==best]
        else:cand=list(range(3))
    elif policy=='none':
        cand=list(range(3))
    else:raise ValueError(policy)
    i=rng.choice(cand)
    return [x for x in cards[i] if x],cand

def run_doctrine_policy_v2(faction='Lions',waves=35,policy='aggressive',
                           family_schedule=None,tb_multiplier_schedule=None,seed=1):
    rng=random.Random(seed); removed=set(); first_target=None; removed_weight=0; checkpoints={}
    family_schedule=family_schedule or (lambda w:1); tb_multiplier_schedule=tb_multiplier_schedule or (lambda w:3)
    for w in range(1,waves+1):
        fam=family_schedule(w); mult=tb_multiplier_schedule(w)
        cards=doctrine_screen_fast(rng,faction,w,removed,fam,mult)
        targets=[x for x in deployment_targets(w) if x not in removed]
        taken,_=choose_doctrine_card_v2(cards,policy,rng,targets,w,mult)
        if first_target is None and any(x in targets for x in taken):first_target=w
        for x in taken:
            if x not in removed and not x.startswith('TB'): removed_weight += doctrine_weight_at_wave(x,w,mult)
        removed.update(taken)
        if w in (5,7,10,15,20,25,35):checkpoints[w]=(first_target is not None,len(removed),removed_weight)
    return first_target,len(removed),removed_weight,checkpoints

def policy_monte_carlo_v2(n=10000,**kwargs):
    first=[]; nrem=[]; rw=[]; cp={w:0 for w in (5,7,10,15,20,25,35)}
    for seed in range(n):
        fw,nr,weight,cps=run_doctrine_policy_v2(seed=seed,**kwargs)
        if fw is not None:first.append(fw)
        nrem.append(nr); rw.append(weight)
        for w,(hit,_,_) in cps.items():cp[w]+=hit
    return {'acquired_by_end':len(first)/n,'mean_first_wave':sum(first)/len(first) if first else None,
            'mean_removed':sum(nrem)/n,'mean_removed_weight':sum(rw)/n,
            'checkpoints':{w:v/n for w,v in cp.items()}}

def full_screen(rng,faction,wave,removed=(),tb_families=0,tb_mult=3,bp_count=28):
    """Generate six typed candidates and group 3x2, preserving concrete doctrines.
    Blueprint identities are placeholders here because this experiment values access,
    not a particular building."""
    rem=removed if isinstance(removed,set) else set(removed)
    dpool=[list(x) for x in cached_wave_weights(faction,wave,tb_families,tb_mult) if x[0] not in rem]
    bpool=[(f'BP{i}',1) for i in range(bp_count)]
    out=[]
    for _ in range(6):
        typ=pick_weighted(OUTER,rng)
        if typ=='doctrine':
            out.append(('doctrine',doctrine_draw(dpool,rng)))
        elif typ=='bp':
            out.append(('bp',bp_draw(bpool,rng)))
        else:
            out.append((typ,pick_weighted(Q[typ],rng)))
    rng.shuffle(out)
    return [out[0:2],out[2:4],out[4:6]]

def immediate_item_utility(item,bp_value=1.0,supply_per_unit=1/139,recon_per_unit=1/34.25,
                           ordinary_doctrine_value=0.0,tb_doctrine_value=0.0):
    typ,val=item
    if typ=='bp':return bp_value
    if typ=='supply':return val*supply_per_unit
    if typ=='recon':return val*recon_per_unit
    if typ=='doctrine':
        return tb_doctrine_value if val.startswith('TB') else ordinary_doctrine_value
    return 0.0

def choose_card_utility(cards,rng,targets=(),wave=1,tb_mult=3,cleanup_bonus=0.0,**utility):
    targets=set(targets); scores=[]
    for i,c in enumerate(cards):
        score=sum(immediate_item_utility(x,**utility) for x in c)
        for typ,val in c:
            if typ=='doctrine':
                if val in targets: score += 1000000 # hunting target dominates experiment
                elif not val.startswith('TB'):
                    # normalize cleanup by T1=1 unit; later low-weight tiers contribute less.
                    score += cleanup_bonus*doctrine_weight_at_wave(val,wave,tb_mult)/100
        scores.append((score,i))
    best=max(x[0] for x in scores); cand=[i for s,i in scores if abs(s-best)<1e-12]
    i=rng.choice(cand); return i,scores

def run_utility_policy(faction='Lions',waves=20,cleanup_bonus=0.0,family_schedule=None,
                       tb_multiplier_schedule=None,seed=1,**utility):
    rng=random.Random(seed); removed=set(); first=None; removed_weight=0
    family_schedule=family_schedule or (lambda w:1); tb_multiplier_schedule=tb_multiplier_schedule or (lambda w:3)
    cps={}
    for w in range(1,waves+1):
        fam=family_schedule(w); mult=tb_multiplier_schedule(w)
        cards=full_screen(rng,faction,w,removed,fam,mult)
        targets=[x for x in deployment_targets(w) if x not in removed]
        idx,_=choose_card_utility(cards,rng,targets,w,mult,cleanup_bonus,**utility)
        taken=[v for typ,v in cards[idx] if typ=='doctrine']
        if first is None and any(x in targets for x in taken):first=w
        for x in taken:
            if x not in removed and not x.startswith('TB'):removed_weight+=doctrine_weight_at_wave(x,w,mult)
        removed.update(taken)
        if w in (5,7,10,15,20):cps[w]=(first is not None,len(removed),removed_weight)
    return first,len(removed),removed_weight,cps

def utility_monte_carlo(n=1000,**kwargs):
    first=[]; rw=[]; cp={w:0 for w in (5,7,10,15,20)}
    for seed in range(n):
        fw,nr,weight,cps=run_utility_policy(seed=seed,**kwargs)
        if fw is not None:first.append(fw)
        rw.append(weight)
        for w,(hit,_,_) in cps.items():cp[w]+=hit
    return {'checkpoints':{w:v/n for w,v in cp.items()},'mean_removed_weight':sum(rw)/n,
            'mean_first_wave':sum(first)/len(first) if first else None}

# Faithful standard TB-family progression. Each family has two three-node branches;
# D7 becomes eligible when either branch is complete. Owned predecessors advance the
# active progression node instead of simply deleting TB weight from the pool.
def tb_active_nodes(family,owned,placed=True):
    p=f'TB{family}D'
    active=[]
    # D1/D4 are placement-gated. Once a branch is started, successors are
    # gated by owned predecessors and persist if the building is removed.
    # cost branch D1->D2->D3
    if p+'1' not in owned:
        if placed: active.append(p+'1')
    elif p+'2' not in owned: active.append(p+'2')
    elif p+'3' not in owned: active.append(p+'3')
    # efficiency branch D4->D5->D6
    if p+'4' not in owned:
        if placed: active.append(p+'4')
    elif p+'5' not in owned: active.append(p+'5')
    elif p+'6' not in owned: active.append(p+'6')
    # OR prerequisite: D3 or D6
    if (p+'3' in owned or p+'6' in owned) and p+'7' not in owned:
        active.append(p+'7')
    return active

def dynamic_doctrine_pool(faction,wave,removed=(),family_count=0,tb_owned=(),tb_mult=3):
    # ordinary portion only from base wave pool
    pool=[x for x in wave_weights(faction,wave,0,tb_mult) if x[0] not in set(removed)]
    owned=set(tb_owned)
    for f in range(family_count):
        pool.extend((name,100*tb_mult) for name in tb_active_nodes(f,owned))
    return pool

def dynamic_doctrine_screen(rng,faction,wave,removed=(),family_count=0,tb_owned=(),tb_mult=3):
    pool=dynamic_doctrine_pool(faction,wave,removed,family_count,tb_owned,tb_mult)
    k=sum(rng.random()<.29 for _ in range(6))
    doctrines=sample_doctrines(rng,pool,k)
    slots=doctrines+[None]*(6-len(doctrines)); rng.shuffle(slots)
    return [slots[i:i+2] for i in range(0,6,2)]

def run_dynamic_policy(faction='Lions',waves=35,policy='aggressive',family_schedule=None,seed=1):
    rng=random.Random(seed); removed=set(); tb_owned=set(); first=None; cps={}
    family_schedule=family_schedule or (lambda w:1)
    for w in range(1,waves+1):
        fam=family_schedule(w)
        cards=dynamic_doctrine_screen(rng,faction,w,removed,fam,tb_owned,3)
        targets=[x for x in deployment_targets(w) if x not in removed]
        taken,_=choose_doctrine_card_v2(cards,policy,rng,targets,w,3)
        if first is None and any(x in targets for x in taken): first=w
        for x in taken:
            if x.startswith('TB'):tb_owned.add(x)
            else:removed.add(x)
        if w in (5,7,10,15,20,25,35):
            active=sum(len(tb_active_nodes(f,tb_owned)) for f in range(fam))
            cps[w]=(first is not None,len(removed),len(tb_owned),active)
    return first,removed,tb_owned,cps

def dynamic_monte_carlo(n=1000,**kwargs):
    cp={w:0 for w in (5,7,10,15,20,25,35)}; tb=[]; ordinary=[]
    for seed in range(n):
        first,rem,tbo,cps=run_dynamic_policy(seed=seed,**kwargs)
        tb.append(len(tbo)); ordinary.append(len(rem))
        for w,(hit,_,_,_) in cps.items():cp[w]+=hit
    return {'checkpoints':{w:v/n for w,v in cp.items()},
            'mean_tb_taken':sum(tb)/n,'mean_ordinary_removed':sum(ordinary)/n}

_ORDINARY_CACHE={}
def cached_ordinary_pool(faction,wave):
    key=(faction,wave)
    if key not in _ORDINARY_CACHE:_ORDINARY_CACHE[key]=tuple(wave_weights(faction,wave,0,3))
    return _ORDINARY_CACHE[key]

def dynamic_doctrine_pool_fast(faction,wave,removed=(),family_count=0,tb_owned=(),tb_mult=3,placed_families=None):
    rem=removed if isinstance(removed,set) else set(removed)
    pool=[x for x in cached_ordinary_pool(faction,wave) if x[0] not in rem]
    owned=tb_owned if isinstance(tb_owned,set) else set(tb_owned)
    wt=100*tb_mult
    # Legacy family_count means families 0..N-1 are currently placed.
    # Explicit placed_families also keeps progressed-but-removed families in
    # consideration, because owned successors can remain eligible after removal.
    if placed_families is None:
        placed=set(range(family_count))
        families=set(placed)
    else:
        placed=set(placed_families)
        families=set(placed)
        for name in owned:
            if name.startswith('TB') and 'D' in name:
                try: families.add(int(name[2:name.index('D')]))
                except ValueError: pass
    for f in sorted(families):
        pool.extend((name,wt) for name in tb_active_nodes(f,owned,f in placed))
    return pool

# Route dynamic screen through cached ordinary pool.
COMMANDER_REINFORCEMENT_RULES = {
    'standard': {'card_count':3, 'doctrine_draft_size':0, 'doctrine_draft_cadence':0},
    'tander':   {'card_count':4, 'doctrine_draft_size':0, 'doctrine_draft_cadence':0},
    'magel':    {'card_count':3, 'doctrine_draft_size':3, 'doctrine_draft_cadence':2},
}

def dynamic_doctrine_screen(rng,faction,wave,removed=(),family_count=0,tb_owned=(),tb_mult=3,placed_families=None,card_count=3):
    pool=dynamic_doctrine_pool_fast(faction,wave,removed,family_count,tb_owned,tb_mult,placed_families)
    candidates=card_count*2
    k=sum(rng.random()<.29 for _ in range(candidates))
    doctrines=sample_doctrines(rng,pool,k)
    slots=doctrines+[None]*(candidates-len(doctrines)); rng.shuffle(slots)
    return [slots[i:i+2] for i in range(0,candidates,2)]

def magel_doctrine_draft(rng,faction,wave,removed=(),family_count=0,tb_owned=(),tb_mult=3,placed_families=None):
    """Magel's separate every-other-wave choose-1-among-3 Doctrine draft.
    It samples the same current eligible weighted Doctrine pool without replacement."""
    pool=dynamic_doctrine_pool_fast(faction,wave,removed,family_count,tb_owned,tb_mult,placed_families)
    return sample_doctrines(rng,pool,COMMANDER_REINFORCEMENT_RULES['magel']['doctrine_draft_size'])

def magel_draft_due(wave):
    cadence=COMMANDER_REINFORCEMENT_RULES['magel']['doctrine_draft_cadence']
    return cadence>0 and wave%cadence==0

def run_commander_dynamic_policy(faction='Lions',waves=35,commander='standard',policy='aggressive',family_schedule=None,seed=1):
    """Sequential Doctrine model with commander-specific reinforcement mechanics.
    Magel's separate draft is generated after the normal reward updates same-wave state."""
    if commander not in COMMANDER_REINFORCEMENT_RULES: raise ValueError(commander)
    rng=random.Random(seed); removed=set(); tb_owned=set(); history=[]
    family_schedule=family_schedule or (lambda w:1)
    rules=COMMANDER_REINFORCEMENT_RULES[commander]
    for w in range(1,waves+1):
        fam=family_schedule(w); placed=set(range(fam))
        cards=dynamic_doctrine_screen(rng,faction,w,removed,tb_owned=tb_owned,placed_families=placed,card_count=rules['card_count'])
        targets=[x for x in deployment_targets(w) if x not in removed]
        taken,_=choose_doctrine_card_v2(cards,policy,rng,targets,w,3)
        for x in taken:
            (tb_owned if x.startswith('TB') else removed).add(x)
        special=[]; special_taken=None
        if commander=='magel' and magel_draft_due(w):
            special=magel_doctrine_draft(rng,faction,w,removed,tb_owned=tb_owned,placed_families=placed)
            # Doctrine-focused policy: desired family first; otherwise ordinary cleanup if requested.
            desired=[x for x in special if x.startswith('TB0D')]
            if desired: special_taken=rng.choice(desired)
            elif policy=='aggressive': special_taken=max(special,key=lambda x:doctrine_weight_at_wave(x,w,3)) if special else None
            elif special: special_taken=rng.choice(special)
            if special_taken:
                (tb_owned if special_taken.startswith('TB') else removed).add(special_taken)
        history.append((w,cards,taken,special,special_taken,set(tb_owned),set(removed)))
    return {'tb_owned':tb_owned,'removed':removed,'history':history}

def doctrine_pool_snapshot(faction,wave,removed=(),tb_owned=(),tb_mult=3,placed_families=None,desired_family=0):
    """Exact ticket composition of the currently eligible Doctrine lottery.
    Raw weight is retained; tickets are raw/100 for player-facing interpretation."""
    pool=dynamic_doctrine_pool_fast(faction,wave,removed,tb_owned=tb_owned,tb_mult=tb_mult,placed_families=placed_families or set())
    desired_prefix=f'TB{desired_family}D'
    ordinary=sum(w for n,w in pool if not n.startswith('TB'))
    desired=sum(w for n,w in pool if n.startswith(desired_prefix))
    competing=sum(w for n,w in pool if n.startswith('TB') and not n.startswith(desired_prefix))
    total=ordinary+desired+competing
    return {'wave':wave,'ordinary_raw':ordinary,'desired_tb_raw':desired,'competing_tb_raw':competing,'total_raw':total,
            'ordinary_tickets':ordinary/100,'desired_tb_tickets':desired/100,'competing_tb_tickets':competing/100,'total_tickets':total/100,
            'desired_per_doctrine_draw':desired/total if total else 0,
            'eligible_count':len(pool),'pool':tuple(pool)}

def commander_wave_opportunities(commander,wave):
    """Category-level Doctrine opportunity structure before pool identity sampling."""
    rules=COMMANDER_REINFORCEMENT_RULES[commander]
    n=rules['card_count']*2
    extra=rules['doctrine_draft_size'] if commander=='magel' and magel_draft_due(wave) else 0
    return {'normal_candidates':n,'expected_normal_doctrine_candidates':n*.29,
            'p_at_least_one_normal_doctrine':1-(1-.29)**n,
            'guaranteed_special_doctrine_candidates':extra,
            'expected_total_doctrine_candidates':n*.29+extra}

def wave_state(faction,wave,commander='standard',removed=(),tb_owned=(),tb_mult=3,placed_families=None,desired_family=0):
    return {'pool':doctrine_pool_snapshot(faction,wave,removed,tb_owned,tb_mult,placed_families,desired_family),
            'opportunities':commander_wave_opportunities(commander,wave)}
