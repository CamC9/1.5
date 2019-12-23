'''
This program will simulate a poker game, but with one player and a dealer,
where the objective of the game is to gain points by getting good combinations
of cards (hands)

It's possible we can expand the game to support playing against a computer
'''

import math, random, pygame, sys, time

pygame.init()
pygame.font.init()

win = pygame.display.set_mode((800,800))
win.fill((255,255,255))



class button():
    
    def __init__(self, color, x, y, width, height, text = '', fontColor = (0,0,0), fontSize = 60):
        
        self.color = color
        self.originalColor = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.fontColor = fontColor
        self.fontSize = fontSize

    def draw(self, win, outline = None):
        
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans',self.fontSize)
            text = font.render(self.text, 1, self.fontColor)
            win.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class Card(pygame.sprite.Sprite):

    def __init__(self, image, suit, value, x = 0, y = 280):
        
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.suit = suit
        self.value = value

    def draw(self, win, outline = None):
        
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        if self.image != None:
            win.blit(self.image, [self.x, self.y])
            
    def scaleImage(self, scaleX, scaleY):
        self.image = pygame.transform.scale(self.image,[scaleX,scaleY])
        self.rect = self.image.get_rect()



def redrawWindow(buttonList=[], textsList=[], spriteList=[]):
    
    win.fill((255,255,255))
    for button in buttonList:
        button.draw(win,(0,0,0))
    for text in textsList:
        text.draw(win)
    for sprite in spriteList:
        sprite.draw(win)
    


def dealPair(currentPair=''): #Randomly generates a pair of cards for the player

    availableCards = [e for e in cardsList if e not in currentPair]
    newCard1,newCard2 = random.sample(availableCards,2)
    return([newCard1,newCard2])



def addCards(currentCards): #Randomly generates a group of 5 table cards for the player to compare their hand to
    
    availableCards = [e for e in cardsList if e not in currentCards]
    table = random.sample(availableCards, 5)
    return(table)



def combine(pair,table): #Combines the player's pair cards and the table cards into a single list

    totalCards = pair + table
    totalCards.sort()
    printReturn = 'Total cards: ' + str(reorder(totalCards))
    return(totalCards,printReturn)



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



def removeAll(someList,val):
   
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

        elif cards[0][-1] == '2' and cards[1][-1] == '3' and cards[2][-1] == '4' and cards[3][-1] == '5' and cards[5][-1] == 'A':
            return[True,[cards[5],cards[0],cards[1],cards[2],cards[3]]]

        elif cards[0][-1] == '2' and cards[1][-1] == '3' and cards[2][-1] == '4' and cards[3][-1] == '5' and cards[6][-1] == 'A':
            return[True,[cards[6],cards[0],cards[1],cards[2],cards[3]]]
    
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

        elif cards[0][-1] == '2' and cards[1][-1] == '3' and cards[2][-1] == '4' and cards[3][-1] == '5' and cards[5][-1] == 'A':
            return[True]

        elif cards[0][-1] == '2' and cards[1][-1] == '3' and cards[2][-1] == '4' and cards[3][-1] == '5' and cards[6][-1] == 'A':
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
    winningHandName = ''
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

    if isHighCard:
        winningHandName = 'highCard'
    elif isPair:
        winningHandName = 'pair'
    elif isTwoPair:
        winningHandName = 'twoPair'
    elif is3OfKind:
        winningHandName = '3ofKind'
    elif is4OfKind:
        winningHandName = '4ofKind'
    elif isFullHouse:
        winningHandName = 'fullHouse'

    return([winningHand,winningHandName])



def returnWinningHand(currentPair='',currentTable='',totalCards=''):

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

    if totalCards == '':
        totalCards = combine(currentPair, currentTable)[0]

    if isRoyalFlush(totalCards):
        winningHand3 = isRoyalFlush(totalCards)[-1]
        return([winningHand3,'royalFlush'])

    elif isStraightFlush(totalCards):
        winningHand3 = isStraightFlush(totalCards)[-1]
        return([winningHand3,'straightFlush'])

    elif isFlush(totalCards):
        winningHand3 = isFlush(totalCards)[-1]
        return([winningHand3,'flush'])
    
    elif isStraight(totalCards):
        winningHand3 = isStraight(totalCards)[-1]
        return([winningHand3,'straight'])

    winningHand4 = checkOccurrences(totalCards)
    return([winningHand4[0],winningHand4[-1]])



