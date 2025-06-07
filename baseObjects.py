import pygame as pg
from params import *

class pointCityCard:
	def __init__(self, tier, ressource, type, cost, value, imageBat):
		# constant
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

	def draw(self, screen, pos):
		screen.blit(self.getImage(), pos)


class pointCityToken:
	def __init__(self, type, info, image):
		self.type = type
		self.info = info
		self.image = jetons[image]

	def draw(self, screen, pos):
		screen.blit(self.image, pos)
