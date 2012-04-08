'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import threading
import time
import re

import unittest
from gameengine import testhelper

from gameengine import game, commands, players, utils, errors

###############################################################################
# Context

class ContextTest(unittest.TestCase):
  
  def testContextHasHistoricOfCommands(self):
    context = game.Context()
    self.assertEquals(None, context.player)
    self.assertEquals(None, context.currentGamePlayers)
    self.assertEquals(None, context.configurations)
    
  def testToStringIsSummary(self):
    class MyContext(game.Context): pass
    self.assertEquals(MyContext().summary(), str(MyContext()))    
    
  def testContextMustBeObserver(self):
    self.assertTrue(isinstance(game.Context(), utils.Observer))

###############################################################################

class GameReportTest(testhelper.GameEngineTests):

  def basicAttributesGameReport(self, report):
    self.assertEquals([], report.players)
    self.assertEquals(0, report.initialNumberOfPlayers)
    self.assertEquals(None, report.configurations)
    self.assertEquals([], report.winners)
    self.assertEquals([], report.losers)
    self.assertEquals([], report.commands)
    self.assertEquals({}, report.playersDurationTime)
    self.assertEquals(0, report.durationTime)
    self.assertEquals(None, report.exception)
  
  def testBasicAttributesGameReport(self):
    self.basicAttributesGameReport(self.gamereport)
    
  def addItem(self, list, addMethod):
    self.assertEquals([], list)
    addMethod('x')
    self.assertEquals(['x'], list)
    
  def testAddContentToReport(self):
    self.addItem(self.gameofroundsreport.players, self.gameofroundsreport.addPlayers)
    self.addItem(self.gameofroundsreport.winners, self.gameofroundsreport.addWinners)
    self.addItem(self.gameofroundsreport.losers, self.gameofroundsreport.addLosers)
    
class GameOfRoundsReportTest(testhelper.GameEngineTests):
    
  def testBasicAttributesGameOfRounds(self):
    self.assertEquals([], self.gameofroundsreport.roundsReports)
    
  def testAddRoundReport(self):
    self.assertEquals([], self.gameofroundsreport.roundsReports)
    self.gameofroundsreport.addRoundReport('x')
    self.assertEquals(['x'], self.gameofroundsreport.roundsReports)
    
###############################################################################
    
class ConfigurationTest(testhelper.GameEngineTests):
  
  def testDefaultConfigurationHasInfiniteTimeForPlayingAndGaming(self):
    self.assertEquals(-1, game.Configurations().timeForCommand)
    self.assertEquals(-1, game.Configurations().timeForPlay)
    self.assertEquals(-1, game.Configurations().timeForGame)
    
  def testConfigurationsAcceptTimeForPlayAndForGame(self):
    c = game.Configurations(2, 3, 5)
    self.assertEquals(2, c.timeForCommand)
    self.assertEquals(3, c.timeForPlay)
    self.assertEquals(5, c.timeForGame)
    
  def testConfigurationIsOptional(self):
    mygame = testhelper.MyGame(self.twoplayers)
    self.assertTrue(isinstance(mygame.configurations, game.Configurations))
    mygame = testhelper.MyGame(self.twoplayers, self.configurations)
    self.assertEquals(self.configurations, mygame.configurations)

    
###############################################################################

class MyStrategy(players.Strategy):
  def play(self, commandsManager):
    commandsManager.addCommand(testhelper.SlowCommand(1))
    commandsManager.addCommand(testhelper.FinishCommand())
    
