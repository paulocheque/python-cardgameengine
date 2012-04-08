'''

@author: Paulo Cheque (paulocheque@gmail.com)
@author: Ricardo Yamamoto (ricardoy@gmail.com)
'''
'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

# File called: mygameTests.py
# Tip: Replace all text called 'mygame' to name of your game module
# Tip: Replace all text called 'My' to name of your game
# This is a simple skeleton!!!

import unittest

from cardgameengine import cardgame
from cardgameengine import commands
from cardgameengine import players
from cardgameengine import cards
from cardgameengine.constants import *

from cardgames import mygame

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class MyCardTests(unittest.TestCase):
  
  def testValues(self):
    self.assertEquals([], mygame.MyCard.values)
    
  def testSuits(self):
    self.assertEquals([], mygame.MyCard.suits)
    
###############################################################################
# [required] 2): Define the rules of command's execution

class MyRoundContextTests(unittest.TestCase):
  
  def setUp(self):
    self.context = mygame.MyRoundContext()
    
  def testAttributes(self):
    # self.assertEquals(somevalue, self.context.someattr)
    pass
  
  def testSummary(self):
    self.assertEquals('MyRoundContext', self.context.summary())
    
###############################################################################
# [required] 3): Define player's commands

class MyCommandTests(unittest.TestCase):
  
  def setUp(self):
    self.context = mygame.MyRoundContext()
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.player = self.players[0]
    self.params = None
    self.game = mygame.MyCardGame(self.players)
    self.game.newRound()
    self.command = mygame.MyCommand(self.player, self.params, self.context)
  
  def testIsValid(self):
    self.assertTrue(self.command.isValid())
    # self.context.someflag = False
    self.command.execute(self.game, self.currentRound)
    self.assertFalse(self.command.isValid())
  
  def testExecuteMustDoSomething(self):
    self.command.execute(self.game, self.currentRound)
    self.assertEquals(0, self.game.currentRound.seeCards(self.player).height())
  
###############################################################################
# [required] 4): Define strategies to a player

class MyStrategyTests(unittest.TestCase):

  def setUp(self):
    self.deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(mygame.MyCard, 4, 13, 2, 2)
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = mygame.MyCardGame(self.players)
    self.round = mygame.MyRound(self.game, self.players, commands.CommandsManager(self.game))
    self.strategy = mygame.MyStrategy()
    self.context = mygame.MyRoundContext()

  def testPlay(self):
    self.strategy.play(self.game.commandsManager, self.context)
      
###############################################################################
# [optional] 5): Define a model of reports to store informations.

class MyRoundReportTests(unittest.TestCase):
  
  def setUp(self):
    self.report = mygame.MyRoundReport()
  
  def testBasicAttributes(self):
    self.report.players
    self.report.initialNumberOfPlayers
    self.report.durationTime
    self.report.winners
    self.report.commands
    self.report.algorithmsErrors
  
class MyCardGameReportTests(unittest.TestCase):
  
  def setUp(self):
    self.report = mygame.MyCardGameReport()
  
  def testBasicAttributes(self):
    self.report.players
    self.report.initialNumberOfPlayers
    self.report.durationTime
    self.report.winners
    self.report.roundsReports

###############################################################################
# [required] 6) Create the logic of a round of the game:

class MyRoundTests(unittest.TestCase):
  
  def setUp(self):
    self.deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(mygame.MyCard, 4, 13, 2, 2)
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = mygame.MyCardGame(self.players)
    self.round = mygame.MyRound(self.game, self.players, commands.CommandsManager(self.game))
  
  def testPopulateContext(self):
    context = mygame.MyRoundContext()
    self.round.populateContext(context)
    # self.assertEquals('', context.attr1)
  
  def testOrganize(self):
    pass
  
  def testEnd(self):
    pass
  
  def testConditionToWin(self): 
    pass

###############################################################################
# [optional] 7) Define configurations of the game

class MyConfigurationsTests(unittest.TestCase):

  def setUp(self):
    self.deckPrototype = mygame.MyConfigurations().deckPrototype.clone()
    
  def testHeight(self):
    self.assertEquals(108, len(self.deckPrototype.cards))
    
  def testContainCards(self):
    self.assertTrue(self.deckPrototype.containsCard(mygame.MyCard(0, 0)))
    self.assertFalse(self.deckPrototype.containsCard(mygame.MyCard(15, 4)))
    
  def testScore(self):
    self.assertEquals(20, self.deckPrototype.popCard(hole.HoleCard(0, 0)).score)
    self.assertEquals(5, self.deckPrototype.popCard(hole.HoleCard(3, 1)).score)

  def testAttributes(self):
    pass
    
###############################################################################
# [required] 8) Create the logic of the game: Probably this is easy to create than MyRound class.

class MyCardGameTests(unittest.TestCase):
  
  def setUp(self):
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = mygame.MyCardGame(self.players)
  
  def testValidCommands(self):
    self.assertEquals([], mygame.MyCardGame.validCommands)
  
  def testOrganize(self):
    pass
  
  def testEnd(self):
    pass
  
  def testConditionToWin(self): 
    pass


###############################################################################
# [optional] 9) Another classes (custom) to encapsulate things and algorithms. 

# more tests here


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
