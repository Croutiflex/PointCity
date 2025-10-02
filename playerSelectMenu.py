import pygame as pg
from params import *
from utils import *

HLratio = 1.05
textPos = (screenSize[0]/2, screenSize[1]/3)
avL2 = screenSize[1]/8
avatarSize2 = (avL2, avL2)

class PlayerSelectMenu:
	def __init__(self, nPlayers):
		self.nPlayers = nPlayers
		self.choosingPlayer = 0
		self.closeButton = CloseButton()
		self.avatars = pg.sprite.RenderPlain()
		for i in range(6):
			self.avatars.add(AvatarSelect(i, ((1+i)*screenSize[0]/7, screenSize[1]/2)))
		for i in range(6):
			self.avatars.add(AvatarSelect(i+6, ((1+i)*screenSize[0]/7, screenSize[1]*3/4)))

		self.HL = HighLightRect(white, avatarSize2[0]+2*space1, avatarSize2[1]+2*space1, 0,0)
		self.drawables = pg.sprite.LayeredUpdates(self.avatars.sprites())
		self.drawables.add(self.closeButton)
		self.BGColor = playerColors[self.choosingPlayer]
		self.text = font2.render(str("Joueur " + str(self.choosingPlayer+1) + ", choisissez un avatar"), True, darkBlue, self.BGColor)
		self.currentPick = None
		self.picked = []

	# renvoie "close" si le jeu ferme, "ready" si on peut lancer une partie, ou "nope" s'il ne se passe rien
	def leftClick(self):
		if self.closeButton.isSelected:
			return "close"
		elif self.currentPick != None:
			self.picked.append(self.currentPick.avatarNum)
			self.choosingPlayer += 1
			if self.choosingPlayer == self.nPlayers:
				return "ready"
			else:
				self.avatars.remove(self.currentPick)
				self.drawables.remove(self.currentPick)
				self.BGColor = playerColors[self.choosingPlayer]
				self.text = font2.render(str("Joueur " + str(self.choosingPlayer+1) + ", choisissez un avatar"), True, darkBlue, self.BGColor)
		return "nope"

	def update(self):
		self.closeButton.update()
		collide = pg.sprite.spritecollide(Point(pg.mouse.get_pos()), self.avatars, 0)
		self.currentPick = collide[0] if len(collide) > 0 else None
		if self.currentPick:
			self.HL.move(self.currentPick.rect.center)
			self.drawables.add(self.HL)
		else:
			self.drawables.remove(self.HL)

	def draw(self, screen):
		screen.fill(self.BGColor)
		rect = self.text.get_rect()
		rect.center = textPos
		screen.blit(self.text, rect)
		self.drawables.draw(screen)

class AvatarSelect(pg.sprite.Sprite):
	def __init__(self, avatarNum, center):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.transform.smoothscale(avatarImg[avatarNum], avatarSize2)
		self.rect = self.image.get_rect(center = center)
		self.avatarNum = avatarNum
		self.layer = 2