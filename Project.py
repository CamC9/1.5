'''
This program will simulate a poker game, but with one player and a dealer,
where the objective of the game is to gain points by getting good combinations
of cards (hands)

It's possible we can expand the game to support playing against a computer
'''

import math, random, pygame, sys

pygame.init()
pygame.font.init()

win = pygame.display.set_mode((800,800))
win.fill((255,255,255))

class button():
    def __init__(self, color, x,y,width,height, text='', fontColor = (0,0,0), fontSize=60):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fontColor = fontColor
        self.fontSize = fontSize

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans',self.fontSize)
            text = font.render(self.text, 1, self.fontColor)
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

def redrawWindow(B1,B2, B3, B4):
    win.fill((255,255,255))
    B2.draw(win)
    B3.draw(win)
    B4.draw(win)
    B1.draw(win,(0,0,0))
    

def dealPair(currentPair = ''): #Randomly generates a pair of cards for the player

    availableCards = [e for e in cardsList if e not in currentPair]
    newCard1, newCard2 = random.sample(availableCards,2)
    return([newCard1, newCard2])



def addCards(currentPair): #Randomly generates a group of 5 table cards for the player to compare their hand to
    
    availableCards = [e for e in cardsList if e not in currentPair]
    table = random.sample(availableCards, 5)
    return(table)



def combine(pair, table): #Combines the player's pair cards and the table cards into a single list

    totalCards = pair + table
    totalCards.sort()
    printReturn = 'Total cards: ' + str(reorder(totalCards))
    return(totalCards, printReturn)

print('')

def checkValue(x): #Converts face cards to 

    if x == 'J':
        return(11)
    elif x == 'Q':
        return(12)
    elif x == 'K':
        return(13)
    elif x == 'A':
        return(14)
    elif RepresentsInt(x):
        return(int(x))
    else:
        return('N/A')



def returnValues(cardList):

    newList = []

    for card in cardList:
        if len(card) == 2:
            newList += list(card)
        else:
            newList += card[0]
            newList += ['10']
    newList.sort()

    for x, value in enumerate(newList):
        if RepresentsInt(checkValue(value)):
            newList[x] = checkValue(value)
        else:
            newList = removeAll(newList, value)
    newList.sort()
    return(newList)



def reorder(myList):

    newList = []
    for h in range(2,11):
        newList += [item for i, item in enumerate(myList) if RepresentsInt(myList[i][-1]) and len(myList[i]) == 2 and int(myList[i][-1]) == h]
    newList += [item for i, item in enumerate(myList) if len(myList[i]) == 3]
    
    for j in range(4):
        newList += [item for i, item in enumerate(myList) if myList[i][-1] == valueOrder[j]]
    return(newList)



def removeAll(someList, val):
   return([value for value in someList if value != val])



def RepresentsInt(s):
    try: 
        int(s)
        return(True)
    except ValueError:
        return(False)



def convert(letter):
    conversion = {'J':11,
                  'Q':12,
                  'K':13,
                  'A':14}
    
    if letter == 'J' or letter == 'Q' or letter == 'K' or letter == 'A':
        return(conversion[letter])

    else:
        return('z')


def isStraight(cards):

    cards = reorder(cards)
    winningHand = []
    values = returnValues(cards)
    values = list(set(values))

    for i in range(len(values)-4):
        if values[-(i+1)] - values[-(i+5)] == 4:
            for j in range(5):
                winningHand += [card for card in cards if (str(values[(-(i+5))+j]) in card or values[(-(i+5))+j] == checkValue(card[-1]))]

            if len(winningHand) > 5:

                if winningHand[-3][-1] == winningHand[-1][-1]:
                    winningHand.remove(winningHand[-3])
                    winningHand.remove(winningHand[-2])
                
                elif winningHand[-2][-1] == winningHand[-1][-1]:
                    winningHand.remove(winningHand[-2])

                for k in range(len(winningHand)):
                    if k < 4:
                        if winningHand[k+1][-1] == winningHand[k][-1]:
                            if winningHand[k+2][-1] == winningHand[k][-1]:
                                winningHand.remove(winningHand[k+2])
                                winningHand.remove(winningHand[k+1])
                            else:
                                winningHand.remove(winningHand[k+1])
            return[True,winningHand]
    
    return(False)



def isStraightSafe(cards):

    results = []
    values = returnValues(cards)
    values = list(set(values))

    for i in range(len(values)-4):
        if values[-(i+1)] - values[-(i+5)] == 4:
            for j in range(5):
                results += [values[(-(i+5))+j]]
            return[True]
    return(False)



