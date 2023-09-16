import random
from classes import *
import pygame
import copy

#return if that node can be selected, to put an edge
def chooseNode(graph):
    node = random.randint(1,9)
    if node == 1 and len(graph[node]) == 2:
        return False,node
    elif node == 2 and len(graph[node]) == 3:
        return False,node
    elif node == 3 and len(graph[node]) == 2:
        return False,node
    elif node == 4 and len(graph[node]) == 3:
        return False,node
    elif node == 5 and len(graph[node]) == 4:
        return False,node
    elif node == 6 and len(graph[node]) == 3:
        return False,node
    elif node == 7 and len(graph[node]) == 2:
        return False,node
    elif node == 8 and len(graph[node]) == 3:
        return False,node
    elif node == 9 and len(graph[node]) == 2:
        return False,node
    else:
        # print("this node was selected because it has available spaces",node)
        # print2(graph)
        return True,node

#it returns a set containing the nodeId that it its connected to
def getNodesConnected(graph,node):
    #its a set
    _set = set()
    for i in graph[node]:
        _set.add(i.to)
    return _set

#it returns the nodeId number to the node that it can be connected to
def chooseConection(graph,node):
    ###warning
    set1 = getNodesConnected(graph,node)
    # print("node",node,"set",set1)
    #they are sets
    options = {
        1:{2,4},
        2:{1,3,5},
        3:{2,6},
        4:{1,5,7},
        5:{2,4,6,8},
        6:{3,5,9},
        7:{4,8},
        8:{5,7,9},
        9:{6,8}
    }
    toChoose = options[node].difference(set1)
    toChoose = list(toChoose)
    # print("options to select",toChoose)
    if len(toChoose) == 0:
        return False
    else:
        x = random.choice(toChoose)
        # print(x,"was selected")
        return x

#it makes the connection to the graph,it uses the functions above
def makeConnection(graph,node,player):
    nodeIdTo = chooseConection(graph,node)
    # print(nodeIdTo,"MAKE CONNECTION()")
    while nodeIdTo == False:
        # return False
        nodeIdTo = chooseConection(graph,node)
   
    graph[node].append(Edge(nodeIdTo,player))  
    graph[nodeIdTo].append(Edge(node,player)) 
    # print("we make a connection so the graph is now")
    # print2(graph)
    # return graph 

#verify if all the nodes have edges
def verifyIfAvailable(graph):
    if len(graph[1]) == 2 and len(graph[2]) == 3 and len(graph[3]) == 2 and len(graph[4]) == 3 and len(graph[5]) == 4 and len(graph[6]) == 3 and len(graph[7]) == 2 and len(graph[8]) == 3 and len(graph[9]) == 2:
        return False
    return True

#check if move can be made
def checkIfMakeMove(graph):
    if verifyIfAvailable(graph) == False:
        # print("The board is full")
        return False
    else:
        return True

#it makes a random move, from the available positions
def makeMove(graph,player):
    flag,nodeId = chooseNode(graph)
    if verifyIfAvailable(graph) == False:
        # print("The board is full")
        return False
    else:
        while flag == False:
            flag,nodeId = chooseNode(graph)

        makeConnection(graph,nodeId,player)

def drawBoard(graph,screen,offSetX=500,offSetY=100,factor=100,radius=10,circles=False):
    # pygame.draw.rect(screen,self.bgColor,self.rect)
    pos = {
        1:(0,0),
        2:(0,1),
        3:(0,2),
        4:(1,0),
        5:(1,1),
        6:(1,2),
        7:(2,0),
        8:(2,1),
        9:(2,2)
    }
    color = (200,200,200)
    width = 4

    if circles == True:
        pygame.draw.circle(screen,(50,50,50),(offSetX+30,offSetY+30),radius*10)
        pygame.draw.circle(screen,(180,180,180),(offSetX+30,offSetY+30),radius*10,3)

    for i in graph:
        pygame.draw.circle(screen,color,((pos[i][1]*factor)+offSetX,(pos[i][0]*factor)+offSetY),radius)
        for j in graph[i]:
            #it is drawing 2 times the lines
            if j.player == 1:
                pygame.draw.line(screen, (100,100,200),((pos[i][1]*factor)+offSetX,(pos[i][0]*factor)+offSetY), ((pos[j.to][1]*factor)+offSetX,(pos[j.to][0]*factor)+offSetY), width)
            else:
                pygame.draw.line(screen, (190,20,20),((pos[i][1]*factor)+offSetX,(pos[i][0]*factor)+offSetY), ((pos[j.to][1]*factor)+offSetX,(pos[j.to][0]*factor)+offSetY), width)

