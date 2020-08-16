# @TheWorldFoundry

from math import pi,sin,cos,sqrt,tan
import sys
from random import randint,random, Random
import pygame
from pygame import gfxdraw,Surface
from pygame.locals import *
# pygame.init()


GLOBDEBUG = False

# Cache floating point constants for speed
SIN = []
COS = []
TAN = []
MAXANG = 360
ANG = 2.0*pi/MAXANG
for i in xrange(0,MAXANG):
	A = ANG*i
	SIN.append(sin(A))
	COS.append(cos(A))
	TAN.append(tan(A))


def render(points,colour,degraded,R,lines,panelsize):
	

	(r,g,b) = colour
	minx = 999999999
	miny = 999999999
	maxx = -999999999
	maxy = -999999999
	
	# Scan the points for min/max dimensions
	for(x,y) in points:
		if minx == None or x < minx:
			minx = x
		if minx == None or x > maxx:
			maxx = x
		if miny == None or y < miny:
			miny = y
		if maxy == None or y > maxy:
			maxy = y
	# Normalise the dimensions and allocate image storage to draw into	
	width = int(maxx-minx)
	height = int(maxy-miny)
	# Conditionally normalise the points to the workspace - a transformation
	if minx != 0 or miny != 0:
		newPoints = []
		for(x,y) in points:
			newPoints.append((x-minx,y-miny))
		points = newPoints
	# print points
	cx = width>>1
	result = Surface((width<<1,height),SRCALPHA) # Target image has to cater for two flipped images, so twice the size
	result.convert()
	result.blit(renderhalf((width,height),points,colour,degraded,R,lines,panelsize,False),(width-1,0))
	result.blit(pygame.transform.flip(renderhalf((width,height),points,colour,degraded,R,lines,panelsize,False),True,False),(0,0))
	if GLOBDEBUG == True: pygame.image.save(result, "RENDER_"+str(randint(1000000000,9999999999))+"TEST.png")
	return result

def renderhalf(size,points,colour,degraded,R,lines,panelsize,normaliseHint):
	''' Given a 2D polygon defined by points, render it as if it's a 3d rotation of panels
	'''
	(r,g,b) = colour
	width,height = size
	if normaliseHint == True:
		# Scan the points for min/max dimensions
		minx = 999999999
		miny = 999999999
		maxx = -999999999
		maxy = -999999999
		for(x,y) in points:
			if minx == None or x < minx:
				minx = x
			if minx == None or x > maxx:
				maxx = x
			if miny == None or y < miny:
				miny = y
			if maxy == None or y > maxy:
				maxy = y
		# Normalise the dimensions and allocate image storage to draw into	
		width = int(maxx-minx)
		height = int(maxy-miny)

		# Conditionally normalise the points to the workspace - a transformation
		if minx != 0 or miny != 0:
			newPoints = []
			for(x,y) in points:
				newPoints.append((x-minx,y-miny))
			points = newPoints
		
	# Now we have a workspace and a pattern to use, go!
	# Make the shape
	template = Surface((width,height),SRCALPHA) # Template is a form guide
	template.convert()
	# Sketch the lines
	col = (r>>1,g>>1,b>>1)

	# Paint detail

	# Panels
	(px,py) = points[0]
	# R = Random(seed)
	numPanels = int(pi/2.0*width/panelsize) # TODO: Scale this with the size of area?
	#print numPanels,radius,panelsize
	if numPanels < 3:
		numPanels = 3
	deltangle = pi/2.0/numPanels
	for (newpx,newpy) in points:
		(x3,y3) = (-1,-1)
		(x4,y4) = (-1,-1)
		for i in xrange(0,numPanels+1):
			angle = deltangle*i
			xhere1 = px*cos(angle)
			xhere2 = newpx*cos(angle)
			(x1,y1) = (int(xhere2),int(newpy))
			(x2,y2) = (int(xhere1),int(py))
			p = [(x1,y1),(x2,y2),(x3,y3),(x4,y4)]
			rshade = r * sin(angle)
			gshade = g * sin(angle)
			bshade = b * sin(angle)
			if x3 != -1:
				type = R.randint(1,10)
				if type>degraded:
					gfxdraw.filled_polygon(template, p, (rshade,gshade,bshade))
				else:
					shift = R.randint(1,3)
					gfxdraw.filled_polygon(template, p, (int(rshade)>>shift,int(gshade)>>shift,int(bshade)>>shift))
			(x3,y3) = (x2,y2)
			(x4,y4) = (x1,y1)
		(px,py) = (newpx,newpy)
	# Lines						  
	if lines == True:
		(px,py) = points[0]						  
		for (newpx,newpy) in points:
			for i in xrange(0,numPanels+1):
				angle = deltangle*i
				xhere1 = px*cos(angle)
				xhere2 = newpx*cos(angle)
				(x1,y1) = (int(xhere2),int(newpy))
				(x2,y2) = (int(xhere1),int(py))

				rshade = r * sin(angle)
				
				gshade = g * sin(angle)
				bshade = (b-64) * sin(angle)								
				if bshade < 0: bshade = 0
				if lines: pygame.draw.line(template,(rshade,gshade,bshade),(x1,y1),(x2,y2),1)
			(px,py) = (newpx,newpy)				   
		for (x,y) in points: # Dividers
			pygame.draw.line(template,col,(0,y),(x,y), 1) # Divider
		col = (r>>2,g>>2,b>>2)
		pygame.draw.lines(template,col,False,points,1) # Exterior

	if GLOBDEBUG == True: pygame.image.save(template, "RENDERHALF_"+str(randint(1000000000,9999999999))+"TEST.png")
	return template	
	
