import pygame
import time
import random


colors = (
    (255, 255, 255), (0, 0, 255), (255, 40, 0), (0, 255, 0)
)


class Maze:
    def __init__(self, resolution):
        self.resolution = resolution
        self.display = pygame.display.set_mode(self.resolution)
        self.graphVertices = []  # Grid
        self.exploredVertices = []
        self.solution = {}

    def drawLine(self, color, initalPosition, endPosition):
        pygame.draw.line(self.display, color, initalPosition, endPosition)

    def drawBacktrackingStart(self, vertice, pathWidth):
        print("Realizando o backtraking...")

        pygame.draw.rect(
            self.display, colors[2],
            (vertice[0]+1, vertice[1]+1, pathWidth-2, pathWidth-2), 0
        )
        pygame.display.update()

        time.sleep(0.1)

        pygame.draw.rect(
            self.display, colors[1],
            (vertice[0]+1, vertice[1]+1, pathWidth-2, pathWidth-2), 0
        )
        pygame.display.update()

    def getNeighbor(self, vertice, pathWidth):
        # Direções
        directions = {}
        directions['left'] = (vertice[0] - pathWidth, vertice[1])
        directions['top'] = (vertice[0], vertice[1] - pathWidth)
        directions['bottom'] = (vertice[0], vertice[1] + pathWidth)
        directions['right'] = (vertice[0] + pathWidth, vertice[1])

        options = []
        for direction, v in directions.items():
            if v in self.graphVertices and v not in self.exploredVertices:
                options.append((direction, v))

        neighbor = random.choice(options) if options else None

        if not neighbor:
            self.drawBacktrackingStart(vertice, pathWidth)

        print("Vizinho encontrado.")
        return neighbor

    def drawProgress(self, origin, destiny, pathWidth):
        if destiny[0] == "left":
            pygame.draw.rect(
                self.display, colors[1],
                (
                    origin[0]-pathWidth+1, origin[1]+1,
                    2*pathWidth-1, pathWidth-1
                ), 0
            )
            pygame.display.update()
        if destiny[0] == "right":
            pygame.draw.rect(
                self.display, colors[1],
                (origin[0]+1, origin[1]+1, 2*pathWidth-1, pathWidth-1), 0
            )
            pygame.display.update()
        if destiny[0] == "top":
            pygame.draw.rect(
                self.display, colors[1],
                (
                    origin[0]+1, origin[1]-pathWidth+1,
                    pathWidth-1, 2*pathWidth-1
                ), 0
            )
            pygame.display.update()
        if destiny[0] == "bottom":
            pygame.draw.rect(
                self.display, colors[1],
                (origin[0]+1, origin[1]+1, pathWidth-1, 2*pathWidth-1), 0
            )
            pygame.display.update()

        self.solution[(destiny[1])] = origin

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

        # Utiliza DFS para gerar labirinto
        print("Iniciando DFS...")

        stack = []
        for vertice in self.graphVertices:
            if vertice not in self.exploredVertices:
                stack.append(vertice)
                self.exploredVertices.append(vertice)
                while stack:
                    time.sleep(0.1)
                    u = stack[-1]
                    print("Procurando arestas...")
                    neighbor = self.getNeighbor(u, pathWidth)
                    if neighbor:
                        self.drawProgress(u, neighbor, pathWidth)
                        self.exploredVertices.append(neighbor[1])
                        stack.append(neighbor[1])
                    else:
                        stack.pop()

        print("Labirinto gerado com sucesso.")

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
