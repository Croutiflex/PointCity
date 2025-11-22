import pygame as pg
from params import *
from utils import *
import time

w, h = 2*space1+cardSize[0][0], 2*space1+cardSize[0][1]
# card positions :
# 0 1 2 3
# 4 5 6 7
# 8 9 10 11
# 12 13 14 15
class PointCityMarket:
	def __init__(self, cards, modeSolo=False):
		self.modeSolo = modeSolo
		self.gamePhase = GPhase.DISCOVER
		self.selectedCards = []
		self.adjCards = []

		self.cards = cards
		(x,y) = marketPos
		for i in range(4):
			x = marketPos[0]
			for j in range(4):
				self.cards[i*4+j].move((x,y))
				x += cardSize[0][0] + space2
			y += cardSize[0][1] + space2
		self.drawables = pg.sprite.LayeredUpdates(self.cards)
		self.blueHL = HighLightRect(blue, w, h, layer=-2)
		self.whiteHL = HighLightRect(white, w, h)
		self.redHL = [HighLightRect(red, w, h), HighLightRect(red, w, h)]
		self.redHLTimer = 0
		self.lastFrameTime = None
		if modeSolo:
			self.automaCards = [4, 8]
			self.automaHL = [HighLightRect(orange, w, h, layer=-1) for i in range(2)]
			self.drawables.add(self.automaHL)

		self.greenHL = pg.sprite.RenderPlain(self.cards)
		self.updateFlip()

	def goToNewTurn(self):
		if self.modeSolo:
			self.drawables.add(self.automaHL)
		self.updateFlip()
		if self.canFlip():
			self.gamePhase = GPhase.DISCOVER
		else:
			self.gamePhase = GPhase.MARKET

	def endMarketPhase(self):
		self.selectedCards = []
		self.adjCards = []
		self.drawables.remove(self.whiteHL)
		self.drawables.remove(self.automaHL)
		self.drawables.remove(self.blueHL)

	# si la souris est sur une carte, renvoie sa position. sinon -1.
	def findCard(self):
		for i in range(16):
			if self.cards[i].rect.collidepoint(pg.mouse.get_pos()):
				return i
		return -1

	def findAdjacent(self, i):
		ret = []
		if i > 3:
			ret.append(i-4)
		if i < 12:
			ret.append(i+4)
		if i%4 > 0:
			ret.append(i-1)
		if i%4 < 3:
			ret.append(i+1)
		return ret

	# renvoie True si une carte a été retournée, false sinon
	def flipCard(self):
		i = self.findCard()
		if i == -1:
			return False
		if self.cards[i].flip():
			self.gamePhase = GPhase.MARKET
			return True
		return False

	# renvoie True si on sélectionne la 2e carte
	def selectCard(self):
		i = self.findCard()
		if i == -1:
			return False
		self.selectedCards.append(i)
		if len(self.selectedCards) == 1: # sélection première carte
			self.blueHL.moveC(self.cards[i].rect.center)
			self.drawables.add(self.blueHL)
			self.adjCards = self.findAdjacent(i)
			return False
		elif len(self.selectedCards) == 2: # sélection 2e carte
			if i in self.adjCards:
				self.drawables.remove(self.blueHL)
				self.selectedCards.sort()
				return True

	def getSelectedCards(self):
		return [self.cards[i] for i in self.selectedCards]

	def cancelSelect(self):
		if len(self.selectedCards) > 0:
			self.drawables.remove(self.blueHL)
			self.selectedCards = []
			self.adjCards = []

	def updateFlip(self):
		# horizontally
		for i in range(4):
			v = True
			for j in range(4):
				if self.cards[i//4 + j].side == BATIMENT:
					v = False
					break
			for k in range(4):
			 	self.cards[i//4 + k].canFlip = v
		# vertically
		for j in range(4):
			v = True
			for i in range(4):
				if self.cards[i//4 + j].side == BATIMENT:
					v = False
					break
			for k in range(4):
			 	self.cards[k//4 + j].canFlip = v or self.cards[k//4 + j].canFlip
		# update green HL
		self.greenHL.empty()
		for c in self.cards:
			if c.canFlip:
				self.greenHL.add(HighLightRect(green, w, h, layer=0,pos=c.rect.center))

	# can we flip a card?
	def canFlip(self):
		for card in self.cards:
			if card.canFlip:
				return True
		return False

	def moveAutomaCards(self):
		for x in range(2):
			i = self.automaCards.pop(0)
			if i == 15:
				i = 0
			elif i%4 == 3:
				i += 1
			elif i > 11:
				i -= 11
			else:
				i += 5
			self.automaCards.append(i)
			self.automaHL[x].moveC(cards[i].rect.center)

	def failedBuy(self):
		i = 0
		for j in self.selectedCards:
			self.redHL[i].moveC(self.cards[j].rect.center)
			i += 1
		self.drawables.add(self.redHL)
		self.selectedCards = []
		self.redHLTimer = failedBuyIndicationTime
		self.lastFrameTime = time.time()

	def update(self):
		if self.gamePhase == GPhase.MARKET:
			if self.redHLTimer > 0:
				now = time.time()
				dt = now - self.lastFrameTime
				self.lastFrameTime = now
				self.redHLTimer -= dt
				if self.redHLTimer <= 0:
					self.drawables.remove(self.redHL)
			i = self.findCard()
			if i == -1:
				self.drawables.remove(self.whiteHL)
			elif len(self.selectedCards) == 1:
				if i in self.adjCards:
					self.whiteHL.moveC(self.cards[i].rect.center)
					self.drawables.add(self.whiteHL)
				else:
					self.drawables.remove(self.whiteHL)
			else:
				self.whiteHL.moveC(self.cards[i].rect.center)
				self.drawables.add(self.whiteHL)
		elif self.gamePhase == GPhase.DISCOVER:
			i = self.findCard()
			if i == -1:
				self.drawables.remove(self.whiteHL)
			else:
				self.whiteHL.moveC(self.cards[i].rect.center)
				self.drawables.add(self.whiteHL)

	def draw(self, screen):
		if self.gamePhase == GPhase.DISCOVER:
			self.greenHL.draw(screen)
		self.drawables.draw(screen)