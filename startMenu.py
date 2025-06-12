import pygame as pg
import sys
from params import *
from pointcity import *
from rulesMenu import *

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
banner = pg.transform.smoothscale(banner, bannerRect.size)

w1 = screenSize[0]/5
boutonSize1 = (w1, w1*b/a)

# boutons
bouton1Rect = pg.Rect((w1, 0), boutonSize1)
bouton1Rect.centery = (screenSize[1] + bannerRect.centery)/2
bouton1HL = bouton1Rect.scale_by(HLratio)
bouton2Rect = bouton1Rect.move(2*w1, 0)
bouton2HL = bouton2Rect.scale_by(HLratio)
boutonGroup1 = [bouton1Rect, bouton2Rect]
boutonHLGroup1 = [bouton1HL, bouton2HL]

bouton3Rect = bouton1Rect.copy()
bouton3Rect.centery = bannerRect.centery + (screenSize[1] - bannerRect.centery)/3
bouton3HL = bouton3Rect.scale_by(HLratio)
bouton4Rect = bouton1Rect.copy()
bouton4Rect.centery = bannerRect.centery + 2*(screenSize[1] - bannerRect.centery)/3
bouton4HL = bouton4Rect.scale_by(HLratio)
bouton5Rect = bouton3Rect.move(2*w1, 0)
bouton5HL = bouton5Rect.scale_by(HLratio)
bouton6Rect = bouton4Rect.move(2*w1, 0)
bouton6HL = bouton6Rect.scale_by(HLratio)
boutonGroup2 = [bouton3Rect, bouton4Rect, bouton5Rect, bouton6Rect]
boutonHLGroup2 = [bouton3HL, bouton4HL, bouton5HL, bouton6HL]

# images
boutonPlayImg = pg.transform.smoothscale(pg.image.load("res/startMenu/play.png"), boutonSize1)
boutonReglesImg = pg.transform.smoothscale(pg.image.load("res/startMenu/boutonregles.png"), boutonSize1)
boutonNewGameImg = pg.transform.smoothscale(pg.image.load("res/startMenu/newgame.png"), boutonSize1)
boutonLoadGameImg = pg.transform.smoothscale(pg.image.load("res/startMenu/loadgame.png"), boutonSize1)
boutonJImg = [pg.transform.smoothscale(pg.image.load("res/startMenu/"+str(i)+"joueurs.png"), boutonSize1) for i in range(1,5)]
boutonSaveImg = [pg.transform.smoothscale(pg.image.load("res/startMenu/saveSlot"+str(i+1)+".png"), boutonSize1) for i in range(4)]

# Nrs boutons
class boutonNr(IntEnum):
	RIEN = -1
	JOUER = 0
	REGLES = 1
	NEWGAME = 2
	LOADGAME = 3
	PICKNP = 4
	X = 5
	LOADSAVE = 6

class startMenu:
	def __init__(self, screen):
		self.screen = screen
		self.cheatMode = False
		self.slot = 1
		self.nPlayers = 1
		self.mode = 0
		self.page = 0
		self.selectedButton = boutonNr.RIEN
		self.rules = rulesMenu(screen)

	def leftClick(self):
		PCgame = None
		if self.mode == 1:
			if self.rules.leftClick():
				self.mode = 0
				self.rules.page = 0
			self.selectedButton = boutonNr.RIEN
			return PCgame
		match self.selectedButton:
			case boutonNr.X:
				sys.exit()
			case boutonNr.REGLES:
				self.mode = 1
			case boutonNr.JOUER:
				self.page = 1
			case boutonNr.NEWGAME:
				self.page = 2
			case boutonNr.PICKNP:
				PCgame = pointCityGame(self.screen, False, nPlayers=self.nPlayers, cheatMode=self.cheatMode)
			case boutonNr.LOADGAME:
				self.page = 3
			case boutonNr.LOADSAVE:
				print("chargement partie ", self.slot)
				PCgame = pointCityGame(self.screen, True, saveSlot=self.slot)
		return PCgame

	def retour(self):
		if self.mode == 0: # menu principal
			if self.page > 1:
				self.page = 1
			elif self.page == 1:
				self.page = 0
		elif self.mode == 1: # menu règles
			self.mode = 0
			self.rules.page = 0
		self.selectedButton = boutonNr.RIEN

	def cheatOrNotCheat(self):
		self.cheatMode = not self.cheatMode
		print("cheatMode : "+str(self.cheatMode))

	def draw(self):
		mousePos = pg.mouse.get_pos()
		if self.mode == 0: # menu principal
			self.screen.fill(menuBackgroundColor)
			self.screen.blit(banner, bannerRect)
			if boutonXRect.collidepoint(mousePos):
				self.selectedButton = boutonNr.X
				self.screen.blit(boutonXImg2, boutonXRect)
			else: 
				self.selectedButton = boutonNr.RIEN
				self.screen.blit(boutonXImg, boutonXRect)
			match self.page:
				case 0: # menu de départ
					if bouton1Rect.collidepoint(mousePos):
						self.selectedButton = boutonNr.JOUER
						self.screen.fill(white, bouton1HL)
					elif bouton2Rect.collidepoint(mousePos):
						self.selectedButton = boutonNr.REGLES
						self.screen.fill(white, bouton2HL)

					self.screen.blit(boutonPlayImg, bouton1Rect)
					self.screen.blit(boutonReglesImg, bouton2Rect)
				case 1: # menu jouer
					if bouton1Rect.collidepoint(mousePos):
						self.selectedButton = boutonNr.NEWGAME
						self.screen.fill(white, bouton1HL)
					elif bouton2Rect.collidepoint(mousePos):
						self.selectedButton = boutonNr.LOADGAME
						self.screen.fill(white, bouton2HL)

					self.screen.blit(boutonNewGameImg, bouton1Rect)
					self.screen.blit(boutonLoadGameImg, bouton2Rect)
				case 2: # menu sélection nb joueurs
					for i in range(4):
						if boutonGroup2[i].collidepoint(mousePos):
							self.selectedButton = boutonNr.PICKNP
							self.nPlayers = i+1
							self.screen.fill(white, boutonHLGroup2[i])
						self.screen.blit(boutonJImg[i], boutonGroup2[i])
				case 3: # menu sélection sauvegarde
					for i in range(4):
						if boutonGroup2[i].collidepoint(mousePos):
							self.selectedButton = boutonNr.LOADSAVE
							self.slot = i+1
							self.screen.fill(white, boutonHLGroup2[i])
						self.screen.blit(boutonSaveImg[i], boutonGroup2[i])
		else: # menu règles & commandes
			self.rules.draw()