def isFlush(cards):

    suitOrder = ['s','h','c','d']
    winningHand = []
    occ = {'s':[],
           'h':[],
           'c':[],
           'd':[]}
        
    for card in cards:
        if card[0] == 's':
            occ['s'] += [card]
        elif card[0] == 'h':
            occ['h'] += [card]
        elif card[0] == 'c':
            occ['c'] += [card]
        elif card[0] == 'd':
            occ['d'] += [card]

    for suit in suitOrder:
        if len(occ[suit]) >= 5:
            winningHand = reorder(occ[suit])
            while len(winningHand) > 5:
                winningHand.remove(winningHand[0])
            return(True,winningHand)

    return(False)



def isRoyalFlush(cards):
    if isFlush(cards):
        if isStraight(isFlush(cards)[-1]) and isFlush(cards)[-1][-1][-1] == 'A':
            return(True,isStraight(isFlush(cards)[-1])[-1])



def isStraightFlush(cards):
    if isFlush(cards):
        if isStraight(isFlush(cards)[-1]):
            return(True,isStraight(isFlush(cards)[-1])[-1])



def checkOccurrences(cards):

    global isTwoPair
    global isPair
    global is3OfKind
    global is4OfKind
    global isFullHouse
    global isHighCard

    winningHand = []
    reordered = reorder(cards)
    values = returnValues(reordered)
    occurrences = 0
    newList = []

    for i, value in enumerate(values):
        if i < 5:
            if values[i+2] == values[i-1]:
                occurrences += 3
                for j in range(-1,3):
                    newList += [values[i+j]]
                break
            elif values[i+2] == value:
                occurrences += 2
                for j in range(3):
                    newList += [values[i+j]]
            elif (values[i+1] == value and values[i+2] != value and values[i-1] != value) :
                occurrences += 1
                for j in range(2):
                    newList += [values[i+j]]
            elif values[i+1] == values[i+2] and values[i+1] != value and i == 4:
                occurrences += 1
                for j in range(2):
                    newList += [values[(i+1)+j]]

    

    
    if occurrences > 2 and len(newList) == 7 and newList[0] == newList[-1]:
        is4OfKind = True

    elif len(newList) >= 9:
        is4OfKind = True
        newList = removeAll(newList,newList[0])

    elif occurrences > 2 and len(newList) == 5:
        isFullHouse = True

    elif occurrences > 2 and len(newList) == 7:
        isFullHouse = True
        newList = removeAll(newList,newList[0])

    elif occurrences > 2 and len(newList) == 6 and newList[0] == newList[2]:
        isFullHouse = True
        newList.remove(newList[0])

    elif occurrences > 2 and len(newList) == 6 and newList[0] != newList[2]:
        isTwoPair = True
        newList = removeAll(newList,newList[0])

    elif occurrences > 1 and newList[0] == newList[-1]:
        is3OfKind = True

    elif occurrences > 1:
        isTwoPair = True

    elif occurrences == 1:
        isPair = True
    
    else:
        isPair = False
        isTwoPair = False
        is3OfKind = False
        is4OfKind = False
        isFullHouse = False

        if not isStraightSafe(cards) and not isFlush(cards):
            isHighCard = True
    
    for num in list(set(newList)):
        for card in cards:
            if str(num) in card or num == checkValue(card[-1]):
                winningHand += [card]
                winningHand = reorder(winningHand)

    if len(winningHand) > 5:
        for i in range(len(winningHand)-5):
            winningHand.remove(winningHand[i])

    for item in winningHand:
        reordered = removeAll(reordered,item)

    if len(winningHand) < 5:
        for i in range(5-len(winningHand)):
            winningHand += [reordered[-1-i]]

    winningHand = reorder(winningHand)
    return(winningHand)



def returnWinningHand(currentPair, currentTable):

    global isTwoPair
    global isPair
    global is3OfKind
    global is4OfKind
    global isFullHouse
    global isHighCard

    isPair = False
    isTwoPair = False
    is3OfKind = False
    is4OfKind = False
    isFullHouse = False
    isHighCard = False

    winningHand3 = []
    winningHand4 = []

    totalCards = combine(currentPair, currentTable)[0]

    if isRoyalFlush(totalCards):
        winningHand3 = isRoyalFlush(totalCards)[-1]
        return(winningHand3)

    elif isStraightFlush(totalCards):
        winningHand3 = isStraightFlush(totalCards)[-1]
        return(winningHand3)

    elif isFlush(totalCards):
        winningHand3 = isFlush(totalCards)[-1]
        return(winningHand3)
    
    elif isStraight(totalCards):
        winningHand3 = isStraight(totalCards)[-1]
        return(winningHand3)

    winningHand4 = checkOccurrences(totalCards)
    return(winningHand4)



