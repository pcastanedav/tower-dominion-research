import math
rows=[
("one",.226,.2537,.5843,.6187),
("two",.1697,.2417,.5303,.5913),
("three",.1533,.236,.4483,.5383),
]
for name,e20,l20,e35,l35 in rows:
 print(name,
       "W20_pp",round((l20-e20)*100,2),
       "W20_rel",round((l20/e20-1)*100,1),
       "W35_pp",round((l35-e35)*100,2),
       "W35_rel",round((l35/e35-1)*100,1))
