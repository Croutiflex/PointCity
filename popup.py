import pygame as pg
import time
from params import *

class popUp:
	def __init__(self, screen, image, pos, timed=False, duration=2):
		self.screen = screen
		self.image = image
		self.pos = pos
		if timed:
			self.duration = duration
			self.startTime = time.time()
			self.done = False
		else:
			self.on = False

	def drawSingle(self):
		self.screen.blit(self.image, self.pos)

	def draw(self):
		if self.done:
			return
		self.drawSingle()
		if time.time() - self.startTime >= self.duration:
			self.done = True