def checkHand(currentPair, currentTable, points):

    global isTwoPair
    global isPair
    global is3OfKind
    global is4OfKind
    global isFullHouse
    global isHighCard

    isPair = False
    isTwoPair = False
    is3OfKind = False
    is4OfKind = False
    isFullHouse = False
    isHighCard = False

    winningHand1 = []
    winningHand2 = []

    totalCards = combine(currentPair, currentTable)[0]
    print(combine(currentPair, currentTable)[1])

    if isRoyalFlush(totalCards):
        winningHand1 = isRoyalFlush(totalCards)[-1]
        points += pointSystem['royalFlush']
        print('Winning Hand: ' + str(winningHand1))
        print('')
        pointsMessage = 'You got a royal flush! +' + str(pointSystem['royalFlush']) + ' points'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)

    elif isStraightFlush(totalCards):
        winningHand1 = isStraightFlush(totalCards)[-1]
        points += pointSystem['straightFlush']
        print('Winning Hand: ' + str(winningHand1))
        print('')
        pointsMessage = 'You got a straight flush! +' + str(pointSystem['straightFlush']) + ' points'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)

    elif isFlush(totalCards):
        winningHand1 = isFlush(totalCards)[-1]
        points += pointSystem['flush']
        print('Winning Hand: ' + str(winningHand1))
        print('')
        pointsMessage = 'You got a flush! +' + str(pointSystem['flush']) + ' points'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)
    
    elif isStraight(totalCards):
        winningHand1 = isStraight(totalCards)[-1]
        points += pointSystem['straight']
        print('Winning Hand: ' + str(winningHand1))
        print('')
        pointsMessage = 'You got a straight! +' + str(pointSystem['straight']) + ' points'
        print
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)

    winningHand2 = checkOccurrences(totalCards)

    if is4OfKind:
        points += pointSystem['4ofKind']
        print('Winning Hand: ' + str(winningHand2))
        print('')
        pointsMessage = 'You got a 4 of a kind! +' + str(pointSystem['4ofKind']) + ' points'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)
    
    if isFullHouse:
        points += pointSystem['fullHouse']
        print('Winning Hand: ' + str(winningHand2))
        print('')
        pointsMessage = 'You got a full house! +' + str(pointSystem['fullHouse']) + ' points'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)

    if is3OfKind:
        points += pointSystem['3ofKind']
        print('Winning Hand: ' + str(winningHand2))
        print('')
        pointsMessage = 'You got a 3 of a kind! +' + str(pointSystem['3ofKind']) + ' points'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)

    if isTwoPair:
        points += pointSystem['twoPair']
        print('Winning Hand: ' + str(winningHand2))
        print('')
        pointsMessage = 'You got a two pair! +' + str(pointSystem['twoPair']) + ' points'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)

    if isPair:
        points += pointSystem['pair']
        print('Winning Hand: ' + str(winningHand2))
        print('')
        pointsMessage = 'You got a pair! +' + str(pointSystem['pair']) + ' points'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)

    elif isHighCard:
        points += pointSystem['highCard']
        print('Winning Hand: ' + str(winningHand2))
        print('')
        pointsMessage = 'You got a high card! +' + str(pointSystem['highCard']) + ' point'
        print('Total points: ' + str(points))
        print('')
        return(points,pointsMessage)
    
    

pointSystem = {'highCard':1,
               'pair':5,
               'twoPair':100,
               '3ofKind':200,
               'straight':1250,
               'flush':2500,
               'fullHouse':3500,
               '4ofKind':20000,
               'straightFlush':350000,
               'royalFlush':3200000}

points = [0,'']
valueOrder = ['J','Q','K','A']

isTwoPair = False
isPair = False
is3OfKind = False
is4OfKind = False
isFullHouse = False
isHighCard = False

cardTypes = ['s','c','h','d'] #The suits for a card are: 's' for spades, 'c' for clubs, 'h' for hearts, or 'd' for diamonds
cardVals = [str(i) for i in range(2,11)] + valueOrder #The values for a card are numbers 2-10, 'J' for Jack, 'Q' for Queen, 'K' for King, or 'A' for Ace
cardsList = [s + c for s in cardTypes for c in cardVals] #The list of all 52 possible cards in a deck are compiled into a list

'''
for i in range(300):
    pair = dealPair()
    Table = addCards(pair)
    points = checkHand(pair, Table, points)
'''

#print('Dealt hand: ' + str(pair))
#print('Table cards: ' + str(Table))