def Sphere(width,height,seed,colour,lines,degraded,panelSize):
	''' Return a new part as an image
	'''
	# height is the centreline
	# width off the centreline at any point defines the countour line

	cx = width>>1
	radius = cx
	cy = height>>1
	h = height-1
	if seed == 0:
			seed = randint(1,999999999999)
	R = Random(seed)

	# Between each of the marked points, add detail and greeble points to the shape
	points = []
	divisions = 8
	if height > 16:
			divisions = h/R.randint(4,16)
	angledelta = pi/divisions
   
	for i in xrange(0,divisions+1):
			angle = pi/2-angledelta*i
			x = radius*cos(angle)
			y = cy+cy*sin(angle)
			points.append((x,y))
	
	# Make the shape

	return render(points,colour,degraded,R,lines,panelSize)

def Wings(width,height,seed,colour,lines,degraded,panelSize):
	''' Return a new part as an image
	'''
	# height is the centreline
	# width off the centreline at any point defines the countour line

	cx = width>>1
	radius = cx
	cy = height>>1
	h = height-1
	if seed == 0:
			seed = randint(1,999999999999)
	R = Random(seed)

	# Between each of the marked points, add detail and greeble points to the shape
	points = []
	points.append((0,0))
	points.append((cx>>3,height>>4))
	points.append((cx>>2,height>>3))
	points.append((R.randint(cx>>3,cx>>2),height>>2))
	points.append((cx,height-(height>>3)))
	points.append((cx-(cx>>3),height-1))
	points.append((0,height-1))

	
	# Make the shape
	img = render(points,colour,degraded,R,lines,panelSize)
	# markImage(img)

	overlayPoints = []
	for (x,y) in points:
		overlayPoints.append((x-(x>>4),y))

	img2 = render(overlayPoints,colour,degraded,R,lines,2)

	img.blit(img2,((img.get_width()-img2.get_width())>>1,0))

	return img

def Thruster(width,height,seed,colour,lines,degraded,panelSize):
	''' Return a new part as an image
	'''
	# height is the centreline
	# width off the centreline at any point defines the countour line

	radius = cx = width>>1
	cy = height>>1
	h = height-1
	R = Random(seed)

	# Between each of the marked points, add detail and greeble points to the shape
	points = []
	points.append((0,0))
	cursw = R.randint(0,radius)
	points.append((cursw,0))
	cursor = 1
	widthRange = width>>6
	if widthRange < 4:
		widthRange = 4
	while cursor < height:
			cursw += R.randint(-widthRange,widthRange)
			if cursw < 1:
					cursw = 1
			if cursw > radius:
					cursw = radius
			points.append((cursw,cursor))
			cursor += R.randint(3,11) # Make this noise smoother?
	points.append((cursw/2,h))
	points.append((0,h))
	
	# Make the shape

	return render(points,colour,degraded,R,lines,panelSize)

