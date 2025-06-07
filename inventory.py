from params import *
import pygame as pg
from baseObjects import *

class pointCityPlayerInventory:
	def __init__(self, Id):
		card = pointCityCard(0, INGENIEUR, 'ressource', 0, 0, 0)
		card.imageRes = pg.transform.scale(card.imageRes, cardSize2)
		self.resCards = [card]
		self.batCards = []
		self.tokens = []
		self.id = Id
		self.pos = Id
		self.tokenPosL = [(tokenPosLX[i], tokenPosLY) for i in range(2)]
		self.handPosL = [handPosL]
		self.hasRecentlyChanged = False

	def endTurn(self, n):
		self.hasRecentlyChanged = True
		p = self.pos - 1
		self.pos = p if p >= 0 else n-1

	def addToken(self, token):
		self.hasRecentlyChanged = True
		self.tokens.append(token)
		L = len(self.tokens)
		if L > 2:
			if L%2 == 0:
				self.tokenPosL.append((self.tokenPosL[L-3][0], self.tokenPosL[L-2][1]))
			else:
				self.tokenPosL.append((self.tokenPosL[L-3][0], self.tokenPosL[L-3][1] + tokenSize2 + space1))

	def addResCard(self, card):
		self.hasRecentlyChanged = True
		card.imageRes = pg.transform.scale(card.imageRes, cardSize2)
		self.resCards.append(card)
		self.handPosL = []
		(x,y) = handPosL
		space = ((3/8)*PIL - 2*space1 - cardSize[0])/len(self.resCards)
		for c in self.resCards:
			self.handPosL.append((x,y))
			x += space

	def draw(self, screen):
		screen.fill(playerColors[self.id], PIRect[self.pos])
		if self.pos == 0: # inventaire détaillé
			# jetons
			for tk in range(len(self.tokens)):
				self.tokens[tk].draw(screen, self.tokenPosL[tk])
			# main
			for i in range(len(self.resCards)):
				self.resCards[i].draw(screen, self.handPosL[i])
			# bat. ressources
			for i in range(len(self.resCards)):
				pass
		else: # inventaire réduit
			pass

	def lazyDraw(self, screen):
		if self.hasRecentlyChanged:
			self.draw(screen)
			self.hasRecentlyChanged = False