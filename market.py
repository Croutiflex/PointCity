import pygame as pg
from params import *

# card positions :
# 0 1 2 3
# 4 5 6 7
# 8 9 10 11
# 12 13 14 15
class pointCityMarket:
	def __init__(self, screen, cards, modeSolo=False):
		self.screen = screen
		self.modeSolo = modeSolo
		self.automaCards = [4, 8] if modeSolo else []
		self.selectedCards = []
		self.adjCards = []
		self.lastMousePos = -1
		self.cards = pg.sprite.RenderUpdates()
		self.highlightOn = pg.sprite.RenderUpdates()
		(x,y) = marketPos
		for i in range(4):
			x = marketPos[0]
			for j in range(4):
				card = cards.pop()
				card.rect = card.image.get_rect(x=x, y=y)
				self.cards.add(card)
				self.highlightOn.add(cardHighLight(backgroundColor, 2*space1+cardSize[0], 2*space1+cardSize[1], x-space1, y-space1))
				x += cardSize[0] + space2
			y += cardSize[1] + space2

	def update(self):
		pass

	# si la souris est sur une carte, renvoie ses coordonnées. sinon -1.
	def findCard(self, mousePos):
		for i in range(16):
			if self.card[i].rect.collidepoint(mousePos):
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
	def flipCard(self, mousePos):
		i = self.findCard(mousePos)
		if i == -1:
			return False
		if self.cards[i].flip():
			self.updateFlip()
			return True
		return False

	# renvoie la liste des cartes sélectionnées
	def selectCard(self, mousePos):
		i = self.findCard(mousePos)
		if i == -1:
			return self.selectedCards
		if len(self.selectedCards) == 0:
			self.selectedCards.append(i)
			self.highlightOn[i].set_color(blue)
			self.adjCards = self.findAdjacent(i)
			return self.selectedCards
		elif len(self.selectedCards) == 1:
			if i in self.adjCards:
				self.adjCards = []
				L = self.selectedCards
				L.append(i)
				self.selectedCards = []
				return L
			else:
				return self.selectedCards

	def cancelSelect(self):
		if len(self.selectedCards) > 0:
			self.highlightOn[self.selectedCards[0]].set_color(backgroundColor)
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

	def draw(self, gamePhase):
		(x,y) = self.findCard(pg.mouse.get_pos())
		# self.screen.fill(backgroundColor, marketBackgroundRect)
		match gamePhase:
			case GPhase.DISCOVER:
				for i in range(4):
					for j in range(4):
						if self.cards[i][j].canFlip:
							self.screen.fill(green, self.highlightRects[i][j])
				if x != -1 and self.cards[x][y].canFlip:
					self.screen.fill(white, self.highlightRects[x][y])
			case GPhase.MARKET:
				for (i,j) in self.automaCards:
					self.screen.fill(orange, self.highlightRects[i][j])
				if len(self.selectedCards) == 1:
					(i,j) = self.selectedCards[0]
					self.screen.fill(blue, self.highlightRects[i][j])
					if (x,y) in self.adjCards:
						self.screen.fill(white, self.highlightRects[x][y])
				elif x != -1:
					self.screen.fill(white, self.highlightRects[x][y])

		for i in range(4):
			for j in range(4):
				if self.cards[i][j] != None:
					self.cards[i][j].draw(self.cardPos[i][j])

	def lazyDraw(self, gamePhase): # deprecated
		(x,y) = self.findCard(pg.mouse.get_pos())
		(a,b) = self.lastMousePos
		if (x,y) == (a,b):
			return
		match gamePhase:
			case GPhase.DISCOVER:
				if x != -1:
					self.drawSingleCard((x,y), white)
				if a != -1:
					self.drawSingleCard((a,b), green if self.cards[a][b].canFlip else backgroundColor)
			case GPhase.MARKET:
				if len(self.selectedCards) == 1:
					if (x,y) in self.adjCards:
						self.drawSingleCard((x,y), white)
				elif x != -1:
					self.drawSingleCard((x,y), white)
				if a != -1:
					if len(self.selectedCards) != 1 or self.selectedCards[0] != (a,b):
						self.drawSingleCard((a,b), backgroundColor)
		self.lastMousePos = (x,y)

	def drawSingleCard(self, card, color):
		# print("last draw: ", card, color)
		(i,j) = card
		self.screen.fill(color, self.highlightRects[i][j])
		self.cards[i][j].draw(self.cardPos[i][j])