def Band(width,height,seed,colour,lines,degraded,panelSize):
	''' Return a new part as an image
	'''
	# height is the centreline
	# width off the centreline at any point defines the countour line

	cx = width>>1
	radius = cx
	cy = height>>1
	h = height-1
	R = Random(seed)

	# Between each of the marked points, add detail and greeble points to the shape
	points = []
	points.append((0,0))
	cursor = 1
	while cursor < height:
			points.append((cx,cursor))
			cursor += R.randint(panelSize,panelSize<<1) # Make this noise smoother?
	points.append((0,h))
	
	# Make the shape
	return render(points,colour,degraded,R,lines,panelSize)

	
def Chassis(width,height,seed,colour,lines,degraded,panelSize):
	''' Return a new part as an image
	'''
	# height is the centreline
	# width off the centreline at any point defines the countour line

	cx = width>>1
	radius = cx
	cy = height>>1
	h = height-1
	R = Random(seed)

	# Between each of the marked points, add detail and greeble points to the shape
	points = []
	points.append((0,0))
	cursw = R.randint(0,radius>>1)
	points.append((cursw,0))
	cursor = 1
	while cursor < height:
			cursw += R.randint(-8,2)
			if cursw < 1:
					cursw = 1
			if cursw > radius:
					cursw = radius
			points.append((cursw,cursor))
			cursor += R.randint(3,11) # Make this noise smoother?
	points.append((cursw/2,h))
	points.append((0,h))
	
	# Make the shape
	return render(points,colour,degraded,R,lines,panelSize)

def markImage(img):
	col = (0,255,0)
	width = img.get_width()
	height = img.get_height()
	pygame.gfxdraw.vline(img, 0, 0, height, col)
	pygame.gfxdraw.vline(img, width-1, 0, height, col)
	pygame.gfxdraw.vline(img, width>>1, 0, height, col)
	pygame.gfxdraw.hline(img, 0, width-1, 0, col)
	pygame.gfxdraw.hline(img, 0, width-1, height>>1, col)
	pygame.gfxdraw.hline(img, 0, width-1, height-1, col)

class Part:
	def __init__(self,label,img,(x,y,z)):
		self.width = img.get_width()
		self.height = img.get_height()
		self.img = img
		if False:
			markImage(self.img) # Debug - bounding boxes
		self.label = label
		self.x = x
		self.y = y
		self.z = z
		self.parts = []
		# Simple z buffering
		self.zdraworder = []
		self.zdraworder.append(self)
		
	def placeByCentre(self,surface,(x,y)):
		surface.blit(self.img,(x-(self.width>>1),y-(self.height>>1)))

	def draw(self,surface):
		x = surface.get_width()>>1
		y = surface.get_height()>>1
		
		for part in self.zdraworder:
			part.placeByCentre(surface,(x+part.x,y+part.y))
		#self.placeByCentre(surface,(x+self.x,y+self.y))
		#for part in self.parts:
		#	part.draw(surface)
		
	def add(self,part):
		self.parts.append(part)
		i = 0
		placed = False
		for drawobj in self.zdraworder:
			if part.z < drawobj.z:
				self.zdraworder.insert(i,part)
				placed = True
				break
			i += 1
		if placed == False:
			self.zdraworder.append(part)
		
class Ship(object):
	DIRFACING = 270
	def __init__(self, size, seed):
		self.width, self.height = size
		self.shipseed = seed
		self.thrustseed = seed
		if seed == 0:
			self.shipseed = randint(1,9999999999)
			self.thrustseed = randint(1,9999999999)
		self.Rship = Random(self.shipseed)
		self.Rthrust = Random(self.thrustseed)
		self.basecol = (self.Rship.randint(0,127)+120,self.Rship.randint(0,127)+120,self.Rship.randint(0,127)+120)

		self.shipSeed = self.Rship.randint(1000000000,9999999999)
		self.chassisWidth = self.Rship.randint(self.width>>3,self.width>>1)
		self.chassisLength = self.Rship.randint(self.height>>1,self.height)

		self.flines = True
		if self.Rship.randint(1,10) > 5:
			self.flines = False

		self.decayamount = randint(0,10)
		self.panelsize = randint(2,12)

		# Physics
		self.velocity = 0
		self.direction = self.DIRFACING
		
		
		# Collision
		
			
	def rotate(self,angle):
		self.direction = (angle+self.DIRFACING)%MAXANG
		self.gfxrot = pygame.transform.rotate(self.gfx,angle)
	
	def draw(self,surface):
		surface.blit(self.gfxrot,((surface.get_width()>>1)-(self.gfxrot.get_width()>>1),(surface.get_height()>>1)-(self.gfxrot.get_height()>>1)))
    
		
