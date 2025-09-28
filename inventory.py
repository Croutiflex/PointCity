from params import *
import pygame as pg
from baseObjects import *
import math
import random

class pointCityPlayerInventory:
	def __init__(self, screen, Id, pos, avatar=-1, newGame=True):
		self.screen = screen
		self.pos = pos
		self.isAutoma = avatar == -1
		self.avatarNr = avatar
		self.avatar = pg.transform.smoothscale(avatarImg[avatar], avatarSize1)
		self.resCards = []
		self.batCards = [[] for i in range(5)]
		self.production = [0 for i in range(5)]
		self.muniBats = []
		self.pointsBats = []
		self.tokens = []
		self.Id = Id
		self.score = 0
		self.tokenPosL = []
		self.tokenPosl = [[] for i in range(3)]
		self.handPosL = []
		self.handPosl = [[] for i in range(3)]
		self.cityPosL = [[] for i in range(5)]
		self.muniPosL = []
		self.pointsPosL = []
		if newGame:
			self.addInge()

		self.selectedCards = []

		# text intitulé joueur
		self.font = pg.font.Font('freesansbold.ttf', fontsize1)

		# self.surface = screen.subsurface(PIRect[0])
		self.mouseWasOnHand = False
		self.hasRecentlyChanged = True

	def addInge(self):
		self.hasRecentlyChanged = True
		card = pointCityCard(self.screen, 0, INGENIEUR, 'ressource', None, 0, -1)
		card.resize(self.getSize())
		self.addCard(card)

	def computeScore(self):
		total = self.score
		for tk in self.tokens:
			match tk.type:
				case 0: # points bruts
					total += int(tk.info)
				case 1: # 2 par production ou ingé
					res = int(tk.info)
					if res == INGENIEUR:
						for c in self.resCards:
							if c.ressource == INGENIEUR:
								total += 2
					else:
						total += self.production[res]*2
				case 2: # 
					total += 3*min([self.production[int(res)] for res in tk.info.split('/')])
				case 3: # 2/3 par production double/triple
					for i in range(5):
						if self.production[i] >= int(tk.info):
							total += int(tk.info)
				case 4: # 4 par ressource non produite
					for i in range(5):
						if self.production[i] == 0:
							total += int(tk.info)
				case 5: # multi
					total += min(self.production)*int(tk.info)
		return total

	def computeAutomaScore(self, diff):
		total = self.score
		scale = automaScale[diff]
		if diff == 0:
			total += sum(self.production)
		else:
			for prod in self.production:
				if prod > 0:
					p = min(prod, 3)
					total += scale[p-1]
		total += scale[3]*len(self.tokens)
		if diff == 2:
			total += len(self.resCards)
		return total

	def endTurn(self, n):
		self.hasRecentlyChanged = True
		p = self.pos - 1
		self.pos = p if p >= 0 else n-1
		# print("Joueur ", self.Id, " passe en pos : ", self.pos)
		self.resize()
		self.resetSelection()

	def getSize(self):
		return 2 if self.pos == 0 else 3

	def resize(self):
		size = self.getSize()
		# print("player ", self.Id,", resize : ", size)
		for j in self.tokens:
			j.resize(size)
		for c in self.resCards:
			c.resize(size)

	def resetSelection(self):
		self.hasRecentlyChanged = True
		self.selectedCards = []
		self.updateHandPos()

	def selectHandCard(self, mousePos):
		if not self.mouseWasOnHand:
			return
		for i in range(1, len(self.resCards)+1):
			pos = self.handPosL[-i]
			rect = pg.Rect(pos, cardSize2)
			if rect.collidepoint(mousePos):
				self.hasRecentlyChanged = True
				if pos[1] < handPosL[1]: # si la carte est déjà sélectionnée
					self.handPosL[-i] = (pos[0], handPosL[1])
					if self.resCards[-i] not in self.selectedCards:
						print("ERROR")
					else:
						self.selectedCards.remove(self.resCards[-i])
				else:
					self.handPosL[-i] = (pos[0], pos[1] - space2)
					self.selectedCards.append(self.resCards[-i])
				return

	def addToken(self, token):
		self.hasRecentlyChanged = True
		self.tokens.append(token)

	def updateTokenPos(self, gameLoad = False):
		self.hasRecentlyChanged = True
		# détaillé
		L = len(self.tokens)
		if not gameLoad:
			L += 1
		self.tokenPosL = []
		(x,y) = tokenPosL
		space = min((PIH + space3 - y - space2)/math.ceil(L/2), tokenSize2+space1)
		for i in range(L//2):
			self.tokenPosL.append((x,y))
			self.tokenPosL.append((x + tokenSize2, y))
			y += space
		if L%2 == 1:
			self.tokenPosL.append((x,y))
		# réduit
		self.tokenPosl = []
		for i in range(3):
			tkpl = []
			(x,y) = tokenPosl[i]
			space = min((PIxHalf - x - space1 - tokenSize3)/L, tokenSize3+space1)
			for i in range(L):
				tkpl.append((x,y))
				x += space
			self.tokenPosl.append(tkpl)

		return self.tokenPosL[-1]

	def updateHandPos(self):
		self.handPosL = []
		self.handPosl = []
		if len(self.resCards) == 0:
			return
		# détail
		(x,y) = handPosL
		space = (handRect.w - cardSize2[0])/len(self.resCards)
		for c in self.resCards:
			self.handPosL.append((x,y))
			x += space
		# réduit
		for i in range(3):
			hpl = []
			(x,y) = handPosl[i]
			space = min(((screenSize[0] - x - space1 - space2 - cardSize3[0])/len(self.resCards)), cardSize3[0]*0.8)
			for i in range(len(self.resCards)):
				hpl.append((x,y))
				x += space
			self.handPosl.append(hpl)

	def addCard(self, card):
		# print("carte ", card.Id, " pour joueur ", self.Id)
		self.hasRecentlyChanged = True
		if card.side == RESSOURCE:
			self.addResCard(card)
		else:
			self.addBatCard(card)

	def addResCard(self, card):
		if self.isAutoma and card.ressource != INGENIEUR:
			return
		self.resCards.append(card)
		self.updateHandPos()

	def addBatCard(self, card):
		self.score += card.value
		match card.type:
			case "ressource":
				self.batCards[card.ressource].append(card)
				self.production[card.ressource] += 1
				if self.production[card.ressource] == 1:
					self.cityPosL[card.ressource].append(cityPosL[card.ressource])
				elif self.production[card.ressource] > 4:
					self.cityPosL[card.ressource] = []
					(x,y) = cityPosL[card.ressource]
					space = (PIH - space2 - 2*space1 - 2*cardSize2[1])/len(self.batCards[card.ressource])
					for c in self.batCards[card.ressource]:
						self.cityPosL[card.ressource].append((x,y))
						y += space
				else:
					(x,y) = self.cityPosL[card.ressource][-1]
					self.cityPosL[card.ressource].append((x, y + space3))
			case "municipal":
				self.muniBats.append(card)
				self.muniPosL = []
				(x,y) = muniPosL
				space = 0.4*(pointsPosL[0] - cardSize2[0] - muniPosL[0] - space1)/len(self.muniBats)
				for c in self.muniBats:
					self.muniPosL.append((x,y))
					x += space
			case "points":
				self.pointsBats.append(card)
				self.pointsPosL = []
				(x,y) = pointsPosL
				space = 0.6*(pointsPosL[0] - cardSize2[0] - muniPosL[0] - space1)/len(self.pointsBats)
				for c in self.pointsBats:
					self.pointsPosL.append((x,y))
					x -= space

	def drawBatCards(self, ressource):
		for i in range(len(self.batCards[ressource])):
			self.batCards[ressource][i].draw(self.cityPosL[ressource][i])

	def draw(self, isMarketPhase=False):
		if isMarketPhase:
			isOnHand = handRect.collidepoint(pg.mouse.get_pos())
			if isOnHand != self.mouseWasOnHand:
				self.mouseWasOnHand = isOnHand
		self.screen.fill(playerColors[self.Id], PIRect[self.pos])
		if self.pos == 0: # inventaire détaillé
			# nom du joueur
			self.screen.blit(playerTitleImg[self.Id], titlePos[self.pos])
			# avatar
			self.screen.blit(self.avatar, avatarPos)
			# jetons
			for tk in range(len(self.tokens)):
				self.tokens[tk].draw(self.tokenPosL[tk])
			# main
			if isMarketPhase and self.mouseWasOnHand:
				self.screen.fill(white, handRect)
			for i in range(len(self.resCards)):
				self.resCards[i].draw(self.handPosL[i])
			# bat. ressources
			for res in range(5):
				self.drawBatCards(res)
			# bat. municipaux
			for i in range(len(self.muniBats)):
				self.muniBats[i].draw(self.muniPosL[i])
			# bat. à points
			for i in range(len(self.pointsBats)):
				self.pointsBats[i].draw(self.pointsPosL[i])

		else: # inventaire réduit
			# nom du joueur
			self.screen.blit(playerTitleImgSmall[self.Id], titlePos[self.pos])
			# jetons
			for tk in range(len(self.tokens)):
				self.tokens[tk].draw(self.tokenPosl[self.pos - 1][tk])
			# main
			for i in range(len(self.resCards)):
				self.resCards[i].draw(self.handPosl[self.pos - 1][i])
			# production
			for i in range(5):
				self.screen.blit(iconRes[i], (iconResX[i], titlePos[self.pos][1]))
				pText = self.font.render(str(self.production[i]), True, textColor, playerColors[self.Id])
				self.screen.blit(pText, pText.get_rect().move((prodTextX[i], titlePos[self.pos][1])))

			# points des batiments
			pg.draw.circle(self.screen, white, pointBubbleCenter[self.pos-1], pointBubbleR1)
			pg.draw.circle(self.screen, darkBlue, pointBubbleCenter[self.pos-1], pointBubbleR2)
			pText = self.font.render(str(self.score), True, white, darkBlue)
			rect = pText.get_rect()
			rect.center = pointBubbleCenter[self.pos-1]
			self.screen.blit(pText, rect)

	def lazyDraw(self, isMarketPhase=False): # deprecated
		if isMarketPhase:
			isOnHand = handRect.collidepoint(pg.mouse.get_pos())
			if isOnHand != self.mouseWasOnHand:
				self.mouseWasOnHand = isOnHand
				self.hasRecentlyChanged = True
		if self.hasRecentlyChanged:
			# print("draw inv: ", self.Id+1, " at pos ", self.pos)
			self.resize()
			self.draw(isMarketPhase)
			self.hasRecentlyChanged = False