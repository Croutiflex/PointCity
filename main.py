import numpy as np
import pygame as pg
pg.init()
import sys
import random
import time
from pointcity import *
from startMenu import *
from mainMenu import *
from params import *
from endScreen import *

def main():

	# setup
	screen = pg.display.set_mode(screenSize, pg.SCALED | pg.FULLSCREEN)
	pg.display.set_caption('Show Text')
	screen.fill(backgroundColor)
	pg.display.flip()
	pg.mouse.set_visible(False)

	StartMenu = startMenu(screen)
	MainMenu = mainMenu(screen)
	PCGame = None
	EndScreen = None
	state = "STARTMENU"
	lastFrame = time.time()

	# test
	# EndScreen = endScreen(screen, [(i, i%2*10, i) for i in range(4)])
	# EndScreen = endScreen(screen, [(11, 18, 7)] + [(-1, i*9, 4) for i in range(3)])
	# state = "END"

	# frame loop
	while 1:
		T = time.time()
		if T - lastFrame < minFrameTime:
			continue
		lastFrame = T
		mousePos = pg.mouse.get_pos()
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
				PCGame.draw()
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
									if MainMenu.retour():
										state = "GAME"
										MainMenu.isActive = False
										PCGame.firstDraw()
				if MainMenu.redrawGame:
					PCGame.firstDraw()
					MainMenu.redrawGame = False
			case "GAME":
				PCGame.draw()
				if PCGame.over:
					EndScreen = PCGame.computeScores()
					state = "END"
				for event in pg.event.get():
					match event.type:
						case pg.QUIT: sys.exit()
						case pg.MOUSEBUTTONDOWN:
							if event.button == 1:
								PCGame.leftClick(mousePos)
							elif event.button == 3:
								PCGame.rightClick()
							PCGame.draw()
						case pg.KEYDOWN:
							match event.key:
								case pg.K_ESCAPE:
									state = "MAINMENU"
									MainMenu.isActive = True
			case "END":
				EndScreen.draw()
				for event in pg.event.get():
					if event.type == pg.MOUSEBUTTONDOWN or event.type ==pg.KEYDOWN:
						sys.exit()
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

		screen.blit(cursorImg, mousePos)
		pg.display.flip()

if __name__ == '__main__':
	main()