import pygame as pg
from enum import IntEnum
import os

## ENUMS

# face carte
RESSOURCE = 0
BATIMENT = 1

# ressources
COMMU = 0
ECONOMIE = 1
ENERGIE = 2
ECOLOGIE = 3
INDUSTRIE = 4
INGENIEUR = 5

# type de batiment
RESSOURCE = 0
MUNICIPAL = 1
POINTS = 2

# phase de jeu
class GPhase(IntEnum):
	DISCOVER = 0
	MARKET = 1
	TOKEN = 2 

# types de jetons
POINTS = 0
SIMPLE = 1
DOUBLE = 2
DIVERSITY = 3
MISS = 4
MULTI = 5

## DISTRUBUTION
# nombre de cartes/jetons de chaque tier en fct du nb de joueurs
matos1 = [40, 24, 18, 10]
matos2 = [40, 24, 18, 10]
matos3 = [52, 36, 28, 12]
matos4 = [64, 48, 38, 14]
matos = [matos1, matos2, matos3, matos4]

## DIMENSIONS (PARAM)
# constantes
screenSize = (1920, 1080)
space1 = 5
space2 = 15
space3 = 25
cardRatio = 0.66
# adaptables
cardH = (screenSize[1] - 2*space3 - 3*space2)/4
cardL = cardH*cardRatio
cardSize = (cardL, cardH)
marketPos = (space3, space3)
piochePos = (space3*2 + cardL*4 + space2*3, space3)
tkMarketPos = (piochePos[0], piochePos[1] + cardSize[1] + space2)
tokenSize = (screenSize[1]-2*space3-space2-6*space1-cardH)/7
TKR = space1 + tokenSize/2
PIx = piochePos[0] + tokenSize*2 + space1 + space3
PIL = screenSize[0] - PIx - space3
PIH = (screenSize[1] - 2*space3)/2 - space2
PIh = ((screenSize[1] - 2*space3)/2 - 3*space2)/3
PIRect = [pg.Rect((PIx, space3), (PIL, PIH))]
PIRect += [pg.Rect((PIx, PIH + space3 + space2 + i*(PIh + space2)), (PIL, PIh)) for i in range(3)]
# fonds par zones
marketBackgroundRect = pg.Rect((0,0), (PIx, screenSize[1]))
PIBackgroundRect = pg.Rect((piochePos[0] - space2, 0), (screenSize[0] - PIx, screenSize[1]))
# inventaire détaillé
tokenSize2 = (PIL/5 + space1*2)/2
tokenPosLX = (PIx + space1, PIx + space1 + tokenSize2)
tokenPosLY = 2*space3
handPosL = (tokenPosLX[1] + tokenSize2 + space1, space3 + space1)
cardH2 = (PIH - 2*space1 - space2)/2.5
cardSize2 = (cardH2*cardRatio, cardH2)
cityPosL = [(handPosL[0], handPosL[1] + cardH2 + space2)]
cityPosL += [(cityPosL[0][0] + i*(cardSize2[0] + space2), cityPosL[0][1]) for i in range(1,5)]

## TIMING
translationTime = 30

## COLORS
backgroundColor = pg.Color(200,200,200)
boardBackgroundColor = pg.Color(0,0,30)
white = pg.Color(255,255,255)
blue = pg.Color(50,100,255)
green = pg.Color(50,255,100)
red = pg.Color(255,100,50)
playerColors = [pg.Color(25,50,128), pg.Color(25,128,50), pg.Color(128,50,25), pg.Color(128,128,25)]

## IMAGES
# RESSOURCES
ImgRes = []
ImgRes.append(pg.transform.scale(pg.image.load("res/commu.png"), cardSize))
ImgRes.append(pg.transform.scale(pg.image.load("res/economie.png"), cardSize))
ImgRes.append(pg.transform.scale(pg.image.load("res/energie.png"), cardSize))
ImgRes.append(pg.transform.scale(pg.image.load("res/ecologie.png"), cardSize))
ImgRes.append(pg.transform.scale(pg.image.load("res/industrie.png"), cardSize))
ImgRes.append(pg.transform.scale(pg.image.load("res/ingenieur.png"), cardSize))
ImgRes2 = []
ImgRes2.append(pg.transform.scale(pg.image.load("res/commu_double.png"), cardSize))
ImgRes2.append(pg.transform.scale(pg.image.load("res/economie_double.png"), cardSize))
ImgRes2.append(pg.transform.scale(pg.image.load("res/energie_double.png"), cardSize))
ImgRes2.append(pg.transform.scale(pg.image.load("res/ecologie_double.png"), cardSize))
ImgRes2.append(pg.transform.scale(pg.image.load("res/industrie_double.png"), cardSize))
ImgRes2.append(pg.transform.scale(pg.image.load("res/ingenieur.png"), cardSize))

# BATIMENTS
batiments = []
for i in range(160):
	file = "res/batiments/"+str(i)+".png"
	if os.path.exists(file):
		batiments.append(pg.transform.scale(pg.image.load(file), cardSize))
	else:
		batiments.append(pg.transform.scale(pg.image.load("res/batiments/dummy.png"), cardSize))

# JETONS
jetons = []
for i in range(22):
	jetons.append(pg.transform.scale(pg.image.load("res/jetons/"+str(i)+".png"), (tokenSize, tokenSize)))