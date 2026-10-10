#!/usr/bin/env python3
"""Generate the approved Tower Dominion report from editable source files."""
from pathlib import Path
import json,re,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether,Flowable
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT,TA_CENTER,TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing,Line,Rect,String,PolyLine
from reportlab.lib.colors import HexColor

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'docs/tasks/mission-control-chain'
OUT=SRC/'Tower_Dominion_Mission_Control_Chain_Analysis.pdf'
DATA=json.loads((SRC/'SIMULATION-1000-RUNS.json').read_text())
NAVY=HexColor('#172331'); SLATE=HexColor('#26394C'); GOLD=HexColor('#D5A34B')
GRAY=HexColor('#6B7885'); IVORY=HexColor('#F4F2EC')
PALETTE={'Baseline':'#777777','Lions':'#D64545','Eleonor':'#36965C','Tander':'#3478D4','Magel':'#9B59B6'}
FONT='/usr/share/fonts/TTF/DejaVuSans.ttf'
BOLD='/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'
if not Path(FONT).exists():
 FONT='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
 BOLD='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('TD',FONT))
pdfmetrics.registerFont(TTFont('TD-Bold',BOLD))
S={
 'body':ParagraphStyle('body',fontName='TD',fontSize=9.7,leading=14.6,textColor=SLATE,spaceAfter=7,allowWidows=0,allowOrphans=0),
 'bodykeep':ParagraphStyle('bodykeep',fontName='TD',fontSize=9.7,leading=14.6,textColor=SLATE,spaceAfter=7,keepWithNext=True),
 'h1':ParagraphStyle('h1',fontName='TD-Bold',fontSize=18,leading=24,textColor=NAVY,spaceAfter=17,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='TD-Bold',fontSize=12,leading=17,textColor=NAVY,spaceBefore=15,spaceAfter=8,keepWithNext=True),
 'minor':ParagraphStyle('minor',fontName='TD-Bold',fontSize=10,leading=14,textColor=SLATE,spaceBefore=11,spaceAfter=6,keepWithNext=True),
 'meta':ParagraphStyle('meta',fontName='TD',fontSize=8,leading=12,textColor=GRAY,spaceAfter=4),
 'small':ParagraphStyle('small',fontName='TD',fontSize=7.4,leading=10.5,textColor=SLATE),
 'thead':ParagraphStyle('thead',fontName='TD-Bold',fontSize=7.2,leading=10,textColor=colors.white),
 'tcell':ParagraphStyle('tcell',fontName='TD',fontSize=7.5,leading=11,textColor=SLATE),
 'coverk':ParagraphStyle('coverk',fontName='TD-Bold',fontSize=12,leading=17,textColor=GOLD),
 'covert':ParagraphStyle('covert',fontName='TD-Bold',fontSize=28,leading=39,textColor=colors.white),
 'covers':ParagraphStyle('covers',fontName='TD',fontSize=12,leading=20,textColor=HexColor('#D3DCE4')),
}
def P(text,style='body'):
 return Paragraph(html.escape(text).replace('>=','≥'),S[style])
class Anchor(Flowable):
 def __init__(self,key,title):Flowable.__init__(self);self.key=key;self.title=title;self.width=0;self.height=0
 def draw(self):
  c=self.canv;c.bookmarkPage(self.key);c.addOutlineEntry(self.title,self.key,level=0,closed=False)
class Cover(Flowable):
 def __init__(self):Flowable.__init__(self);self.width=480;self.height=700
 def draw(self):
  c=self.canv;c.saveState();c.setFillColor(NAVY);c.rect(-48,-38,700,810,stroke=0,fill=1)
  c.setFillColor(GOLD);c.setFont('TD-Bold',12);c.drawString(18,645,'TOWER DOMINION  /  STRATEGY RESEARCH')
  c.setFillColor(colors.white);c.setFont('TD-Bold',34);c.drawString(18,455,'MISSION CONTROL')
  c.setFillColor(GOLD);c.setFont('TD-Bold',30);c.drawString(18,406,'CHAIN ANALYSIS')
  c.setFillColor(HexColor('#D3DCE4'));c.setFont('TD',11)
  for i,line in enumerate(['A simulation-based comparison of Blueprint acquisition,','faction and commander advantages, and Amplifier effects.']):
   c.drawString(18,355-19*i,line)
  c.setStrokeColor(GOLD);c.setLineWidth(2);c.line(18,283,135,283)
  c.setFont('TD',10);c.drawString(18,247,'10,000 simulated runs  |  Waves 1–103')
  c.setFont('TD',8);c.drawString(18,75,'MODELED ACQUISITION — NOT COMBAT SURVIVAL')
  c.restoreState()
