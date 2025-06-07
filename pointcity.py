import pygame as pg
import random
from params import *
from tokenMarket import *
from baseObjects import *
from market import *
from animations import *
from inventory import *

class pointCityGame:
	def __init__(self, screen, nPlayers):
		self.nPlayers = nPlayers # nombre de joueurs
		self.startingPlayer = random.randint(0, nPlayers - 1) # qui commence?
		self.currentPlayer = self.startingPlayer # à qui le tour?
		self.gamePhase = GPhase.DISCOVER # quelle phase de jeu?
		self.translationsMJ = [] # marché vers joueur
		self.translationsPM = [] # pioche vers marché
		self.translationsPJ = [] # pioche vers joueur
		self.tokensLeft = 0

		## par joueur :
		self.playerInventory = []
		for p in range(self.nPlayers):
			self.playerInventory.append(pointCityPlayerInventory(p))

		# lecture des cartes & jetons
		tier1cards = []
		tier2cards = []
		tier3cards = []
		f = open('res/PointCityCards.tsv')
		for L in f.readlines()[1:]:
			LL = L.strip().split('\t')
			tier = int(LL[0])
			ressource = int(LL[1])
			type = LL[2]
			cost = [int(c) for c in LL[3][1:-1].split(',')]
			value = int(LL[4])
			numImg = int(LL[5])
			card = pointCityCard(tier, ressource, type, cost, value, numImg)
			match tier:
				case 0:
					tier1cards.append(card)
				case 1:
					tier2cards.append(card)
				case 2:
					tier3cards.append(card)
		f.close()

		f = open('res/PointCityTokens.tsv')
		allTokens = []
		for L in f.readlines()[1:]:
			(type, info, image) = L.split('\t')
			allTokens.append(pointCityToken(int(type), info, int(image)))
		f.close()

		# pioche
		random.shuffle(tier1cards)
		random.shuffle(tier2cards)
		random.shuffle(tier3cards)
		gameMatos = matos[nPlayers-1]
		cards = tier1cards[:gameMatos[0]] + tier2cards[:gameMatos[1]] + tier3cards[:gameMatos[2]]
		self.pioche = cards[16:]
		(x,y) = piochePos
		self.piocheRect = pg.Rect(x-space1, y-space1, 2*space1+cardSize[0], 2*space1+cardSize[1])
		
		# marché
		marketCards = []
		n = 0
		for i in range(4):
			L = []
			for j in range(4):
				L.append(cards[n])
				n += 1
			marketCards.append(L)
		self.market = pointCityMarket(marketCards)

		# inventaire des jetons
		random.shuffle(allTokens)
		self.tokenMarket = pointCityTokenMarket(allTokens[:gameMatos[3]])

		# premier draw
		self.market.draw(screen, self.gamePhase)
		for p in self.playerInventory:
			p.draw(screen)

	def leftClick(self,	screen, mousePos):
		match self.gamePhase:
			case GPhase.DISCOVER:
				if self.market.flipCard(mousePos):
					self.gamePhase = GPhase.MARKET
					self.market.draw(screen, self.gamePhase)
			case GPhase.MARKET:
				if self.piocheRect.collidepoint(mousePos) and len(self.market.selectedCards) == 0: # pioche directe
					self.directDraw()
					return
				selcards = self.market.selectCard(screen, mousePos)
				if len(selcards) == 2: # sélection marché
					selcards.sort(key = lambda c : 4*c[0] + c[1])
					self.drawFromMarket(selcards)
					
			case GPhase.TOKEN:
				tk = self.tokenMarket.getToken(mousePos)
				tkpos = self.tokenMarket.findToken(mousePos)
				tk.resize((tokenSize2, tokenSize2))
				if tk != None:
					def f():
						self.playerInventory[self.currentPlayer].addToken(tk)
						self.tokensLeft -= 1
						if self.tokensLeft == 0:
							self.endTurn()
					self.translationsPJ.append(translation(tk.image, self.tokenMarket.tokenPos[tkpos], (tokenPosLX[0], tokenPosLY), f))

	def directDraw(self):
		card1 = self.pioche[0]
		self.pioche = self.pioche[1:]
		card1.resize(cardSize2)
		card2 = self.pioche[0]
		def f1():
			card2.resize(cardSize2)
			self.pioche = self.pioche[1:]
			self.playerInventory[self.currentPlayer].addResCard(card1)
		def f2():
			self.playerInventory[self.currentPlayer].addResCard(card2)
			self.endTurn()
		self.translationsPJ.append(translation(card1.imageRes, piochePos, handPosL, f1))
		self.translationsPJ.append(translation(pg.transform.scale(card2.imageRes, cardSize2), piochePos, handPosL, f2))

	# compare le coût des batiments sélectionnés et les ressources du joueur. Renvoie True si l'achat est possible.
	def checkCost(self, selcards):
		return True

	def drawFromMarket(self, selcards):
		if not self.checkCost(selcards): # si achat pas possible
			return
		(i,j) = selcards[0]
		(k,l) = selcards[1]
		card1 = self.market.cards[i][j]
		card2 = self.market.cards[k][l]
		self.market.cards[i][j] = None
		self.market.cards[k][l] = None
		newcard1 = self.pioche[0]
		newcard2 = self.pioche[1]
		municipalDrawn = 0
		if card1.side == BATIMENT:
			if card1.type == "municipal":
				municipalDrawn += 1
		else:
			newcard1.flip()
		if card2.side == BATIMENT:
			if card2.type == "municipal":
				municipalDrawn += 1
		else:
			newcard2.flip()

		def f1():
			self.playerInventory[self.currentPlayer].addResCard(card1)
		def f2():
			self.playerInventory[self.currentPlayer].addResCard(card2)
			self.pioche = self.pioche[1:]
		# marché vers joueur
		self.translationsMJ.append(translation(card1.getImage(), self.market.cardPos[i][j], handPosL, f1))
		self.translationsMJ.append(translation(card2.getImage(), self.market.cardPos[k][l], handPosL, f2))

		def f3():
			self.market.cards[i][j] = newcard1
			self.pioche = self.pioche[1:]
		def f4():
			self.market.cards[k][l] = newcard2
			if municipalDrawn > 0:
				self.tokensLeft = municipalDrawn
				self.gamePhase = GPhase.TOKEN
			else:
				self.endTurn()
		# pioche vers marché
		self.translationsPM.append(translation(newcard1.getImage(), piochePos, self.market.cardPos[i][j], f3))
		self.translationsPM.append(translation(newcard2.getImage(), piochePos, self.market.cardPos[k][l], f4))

	def pressEscape(self, screen):
		match self.gamePhase:
			case GPhase.DISCOVER:
				self.gamePhase = GPhase.MARKET
			case GPhase.MARKET:
				self.market.cancelSelect(screen)

	def endTurn(self):
		self.currentPlayer += 1
		if self.currentPlayer == self.nPlayers:
			self.currentPlayer = 0
		for p in self.playerInventory:
			p.endTurn(self.nPlayers)
		self.market.updateFlip()
		if self.market.canFlip():
			self.gamePhase = GPhase.DISCOVER
		else:
			self.gamePhase = GPhase.MARKET

	def computeScores(self):
		pass

	def draw(self, screen):
		# marché
		if len(self.translationsMJ) + len(self.translationsPM) > 0:
			self.market.draw(screen, self.gamePhase)
		else:
			self.market.lazyDraw(screen, self.gamePhase)

		# joueurs
		if len(self.translationsMJ) + len(self.translationsPJ) > 0:
			screen.fill(backgroundColor, PIBackgroundRect)
			for p in self.playerInventory:
				p.draw(screen)
		else:
			for p in self.playerInventory:
				p.lazyDraw(screen)
		mousePos = pg.mouse.get_pos()
		# pioche
		if self.gamePhase == GPhase.MARKET and self.piocheRect.collidepoint(mousePos) and len(self.market.selectedCards) == 0:
			screen.fill(white, self.piocheRect)
		self.pioche[0].draw(screen, piochePos)
		# jetons
		self.tokenMarket.draw(screen, self.gamePhase == GPhase.TOKEN)
		
		# animations
		if len(self.translationsPJ) > 0:
			t = self.translationsPJ.pop(0)
			if not t.done:			
				t.draw(screen)
				self.translationsPJ.insert(0, t)

		L = []
		while len(self.translationsMJ) > 0:
			t = self.translationsMJ.pop()
			if not t.done:			
				t.draw(screen)
				L.append(t)
		self.translationsMJ = L

		if len(self.translationsMJ) == 0 and len(self.translationsPM) > 0:
			t = self.translationsPM.pop(0)
			if not t.done:			
				t.draw(screen)
				self.translationsPM.insert(0, t)

