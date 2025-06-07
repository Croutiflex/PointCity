import pygame as pg
from params import *

class pointCityCard:
	def __init__(self, screen, tier, ressource, type, cost, value, imageBat):
		# constant
		self.screen = screen
		self.tier = tier
		self.ressource = ressource
		self.type = type # type de batiment
		self.cost = cost
		self.value = value
		self.imageRes = ImgRes[ressource] if tier == 0 else ImgRes2[ressource]
		self.imageBat = batiments[imageBat]
		# variable
		self.side = RESSOURCE
		self.canFlip = True

	def __str__(self):
		return str(self.ressource)

	def getImage(self):
		return self.imageRes if self.side == RESSOURCE else self.imageBat

	# renvoie True si la carte a été retournée, false sinon
	def flip(self):
		if self.canFlip:
			self.side = BATIMENT
			return True
		return False

	def resize(self, size):
		self.imageBat = pg.transform.scale(self.imageBat, size)
		self.imageRes = pg.transform.scale(self.imageRes, size)

	def draw(self, pos):
		self.screen.blit(self.getImage(), pos)


class pointCityToken:
	def __init__(self, screen, type, info, image):
		self.screen = screen
		self.type = type
		self.info = info
		self.image = jetons[image]

	def resize(self, size):
		self.image = pg.transform.scale(self.image, size)

	def draw(self, pos):
		self.screen.blit(self.image, pos)
