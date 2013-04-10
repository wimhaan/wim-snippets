from scene import *
import pickle
from digit import *
class Digit ():

	num=0
	def __init__(self,digit):
		self.digit=0
	
		self.setDigit(digit)
	def setDigit(self,d):
		d<<=2
		#print 'd=',d
		self.digit&=(~60)
		self.digit|=d
	def getDigit(self):
		return (self.digit>>2)&15
	def setCandidate(self,c):
		d=1
		d<<=(c+5)
		self.digit|=d
	def resetCandidate(self,c):
		d=1
		d<<=(c+5)
		self.digit&=(~d)
	def getCandidates(self):
		d=self.digit>>6
		c=set()
		for i in range(9):
			if d&1: c.add(i+1)
			d>>=1
		return c
	def toggleCandidate(self,c):
		self.digit^=1<<(c+5)
	def setMode(self,m):
		self.digit&=(~3)
		self.digit|=m
	def getMode(self):
		return self.digit & 3
	def set(self,d,m):
		pm=self.getMode()
		pd=self.getDigit()
		if pm==0 and m!=0 and pd!=0: return
		if pm==1 and m==2 and pd!=0: return
		self.setMode(m)
		if m==2:self.toggleCandidate(d)
		else:
			if pd==d:
				d=0
				if m==1: self.setMode(2)
			self.setDigit(d)
	def reset(self):
		if self.getMode():
			self.digit=0
		

class Button():
	def __init__(self,x,y,name,f):
		self.name=name
		self.f=f
		self.x,self.y=x,y
		self.w,self.h=90,30
	def label(self):
		return self.name
	def setLabel(self,name):
		self.name=name
	def func(self):
		print self.name
		self.f()
	def touched(self,loc):
		if loc.x>self.x and loc.x<(self.x+self.w) and loc.y>self.y and loc.y<(self.y+self.h):
			return 1
		return 0
	def draw(self):
		fill(1,1.0,1)
		rect(self.x,self.y,self.w,self.h)
		text(self.name,'Helvetica',20,self.x+self.w/2,self.y+self.h/2)
	
	
class Puzzle ():
	def __init__(self):
		self.initDigits()
		self.load()
	#	self.reset()
	def getDigit(self,x,y):
		return self.cel[x][y].getDigit()
	def getCandidates(self,x,y):
		return self.cel[x][y].getCandidates()
	def save(self):
		f=open('status.nrc','w')
		pickle.dump(self.cel,f)
		f.close()
	def load(self):
		f=open('status.nrc','r')
		self.cel=pickle.load(f)
		f.close()
	def reset(self):
		for i in range(9):
			for j in range(9):
				self.cel[i][j].reset()
	def initDigits(self):
		self.cel=[[Digit(0) for i in range(9)] for j in range(9)]
	
	def setDigit(self,x,y,digit,celltype=0):
		if (x<0)or(x>8)or(y<0)or(y>8): return 
		self.cel[x][y].set(digit,celltype)
		self.save()

	def getDigitType(self,x,y):
		return self.cel[x][y].getMode()
	
	def testload(self):
		p=[[0,5,4],[1,3,6],[2,4,2],[2,5,8],[3,6,6],[4,6,3],[4,8,8],[5,1,4],[5,3,9],[5,4,1],[5,6,7],[6,4,9],[6,7,1],[7,5,5],[7,8,3],[8,2,2],[8,4,3]]
		for i in range(len(p)): self.setDigit(p[i][0],p[i][1],p[i][2])
		
