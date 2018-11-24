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

def isFlush(cards):

    results = [card for i, card in enumerate(cards) if cards[i-1][0] == cards[i][0]]

    if len(results) == 4 and results[0][0] == results[1][0] == results[2][0] == results[3][0]: #Not sure how to make this statement more compact
        return(True)
    
    else:
        return(False)

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



def removeAll(someList, val):
   return([value for value in someList if value != val])



def RepresentsInt(s):
    try: 
        int(s)
        return(True)
    except ValueError:
        return(False)



def isStraight(cards):

    values = returnValues(cards)

    for i in range(len(values)-4):
        if values[-(i+1)] - values[-(i+5)] == 4:
            return(True)
    return(False)



def isPair(cards):

    values = returnValues(cards)



def checkHand(currentPair, currentTable, points):

    totalCards = combine(currentPair, currentTable)

    if isFlush(totalCards):
        points += 3500
        print('')
        print('You got a flush! +3500 points')
        print('')
        print('Total points: ' + str(points))
        print('')
    
    if isStraight(totalCards):
        points += 1800
        print('')
        print('You got a straight! +1800 points')
        print('')
        print('Total points: ' + str(points))
        print('')
    
    return(points)

    if isPair(totalCards):

    #if is3OfKind:

    #if is4OfKind:

    #if isFullhouse:


cardTypes = ['s','c','h','d'] #The suits for a card are: 's' for spades, 'c' for clubs, 'h' for hearts, or 'd' for diamonds
cardVals = [str(i) for i in range(2,11)] + ['J','Q','K','A'] #The values for a card are numbers 2-10, 'J' for Jack, 'Q' for Queen, 'K' for King, or 'A' for Ace
cardsList = [s + c for s in cardTypes for c in cardVals] #The list of all 52 possible cards in a deck are compiled into a list

points = 0

pair = dealPair()
print('Dealt hand: ' + str(pair))
    
Table = addCards(pair)
print('Table cards: ' + str(Table))
    
#testList = ['d10', 'cA', 'c5', 'c2', 'd9', 's8', 's9']