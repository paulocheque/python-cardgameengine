'''
Created on Mar 24, 2009

@author: paulo
'''

from cardgameengine import cards
from cardgames import pokertexasholdem

SPADES=1
HEARTS=2
DIAMONDS=3
CLUBS=4
AS=1
J=11
Q=12
K=13


def c(*tuples):
  stack = cards.StackOfCards()
  for value, suit in tuples:
    stack.push(pokertexasholdem.PokerTexasHoldEmCard(value, suit))
  return stack
    

def lowerHighCards():
  return c((2, CLUBS), (3, CLUBS), (4, CLUBS), (5, CLUBS), (7, HEARTS))

print(lowerHighCards().cards[0])
print(lowerHighCards().cards[1])

def greaterHighCards():
  return c((9, CLUBS), (J, CLUBS), (Q, CLUBS), (K, CLUBS), (AS, HEARTS))


def lowerOnePair():
  return c((2, CLUBS), (2, HEARTS), (3, CLUBS), (4, CLUBS), (5, CLUBS))


def greaterOnePair():
  return c((AS, CLUBS), (AS, HEARTS), (K, CLUBS), (Q, CLUBS), (J, CLUBS))


def lowerTwoPairs():
  return c((2, CLUBS), (2, HEARTS), (3, CLUBS), (3, HEARTS), (4, CLUBS))


def greaterTwoPairs():
  return c((AS, CLUBS), (AS, HEARTS), (K, CLUBS), (K, HEARTS), (Q, CLUBS))


def lowerThreeOfAKind():
  return c((2, CLUBS), (2, HEARTS), (2, SPADES), (3, CLUBS), (4, HEARTS))


def greaterThreeOfAKind():
  return c((AS, CLUBS), (AS, HEARTS), (AS, SPADES), (K, CLUBS), (Q, HEARTS))


def lowerStraight():
 return c((2, CLUBS), (3, HEARTS), (4, SPADES), (5, DIAMONDS), (6, CLUBS)) 


def greaterStraight():
 return c((AS, CLUBS), (K, HEARTS), (Q, SPADES), (J, DIAMONDS), (10, CLUBS)) 


def StraightWithAS2():
 return c((AS, CLUBS), (2, HEARTS), (3, SPADES), (4, DIAMONDS), (5, CLUBS)) 


def lowerFullHouse():
  return c((2, CLUBS), (2, HEARTS), (2, SPADES), (3, CLUBS), (3, HEARTS))


def greaterFullHouse():
  return c((AS, CLUBS), (AS, HEARTS), (AS, SPADES), (K, CLUBS), (K, HEARTS))


def lowerFlush():
  return c((2, DIAMONDS), (3, DIAMONDS), (4, DIAMONDS), (5, DIAMONDS), (7, DIAMONDS))


def greaterFlush():
  return c((AS, DIAMONDS), (K, DIAMONDS), (Q, DIAMONDS), (J, DIAMONDS), (9, DIAMONDS))


def lowerFourOfAKind():
  return c((2, CLUBS), (2, HEARTS), (2, SPADES), (2, DIAMONDS), (3, CLUBS))


def greaterFourOfAKind():
  return c((AS, CLUBS), (AS, HEARTS), (AS, SPADES), (AS, DIAMONDS), (K, CLUBS))


def lowerStraightFlush():
 return c((2, CLUBS), (3, CLUBS), (4, CLUBS), (5, CLUBS), (6, CLUBS)) 


def greaterStraightFlush():
 return c((AS, CLUBS), (K, CLUBS), (Q, CLUBS), (J, CLUBS), (10, CLUBS)) 
