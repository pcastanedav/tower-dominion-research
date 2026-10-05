import random, math
p=.29
for n in (6,8):
    probs=[]
    for k in range(n+1):
        q=math.comb(n,k)*p**k*(1-p)**(n-k)
        probs.append(q)
    print("candidates",n,"E",n*p,"P>=1",1-probs[0],"P>=2",1-probs[0]-probs[1])
    print(" ".join(f"{k}:{100*q:.4f}%" for k,q in enumerate(probs)))
