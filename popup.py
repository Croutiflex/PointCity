import pygame as pg
import time
from params import *

class popUp:
	def __init__(self, screen, image, pos, timed=False, duration=2):
		self.screen = screen
		self.image = image
		self.pos = pos
		self.rect = image.get_rect()
		self.rect.center = pos
		self.timed = timed
		if timed:
			self.duration = duration
			self.startTime = time.time()
			self.done = False
		else:
			self.on = False

	def drawSingle(self):
		# draw_rect_alpha(self.screen, transparent, self.screen.get_rect()) # test voile transparent
		self.screen.blit(self.image, self.rect)

	def drawTimed(self):
		if self.done:
			return
		self.drawSingle()
		if time.time() - self.startTime >= self.duration:
			self.done = True

	def draw(self):
		if self.timed:
			self.drawTimed()
		else:
			self.drawSingle()



class nextTurnPopUp(popUp):
	def __init__(self, screen, image, pos, timed=False, duration=2):
		super().__init__(screen, image, pos, timed, duration)
		self.rect.center = (pos[0], pos[1] - screenSize[1]/10)
		self.playerImage = playerTitleImg[0]
		self.playerRect = self.playerImage.get_rect()
		self.playerRect.center = (pos[0] - self.playerRect.w/2 - space2, pos[1] + screenSize[1]/20)
		font = pg.font.Font('freesansbold.ttf', fontsize2)
		self.text = font.render(str("C'est à vous!"), True, darkBlue, backgroundColor)
		self.textRect = self.text.get_rect()
		self.textRect.center = (pos[0] + self.textRect.w/2 + space2, pos[1] + screenSize[1]/20)

	def setNextPlayer(self, avatar, player):
		self.image = avatar
		self.playerImage = playerTitleImg[player]

	def drawSingle(self):
		super().drawSingle()
		self.screen.blit(self.playerImage, self.playerRect)
		self.screen.blit(self.text, self.textRect)

