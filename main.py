import numpy as np
import pygame as pg
import sys
import random
from pointcity import *
from params import *

def main():
	# bordel

	# setup
	pg.init()
	screen = pg.display.set_mode(screenSize)
	screen.fill(backgroundColor)
	pg.display.flip()

	PCGame = pointCityGame(1)

	# first draw

	# frame loop
	while 1:
		for event in pg.event.get():
			match event.type:
				case pg.QUIT: sys.exit()
				case pg.MOUSEBUTTONDOWN:
					if event.button == 1:
						PCGame.leftClick(pg.mouse.get_pos())
						# 			sys.exit()
						# 		elif ES.clickRestart():
						# 			# reset game
						# 			screenMode = sMode.SELECTION
						# 			SS.draw(screen)
				case pg.KEYDOWN:
					if event.key == pg.K_ESCAPE:
						PCGame.pressEscape()
		screen.fill(backgroundColor)
		PCGame.draw(screen)
		pg.display.flip()

if __name__ == '__main__':
	main()