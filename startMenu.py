import pygame as pg
from params import *

#dimensions
bannerY = screenSize[1]/2
banner = pg.image.load("res/startMenu/banner.png")
boutonPlayImg = pg.image.load("res/startMenu/play.png")
(a,b) = boutonPlayImg.get_rect().size
bannerRect = banner.get_rect()
bannerRect.scale_by_ip(bannerY/bannerRect.h)
bannerRect.centerx = screenSize[0]/2
bannerRect.top = 0
HLratio = 1.05
banner = pg.transform.scale(banner, bannerRect.size)

w1 = screenSize[0]/5
boutonSize1 = (w1, w1*b/a)

# boutons
boutonPlayRect = pg.Rect((w1, 0), boutonSize1)
boutonPlayRect.centery = (screenSize[1] + bannerRect.centery)/2
boutonPlayHL = boutonPlayRect.scale_by(HLratio)
boutonReglesRect = boutonPlayRect.move(2*w1, 0)
boutonReglesHL = boutonReglesRect.scale_by(HLratio)

# images
boutonPlayImg = pg.transform.scale(pg.image.load("res/startMenu/play.png"), boutonSize1)
boutonReglesImg = pg.transform.scale(pg.image.load("res/startMenu/boutonregles.png"), boutonSize1)
boutonNewGameImg = pg.transform.scale(pg.image.load("res/startMenu/newgame.png"), boutonSize1)
pageBackGround = [pg.transform.scale(pg.image.load("res/startMenu/"+str(i)+".png"), screenSize) for i in range(1)]

# codes boutons
class code(IntEnum):
	RIEN = -1
	JOUER = 0
	REGLES = 1

class startMenu:
	def __init__(self, screen):
		self.screen = screen
		self.nPlayers = 0
		self.mode = 0
		self.page = 0
		self.selectedButton = code.RIEN

	def leftClick(self, mousePos):
		endMenu = False
		match self.selectedButton:
			case code.JOUER:
				self.nPlayers = 2
				endMenu = True
		return endMenu

	def draw(self):
		mousePos = pg.mouse.get_pos()
		if self.mode == 0: # menu principal
			self.screen.fill(menuBackgroundColor)
			self.screen.blit(banner, bannerRect)
			match self.page:
				case 0:
					if boutonPlayRect.collidepoint(mousePos):
						self.selectedButton = code.JOUER
						self.screen.fill(white, boutonPlayHL)
					elif boutonReglesRect.collidepoint(mousePos):
						self.selectedButton = code.REGLES
						self.screen.fill(white, boutonReglesHL)
					else:
						self.selectedButton = code.RIEN

					self.screen.blit(boutonPlayImg, boutonPlayRect)
					self.screen.blit(boutonReglesImg, boutonReglesRect)
		else: # menu aide & commandes
			self.screen.blit(pageBackGround[self.page], (0,0))