import pygame
from Game import Game

def main():
    game = Game()

    while game.running():
        game.update()
        game.render()

    pygame.quit()

if __name__=='__main__':
    main()

# TODO opisać grę
# TODO powoli skracać czas między spawnem enemy (początkowy jest dobry)
