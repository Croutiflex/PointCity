import pygame as pg
pg.init()
from pointcity import *
from startMenu import *
from mainMenu import *
from params import *
from endScreen import *

def main():

	# setup
	screen = pg.display.set_mode(screenSize, pg.SCALED | pg.FULLSCREEN)
	clock = pg.time.Clock()
	pg.display.set_caption('Show Text')
	screen.fill(backgroundColor)
	pg.display.flip()
	pg.mouse.set_cursor(pg.cursors.Cursor(cursorHotspot, cursorImg))

	running = True
	displayFPS = True
	startMenu = StartMenu()
	MainMenu = mainMenu(screen)
	PCGame = None
	EndScreen = None
	state = "STARTMENU"

	# test
	# EndScreen = endScreen(screen, [(i, i%2*10, i) for i in range(4)])
	# EndScreen = endScreen(screen, [(11, 18, 7)] + [(-1, i*9, 4) for i in range(3)])
	# state = "SCORES"

	# frame loop
	while running:
		mousePos = pg.mouse.get_pos()
		# keys = pg.key.get_pressed()
		events = {}
		for event in pg.event.get():
			match event.type:
				case pg.QUIT: running = False
				case pg.MOUSEBUTTONDOWN:
					match event.button:
						case 1:
							events["leftClick"] = True
						case 3:
							events["rightClick"] = True
				case pg.KEYDOWN:
					match event.key:
						case pg.K_ESCAPE:
							events["escape"] = True
						case pg.K_RETURN:
							events["return"] = True
						case pg.K_TAB:
							events["tab"] = True
		if "tab" in events:
			displayFPS = not displayFPS

		match state:
			case "STARTMENU":
				startMenu.update()
				startMenu.draw(screen)
				if "leftClick" in events:
					match startMenu.leftClick():
						case "close":
							running = False
						case "newgame":
							av = startMenu.avSelect.picked
							if startMenu.nPlayers == 1:
								av.append(-1)
							PCGame = pointCityGame(screen, False, nPlayers=startMenu.nPlayers, avatars=av, cheatMode=startMenu.cheatMode)
							state = "GAME"
							del startMenu
						case "loadgame":
							print("chargement partie ", startMenu.slot)
							PCgame = pointCityGame(screen, True, saveSlot=startMenu.slot)
							state = "GAME"
							del startMenu
				if "escape" in events:
					startMenu.retour()
				if "return" in events:
					startMenu.cheatOrNotCheat()

			case "MAINMENU":
				PCGame.drawBase()
				MainMenu.draw()
				if "leftClick" in events:
					if MainMenu.leftClick():
						PCGame.saveGame(MainMenu.slot)
					if not MainMenu.isActive:
						state = "GAME"
						PCGame.drawBase()
				if "escape" in events:
					if MainMenu.retour():
						state = "GAME"
						MainMenu.isActive = False
						PCGame.drawBase()
				if MainMenu.redrawGame:
					PCGame.drawBase()
					MainMenu.redrawGame = False

			case "GAME":
				PCGame.draw()
				if PCGame.over:
					EndScreen = PCGame.computeScores()
					state = "SCORES"
				if "leftClick" in events:
					PCGame.leftClick(mousePos)
				if "rightClick" in events:
					PCGame.rightClick()
				if "escape" in events:
					state = "MAINMENU"
					MainMenu.isActive = True

			case "SCORES":
				EndScreen.draw()
				if len(events) > 0:
					running = False
			# case "TEST":
			# 	# screen.fill(backgroundColor)
			# 	mySurface.fill(red)
			# 	screen.blit(image, (0,0))
			# 	screen.blit(mySurface, (screenSize[0]/2, screenSize[1]))
			# 	for event in pg.event.get():
			# 		match event.type:
			# 			case pg.KEYDOWN:
			# 				match event.key:
			# 					case pg.K_RETURN:
			# 						sys.exit()

		if displayFPS:
			FPSText = font.render(str(int(clock.get_fps())), True, white, "black")
			rect = FPSText.get_rect(centerx = midx, bottom = screenSize[1] - space1)
			screen.blit(FPSText, rect)
		pg.display.flip()
		clock.tick(maxFramerate)

	# end loop
	pg.quit()

if __name__ == '__main__':
	main()