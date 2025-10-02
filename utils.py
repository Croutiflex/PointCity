import pygame as pg
from params import *

class HighLightRect(pg.sprite.Sprite):
	def __init__(self,color,width,height,x,y):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect(x=x,y=y)
		self.layer = 1
	def set_color(self,color):
		self.image.fill(color)
	def move(self,pos):
		self.rect.center = pos

class Button(pg.sprite.Sprite):
	def __init__(self, path1, path2, size, pos=(0,0)):
		pg.sprite.Sprite.__init__(self)
		self.imgOn = pg.transform.smoothscale(pg.image.load(path2), size)
		self.imgOff = pg.transform.smoothscale(pg.image.load(path1), size)
		self.image = self.imgOff
		self.rect = self.image.get_rect(x=pos[0], y=pos[1])
		self.isSelected = False
	def update(self):
		if self.rect.collidepoint(pg.mouse.get_pos()):
			self.image = self.imgOn
			self.isSelected = True
		else:
			self.image = self.imgOff
			self.isSelected = False

class CloseButton(Button):
	def __init__(self):
		h2 = screenSize[1]/20
		size = (h2, h2)
		Button.__init__(self, "res/X.png", "res/X2.png", size, (screenSize[0] - h2*2, h2))

class Point(pg.sprite.Sprite):
	def __init__(self, pos):
		(x, y) = pos
		pg.sprite.Sprite.__init__(self)
		self.rect = pg.Rect(x, y, x + 1, y + 1)