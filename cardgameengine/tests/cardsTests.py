'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest

from cardgameengine import cards

class CardTest(unittest.TestCase):
  
  def testCardHasSuiteValue(self):
    card = cards.Card(1, 2)
    self.assertEquals(card.value, 1)
    self.assertEquals(card.suit, 2)
    
  def testEqualsCompareValueAndSuite(self):
    self.assertEquals(cards.Card(1, 2), cards.Card(1, 2))
    self.assertNotEquals(cards.Card(1, 1), cards.Card(1, 2))
    self.assertNotEquals(cards.Card(1, 1), cards.Card(2, 1))
    
  def testOrderUseOnlyValue(self):
    self.assertTrue(cards.Card(1, 2) < cards.Card(2, 1))
    self.assertTrue(cards.Card(2, 1) > cards.Card(1, 1))
    self.assertTrue(cards.Card(1, 1) <= cards.Card(1, 2))
    self.assertTrue(cards.Card(1, 1) >= cards.Card(1, 2))
    
  def testCardHasADefaultRepresentationUsingValueAndSuit(self):
    self.assertEquals('1-2', str(cards.Card(1, 2)))
    self.assertEquals('50-53', str(cards.Card(50, 53)))
    
  def testCardCanHaveMapsOfValuesAndSuitsToCustomizeItsRepresentation(self):
    class MyCard(cards.Card):
      values = {1:'AS'}
      suits = {1:'PAUS', 2:'COPAS'}
    self.assertEquals('1-1', str(cards.Card(1, 1)))
    self.assertEquals('AS-PAUS', str(MyCard(1, 1)))
    self.assertEquals('AS-COPAS', str(MyCard(1, 2)))
    self.assertEquals('AS-4', str(MyCard(1, 4)))
    self.assertEquals('3-COPAS', str(MyCard(3, 2)))
    self.assertEquals('3-4', str(MyCard(3, 4)))

class ValueCardTest(unittest.TestCase):
  
  def testEqualsCompareOnlyValueIgnoringSuite(self):
    self.assertEquals(cards.ValueCard('a', 'b'), cards.ValueCard('a', 'b'))
    self.assertEquals(cards.ValueCard('a', 'a'), cards.ValueCard('a', 'b'))
    self.assertNotEquals(cards.ValueCard('a', 'a'), cards.ValueCard('b', 'a'))

class SuitCardTest(unittest.TestCase):
  
  def testOrderUseValueAndSuit(self):
    self.assertTrue(cards.SuitCard(1, 2) < cards.SuitCard(2, 1))
    self.assertTrue(cards.SuitCard(2, 1) > cards.SuitCard(1, 2))
    self.assertTrue(cards.SuitCard(1, 1) < cards.SuitCard(1, 2))
    self.assertTrue(cards.SuitCard(1, 2) > cards.SuitCard(1, 1))
    