#alreadyBoxID is an array
def determineIfIdIsOnAlreadyBoxes(id,alreadyBoxID):
    for i in alreadyBoxID:
        if i.id == id:
            return True
    return False

#the alreadyBoxID is to determine if a box has already been filled
def determineIfBoxCanBeMade(graph,alreadyBoxID):
    connected = {
        1:getNodesConnected(graph,1),
        2:getNodesConnected(graph,2),
        3:getNodesConnected(graph,3),
        4:getNodesConnected(graph,4),
        5:getNodesConnected(graph,5),
        6:getNodesConnected(graph,6),
        7:getNodesConnected(graph,7),
        8:getNodesConnected(graph,8),
        9:getNodesConnected(graph,9)
    }
    #first box
    op = []
    if 2 in connected[1] and 5 in connected[2] and 4 in connected[1] and 5 in connected[4] and not determineIfIdIsOnAlreadyBoxes(1,alreadyBoxID):
        op.append(1)
    if 2 in connected[3] and 5 in connected[2] and 5 in connected[6] and 3 in connected[6] and not determineIfIdIsOnAlreadyBoxes(2,alreadyBoxID):
        op.append(2)
    if 4 in connected[5] and 5 in connected[8] and 4 in connected[7] and 7 in connected[8] and not determineIfIdIsOnAlreadyBoxes(3,alreadyBoxID):
        op.append(3)
    if 5 in connected[6] and 5 in connected[8] and 8 in connected[9] and 6 in connected[9] and not determineIfIdIsOnAlreadyBoxes(4,alreadyBoxID):
        op.append(4)
    return op

#uses the last element added to the boxesId and draw it according to the player
#improve
def drawBoxes1(screen,boxesId):
    color1 = (100,100,200)
    color2 = (200,100,100)
    x,y = (500,100)
    if len(boxesId)==0:
        return 
    for i in boxesId:
        if i.id == 1:
            if i.player == 1:
                pygame.draw.rect(screen,color1,(0+x,0+y,100,100))
            else:
                pygame.draw.rect(screen,color2,(0+x,0+y,100,100))
        elif i.id == 2:
            if i.player == 1:
                pygame.draw.rect(screen,color1,(100+0+x,0+y,100,100))
            else:
                pygame.draw.rect(screen,color2,(100+x,0+y,100,100))
        elif i.id == 3:
            if i.player == 1:
                pygame.draw.rect(screen,color1,(0+x,100+y,100,100))
            else:
                pygame.draw.rect(screen,color2,(0+x,100+y,100,100))
        elif i.id == 4:
            if i.player == 1:
                pygame.draw.rect(screen,color1,(100+x,100+y,100,100))
            else:
                pygame.draw.rect(screen,color2,(100+x,100+y,100,100))
