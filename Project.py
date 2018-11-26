'''
This program will simulate a poker game, but with one player and a dealer,
where the objective of the game is to gain points by getting good combinations
of cards (hands)

It's possible we can expand the game to support playing against a computer
'''

import math, random





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
    print('Total cards: ' + str(totalCards))
    return(totalCards)



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



def isStraight(cards):

    results = []
    values = returnValues(cards)
    values = list(set(values))

    for i in range(len(values)-4):
        if values[-(i+1)] - values[-(i+5)] == 4:
            for j in range(5):
                results += [values[(-(i+5))+j]]
            return[True,results]
    return(False)



def isFlush(cards):

    results = [card for i, card in enumerate(cards) if cards[i-1][0] == cards[i][0]]

    if len(results) == 4 and results[0][0] == results[1][0] == results[2][0] == results[3][0]: #Not sure how to make this statement more compact
        results += [cards[(cards.index(results[0]))-1]]
        results = reorder(results)
        return[True,results]    
    else:
        return(False)



def checkOccurrences(cards):

    global isTwoPair
    global isPair
    global is3OfKind
    global is4OfKind
    global isFullHouse

    reordered = reorder(cards)
    values = returnValues(reordered)
    occurrences = 0
    newList = []

    for i, value in enumerate(values):
        if values[i-1] == value:
            occurrences += 1
            newList += [value]

    if occurrences > 2 and newList[0] == newList[1] == newList[2]:
        is4OfKind = True

    elif occurrences > 2:
        isFullHouse = True

    elif occurrences > 1 and newList[0] == newList[1]:
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
    


def checkHand(currentPair, currentTable, points):

    global isTwoPair
    global isPair
    global is3OfKind
    global is4OfKind
    global isFullHouse

    isPair = False
    isTwoPair = False
    is3OfKind = False
    is4OfKind = False
    isFullHouse = False

    totalCards = combine(currentPair, currentTable)

    if isFlush(totalCards):

        if isStraight(isFlush(totalCards)[-1]) and isFlush(totalCards) and isFlush(totalCards)[-1][-1][-1] == 'A':
            points += pointSystem['royalFlush']
            print('')
            print('You got a royal flush! +' + str(pointSystem['royalFlush']) + ' points')
            print('')
            print('Total points: ' + str(points))
            print('')
            return(points)

        if isStraight(isFlush(totalCards)[-1]) and isFlush(totalCards):
            points += pointSystem['straightFlush']
            print('')
            print('You got a straight flush! +' + str(pointSystem['straightFlush']) + ' points')
            print('')
            print('Total points: ' + str(points))
            print('')
            return(points)

        points += pointSystem['flush']
        print('')
        print('You got a flush! +' + str(pointSystem['flush']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print(isFlush(totalCards))
        print('')
        return(points)
    
    if isStraight(totalCards):
        points += pointSystem['straight']
        print('')
        print('You got a straight! +' + str(pointSystem['straight']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print(isStraight(totalCards))
        print('')
        return(points)

    checkOccurrences(totalCards)
    
    if is4OfKind:
        points += pointSystem['4ofKind']
        print('')
        print('You got a 4 of a kind! +' + str(pointSystem['4ofKind']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print('')
        return(points)
    
    if isFullHouse:
        points += pointSystem['fullHouse']
        print('')
        print('You got a full house! +' + str(pointSystem['fullHouse']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print('')
        return(points)

    if is3OfKind:
        points += pointSystem['3ofKind']
        print('')
        print('You got a 3 of a kind! +' + str(pointSystem['3ofKind']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print('')
        return(points)

    if isTwoPair:
        points += pointSystem['twoPair']
        print('')
        print('You got a two pair! +' + str(pointSystem['twoPair']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print('')
        return(points)

    if isPair:
        points += pointSystem['pair']
        print('')
        print('You got a pair! +' + str(pointSystem['pair']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print('')
        return(points)

    else:
        points += pointSystem['highCard']
        print('')
        print('You got a high card! +' + str(pointSystem['highCard']) + ' point')
        print('')
        print('Total points: ' + str(points))
        print('')
        return(points)

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

points = 0
valueOrder = ['J','Q','K','A']

isTwoPair = False
isPair = False
is3OfKind = False
is4OfKind = False
isFullHouse = False

cardTypes = ['s','c','h','d'] #The suits for a card are: 's' for spades, 'c' for clubs, 'h' for hearts, or 'd' for diamonds
cardVals = [str(i) for i in range(2,11)] + valueOrder #The values for a card are numbers 2-10, 'J' for Jack, 'Q' for Queen, 'K' for King, or 'A' for Ace
cardsList = [s + c for s in cardTypes for c in cardVals] #The list of all 52 possible cards in a deck are compiled into a list

'''
for i in range(300):
    pair = dealPair()
    print('Dealt hand: ' + str(pair))
        
    Table = addCards(pair)
    print('Table cards: ' + str(Table))

    points = checkHand(pair, Table, points)
'''
    
#testList = ['d10', 'cA', 'h10', 'c2', 'h4', 's10', 'c10']

testPair = ['sA', 'sK']
testTable = ['sQ', 'sJ', 's10', 'c4', 'h9']

points = checkHand(testPair, testTable, points)

'''
print('isPair: ' + str(isPair))
print('isTwoPair: ' + str(isTwoPair))
print('is3OfKind: ' + str(is3OfKind))
print('is4OfKind: ' + str(is4OfKind))
print('isFullHouse: ' + str(isFullHouse))
'''