tHighCard = [['d9', 'cJ'], ['d5', 'h4', 'h2', 'sA', 's8']]
tPair = [['d10', 'c10'], ['c6', 'hA', 'h7', 'd4', 'd3']]
t2Pair = [['d10', 'c10'], ['c6', 'hA', 'h7', 'd4', 'd6']]
t3OfKind = [['d10', 'c10'], ['c6', 'h10', 'h7', 'd4', 'd3']]
tTwo3OfKind = [['d10', 'c10'], ['c7', 'h10', 'h7', 'd7', 'd3']]
t4OfKind = [['d10', 'c10'], ['c6', 'h10', 'h7', 's10', 'd3']]
t4OfKind6 = [['d10', 'c10'], ['c6', 'h10', 'h6', 's10', 'd3']]
t4OfKind7 = [['d10', 'c10'], ['c6', 'h10', 'h6', 's10', 'd6']]
t3Pair = [['d10', 'c10'], ['c6', 'hA', 'h7', 'd7', 'd6']]
tFullHouse = [['d10', 'c10'], ['c6', 'h10', 'h7', 's3', 'd3']]

tFlush5 = [['d10', 'cJ'], ['cQ', 'cK', 'h8', 'c2', 'c4']]
tFlush6 = [['c10', 'cJ'], ['cQ', 'cK', 'h8', 'c2', 'c4']]

tStraight5 = [['d4', 's5'], ['s6', 'd7', 'h8', 'cJ', 'cA']] #_______
tStraight6 = [['d4', 's5'], ['s6', 'd7', 'h8', 'c9', 'cA']] #_______
tStraightD1 = [['d5', 's5'], ['s6', 'd7', 'h8', 'c9', 'hJ']] #______
tStraightD2 = [['d6', 's5'], ['s6', 'd7', 'h8', 'c9', 'hJ']] #______
tStraight6D1 = [['d5', 's5'], ['s6', 'd7', 'h8', 'c9', 'h10']] #____
tStraight6D2 = [['d6', 's5'], ['s6', 'd7', 'h8', 'c9', 'h10']] #____
tStraight6D3 = [['d4', 's5'], ['s6', 'd7', 'h8', 'c9', 'h9']] #_____
tStraight6T1 = [['d5', 's5'], ['s6', 'd7', 'h8', 'c9', 'h5']] #_____
tStraight6T2 = [['d8', 's5'], ['s6', 'd7', 'h8', 'c9', 's8']] #_____
tStraight6T3 = [['d9', 's5'], ['s6', 'd7', 'h8', 'c9', 'h9']] #_____
tStraight7 = [['d4', 's5'], ['s6', 'd7', 'h8', 'c9', 'c10']] #______

tStraightFlush5 = [['d4', 'd5'], ['d6', 'd7', 'd8', 'cJ', 'cA']]
tStraightFlush6 = [['d4', 'd5'], ['d6', 'd7', 'd8', 'd9', 'cA']]
tFakeStraightFlush = [['c4', 'h5'], ['d6', 'd7', 'd8', 'dJ', 'dA']]
tRoyalFlush = [['d10', 'dJ'], ['dQ', 'dK', 'dA', 'cJ', 'cA']]

testPair = [['d2', 's2'], ['c3', 'h4', 's5', 'h6', 's6']]

#points = checkHand(tStraightFlush6[0], tStraightFlush6[1], points)

#print(returnWinningHand(tPair[0], tPair[1], points))
#print(isStraight(combine(tStraight6T2[0], tStraight6T2[1])[0]))


run = True
dealButton = button((255,255,255),280,550,250,100,'Deal Hand')
pointsTotalButton = button((255,255,255),400,500,1,1,'')
winningHandTextButton = button((255,255,255),400,450,1,1,'')
pointsMessageButton = button((255,255,255),400,400,1,1,'')

while run:
    redrawWindow(dealButton, pointsTotalButton, winningHandTextButton, pointsMessageButton)
    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if dealButton.isOver(pos):
                newPair = dealPair()
                newTableCards = addCards(newPair)
                points = checkHand(newPair,newTableCards, points[0])
                pointsText = str(points[0])
                pointsMessage = str(points[1])
                winningHandText = 'Winning Hand: ' + str(returnWinningHand(newPair,newTableCards))
                print(winningHandText)
                print(pointsMessage)
                pointsTotalButton.text = (str('Points: ' + pointsText))
                pointsTotalButton.fontColor = (255,0,0)
                winningHandTextButton.text = winningHandText
                winningHandTextButton.fontSize = 40
                pointsMessageButton.text = points[1]
                print(str('Points: ' + pointsText))
        
        if event.type == pygame.MOUSEMOTION:
            if dealButton.isOver(pos):
                dealButton.color = (128,128,128)
            else:
                dealButton.color = (255,255,255)
