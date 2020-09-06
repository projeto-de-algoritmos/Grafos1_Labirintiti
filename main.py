import pygame


class Maze:
    def __init__(self, resolution):
        self.resolution = resolution
        self.display = pygame.display.set_mode(self.resolution)

    def principal(self):
        while True:
            continue


def main():
    pygame.init()

    resolution = (800, 600)
    pygame.display.set_caption("aMAZE")

    newMaze = Maze(resolution)
    newMaze.principal()


if __name__ == '__main__':
    main()
    pygame.quit()
    quit()
