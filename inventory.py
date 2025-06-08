from params import *
import pygame as pg
from baseObjects import *

class pointCityPlayerInventory:
	def __init__(self, screen, Id):
		self.screen = screen
		card = pointCityCard(screen, 0, INGENIEUR, 'ressource', 0, 0, 0)
		card.imageRes = pg.transform.scale(card.imageRes, cardSize2)
		self.resCards = [card]
		self.batCards = [[] for i in range(5)]
		self.production = [0 for i in range(5)]
		self.muniBats = []
		self.pointsBats = []
		self.tokens = []
		self.id = Id
		self.pos = Id
		self.score = 0
		self.tokenPosL = []
		self.nextTokenPos = (tokenPosLX[0], tokenPosLY)
		self.handPosL = [handPosL]
		self.cityPosL = [[] for i in range(5)]
		self.muniPosL = []
		self.pointsPosL = []
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

	def addToken(self, token):
		self.hasRecentlyChanged = True
		self.tokens.append(token)
		self.tokenPosL.append(self.nextTokenPos)
		L = len(self.tokens)
		if L%2 == 0:
			self.nextTokenPos = (self.nextTokenPos[0] - tokenSize2, self.nextTokenPos[1] + tokenSize2 + space1)
		else:
			self.nextTokenPos = (self.nextTokenPos[0] + tokenSize2, self.nextTokenPos[1])

		# print("Score du joueur ", int(self.id+1), ": ", self.computeScore())

	def addCard(self, card):
		card.resize(cardSize2)
		if card.side == RESSOURCE:
			self.addResCard(card)
		else:
			self.addBatCard(card)

	def addResCard(self, card):
		self.hasRecentlyChanged = True
		self.resCards.append(card)
		self.handPosL = []
		(x,y) = handPosL
		space = (muniPosL[0] - handPosL[0] - cardSize2[0] - space1)/len(self.resCards)
		for c in self.resCards:
			self.handPosL.append((x,y))
			x += space

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
			pass

	# test non concluant
	# def passiveDraw(self):
	# 	self.screen.blit(self.surface, PIRect[0])

	def lazyDraw(self):
		if self.hasRecentlyChanged:
			self.draw()
			self.hasRecentlyChanged = False