import numpy as np
import pygame as pg
import sys
import random
from pointcity import *
from startMenu import *
from params import *

def main():

	# setup
	pg.init()
	screen = pg.display.set_mode(screenSize, pg.SCALED | pg.FULLSCREEN)
	pg.display.set_caption('Show Text')
	screen.fill(backgroundColor)
	pg.display.flip()

	StartMenu = startMenu(screen)
	PCGame = None
	state = "STARTMENU"

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
								PCGame = StartMenu.leftClick(pg.mouse.get_pos())
								if PCGame != None:
									state = "GAME"
									del StartMenu
						case pg.KEYDOWN:
							match event.key:
								case pg.K_ESCAPE:
									StartMenu.retour()
								case pg.K_BACKSPACE:
									StartMenu.cheatOrNotCheat()
								case pg.K_RETURN:
									sys.exit()
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
						case pg.KEYDOWN:
							match event.key:
								case pg.K_ESCAPE:
									PCGame.pressEscape()
								case pg.K_RETURN:
									sys.exit()
								case pg.K_TAB:
									PCGame.pressTab()
			case "END":
				pass
		pg.display.flip()

if __name__ == '__main__':
	main()