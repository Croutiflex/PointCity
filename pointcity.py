import pygame as pg
import random
from params import *
from tokenMarket import *
from baseObjects import *
from market import *
from animations import *
from inventory import *

class pointCityGame:
	def __init__(self, screen, isLoadedGame, *, saveSlot=1, nPlayers=1, cheatMode=False):
		self.screen = screen
		self.lazyScreen = screen
		self.cheatMode = cheatMode
		self.nPlayers = nPlayers # nombre de joueurs
		self.startingPlayer = random.randint(0, nPlayers - 1) # qui commence?
		self.currentPlayer = self.startingPlayer # à qui le tour?
		self.gamePhase = GPhase.DISCOVER # quelle phase de jeu?
		self.translationsMJ = [] # marché vers joueur
		self.translationsPM = [] # pioche vers marché
		self.translationsPJ = [] # pioche vers joueur
		self.playerInventory = []
		self.over = False
		self.piocheText = pg.font.Font('freesansbold.ttf', fontsize1)
		(x,y) = piochePos
		self.piocheRect = pg.Rect(x-space1, y-space1, 2*space1+cardSize[0], 2*space1+cardSize[1])

		# lecture du détail des cartes & jetons
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
			Id = int(LL[5])
			card = pointCityCard(screen, tier, ressource, type, cost, value, Id)
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
			(type, info, Id) = L.split('\t')
			allTokens.append(pointCityToken(screen, int(type), info, int(Id)))
		f.close()

		if isLoadedGame: # partie sauvegardée
			f = open("saves/save_"+str(saveSlot))
			mainInfo = f.readline().strip().split('\t')
			saveInfo = f.readlines()
			f.close()
			sep = 0
			for i in range(len(saveInfo)):
				if saveInfo[i].strip() == "-----":
					sep = i
					break
			jetonsInfo = saveInfo[:i]
			cardInfo = saveInfo[i+1:]

			# infos générales
			self.cheatMode = mainInfo[0] == "True"
			self.nPlayers = int(mainInfo[1]) 
			self.startingPlayer = int(mainInfo[2])
			self.currentPlayer = int(mainInfo[3])
			self.gamePhase = int(mainInfo[4])

			# joueurs
			Id = self.currentPlayer
			print("au tour du joueur ", self.currentPlayer+1)
			for pos in range(self.nPlayers):
				self.playerInventory.append(pointCityPlayerInventory(screen, Id, pos, False))
				Id += 1
				if Id == self.nPlayers:
					Id = 0
			self.playerInventory.sort(key = lambda p : p.Id)

			# jetons
			marketTokens = []
			for line in jetonsInfo:
				L = line.strip().split('\t')
				(Id, place) = (int(L[0]), int(L[1]))
				if place == 0:
					marketTokens.append(allTokens[Id])
				else:
					self.playerInventory[place-1].addToken(allTokens[Id])

			for i in range(self.nPlayers):
				if len(self.playerInventory[i].tokens) > 0:
					self.playerInventory[i].updateTokenPos(True)
			self.tokenMarket = pointCityTokenMarket(screen, marketTokens)

			# cartes
			allCards = tier1cards + tier2cards + tier3cards
			self.pioche = []
			marketCards = [[None for i in range(4)] for i in range(4)]
			for line in cardInfo:
				L = line.strip().split('\t')
				(Id, place) = (int(L[0]), int(L[1]))
				if place == -1:
					self.pioche.append(allCards[Id])
				elif place == 0:
					LL = L[2].split(',')
					(pos, side) = ((int(LL[0]), int(LL[1])), int(L[3]))
					if side == BATIMENT:
						allCards[Id].flip()
					marketCards[pos[0]][pos[1]] = allCards[Id]
				else:
					if Id == -1:
						self.playerInventory[place-1].addInge()
					else:
						side = int(L[2])
						if side == BATIMENT:
							allCards[Id].flip()
						allCards[Id].resize(2)
						self.playerInventory[place-1].addCard(allCards[Id])
			# for p in self.playerInventory:
			# 	print("Joueur ", p.Id+1, ", prod:", p.production)
			self.market = pointCityMarket(screen, marketCards)
			self.market.updateFlip()
			self.tokensLeft = len(self.playerInventory[self.currentPlayer].muniBats) - len(self.playerInventory[self.currentPlayer].tokens)
		else: # nouvelle partie
			# joueurs
			Id = self.startingPlayer
			print("Joueur ", self.startingPlayer+1, " commence")
			for pos in range(self.nPlayers):
				self.playerInventory.append(pointCityPlayerInventory(screen, Id, pos))
				Id += 1
				if Id == self.nPlayers:
					Id = 0
			self.playerInventory.sort(key = lambda p : p.Id)

			# pioche
			random.shuffle(tier1cards)
			random.shuffle(tier2cards)
			random.shuffle(tier3cards)
			gameMatos = matos[nPlayers-1]
			cards = tier1cards[:gameMatos[0]] + tier2cards[:gameMatos[1]] + tier3cards[:gameMatos[2]]
			self.pioche = cards[16:]

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

		self.turnsLeft = 1 + int(len(self.pioche)/2)
		self.turn = 0 # à changer

		# premier draw
		self.screen.fill(backgroundColor)
		self.market.draw(self.gamePhase)
		for p in self.playerInventory:
			p.lazyDraw()
		self.tokenMarket.draw(self.gamePhase == GPhase.TOKEN)

	# sauvegarde la partie dans un fichier texte
	# slot à préciser, si le slot n'est pas vide il sera écrasé
	def saveGame(self, slot): 
		f = open("saves/save_"+str(slot), 'w')

		# infos générales
		mainInfo = str(self.cheatMode)
		mainInfo += "\t" + str(self.nPlayers)
		mainInfo += "\t" + str(self.startingPlayer)
		mainInfo += "\t" + str(self.currentPlayer)
		mainInfo += "\t" + str(int(self.gamePhase))
		f.write(mainInfo)
		
		# jetons
		for j in self.tokenMarket.tokens:
			f.write("\n" + str(j.Id) + "\t" + str(0))
		for i in range(self.nPlayers):
			for j in self.playerInventory[i].tokens:
				f.write("\n" + str(j.Id) + "\t" + str(i+1))
		
		f.write("\n-----") # ligne de séparation

		# cartes
		for c in self.pioche: #pioche
			f.write("\n" + str(c.Id) + "\t" + str(-1))
		for i in range(4):
			for j in range(4): # marché
				card = self.market.cards[i][j]
				f.write("\n" + str(card.Id) + "\t" + str(0)  + "\t" + str(i) + "," + str(j) + "\t" + str(card.side))
		for i in range(self.nPlayers): #joueurs
			for c in self.playerInventory[i].resCards + self.playerInventory[i].muniBats + self.playerInventory[i].pointsBats:
				f.write("\n" + str(c.Id) + "\t" + str(i+1) + "\t" + str(c.side))
			for j in range(5):
				for c in self.playerInventory[i].batCards[j]:
					f.write("\n" + str(c.Id) + "\t" + str(i+1) + "\t" + str(c.side))
		f.close()
		print("Partie sauvegardée! (", slot,")")

	def pressTab(self):
		self.saveGame(self.nPlayers)

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
				self.playerInventory[self.currentPlayer].selectHandCard(mousePos)
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
					self.translationsPJ.append(translation(self.screen, tk.getImage(), self.tokenMarket.tokenPos[tkpos], pos, f, translationTime2))

	def directDraw(self):
		if len(self.pioche) == 0:
			self.screen.fill(red, self.piocheRect)
			return
		card1 = self.pioche[0]
		self.pioche = self.pioche[1:]
		card1.resize(2)
		card2 = self.pioche[0]
		print("pioche cartes ", card1.Id, " et ", card2.Id)
		def f1():
			card2.resize(2)
			self.pioche = self.pioche[1:]
			self.playerInventory[self.currentPlayer].addCard(card1)
		def f2():
			self.playerInventory[self.currentPlayer].addCard(card2)
			self.endTurn()
		self.translationsPJ.append(translation(self.screen, card1.getImage(), piochePos, handPosL, f1))
		self.translationsPJ.append(translation(self.screen, card2.getImage(2), piochePos, handPosL, f2))

	# compare le coût des batiments sélectionnés et les ressources du joueur. Renvoie True si l'achat est possible.
	def checkCost(self, cards):
		if self.cheatMode:
			return True
		cost = [0 for i in range(5)]

		drawnCards = []
		for c in cards:
			if c.side == BATIMENT:
				for i in range(5):
					cost[i] += c.cost[i]
			else:
				drawnCards.append(c)

		# on déduit d'abord la prod
		prodRes = self.playerInventory[self.currentPlayer].production
		print("coût: ", cost, ", prod: ", prodRes, ", current =", self.currentPlayer+1)
		unpaidRes = []
		for i in range(5):
			cost[i] = max(0, cost[i] - prodRes[i])
			if cost[i] > 0:
				unpaidRes.append(i)
		if len(unpaidRes) == 0:
			return True

		# ressources simples & doubles
		doubleResCards = {}
		simpleResCards = {}
		for i in range(5):
			doubleResCards[i] = []
			simpleResCards[i] = []
		ingés = []
		handCards = self.playerInventory[self.currentPlayer].selectedCards
		# ressources sélectionnées dans la main + carte piochée s'il y a
		for c in handCards + drawnCards:
			if c.ressource == INGENIEUR:
				ingés.append(c)
			elif c.ressource in unpaidRes:
				if c.tier > 0:
					doubleResCards[c.ressource].append(c)
				else:
					simpleResCards[c.ressource].append(c)

		usedCards = []
		canPayOneWithDouble = [False for i in range(5)]
		# 1re passe
		for i in unpaidRes:
			while cost[i] > 1 and len(doubleResCards[i]) > 0:
				usedCards.append(doubleResCards[i].pop())
				cost[i] -= 2
			while cost[i] > 0 and len(simpleResCards[i]) > 0:
				usedCards.append(simpleResCards[i].pop())
				cost[i] -= 1
			if cost[i] > 0 and len(doubleResCards[i]) > 0:
				canPayOneWithDouble[i] = True
		unpaidRes2 = []
		for i in unpaidRes:
			if cost[i] > 0:
				unpaidRes2.append(i)
		unpaidRes = unpaidRes2

		# 2e passe
		for i in unpaidRes:
			if not canPayOneWithDouble[i]:
				# print("ressource: ", i, ', coût: ', cost[i], ", ingés: ", len(ingés))
				while cost[i] > 0 and len(ingés) > 0:
					usedCards.append(ingés.pop())
					cost[i] -= 1
				if cost[i] > 0:
					print("pas de quoi payer : ", i)
					return False
		unpaidRes2 = []
		for i in unpaidRes:
			if cost[i] > 0:
				unpaidRes2.append(i)
		unpaidRes = unpaidRes2

		# 3e passe
		for i in unpaidRes:
			if canPayOneWithDouble[i]:
				usedCards.append(doubleResCards[i].pop())
			else:
				print("pas de quoi payer : ", i)
				return False

		# on enlève les cartes utilisées pour payer
		print("cartes utilisées:")
		for c in usedCards:
			print(c.Id)
			if c in drawnCards:
				# si la carte ressource piochée est utilisée pour l'achat, on envoie un signal
				c.cost = 0
			else:
				self.playerInventory[self.currentPlayer].resCards.remove(c)
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
			self.playerInventory[self.currentPlayer].resetSelection()
			self.market.drawSingleCard((i,j), red)
			self.market.drawSingleCard((k,l), red)
			return

		self.playerInventory[self.currentPlayer].resetSelection()
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
		# print("Tour ", self.turn)
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
		pg.time.wait(pauseTime1)

	def computeScores(self):
		scores = [(i+1, self.playerInventory[i].computeScore()) for i in range(self.nPlayers)]
		scores.sort(reverse = True, key = lambda x: x[1])
		print("Joueur ", scores[0][0], " a gagné!")
		for (player, score) in scores:
			print("Score du joueur ", player, ": ", score)

	def draw(self):
		if self.turnsLeft == 0 and len(self.translationsMJ) + len(self.translationsPM) + len(self.translationsPJ) == 0: # fin de partie à la fin des animations
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
				p.lazyDraw(self.gamePhase==GPhase.MARKET)

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

