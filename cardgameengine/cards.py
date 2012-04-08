'''

@author: Paulo Cheque (paulocheque@gmail.com)

Possible values: 
'Card': Ordered by value / Equality by value and suit
'ValueCard': Ordered by value / Equality by value
'SuitCard': Ordered by value and suit / Equality by value and suit
'''

from domain import dataobjects
import random
import copy
from gameengine import utils
from cardgameengine.constants import *

class Card(dataobjects.OrderedValueObject):
  '''
  Ordered by value / Equality by value and suit
  '''
  
  values = {}
  suits = {}
  
  def __init__(self, value, suit, score=0):
    self.value = value
    self.suit = suit
    self.score = score
    
  def equalsVariables(self):
    return ['value', 'suit']
    
  def priorityOrder(self):
    return ['value']
  
  def __str__(self):
    if self.value in self.values: v = self.values[self.value]
    else: v = str(self.value)
    if self.suit in self.suits: s = self.suits[self.suit]
    else: s = str(self.suit)
    return v + '-' + s
  
class ValueCard(Card):
  '''
  Ordered by value / Equality by value
  '''
  
  def equalsVariables(self):
    return ['value']  

class SuitCard(Card):
  '''
  Ordered by value and suit / Equality by value and suit
  '''

  def priorityOrder(self):
    return ['value', 'suit']
  
