class Edge:
    def __init__(self,toNodeId,player):
        self.to = toNodeId
        self.player = player
class Box:
    def __init__(self,idx,player):
        self.id = idx
        self.setPlayerId(player)
        
    def setPlayerId(self,player1Turn):
        if player1Turn == True:
            self.player = 1
        else:
            self.player = 2

def State():
    def __init__(self,currentStateStringRepresentationOfGraph,parentStringRepresentationOfGraph,step,value):
        self.current = currentStateStringRepresentationOfGraph
        self.parent = parentStringRepresentationOfGraph
        self.step = step
        self.value = value

class Graph:
    def __init__(self,graph):
        self.graph = graph
    def print3(self):
        aux = 0
        for i in self.graph:
            for edges in self.graph[i]:
                print(i,"to",edges.to,"player",edges.player)
                aux+=1
        print("aux",aux)

if __name__ == "__main__":
    x = Box(1,True)
    print(x.player)