'''
This program will simulate a poker game, but with one player and a dealer,
where the objective of the game is to gain points by getting good combinations
of cards (hands)

It's possible we can expand the game to support playing against a computer
'''

import math, random

cardTypes = ['s','c','h','d'] #The suits for a card are: 's' for spades, 'c' for clubs, 'h' for hearts, or 'd' for diamonds
cardVals = [str(i) for i in range(2,11)] + ['J','Q','K','A'] #The values for a card are numbers 2-10, 'J' for Jack, 'Q' for Queen, 'K' for King, or 'A' for Ace
cardsList = [s + c for s in cardTypes for c in cardVals] #The list of all 52 possible cards in a deck are compiled into a list
#print(cardsList)

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
    print('Total cards: ' + str(totalCards))
    return(totalCards)

def isFlush(pair, table):

    totalCards = combine(pair, table)
    totalCards.sort()
    
    results = [card for i, card in enumerate(totalCards) if totalCards[i-1][0] == totalCards[i][0]]

    if len(results) == 4 and results[0][0] == results[1][0] == results[2][0] == results[3][0]: #Not sure how to make this statement more compact
        return(True)
    
    else:
        return(False)

'''
def checkHand(currentPair, currentTable):


    if isFlush:
    
    if isStrsight:

    if isPair:

    if is3OfKind:

    if is4OfKind:

    if isFullhouse:
'''

#For testing purposes:
''' 
for i in range(100):
    pair = dealPair()
    print('Dealt hand: ' + str(pair))
    Table = addCards(pair)
    print('Table cards: ' + str(Table))
    print(isFlush(pair, Table))
'''