class StackOfCards(dataobjects.ValueObject):
  '''
  One deck is a stack of cards. 
  This class has useful methods to manipulate the stack and to verifify the deck.
  '''
  
  def __init__(self):
    self.cards = []
    
  def __str__(self):
    return ' '.join([str(card) for card in self.cards])
    
  # Prototype
  def clone(self):
    theclone = self.__class__()
    theclone.pushAll(self)
    return theclone
  
  def __cardsFromCardOrStackOrList(self, cardOrStackOrList):
    cards = cardOrStackOrList
    if isinstance(cardOrStackOrList, StackOfCards):
      cards = cardOrStackOrList.cards
    elif isinstance(cardOrStackOrList, Card):
      cards = [cardOrStackOrList]
    return cards
    
  def score(self):
    score = 0
    for card in self.cards:
      score += card.score
    return score
      
  def isEmpty(self):
    return len(self.cards) == 0
  
  def push(self, card):
    self.cards.append(card)
  
  def pushAll(self, cardOrStackOrList):
    '''
    Accept cards.StackOfCards or a []
    
    Example:
    deck1 = cards.StackOfCards()
    deck2 = cards.StackOfCards()
    deck1.pushAll(deck2) # dont remove elements of deck2
    deck1.pushAll(deck2.popAll()) # remove elements of deck2 because popAll does it
    '''
    cards = self.__cardsFromCardOrStackOrList(cardOrStackOrList)
    for card in cards:
      self.push(card)

  def pop(self):
    return self.cards.pop()

  def popIndex(self, index):
    c = self.see(index)
    self.cards.remove(c)
    return c
  
  def popAll(self):
    cards = self.cards
    self.cards = []
    list = StackOfCards()
    list.pushAll(cards)
    return list

  def popCard(self, card):
    c = self.see(self.cards.index(card))
    self.cards.remove(c)
    return c
  
  def popCards(self, cardOrStackOrList):
    cards = self.__cardsFromCardOrStackOrList(cardOrStackOrList)
    list = StackOfCards()
    for card in cards[:]:
      list.push(self.popCard(card))
    return list
  
  def popCardsWithValue(self, value):
    list = StackOfCards()
    for card in self.cards[:]:
      if card.value == value:
        list.push(self.popCard(card))
    return list
  
  def popCardsWithSuit(self, suit):
    list = StackOfCards()
    for card in self.cards[:]:
      if card.suit == suit:
        list.push(self.popCard(card))
    return list

  def see(self, index):
    return self.cards[index]
  
  def seeFirstCard(self):
    return self.see(0)
  
  def seeLastCard(self):
    return self.see(len(self.cards)-1)
  
  def numberOfCards(self, aCard):
    number = 0
    for card in self.cards:
      if aCard.value == card.value and aCard.suit == card.suit:
        number += 1
    return number
      
  def numberOfCardsWithValue(self, value):
    number = 0
    for card in self.cards:
      if value == card.value:
        number += 1
    return number
      
  def numberOfCardsWithSuit(self, suit):
    number = 0
    for card in self.cards:
      if suit == card.suit:
        number += 1
    return number

  def containsCard(self, card):
    return card in self.cards
  
  def containsAllCards(self, cardOrStackOrList):
    cards = self.__cardsFromCardOrStackOrList(cardOrStackOrList)
    for card in cards:
      if not self.containsCard(card):
        return False
    return True
  
  def containsCardWithValue(self, value):
    for card in self.cards:
      if card.value == value:
        return True
    return False
  
  def containsCardWithSuit(self, suit):
    for card in self.cards:
      if card.suit == suit:
        return True
    return False
  
  def compareByHeight(self, that):
    return self.height() - that.height()

  def compareByHighValue(self, that):
    cards = self.cards[:]
    cards.sort(key=self.keySortByValue)
    thatcards = that.cards[:]
    thatcards.sort(key=self.keySortByValue)
    for card, thatcard in reversed(zip(cards, thatcards)):
      difference = card.value - thatcard.value
      if difference != 0: return difference
    return self.compareByHeight(that)
  
  def compareByLowValue(self, that):
    cards = self.cards[:]
    cards.sort(key=self.keySortByValue)
    thatcards = that.cards[:]
    thatcards.sort(key=self.keySortByValue)
    for card, thatcard in zip(cards, thatcards):
      difference = thatcard.value - card.value
      if difference != 0: return difference
    return self.compareByHeight(that)
  
  def sort(self):
    self.cards = sorted(self.cards)
    
  @staticmethod
  def keySortByValue(card): return card.value
  @staticmethod  
  def keySortBySuit(card): return card.suit
  @staticmethod
  def keySortByValueAndSuit(card): return card.value, card.suit
  @staticmethod
  def keySortBySuitAndValue(card): return card.suit, card.value
  @staticmethod
  def keySortByScore(card): return card.score

  def sortByValue(self):
    self.cards.sort(key=self.keySortByValue)
  
  def sortBySuit(self):
    self.cards.sort(key=self.keySortBySuit)
  
  def sortByValueAndSuit(self):
    self.cards.sort(key=self.keySortByValueAndSuit)
    
  def sortBySuitAndValue(self):
    self.cards.sort(key=self.keySortBySuitAndValue)
    
  def sortByScore(self):
    self.cards.sort(key=self.keySortByScore)
  
  def shuffle(self):
    random.shuffle(self.cards)
    
  def height(self):
    return len(self.cards)
    
  def allCardsWithSameValue(self):
    for card1, card2 in zip(self.cards, self.cards[1:]):
      if card1.value != card2.value:
        return False
    return True
  
  def allCardsWithSameSuit(self):
    for card1, card2 in zip(self.cards, self.cards[1:]):
      if card1.suit != card2.suit:
        return False
    return True
  
  def allCardsWithSameValueAndSuit(self):
    return self.allCardsWithSameValue() and self.allCardsWithSameSuit()
  
  def allCardsInSequence(self):
    return self.allCardsInSequenceWithJokers(0)

  def allCardsInSequenceWithSameSuit(self):
    return self.allCardsInSequenceWithSameSuitWithJokers(0)

  # Jokers

  def allCardsInSequenceWithJokers(self, numberOfJokers):
    control = numberOfJokers
    sortedcards = self.cards[:]
    sortedcards.sort(key=self.keySortByValue)
    for card1, card2 in zip(sortedcards, sortedcards[1:]):
      difference = card2.value - card1.value
      if difference == 0: return False
      control -= (difference - 1)
      if control < 0: 
        return False
    return True
  
  def allCardsInSequenceWithSameSuitWithJokers(self, numberOfJokers):
    return self.allCardsInSequenceWithJokers(numberOfJokers) and self.allCardsWithSameSuit()
  
  def allCombinationsOfCards(self, min=1, max=0):
    combinations = []
    if max == 0: max = self.height()
    if min > max or max > self.height(): return combinations
    for r in range(min, max+1):
      generator = utils.CombinationGenerator(self.height(), r)
      while generator.hasNext():
        indexes = generator.next()
        combination = StackOfCards()
        for i in indexes:
          combination.push(self.see(i))
        combinations.append(combination)
    return combinations
  