class StackOfCards(unittest.TestCase):
  
  def testToString(self):
    deck = cards.StackOfCards()
    self.assertEquals('', str(deck))
    deck.push(cards.Card(1, 1))
    self.assertEquals('1-1', str(deck))
    deck.push(cards.Card(2, 2))
    self.assertEquals('1-1 2-2', str(deck))
    deck.push(cards.Card(11, 5))
    self.assertEquals('1-1 2-2 11-5', str(deck))
    
  def testStackMustBePrototype(self):
    deck = cards.strToStackOfCards('1-2 2-1 4-1 6-1')
    self.assertEquals(deck, deck.clone())
    self.assertNotEquals(id(deck), id(deck.clone()))
    
    
  def testToStringWithMappedCards(self):
    class MappedCard(cards.Card):
      values = {1:'AS'}
      suits = {1:'PAUS', 2:'COPAS'}
    deck = cards.StackOfCards()
    self.assertEquals('', str(deck))
    deck.push(MappedCard(1, 1))
    self.assertEquals('AS-PAUS', str(deck))
    deck.push(MappedCard(2, 2))
    self.assertEquals('AS-PAUS 2-COPAS', str(deck))
    deck.push(MappedCard(11, 5))
    self.assertEquals('AS-PAUS 2-COPAS 11-5', str(deck))
  
  def testPushPop(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    self.assertEquals(1, deck.height())
    deck.pop()
    self.assertEquals(0, deck.height())
    deck.push(cards.Card(2, 1))
    self.assertEquals(1, deck.height())
    deck.push(cards.Card(3, 1))
    self.assertEquals(2, deck.height())
    deck.pop()
    deck.pop()
    self.assertEquals(0, deck.height())
    
  def testIsEmpty(self):
    deck = cards.StackOfCards()
    self.assertTrue(deck.isEmpty())
    deck.push(cards.Card(1, 1))
    self.assertFalse(deck.isEmpty())
    deck.pop()
    self.assertTrue(deck.isEmpty())
    
  def testPushAll(self):
    deck = cards.StackOfCards()
    deck2 = cards.StackOfCards()
    deck2.push(cards.Card(1, 1))
    deck2.push(cards.Card(2, 2))
    deck.pushAll(deck2)
    self.assertEquals(2, deck.height())
    self.assertEquals(2, deck2.height())
    self.assertEquals(cards.Card(2, 2), deck.pop())
    self.assertEquals(1, deck.height())
    self.assertEquals(cards.Card(1, 1), deck.pop())
    self.assertEquals(0, deck.height())
  
  def testPushAllAcceptCardOrStackOrList(self): 
    deck = cards.StackOfCards()
    deck.pushAll(cards.Card(1, 1))
    self.assertEquals(1, deck.height())
    
    deck2 = cards.StackOfCards()
    deck2.push(cards.Card(1, 1))
    deck.pushAll(deck2)
    self.assertEquals(2, deck.height())
    
    deck.pushAll([cards.Card(1, 1)])
    self.assertEquals(3, deck.height())
    
  def testPushPopAcceptSimilarCards(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(1, 1))
    self.assertEquals(2, deck.height())
    
  def testPushAllPopAll(self):
    deck1 = cards.StackOfCards()
    deck1.pushAll([cards.Card(1, 1), cards.Card(2, 2)])
    self.assertEquals(2, deck1.height())
    deck2 = cards.StackOfCards()
    deck2.pushAll(deck1.popAll())
    self.assertEquals(0, deck1.height())
    self.assertEquals(2, deck2.height())
    
  def testPopAll(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 2))
    self.assertEquals(2, deck.height())
    self.assertEquals(cards.strToStackOfCards('1-1 2-2'), deck.popAll())
    self.assertEquals(0, deck.height())
    
  def testPopCard(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    self.assertEquals(1, deck.height())
    self.assertEquals(cards.Card(1, 1), deck.popCard(cards.Card(1, 1)))
    self.assertEquals(0, deck.height())
    deck.push(cards.Card(2, 1))
    self.assertEquals(1, deck.height())
    deck.push(cards.Card(3, 1))
    self.assertEquals(2, deck.height())
    self.assertEquals(cards.Card(3, 1), deck.popCard(cards.Card(3, 1)))
    self.assertEquals(1, deck.height())
    self.assertEquals(cards.Card(2, 1), deck.popCard(cards.Card(2, 1)))
    self.assertEquals(0, deck.height())
    
  def testPopIndex(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 1))
    deck.push(cards.Card(3, 1))
    self.assertEquals(cards.Card(2, 1), deck.popIndex(1))
    self.assertEquals(cards.Card(3, 1), deck.popIndex(1))
    self.assertEquals(cards.Card(1, 1), deck.popIndex(0))
  
  def testPopCards(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 2))
    deck.push(cards.Card(3, 3))
    deck.push(cards.Card(4, 4))
    self.assertEquals(cards.strToStackOfCards('1-1 2-2'), 
                      deck.popCards([cards.Card(1, 1), cards.Card(2, 2)]))
    self.assertEquals(2, deck.height())
    self.assertEquals(cards.strToStackOfCards('3-3'), deck.popCards([cards.Card(3, 3)]))
    self.assertEquals(1, deck.height())
    self.assertEquals(cards.strToStackOfCards('4-4'), deck.popCards([cards.Card(4, 4)]))
    self.assertEquals(0, deck.height())
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 2))
    self.assertEquals(cards.strToStackOfCards('1-1 2-2'), 
                      deck.popCards(deck.cards))
    
  def testPopCardsAcceptCardOrStackOrList(self): 
    deck = cards.StackOfCards()
    deck.pushAll(cards.Card(1, 1))
    deck.pushAll(cards.Card(2, 1))
    deck.pushAll(cards.Card(3, 1))
    self.assertEquals(cards.strToStackOfCards('1-1'), deck.popCards(cards.Card(1, 1)))
    self.assertEquals(cards.strToStackOfCards('2-1'), deck.popCards([cards.Card(2, 1)]))
    self.assertEquals(cards.strToStackOfCards('3-1'), deck.popCards(deck))
    
  
  def testPopCardsWithValue(self):
    deck = cards.StackOfCards()
    self.assertEquals(cards.StackOfCards(), deck.popCardsWithValue(1))
    
    deck = cards.strToStackOfCards('1-2 2-1 4-1 2-2')
    self.assertEquals(cards.strToStackOfCards('1-2'), deck.popCardsWithValue(1))
    self.assertEquals(3, deck.height())
    
    deck = cards.strToStackOfCards('1-2 2-1 4-1 2-2')
    self.assertEquals(cards.strToStackOfCards('2-1 2-2'), deck.popCardsWithValue(2))
    self.assertEquals(2, deck.height())
    
    deck = cards.strToStackOfCards('1-2 2-1 4-1 2-2')
    self.assertEquals(cards.strToStackOfCards(''), deck.popCardsWithValue(3))
    
    deck = cards.strToStackOfCards('1-2 2-1 4-1 2-2')
    self.assertEquals(cards.strToStackOfCards('4-1'), deck.popCardsWithValue(4))
  
  def testPopCardsWithSuit(self):
    deck = cards.StackOfCards()
    self.assertEquals(cards.StackOfCards(), deck.popCardsWithSuit(1))
    
    deck = cards.strToStackOfCards('1-2 2-1 4-1 2-2')
    self.assertEquals(cards.strToStackOfCards('2-1 4-1'), deck.popCardsWithSuit(1))
    self.assertEquals(2, deck.height())
    
    deck = cards.strToStackOfCards('1-2 2-1 4-1 2-2')
    self.assertEquals(cards.strToStackOfCards('1-2 2-2'), deck.popCardsWithSuit(2))
    
    deck = cards.strToStackOfCards('1-2 2-1 4-1 2-2')
    self.assertEquals(cards.strToStackOfCards(''), deck.popCardsWithSuit(3))
    self.assertEquals(4, deck.height())
    
  def testSee(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 2))
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(2, 2), deck.see(1))
    self.assertEquals(cards.Card(1, 1), deck.seeFirstCard())
    self.assertEquals(cards.Card(2, 2), deck.seeLastCard())
    
  def testConstainsCard(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(2, 2))
    deck.push(cards.Card(1, 1))
    self.assertTrue(deck.containsCard(cards.Card(1, 1)))
    self.assertTrue(deck.containsCard(cards.Card(2, 2)))
    self.assertFalse(deck.containsCard(cards.Card(1, 2)))
    self.assertFalse(deck.containsCard(cards.Card(2, 1)))
    
  def testConstainsCardWithValue(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(2, 3))
    deck.push(cards.Card(1, 1))
    self.assertTrue(deck.containsCardWithValue(1))
    self.assertTrue(deck.containsCardWithValue(2))
    self.assertFalse(deck.containsCardWithValue(3))
    self.assertFalse(deck.containsCardWithValue(4))
    
  def testConstainsCardWithSuit(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(2, 3))
    deck.push(cards.Card(1, 1))
    self.assertTrue(deck.containsCardWithSuit(3))
    self.assertTrue(deck.containsCardWithSuit(1))
    self.assertFalse(deck.containsCardWithSuit(2))
    self.assertFalse(deck.containsCardWithSuit(4))
    
  def testConstainsCardWithSuitCards(self):
    deck = cards.StackOfCards()
    deck.push(cards.SuitCard(2, 2))
    deck.push(cards.SuitCard(1, 1))
    self.assertTrue(deck.containsCard(cards.SuitCard(1, 1)))
    self.assertTrue(deck.containsCard(cards.SuitCard(2, 2)))
    self.assertFalse(deck.containsCard(cards.SuitCard(1, 2)))
    self.assertFalse(deck.containsCard(cards.SuitCard(2, 1)))
    
  def testConstainsCardWithValueCards(self):
    deck = cards.StackOfCards()
    deck.push(cards.ValueCard(2, 2))
    deck.push(cards.ValueCard(1, 1))
    self.assertTrue(deck.containsCard(cards.ValueCard(1, 1)))
    self.assertTrue(deck.containsCard(cards.ValueCard(2, 2)))
    self.assertTrue(deck.containsCard(cards.ValueCard(1, 3)))
    self.assertTrue(deck.containsCard(cards.ValueCard(2, 3)))
    self.assertFalse(deck.containsCard(cards.ValueCard(3, 3)))
    
  def testConstainsAllCards(self):
    deck = cards.strToStackOfCards('1-1 2-2 3-3')
    deck1 = cards.strToStackOfCards('1-1 2-2 3-3')
    deck2 = cards.strToStackOfCards('1-1 2-2')
    deck3 = cards.strToStackOfCards('1-1 4-4')
    self.assertTrue(deck.containsAllCards(deck))
    self.assertTrue(deck.containsAllCards(deck1))
    self.assertTrue(deck.containsAllCards(deck2))
    self.assertFalse(deck.containsAllCards(deck3))
    
    self.assertTrue(deck.containsAllCards(deck.cards))
    self.assertTrue(deck.containsAllCards(deck1.cards))
    self.assertTrue(deck.containsAllCards(deck2.cards))
    self.assertFalse(deck.containsAllCards(deck3.cards))
    
  def testConstainsAllCardsAcceptCardOrStackOrList(self): 
    deck = cards.StackOfCards()
    deck.pushAll(cards.Card(1, 1))
    self.assertTrue(deck.containsAllCards(cards.Card(1, 1)))
    self.assertTrue(deck.containsAllCards(deck))
    self.assertTrue(deck.containsAllCards([cards.Card(1, 1)]))

  def testCompareByHeight(self):
    deck = cards.strToStackOfCards('1-1 2-2 3-3')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3')
    self.assertEquals(0, deck.compareByHeight(deck2))
    self.assertEquals(0, deck2.compareByHeight(deck))
    
    deck = cards.strToStackOfCards('1-1 2-2 4-4')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3')
    self.assertEquals(0, deck.compareByHeight(deck2))
    self.assertEquals(0, deck2.compareByHeight(deck))
    
    deck = cards.strToStackOfCards('1-1 2-2')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3 4-4')
    self.assertEquals(-2, deck.compareByHeight(deck2))
    self.assertEquals(2, deck2.compareByHeight(deck))
    
    deck = cards.strToStackOfCards('')
    deck2 = cards.strToStackOfCards('1-1')
    self.assertEquals(-1, deck.compareByHeight(deck2))
    self.assertEquals(1, deck2.compareByHeight(deck))
    
  def testCompareByHighValue(self):
    deck = cards.strToStackOfCards('1-1 2-2 3-3')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3')
    self.assertEquals(0, deck.compareByHighValue(deck2))
    self.assertEquals(0, deck2.compareByHighValue(deck))
    
    deck = cards.strToStackOfCards('1-1 2-2 4-4')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3')
    self.assertEquals(1, deck.compareByHighValue(deck2))
    self.assertEquals(-1, deck2.compareByHighValue(deck))
    
    deck = cards.strToStackOfCards('2-2 2-2 5-4')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3')
    self.assertEquals(2, deck.compareByHighValue(deck2))
    self.assertEquals(-2, deck2.compareByHighValue(deck))
    
    deck = cards.strToStackOfCards('1-1 2-2')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3 4-4')
    self.assertEquals(-2, deck.compareByHighValue(deck2))
    self.assertEquals(2, deck2.compareByHighValue(deck))
    
    deck = cards.strToStackOfCards('1-1 5-5')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3 4-4')
    self.assertEquals(3, deck.compareByHighValue(deck2))
    self.assertEquals(-3, deck2.compareByHighValue(deck))
    
    deck = cards.strToStackOfCards('1-1 2-2')
    deck2 = cards.strToStackOfCards('1-1 3-3 3-3 4-4')
    self.assertEquals(-1, deck.compareByHighValue(deck2))
    self.assertEquals(1, deck2.compareByHighValue(deck))

  def testCompareByLowValue(self):
    deck = cards.strToStackOfCards('1-1 2-2 3-3')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3')
    self.assertEquals(0, deck.compareByLowValue(deck2))
    self.assertEquals(0, deck2.compareByLowValue(deck))
    
    deck = cards.strToStackOfCards('1-1 2-2 4-4')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3')
    self.assertEquals(-1, deck.compareByLowValue(deck2))
    self.assertEquals(1, deck2.compareByLowValue(deck))
    
    deck = cards.strToStackOfCards('2-2 2-2 5-4')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3')
    self.assertEquals(-1, deck.compareByLowValue(deck2))
    self.assertEquals(1, deck2.compareByLowValue(deck))
    
    deck = cards.strToStackOfCards('1-1 2-2')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3 4-4')
    self.assertEquals(-2, deck.compareByLowValue(deck2))
    self.assertEquals(2, deck2.compareByLowValue(deck))
    
    deck = cards.strToStackOfCards('1-1 5-5')
    deck2 = cards.strToStackOfCards('1-1 2-2 3-3 4-4')
    self.assertEquals(-3, deck.compareByLowValue(deck2))
    self.assertEquals(3, deck2.compareByLowValue(deck))
    
    deck = cards.strToStackOfCards('1-1 2-2')
    deck2 = cards.strToStackOfCards('1-1 3-3 3-3 4-4')
    self.assertEquals(1, deck.compareByLowValue(deck2))
    self.assertEquals(-1, deck2.compareByLowValue(deck))
    
  def testNumberOfCards(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 2))
    deck.push(cards.Card(1, 2))
    deck.push(cards.Card(1, 2))
    deck.push(cards.Card(3, 3))
    self.assertEquals(1, deck.numberOfCards(cards.Card(1, 1)))
    self.assertEquals(2, deck.numberOfCards(cards.Card(1, 2)))
    self.assertEquals(1, deck.numberOfCards(cards.Card(2, 2)))
    self.assertEquals(1, deck.numberOfCards(cards.Card(3, 3)))
    self.assertEquals(0, deck.numberOfCards(cards.Card(3, 4)))
    self.assertEquals(0, deck.numberOfCards(cards.Card(4, 3)))
    self.assertEquals(0, deck.numberOfCards(cards.Card(4, 4)))
    
  def testNumberOfCardsWithValue(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 2))
    deck.push(cards.Card(1, 2))
    deck.push(cards.Card(1, 2))
    deck.push(cards.Card(3, 3))
    self.assertEquals(3, deck.numberOfCardsWithValue(1))
    self.assertEquals(1, deck.numberOfCardsWithValue(2))
    self.assertEquals(1, deck.numberOfCardsWithValue(3))
    self.assertEquals(0, deck.numberOfCardsWithValue(4))
    
  def testNumberOfCardsWithSuit(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 2))
    deck.push(cards.Card(1, 2))
    deck.push(cards.Card(1, 2))
    deck.push(cards.Card(3, 3))
    self.assertEquals(1, deck.numberOfCardsWithSuit(1))
    self.assertEquals(3, deck.numberOfCardsWithSuit(2))
    self.assertEquals(1, deck.numberOfCardsWithSuit(3))
    self.assertEquals(0, deck.numberOfCardsWithSuit(4))
    
  def testScoreMustSumScoreOfEachCard(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(10, 1))
    deck.push(cards.Card(10, 2))
    deck.push(cards.Card(3, 10))
    self.assertEquals(0, deck.score())
    
    deck.push(cards.Card(1, 1, 7))
    deck.push(cards.Card(1, 1, 1))
    deck.push(cards.Card(10, 10))
    deck.push(cards.Card(10, 10, 8))
    self.assertEquals(16, deck.score())
    
  def testSortDefaultCardThatIsOrderedOnlyByValue(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(4, 2))
    deck.push(cards.Card(4, 1))
    deck.push(cards.Card(2, 1))
    deck.sort()
    self.assertEquals(cards.Card(4, 1), deck.pop())
    self.assertEquals(cards.Card(4, 2), deck.pop())
    self.assertEquals(cards.Card(2, 1), deck.pop())
    self.assertEquals(cards.Card(1, 1), deck.pop())

  def testSortSuitCardThatIsOrderedByValueAndSuit(self):
    deck = cards.StackOfCards()
    deck.push(cards.SuitCard(1, 1))
    deck.push(cards.SuitCard(4, 2))
    deck.push(cards.SuitCard(4, 1))
    deck.push(cards.SuitCard(2, 1))
    deck.sort()
    self.assertEquals(cards.SuitCard(4, 2), deck.pop())
    self.assertEquals(cards.SuitCard(4, 1), deck.pop())
    self.assertEquals(cards.SuitCard(2, 1), deck.pop())
    self.assertEquals(cards.SuitCard(1, 1), deck.pop())
    
  def testSortByValue(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(4, 2))
    deck.push(cards.Card(4, 1))
    deck.push(cards.Card(2, 1))
    deck.sortByValue()
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(2, 1), deck.see(1))
    self.assertEquals(cards.Card(4, 2), deck.see(2))
    self.assertEquals(cards.Card(4, 1), deck.see(3))
    
  def testSortBySuit(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(4, 2))
    deck.push(cards.Card(4, 1))
    deck.push(cards.Card(2, 1))
    deck.sortBySuit()
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(4, 1), deck.see(1))
    self.assertEquals(cards.Card(2, 1), deck.see(2))
    self.assertEquals(cards.Card(4, 2), deck.see(3))
    
  def testSortByValueAndSuit(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(4, 2))
    deck.push(cards.Card(4, 1))
    deck.push(cards.Card(2, 1))
    deck.sortByValueAndSuit()
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(2, 1), deck.see(1))
    self.assertEquals(cards.Card(4, 1), deck.see(2))
    self.assertEquals(cards.Card(4, 2), deck.see(3))
    
  def testSortBySuitAndValue(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(4, 2))
    deck.push(cards.Card(4, 1))
    deck.push(cards.Card(2, 1))
    deck.sortBySuitAndValue()
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(2, 1), deck.see(1))
    self.assertEquals(cards.Card(4, 1), deck.see(2))
    self.assertEquals(cards.Card(4, 2), deck.see(3))
    
  def testSortByScore(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1, 15))
    deck.push(cards.Card(4, 2, 15))
    deck.push(cards.Card(4, 1, 20))
    deck.push(cards.Card(2, 1, 11))
    deck.sortByScore()
    self.assertEquals(cards.Card(2, 1, 11), deck.see(0))
    self.assertEquals(cards.Card(1, 1, 15), deck.see(1))
    self.assertEquals(cards.Card(4, 2, 15), deck.see(2))
    self.assertEquals(cards.Card(4, 1, 20), deck.see(3))
    
  def testShuffle(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 1))
    deck.push(cards.Card(3, 1))
    deck.push(cards.Card(4, 1))
    deck.shuffle()
    self.assertTrue(
                   cards.Card(4, 1) != deck.pop() or
                   cards.Card(3, 1) != deck.pop() or
                   cards.Card(2, 1) != deck.pop() or
                   cards.Card(4, 1) != deck.pop())
    
  def testAllCardsWithSameValue(self):
    deck = cards.StackOfCards()
    self.assertTrue(deck.allCardsWithSameValue())
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(1, 2))
    self.assertTrue(deck.allCardsWithSameValue())
    deck.push(cards.Card(2, 1))
    self.assertFalse(deck.allCardsWithSameValue())

  def testAllCardsWithSameSuit(self):
    deck = cards.StackOfCards()
    self.assertTrue(deck.allCardsWithSameSuit())
    deck.push(cards.Card(1, 1))
    deck.push(cards.Card(2, 1))
    self.assertTrue(deck.allCardsWithSameSuit())
    deck.push(cards.Card(3, 2))
    self.assertFalse(deck.allCardsWithSameSuit())
    
  def testAllCardsWithSameValueAndSuit(self):
    deck = cards.StackOfCards()
    self.assertTrue(deck.allCardsWithSameValueAndSuit())
    deck.push(cards.Card(1, 1))
    self.assertTrue(deck.allCardsWithSameValueAndSuit())
    deck.push(cards.Card(1, 1))
    self.assertTrue(deck.allCardsWithSameValueAndSuit())
    deck.push(cards.Card(1, 2))
    self.assertFalse(deck.allCardsWithSameValueAndSuit())
    deck.pop()
    self.assertTrue(deck.allCardsWithSameValueAndSuit())
    deck.push(cards.Card(2, 1))
    self.assertFalse(deck.allCardsWithSameValueAndSuit())
  
  def testAllCardsInSequence(self):
    deck = cards.StackOfCards()
    self.assertTrue(deck.allCardsInSequence())
    deck.push(cards.Card(2, 2))
    self.assertTrue(deck.allCardsInSequence())
    deck.push(cards.Card(1, 1))
    self.assertTrue(deck.allCardsInSequence())
    deck.push(cards.Card(4, 1))
    self.assertFalse(deck.allCardsInSequence())
    
  def testAllCardsInSequenceWithSameSuit(self):
    deck = cards.StackOfCards()
    self.assertTrue(deck.allCardsInSequenceWithSameSuit())
    deck.push(cards.Card(2, 1))
    self.assertTrue(deck.allCardsInSequenceWithSameSuit())
    deck.push(cards.Card(1, 1))
    self.assertTrue(deck.allCardsInSequenceWithSameSuit())
    deck.push(cards.Card(4, 1))
    self.assertFalse(deck.allCardsInSequenceWithSameSuit())
    deck.pop()
    self.assertTrue(deck.allCardsInSequenceWithSameSuit())
    deck.push(cards.Card(3, 2))
    self.assertFalse(deck.allCardsInSequenceWithSameSuit())
    
  def testAllCardsInSequenceWithJokers(self):
    deck = cards.strToStackOfCards('1-2 2-1 4-1')
    self.assertFalse(deck.allCardsInSequenceWithJokers(0))
    self.assertTrue(deck.allCardsInSequenceWithJokers(1))
    self.assertTrue(deck.allCardsInSequenceWithJokers(2))
    
    deck = cards.strToStackOfCards('1-2 2-1 5-1')
    self.assertFalse(deck.allCardsInSequenceWithJokers(1))
    self.assertTrue(deck.allCardsInSequenceWithJokers(2))
    
    deck = cards.strToStackOfCards('1-2 2-1 4-1 6-1')
    self.assertFalse(deck.allCardsInSequenceWithJokers(1))
    self.assertTrue(deck.allCardsInSequenceWithJokers(2))
    
    deck = cards.strToStackOfCards('1-2 2-1 5-1 7-1')
    self.assertFalse(deck.allCardsInSequenceWithJokers(1))
    self.assertFalse(deck.allCardsInSequenceWithJokers(2))
    self.assertTrue(deck.allCardsInSequenceWithJokers(3))
    
    deck = cards.strToStackOfCards('13-1 12-1 13-1')
    self.assertFalse(deck.allCardsInSequenceWithJokers(1))
    self.assertFalse(deck.allCardsInSequenceWithJokers(2))
  
  def testAllCardsInSequenceWithSameSuitWithJokers(self):
    suitdeck = cards.strToStackOfCards('1-1 2-1 4-1')
    deck = cards.strToStackOfCards('1-2 2-1 4-1')
    self.assertFalse(suitdeck.allCardsInSequenceWithSameSuitWithJokers(0))
    self.assertFalse(deck.allCardsInSequenceWithSameSuitWithJokers(1))
    self.assertFalse(deck.allCardsInSequenceWithSameSuitWithJokers(2))
    self.assertTrue(suitdeck.allCardsInSequenceWithSameSuitWithJokers(1))
    self.assertTrue(suitdeck.allCardsInSequenceWithSameSuitWithJokers(2))
    
    suitdeck = cards.strToStackOfCards('1-1 2-1 5-1')
    deck = cards.strToStackOfCards('1-2 2-1 5-1')
    self.assertFalse(suitdeck.allCardsInSequenceWithSameSuitWithJokers(1))
    self.assertFalse(deck.allCardsInSequenceWithSameSuitWithJokers(2))
    self.assertTrue(suitdeck.allCardsInSequenceWithSameSuitWithJokers(2))
    
    suitdeck = cards.strToStackOfCards('1-1 2-1 4-1 6-1')
    deck = cards.strToStackOfCards('1-2 2-1 4-1 6-1')
    self.assertFalse(suitdeck.allCardsInSequenceWithSameSuitWithJokers(1))
    self.assertFalse(deck.allCardsInSequenceWithSameSuitWithJokers(2))
    self.assertTrue(suitdeck.allCardsInSequenceWithSameSuitWithJokers(2))
    
    suitdeck = cards.strToStackOfCards('1-1 2-1 5-1 7-1')
    deck = cards.strToStackOfCards('1-2 2-1 5-1 7-1')
    self.assertFalse(suitdeck.allCardsInSequenceWithSameSuitWithJokers(1))
    self.assertFalse(suitdeck.allCardsInSequenceWithSameSuitWithJokers(2))
    self.assertFalse(deck.allCardsInSequenceWithSameSuitWithJokers(3))
    self.assertTrue(suitdeck.allCardsInSequenceWithSameSuitWithJokers(3))
    
  # combinations and combinations
    
  def testAllCombinationsOfOneCard(self):
    stack = cards.strToStackOfCards('3-1')
    combinations = stack.allCombinationsOfCards()
    self.assertEquals(1, len(combinations))
    self.assertTrue(cards.strToStackOfCards('3-1') in combinations)
    
  def testAllCombinationsOfTwoCards(self):
    stack = cards.strToStackOfCards('3-1 4-1')
    combinations = stack.allCombinationsOfCards()
    self.assertEquals(3, len(combinations))
    self.assertTrue(cards.strToStackOfCards('3-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('4-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 4-1') in combinations)
    
  def testAllCombinationsOfThreeCards(self):
    stack = cards.strToStackOfCards('3-1 4-1 5-1')
    combinations = stack.allCombinationsOfCards()
    self.assertEquals(7, len(combinations))
    self.assertTrue(cards.strToStackOfCards('3-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('4-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 4-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('4-1 5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 4-1 5-1') in combinations)
    
  def testAllCombinationsOfRepeatedCards(self):
    stack = cards.strToStackOfCards('3-1 3-1 5-1')
    combinations = stack.allCombinationsOfCards()
    self.assertEquals(7, len(combinations))
    self.assertTrue(cards.strToStackOfCards('3-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 3-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 3-1 5-1') in combinations)
    
  def testAllCombinationsWithMinMax(self):
    stack = cards.strToStackOfCards('3-1 4-1 5-1')
    combinations = stack.allCombinationsOfCards(1, 1)
    self.assertEquals(3, len(combinations))
    self.assertTrue(cards.strToStackOfCards('3-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('4-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('5-1') in combinations)
    
    combinations = stack.allCombinationsOfCards(1, 2)
    self.assertEquals(6, len(combinations))
    self.assertTrue(cards.strToStackOfCards('3-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('4-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 4-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('4-1 5-1') in combinations)
    
    combinations = stack.allCombinationsOfCards(2, 2)
    self.assertEquals(3, len(combinations))
    self.assertTrue(cards.strToStackOfCards('3-1 4-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('4-1 5-1') in combinations)

    combinations = stack.allCombinationsOfCards(2, 3)
    self.assertEquals(4, len(combinations))
    self.assertTrue(cards.strToStackOfCards('3-1 4-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('3-1 5-1') in combinations)
    self.assertTrue(cards.strToStackOfCards('4-1 5-1') in combinations)    
    self.assertTrue(cards.strToStackOfCards('3-1 4-1 5-1') in combinations)
    
  def testAllCombinationsWithMinAndMaxGreaterThanHeight(self):
    stack = cards.strToStackOfCards('3-1 4-1 5-1')
    combinations = stack.allCombinationsOfCards(4, 5)
    self.assertEquals(0, len(combinations))
    combinations = stack.allCombinationsOfCards(4, 0)
    self.assertEquals(0, len(combinations))
    
  def testAllCombinationsWithMaxLowerThanMin(self):
    stack = cards.strToStackOfCards('3-1 4-1 5-1')
    combinations = stack.allCombinationsOfCards(2, 1)
    self.assertEquals(0, len(combinations))
    
    
  def testPerformanceOfAllCombinationsOfRepeatedCards(self):
    cardsString = ' '.join([(str(i) + '-1') for i in range(1, 15+1)])
    stack = cards.strToStackOfCards(cardsString)
    combinations = stack.allCombinationsOfCards()
    self.assertEquals(32767, len(combinations))
    
class DeckPrototypeTest(unittest.TestCase):
  
  def testCloneForEmptyDeck(self):
    deck = cards.StackOfCards()
    self.assertEquals(deck, deck.clone())
    self.assertTrue(deck is not deck.clone())
    
  def testCloneMustCopyCardsInOrder(self):
    deck = cards.StackOfCards()
    deck.push(cards.Card(1, 2))
    deck.push(cards.Card(2, 3))
    deck.push(cards.Card(7, 1))
    clone = deck.clone()
    self.assertEquals(deck, clone)
    self.assertTrue(deck is not clone)
    self.assertEquals(3, clone.height())
    self.assertEquals(cards.Card(1, 2), clone.see(0))
    self.assertEquals(cards.Card(2, 3), clone.see(1))
    self.assertEquals(cards.Card(7, 1), clone.see(2))
    
class DeckPrototypeBuilderTest(unittest.TestCase):
  
  def testCreateCommonDeck(self):
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.Card, 1, 1, 1)
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.Card, 2, 1, 1)
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(1, 2), deck.see(1))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.Card, 1, 2, 1)
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(2, 1), deck.see(1))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.Card, 1, 1, 2)
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(1, 1), deck.see(1))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.Card, 2, 2, 2)
    self.assertEquals(cards.Card(1, 1), deck.see(0))
    self.assertEquals(cards.Card(1, 2), deck.see(1))
    self.assertEquals(cards.Card(1, 1), deck.see(2))
    self.assertEquals(cards.Card(1, 2), deck.see(3))
    self.assertEquals(cards.Card(2, 1), deck.see(4))
    self.assertEquals(cards.Card(2, 2), deck.see(5))
    self.assertEquals(cards.Card(2, 1), deck.see(6))
    self.assertEquals(cards.Card(2, 2), deck.see(7))
    
  def testCreateCommonDeckWithSuitCard(self):
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.SuitCard, 1, 1, 1)
    self.assertEquals(cards.SuitCard(1, 1), deck.see(0))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.SuitCard, 2, 1, 1)
    self.assertEquals(cards.SuitCard(1, 1), deck.see(0))
    self.assertEquals(cards.SuitCard(1, 2), deck.see(1))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.SuitCard, 1, 2, 1)
    self.assertEquals(cards.SuitCard(1, 1), deck.see(0))
    self.assertEquals(cards.SuitCard(2, 1), deck.see(1))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.SuitCard, 1, 1, 2)
    self.assertEquals(cards.SuitCard(1, 1), deck.see(0))
    self.assertEquals(cards.SuitCard(1, 1), deck.see(1))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.SuitCard, 2, 2, 2)
    self.assertEquals(cards.SuitCard(1, 1), deck.see(0))
    self.assertEquals(cards.SuitCard(1, 1), deck.see(1))
    self.assertEquals(cards.SuitCard(1, 2), deck.see(2))
    self.assertEquals(cards.SuitCard(1, 2), deck.see(3))
    self.assertEquals(cards.SuitCard(2, 1), deck.see(4))
    self.assertEquals(cards.SuitCard(2, 1), deck.see(5))
    self.assertEquals(cards.SuitCard(2, 2), deck.see(6))
    self.assertEquals(cards.SuitCard(2, 2), deck.see(7))
    
  def testCreateCommonDeckWithJokers(self):
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.SuitCard, 1, 1, 1, 2)
    self.assertEquals(cards.SuitCard(0, 0), deck.see(0))
    self.assertEquals(cards.SuitCard(0, 0), deck.see(1))
    self.assertEquals(cards.SuitCard(1, 1), deck.see(2))
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.SuitCard, 1, 1, 2, 2)
    self.assertEquals(cards.SuitCard(0, 0), deck.see(0))
    self.assertEquals(cards.SuitCard(0, 0), deck.see(1))
    self.assertEquals(cards.SuitCard(0, 0), deck.see(2))
    self.assertEquals(cards.SuitCard(0, 0), deck.see(3))
    self.assertEquals(cards.SuitCard(1, 1), deck.see(4))
    self.assertEquals(cards.SuitCard(1, 1), deck.see(5))
    
  def testCreateCommomDeckWithScore(self):
    def scoreFunction(value, suit):
      if value == 0: return 20
      if value == 1: return 15
      if value == 2: return 10
      if value >= 3 and value <= 7: return 5
      if value >= 8 and value <= 13: return 10
      return 0
    deck = cards.DeckPrototypeBuilder.createCommonDeck(cards.Card, 1, 13, 1, 1, scoreFunction)
    self.assertEquals(20, deck.popCard(cards.Card(0, 0)).score)
    self.assertEquals(15, deck.popCard(cards.Card(1, 1)).score)
    self.assertEquals(10, deck.popCard(cards.Card(2, 1)).score)
    self.assertEquals(5, deck.popCard(cards.Card(3, 1)).score)
    self.assertEquals(10, deck.popCard(cards.Card(8, 1)).score)
  
