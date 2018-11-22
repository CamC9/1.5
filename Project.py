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

def dealPair(currentPair = ''):

    availableCards = [e for e in cardsList if e not in currentPair]
    newCard1, newCard2 = random.sample(availableCards,2)

    return([newCard1, newCard2])

def addCards(currentPair):
    
    availableCards = [e for e in cardsList if e not in currentPair]
    deck = random.sample(availableCards, 5)
    return(deck)

pair = dealPair()
print('Dealt hand: ' + str(pair))
print('Dealt deck: ' + str(addCards(pair)))