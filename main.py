import pygame
import random
from functions import *
from classes import *
import copy


pygame.init()
# screen = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE, 32)
screen = pygame.display.set_mode((1920, 1080), pygame.SHOWN, 32)
pygame.display.set_caption("Dot and crosses")
font = pygame.font.SysFont("monospace", 26)
font2 = pygame.font.SysFont("monospace", 46)
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

# Fill background
background = pygame.Surface(screen.get_size())
background.fill((50,50,50))

# Display some text
text = font.render("Dot and crosses",True, (0,0,0), (255, 255, 255))

graph = {
    1:[Edge(2,1),Edge(4,1)],
    2:[Edge(1,1),Edge(3,1)],
    3:[Edge(2,1)],
    4:[Edge(1,1)],
    5:[],
    6:[Edge(9,2)],
    7:[Edge(8,1)],
    8:[Edge(7,1),Edge(9,1)],
    9:[Edge(8,1),Edge(6,2)]
}

# select which is first
player1Turn = True

# # Event loop
on = True

#determines if there cant be more moves
endOfMoves = False

#it stores boxes 1,2,3,4 according to the grid, from top to down, left right
boxesId = []

steps = 7####

arrayOfGraphs = [[(copy.deepcopy(graph))]]

def printF():
    global boxesId
    print("----")

    for i in boxesId:
        print(i.id,i.player)
    print("----")

states = [Graph(copy.deepcopy(graph))]

#for determining where to put a circle
arrayOfCircles = []

#to reset
def setup():
    global graph,boxesId,endOfMoves,player1Turn,states,steps,arrayOfGraphs,arrayOfCircles
    boxesId = []
    endOfMoves = False
    graph = {
        1:[Edge(2,1),Edge(4,1)],
        2:[Edge(1,1),Edge(3,1)],
        3:[Edge(2,1)],
        4:[Edge(1,1)],
        5:[],
        6:[Edge(9,2)],
        7:[Edge(8,1)],
        8:[Edge(7,1),Edge(9,1)],
        9:[Edge(8,1),Edge(6,2)]
    }
    player1Turn = True
    states = [Graph(copy.deepcopy(graph))]
    steps = 7
    arrayOfGraphs = [[(copy.deepcopy(graph))]]
    arrayOfCircles = []



text3 = font.render("Presione e para mover, r para reiniciar",True, (0,0,0), (255, 255, 255))




while on:
    screen.blit(background,(0,0))
    screen.blit(text3,(1200,900))
    if endOfMoves:
        text2 = font.render("Fin del juego",True, (0,0,0), (255, 255, 255))
        screen.blit(text2, (70,40))
        score = getScore(boxesId)
        text4 = font2.render("Puntuación {}".format(score),True, (0,0,0), (255, 255, 255))
        screen.blit(text4, (570,800))
        # states = states[:-1]
        # on = False
        # continue
        #exit

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            on = False
            break
        if e.type == pygame.KEYDOWN:

            if (e.unicode) == "q":
                on = False
                break

            if (e.unicode) == "e":
                

                if player1Turn:
                    
                    if checkIfMakeMove(graph) != False:
                        # print2(graph)


                        add(player1Turn,arrayOfGraphs,graph,steps)

                        

                        makeMove(graph,1)

                        arrayOfCircles.append(searchState(graph,arrayOfGraphs))
                        # saveToFile(graph)
                        boxes2 = determineIfBoxCanBeMade(graph,boxesId)
                        steps -= 1
                        if len(boxes2) != 0:
                            for i in boxes2:
                                boxesId.append(Box(i,player1Turn))
                    else:
                        endOfMoves = True

                elif player1Turn == False:

                    if checkIfMakeMove(graph) != False:


                        add(player1Turn,arrayOfGraphs,graph,steps)


                        # print2(graph)
                        # saveToFile(graph)

                        makeMove(graph,2)

                        arrayOfCircles.append(searchState(graph,arrayOfGraphs))


                        boxes2 = determineIfBoxCanBeMade(graph,boxesId)
                        steps -= 1

                        if len(boxes2) != 0:
                            for i in boxes2:
                                boxesId.append(Box(i,player1Turn))
                                
                    else:
                        endOfMoves = True

                if endOfMoves == False:
                    x = copy.deepcopy(graph)
                    states.append(Graph(x))


                player1Turn = not player1Turn

            if (e.unicode) == "r":
                setup()
                
    screen.blit(text, (70,10))
    drawBoard(graph,screen,offSetX=1600)
    drawBoxes2(screen,boxesId,font2,1600)
    drawLines(arrayOfCircles,screen)
    drawStates(arrayOfGraphs,screen)
    drawCircles(arrayOfCircles,screen)

    pygame.display.update()

pygame.quit()

