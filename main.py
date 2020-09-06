import pygame


colors = (
    (255, 255, 255), (0, 0, 255), (255, 40, 0), (0, 255, 0)
)


class Maze:
    def __init__(self, resolution):
        self.resolution = resolution
        self.display = pygame.display.set_mode(self.resolution)
        self.graphVertices = []  # Grid

    def drawLine(self, color, initalPosition, endPosition):
        pygame.draw.line(self.display, color, initalPosition, endPosition)

    def mazeGenerator(self, pathWidth):
        print("Iniciando geração do labirinto...")
        print("Construindo grafo...")

        # Pontos iniciais
        x, y, w = pathWidth, pathWidth, pathWidth
        limit_x = int(self.resolution[0]/pathWidth)
        limit_y = int(self.resolution[1]/pathWidth)

        for j in range(1, limit_y-1):
            x = pathWidth

            for i in range(1, limit_x-1):
                # Linhas da Esquerda
                self.drawLine(colors[0], (x, y), (x, y + w))

                # Linhas do Topo
                self.drawLine(colors[0], (x, y), (x + w, y))

                # Linhas de Baixo
                self.drawLine(colors[0], (x, y + w), (x + w, y + w))

                # Linhas da Direita
                self.drawLine(colors[0], (x + w, y), (x + w, y + w))

                pygame.display.update()

                self.graphVertices.append((x, y))

                x = x + pathWidth
            y = y + pathWidth

        pygame.display.update()

    def principal(self):
        pathWidth = 20
        self.mazeGenerator(pathWidth)

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
