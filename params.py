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

resName = ["Communauté", "Economie", "Energie", "Ecologie", "Industrie", "Ingénieur"]

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
cardRatio = 0.66 # H/L
fontsize1 = 30

# adaptables
cardH = (screenSize[1] - 2*space3 - 3*space2)/4
# cardH = 500
cardL = cardH*cardRatio
cardSize = (cardL, cardH)
marketPos = (space3, space3)
piochePos = (space3*2 + cardL*4 + space2*3, space3)
piocheTextPos = (piochePos[0] + cardSize[0] + space1, piochePos[1])
tkMarketPos = (piochePos[0], piochePos[1] + cardSize[1] + space2)
tokenSize = (screenSize[1]-2*space3-space2-6*space1-cardH)/7
TKR = space1 + tokenSize/2

# inventaires
PIx = piochePos[0] + tokenSize*2 + space1 + space3
PIL = screenSize[0] - PIx - space3
PIxHalf = PIx + PIL/2
PIH = (screenSize[1] - 2*space3)/2 - space2
PIh = ((screenSize[1] - 2*space3)/2 - 3*space2)/3
PIRect = [pg.Rect((PIx, space3), (PIL, PIH))]
PIRect += [pg.Rect((PIx, PIH + space3 + space2 + i*(PIh + space2)), (PIL, PIh)) for i in range(3)]
titlePos = [(PIRect[i].x + space2, PIRect[i].y + space2) for i in range(4)]

# inventaire détaillé
cardH2 = (PIH - 2*space1 - space2)/2.5
cardSize2 = (cardH2*cardRatio, cardH2)
tokenSize2 = (PIL/5 + space1*2)/2
tokenPosL = (PIx + space1, titlePos[0][1] + fontsize1 + space2)
handPosL = (titlePos[0][0] + tokenSize2*2 + space1, titlePos[0][1])
muniPosL = (handPosL[0] + cardSize2[0]*2.5 + space1, handPosL[1])
handRect = pg.Rect(handPosL, (muniPosL[0] - handPosL[0] - space1, cardSize2[1])).scale_by(1.05)
pointsPosL = (screenSize[0] - space3 - space2 - cardSize2[0], handPosL[1])
cityPosL = [(handPosL[0], handPosL[1] + cardH2 + space2)]
cityPosL += [(cityPosL[0][0] + i*(cardSize2[0] + space2), cityPosL[0][1]) for i in range(1,5)]

# inventaire réduit, par joueur après le 1er
tokenSize3 = PIh - 2*space1 - fontsize1 - space2
cardSize3 = (tokenSize3*cardRatio, tokenSize3)
tokenPosl = [(p[0], p[1] + fontsize1 + space1) for p in titlePos[1:]]
handPosl = [(PIxHalf + space1, p[1]) for p in tokenPosl]
iconResSize = (fontsize1, fontsize1)
iconResX = [titlePos[0][0] + fontsize1*7 + i*(fontsize1*4) for i in range(5)]
prodTextX = [x + fontsize1*2 for x in iconResX]
pointBubbleR1 = fontsize1+space1
pointBubbleR2 = fontsize1
pointBubbleCenter = [(R.right-pointBubbleR1, R.top+pointBubbleR1) for R in PIRect[1:]]

# fonds
marketBackgroundRect = pg.Rect((0,0), (PIx, screenSize[1]))
PIBackgroundRect = pg.Rect((piochePos[0] - space2, 0), (screenSize[0] - PIx, screenSize[1]))

## TIMING
translationTime = 30

## COLORS
menuBackgroundColor = pg.Color(122,183,191)
backgroundColor = pg.Color(200,200,200)
textColor = pg.Color(120,0,60)
white = pg.Color(255,255,255)
darkBlue = pg.Color(20,0,77)
blue = pg.Color(50,100,255)
green = pg.Color(50,255,100)
red = pg.Color(255,100,50)
playerColors = [pg.Color(200,200,255), pg.Color(200,255,200), pg.Color(255,200,200), pg.Color(255,255,200)]

## IMAGES
# RESSOURCES
ImgRes = []
ImgRes.append(pg.transform.smoothscale(pg.image.load("res/commu.png"), cardSize))
ImgRes.append(pg.transform.smoothscale(pg.image.load("res/economie.png"), cardSize))
ImgRes.append(pg.transform.smoothscale(pg.image.load("res/energie.png"), cardSize))
ImgRes.append(pg.transform.smoothscale(pg.image.load("res/ecologie.png"), cardSize))
ImgRes.append(pg.transform.smoothscale(pg.image.load("res/industrie.png"), cardSize))
ImgRes.append(pg.transform.smoothscale(pg.image.load("res/ingenieur.png"), cardSize))

ImgRes2 = []
ImgRes2.append(pg.transform.smoothscale(pg.image.load("res/commu_double.png"), cardSize))
ImgRes2.append(pg.transform.smoothscale(pg.image.load("res/economie_double.png"), cardSize))
ImgRes2.append(pg.transform.smoothscale(pg.image.load("res/energie_double.png"), cardSize))
ImgRes2.append(pg.transform.smoothscale(pg.image.load("res/ecologie_double.png"), cardSize))
ImgRes2.append(pg.transform.smoothscale(pg.image.load("res/industrie_double.png"), cardSize))
ImgRes2.append(pg.transform.smoothscale(pg.image.load("res/ingenieur.png"), cardSize))

iconRes = [pg.transform.smoothscale(pg.image.load("res/icon"+str(i)+".png"), iconResSize) for i in range(5)]

# BATIMENTS
batiments = []
for i in range(160):
	file = "res/batiments/"+str(i)+".png"
	if os.path.exists(file):
		batiments.append(pg.transform.smoothscale(pg.image.load(file), cardSize))
	else:
		batiments.append(pg.transform.smoothscale(pg.image.load("res/batiments/dummy.png"), cardSize))

# JETONS
jetons = []
for i in range(22):
	jetons.append(pg.transform.smoothscale(pg.image.load("res/jetons/"+str(i)+".png"), (tokenSize, tokenSize)))
