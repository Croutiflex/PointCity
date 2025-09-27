import pygame as pg
import sys
from params import *
from pointcity import *

HLratio = 1.05
textPos = (screenSize[0]/2, screenSize[1]/3)
avL2 = screenSize[1]/8
avatarSize2 = (avL2, avL2)
avatarImgs = [pg.transform.smoothscale(av, avatarSize2) for av in avatarImg]
avatarRect = [av.get_rect() for av in avatarImgs]
for i in range(6):
	avatarRect[i].center = ((1+i)*screenSize[0]/7, screenSize[1]/2)

for i in range(6):
	avatarRect[i+6].center = ((1+i)*screenSize[0]/7, screenSize[1]*3/4)

avatarHL = [avR.scale_by(HLratio) for avR in avatarRect]

h2 = screenSize[1]/20
boutonSize2 = (h2, h2)
boutonXRect = pg.Rect((screenSize[0] - h2*2, h2), boutonSize2)
boutonXImg = pg.transform.smoothscale(pg.image.load("res/X.png"), boutonSize2)
boutonXImg2 = pg.transform.smoothscale(pg.image.load("res/X2.png"), boutonSize2)

class playerSelectMenu:
	def __init__(self, screen, nPlayers):
		self.screen = screen
		self.font = pg.font.Font('freesansbold.ttf', fontsize2)
		self.nPlayers = nPlayers
		self.choosingPlayer = 0
		self.text = "Joueur " + str(self.choosingPlayer+1) + ", choisissez un avatar"
		self.BGColor = playerColors[self.choosingPlayer]
		self.currentButton = None
		self.selectedAvatar = [None for i in range(nPlayers)]

	def leftClick(self):
		# print(self.currentButton)
		if self.currentButton == -1:
			sys.exit()
		elif self.currentButton != None:
			self.selectedAvatar[self.choosingPlayer] = self.currentButton
			self.choosingPlayer += 1
			if self.choosingPlayer == self.nPlayers:
				return True
			print(self.selectedAvatar, self.choosingPlayer)
			self.BGColor = playerColors[self.choosingPlayer]
			self.text = "Joueur " + str(self.choosingPlayer+1) + ", choisissez un avatar"
			print("selectedAvatar: ", self.selectedAvatar, ", choosingPlayer: ", self.choosingPlayer, ", currentButton: ", self.currentButton)
		return False

	def draw(self):
		# print("selectedAvatar: ", self.selectedAvatar, ", choosingPlayer: ", self.choosingPlayer, ", currentButton: ", self.currentButton)
		self.screen.fill(self.BGColor)

		mousePos = pg.mouse.get_pos()

		text = self.font.render(str(self.text), True, darkBlue, self.BGColor)
		rect = text.get_rect()
		rect.center = textPos
		self.screen.blit(text, rect)

		if boutonXRect.collidepoint(mousePos):
			self.currentButton = -1
			self.screen.blit(boutonXImg2, boutonXRect)
		else: 
			self.currentButton = None
			self.screen.blit(boutonXImg, boutonXRect)

		for i in range(12):
			if i not in self.selectedAvatar:
				if avatarRect[i].collidepoint(mousePos):
					self.currentButton = i
					self.screen.fill(white, avatarHL[i])
				self.screen.blit(avatarImgs[i], avatarRect[i])