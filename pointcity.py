import pygame as pg
import random
from params import *
from tokenMarket import *
from baseObjects import *
from market import *
from animations import *
from inventory import *

class pointCityGame:
	def __init__(self, nPlayers):
		self.nPlayers = nPlayers # nombre de joueurs
		self.startingPlayer = random.randint(0, nPlayers - 1) # qui commence?
		self.currentPlayer = self.startingPlayer # à qui le tour?
		self.gamePhase = GPhase.DISCOVER # quelle phase de jeu?
		self.translations = []
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

	def leftClick(self, mousePos):
		match self.gamePhase:
			case GPhase.DISCOVER:
				if self.market.flipCard(mousePos):
					self.gamePhase = GPhase.MARKET
			case GPhase.MARKET:
				if self.piocheRect.collidepoint(mousePos) and len(self.market.selectedCards) == 0: # pioche directe
					def func():
						newcard = self.pioche[0]
						self.pioche = self.pioche[1:]
						self.playerInventory[self.currentPlayer].addResCard(newcard)
					self.translations.append(translation(self.pioche[0].imageRes, piochePos, playerPos, False, func))
					self.translations.append(translation(self.pioche[1].imageRes, piochePos, playerPos, False, None))
					func()
					self.endTurn()
					return
				selcards = self.market.selectCard(mousePos)
				if len(selcards) == 2: # sélection marché
					selcards.sort(key = lambda c : 4*c[0] + c[1])
					self.endMarketPhase(selcards)
					
			case GPhase.TOKEN:
				tk = self.tokenMarket.getToken(mousePos)
				if tk != None:
					def f():
						self.playerInventory[self.currentPlayer].addToken(tk)
						self.tokensLeft -= 1
						if self.tokensLeft == 0:
							self.endTurn()
					self.addAnimation(translation(tk.image, self.tokenMarket.tokenPos[0], (tokenPosLX[0], tokenPosLY), 1, f))

	def endMarketPhase(self, selcards):
		(i,j) = selcards[0]
		(k,l) = selcards[1]
		card1 = self.market.cards[i][j]
		card2 = self.market.cards[k][l]
		self.market.cards[i][j] = None
		self.market.cards[k][l] = None
		newcard1 = self.pioche[0]
		newcard2 = self.pioche[1]
		self.pioche = self.pioche[1:]
		municipalDrawn = 0
		if card1.side == BATIMENT:
			if card1.type == MUNICIPAL:
				municipalDrawn += 1
		else:
			newcard1.flip()
		if card2.side == BATIMENT:
			if card2.type == MUNICIPAL:
				municipalDrawn += 1
		else:
			newcard2.flip()

		def f1():
			self.playerInventory[self.currentPlayer].addResCard(card1)
		def f2():
			self.playerInventory[self.currentPlayer].addResCard(card2)
		# marché vers joueur
		self.addAnimation(translation(card1.getImage(), self.market.cardPos[i][j], handPosL, 0, f1))
		self.addAnimation(translation(card2.getImage(), self.market.cardPos[k][l], handPosL, 0, f2))
		# pioche vers marché
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
		self.addAnimation(translation(self.pioche[0].getImage(), piochePos, self.market.cardPos[i][j], 1, f3))
		self.addAnimation(translation(self.pioche[1].getImage(), piochePos, self.market.cardPos[k][l], 1, f4))

	def pressEscape(self):
		match self.gamePhase:
			case GPhase.DISCOVER:
				self.gamePhase = GPhase.MARKET
			case GPhase.MARKET:
				self.market.cancelSelect()

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

	def addAnimation(self, anim):
		if anim.mode == AnimMode.SEQUENTIEL:
			self.translations.append(anim)
		else:
			self.translations.insert(0, anim)

	def computeScores(self):
		pass

	def draw(self, screen):
		mousePos = pg.mouse.get_pos()
		# pioche
		if self.gamePhase == GPhase.MARKET and self.piocheRect.collidepoint(mousePos) and len(self.market.selectedCards) == 0:
			screen.fill(white, self.piocheRect)
		self.pioche[0].draw(screen, piochePos)
		# marché
		self.market.draw(screen, self.gamePhase)
		# jetons
		self.tokenMarket.draw(screen, self.gamePhase == GPhase.TOKEN)
		# joueurs
		for p in self.playerInventory:
			p.draw(screen)
		# animations
		if len(self.translations) > 0:
			print(len(self.translations))
			L = [t for t in self.translations if t.mode == AnimMode.SIMULTANE]
			if len(L) == 0:
				L.append(self.translations[0])
			for e in L:
				e.draw(screen)
				if e.done:
					self.translations.remove(e)

