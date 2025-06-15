import pygame as pg
from params import *
from pointcity import *

# images
boutonLeftImg = pg.image.load("res/rules/left.png")
boutonRightImg = pg.image.load("res/rules/right.png")
boutonXImg = pg.image.load("res/X.png")
reglesImg = [pg.image.load("res/rules/"+str(i)+".png") for i in range(1,4)]

#dimensions
reglesSize = (screenSize[0]*screenSize[1]/reglesImg[0].get_rect().h, screenSize[1])
reglesPos = ((screenSize[0] - reglesSize[0])/2, 0)
space = 30
h1 = screenSize[1]/10
h2 = screenSize[1]/20
(a,b) = boutonLeftImg.get_rect().size
boutonSize1 = (h1*a/b, h1)
boutonSize2 = (h2, h2)

# boutons
boutonLRect = pg.Rect((space, 0), boutonSize1)
boutonLRect.centery = screenSize[1]/2
boutonRRect = boutonLRect.copy()
boutonRRect.right = screenSize[0] - space
boutonXRect = pg.Rect((screenSize[0] - h2*2, h2), boutonSize2)

# redimensionnement
boutonLeftImg = pg.transform.smoothscale(boutonLeftImg, boutonSize1)
boutonRightImg = pg.transform.smoothscale(boutonRightImg, boutonSize1)
boutonLeftImg2 = pg.transform.smoothscale(pg.image.load("res/rules/left2.png"), boutonSize1)
boutonRightImg2 = pg.transform.smoothscale(pg.image.load("res/rules/right2.png"), boutonSize1)
boutonXImg = pg.transform.smoothscale(boutonXImg, boutonSize2)
boutonXImg2 = pg.transform.smoothscale(pg.image.load("res/X2.png"), boutonSize2)
reglesImg = [pg.transform.smoothscale(reglesImg[i], reglesSize) for i in range(3)]


# Nrs boutons
class boutonNr(IntEnum):
	RIEN = -1
	RIGHT = 0
	LEFT = 1
	X = 2

class rulesMenu:
	def __init__(self, screen):
		self.screen = screen
		self.page = 0
		self.selectedButton = boutonNr.RIEN

	def leftClick(self):
		match self.selectedButton:
			case boutonNr.RIGHT:
				self.page += 1
			case boutonNr.LEFT:
				self.page -= 1
			case boutonNr.X:
				return True
		return False

	def draw(self):
		mousePos = pg.mouse.get_pos()
		self.screen.fill(menuBackgroundColor)
		self.screen.blit(reglesImg[self.page], reglesPos)
		imgL = boutonLeftImg
		imgR = boutonRightImg
		imgX = boutonXImg
		if self.page > 0 and boutonLRect.collidepoint(mousePos):
			imgL = boutonLeftImg2
			self.selectedButton = boutonNr.LEFT
		elif self.page < len(reglesImg) - 1 and boutonRRect.collidepoint(mousePos):
			imgR = boutonRightImg2
			self.selectedButton = boutonNr.RIGHT
		elif boutonXRect.collidepoint(mousePos):
			imgX = boutonXImg2
			self.selectedButton = boutonNr.X
		else:
			self.selectedButton = boutonNr.RIEN
		if self.page > 0:
			self.screen.blit(imgL, boutonLRect)
		if self.page < len(reglesImg) - 1:
			self.screen.blit(imgR, boutonRRect)
		self.screen.blit(imgX, boutonXRect)