class MyScene (Scene):
	def setup(self):
		self.device=0
		self.root_layer = Layer(self.bounds)
		center = self.bounds.center()
		self.cellsize=55 if self.device else 35
		self.bordersize=3 if self.device else 2
		self.offsetx=(self.bounds.w-(self.cellsize*9+self.bordersize*2))/2+self.bordersize
		self.offsety=400 if self.device else 200
		self.currentDigit=1
		self.mode=1
		self.nrc=[[1,1],[5,1],[1,5],[5,5]]
		self.puzzle = Puzzle()
		vs=130 if self.device else 30
		self.buttons=[Button(self.offsetx,vs,'reset',self.reset)]
		self.buttons+=[Button(self.offsetx+100,vs,'autofill',self.tst2)]
		self.buttons+=[Button(self.offsetx+200,vs,'puzzle',self.toggleMode)]
		
	def pause(self):
		print 'home pressed'
	def resume(self):
		print 'continue'
		
	def reset(self):
		self.puzzle.reset()
	
	def toggleMode(self):
		self.mode=0 if self.mode==1 else 1
		lb='define' if self.mode==0 else 'puzzle'
		self.buttons[2].setLabel(lb)
	def tst2(self):
		print 'tst2'
		self.puzzle.setDigit(0,0,2,2)
	def setCurrentDigit(self,d):
		if(d<0)or(d>8):return
		if self.currentDigit==(1+d) and self.mode!=0:
			self.mode=1 if self.mode==2 else 2
		self.currentDigit=1+d
		
	def drawDigit(self,x,y):
		tint(0,0,0)
		fnt='Helvetica'
		if (y>=0):
			digit=self.puzzle.getDigit(x,y)
			if self.puzzle.getDigitType(x,y)==1:
				tint(0,0,1)
		else: digit=x+1
		px=self.offsetx+self.cellsize*(x+0.5)
		py=self.offsety+self.cellsize*(y+0.5)
		mg=18 if self.device else 12
		if (self.mode==2 and y<0) or (self.puzzle.getDigitType(x,y)==2 and y>=0):
			cs=0.3*self.cellsize
			v=set([digit]) if y<0 else self.puzzle.getCandidates(x,y)
			for i in v:
				text(str(i),fnt,cs,px+mg*((i-1)%3)-mg,py-mg*((i-1)/3)+mg)
		else: 
			cs=0.8*self.cellsize
			if digit:text(str(digit),fnt,cs,px,py)
		
	def drawAllDigits(self):
		for i in range(9):
			self.drawDigit(i,-3)
			for j in range(9):
				self.drawDigit(i,j)
	
	def drawCellRow(self,y,offsety):
		for i in range(9):
			fill(1,1,1)
			if i in self.nrc and y in self.nrc: fill(0.8,0.8,0.8)
			oy=offsety+y*self.cellsize
			rect(self.offsetx+self.cellsize*i,oy,self.cellsize,self.cellsize)
		
	def drawBoard2(self):
		fill(0.1,0.1,0.1)
		bz=9*self.cellsize
		cc=self.cellsize
		rect(self.offsetx-self.bordersize,self.offsety-self.bordersize,bz+self.bordersize*2,bz+self.bordersize*2)
		cs=self.cellsize
		oy=self.offsety
		nrc=(1,2,3,5,6,7)
		cd=self.currentDigit
		for i in range(9):
			ox=self.offsetx
			for j in range(9):
				gd,md=self.puzzle.getDigit(j,i),self.puzzle.getDigitType(j,i)
				
				if cd and cd==gd and md!=2:
					(r,g,b)=(1,1,0)
				elif cd and md==2 and cd in self.puzzle.getCandidates(j,i):
					(r,g,b)=(1.0,0.6,0.6) if i in nrc and j in nrc else (1.0,0.8,0.8)
					
				else:
					(r,g,b)=(0.9,0.9,0.9) if i in nrc and j in nrc else (1,1,1)
					
				fill(r,g,b)	
				rect(ox,oy,cs,cs)		
				ox+=cs
			oy+=cs
			
		
		stroke(0.1,0.1,0.1)
		stroke_weight(1)
		xtop,ytop=self.offsetx+bz, self.offsety+bz
		for i in range(1,9):
			if i in [3,6]: 
				stroke(0,0,0) 
				stroke_weight(3)
			else:
				stroke(0.3,0.3,0.3) 
				stroke_weight(1)
			cum=i*self.cellsize
			line(self.offsetx+cum,self.offsety,self.offsetx+cum,ytop)
			line(self.offsetx,self.offsety+cum,xtop,self.offsety+cum)	
	
	def drawDigitBars(self):
		for i in range(9):
			cs=self.cellsize
			b=0 if (i+1)==self.currentDigit else 1
			fill(1,1,b)
			rect(self.offsetx+(i*cs),self.offsety-3*cs,cs,cs)
			
	def draw(self):
		background(0.9,0.9,0.9)
		self.drawBoard2()
		self.drawDigitBars()
		self.drawAllDigits()
		for button in self.buttons:button.draw()
		self.root_layer.draw()
	
	def touch_ended(self, touch):
		for button in self.buttons:
		  if button.touched(touch.location): button.func()
		x,y=touch.location.x-self.offsetx,touch.location.y-self.offsety+(3*self.cellsize)
		x,y=int(x/self.cellsize),int(y/self.cellsize)
		if (x<0)or(y<0):return 	
		if y==0:
			self.setCurrentDigit(x)
			return
		y-=3
		self.puzzle.setDigit(int(x),int(y),self.currentDigit,self.mode)

run(MyScene())
