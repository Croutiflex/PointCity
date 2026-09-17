from params import *
import pygame as pg
import math

r = tokenD1/2

class PointCityTokenMarket:
	def __init__(self, tokens, modeSolo=False):
		self.modeSolo = modeSolo
		self.tokens = tokens
		self.drawables = pg.sprite.RenderPlain(self.tokens)
		self.lastMousePos = -1
		(x,y) = tkMarketPos
		d = tokenD1 + space1
		for i in range(len(tokens)//2):
			self.tokens[2*i].move((x,y+i*d))
			self.tokens[2*i+1].move((x+d,y+i*d))
		self.tokenPhase = False

	def findToken(self):
		for i in range(len(self.tokens)):
			if math.dist(pg.mouse.get_pos(), self.tokens[i].rect.center) < r:
				return i
		return -1

	def getToken(self):
		i = self.findToken()
		if i == -1:
			return None
		ret = self.tokens.pop(i)
		self.drawables.remove(ret)
		return ret

	def draw(self, screen):
		if self.modeSolo and len(self.tokens) > 0:
			pg.draw.circle(screen, orange, self.tokens[0].rect.center, r+space1) # prochain jeton de l'automa
		if self.tokenPhase:
			i = self.findToken()
			if i != -1:
				pg.draw.circle(screen, white, self.tokens[i].rect.center, r+space1)
		self.drawables.draw(screen)