def returnBetterHand(hand1,hand2):

    print()
    print(hand1)
    print(hand2)

    winningHandRank1 = returnWinningHand('','',hand1)[-1]
    winningHandRank2 = returnWinningHand('','',hand2)[-1]

    winningHand1 = returnWinningHand('','',hand1)[0]
    winningHand2 = returnWinningHand('','',hand2)[0]

    if handSystem[winningHandRank1] > handSystem[winningHandRank2]:
        return([winningHand1,'User wins with a ' + winningHandRank1,0])

    elif handSystem[winningHandRank2] > handSystem[winningHandRank1]:
        return([winningHand2,'Comp wins with a ' + winningHandRank2,1])

    for i in range(5):
        if checkValue(winningHand1[-(i+1)][-1]) > checkValue(winningHand2[-(i+1)][-1]):
            return([winningHand1,'User wins with a ' + winningHandRank1,0])

        elif checkValue(winningHand2[-(i+1)][-1]) > checkValue(winningHand1[-(i+1)][-1]):
            return([winningHand2,'Comp wins with a ' + winningHandRank2,1])

    return([winningHand1,'Both win with a ' + winningHandRank1,2])



def displayMessage(text):
    displayedMessageText.text = text
    redrawWindow(buttonList,textsList)
    pygame.display.update()
    time.sleep(1.5)
    displayedMessageText.text = ''

handSystem = {'highCard':1,
               'pair':2,
               'twoPair':3,
               '3ofKind':4,
               'straight':5,
               'flush':6,
               'fullHouse':7,
               '4ofKind':8,
               'straightFlush':9,
               'royalFlush':10}

valueOrder = ['J','Q','K','A']

chips = 1000

isTwoPair = False
isPair = False
is3OfKind = False
is4OfKind = False
isFullHouse = False
isHighCard = False

cardTypes = ['s','c','h','d'] #The suits for a card are: 's' for spades, 'c' for clubs, 'h' for hearts, or 'd' for diamonds
cardVals = [str(i) for i in range(2,11)] + valueOrder #The values for a card are numbers 2-10, 'J' for Jack, 'Q' for Queen, 'K' for King, or 'A' for Ace
cardsList = [s + c for s in cardTypes for c in cardVals] #The list of all 52 possible cards in a deck are compiled into a list

tHighCard = [['d9', 'cJ'], ['d5', 'h4', 'h2', 'sA', 's8']]
tPair = [['d10', 'c10'], ['c6', 'hA', 'h7', 'd4', 'd3']]
t2Pair1 = [['d10', 'c10'], ['c6', 'hA', 'h7', 'd4', 'd6']]
t2Pair2 = [['d2', 'c2'], ['c6', 'hA', 'h7', 'd4', 'd6']]
t3OfKind = [['d10', 'c10'], ['c6', 'h10', 'h7', 'd4', 'd3']]
tTwo3OfKind = [['d10', 'c10'], ['c7', 'h10', 'h7', 'd7', 'd3']]
t4OfKind = [['d10', 'c10'], ['c6', 'h10', 'h7', 's10', 'd3']]
t4OfKind6 = [['d10', 'c10'], ['c6', 'h10', 'h6', 's10', 'd3']]
t4OfKind7 = [['d10', 'c10'], ['c6', 'h10', 'h6', 's10', 'd6']]
t3Pair = [['d10', 'c10'], ['c6', 'hA', 'h7', 'd7', 'd6']]
tFullHouse = [['d10', 'c10'], ['c6', 'h10', 'h7', 's3', 'd3']]
tFlush5 = [['d10', 'cJ'], ['cQ', 'cK', 'h8', 'c2', 'c4']]
tFlush6 = [['c10', 'cJ'], ['cQ', 'cK', 'h8', 'c2', 'c4']]
tStraightA = [['s2', 'sA'], ['c5', 'c3', 'c4', 'h7', 'h10']] #______
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
tTotal1 = ['c2','s2','d3','c3','sJ','hA','hQ']
tTotal2 = ['c8','s8','d3','c3','sJ','hA','hQ']
testPair = [['d2', 's2'], ['c3', 'h4', 's5', 'h6', 's6']]

