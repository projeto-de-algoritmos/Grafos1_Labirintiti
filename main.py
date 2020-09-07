import pygame
import time
import random
import math


colors = (
    (255, 255, 255),  # Branco
    (0, 0, 255),  # Azul
    (255, 40, 0),  # Vermelho
    (0, 255, 0),  # Verde
    (0, 0, 0),  # Preto
    (139, 0, 0),  # Vermelho Escuro
    (0, 0, 139)  # Azul Escuro
)


class Maze:
    def __init__(self, resolution, display):
        self.resolution = resolution
        self.display = display
        self.graphVertices = []  # Grid
        self.exploredVertices = []
        self.numberSteps = 0
        self.numberBacktracking = 0
        self.endNBacktrackingTitleArea_x = 0
        self.solution = {}

    def drawLine(self, color, initalPosition, endPosition):
        pygame.draw.line(self.display, color, initalPosition, endPosition)

    def drawBacktrackingStart(self, vertice, pathWidth):
        print("Realizando o backtraking...")

        self.numberSteps = self.numberSteps + 1
        self.numberBacktracking = self.numberBacktracking + 1

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
        self.numberSteps = self.numberSteps + 1

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

    def stepCount(self, textFont, endNStepsTitleArea_x, backtraking=0):
        numberStepsText = textFont.render(
            str(self.numberSteps), True, colors[6]
        )
        numberStepsArea = numberStepsText.get_rect()
        pygame.draw.rect(
            self.display, colors[0],
            (endNStepsTitleArea_x, 10, numberStepsArea[2], numberStepsArea[3])
        )

        numberStepsArea.center = (
            endNStepsTitleArea_x+int(numberStepsArea[2]/2),
            10+int(numberStepsArea[3]/2)
        )
        self.display.blit(numberStepsText, numberStepsArea)

        digitIncrease = math.log10(self.numberSteps) % 1 == 0.0
        if backtraking or digitIncrease:
            if self.numberBacktracking == 1 or digitIncrease:
                numberBacktrackingTitle = textFont.render(
                    'Número de Backtracking: ', True, colors[5]
                )
                nBacktrackingTitleArea = numberBacktrackingTitle.get_rect()

                endNStepsArea_x = endNStepsTitleArea_x + numberStepsArea[2]
                pygame.draw.rect(
                    self.display, colors[0],
                    (
                        endNStepsArea_x, 10,
                        nBacktrackingTitleArea[2]+20, nBacktrackingTitleArea[3]
                    )
                )

                nBacktrackingTitleArea.center = (
                    endNStepsArea_x+20+int(nBacktrackingTitleArea[2]/2),
                    10+int(nBacktrackingTitleArea[3]/2)
                )

                self.endNBacktrackingTitleArea_x = (
                    endNStepsArea_x + 20 + nBacktrackingTitleArea[2]
                )

                self.display.blit(
                    numberBacktrackingTitle, nBacktrackingTitleArea
                )

            numberBacktrackingText = textFont.render(
                str(self.numberBacktracking), True, colors[5]
            )
            numBacktrackingArea = numberBacktrackingText.get_rect()
            pygame.draw.rect(
                self.display, colors[0],
                (
                    self.endNBacktrackingTitleArea_x, 10,
                    numBacktrackingArea[2], numBacktrackingArea[3]
                )
            )
            numBacktrackingArea.center = (
                self.endNBacktrackingTitleArea_x+int(numBacktrackingArea[2]/2),
                10+int(numBacktrackingArea[3]/2)
            )
            self.display.blit(numberBacktrackingText, numBacktrackingArea)

        pygame.display.update()

    def mazeGenerator(self, pathWidth):
        print("Iniciando geração do labirinto...")
        print("Construindo grafo...")

        # Pontos iniciais
        x, y, w = pathWidth, pathWidth+20, pathWidth

        limit_x = int(self.resolution[0]/pathWidth)
        limit_y = int((self.resolution[1]-20)/pathWidth)

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

                # pygame.display.update()

                self.graphVertices.append((x, y))

                x = x + pathWidth

            y = y + pathWidth

        pygame.display.update()

        # Utiliza DFS para gerar labirinto
        print("Iniciando DFS...")

        stack = []

        textFont = pygame.font.Font('./assets/fonts/Roboto-Bold.ttf', 17)
        numberStepsTitle = textFont.render(
            'Número de Passos: ', True, colors[6]
        )
        numberStepsTitleArea = numberStepsTitle.get_rect()
        numberStepsTitleArea.center = (
            20+int(numberStepsTitleArea[2]/2),
            10+int(numberStepsTitleArea[3]/2)
        )
        endNumberStepsTitleArea_x = numberStepsTitleArea[2] + 20
        self.display.blit(numberStepsTitle, numberStepsTitleArea)

        for vertice in self.graphVertices:
            if vertice not in self.exploredVertices:
                stack.append(vertice)
                self.exploredVertices.append(vertice)
                while stack:
                    time.sleep(0.1)
                    u = stack[-1]
                    # print("Procurando arestas...")
                    neighbor = self.getNeighbor(u, pathWidth)
                    if neighbor:
                        self.drawProgress(u, neighbor, pathWidth)
                        self.stepCount(textFont, endNumberStepsTitleArea_x)
                        self.exploredVertices.append(neighbor[1])
                        stack.append(neighbor[1])
                    else:
                        self.stepCount(textFont, endNumberStepsTitleArea_x, 1)
                        stack.pop()

        print("Labirinto gerado com sucesso.")

    def drawSolutionStep(self, vertice, pathWidth):
        pygame.draw.rect(
            self.display, colors[3],
            (
                vertice[0]+int(pathWidth/4), vertice[1]+int(pathWidth/4),
                int(pathWidth/2), int(pathWidth/2)
            ), 0
        )
        pygame.display.update()
        time.sleep(0.1)

    def mazeSolution(self, pathWidth):
        endVertice = (
            self.resolution[0]-2*pathWidth, self.resolution[1]-2*pathWidth
        )
        self.drawSolutionStep(endVertice, pathWidth)

        while endVertice != (pathWidth, pathWidth+20):
            endVertice = self.solution[endVertice]
            self.drawSolutionStep(endVertice, pathWidth)

    def initialPage(self):
        icon = pygame.image.load('./assets/media/icon.png')

        titleFont = pygame.font.Font('./assets/fonts/Roboto-Bold.ttf', 40)
        title = titleFont.render('aMaze', True, colors[0])
        titleArea = title.get_rect()
        titleArea.center = (
            int(self.resolution[0]/2), 280
        )

        buttonsTextFont = pygame.font.Font(
            './assets/fonts/Roboto-Bold.ttf', 20
        )
        quitButtonText = buttonsTextFont.render('SAIR', True, colors[0])

        mouse = pygame.mouse.get_pos()

        quitButtonStart = int(self.resolution[0]/2) - 40
        if (
            quitButtonStart <= mouse[0] <= quitButtonStart+80
            and 520 <= mouse[1] <= 520+40
        ):
            pygame.draw.rect(
                self.display, colors[5], (quitButtonStart, 520, 80, 40)
            )
        else:
            pygame.draw.rect(
                self.display, colors[2], (quitButtonStart, 520, 80, 40)
            )

        generateMazeButtonText = buttonsTextFont.render(
            'GERAR LABIRINTO', True, colors[0]
        )

        gMazeButtonStart = int(self.resolution[0]/2) - 150
        if (
            gMazeButtonStart <= mouse[0] <= gMazeButtonStart+300
            and 330 <= mouse[1] <= 330+40
        ):
            pygame.draw.rect(
                self.display, colors[6], (gMazeButtonStart, 330, 300, 40)
            )
        else:
            pygame.draw.rect(
                self.display, colors[1], (gMazeButtonStart, 330, 300, 40)
            )

        self.display.blit(icon, (int(self.resolution[0]/2) - 100, 40))
        self.display.blit(title, titleArea)
        self.display.blit(quitButtonText, (378, 520+10))
        self.display.blit(generateMazeButtonText, (323, 330+10))

    def principal(self):
        pathWidth = 20

        running = True
        showInitialPage = True
        while running:
            self.display.fill(colors[4])

            if showInitialPage:
                self.initialPage()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse = pygame.mouse.get_pos()
                    quitButtonStart = int(self.resolution[0]/2) - 40
                    if (
                        quitButtonStart <= mouse[0] <= quitButtonStart+80
                        and 520 <= mouse[1] <= 520+40
                    ):
                        running = False

                    gMazeButtonStart = int(self.resolution[0]/2) - 150
                    if (
                        gMazeButtonStart <= mouse[0] <= gMazeButtonStart+300
                        and 330 <= mouse[1] <= 330+40
                    ):
                        self.display.fill(colors[0])
                        pygame.display.update()
                        self.mazeGenerator(pathWidth)
                        self.mazeSolution(pathWidth)
                        time.sleep(0.5)

            pygame.display.update()


def main():
    pygame.init()

    resolution = (800, 620)

    pygame.display.set_caption("aMaze")

    icon = pygame.image.load('./assets/media/icon.png')
    pygame.display.set_icon(icon)

    display = pygame.display.set_mode(resolution)
    newMaze = Maze(resolution, display)
    newMaze.principal()


if __name__ == '__main__':
    main()
    pygame.quit()
    quit()
