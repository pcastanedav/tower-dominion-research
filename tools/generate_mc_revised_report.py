#!/usr/bin/env python3
"""Render reviewed editorial Markdown as a separately named PDF; never read historical chart data."""
from pathlib import Path
import re, html
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.enums import TA_LEFT
ROOT=Path(__file__).resolve().parents[1]/'docs/tasks/mission-control-chain'
SRC=ROOT/'REVISED-REPORT-EDITORIAL-DRAFT.md'
OUT=ROOT/'Tower_Dominion_Mission_Control_Chain_Analysis_REVISED_REVIEW.pdf'
NAVY=HexColor('#172331'); SLATE=HexColor('#26394C'); GOLD=HexColor('#D5A34B'); GRAY=HexColor('#6B7885')
PALETTE={'Baseline':'#777777','Lions':'#D64545','Eleonor':'#36965C','Tander':'#3478D4','Magel':'#9B59B6'}
font='/usr/share/fonts/TTF/DejaVuSans.ttf'; bold='/usr/share/fonts/TTF/DejaVuSans-Bold.ttf'
pdfmetrics.registerFont(TTFont('TD',font));pdfmetrics.registerFont(TTFont('TD-Bold',bold))
styles={
'body':ParagraphStyle('body',fontName='TD',fontSize=9.3,leading=14.2,spaceAfter=8,textColor=SLATE,allowWidows=0,allowOrphans=0),
'h1':ParagraphStyle('h1',fontName='TD-Bold',fontSize=17,leading=23,spaceBefore=20,spaceAfter=13,textColor=NAVY,keepWithNext=True),
'h2':ParagraphStyle('h2',fontName='TD-Bold',fontSize=11.5,leading=17,spaceBefore=13,spaceAfter=7,textColor=NAVY,keepWithNext=True),
'h3':ParagraphStyle('h3',fontName='TD-Bold',fontSize=10,leading=15,spaceBefore=10,spaceAfter=6,textColor=SLATE,keepWithNext=True),
'caption':ParagraphStyle('caption',fontName='TD',fontSize=8,leading=12,spaceAfter=10,textColor=GRAY),
'cell':ParagraphStyle('cell',fontName='TD',fontSize=7.1,leading=10,textColor=SLATE),
'header':ParagraphStyle('header',fontName='TD-Bold',fontSize=7.1,leading=10,textColor=colors.white),
'cover':ParagraphStyle('cover',fontName='TD-Bold',fontSize=29,leading=41,textColor=colors.white),
'covermeta':ParagraphStyle('covermeta',fontName='TD',fontSize=11,leading=19,textColor=HexColor('#D3DCE4'))
}
def markup(s):
 s=html.escape(s.strip())
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)',r'<i>\1</i>',s)
 s=re.sub(r'`([^`]+)`',r'<font color="#6B7885">\1</font>',s)
 return s
def para(s,style='body'):return Paragraph(markup(s),styles[style])
class Doc(SimpleDocTemplate):
 def afterFlowable(self,flowable):
  if isinstance(flowable,Paragraph) and getattr(flowable,'_outline',None):
   key,title,level=flowable._outline
   self.canv.bookmarkPage(key)
   self.canv.addOutlineEntry(title,key,level=level,closed=False)
def footer(c,doc):
 if doc.page==1:return
 w,h=A4;c.saveState();c.setStrokeColor(HexColor('#DDE2E5'));c.line(49,h-40,w-49,h-40)
 c.setFont('TD',7);c.setFillColor(GRAY)
 c.drawString(49,h-32,'TOWER DOMINION  /  MISSION CONTROL CHAIN ANALYSIS')
 c.drawString(49,28,'CORRECTED SIMULATION  •  EDITORIAL REVIEW')
 c.drawRightString(w-49,28,str(doc.page-1));c.restoreState()