start = 0
run = True

dealButton = button((255,255,255),280,550,250,100,'Deal Cards')
userWinningHandText = button((255,255,255),400,450,1,1,'',(0,0,0),40)
compWinningHandText = button((255,255,255),400,475,1,1,'',(0,0,0),40)
displayedMessageText = button((255,255,255),400,125,1,1,'',(255,0,0),50)
chipsText = button((255,255,255),650,50,1,1,'Chips: ' + str(chips),(0,0,255))
tableCardsText = button((255,255,255),400,300,1,1,'')
userPairText = button((255,255,255),200,375,1,1,'',(0,0,0),40)
compPairText = button((255,255,255),600,375,1,1,'',(0,0,0),40)
winnerText = button((255,255,255),400,200,1,1,'',(47,150,6),50)

startButton = button((0,255,0),230,400,350,150,'START',(0,0,0),100)
quitButton = button((255,0,0),10,20,90,30,'QUIT',(0,0,0),35)
betButton = button((255,255,0),50,600,180,90,'Bet')

buttonList = [dealButton,startButton,quitButton,betButton]
textsList = [winnerText,userWinningHandText,compWinningHandText,displayedMessageText,chipsText,tableCardsText,userPairText,compPairText]

activeSprites = pygame.sprite.Group()
totalSprites = pygame.sprite.Group()

C2 = Card('Cardz/2C.png','c',2)
C3 = Card('Cardz/3C.png','c',3)
C4 = Card('Cardz/4C.png','c',4)
C5 = Card('Cardz/5C.png','c',5)
C6 = Card('Cardz/6C.png','c',6)
C7 = Card('Cardz/7C.png','c',7)
C8 = Card('Cardz/8C.png','c',8)
C9 = Card('Cardz/9C.png','c',9)
C10 = Card('Cardz/10C.png','c',10)
CJ = Card('Cardz/JC.png','c',11)
CQ = Card('Cardz/QC.png','c',12)
CK = Card('Cardz/KC.png','c',13)
CA = Card('Cardz/AC.png','c',14)
D2 = Card('Cardz/2D.png','d',2)
D3 = Card('Cardz/3D.png','d',3)
D4 = Card('Cardz/4D.png','d',4)
D5 = Card('Cardz/5D.png','d',5)
D6 = Card('Cardz/6D.png','d',6)
D7 = Card('Cardz/7D.png','d',7)
D8 = Card('Cardz/8D.png','d',8)
D9 = Card('Cardz/9D.png','d',9)
D10 = Card('Cardz/10D.png','d',10)
DJ = Card('Cardz/JD.png','d',11)
DQ = Card('Cardz/QD.png','d',12)
DK = Card('Cardz/KD.png','d',13)
DA = Card('Cardz/AD.png','d',14)
H2 = Card('Cardz/2H.png','h',2)
H3 = Card('Cardz/3H.png','h',3)
H4 = Card('Cardz/4H.png','h',4)
H5 = Card('Cardz/5H.png','h',5)
H6 = Card('Cardz/6H.png','h',6)
H7 = Card('Cardz/7H.png','h',7)
H8 = Card('Cardz/8H.png','h',8)
H9 = Card('Cardz/9H.png','h',9)
H10 = Card('Cardz/10H.png','h',10)
HJ = Card('Cardz/JH.png','h',11)
HQ = Card('Cardz/QH.png','h',12)
HK = Card('Cardz/KH.png','h',13)
HA = Card('Cardz/AH.png','h',14)
S2 = Card('Cardz/2S.png','s',2)
S3 = Card('Cardz/3S.png','s',3)
S4 = Card('Cardz/4S.png','s',4)
S5 = Card('Cardz/5S.png','s',5)
S6 = Card('Cardz/6S.png','s',6)
S7 = Card('Cardz/7S.png','s',7)
S8 = Card('Cardz/8S.png','s',8)
S9 = Card('Cardz/9S.png','s',9)
S10 = Card('Cardz/10S.png','s',10)
SJ = Card('Cardz/JS.png','s',11)
SQ = Card('Cardz/QS.png','s',12)
SK = Card('Cardz/KS.png','s',13)
SA = Card('Cardz/AS.png','s',14)
cardBack = Card('Cardz/red_back.png','',0)

