import pygame as pg
import time
from params import *

class popUp:
	def __init__(self, screen, image, pos, duration=2):
		self.screen = screen
		self.image = image
		self.pos = pos
		self.duration = duration
		self.startTime = time.time()
		self.done = False

	def draw(self):
		if self.done:
			return
		self.screen.blit(self.image, self.pos)
		if time.time() - self.startTime >= self.duration:
			self.done = True