def drawBoxes2(screen,boxesId,font,offSetX=500,offSetY=100):
    color1 = (100,100,200)
    color2 = (200,100,100)
    x,y,n = (offSetX,offSetY,29)

    if len(boxesId)==0:
        return 
    for i in boxesId:
        if i.id == 1:
            if i.player == 1:
                # pygame.draw.rect(screen,color1,(0+x,0+y,100,100))
                screen.blit(font.render("A",True, color1), (0+x+n,0+y+n))

            else:
                # pygame.draw.rect(screen,color2,(0+x,0+y,100,100))
                screen.blit(font.render("B",True, color2), (0+x+n,0+y+n))

        elif i.id == 2:
            if i.player == 1:
                # pygame.draw.rect(screen,color1,(100+0+x,0+y,100,100))
                screen.blit(font.render("A",True, color1), (100+x+n,0+y+n))

            else:
                # pygame.draw.rect(screen,color2,(100+x,0+y,100,100))
                screen.blit(font.render("B",True, color2), (100+x+n,0+y+n))

        elif i.id == 3:
            if i.player == 1:
                screen.blit(font.render("A",True, color1), (0+x+n,100+y+n))

                # pygame.draw.rect(screen,color1,(0+x,100+y,100,100))
            else:
                # pygame.draw.rect(screen,color2,(0+x,100+y,100,100))
                screen.blit(font.render("B",True, color2), (0+x+n,100+y+n))

        elif i.id == 4:
            if i.player == 1:
                # pygame.draw.rect(screen,color1,(100+x,100+y,100,100))
                screen.blit(font.render("A",True, color1), (100+x+n,100+y+n))

            else:
                # pygame.draw.rect(screen,color2,(100+x,100+y,100,100))
                screen.blit(font.render("B",True, color2), (100+x+n,100+y+n))


def print2(graph):
    connected = {
        1:getNodesConnected(graph,1),
        2:getNodesConnected(graph,2),
        3:getNodesConnected(graph,3),
        4:getNodesConnected(graph,4),
        5:getNodesConnected(graph,5),
        6:getNodesConnected(graph,6),
        7:getNodesConnected(graph,7),
        8:getNodesConnected(graph,8),
        9:getNodesConnected(graph,9)
    }
    print("graph")
    for i in connected:
        print(i,connected[i])
    print("")

#we dont have the player who made that connection
def getCurrentGraph(graph):
    connected = {
        1:getNodesConnected(graph,1),
        2:getNodesConnected(graph,2),
        3:getNodesConnected(graph,3),
        4:getNodesConnected(graph,4),
        5:getNodesConnected(graph,5),
        6:getNodesConnected(graph,6),
        7:getNodesConnected(graph,7),
        8:getNodesConnected(graph,8),
        9:getNodesConnected(graph,9)
    }
    return connected

def getStringRepresentationOfGraph(graph):
    return str(getCurrentGraph(graph))

def getScore(boxes):
    score = 0
    for i in boxes:
        if i.player == 1:
            score += 1
        else:
            score -= 1
    return score

def getToAndPlayerGivenEdge(edge):
    return [edge.to,edge.player]

#the graph has to be of type Graph
def getAllEdgesAsArrays(index,graph):
    arr = []
    for edge in graph[index]:
        arr.append(getToAndPlayerGivenEdge(edge))
    return arr

#we use this to compare if that graph has been already made, to generate
#the different games given a graph
def getArraysRepresentationOfGraphIncludingThePlayer(graph):
    graph2 = {
        1:getAllEdgesAsArrays(1,graph),
        2:getAllEdgesAsArrays(2,graph),
        3:getAllEdgesAsArrays(3,graph),
        4:getAllEdgesAsArrays(4,graph),
        5:getAllEdgesAsArrays(5,graph),
        6:getAllEdgesAsArrays(6,graph),
        7:getAllEdgesAsArrays(7,graph),
        8:getAllEdgesAsArrays(8,graph),
        9:getAllEdgesAsArrays(9,graph),
    }
    return graph2

#it makes the connection to the graph,it uses the functions above
#it doesnt modify the current graph, it returns another graph
def makeConnection2(graph,node,player):
    nodeIdTo = chooseConection(graph,node)
    # print(nodeIdTo,"MAKE CONNECTION()")
    while nodeIdTo == False:
        # return False
        nodeIdTo = chooseConection(graph,node)

    x = copy.deepcopy(graph)
    x[node].append(Edge(nodeIdTo,player))
    x[nodeIdTo].append(Edge(node,player))
    # print("we make a connection so the graph is now")
    # print2(graph)
    return x

#it makes a random move, from the available positions
#return the new graph when making the move
#it makes a random move
def makeMove2(graph,player):
    flag,nodeId = chooseNode(graph)
    if verifyIfAvailable(graph) == False:
        # print("The board is full")
        return False
    else:
        while flag == False:
            flag,nodeId = chooseNode(graph)

        return makeConnection2(graph,nodeId,player)


