import pygame as pg
import sys
from params import *
from pointcity import *
from utils import *

avatarSize = (190, 190)
winnerBannerSize = (450, 120)
leftcol = screenSize[0]/4
rightcol = 3*screenSize[0]/4
winAvatarRect = pg.Rect((0,0), avatarSize)
winnerTitleRect = playerTitleImg[0].get_rect()
winnerTitleRect.centerx = midx
winnerTitleRect.top = winAvatarRect.bottom + space1
winnerBanner = pg.transform.smoothscale(pg.image.load("res/winner.png"), winnerBannerSize)
winnerBannerRect = winnerBanner.get_rect()
winnerBannerRect.centerx = midx
winnerBannerRect.top = winnerTitleRect.bottom + space1

tabPos = (screenSize[0]/6, winnerBannerRect.bottom + space3 - space1)
tabSize = (screenSize[0] - 2*tabPos[0], screenSize[1] - tabPos[1] - space3)
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
		self.drawables = pg.sprite.LayeredUpdates()
		self.drawables.add(HighLightRect(menuBackgroundColor, tabSize[0], tabSize[1], 0, tabPos))

		# tri par score + nb de cartes
		order = [i for i in range(len(playerList))]
		order.sort(reverse = True, key = lambda i: playerList[i][1]*100 + playerList[i][2])
		# print("scores: ", [playerList[i] for i in order])

		if self.modeSolo:
			i = order.index(0)
			nStars = 3 - i
			order = [order[2], 0] if i == 3 else [0, order[i+1]]
			stars = [BasicSprite(starImg) for i in range(3)]
			self.drawables.add(stars)
			for i in range(3):
				stars[i].move((5*screenSize[1]/6, midx + (i-1)*(space1 + stars[0].rect.w)))
			starOffset = i*(space1 + stars[0].rect.w)/2
			for i in range(nStars):
				stars[i].rect.move_ip(starOffset, 0)

		# images
		self.avatars = [BasicSprite(pg.transform.smoothscale(avatarImg[playerList[i][0]], avatarSize2)) for i in order]
		self.drawables.add(self.avatars)
		winAvatar = BasicSprite(pg.transform.smoothscale(avatarImg[playerList[order[0]][0]], avatarSize))
		winAvatar.move((midx, space2 + avatarSize[0]/2))
		self.drawables.add(winAvatar)
		winnerTitle = BasicSprite(playerTitleImg[min(order[0], 1) if self.modeSolo else order[0]])
		winnerTitle.rect.centerx = midx
		winnerTitle.rect.top = winAvatar.rect.bottom + space1
		self.drawables.add(winnerTitle)
		winnerBanner = BasicSprite(pg.transform.smoothscale(pg.image.load("res/winner.png"), winnerBannerSize))
		winnerBanner.rect.centerx = midx
		winnerBanner.rect.top = winnerTitle.rect.bottom + space1
		self.drawables.add(winnerBanner)
		scores = [BasicSprite(font.render(str(playerList[i][1]), True, darkBlue, menuBackgroundColor)) for i in order]
		self.drawables.add(scores)
		nCartes = [BasicSprite(font.render(str(playerList[i][2]), True, darkBlue, menuBackgroundColor)) for i in order]
		self.drawables.add(nCartes)
		y = winnerBanner.rect.bottom + space2 + space3 + fontsize1
		for i in range(len(order)):
			self.avatars[i].rect.centerx = leftcol
			self.avatars[i].rect.top = y + i*(avL + space1)
			scores[i].move((midx, self.avatars[i].rect.centery))
			nCartes[i].move((rightcol, self.avatars[i].rect.centery))

	def draw(self, screen):
		screen.blit(backGround, (0,0))
		self.drawables.draw(screen)