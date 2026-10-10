#!/usr/bin/env python3
import UnityPy,struct,re
P="/home/downloads/SteamLibrary/steamapps/common/Tower Dominion/tower-dominion_Data/resources.assets"
env=UnityPy.load(P)
objs={o.path_id:o for o in env.objects}
def name(o):
 try:
  b=o.get_raw_data(); n=struct.unpack_from("<I",b,28)[0]
  return b[32:32+n].decode() if n<200 else "?"
 except: return "?"
targets={25777,26731,26729,26718,26492,26493}
for o in env.objects:
 if o.type.name!="MonoBehaviour":continue
 b=o.get_raw_data()
 refs=[i for i in targets if struct.pack("<q",i) in b]
 if refs:print("REF",o.path_id,name(o),"->",[(i,name(objs[i])) for i in refs])
for i in [25611,25612,25716,25717,25777,26731,26492,26493]:
 b=objs[i].get_raw_data()
 refs=[]
 for off in range(32,len(b)-11,4):
  fileid=struct.unpack_from("<i",b,off)[0]
  target=struct.unpack_from("<q",b,off+4)[0]
  if fileid==0 and target in objs and target!=i:refs.append((off,target,name(objs[target])))
 print("OBJECT",i,name(objs[i]),"REFS",refs[:45])
