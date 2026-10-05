base20=[30.480,21.700,16.680,12.220,9.460,8.000]
base35=[69.960,58.920,49.620,41.600,35.360,29.360]
tan20 =[50.840,40.940,31.720,26.600,20.020,16.900]
tan35 =[87.380,80.580,72.580,65.940,57.820,51.740]
for f in range(6):
    # largest extra family count whose Tander result still meets/exceeds baseline at f=0
    eq20=max([j for j,x in enumerate(tan20) if x>=base20[0]],default=None)
    eq35=max([j for j,x in enumerate(tan35) if x>=base35[0]],default=None)
print("Tander families still >= baseline 0-family: W20",eq20,"W35",eq35)
for f in range(6):
 print(f,"Tander minus same-family baseline pp:",round(tan20[f]-base20[f],2),round(tan35[f]-base35[f],2))
