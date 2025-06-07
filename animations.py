from params import *
import pygame as pg

# modes d'animation
class AnimMode(IntEnum):
	SEQUENTIEL = 0
	SIMULTANE = 1

# modélise le déplacement en ligne droite d'une image d'un point A à un point B
# onDone = fonction à exécuter quand l'animation est finie
# mode = 0 pour simultané, 1 pour séquencé
class translation:
	def __init__(self, screen, image, A, B, onDone):
		self.screen = screen
		self.image = image
		self.A = A
		self.B = B
		self.speedVector = ((B[0]-A[0])/translationTime, (B[1]-A[1])/translationTime)
		self.currentPos = self.A
		self.framesLeft = translationTime # = durée de l'animation en nbr de frames
		self.done = False
		self.onDone = onDone

	def draw(self):
		if not self.done:
			self.screen.blit(self.image, self.currentPos)
			self.currentPos = (self.currentPos[0] + self.speedVector[0], self.currentPos[1] + self.speedVector[1])
			self.framesLeft -= 1
			if self.framesLeft == 0:
				self.done = True
				if self.onDone != None:
					# print(id(self)," done!")
					self.onDone()