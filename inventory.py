from params import *
import pygame as pg
from baseObjects import *

class pointCityPlayerInventory:
	def __init__(self, screen, Id):
		self.screen = screen
		card = pointCityCard(screen, 0, INGENIEUR, 'ressource', 0, 0, 0)
		card.imageRes = pg.transform.scale(card.imageRes, cardSize2)
		self.resCards = [card]
		self.batCards = [[] for i in range(5)]
		self.tokens = []
		self.id = Id
		self.pos = Id
		self.tokenPosL = [(tokenPosLX[i], tokenPosLY) for i in range(2)]
		self.handPosL = [handPosL]
		self.cityPosL = [[] for i in range(5)]
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

	def addCard(self, card):
		card.resize(cardSize2)
		if card.side == RESSOURCE:
			self.addResCard(card)
		else:
			self.addBatCard(card)

	def addResCard(self, card):
		self.hasRecentlyChanged = True
		self.resCards.append(card)
		self.handPosL = []
		(x,y) = handPosL
		space = ((3/8)*PIL - 2*space1 - cardSize[0])/len(self.resCards)
		for c in self.resCards:
			self.handPosL.append((x,y))
			x += space

	def addBatCard(self, card):
		self.hasRecentlyChanged = True
		if card.type == "ressource":
			self.batCards[card.ressource].append(card)
			if len(self.cityPosL[card.ressource]) == 0:
				self.cityPosL[card.ressource].append(cityPosL[card.ressource])
			else:
				space = space3
				(x,y) = self.cityPosL[card.ressource][-1]
				self.cityPosL[card.ressource].append((x, y + space))

	def drawBatCards(self, ressource):
		for i in range(len(self.batCards[ressource])):
			self.batCards[ressource][i].draw(self.cityPosL[ressource][i])

	def draw(self):
		self.screen.fill(playerColors[self.id], PIRect[self.pos])
		if self.pos == 0: # inventaire détaillé
			# jetons
			for tk in range(len(self.tokens)):
				self.tokens[tk].draw(self.tokenPosL[tk])
			# main
			for i in range(len(self.resCards)):
				self.resCards[i].draw(self.handPosL[i])
			# bat. ressources
			for res in range(5):
				self.drawBatCards(res)
		else: # inventaire réduit
			pass

	def lazyDraw(self):
		if self.hasRecentlyChanged:
			self.draw()
			self.hasRecentlyChanged = False