Cards = [
            C2, C3, C4, C5, C6, C7, C8, C9, C10, CJ, CQ, CK, CA,
            D2, D3, D4, D5, D6, D7, D8, D9, D10, DJ, DQ, DK, DA,
            H2, H3, H4, H5, H6, H7, H8, H9, H10, HJ, HQ, HK, HA,
            S2, S3, S4, S5, S6, S7, S8, S9, S10, SJ, SQ, SK, SA,
            cardBack
        ]

for card in Cards:
    card.scaleImage(69*2,106*2)
    totalSprites.add(card)



while run:

    pygame.display.update()

    for event in pygame.event.get():
        pos = pygame.mouse.get_pos()

        if event.type == pygame.QUIT:
            run = False
            start = 0
            pygame.quit()
            quit()

        if start == 1:
            redrawWindow(buttonList,textsList,activeSprites)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if dealButton.isOver(pos):
                    
                    userPair = dealPair()
                    compPair = dealPair(userPair)

                    usedCards = userPair + compPair

                    newTableCards = addCards(usedCards)
                    print(reorder(usedCards + newTableCards))

                    tableCardsText.text = 'Table cards: ' + str(newTableCards)
                    userPairText.text = 'User pair: ' + str(userPair)
                    compPairText.text = 'Comp pair: ' + str(compPair)
                    
                    userWinningHandMessage = 'User Winning Hand: ' + str(returnWinningHand(userPair,newTableCards)[0])
                    userWinningHandText.text = userWinningHandMessage

                    compWinningHandMessage = 'Comp Winning Hand: ' + str(returnWinningHand(compPair,newTableCards)[0])
                    compWinningHandText.text = compWinningHandMessage
                
                    winnerText.text = str(returnBetterHand(combine(userPair,newTableCards)[0],combine(compPair,newTableCards)[0])[1])

                elif betButton.isOver(pos):
                    betButton.color = (255,255,255)
                    done = False
                    betButton.text = ''

                    while not done:
                        for event in pygame.event.get():
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_RETURN:
                                    try:
                                        betAmount = int(betButton.text)

                                        if betAmount <= chips and betAmount > 0:
                                            displayMessage('You bet ' + str(betButton.text) + ' chips')
                                            done = True
                                            chips -= betAmount
                                            chipsText.text = 'Chips: ' + str(chips)

                                        elif betAmount <= 0:
                                            displayMessage("You must bet a positive amount!")

                                        else:
                                            displayMessage("You can't bet more chips than you have!")
                                        
                                    except ValueError:
                                        displayMessage('Your bet must be an integer!')
                                    
                                elif event.key == pygame.K_BACKSPACE:
                                    betButton.text = betButton.text[:-1]
                                    D8.x += 10
                                else:
                                    if len(betButton.text) <= 5:
                                        betButton.text += event.unicode
                            
                            elif event.type == pygame.QUIT:
                                run = False
                                done = True
                                start = 0
                                pygame.quit()
                                quit()

                        redrawWindow(buttonList,textsList,activeSprites)
                        pygame.display.update()

                    betButton.color = betButton.originalColor
                    betButton.text = 'Bet'

                elif quitButton.isOver(pos):
                    start = 0
                    buttonList.append(startButton)
                    activeSprites = pygame.sprite.Group()

                    for card in Cards:
                        card.x = 0
                        card.y = 280
        
        else:
            redrawWindow([startButton])

            if event.type == pygame.MOUSEBUTTONDOWN:
                if startButton.isOver(pos):
                    start = 1
                    userWinningHandText.text = ''
                    compWinningHandText.text = ''
                    userPairText.text = ''
                    compPairText.text = ''
                    winnerText.text = ''
                    tableCardsText.text = ''
                    chips = 1000
                    buttonList.remove(startButton)
                    betButton.text = 'Bet'
                    chipsText.text = 'Chips: ' + str(chips)

                    for i, card in enumerate(Cards):
                        if card.suit == 'c':
                            card.x += 15 * i
                            activeSprites.add(card)
                    cardBack.x += 400
                    activeSprites.add(cardBack)
        
        if event.type == pygame.MOUSEMOTION:
            for button in buttonList:
                if button.isOver(pos):
                    button.color = (128,128,128)
                else:
                    button.color = button.originalColor