class ShipRocket(Ship):
	def __init__(self, size, seed):
		super(ShipRocket,self).__init__(size,seed)
		# Structure of the ship is a central tube with surface variations
		# A symmetrical / asymmetrical collection of one or more thrusters encircling the back
		numThrusters = self.Rship.randint(2,7)
		self.thrusterRadius = self.Rship.randint(self.width>>3,self.width>>2)
		self.thrusterLength = self.Rship.randint(self.height>>2,self.height>>1)
		self.thrusterAngle = int(360/numThrusters)
		self.thrusters = []
		thrusterSeed = self.Rthrust.randint(1000000000,9999999999)
		for i in xrange(0,numThrusters+1):
			A = (self.thrusterAngle*i)%MAXANG
			self.thrusters.append((Thruster(self.thrusterRadius<<1,self.thrusterLength,thrusterSeed,self.basecol,self.flines,randint(0,10),randint(2,12)),(COS[A],SIN[A])))
			
		self.chassis = []
		y = 0
		x = (self.width>>1)-(self.chassisWidth>>1)
	
		self.model = Part("Ship", Thruster(self.chassisWidth,self.chassisLength,self.shipSeed,self.basecol,self.flines,self.decayamount,self.panelsize),(0,0,0))

		y = self.model.height-1-self.thrusterLength-self.Rship.randint(0,self.model.height>>3)
		for (img,(x,z)) in self.thrusters:
			#self.gfx.blit(img,((self.width>>1)+thustHarnessRadius*theta,(self.height-1-self.thrusterLength)))
			self.model.add(Part("Thruster", Thruster(self.thrusterRadius<<1,self.thrusterLength,thrusterSeed,self.basecol,self.flines,self.decayamount,self.panelsize), (x*(self.model.width>>1),y,(z*(self.model.width>>1))) ))
		
		# Render all the parts
		self.gfx = Surface(size,SRCALPHA)
		self.gfx.convert()
		print "Drawing"
		self.model.draw(self.gfx)
		self.rotation = 0
		self.gfxrot = self.gfx

class ShipCruiser(Ship):
	def __init__(self, size, seed):
		super(ShipCruiser,self).__init__(size,seed)
		# Structure of the ship is a central tube with surface variations
		# A symmetrical / asymmetrical collection of one or more thrusters encircling the back
		numThrusters = self.Rship.randint(2,7)
		self.thrusterRadius = self.Rship.randint(self.width>>4,self.width>>3)
		self.thrusterLength = self.Rship.randint(self.height>>5,self.height>>3)
		self.thrusterAngle = pi/numThrusters
		self.thrusters = []
		thrusterSeed = self.Rthrust.randint(1000000000,9999999999)
		for i in xrange(0,numThrusters+1):
			self.thrusters.append((Thruster(self.thrusterRadius<<1,self.thrusterLength,thrusterSeed,self.basecol,self.flines,randint(0,10),randint(2,12)),(cos(self.thrusterAngle*i),sin(self.thrusterAngle*i))))
			
		self.chassis = []
		y = 0
		x = (self.width>>1)-(self.chassisWidth>>1)
	
		self.winglength = self.Rship.randint(self.chassisLength>>3,self.chassisLength>>2)
		self.model = Part("Wing", Wings(self.width,self.winglength,self.shipSeed,self.basecol,self.flines,self.decayamount,self.panelsize),(0,-self.Rship.randint(self.chassisLength>>4,self.chassisLength>>1)+(self.chassisLength-self.winglength)>>2,100))

		self.winglength = self.Rship.randint(self.chassisLength>>2,self.chassisLength>>1)
		thrusterMountPoint = self.winglength-self.Rship.randint(self.chassisLength>>4,self.chassisLength>>1)+(self.chassisLength-self.winglength)>>2
		self.model.add(Part("Wing", Wings(self.width>>1,self.winglength,self.shipSeed,self.basecol,self.flines,self.decayamount,self.panelsize),(0,thrusterMountPoint,100)))

		self.winglength = self.Rship.randint(self.chassisLength>>1,self.chassisLength)
		self.model.add(Part("Wing", Wings(self.width>>2,self.winglength,self.shipSeed,self.basecol,self.flines,self.decayamount,self.panelsize),(0,-self.Rship.randint(self.chassisLength>>4,self.chassisLength>>1)+(self.chassisLength-self.winglength)>>2,100)))


		y = thrusterMountPoint #self.model.height-1-self.thrusterLength-self.Rship.randint(0,self.model.height>>3)
		for (img,(x,z)) in self.thrusters:
			#self.gfx.blit(img,((self.width>>1)+thustHarnessRadius*theta,(self.height-1-self.thrusterLength)))
			self.model.add(Part("Thruster", Thruster(self.thrusterRadius<<1,self.thrusterLength,thrusterSeed,self.basecol,self.flines,self.decayamount,self.panelsize), (x*(self.model.width>>2),y,(z*(self.model.width>>1))) ))
		
		# Render all the parts
		self.gfx = Surface(size,SRCALPHA)
		self.gfx.convert()
		print "Drawing"
		self.model.draw(self.gfx)
		self.rotation = 0
		self.gfxrot = self.gfx