def footer(c,doc):
 if doc.page==1:return
 c.saveState();w,h=A4;c.setStrokeColor(HexColor('#DDE2E5'));c.line(49,h-40,w-49,h-40)
 c.setFont('TD',7);c.setFillColor(GRAY)
 c.drawString(49,h-32,'TOWER DOMINION / MISSION CONTROL CHAIN ANALYSIS')
 c.drawString(49,28,'SIMULATION REPORT  •  1,000 RUNS PER SCENARIO')
 c.drawRightString(w-49,28,str(doc.page-1));c.restoreState()
class Doc(SimpleDocTemplate):
 def afterFlowable(self,f):pass
doc=Doc(str(OUT),pagesize=A4,rightMargin=49,leftMargin=49,topMargin=56,bottomMargin=49,title='Tower Dominion — Mission Control Chain Analysis',author='Tower Dominion Strategy Research')
WIDTH=A4[0]-98
story=[Cover(),PageBreak(),P('CONTENTS','h1')]
titles=[]
for i in range(1,9):
 lines=(SRC/f'REPORT-SECTION-{i:02d}.txt').read_text().splitlines()
 titles.append(lines[0].replace(' — ','  ·  ',1))
titles.append('APPENDIX  ·  SIMULATION PARAMETERS AND REPRODUCIBILITY')
for i,title in enumerate(titles):
 story.append(P(title,'body'))
story.extend([Spacer(1,18),P('Scope: Mission Control acquisition, not survival probability. All scenarios use the same 1,000-run simulation framework.','meta')])

def isrow(line):
 return len(re.split(r'\s{2,}',line.strip()))>=3 and (line.strip().startswith(('Baseline','Lions','Eleonor','Tander','Magel','Scenario','Commander','Checkpoint','0 Amplifiers','1 Amplifier','2 Amplifiers')) or re.search(r'\d+\.\d+%?',line))