class UsefulMethodsTests(unittest.TestCase):
  
  def setUp(self):
    self.deck = cards.StackOfCards()
    self.deck.pushAll([cards.Card(1,1), cards.Card(2,1), 
                       cards.Card(3,1), cards.Card(4,1),
                       cards.Card(5,1)])
  
  def testDistributeOneCardsFromDeckTo1Stack(self):
    stacks = [cards.StackOfCards()]
    cards.distributeCards(self.deck, stacks, 1)
    self.assertEquals(4, self.deck.height())
    self.assertEquals(1, stacks[0].height())
  
  def testDistributeOneCardsFromDeckTo2Stacks(self):
    stacks = [cards.StackOfCards(), cards.StackOfCards()]
    cards.distributeCards(self.deck, stacks, 1)
    self.assertEquals(3, self.deck.height())
    self.assertEquals(1, stacks[0].height())
    self.assertEquals(1, stacks[1].height())
    
  def testDistributeTwoCardsFromDeckTo2Stacks(self):
    stacks = [cards.StackOfCards(), cards.StackOfCards()]
    cards.distributeCards(self.deck, stacks, 2)
    self.assertEquals(1, self.deck.height())
    self.assertEquals(2, stacks[0].height())
    self.assertEquals(2, stacks[1].height())
    
  def testDistributeThreeCardsFromDeckTo2Stacks(self):
    stacks = [cards.StackOfCards(), cards.StackOfCards()]
    cards.distributeCards(self.deck, stacks, 3)
    self.assertEquals(0, self.deck.height())
    self.assertEquals(3, stacks[0].height())
    self.assertEquals(2, stacks[1].height())
  
  def testDistributeOneCardsFromDeckTo3Stacks(self):
    stacks = [cards.StackOfCards(), cards.StackOfCards(), cards.StackOfCards()]
    cards.distributeCards(self.deck, stacks, 1)
    self.assertEquals(2, self.deck.height())
    self.assertEquals(1, stacks[0].height())
    self.assertEquals(1, stacks[1].height())
    self.assertEquals(1, stacks[2].height())
    