#graph has to be of type Graph, but it was modified, it is not necesary anymore
#there is 
#the steps is measured to give the possible values
def returnAllPossible1LevelMovesGamesGivenGraph(graph,player,steps):
    #graph.grap
    arr = []
    arr_graphs = []
    # if checkIfMakeMove(graph) != False:
    # print(getArraysRepresentationOfGraphIncludingThePlayer(graph))
    # return
    while len(arr)<steps-1:
        # print("LLL steps",steps)
        moveGraph = makeMove2(graph,player)
        moveArrays = getArraysRepresentationOfGraphIncludingThePlayer(moveGraph)
        if str(moveArrays) not in arr:
            arr.append(str(moveArrays))
            arr_graphs.append(moveGraph)
            # print("TXX")
    # print("ARR",arr)
    return arr_graphs

def add(player1Turn,arrayOfGraphs,graph,steps):
    p = 1
    if player1Turn == True:
        p = 1
    else:
        p = 2
    arrayOfGraphs.append(returnAllPossible1LevelMovesGamesGivenGraph(copy.deepcopy(graph),p,steps))

def drawStates(arrayOfGraphs,screen):
    for i in range(len(arrayOfGraphs)):
        for j in range(len(arrayOfGraphs[i])):
            drawBoard(arrayOfGraphs[i][j],screen,(j+1)*130,(i+1)*130,30,5,circles=True)

                
def searchState(currentGraph,arrayOfGraphs):
    for i in range(len(arrayOfGraphs)):
        for j in range(len(arrayOfGraphs[i])):
            if str(getArraysRepresentationOfGraphIncludingThePlayer(arrayOfGraphs[i][j])) == str(getArraysRepresentationOfGraphIncludingThePlayer(currentGraph)):
                return [i,j]
    raise Exception

def drawCircles(arrayOfIndicesIJ,screen):
    for i in arrayOfIndicesIJ:
        pygame.draw.circle(screen,(200,200,0),(((i[1]+1)*130)+30,((i[0]+1)*130)+30),60,2)

def drawLines(arrayOfIndicesIJ,screen):
    color = (170,170,170)
    width = 3
    for i in range(len(arrayOfIndicesIJ)):
        if i == 0:
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(150,400), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(280,400), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(400,400), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(540,400), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(680,400), width)
            
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(160,160), width)
        elif i == 1:
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(120,550), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(280,550), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(440,550), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(580,550), width)
        elif i == 2:
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(130,650), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(280,650), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(400,650), width)
        elif i == 3:
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(180,800), width)
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(280,800), width)
        elif i == 4:
            pygame.draw.line(screen, color,(((arrayOfIndicesIJ[i][1]+1)*130)+30,((arrayOfIndicesIJ[i][0]+1)*130)+30),(160,950), width)






# def addLinesStates(arrayOfIndicesIJ,screen,arrayOfGraphs):
#     if len(arrayOfGraphs)>1:
#         arrayOfGraphs[-1]

#         arrayOfGraphs[]

if __name__ == "__main__":
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
    # print(getNodesConnected(graph,5))
    # print(chooseConection(graph,5))

    #print(getToAndPlayerGivenEdge(graph[1][1]))
    #print(getAllEdgesAsArrays(1,graph))
    # print(getArraysRepresentationOfGraphIncludingThePlayer(graph))
    # print(getArraysRepresentationOfGraphIncludingThePlayer(makeMove2(graph,1)))
    # print(str(getArraysRepresentationOfGraphIncludingThePlayer(graph))==str(getArraysRepresentationOfGraphIncludingThePlayer(makeMove2(graph,1))))

    # # print(returnAllPossible1LevelMovesGamesGivenGraph(Graph(graph),1,5))
    # # x = (returnAllPossible1LevelMovesGamesGivenGraph(Graph(graph),1,5))
    # #for i in x:
    # a = [[1,2,3],45,67]
    # b = []  
    # b.append(str(a))
    # print(str(a) not in b)
