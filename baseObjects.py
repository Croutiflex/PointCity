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
		self.size = 0
		img1 = ImgRes[ressource] if tier == 0 else ImgRes2[ressource]
		img2 = batiments[imageBat]
		self.imageRes = [img1, pg.transform.scale(img1, cardSize2), pg.transform.scale(img1, cardSize3)] # image face ressource, par taille
		self.imageBat = [img2, pg.transform.scale(img2, cardSize2), pg.transform.scale(img2, cardSize3)] # image face batiment, par taille
		# variable
		self.side = RESSOURCE
		self.canFlip = True

	def __str__(self):
		return str(self.ressource)

	def getImage(self):
		return self.imageRes[self.size] if self.side == RESSOURCE else self.imageBat[self.size]

	# renvoie True si la carte a été retournée, false sinon
	def flip(self):
		if self.canFlip:
			self.side = BATIMENT
			return True
		return False

	def resize(self, size):
		self.size = size - 1

	def draw(self, pos):
		self.screen.blit(self.getImage(), pos)


class pointCityToken:
	def __init__(self, screen, type, info, imageNr):
		self.screen = screen
		self.type = type
		self.info = info
		self.size = 0
		img = jetons[imageNr]
		self.image = [img, pg.transform.scale(img, (tokenSize2, tokenSize2)), pg.transform.scale(img, (tokenSize3, tokenSize3))]

	def resize(self, size):
		self.size = size - 1

	def getImage(self):
		return self.image[self.size]

	def draw(self, pos):
		self.screen.blit(self.getImage(), pos)
