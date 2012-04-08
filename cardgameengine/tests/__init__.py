'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

'''
=Example of unit tests for your game=

{{{
# File called: mygameTests.py
# Tip: Replace all text called 'mygame' to name of your game module
# This is a simple skeleton!!!

import unittest

from gameengine import commands, players, errors
from cardgameengine.constants import *
from cardgameengine import cards, cardgame

from cardgames import mygame

###############################################################################
# [optional] 0): Define base class with common data to clear testcases

class GameTestsHelper(unittest.TestCase):

  def setUp(self):
    self.players = [players.Player('Player1', 
                                   strategy=mygame.Strategy(), 
                                   contextClass=mygame.Context), 
                    players.Player('Player2', 
                                   strategy=mygame.Strategy(), 
                                   contextClass=mygame.Context)]
    self.player = self.players[0]
    self.strategy = self.player.strategy
    self.context = self.player.context
    
    self.params = None
    self.startGameCommand = simplepokertexasholdem.StartGameCommand()
    self.endGameCommand = simplepokertexasholdem.EndGameCommand()
    self.startGameRoundCommand = simplepokertexasholdem.StartGameRoundCommand()
    self.endGameRoundCommand = simplepokertexasholdem.EndGameRoundCommand()
    self.playerPlaysCommand = simplepokertexasholdem.PlayerPlaysGameCommand()
    self.command = simplepokertexasholdem.FooCommand(self.player, self.params)
    
    self.roundreport = mygame.RoundReport()
    self.report = mygame.GameReport()
    self.configurations = mygame.Configurations()
    self.deckPrototype = self.configurations.deckPrototype.clone()
    
    self.game = mygame.Game(self.players, self.configurations)
    self.round = mygame.Round(self.game, self.players[:], self.configurations, self.game.commandsManager)
    self.round.currentPlayer = self.player
    self.game.currentRound = self.round

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class CardTests(GameTestsHelper):
  
  def testValues(self):
    self.assertEquals({'Q': 12, 'AS': 1, 'J': 11, 'K': 13}, 
                      mygame.Card.values)
    
  def testSuits(self):
    self.assertEquals({'HEARTS': 2, 'CLUBS': 4, 'SPADES': 1, 'DIAMONDS': 3},
                       mygame.Card.suits)
    
###############################################################################
# [optional] 2) Define configurations of the game

class ConfigurationsTests(GameTestsHelper):

  def setUp(self):
    super(ConfigurationsTests, self).setUp()
    self.deckPrototype = mygame.Configurations().deckPrototype.clone()

  def testHeight(self):
    self.assertEquals(53, len(self.deckPrototype.cards))
    
  def testContainCards(self):
    self.assertTrue(self.deckPrototype.containsCard(mygame.Card(0, 0)))
    self.assertFalse(self.deckPrototype.containsCard(mygame.Card(15, 4)))
    
  def testScore(self):
    self.assertEquals(20, self.deckPrototype.popCard(mygame.Card(0, 0)).score)
    self.assertEquals(5, self.deckPrototype.popCard(mygame.Card(3, 1)).score)

  def testAttributes(self):
    self.assertEquals(-1, self.configurations.timeForPlay)
    
###############################################################################
# [required] 3): Define the rules of command's execution

class ContextTests(GameTestsHelper):
  
  def testAttributes(self):
    self.assertEquals(self.player, self.context.player)
    self.assertEquals(None, self.context.currentGamePlayers)
    self.assertEquals(None, self.context.configurations)
    
    self.assertEquals(None, self.context.playercards)
    
    # more attributes
  
###############################################################################
# [required] 4) Card game logic

#################################
# [optional] 4.1): Define a model of reports to store informations.

class GameReportTests(GameTestsHelper):
  
  def testBasicAttributes(self):
    self.assertEquals([], self.report.players)
    self.assertEquals(0, self.report.initialNumberOfPlayers)
    self.assertEquals(None, self.report.configurations)
    self.assertEquals([], self.report.winners)
    self.assertEquals([], self.report.losers)
    self.assertEquals([], self.report.commands)
    self.assertEquals(0, self.report.durationTime)

#################################s
# [required] 4.2) Create the logic of the game

class GameTests(GameTestsHelper):
  
  def setUp(self):
    super(GameTests, self).setUp()
  
  def testAttributes(self):
    pass
  
  def testValidCommands(self):
    self.assertTrue(mygame.StartGameCommand in self.game.commandsManager.validCommands)
    self.assertTrue(mygame.EndGameCommand in self.game.commandsManager.validCommands)
    self.assertTrue(mygame.PlayerPlaysGameCommand in self.game.commandsManager.validCommands)
  
  def testConditionToWin(self): 
    pass

###############################################################################
# [required] 5) Round logic

#################################
# [optional] 5.1): Define a model of reports to store informations

class RoundReportTests(GameTestsHelper):
  
  def testBasicAttributes(self):
    self.assertEquals([], self.roundreport.players)
    self.assertEquals(0, self.roundreport.initialNumberOfPlayers)
    self.assertEquals(None, self.roundreport.configurations)
    self.assertEquals([], self.roundreport.winners)
    self.assertEquals([], self.roundreport.losers)
    self.assertEquals([], self.roundreport.commands)
    self.assertEquals(0, self.roundreport.durationTime)

#################################
# [required] 5.2) Create the logic of a round of the game:

class RoundTests(GameTestsHelper):
  
  def testAttributes(self):
    pass
  
  def testConditionToWin(self): 
    pass

###############################################################################
# [required] 6): Define game's commands

class StartGameCommandTests(GameTestsHelper):

  def testExecuteMustDoSomething(self):
    self.startGameCommand.execute(self.game)
    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())
    
class EndGameCommandTests(GameTestsHelper):

  def testExecuteMustDoSomething(self):
    self.endGameCommand.execute(self.game)
    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())
    
class StartGameRoundCommandTests(GameTestsHelper):

  def testExecuteMustDoSomething(self):
    self.startGameRoundCommand.execute(self.game)
    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())
    
class EndGameRoundCommandTests(GameTestsHelper):

  def testExecuteMustDoSomething(self):
    self.endGameRoundCommand.execute(self.game)
    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())
    
class PlayerPlaysGameCommandTests(GameTestsHelper):

  def testExecuteMustDoSomething(self):
    self.playerPlaysCommand.execute(self.game)
    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())

###############################################################################
# [required] 7): Define player's commands

class PlayerCommandTests(GameTestsHelper):
  
  def testValidate(self):
    self.command.validate(self.context)
    
  def testValidateRaiseAnInvalidCommandError(self):
    try:
      self.context.flag = False
      self.command.validate(self.context)
    except simplepokertexasholdem.FooInvalidCommandError: pass
    else: self.fail()
    
  def testValidateRaiseACheatCommandError(self):
    try:
      self.context.flag = None
      self.command.validate(self.context)
    except simplepokertexasholdem.FooCheatCommandError: pass
    else: self.fail()
  
  def testExecuteMustDoSomething(self):
    self.context.flag = True
    self.command.validate(self.context)
    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())
  
###############################################################################
# [required] 8): Define strategies to a player

class StrategyTests(GameTestsHelper):

  def testPlay(self):
    self.strategy.play(self.game.commandsManager)
      
###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 

# more tests here


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
}}}
'''