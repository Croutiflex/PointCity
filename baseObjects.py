import pygame as pg
from params import *
from utils import *
import os

class PointCityCard(SpriteWithTL):
	def __init__(self, tier, ressource, type, cost, value, Id, pos=(0,0)):
		pg.sprite.Sprite.__init__(self)
		# constant
		self.Id = Id
		self.tier = tier
		self.ressource = ressource
		self.type = type # type de batiment
		self.cost = cost
		self.value = value
		self.size = 0

		# variable
		self.imageRes = ImgRes[ressource] if tier == 0 else ImgRes2[ressource]
		file = "res/batiments/"+str(Id)+".png"
		if os.path.exists(file):
			self.imageBat = pg.image.load(file)
		else:
			self.imageBat = pg.image.load("res/batiments/dummy.png")
		self.side = RESSOURCE
		self.canFlip = True
		self.image = pg.transform.smoothscale(self.imageRes, cardSize[0])
		self.rect = self.image.get_rect(x=pos[0], y=pos[1])

	def __str__(self):
		return str(self.ressource)

	def getBaseImg(self):
		return self.imageRes if self.side == RESSOURCE else self.imageBat

	# renvoie True si la carte a été retournée, false sinon
	def flip(self):
		if self.canFlip:
			self.side = BATIMENT
			self.image = pg.transform.smoothscale(self.imageBat, cardSize[0])
			return True
		return False

	def resize(self, size):
		self.size = size
		self.image = pg.transform.smoothscale(self.getBaseImg(), cardSize[size])
		self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)

class PointCityToken(SpriteWithTL):
	def __init__(self, type, info, Id, pos = (0,0)):
		pg.sprite.Sprite.__init__(self)
		self.Id = Id
		self.type = type
		self.info = info
		self.size = 0
		self.image = pg.transform.smoothscale(pg.image.load("res/jetons/"+str(Id)+".png"), tokenSize[0])
		self.rect = self.image.get_rect(x = pos[0], y = pos[1])

	def resize(self, size):
		self.size = size
		self.image = pg.transform.smoothscale(self.image, tokenSize[size])
		self.rect = self.image.get_rect(x = self.rect.x, y = self.rect.y)

	def move(x,y):
		self.rect.x = x
		self.rect.y = y