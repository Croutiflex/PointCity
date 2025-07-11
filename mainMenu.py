import pygame as pg
import sys
from params import *
from rulesMenu import *

#dimensions
menuTitleH = screenSize[1]*3/4
menuTitleImg = pg.image.load("res/mainMenu/menu.png")
menuTitleRect = menuTitleImg.get_rect()
menuTitleRect.scale_by_ip(menuTitleH/menuTitleRect.h)
menuTitleRect.centerx = screenSize[0]/2
menuTitleRect.top = screenSize[1]/8
menuTitleImg = pg.transform.smoothscale(menuTitleImg, menuTitleRect.size)
boutonW = menuTitleRect.w/2
boutonResumeImg = pg.image.load("res/mainMenu/boutonResume.png")
(a,b) = boutonResumeImg.get_rect().size
boutonSize1 = (boutonW, boutonW*b/a)
boutonX = menuTitleRect.left + boutonW/2
boutonY = menuTitleRect.top + menuTitleRect.h/3
padding = boutonSize1[1]/2
HLratio = 1.05

# boutons
boutonRectx4 = [pg.Rect((boutonX, boutonY + i*(menuTitleRect.bottom-boutonY-padding)/4), boutonSize1) for i in range(4)]
boutonHLx4 = [b.scale_by(HLratio) for b in boutonRectx4]

# images
boutonResumeImg = pg.transform.smoothscale(boutonResumeImg, boutonSize1)
boutonReglesImg = pg.transform.smoothscale(pg.image.load("res/startMenu/boutonregles.png"), boutonSize1)
boutonExitImg = pg.transform.smoothscale(pg.image.load("res/mainMenu/exit.png"), boutonSize1)
boutonSaveImg = pg.transform.smoothscale(pg.image.load("res/mainMenu/boutonSave.png"), boutonSize1)
boutonSaveSlotImg = [pg.transform.smoothscale(pg.image.load("res/startMenu/saveSlot"+str(i+1)+".png"), boutonSize1) for i in range(4)]
page1BoutonsImg = [boutonResumeImg, boutonReglesImg, boutonSaveImg, boutonExitImg]

# sauvegardes actives
slotIsEmpty = [not os.path.exists("saves/save_"+str(i+1)) for i in range(4)]

# Nrs boutons
class boutonNr(IntEnum):
	RIEN = -1
	RESUME = 0
	REGLES = 1
	SAVEGAME = 2
	EXIT = 3
	PICKSLOT = 4

#
page1BoutonsList = [boutonNr.RESUME, boutonNr.REGLES, boutonNr.SAVEGAME, boutonNr.EXIT]

class mainMenu:
	def __init__(self, screen):
		self.screen = screen
		self.isActive = False
		self.redrawGame = False
		self.slot = 1
		self.mode = 0
		self.page = 0
		self.selectedButton = boutonNr.RIEN
		self.rules = rulesMenu(screen)

	def leftClick(self): # return True si une partie a été sauvegardée
		if self.mode == 1:
			if self.rules.leftClick():
				self.mode = 0
				self.rules.page = 0
				self.redrawGame = True
			self.selectedButton = boutonNr.RIEN
			return False
		match self.selectedButton:
			case boutonNr.RESUME:
				self.isActive = False
				self.mode = 0
				self.page = 0
			case boutonNr.EXIT:
				sys.exit()
			case boutonNr.REGLES:
				self.mode = 1
			case boutonNr.SAVEGAME:
				self.page = 1
			case boutonNr.PICKSLOT:
				self.page = 0
				return True
		return False

	def retour(self):
		if self.mode == 0: # menu principal
			if self.page == 1:
				self.page = 0
		elif self.mode == 1: # menu règles
			self.mode = 0
			self.rules.page = 0
			self.redrawGame = True
		self.selectedButton = boutonNr.RIEN

	def draw(self):
		mousePos = pg.mouse.get_pos()
		if self.mode == 0: # menu principal
			self.screen.blit(menuTitleImg, menuTitleRect)
			self.selectedButton = boutonNr.RIEN
			match self.page:
				case 0: # menu de départ
					for i in range(4):
						if boutonRectx4[i].collidepoint(mousePos):
							self.screen.fill(white, boutonHLx4[i])
							self.selectedButton = page1BoutonsList[i]
						self.screen.blit(page1BoutonsImg[i], boutonRectx4[i])
				case 1: # menu sélection sauvegarde
					for i in range(4):
						if boutonRectx4[i].collidepoint(mousePos):
							self.selectedButton = boutonNr.PICKSLOT
							self.slot = i+1
							self.screen.fill(white, boutonHLx4[i])
						self.screen.blit(boutonSaveSlotImg[i], boutonRectx4[i])
		else: # menu règles & commandes
			self.rules.draw()