class GameTest(testhelper.GameEngineTests):

  def testName(self):
    self.assertEquals('My', testhelper.MyGame.name())
    self.assertEquals('My', self.game.name())
  
  def testCardGameAbstractMethods(self):
    self.game.isTheEnd()
    self.game.report()
    
  def testStartMustStopIfTheGameIsEnd(self):
    class StrategyForTests(players.Strategy):
      def play(self, commandsManager):
        commandsManager.addCommand(testhelper.SlowCommand(self.player, 0.1))
        commandsManager.addCommand(testhelper.FinishCommand(self.player))
    configurations = game.Configurations(0.2, 0.3, 0.4)
    someplayers = players.Player('Player1', StrategyForTests())
    testgame = testhelper.MyGame([someplayers], configurations)
    testgame.start()
    self.assertFalse(testgame.thread.isAlive())
    
  def testStartMustStopIfTheTimeForGameIsExpired(self):
    class StrategyForTests(players.Strategy):
      def play(self, commandsManager):
        commandsManager.addCommand(testhelper.SlowCommand(self.player, 1))
        commandsManager.addCommand(testhelper.FinishCommand(self.player))
    configurations = game.Configurations(2, 2, 0.1)
    someplayers = players.Player('Player1', StrategyForTests())
    testgame = testhelper.MyGame([someplayers], configurations)
    try:
      testgame.start()
    except: pass
    else: self.fail()
    self.assertEquals(str(errors.TimeoutGameError()), 
                      testgame.report().exception.message)
    self.assertFalse(testgame.thread.isAlive())
    
  def testStartMustStopIfTheTimeForPlayIsExpired(self):
    class StrategyForTests(players.Strategy):
      def play(self, commandsManager):
        commandsManager.addCommand(testhelper.SlowCommand(self.player, 1))
        commandsManager.addCommand(testhelper.FinishCommand(self.player))
    configurations = game.Configurations(2, 0.1, 2)
    someplayers = players.Player('Player1', StrategyForTests())
    testgame = testhelper.MyGame([someplayers], configurations)
    try:
      testgame.start()
    except: pass
    else: self.fail()
    self.assertTrue(re.search(str(errors.TimeoutStrategyError()) + ': Player1', 
                   testgame.report().exception.message))
    self.assertFalse(testgame.thread.isAlive())
    
  def testStartMustStopIfTheTimeForCommandIsExpired(self):
    class StrategyForTests(players.Strategy):
      def play(self, commandsManager):
        commandsManager.addCommand(testhelper.SlowCommand(self.player, 1))
        commandsManager.addCommand(testhelper.FinishCommand(self.player))
    configurations = game.Configurations(0.1, 2, 2)
    someplayers = players.Player('Player1', StrategyForTests())
    testgame = testhelper.MyGame([someplayers], configurations)
    try:
      testgame.start()
    except: pass
    else: self.fail()
    self.assertTrue(re.search(errors.TimeoutCommandError.__doc__ + ': Slow, Player1, 1 - 0.0s', 
                   testgame.report().exception.message))
    self.assertFalse(testgame.thread.isAlive())
    
  def testStartMustStopIfTheCommandManagerReceiveAnUnknownCommand(self):
    class StrategyForTests(players.Strategy):
      def play(self, commandsManager):
        commandsManager.addCommand(testhelper.UnknownCommand(self.player))
    configurations = game.Configurations(0.1, 2, 2)
    someplayers = players.Player('Player1', StrategyForTests())
    testgame = testhelper.MyGame([someplayers], configurations)
    try:
      testgame.start()
    except: pass
    else: self.fail()
    self.assertTrue(re.search(errors.UnknownCommandError.__doc__.replace('(', '\(').replace(')', '\)'), 
                    testgame.report().exception.message))
    self.assertFalse(testgame.thread.isAlive())
    
  def testStartMustStopIfTheCommandManagerReceiveAnInvalidCommand(self):
    class StrategyForTests(players.Strategy):
      def play(self, commandsManager):
        commandsManager.addCommand(testhelper.InvalidCommand(self.player))
    configurations = game.Configurations(0.1, 2, 2)
    someplayers = players.Player('Player1', StrategyForTests())
    testgame = testhelper.MyGame([someplayers], configurations)
    try:
      testgame.start()
    except: pass
    else: self.fail()
    self.assertTrue(re.search(errors.InvalidCommandError.__doc__, 
                    testgame.report().exception.message))
    self.assertFalse(testgame.thread.isAlive())
    
  def testStartMustStopIfTheCommandManagerReceiveABuggedCommand(self):
    class StrategyForTests(players.Strategy):
      def play(self, commandsManager):
        commandsManager.addCommand(testhelper.BuggedCommand(self.player))
    configurations = game.Configurations(0.1, 2, 2)
    someplayers = players.Player('Player1', StrategyForTests())
    testgame = testhelper.MyGame([someplayers], configurations)
    try:
      testgame.start()
    except: pass
    else: self.fail()
    self.assertTrue(re.search(errors.BuggedCommandError.__doc__, 
                    testgame.report().exception.message))
    self.assertFalse(testgame.thread.isAlive())

###############################################################################

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()