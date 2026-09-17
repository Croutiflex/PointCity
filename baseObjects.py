import pygame as pg
from params import *
from cards import *
import os

class PointCityCard(Card):
	def __init__(self, tier, ressource, type, cost, value, Id):
		self.Id = Id
		self.tier = tier
		self.ressource = ressource
		self.type = type # type de batiment
		self.cost = cost
		self.value = value
		self.canFlip = True

		back = resName[ressource]
		if tier > 0 and self.ressource != INGENIEUR:
			back += "_double"
		back += ".png"
		super().__init__("res/", "batiments/"+str(Id)+".png", back, cardSize[0])

	def __str__(self):
		return resName[self.ressource]

	def resize(self, size):
		self.size = size
		self.image = pg.transform.smoothscale(self.image, cardSize[size])
		self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)

class PointCityToken(SpriteWithTL):
	def __init__(self, type, info, Id):
		self.Id = Id
		self.type = type
		self.info = info
		self.size = 0
		self.refImg = pg.image.load("res/jetons/"+str(Id)+".png")
		super().__init__(pg.transform.smoothscale(self.refImg, tokenSize[0]))

	def resize(self, size):
		self.size = size
		self.image = pg.transform.smoothscale(self.refImg, tokenSize[size])
		self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)