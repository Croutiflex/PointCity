from params import *
import pygame as pg
import time

# modélise le déplacement en ligne droite d'une image d'un point A à un point B
# onDone = fonction à exécuter quand l'animation est finie
# duration = durée de l'animation en s
class translation:
	def __init__(self, screen, image, A, B, onDone, duration=translationTime):
		# print('Nouvelle anim')
		self.screen = screen
		self.image = image
		self.A = A
		self.B = B
		self.speedVector = ((B[0]-A[0])/duration, (B[1]-A[1])/duration)
		self.currentPos = self.A
		self.duration = duration
		self.lastFrameTime = None
		self.elapsedTime = 0
		self.done = False
		self.onDone = onDone

	def draw(self):
		if not self.done:
			# print('elapsedTime: ', self.elapsedTime)
			self.screen.blit(self.image, self.currentPos)
			if self.lastFrameTime == None: # premier draw
				self.lastFrameTime = time.time()
			else:
				now = time.time()
				dt = now - self.lastFrameTime
				self.lastFrameTime = now
				self.elapsedTime += dt
				(dx, dy) = (self.speedVector[0]*dt, self.speedVector[1]*dt)
				self.currentPos = (self.currentPos[0] + dx, self.currentPos[1] + dy)
				if self.elapsedTime >= self.duration:
					self.done = True
					if self.onDone != None:
						self.onDone()