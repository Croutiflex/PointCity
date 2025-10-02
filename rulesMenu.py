import pygame as pg
from params import *
from utils import *

class RulesMenu:
	def __init__(self):
		self.closeButton = CloseButton()
		self.leftButton = Button("res/rules/left.png", "res/rules/left2.png", (screenSize[0]/20, screenSize[1]/10))
		self.leftButton.rect.centery = midy
		self.leftButton.rect.left = 30
		self.rightButton = Button("res/rules/right.png", "res/rules/right2.png", (screenSize[0]/20, screenSize[1]/10))
		self.rightButton.rect.centery = midy
		self.rightButton.rect.right = screenSize[0] - 30
		self.rulesBook = RulesBook()
		self.buttons = pg.sprite.Group([self.rightButton, self.closeButton])
		self.drawables = pg.sprite.RenderPlain([self.rightButton, self.closeButton] + [self.rulesBook])
		self.selectedButton = None

	# renvoie True si croix cliquée
	def leftClick(self):
		b = self.selectedButton
		lastPage = self.rulesBook.page
		if b == self.closeButton:
			return True
		elif b == self.leftButton:
			newPage = self.rulesBook.turn(-1)
			if newPage == 0:
				self.drawables.remove(b)
				self.buttons.remove(b)
			elif newPage == len(self.rulesBook.img) - 2:
				self.drawables.add(self.rightButton)
				self.buttons.add(self.rightButton)
		elif b == self.rightButton:
			newPage = self.rulesBook.turn(1)
			if newPage == 1:
				self.drawables.add(self.leftButton)
				self.buttons.add(self.leftButton)
			elif newPage == len(self.rulesBook.img) - 1:
				self.drawables.remove(b)
				self.buttons.remove(b)
		return False

	def update(self):
		self.drawables.update()
		self.selectedButton = None
		collide = pg.sprite.spritecollide(Point(pg.mouse.get_pos()), self.buttons, 0)
		self.selectedButton = collide[0] if len(collide) > 0 else None

	def draw(self, screen):
		screen.fill(menuBackgroundColor)
		self.drawables.draw(screen)

class RulesBook(pg.sprite.Sprite):
	def __init__(self):
		pg.sprite.Sprite.__init__(self)
		reglesImg = [pg.image.load("res/rules/"+str(i)+".png") for i in range(1,10)]
		self.rect = reglesImg[0].get_rect()
		self.rect.scale_by_ip(screenSize[1]/self.rect.h)
		self.rect.centerx = midx
		self.rect.top = 0
		self.img = [pg.transform.smoothscale(r, self.rect.size) for r in reglesImg]
		self.page = 0
		self.image = self.img[0]
	# tourner les pages
	def turn(self, direction=1):
		self.page = min(len(self.img) - 1 , self.page + direction)
		self.image = self.img[self.page]
		return self.page