import numpy as np
import pygame as pg
import sys
import random
from pointcity import *
from startMenu import *
from mainMenu import *
from params import *

def main():

	# setup
	pg.init()
	screen = pg.display.set_mode(screenSize, pg.SCALED | pg.FULLSCREEN)
	pg.display.set_caption('Show Text')
	screen.fill(backgroundColor)
	pg.display.flip()

	StartMenu = startMenu(screen)
	MainMenu = mainMenu(screen)
	PCGame = None
	state = "STARTMENU"

	# test
	image = reglesImg[1]
	mySurface = pg.Surface((screenSize[0]/2, screenSize[1]))

	# frame loop
	while 1:
		match state:
			case "STARTMENU":
				StartMenu.draw()
				for event in pg.event.get():
					match event.type:
						case pg.QUIT: sys.exit()
						case pg.MOUSEBUTTONDOWN:
							if event.button == 1:
								PCGame = StartMenu.leftClick()
								if PCGame != None:
									state = "GAME"
									del StartMenu
						case pg.KEYDOWN:
							match event.key:
								case pg.K_ESCAPE:
									StartMenu.retour()
								case pg.K_RETURN:
									StartMenu.cheatOrNotCheat()
			case "MAINMENU":
				MainMenu.draw()
				for event in pg.event.get():
					match event.type:
						case pg.QUIT: sys.exit()
						case pg.MOUSEBUTTONDOWN:
							if event.button == 1:
								if MainMenu.leftClick():
									PCGame.saveGame(MainMenu.slot)
								if not MainMenu.isActive:
									state = "GAME"
									PCGame.firstDraw()
						case pg.KEYDOWN:
							match event.key:
								case pg.K_ESCAPE:
									MainMenu.retour()
				if MainMenu.redrawGame:
					PCGame.firstDraw()
					MainMenu.redrawGame = False
			case "GAME":
				PCGame.draw()
				if PCGame.over:
					PCGame.computeScores()
					state = "END"
					break
				for event in pg.event.get():
					match event.type:
						case pg.QUIT: sys.exit()
						case pg.MOUSEBUTTONDOWN:
							if event.button == 1:
								PCGame.leftClick(pg.mouse.get_pos())
							elif event.button == 3:
								PCGame.rightClick()
						case pg.KEYDOWN:
							match event.key:
								case pg.K_ESCAPE:
									state = "MAINMENU"
									MainMenu.isActive = True
			case "END":
				pass
			case "TEST":
				# screen.fill(backgroundColor)
				mySurface.fill(red)
				screen.blit(image, (0,0))
				screen.blit(mySurface, (screenSize[0]/2, screenSize[1]))
				for event in pg.event.get():
					match event.type:
						case pg.KEYDOWN:
							match event.key:
								case pg.K_RETURN:
									sys.exit()
		pg.display.flip()

if __name__ == '__main__':
	main()