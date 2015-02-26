import sys

class Knapsack01(object):
    
    capacity = 0
    numberOfItems = 0
    dataSet = []
    valuesSet = []
    takeSet = []

    def __init__(self, capacity, numberOfItems, dataset):
        self.update(capacity, numberOfItems, dataset)

    def createMatrixes(self):
        self.valuesSet = []
        self.takeSet = []
        
        tmp = []
        
        for _ in range(self.numberOfItems + 1):
            rowVSet = []
            rowTSet = []
            for _ in range(self.capacity + 1):
                rowVSet.append(0)
                rowTSet.append(0)
            
            self.valuesSet.append(rowVSet)
            tmp.append(rowTSet)
        
        self.takeSet.append(tmp)

    def update(self, capacity, numberOfItems, dataset):
        self.capacity = capacity
        self.numberOfItems = numberOfItems
        self.dataSet = dataset
        
        self.createMatrixes()
    
    def solve(self):
        #
        # fill the matrixes
        #
        for i in range(self.numberOfItems + 1):
            
            item = self.dataSet[i - 1]
            
            for w in range(self.capacity + 1):
                
                if i == 0 or w == 0:
                    self.valuesSet[i][w] = 0
                    
                    for x in range(len(self.takeSet)):
                        self.takeSet[x][i][w] = 0
                
                if i != 0 and w != 0:
                    value = item[0]
                    weight = item[1]
                    
                    if weight > w:
                        self.valuesSet[i][w] = self.valuesSet[i - 1][w]
                        
                        for x in range(len(self.takeSet)):
                            self.takeSet[x][i][w] = 0
                    else:
                        cellValue = value + self.valuesSet[i - 1][w - weight]
                        aboveCellValue = self.valuesSet[i - 1][w]
                        
                        maxBetween = max(cellValue, aboveCellValue)
                        
                        self.valuesSet[i][w] = maxBetween
                        
                        if cellValue > aboveCellValue:
                            for x in range(len(self.takeSet)):
                                self.takeSet[x][i][w] = 1
                        
                        elif aboveCellValue > cellValue:
                            for x in range(len(self.takeSet)):
                                self.takeSet[x][i][w] = 0
                        else: #That case. Really, don't be that case dude
                            tmp = list(self.takeSet)
                            
                            #Duplicate to mantain states
                            for mtx in tmp:
                                t = []
                                
                                for row in mtx:
                                    t.append(list(row))
                                
                                self.takeSet.append(t)
        
                            
                            #set 0's for the fist half of the list
                            #set 1's for the rest of the list
                            y = len(self.takeSet)
                            hy = int(y / 2)
                            
                            for x in range(hy):
                                self.takeSet[x][i][w] = 1
                                
                            for x in range(hy):
                                self.takeSet[x + hy][i][w] = 0

        #
        # find the items
        #
        solutionList = []
        
        for takeSet in self.takeSet:
            i = self.numberOfItems
            w = self.capacity
                        
            tmpSolution = []
            
            while i > 0:
                if takeSet[i][w] == 1: #I want this object
                    tmpSolution.append(self.dataSet[i - 1])
                    w -= self.dataSet[i - 1][1]
                
                i -= 1
            
            solutionList.append(tmpSolution)
        
        maxWeight = 0
        maxValue = 0
        
        solutionList = self.unique(solutionList)
        
        for item in solutionList[0]:
            maxWeight += item[1]
            maxValue += item[0]
        
        #print all the take matrixes
        
        return [maxValue, maxWeight, solutionList]
    
    def unique(self, myInput):
        output = []
        
        for x in myInput:
            if x not in output:
                output.append(x)
        
        return output

class Story:
    publicationTime = 0
    score = 0
    height = 0
    myInternalId = 0
    internal_id = 1
    
    def __init__(self, pt, s, h):
        self.publicationTime = pt
        self.score = s
        self.height = h
        self.myInternalId = Story.internal_id
        
        #Keep controlling the story id
        Story.internal_id += 1

class Stories:
    
    stories = []
    globalTime = 0
    windowTime = 0
    windowHeight = 0
    knapsackSolver = None
    
    def __init__(self, wt, wh):
        self.globalTime = int(0)
        self.windowTime = int(wt) #Window time is the max time the story will remain in the list
        self.windowHeight = int(wh)
        self.knapsackSolver = Knapsack01(0, 0, [])
        
    def addStory(self, s):
        
        #force to be a Story
        if not isinstance(s, Story):
            raise TypeError
        
        self.stories.append(s)
        
        #update the global time
        if s.publicationTime > self.globalTime:
            self.globalTime = s.publicationTime
        
        #update the stories
        self.updateStories()
    
    def reload(self, newTime):
        self.globalTime = int(newTime)
        self.updateStories()
        tmpInput = [
                    (story.score, story.height, story) for story in self.stories
                    ]
        self.knapsackSolver.update(self.windowHeight, len(tmpInput), tmpInput)
        
        solutions = self.knapsackSolver.solve()
        
        sortedSolutions = sorted(solutions[2], key=lambda item: (len(item), item))
        
        stories = sortedSolutions[0]
        iIds = [str(story[2].myInternalId) for story in stories]
        iIds.reverse()
        strIds = ' '.join(iIds)
        print("%s %s %s" % (solutions[0], len(stories), strIds))
        
    def updateStories(self):
        #delete every story that not fit anymore
        cutTime = self.globalTime - self.windowTime
        self.stories = [story for story in self.stories if story.publicationTime >= cutTime]

#update the stdin so I can read the txt file
sys.stdin = open("input.txt", "r")

line = sys.stdin.readline()
line = line.strip().split()

numberOfEvents  = int(line[0])
timeWindow      = int(line[1])
windowHeight    = int(line[2])

stories = Stories(timeWindow, windowHeight)

#read the rest of the file and parse it
for _ in range(numberOfEvents):
    line = sys.stdin.readline().strip().split()
    
    if line[0] == "S":
        stories.addStory(Story(int(line[1]), int(line[2]), int(line[3])))
    
    if line[0] == "R":
        stories.reload(int(line[1]))