def tabulate(lines):
 rows=[re.split(r'\s{2,}',line.strip()) for line in lines]
 n=max(map(len,rows))
 if n>7:return None
 rows=[r+['']*(n-len(r)) for r in rows]
 widths=[WIDTH*.29]+[WIDTH*.71/(n-1)]*(n-1)
 data=[]
 for ridx,row in enumerate(rows):
  cells=[]
  for j,val in enumerate(row):
   label=val.strip()
   cell=P(label,'thead' if ridx==0 else 'tcell')
   cells.append(cell)
  data.append(cells)
 t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
 commands=[('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
 ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
 ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
 ('LINEBELOW',(0,1),(-1,-1),.35,HexColor('#DCE1E5'))]
 for i,r in enumerate(rows[1:],1):
  if r[0] in PALETTE:commands.append(('LINEBEFORE',(0,i),(0,i),3,HexColor(PALETTE[r[0]])))
 t.setStyle(TableStyle(commands));return t
def chart(kind):
 d=Drawing(WIDTH,218)
 labels=['Baseline','Lions','Eleonor','Tander','Magel']
 left=48;right=WIDTH-12;top=187;bottom=29
 for i in range(5):
  y=bottom+i*(top-bottom)/4
  d.add(Line(left,y,right,y,strokeColor=HexColor('#DDE2E5'),strokeWidth=.6))
 if kind=='growth':
  waves=[20,35,40,50,60,63,64,83,103]; ymax=65
  for name in labels:
   k='Natural / '+('Eleanor' if name=='Eleonor' else name)
   pts=[(left+(w-20)/(103-20)*(right-left),bottom+DATA[k][str(w)]['mean']/ymax*(top-bottom)) for w in waves]
   for a,b in zip(pts,pts[1:]):
    d.add(Line(a[0],a[1],b[0],b[1],strokeColor=HexColor(PALETTE[name]),strokeWidth=2))
  for w in [20,40,63,83,103]:
   x=left+(w-20)/83*(right-left);d.add(String(x-8,12,str(w),fontName='TD',fontSize=7,fillColor=GRAY))
  for v in [0,15,30,45,60]:
   y=bottom+v/65*(top-bottom);d.add(String(4,y-3,str(v),fontName='TD',fontSize=7,fillColor=GRAY))
 else:
  ymax=100;metric='p_ge_10'
  barw=(right-left)/6
  for i,name in enumerate(labels):
   k='Natural / '+('Eleanor' if name=='Eleonor' else name)
   val=DATA[k]['63'][metric];x=left+i*barw+barw*.2;hh=val/100*(top-bottom)
   d.add(Rect(x,bottom,barw*.55,hh,strokeColor=None,fillColor=HexColor(PALETTE[name])))
   d.add(String(x,bottom+hh+5,f'{val:.1f}%',fontName='TD',fontSize=7,fillColor=SLATE))
   d.add(String(x,12,name,fontName='TD',fontSize=6.8,fillColor=SLATE))
 if kind=='growth':
  for i,name in enumerate(labels):
   x=left+i*(right-left)/5;d.add(Line(x,209,x+12,209,strokeColor=HexColor(PALETTE[name]),strokeWidth=2.4))
   d.add(String(x+15,206,name,fontName='TD',fontSize=7,fillColor=SLATE))
 return d

for idx in range(1,10):
 file=SRC/(f'REPORT-SECTION-{idx:02d}.txt' if idx<=8 else 'REPORT-APPENDIX.txt')
 lines=file.read_text().splitlines()
 story.append(PageBreak())
 title=lines[0].replace(' — ',' · ',1)
 story.extend([Anchor(f'section-{idx}',title),P(title,'h1')])
 if idx==5:
  story.append(KeepTogether([P('FIGURE 1  ·  Wave 63: probability of acquiring at least 10 MCs','minor'),chart('threshold'),P('Natural acquisition; 1,000 runs per scenario. This is not a survival probability.','meta')]))
 if idx==6:
  story.append(KeepTogether([P('FIGURE 2  ·  Mean Mission Controls by recorded checkpoint','minor'),chart('growth'),P('Natural acquisition. Lines connect recorded checkpoints only; no intermediate results are implied.','meta')]))
 i=1
 while i<len(lines):
  line=lines[i].strip()
  if not line:i+=1;continue
  if line.startswith(('Status:','Source:','NOTE:')):
   i+=1;continue
  if re.match(r'^\d+\.\d+\. ',line) or re.match(r'^A\.\d+\. ',line):
   story.append(P(line,'h2'));i+=1;continue
  if re.match(r'^SECTION \d+ SUMMARY$',line) or line=='SECTION SUMMARY':
   story.append(P(line,'h2'));i+=1;continue
  if line.isupper() and len(line)>8 and len(line)<105 and not isrow(line):
   if i+1<len(lines) and lines[i+1].strip() and isrow(lines[i+1]):
    head=line;j=i+1;tbl=[]
    while j<len(lines) and lines[j].strip() and isrow(lines[j]):
     tbl.append(lines[j]);j+=1
    if len(tbl)>=2:
     table=tabulate(tbl)
     if table:
      story.append(KeepTogether([P(head.title(),'minor'),table,Spacer(1,8)]));i=j;continue
   story.append(P(line.title(),'minor'));i+=1;continue
  if isrow(line):
   tbl=[];j=i
   while j<len(lines) and lines[j].strip() and isrow(lines[j]):tbl.append(lines[j]);j+=1
   if len(tbl)>=2:
    table=tabulate(tbl)
    if table:story.append(KeepTogether([table,Spacer(1,8)]));i=j;continue
  if re.match(r'^\d+\. ',line):
   story.append(P(line,'body'));i+=1;continue
  nextline=next((z.strip() for z in lines[i+1:] if z.strip()),'')
  story.append(P(line,'bodykeep' if line.endswith(':') or (len(line)<110 and isrow(nextline)) else 'body'));i+=1

doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('PDF CREATED',OUT,'bytes',OUT.stat().st_size)
