import pygame as pg
import sys
from params import *
from pointcity import *

avatarSize = (190, 190)
winnerBannerSize = (450, 120)
leftcol = screenSize[0]/4
rightcol = 3*screenSize[0]/4
winAvatarRect = pg.Rect((0,0), avatarSize)
winAvatarRect.center = (midx, space2 + avatarSize[0]/2)
winnerTitleRect = playerTitleImg[0].get_rect()
winnerTitleRect.centerx = midx
winnerTitleRect.top = winAvatarRect.bottom + space1
winnerBanner = pg.transform.smoothscale(pg.image.load("res/winner.png"), winnerBannerSize)
winnerBannerRect = winnerBanner.get_rect()
winnerBannerRect.centerx = midx
winnerBannerRect.top = winnerTitleRect.bottom + space1

tabPos = (screenSize[0]/6, winnerBannerRect.bottom + space3 - space1)
tabSize = (screenSize[0] - 2*tabPos[0], screenSize[1] - tabPos[1] - space3)
tabRect = pg.Rect(tabPos, tabSize)
avL = (tabSize[1] - 4*space1 - 2*space2 - fontsize1)/4
avatarSize2 = (avL, avL)

font = pg.font.Font('freesansbold.ttf', fontsize1)
titleText = ["Joueur", "Score", "Cartes en main"]
titles = [font.render(t, True, white, menuBackgroundColor) for t in titleText]
titleRect = [i.get_rect() for i in titles]
for i in range(3):
	titleRect[i].top = winnerBannerRect.bottom + space3
titleRect[0].centerx = leftcol
titleRect[1].centerx = midx
titleRect[2].centerx = rightcol

stars = [starImg.get_rect() for i in range(3)]
for i in range(3):
	stars[i].centery = 5*screenSize[1]/6
	stars[i].centerx = midx + (i-1)*(space1 + stars[0].w)

# playerList = liste de tuples (n° avatar, score, nb de cartes en main) pour chaque joueur.
class endScreen:
	def __init__(self, screen, playerList):
		self.screen = screen
		self.playerList = playerList
		self.modeSolo = playerList[1][0] == -1

		# tri par score + nb de cartes
		order = [i for i in range(len(playerList))]
		order.sort(reverse = True, key = lambda i: playerList[i][1]*100 + playerList[i][2])
		print("scores: ", [playerList[i] for i in order])

		if self.modeSolo:
			i = order.index(0)
			self.nStars = 3 - i
			order = [order[2], 0] if i == 3 else [0, order[i+1]]
			starOffset = i*(space1 + stars[0].w)/2
			for i in range(self.nStars):
				stars[i].move_ip(starOffset, 0)

		# images
		self.avatars = [pg.transform.smoothscale(avatarImg[playerList[i][0]], avatarSize2) for i in order]
		self.winAvatar = pg.transform.smoothscale(avatarImg[playerList[order[0]][0]], avatarSize)
		self.winnerTitle = playerTitleImg[min(order[0], 1) if self.modeSolo else order[0]]
		self.avatarRect = [a.get_rect() for a in self.avatars]
		self.scores = [font.render(str(playerList[i][1]), True, darkBlue, menuBackgroundColor) for i in order]
		self.scoreRect = [i.get_rect() for i in self.scores]
		self.nCartes = [font.render(str(playerList[i][2]), True, darkBlue, menuBackgroundColor) for i in order]
		self.nCartesRect = [i.get_rect() for i in self.scores]
		y = winnerBannerRect.bottom + space2 + space3 + fontsize1
		for i in range(len(order)):
			self.avatarRect[i].centerx = leftcol
			self.avatarRect[i].top = y + i*(avL + space1)
			self.scoreRect[i].centerx = midx
			self.scoreRect[i].centery = self.avatarRect[i].centery
			self.nCartesRect[i].centerx = rightcol
			self.nCartesRect[i].centery = self.avatarRect[i].centery

	def draw(self):
		self.screen.blit(backGround, (0,0))
		self.screen.fill(menuBackgroundColor, tabRect)
		self.screen.blit(self.winAvatar, winAvatarRect)
		self.screen.blit(self.winnerTitle, winnerTitleRect)
		self.screen.blit(winnerBanner, winnerBannerRect)
		if self.modeSolo:
			for i in range(self.nStars):
				self.screen.blit(starImg, stars[i])
		for i in range(3):
			self.screen.blit(titles[i], titleRect[i])
		for i in range(2 if self.modeSolo else len(self.playerList)):
			self.screen.blit(self.avatars[i], self.avatarRect[i])
			self.screen.blit(self.scores[i], self.scoreRect[i])
			self.screen.blit(self.nCartes[i], self.nCartesRect[i])