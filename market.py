import pygame as pg
from params import *

class pointCityMarket:
	def __init__(self, screen, cards):
		self.screen = screen
		self.cards = cards
		self.cardPos = []
		self.selectedCards = []
		self.adjCards = []
		self.highlightRects = []
		self.lastMousePos = (-1, -1)
		(x,y) = marketPos
		for i in range(4):
			L = []
			R = []
			C = []
			x = marketPos[0]
			for j in range(4):
				L.append((x,y))
				R.append(pg.Rect(x-space1, y-space1, 2*space1+cardSize[0], 2*space1+cardSize[1]))
				x += cardSize[0] + space2
			self.cardPos.append(L)
			self.highlightRects.append(R)
			y += cardSize[1] + space2

	# si la souris est sur une carte, renvoie ses coordonnées. sinon (-1,-1).
	def findCard(self, mousePos):
		for i in range(4):
			for j in range(4):
				if self.highlightRects[i][j].collidepoint(mousePos):
					return (i,j)
		return (-1,-1)

	def findAdjacent(self, i, j):
		ret = []
		if i > 0:
			ret.append((i-1,j))
		if i < 3:
			ret.append((i+1,j))
		if j > 0:
			ret.append((i,j-1))
		if j < 3:
			ret.append((i,j+1))
		return ret

	# renvoie True si une carte a été retournée, false sinon
	def flipCard(self, mousePos):
		(i,j) = self.findCard(mousePos)
		if i == -1:
			return
		if self.cards[i][j].flip():
			self.updateFlip()
			return True
		return False

	# renvoie la liste des cartes sélectionnées
	def selectCard(self, mousePos):
		(i,j) = self.findCard(mousePos)
		if i == -1:
			return []
		if len(self.selectedCards) == 0:
			self.selectedCards.append((i,j))
			self.drawSingleCard((i,j), blue)
			self.adjCards = self.findAdjacent(i,j)
			return self.selectedCards
		elif len(self.selectedCards) == 1:
			if (i,j) in self.adjCards:
				self.adjCards = []
				L = self.selectedCards
				L.append((i,j))
				self.selectedCards = []
				return L
			else:
				return self.selectedCards

	def cancelSelect(self):
		self.drawSingleCard(self.selectedCards[0], backgroundColor)
		self.selectedCards = []
		self.adjCards = []

	def updateFlip(self):
		# horizontally
		for i in range(4):
			v = True
			for j in range(4):
				if self.cards[i][j].side == BATIMENT:
					v = False
					break
			for k in range(4):
			 	self.cards[i][k].canFlip = v

		# vertically
		for j in range(4):
			v = True
			for i in range(4):
				if self.cards[i][j].side == BATIMENT:
					v = False
					break
			for k in range(4):
			 	self.cards[k][j].canFlip = v or self.cards[k][j].canFlip

	# can we flip a card?
	def canFlip(self):
		for i in range(4):
			for j in range(4):
				if self.cards[i][j].canFlip:
					return True
		return False

	def draw(self, gamePhase):
		(x,y) = self.findCard(pg.mouse.get_pos())
		self.screen.fill(backgroundColor, marketBackgroundRect)
		match gamePhase:
			case GPhase.DISCOVER:
				for i in range(4):
					for j in range(4):
						if self.cards[i][j].canFlip:
							self.screen.fill(green, self.highlightRects[i][j])
				if x != -1 and self.cards[x][y].canFlip:
					self.screen.fill(white, self.highlightRects[x][y])
			case GPhase.MARKET:
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

	def lazyDraw(self, gamePhase):
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
		(i,j) = card
		self.screen.fill(color, self.highlightRects[i][j])
		self.cards[i][j].draw(self.cardPos[i][j])