width=A4[0]-98
doc=Doc(str(OUT),pagesize=A4,leftMargin=49,rightMargin=49,topMargin=57,bottomMargin=48,title='Tower Dominion — Mission Control Chain Analysis (Revised Review)')
story=[]
from reportlab.platypus import Flowable
class Cover(Flowable):
 def __init__(self):super().__init__();self.width=width;self.height=690
 def draw(self):
  c=self.canv;c.saveState();c.setFillColor(NAVY);c.rect(-49,-50,A4[0],800,fill=1,stroke=0)
  c.setFont('TD-Bold',12);c.setFillColor(GOLD);c.drawString(20,620,'TOWER DOMINION / STRATEGY RESEARCH')
  c.setFillColor(colors.white);c.setFont('TD-Bold',29);c.drawString(20,445,'MISSION CONTROL');c.setFillColor(GOLD);c.drawString(20,400,'CHAIN ANALYSIS')
  c.setFont('TD',11);c.setFillColor(HexColor('#D3DCE4'))
  for i,t in enumerate(['Corrected Blueprint acquisition simulations','Waves 63 and 83 • Commander, faction and package comparisons']):c.drawString(20,340-i*22,t)
  c.setStrokeColor(GOLD);c.setLineWidth(2);c.line(20,263,150,263)
  c.setFont('TD',9);c.drawString(20,228,'REVISED EDITORIAL REVIEW  /  10 OCTOBER 2026')
  c.drawString(20,72,'BLUEPRINT ACQUISITION IS NOT COMBAT SURVIVAL')
  c.restoreState()
story.extend([Cover(),PageBreak()])
lines=SRC.read_text().splitlines()
sections=[re.sub(r'^# ','',l) for l in lines if l.startswith('# ')][1:]
story.append(para('CONTENTS','h1'))
for title in sections:story.append(para(title))
story.append(PageBreak())
i=0;section=0
while i<len(lines):
 l=lines[i].strip()
 if not l:i+=1;continue
 if l.startswith('# '):
  if section:story.append(PageBreak())
  section+=1
  p=para(l[2:],'h1');p._outline=('s'+str(section),l[2:],0);story.append(p);i+=1;continue
 if l.startswith('### '):story.append(para(l[4:],'h3'));i+=1;continue
 if l.startswith('## '):story.append(para(l[3:],'h2'));i+=1;continue
 if l.startswith('|'):
  rows=[]
  while i<len(lines) and lines[i].strip().startswith('|'):
   raw=[x.strip() for x in lines[i].strip().strip('|').split('|')]
   if not all(re.fullmatch(r':?-{3,}:?',x or '') for x in raw):rows.append(raw)
   i+=1
  if not rows:continue
  n=max(len(r) for r in rows);rows=[r+['']*(n-len(r)) for r in rows]
  first=.34 if n<=4 else .29
  widths=[width*first]+[width*(1-first)/(n-1)]*(n-1)
  cells=[[para(x,'header' if ri==0 else 'cell') for x in row] for ri,row in enumerate(rows)]
  t=Table(cells,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=1)
  cmds=[('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,1),(-1,-1),.3,HexColor('#DDE2E5'))]
  for ri,row in enumerate(rows[1:],1):
   if ri%2==0:cmds.append(('BACKGROUND',(0,ri),(-1,ri),HexColor('#F4F2EC')))
   for key,color in PALETTE.items():
    if row[0].startswith(key):cmds.append(('LINEBEFORE',(0,ri),(0,ri),3,HexColor(color)));break
  t.setStyle(TableStyle(cmds));story.append(t);story.append(Spacer(1,8));continue
 if l.startswith('>'):story.append(para(l[1:].strip(),'caption'));i+=1;continue
 if l.startswith('*') and l.endswith('*') and not l.startswith('**'):story.append(para(l,'caption'));i+=1;continue
 # Collect consecutive prose lines into one paragraph.
 block=[l];i+=1
 while i<len(lines) and lines[i].strip() and not lines[i].startswith(('#','|','>')):
  block.append(lines[i].strip());i+=1
 story.append(para(' '.join(block)))
doc.build(story,onFirstPage=footer,onLaterPages=footer)
print('CREATED',OUT)
