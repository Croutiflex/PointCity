from params import *
import pygame as pg
import math

class pointCityTokenMarket:
	def __init__(self, screen, tokens):
		self.screen = screen
		self.tokens = tokens
		self.tokenPos = []
		self.tokenCenter = []
		self.lastMousePos = -1
		(x,y) = tkMarketPos
		r = tokenSize/2
		for i in range(len(tokens)):
			self.tokenPos.append((x,y))
			self.tokenCenter.append((x+r,y+r))
			self.tokenPos.append((x + tokenSize + space1,y))
			self.tokenCenter.append((x + tokenSize + space1 + r,y+r))
			y += tokenSize + space1

	def findToken(self, mousePos):
		for i in range(len(self.tokens)):
			if math.dist(mousePos, self.tokenCenter[i]) < TKR:
				return i
		return -1

	def getToken(self, mousePos):
		i = self.findToken(mousePos)
		if i == -1:
			return None
		ret = self.tokens.pop(i)
		self.draw(False)
		return ret

	def draw(self, isTokenPhase):
		if isTokenPhase:
			i = self.findToken(pg.mouse.get_pos())
			if i != -1:
				pg.draw.circle(self.screen, white, self.tokenCenter[i], TKR)
		for i in range(len(self.tokens)):
			self.tokens[i].draw(self.tokenPos[i])

	def lazyDraw(self, isTokenPhase):
		if not isTokenPhase:
			return
		x = self.findToken(pg.mouse.get_pos())
		y = self.lastMousePos
		if x == y:
			return
		if x != -1:
			pg.draw.circle(self.screen, white, self.tokenCenter[x], TKR)
			self.tokens[x].draw(self.tokenPos[x])
		if y != -1 and y < len(self.tokens):
			pg.draw.circle(self.screen, backgroundColor, self.tokenCenter[y], TKR)
			self.tokens[y].draw(self.tokenPos[y])
		self.lastMousePos = x
