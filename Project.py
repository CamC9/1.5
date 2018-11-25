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
    
    newList = list(set(newList))
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



def isPair(cards):

    values = returnValues(cards)



def checkHand(currentPair, currentTable, points):

    totalCards = combine(currentPair, currentTable)

    if isFlush(totalCards):
        points += pointSystem['flush']
        print('')
        print('You got a flush! +' + str(pointSystem['flush']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print(isFlush(totalCards))
        print('')
    
    if isStraight(totalCards):
        points += pointSystem['straight']
        print('')
        print('You got a straight! +' + str(pointSystem['straight']) + ' points')
        print('')
        print('Total points: ' + str(points))
        print(isStraight(totalCards))
        print('')
    
    if isPair(totalCards):
        points += pointSystem['pair']
    #if is3OfKind:

    #if is4OfKind:

    #if isFullhouse:

    return(points)

pointSystem = {'pair':5,
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
    
#testList = ['d10', 'cA', 'c5', 'c2', 'c9', 's8', 'c10']