class StringToStackTests(unittest.TestCase):
  
  def testStringNoneToStack(self):
    self.assertEquals(cards.StackOfCards(), cards.strToStackOfCards(None))
    
  def testStringEmptyToStack(self):
    self.assertEquals(cards.StackOfCards(), cards.strToStackOfCards(''))
    
  def testStringWithOneCardToStack(self):
    stack = cards.StackOfCards()
    stack.push(cards.Card(1, 2))
    self.assertEquals(stack, cards.strToStackOfCards('1-2'))
    
  def testStringWithTwoCardsToStack(self):
    stack = cards.StackOfCards()
    stack.push(cards.Card(1, 2))
    stack.push(cards.Card(3, 3))
    self.assertEquals(stack, cards.strToStackOfCards('1-2 3-3'))
    
  def testStringWithALotOfCardsToStack(self):
    stack = cards.StackOfCards()
    stack.push(cards.Card(1, 2))
    stack.push(cards.Card(5, 5))
    stack.push(cards.Card(50, 7))
    stack.push(cards.Card(123, 2))
    self.assertEquals(stack, cards.strToStackOfCards('1-2 5-5 50-7 123-2'))
  
  def testInvalidString(self):
    try:
      cards.strToStackOfCards('1/2')
    except: pass
    else: self.fail()
    try:
      cards.strToStackOfCards('1 2')
    except: pass
    else: self.fail()
    try:
      cards.strToStackOfCards('asdasd')
    except: pass
    else: self.fail()
    
    
  
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()