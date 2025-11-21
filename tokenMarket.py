from params import *
import pygame as pg
import math

class PointCityTokenMarket:
	def __init__(self, screen, tokens, modeSolo=False):
		self.screen = screen
		self.modeSolo = modeSolo
		self.tokens = tokens
		self.tokenPos = []
		self.tokenCenter = []
		self.lastMousePos = -1
		(x,y) = tkMarketPos
		r = tokenD1/2
		for i in range(len(tokens)):
			self.tokenPos.append((x,y))
			self.tokenCenter.append((x+r,y+r))
			self.tokenPos.append((x + tokenD1 + space1,y))
			self.tokenCenter.append((x + tokenD1 + space1 + r,y+r))
			y += tokenD1 + space1

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

	def draw(self,screen, isTokenPhase=False):
		if self.modeSolo and len(self.tokens) > 0:
			pg.draw.circle(self.screen, orange, self.tokenCenter[0], TKR)
		if isTokenPhase:
			i = self.findToken(pg.mouse.get_pos())
			if i != -1:
				pg.draw.circle(self.screen, white, self.tokenCenter[i], TKR)
		for i in range(len(self.tokens)):
			self.tokens[i].draw(screen)