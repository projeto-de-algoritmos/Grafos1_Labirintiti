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
    (0, 0, 139),  # Azul Escuro
    (192, 192, 192),  # Prata
    (128, 128, 128),  # Cinza
    (255, 215, 0),  # Ouro
    (240, 230, 140),  # Amarelo Khaki

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

        self.qStart_X = 0
        self.qStart_Y = 0
        self.qText_W = 0
        self.qText_H = 0

        self.gStart_X = 0
        self.gStart_Y = 0
        self.gText_W = 0
        self.gText_H = 0

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
                    endNStepsArea_x + 20 + int(nBacktrackingTitleArea[2]/2),
                    10 + int(nBacktrackingTitleArea[3]/2)
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

        # increaseSpeedButton = textFont.render('+SPEED', True, colors[0])
        # print(increaseSpeedButton.get_height())

        # mouse = pygame.mouse.get_pos()

        # increaseSpeedButtonStart = (
        #    self.resolution[0] - increaseSpeedButton.get_width() - 20
        # )
        # if not (
        #    increaseSpeedButtonStart <= mouse[0] <= self.resolution[0] - 20
        #    and 5 <= mouse[1] <= 15
        # ):
        #    pygame.draw.rect(
        #        self.display, colors[7],
        #        (increaseSpeedButtonStart, 10,
        #           increaseSpeedButton.get_width(), 20)
        #    )

        # self.display.blit(increaseSpeedButton, (360, 10))
        # pygame.display.update()

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
                        self.stepCount(textFont, endNumberStepsTitleArea_x)
                        self.exploredVertices.append(neighbor[1])
                        stack.append(neighbor[1])
                    else:
                        self.stepCount(textFont, endNumberStepsTitleArea_x, 1)
                        stack.pop()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            return -1

        print("Labirinto gerado com sucesso.")
        return 0

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
        self.display.blit(
            icon, (int(self.resolution[0]/2 - icon.get_width()/2), 40)
        )

        titleFont = pygame.font.Font('./assets/fonts/Roboto-Bold.ttf', 40)
        title = titleFont.render('aMaze', True, colors[0])
        titleArea = title.get_rect()
        titleArea.center = (
            int(self.resolution[0]/2),
            int(title.get_height()/2) + icon.get_height() + 40 + 20
        )
        self.display.blit(title, titleArea)

        buttonsTextFont = pygame.font.Font(
            './assets/fonts/Roboto-Bold.ttf', 20
        )
        quitButtonText = buttonsTextFont.render('SAIR', True, colors[0])
        quitButtonText_W = quitButtonText.get_width()
        self.qText_W = quitButtonText_W

        quitButtonText_H = quitButtonText.get_height()
        self.qText_H = quitButtonText_H

        mouse = pygame.mouse.get_pos()

        quitStart_X = (
            int(self.resolution[0]/2 - quitButtonText_W/2 - 10)
        )
        self.qStart_X = quitStart_X

        quitStart_Y = (
            self.resolution[1] - 20 - quitButtonText_H - 20
        )
        self.qStart_Y = quitStart_Y

        if (
            quitStart_X <= mouse[0] <= quitStart_X + quitButtonText_W + 20
            and quitStart_Y <= mouse[1] <= quitStart_Y + quitButtonText_H + 20
        ):
            pygame.draw.rect(
                self.display, colors[5],
                (
                    quitStart_X, quitStart_Y,
                    quitButtonText_W + 20, quitButtonText_H + 20
                )
            )
        else:
            pygame.draw.rect(
                self.display, colors[2],
                (
                    quitStart_X, quitStart_Y,
                    quitButtonText_W + 20, quitButtonText_H + 20
                )
            )

        self.display.blit(quitButtonText, (quitStart_X + 10, quitStart_Y + 10))

        generateMazeButtonText = buttonsTextFont.render(
            'GERAR LABIRINTO', True, colors[0]
        )
        gButtonText_W = generateMazeButtonText.get_width()
        self.gText_W = gButtonText_W

        gButtonText_H = generateMazeButtonText.get_height()
        self.gText_H = gButtonText_H

        gButtonStart_X = int(
            self.resolution[0]/2 - gButtonText_W/2 - 10
        )
        self.gStart_X = gButtonStart_X

        gButtonStart_Y = (
            40 + icon.get_height() + 20 + title.get_height() + 20
        )
        self.gStart_Y = gButtonStart_Y

        if (
            gButtonStart_X <= mouse[0] <= gButtonStart_X + gButtonText_W + 20
            and
            gButtonStart_Y <= mouse[1] <= gButtonStart_Y + gButtonText_H + 20
        ):
            pygame.draw.rect(
                self.display, colors[6],
                (
                    gButtonStart_X, gButtonStart_Y,
                    gButtonText_W + 20, gButtonText_H + 20
                )
            )
        else:
            pygame.draw.rect(
                self.display, colors[1],
                (
                    gButtonStart_X, gButtonStart_Y,
                    gButtonText_W + 20, gButtonText_H + 20
                )
            )

        self.display.blit(
            generateMazeButtonText, (gButtonStart_X + 10, gButtonStart_Y + 10)
        )

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

                    if showInitialPage:
                        qStart_X, qStart_Y = self.qStart_X, self.qStart_Y
                        qText_W, qText_H = self.qText_W, self.qText_H
                        if (
                            qStart_X <= mouse[0] <= qStart_X + qText_W + 20
                            and qStart_Y <= mouse[1] <= qStart_Y + qText_H + 20
                        ):
                            running = False

                        gStart_X, gStart_Y = self.gStart_X, self.gStart_Y
                        gText_W, gText_H = self.gText_W, self.gText_H
                        if (
                            gStart_X <= mouse[0] <= gStart_X + gText_W + 20
                            and gStart_Y <= mouse[1] <= gStart_Y + gText_H + 20
                        ):
                            ####
                            self.display.fill(colors[0])

                            pygame.display.update()

                            r = self.mazeGenerator(pathWidth)
                            if r:
                                running = False
                            else:
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
