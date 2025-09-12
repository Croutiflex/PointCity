import pygame as pg
import sys
from params import *
from pointcity import *

avatarSize = (200, 200)
avatarSize2 = (50, 50)
winAvatarRect = pg.Rect((0,0), avatarSize)
winAvatarRect.center = (midx, space2 + avatarSize[0]/2)
winnerTitleRect = playerTitleImg[0].get_rect()
winnerTitleRect.centerx = midx
winnerTitleRect.top = winAvatarRect.bottom + space1
winnerBanner = pg.image.load("res/winner.png")
winnerBannerRect = winnerBanner.get_rect()
winnerBannerRect.centerx = midx
winnerBannerRect.top = winnerTitleRect.bottom + space1

class endScreen:
	def __init__(self, screen, playerList):
		self.screen = screen
		self.playerList = playerList

		# tri par score
		order = [i for i in range(len(playerList))]
		order.sort(reverse = True, key = lambda i: playerList[i][1])
		bestScore = playerList[order[0]][1]
		n = 0
		for i in order:
			if playerList[order[i]][1] == bestScore:
				n += 1
		if n > 1: # si plusieurs joueurs ont le même score
			L = order[:n]
			L.sort(reverse = True, key = lambda i: playerList[i][2]) # tri par nbre de cartes en main
			order = L + order[n:]
		self.order = order
		print("scores: ", [playerList[i] for i in order])

		# images
		self.avatars = [pg.transform.smoothscale(avatarImg[playerList[i][0]], avatarSize2) for i in order]
		self.winAvatar = pg.transform.smoothscale(avatarImg[playerList[0][0]], avatarSize)
		self.winnerTitle = playerTitleImg[order[0]]
		# self.avatarRect = [a.get_rect() for a in self.avatars]

	def draw(self):
		self.screen.fill(backgroundColor)
		self.screen.blit(self.winAvatar, winAvatarRect)
		self.screen.blit(self.winnerTitle, winnerTitleRect)
		self.screen.blit(winnerBanner, winnerBannerRect)