import pygame as pg
from params import *
from rulesMenu import *
from playerSelectMenu import *
from utils import *

#dimensions
bannerY = screenSize[1]/2
banner = pg.image.load("res/startMenu/banner.png")
boutonPlayImg = pg.image.load("res/startMenu/play.png")
(a,b) = boutonPlayImg.get_rect().size
bannerRect = banner.get_rect()
bannerRect.scale_by_ip(bannerY/bannerRect.h)
bannerRect.centerx = screenSize[0]/2
bannerRect.top = 0
banner = pg.transform.smoothscale(banner, bannerRect.size)

w1 = screenSize[0]/5
boutonSize1 = (w1, w1*b/a)
btny1 = (screenSize[1] + bannerRect.centery)/2
btny2 = bannerRect.centery + (screenSize[1] - bannerRect.centery)/3
btny3 = bannerRect.centery + 2*(screenSize[1] - bannerRect.centery)/3

# sauvegardes actives
slotIsEmpty = [not os.path.exists("saves/save_"+str(i+1)) for i in range(4)]

class StartMenu:
	def __init__(self):
		self.cheatMode = False
		self.slot = 1
		self.nPlayers = None
		self.mode = 0
		self.page = 0
		self.selectedButton = None
		self.rules = None
		self.avSelect = None

		# boutons
		self.buttons = [] # boutons groupés par page du menu principal
		self.drawables = [] 
		self.closeButton = CloseButton()
		# page 0
		self.playBtn = Button("res/startMenu/play.png", "res/startMenu/play.png", boutonSize1, (w1, 0))
		self.playBtn.rect.centery = btny1
		self.rulesBtn = Button("res/startMenu/boutonregles.png", "res/startMenu/boutonregles.png", boutonSize1, (3*w1, 0))
		self.rulesBtn.rect.centery = btny1
		self.buttons.append([self.playBtn, self.rulesBtn, self.closeButton])
		self.drawables.append(pg.sprite.LayeredUpdates(self.buttons[0]))
		# page 1
		self.newgameBtn = Button("res/startMenu/newgame.png", "res/startMenu/newgame.png", boutonSize1, (w1, 0))
		self.newgameBtn.rect.centery = btny1
		self.loadgameBtn = Button("res/startMenu/loadgame.png", "res/startMenu/loadgame.png", boutonSize1, (3*w1, 0))
		self.loadgameBtn.rect.centery = btny1
		self.buttons.append([self.newgameBtn, self.loadgameBtn, self.closeButton])
		self.drawables.append(pg.sprite.LayeredUpdates(self.buttons[1]))
		# page 2
		self.j1Btn = Button("res/startMenu/1joueurs.png", "res/startMenu/1joueurs.png", boutonSize1, (w1, 0))
		self.j1Btn.rect.centery = btny2
		self.j2Btn = Button("res/startMenu/2joueurs.png", "res/startMenu/2joueurs.png", boutonSize1, (3*w1, 0))
		self.j2Btn.rect.centery = btny2
		self.j3Btn = Button("res/startMenu/3joueurs.png", "res/startMenu/3joueurs.png", boutonSize1, (w1, 0))
		self.j3Btn.rect.centery = btny3
		self.j4Btn = Button("res/startMenu/4joueurs.png", "res/startMenu/4joueurs.png", boutonSize1, (3*w1, 0))
		self.j4Btn.rect.centery = btny3
		self.buttons.append([self.j1Btn, self.j2Btn, self.j3Btn, self.j4Btn, self.closeButton])
		self.drawables.append(pg.sprite.LayeredUpdates(self.buttons[2]))
		# page 3
		self.save1Btn = Button("res/startMenu/saveSlot1.png", "res/startMenu/saveSlot1.png", boutonSize1, (w1, 0))
		self.save1Btn.rect.centery = btny2
		self.save2Btn = Button("res/startMenu/saveSlot2.png", "res/startMenu/saveSlot2.png", boutonSize1, (3*w1, 0))
		self.save2Btn.rect.centery = btny2
		self.save3Btn = Button("res/startMenu/saveSlot3.png", "res/startMenu/saveSlot3.png", boutonSize1, (w1, 0))
		self.save3Btn.rect.centery = btny3
		self.save4Btn = Button("res/startMenu/saveSlot4.png", "res/startMenu/saveSlot4.png", boutonSize1, (3*w1, 0))
		self.save4Btn.rect.centery = btny3
		self.buttons.append([self.save1Btn, self.save2Btn, self.save3Btn, self.save4Btn, self.closeButton])
		self.drawables.append(pg.sprite.LayeredUpdates(self.buttons[3]))
		# highlight
		self.HL = HighLightRect(white, boutonSize1[0]+2*space1, boutonSize1[1]+2*space1, 0,0)

	# renvoie True pour quitter le jeu
	def leftClick(self):
		ret = "nope"
		if self.mode == 1:
			if self.rules.leftClick():
				self.mode = 0
				# self.rules.reset()
		elif self.mode == 2:
			match self.avSelect.leftClick():
				case "close":
					self.mode = 0
					self.page = 2
				case "ready":
					av = self.avSelect.picked
					if self.nPlayers == 1:
						av.append(-1)
					self.avatars = av
					return "newgame"
		else:
			selectAv = False
			match self.selectedButton:
				case self.closeButton:
					return "close"
				case self.rulesBtn:
					self.rules = RulesMenu()
					self.mode = 1
				case self.playBtn:
					self.page = 1
				case self.newgameBtn:
					self.page = 2
				case self.loadgameBtn:
					self.page = 3
				case self.j1Btn:
					self.nPlayers = 1
					selectAv = True
				case self.j2Btn:
					self.nPlayers = 2
					selectAv = True
				case self.j3Btn:
					self.nPlayers = 3
					selectAv = True
				case self.j4Btn:
					self.nPlayers = 4
					selectAv = True
				case self.save1Btn:
					self.slot = 1
					return "loadgame"
				case self.save2Btn:
					self.slot = 2
					return "loadgame"
				case self.save3Btn:
					self.slot = 3
					return "loadgame"
				case self.save4Btn:
					self.slot = 4
					return "loadgame"
			if selectAv:
				self.avSelect = PlayerSelectMenu(self.nPlayers)
				self.mode = 2
		self.selectedButton = None
		return ret

	def retour(self):
		match self.mode:
			case 0: # menu principal
				if self.page > 1:
					self.page = 1
				elif self.page == 1:
					self.page = 0
			case 1: # menu règles
				self.mode = 0
				# self.rules.reset()
			case 2: # menu sel. avatars
				self.mode = 0
				self.page = 2
				# self.avSelect.reset()
		self.selectedButton = None

	def cheatOrNotCheat(self):
		self.cheatMode = not self.cheatMode
		print("cheatMode : "+str(self.cheatMode))

	def update(self):
		if self.mode == 1: # menu règles & commandes
			self.rules.update()
		elif self.mode == 2: # menu sélection avatars
			self.avSelect.update()
		else: # menu principal
			self.drawables[self.page].update()
			L = [b for b in self.buttons[self.page] if b.isSelected]
			self.selectedButton = L[0] if len(L) > 0 else None
			if self.selectedButton and self.selectedButton != self.closeButton:
				self.HL.move(self.selectedButton.rect.center)
				self.drawables[self.page].add(self.HL)
			else:
				self.drawables[self.page].remove(self.HL)

	def draw(self, screen):
		if self.mode == 1: # menu règles & commandes
			self.rules.draw(screen)
		elif self.mode == 2: # menu sélection avatars
			self.avSelect.draw(screen)
		else: # menu principal
			screen.fill(menuBackgroundColor)
			screen.blit(banner, bannerRect)
			self.drawables[self.page].draw(screen)