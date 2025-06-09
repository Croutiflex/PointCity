import pygame as pg
import random
from params import *
from tokenMarket import *
from baseObjects import *
from market import *
from animations import *
from inventory import *

class pointCityGame:
	def __init__(self, screen, nPlayers, cheatMode):
		self.cheatMode = cheatMode
		self.nPlayers = nPlayers # nombre de joueurs
		self.startingPlayer = random.randint(0, nPlayers - 1) # qui commence?
		self.currentPlayer = self.startingPlayer # à qui le tour?
		self.gamePhase = GPhase.DISCOVER # quelle phase de jeu?
		self.translationsMJ = [] # marché vers joueur
		self.translationsPM = [] # pioche vers marché
		self.translationsPJ = [] # pioche vers joueur
		self.tokensLeft = 0
		self.screen = screen
		self.over = False
		self.turn = 0

		# text nbr de cartes
		self.piocheText = pg.font.Font('freesansbold.ttf', fontsize1)

		## par joueur :
		self.playerInventory = []
		player = self.startingPlayer
		for p in range(self.nPlayers):
			self.playerInventory.append(pointCityPlayerInventory(screen, p, player))
			player += 1
			if player == nPlayers:
				player = 0

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
			card = pointCityCard(screen, tier, ressource, type, cost, value, numImg)
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
			allTokens.append(pointCityToken(screen, int(type), info, int(image)))
		f.close()

		# pioche
		random.shuffle(tier1cards)
		random.shuffle(tier2cards)
		random.shuffle(tier3cards)
		gameMatos = matos[nPlayers-1]
		cards = tier1cards[:gameMatos[0]] + tier2cards[:gameMatos[1]] + tier3cards[:gameMatos[2]]
		self.pioche = cards[16:]
		self.turnsLeft = 1 + int(len(self.pioche)/2)
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
		self.market = pointCityMarket(screen, marketCards)

		# inventaire des jetons
		random.shuffle(allTokens)
		self.tokenMarket = pointCityTokenMarket(screen, allTokens[:gameMatos[3]])

		# premier draw
		self.market.draw(self.gamePhase)
		for p in self.playerInventory:
			p.draw()
		self.tokenMarket.draw(False)


	def leftClick(self, mousePos):
		if self.over:
			return
		match self.gamePhase:
			case GPhase.DISCOVER:
				if self.market.flipCard(mousePos):
					self.gamePhase = GPhase.MARKET
					self.market.draw(self.gamePhase)
					self.tokenMarket.draw(self.gamePhase == GPhase.TOKEN)
			case GPhase.MARKET:
				if self.piocheRect.collidepoint(mousePos) and len(self.market.selectedCards) == 0: # pioche directe
					self.directDraw()
					return
				selcards = self.market.selectCard(mousePos)
				if len(selcards) == 2: # sélection marché
					selcards.sort(key = lambda c : 4*c[0] + c[1])
					self.drawFromMarket(selcards)
					
			case GPhase.TOKEN:
				if len(self.tokenMarket.tokens) == 0:
					self.endTurn()
					return
				tk = self.tokenMarket.getToken(mousePos)
				tkpos = self.tokenMarket.findToken(mousePos)
				if tk != None:
					tk.resize(2)
					def f():
						self.playerInventory[self.currentPlayer].addToken(tk)
						self.tokensLeft -= 1
						if self.tokensLeft == 0:
							self.endTurn()
					pos = self.playerInventory[self.currentPlayer].updateTokenPos()
					self.translationsPJ.append(translation(self.screen, tk.getImage(), self.tokenMarket.tokenPos[tkpos], pos, f))

	def directDraw(self):
		if len(self.pioche) == 0:
			self.screen.fill(red, self.piocheRect)
			return
		card1 = self.pioche[0]
		self.pioche = self.pioche[1:]
		card1.resize(2)
		card2 = self.pioche[0]
		def f1():
			card2.resize(2)
			self.pioche = self.pioche[1:]
			self.playerInventory[self.currentPlayer].addResCard(card1)
		def f2():
			self.playerInventory[self.currentPlayer].addResCard(card2)
			self.endTurn()
		self.translationsPJ.append(translation(self.screen, card1.getImage(), piochePos, handPosL, f1))
		self.translationsPJ.append(translation(self.screen, pg.transform.scale(card2.getImage(), cardSize2), piochePos, handPosL, f2))

	# compare le coût des batiments sélectionnés et les ressources du joueur. Renvoie True si l'achat est possible.
	def checkCost(self, cards):
		if self.cheatMode:
			return True
		cost = [0 for i in range(5)]
		handCards = self.playerInventory[self.currentPlayer].resCards
		resDrawn = []
		for c in cards:
			if c.side == BATIMENT:
				for i in range(5):
					cost[i] += c.cost[i]
			else:
				resDrawn.append(c)
		resCards = resDrawn + handCards
		resCards.sort(key = lambda c : c.ressource if c.tier == 0 else 10)
		# print([c.ressource for c in resCards])
		freeRes = self.playerInventory[self.currentPlayer].production
		isFree = True
		for i in range(5):
			x = max(0, cost[i] - freeRes[i])
			cost[i] = x
			if x > 0:
				isFree = False
		if isFree:
			return True
		if sum(cost) > len(resCards):
			return False
		usedCards = []
		for i in range(5): 
			if cost[i] > 0:
				# print("ressource nécessaire: ", i, ", quantité: ", cost[i])
				unusedCards = []
				while cost[i] > 0 and len(resCards) > 0:
					c = resCards.pop(0)
					if c.ressource == i or c.ressource == INGENIEUR:
						usedCards.append(c)
						cardValue = 1 if c.tier == 0 or c.ressource == INGENIEUR else 2
						# print("trouvé: ", c.ressource, ", quantité: ", cardValue)
						cost[i] = max(0, cost[i] - cardValue)
					else:
						unusedCards.append(c)
				resCards = unusedCards + resCards
				# print("reste: ", [c.ressource for c in resCards])
				if cost[i] > 0:
					print("ressource manquante: ", i)
					return False
		if len(resDrawn) > 0:
			if resDrawn[0] in resCards:
				# si la carte ressource piochée n'est pas utilisée pour l'achat, on l'enlève car elle sera ajoutée à la main plus tard
				resCards.remove(resDrawn[0]) 
			elif resDrawn[0] in usedCards:
				# si la carte ressource piochée est utilisée pour l'achat, on envoie un signal
				resDrawn[0].cost = 0
		self.playerInventory[self.currentPlayer].resCards = resCards
		return True

	def drawFromMarket(self, selcards):
		(i,j) = selcards[0]
		(k,l) = selcards[1]
		card1 = self.market.cards[i][j]
		card2 = self.market.cards[k][l]
		municipalDrawn = 0
		batDrawn = 0
		if card1.side == BATIMENT:
			batDrawn += 1
			if card1.type == "municipal":
				municipalDrawn += 1
		if card2.side == BATIMENT:
			batDrawn += 1
			if card2.type == "municipal":
				municipalDrawn += 1

		if batDrawn > 0 and not self.checkCost([card1, card2]): # si achat pas possible
			self.market.drawSingleCard((i,j), red)
			self.market.drawSingleCard((k,l), red)
			return

		card1.resize(2)
		card2.resize(2)

		def f1():
			self.playerInventory[self.currentPlayer].addCard(card1)
		def f2():
			self.playerInventory[self.currentPlayer].addCard(card2)

		# marché vers joueur
		if card1.side == RESSOURCE:
			if card1.cost != 0: # si la carte n'a pas été utilisée pour l'achat
				self.translationsMJ.append(translation(self.screen, card1.getImage(), self.market.cardPos[i][j], handPosL, f1))
		else:
			pos = muniPosL
			if card1.type == "ressource":
				pos = cityPosL[card1.ressource]
			elif card1.type == "points":
				pos = pointsPosL
			self.translationsMJ.append(translation(self.screen, card1.getImage(), self.market.cardPos[i][j], pos, f1))

		if card2.side == RESSOURCE:
			if card2.cost != 0: # si la carte n'a pas été utilisée pour l'achat
				self.translationsMJ.append(translation(self.screen, card2.getImage(), self.market.cardPos[k][l], handPosL, f2))
		else:
			pos = muniPosL
			if card2.type == "ressource":
				pos = cityPosL[card2.ressource]
			if card2.type == "points":
				pos = pointsPosL
			self.translationsMJ.append(translation(self.screen, card2.getImage(), self.market.cardPos[k][l], pos, f2))

		self.market.cards[i][j] = None
		self.market.cards[k][l] = None

		if self.turnsLeft == 1: # si c'est le dernier tour
			if municipalDrawn > 0:
				self.tokensLeft = municipalDrawn
				self.gamePhase = GPhase.TOKEN
			else:
				self.endTurn()
			return

		# pioche vers marché
		newcard1 = self.pioche[0]
		newcard2 = self.pioche[1]
		if card1.side == RESSOURCE:
			newcard1.flip()
		if card2.side == RESSOURCE:
			newcard2.flip()

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
		
		self.translationsPM.append(translation(self.screen, newcard1.getImage(), piochePos, self.market.cardPos[i][j], f3))
		self.translationsPM.append(translation(self.screen, newcard2.getImage(), piochePos, self.market.cardPos[k][l], f4))

	def pressEscape(self):
		match self.gamePhase:
			case GPhase.DISCOVER:
				self.gamePhase = GPhase.MARKET
				self.market.draw(GPhase.MARKET)
				self.tokenMarket.draw(self.gamePhase == GPhase.TOKEN)
			case GPhase.MARKET:
				self.market.cancelSelect()

	def endTurn(self):
		self.turnsLeft -= 1
		self.turn += 1
		print("Tour ", self.turn)
		if self.turnsLeft == 0:
			return
		self.currentPlayer += 1
		if self.currentPlayer == self.nPlayers:
			self.currentPlayer = 0
		print("Joueur ", str(self.currentPlayer + 1))
		for p in self.playerInventory:
			p.endTurn(self.nPlayers)
		self.market.updateFlip()
		if self.market.canFlip():
			self.gamePhase = GPhase.DISCOVER
		else:
			self.gamePhase = GPhase.MARKET
		self.market.draw(self.gamePhase)
		self.tokenMarket.draw(self.gamePhase == GPhase.TOKEN)

	def computeScores(self):
		scores = [(i+1, self.playerInventory[i].computeScore()) for i in range(self.nPlayers)]
		scores.sort(reverse = True, key = lambda x: x[1])
		print("Joueur ", scores[0][0], " a gagné!")
		for (player, score) in scores:
			print("Score du joueur ", player, ": ", score)

	def draw(self):
		if self.turnsLeft == 0 and len(self.translationsMJ) + len(self.translationsPM) + len(self.translationsPJ) == 0:
			self.over = True
			return

		# marché & jetons
		if len(self.translationsMJ) + len(self.translationsPM) > 0:
			self.market.draw(self.gamePhase)
			self.tokenMarket.draw(self.gamePhase == GPhase.TOKEN)
		else:
			self.market.lazyDraw(self.gamePhase)
			self.tokenMarket.lazyDraw(self.gamePhase == GPhase.TOKEN)

		# joueurs
		if len(self.translationsMJ) + len(self.translationsPJ) > 0:
			self.screen.fill(backgroundColor, PIBackgroundRect)
			self.tokenMarket.draw(self.gamePhase == GPhase.TOKEN)
			for p in self.playerInventory:
				p.draw()
		else:
			self.tokenMarket.lazyDraw(self.gamePhase == GPhase.TOKEN)
			for p in self.playerInventory:
				p.lazyDraw()

		mousePos = pg.mouse.get_pos()

		# pioche
		if self.gamePhase == GPhase.MARKET and self.piocheRect.collidepoint(mousePos) and len(self.market.selectedCards) == 0:
			self.screen.fill(white, self.piocheRect)
		else:
			self.screen.fill(backgroundColor, self.piocheRect)

		if len(self.pioche) > 0:
			self.pioche[0].draw(piochePos)
		pText = self.piocheText.render(str(len(self.pioche)), True, textColor, backgroundColor)
		self.screen.blit(pText, pText.get_rect().move(piocheTextPos))
		
		# animations
		if len(self.translationsPJ) > 0:
			t = self.translationsPJ.pop(0)
			if not t.done:			
				t.draw()
				self.translationsPJ.insert(0, t)

		l = len(self.translationsMJ)
		L = []
		while len(self.translationsMJ) > 0:
			t = self.translationsMJ.pop()
			if not t.done:			
				t.draw()
				L.append(t)
		if l > 0 and len(L) == 0 and len(self.pioche) > 1:
			self.pioche = self.pioche[1:]
		self.translationsMJ = L

		if len(self.translationsMJ) == 0 and len(self.translationsPM) > 0:
			t = self.translationsPM.pop(0)
			if not t.done:			
				t.draw()
				self.translationsPM.insert(0, t)

