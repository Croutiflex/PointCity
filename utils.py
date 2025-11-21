import pygame as pg
from params import *

class BasicSprite(pg.sprite.Sprite):
	def __init__(self,image,layer=1,pos=(0,0)):
		pg.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = self.image.get_rect(x=pos[0], y=pos[1])
	def moveC(self,pos):
		self.rect.center = pos
	def move(self,pos):
		self.rect.topleft = pos
	def draw(self,screen):
		screen.blit(self.image, self.rect)

class SpriteWithTL(BasicSprite):
	# tell the sprite to start moving to dest = (x,y)
	# when dest is reached, execute onDone.
	def animate(self, dest, onDone, duration=translationTime):
		start = self.rect.topleft
		self.speedVector = ((dest[0]-start[0])/duration, (dest[1]-start[1])/duration)
		self.duration = duration
		self.lastFrameTime = None
		self.elapsedTime = 0
		self.done = False
		self.onDone = onDone
	def resetAnimation(self):
		self.lastFrameTime = None
		self.speedVector = (0,0)
		self.elapsedTime = 0
		self.done = True
		self.onDone = None
	def update(self):
		if not self.done:
			# print('elapsedTime: ', self.elapsedTime)
			if self.lastFrameTime == None: # premier draw
				self.lastFrameTime = time.time()
			else:
				now = time.time()
				dt = now - self.lastFrameTime
				self.lastFrameTime = now
				self.elapsedTime += dt
				(dx, dy) = (self.speedVector[0]*dt, self.speedVector[1]*dt)
				self.rect.topleft = (self.rect.left + dx, self.rect.top + dy)
				if self.elapsedTime >= self.duration:
					if self.onDone != None:
						self.onDone()
					self.resetAnimation()

class HighLightRect(pg.sprite.Sprite):
	def __init__(self,color,width,height,layer=1,pos=(0,0)):
		pg.sprite.Sprite.__init__(self)
		self.image = pg.Surface([width, height])
		self.image.fill(color)
		self.rect = self.image.get_rect(centerx=pos[0], centery=pos[1])
		self.layer = 1
	def set_color(self,color):
		self.image.fill(color)
	def move(self,pos):
		self.rect.center = pos

# bouton avec 2 images (survolé ou pas)
class Button(pg.sprite.Sprite):
	def __init__(self, path1, path2, size, pos=(0,0)):
		pg.sprite.Sprite.__init__(self)
		self.layer = 2
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
		self.rect = pg.Rect(x, y, 1, 1)