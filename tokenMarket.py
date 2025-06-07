from params import *
import pygame as pg
import math

class pointCityTokenMarket:
	def __init__(self, tokens):
		self.tokens = tokens
		self.tokenPos = []
		self.tokenCenter = []
		(x,y) = tkMarketPos
		r = tokenSize/2
		for j in range(len(tokens)):
			self.tokenPos.append((x,y))
			self.tokenCenter.append((x+r,y+r))
			if j == 4 or j == 9:
				x += 2*r + space1
				y = tkMarketPos[1]
			else:
				y += 2*r + space1

	def findToken(self, mousePos):
		for i in range(len(self.tokens)):
			if math.dist(mousePos, self.tokenCenter[i]) < TKR:
				return i
		return -1

	def getToken(self, mousePos):
		i = self.findToken(mousePos)
		if i == -1:
			return None
		return self.tokens.pop(i)

	def draw(self, screen, isTokenPhase):
		if isTokenPhase:
			i = self.findToken(pg.mouse.get_pos())
			if i != -1:
				pg.draw.circle(screen, white, self.tokenCenter[i], TKR)
		for i in range(len(self.tokens)):
			self.tokens[i].draw(screen, self.tokenPos[i])
