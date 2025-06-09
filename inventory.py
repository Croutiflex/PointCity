from params import *
import pygame as pg
from baseObjects import *
import math

class pointCityPlayerInventory:
	def __init__(self, screen, Id, pos):
		self.screen = screen
		self.pos = pos
		card = pointCityCard(screen, 0, INGENIEUR, 'ressource', 0, 0, 0)
		card.resize(2 if pos == 0 else 3)
		self.resCards = [card]
		self.batCards = [[] for i in range(5)]
		self.production = [0 for i in range(5)]
		self.muniBats = []
		self.pointsBats = []
		self.tokens = []
		self.id = Id
		self.score = 0
		self.tokenPosL = []
		self.tokenPosl = [[] for i in range(3)]
		self.handPosL = [handPosL]
		self.handPosl = [[handPosl[i]] for i in range(3)]
		self.cityPosL = [[] for i in range(5)]
		self.muniPosL = []
		self.pointsPosL = []

		# text intitulé joueur
		self.font = pg.font.Font('freesansbold.ttf', fontsize1)

		# self.surface = screen.subsurface(PIRect[0])
		self.hasRecentlyChanged = False

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

	def endTurn(self, n):
		self.hasRecentlyChanged = True
		p = self.pos - 1
		self.pos = p if p >= 0 else n-1
		if self.pos == 0:
			self.resize(2)
		elif self.pos == n-1:
			self.resize(3)

	def resize(self, size):
		for j in self.tokens:
			j.resize(size)
		for c in self.resCards:
			c.resize(size)

	def addToken(self, token):
		self.hasRecentlyChanged = True
		self.tokens.append(token)

	def updateTokenPos(self):
		self.hasRecentlyChanged = True
		# détaillé
		L = 1 + len(self.tokens)
		self.tokenPosL = []
		(x,y) = tokenPosL
		space = (PIH + space3 - y - space2)/math.ceil(L/2)
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
			space = (PIxHalf - x - space1 - tokenSize3)/L
			for i in range(L):
				tkpl.append((x,y))
				x += space
			self.tokenPosl.append(tkpl)

		return self.tokenPosL[-1]

	def addCard(self, card):
		card.resize(2 if self.pos == 0 else 3)
		if card.side == RESSOURCE:
			self.addResCard(card)
		else:
			self.addBatCard(card)

	def addResCard(self, card):
		self.hasRecentlyChanged = True
		self.resCards.append(card)
		# détail
		self.handPosL = []
		(x,y) = handPosL
		space = (muniPosL[0] - handPosL[0] - cardSize2[0] - space1)/len(self.resCards)
		for c in self.resCards:
			self.handPosL.append((x,y))
			x += space
		# réduit
		self.handPosl = []
		for i in range(3):
			hpl = []
			(x,y) = handPosl[i]
			space = min(((screenSize[0] - x - space1 - space2 - cardSize3[0])/len(self.resCards)), cardSize3[0]*0.8)
			for i in range(len(self.resCards)):
				hpl.append((x,y))
				x += space
			self.handPosl.append(hpl)

	def addBatCard(self, card):
		self.hasRecentlyChanged = True
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

	def draw(self):
		self.screen.fill(playerColors[self.id], PIRect[self.pos])
		# nom du joueur
		pText = self.font.render("Joueur " + str(self.id + 1), True, textColor, playerColors[self.id])
		self.screen.blit(pText, pText.get_rect().move(titlePos[self.pos]))
		if self.pos == 0: # inventaire détaillé
			# jetons
			for tk in range(len(self.tokens)):
				self.tokens[tk].draw(self.tokenPosL[tk])
			# main
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

			# self.surface = self.screen.subsurface(PIRect[0])
		else: # inventaire réduit
			# jetons
			for tk in range(len(self.tokens)):
				self.tokens[tk].draw(self.tokenPosl[self.pos - 1][tk])
			# main
			for i in range(len(self.resCards)):
				self.resCards[i].draw(self.handPosl[self.pos - 1][i])
			# production
			for i in range(5):
				self.screen.blit(iconRes[i], (iconResX[i], titlePos[self.pos][1]))
				pText = self.font.render(str(self.production[i]), True, textColor, playerColors[self.id])
				self.screen.blit(pText, pText.get_rect().move((prodTextX[i], titlePos[self.pos][1])))

			# points des batiments
			pg.draw.circle(self.screen, white, pointBubbleCenter[self.pos-1], pointBubbleR1)
			pg.draw.circle(self.screen, darkBlue, pointBubbleCenter[self.pos-1], pointBubbleR2)
			pText = self.font.render(str(self.score), True, white, darkBlue)
			rect = pText.get_rect()
			rect.center = pointBubbleCenter[self.pos-1]
			self.screen.blit(pText, rect)

	# test non concluant
	# def passiveDraw(self):
	# 	self.screen.blit(self.surface, PIRect[0])

	def lazyDraw(self):
		if self.hasRecentlyChanged:
			self.draw()
			self.hasRecentlyChanged = False