class Light:
	def __init__(self,label,radius,colour):
		self.label = label
		self.radius = radius
		self.R,self.G,self.B = colour
		self.A = 255
		self.gfx = None
		
	def apply(self,img,pos):
		for (x,y) in pos:
			
			if self.gfx == None:
				self.gfx = Surface(((self.radius<<1)+1,(self.radius<<1)+1),SRCALPHA)
				self.gfx.convert()
				gfxdraw.filled_circle(self.gfx,self.radius,self.radius,int(self.radius), (self.R,self.G,self.B,self.A))
				
			r2 = self.radius
			img.blit(self.gfx,(x-r2,y-r2),special_flags=BLEND_ADD)
			

def makeShip(pos,seed,size):
	# w = randint(50,200)
	R = Random(seed)
	if R.random() > 0.4:
		ship = ShipRocket(size,seed)
	else:
		ship = ShipCruiser(size,seed)

	return ship

'''
def doit():
	print "Starting initialisation"
	PAINT = False
	SAVE = False
	(width,height) = (480,480)
	cx = width>>1
	cy = height>>1
	print "Creating Surface and Window"
	surface = pygame.display.set_mode((width, height),SRCALPHA)
	print "Converting the surface to optimise rendering"
	surface.convert()
	print "Changing the caption"
	pygame.display.set_caption('eGAD - electronic Game-a-Day')
	FPS = 60
	fpsClock = pygame.time.Clock()
	
	
	angle = pi/180


	FILENAME = "OUT_"+str(randint(10000000,99999999))
	# Set up geometry
	

	shapes = []
	redLight = Light("Red Light",5,(100,100,200))
	blueLight = Light("Red Light",10,(0,0,255))
	blueLight2 = Light("Red Light",15,(0,0,180))
	
	lightPos = []
	for i in xrange(0,randint(15,150)):
		lightPos.append((randint(0,width),randint(0,height)))
	
	# End Set up geometry
	
	iterationCount = 0
	keepGoing = True
	SAVEROT = randint(0,359)
	print "Starting main loop"
	while keepGoing == True:
		iterationCount += 1

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				keepGoing = False
			elif event.type == MOUSEBUTTONUP:
				if event.button == 1: # 1 == Left
					(px,py) = event.pos
					shapes = []
					w1 = randint(50,width)
					shapes.append(makeShip((w1,randint(w1,height)),randint(1,9999999999999999)))

		if PAINT == False: surface.fill((0,0,0))
		else: surface.fill((16,16,16,8),rect=(0,0,width,height),special_flags=BLEND_SUB)
		
		# Render geometry
		
		rotationamount = iterationCount%360

		if rotationamount == 1:
			shapes = []
			w1 = 50 # randint(width>>6,width>>4)
			shapes.append(makeShip((w1,randint(w1,height)),randint(1,9999999999999999)))
			lightPos.append((randint(0,width),randint(0,height)))
			SAVEROT = randint(0,359)
	
		for s in shapes:
			s.rotate(rotationamount)
			redLight.apply(s.gfxrot,lightPos)
			blueLight2.apply(s.gfxrot,lightPos)
			blueLight.apply(s.gfxrot,lightPos)
			s.draw(surface)
			
		# End render geometry
		

		pygame.display.update()
		fpsClock.tick(FPS)
		if SAVE == True or GLOBDEBUG == True or rotationamount == SAVEROT: pygame.image.save(surface, FILENAME+"_"+str(iterationCount)+"_Plot.png")
	print "Shutting down."
	pygame.quit()
	sys.exit()
doit()
'''