'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import threading
import time

import unittest

from gameengine import commands, players, utils
from cardgameengine import cards, cardgame, testhelper

class ReportTest(testhelper.CardGameEngineTests):
  
  def basicAttributes(self, report):
    self.assertEquals([], report.players)
    self.assertEquals(0, report.initialNumberOfPlayers)
    self.assertEquals(0, report.durationTime)
    self.assertEquals([], report.winners)
    
  def testRoundReport(self):
    self.basicAttributes(self.roundreport)
    self.assertEquals([], self.roundreport.commands)
    
  def testCardGameReport(self):
    self.basicAttributes(self.cardgamereport)
    self.assertEquals(None, self.cardgamereport.configurations)
    self.assertEquals([], self.cardgamereport.roundsReports)
    
class RoundContextTest(testhelper.CardGameEngineTests):
  
  def testContextHasHistoricOfCommandsAndRound(self):
    self.assertEquals(None, self.context.player)
    self.assertEquals(None, self.context.playercards)
    self.assertEquals(None, self.context.currentGamePlayers)
    self.assertEquals(None, self.context.configurations)
    
###############################################################################
    
class RoundTest(testhelper.CardGameEngineTests):
  
  def testRoundDefaultInitialization(self):
    self.round = testhelper.MyRound(self.game, self.twoplayers[:], self.configurations)
    self.assertTrue(isinstance(self.round.game, testhelper.MyCardGame))
    self.assertEquals(testhelper.deck, self.round.deck)
    self.assertTrue(self.round.deck is not testhelper.deck)
    self.assertEquals(self.twoplayers, self.round.players)
    self.assertTrue(isinstance(self.round.report(), testhelper.MyRoundReport))
    self.assertEquals({'Player1': cards.StackOfCards(), 'Player2': cards.StackOfCards()}, self.round.playersCards)
    self.assertEquals(None, self.round.currentPlayer)
    
  def testRoundAbstractMethods(self):
    # abstract method
    self.round.organize()
    self.round.isTheEnd()
    self.round.end()
    self.round.report()
    self.round.populateContext(None)
    self.round.winners()
    
  def testSeeCards(self):
    self.assertTrue(isinstance(self.round.seeCards(self.twoplayers[0]), cards.StackOfCards))
    self.assertTrue(isinstance(self.round.seeCards(self.twoplayers[1]), cards.StackOfCards))
    self.assertTrue(self.round.seeCards(self.twoplayers[0]) is not self.round.seeCards(self.twoplayers[1]))
    
  def testNumberOfPlayers(self):
    self.assertEquals(2, self.round.numberOfPlayers())

  def testWhoIsPlaying(self):
    self.assertEquals(self.player, self.round.whoIsPlaying())
    
  def testReportGetInitializationInformations(self):
    self.assertEquals(self.twoplayers, self.round.report().players)
    self.assertEquals(2, self.round.report().initialNumberOfPlayers)
    self.assertEquals(0, self.round.report().durationTime)
    self.assertEquals([], self.round.report().winners)
    
  def testDistributeCardsToAllPlayers(self):
    self.assertEquals(0, self.round.seeCards(self.twoplayers[0]).height())
    self.assertEquals(0, self.round.seeCards(self.twoplayers[1]).height())
    self.round.distributeCardsToAllPlayers(2)
    self.assertEquals(2, self.round.seeCards(self.twoplayers[0]).height())
    self.assertEquals(2, self.round.seeCards(self.twoplayers[1]).height())
  
###############################################################################

class ConfigurationTest(testhelper.CardGameEngineTests):
  
  def testConfigurationHasStackOfCards(self):
    self.game.configurations.deckPrototype
  
  def testConfigurationIsOptional(self):
    game = testhelper.MyCardGame(self.twoplayers)
    self.assertEquals(None, game.configurations)
    game = testhelper.MyCardGame(self.twoplayers, self.configurations)
    self.assertEquals(self.configurations, game.configurations)
  
###############################################################################
    
class CardGameTest(testhelper.CardGameEngineTests):

  def testName(self):
    self.assertEquals('My', testhelper.MyCardGame.name())
    self.assertEquals('My', self.game.name())
  
  def testCardGameAbstractMethods(self):
    self.game.organize()
    self.game.isTheEnd()
    self.game.end()
    self.game.report()
    
  def testNumberOfPlayersDontDependsOnTheRound(self):
    self.assertEquals(2, self.game.numberOfPlayers())
    self.assertEquals(2, self.round.numberOfPlayers())
    self.round.removePlayer(self.twoplayers[0])
    self.assertEquals(2, self.game.numberOfPlayers())
    self.assertEquals(1, self.round.numberOfPlayers())
    self.game.removePlayer(self.twoplayers[0])
    self.assertEquals(1, self.game.numberOfPlayers())
    self.assertEquals(1, self.round.numberOfPlayers())
    
  def testNumberOfRounds(self):
    self.assertEquals(0, self.game.numberOfRounds())

  def testRegisteredClasses(self):
    self.assertTrue(utils.CombinationGenerator in cardgame.accessibleClasses)
    self.assertTrue(cards.StackOfCards in cardgame.accessibleClasses)

###############################################################################

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()