# Builder
class DeckPrototypeBuilder(object):
  '''
  Builder of deck's prototypes
  '''
  
  @staticmethod
  def createCommonDeck(
      cardClass, numberOfSuits, numberOfCardsPerSuit, 
      numberOfDecks=1, numberOfJokersPerDeck=0, scoreFunction=lambda value,suit: 0):
    '''
    # Parameters:
    # cardClass: Class object of the card, to use to create instances, like prototype pattern.
    # numberOfSuits: Number os different suits, tipically is 2 or 4
    # numberOfCardsPerSuit: Number of cards per suit, tipically is 10, 11, 12 or 13
    # numberOfDecks (default 1): Number of decks, i.e., equal cards (value and suit) in the deck
    # numberOfJokersPerDeck (default 0): Number of jokers (Card(0, 0)) per deck
    # scoreFunction (default: lambda value,suit: 0): give a function with rules of score
    # Example:
    def scoreFunction(value, score):
      if value == 0: return 20
      if value == 1: return 15
      if value == 2: return 10
      if value >= 3 and value <= 7: return 5
      if value >= 8 and value <= 13: return 10
      
    deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(MyCard, 4, 13, 1, 0, scoreFunction)
    
    # If you need a not common deck, for example two cards with same value and suit but with different score,
    # you can simply do this (example):
    # deckPrototype = cards.StackOfCards()
    # deckPrototype.pushCard(-1, 500, 34)
    # deckPrototype.pushCard(-50, -123, 1234)
    # deckPrototype.pushCard(-50, -123, 456)
    # deckPrototype.pushCard(-50, -123)
    '''
    
    deck = StackOfCards()
    for x in range(1, numberOfDecks+1):
      for suit in range(1, numberOfSuits+1):
        for value in range(1, numberOfCardsPerSuit+1):
            # Prototype style: cardClass
            deck.push(cardClass(value, suit, scoreFunction(value, suit)))
      for x in range(1, numberOfJokersPerDeck+1):
        deck.push(cardClass(0, 0, scoreFunction(0, 0)))
    deck.sort()
    return deck

SUITS_ANGLO_AMERICAN = {'SPADES': 1, 'HEARTS': 2, 'DIAMONDS': 3, 'CLUBS': 4}
SUITS_ITALIAN = {'COINS': 1, 'SWORDS': 2, 'CUPS': 3, 'CLUBS': 4}
SUITS_GERMAN = {'HEARTS': 1, 'BELLS': 2, 'LEAVES': 3, 'ACORNS': 4}
SUITS_PORTUGUESE = {'ESPADAS': 1, 'COPAS': 2, 'OUROS': 3, 'PAUS': 4}
SUITS_SPANISH = {'ESPADAS': 1, 'COPAS': 2, 'OROS': 3, 'BASTOS': 4}

VALUES_ANGLO_AMERICAN = {'AS':1, 'J':11, 'Q':12, 'K':13}
VALUES_PORTUGUESE = {'AS':1, 'J':11, 'Q':12, 'K':13}
VALUES_SPANISH_48 = {'Q':10, 'J':11, 'K':12}
VALUES_SPANISH_40 = {'Q':8, 'J':9, 'K':10}
VALUES_ITALIAN_36 = {'J':7, 'Q':8, 'K':9}
VALUES_ITALIAN_40 = {'J':8, 'Q':9, 'K':10}
VALUES_ITALIAN_52 = {'J':11, 'Q':12, 'K':13}


def distributeCards(deck, stacks, amount):
  for x in range(amount):
    for stack in stacks:
      if not deck.isEmpty():
        stack.push(deck.pop())
      else: return

def strToStackOfCards(string):
  '''
  Example: 2-2 3-3 4-4 ...
  '''
  stack = StackOfCards()
  if string != None and string != '':
    for card in string.split(' '):
      tokens = card.split('-')
      stack.push(Card(int(tokens[0]), int(tokens[1])))
  return stack