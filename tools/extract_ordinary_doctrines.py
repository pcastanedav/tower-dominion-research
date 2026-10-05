#!/usr/bin/env python3
"""Extract ordinary D1/D2/D3 doctrine availability/effect links from resources.assets."""
import argparse, json, re, struct
from pathlib import Path
import UnityPy

PATTERN = re.compile(r"D[123]_\d\d")

def u32(b,o): return struct.unpack_from("<I",b,o)[0]
def i64(b,o): return struct.unpack_from("<q",b,o)[0]
def astr(b,o):
    n=u32(b,o)
    if n > 4096 or o+4+n > len(b): raise ValueError((o,n,len(b)))
    return b[o+4:o+4+n].decode("utf-8","replace"), (o+4+n+3)&~3

def obj_name(obj):
    try: return astr(obj.get_raw_data(),28)[0]
    except Exception: return None

def restriction(b,o):
    typ=u32(b,o); reverse=bool(b[o+4]); o+=8
    skill,o=astr(b,o); faction,o=astr(b,o); tower,o=astr(b,o)
    return {"type":typ,"reverse":reverse,"skill":skill,"faction":faction,"tower":tower},o

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("resources_assets")
    ap.add_argument("-o","--output")
    args=ap.parse_args()
    env=UnityPy.load(args.resources_assets)
    objects={o.path_id:o for o in env.objects}
    rows=[]
    for obj in env.objects:
        if obj.type.name!="MonoBehaviour": continue
        b=obj.get_raw_data()
        try: name,o=astr(b,28)
        except Exception: continue
        if not PATTERN.fullmatch(name): continue
        o+=4; guid,o=astr(b,o); o+=4
        skill_type=u32(b,o); copies=u32(b,o+4); n_effects=u32(b,o+8); o+=12
        effects=[]
        for _ in range(n_effects):
            file_id=u32(b,o); path_id=i64(b,o+4); o+=12
            effects.append({"file_id":file_id,"path_id":path_id,"name":obj_name(objects.get(path_id)) if path_id in objects else None})
        rarity=u32(b,o); available=bool(b[o+4]); expert_cost=u32(b,o+8); o+=12
        n_and=u32(b,o); o+=4; ands=[]
        for _ in range(n_and):
            r,o=restriction(b,o); ands.append(r)
        n_or=u32(b,o); o+=4; ors=[]
        for _ in range(n_or):
            r,o=restriction(b,o); ors.append(r)
        rows.append({"code":name,"path_id":obj.path_id,"guid":guid,"skill_type":skill_type,
                     "copy_allowed":copies,"rarity_index":rarity,"available_in_bundles":available,
                     "expert_cost":expert_cost,"effects":effects,"restrictions_and":ands,"restrictions_or":ors})
    rows.sort(key=lambda x:x["code"])
    out=json.dumps(rows,indent=2)
    if args.output: Path(args.output).write_text(out+"\n")
    else: print(out)

if __name__=="__main__": main()
