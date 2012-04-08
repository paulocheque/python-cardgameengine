'''

@author: Paulo Cheque (paulocheque@gmail.com)
'''

import unittest

from cardgameengine import cardgame
from cardgameengine import commands
from cardgameengine import players
from cardgameengine import cards
from cardgameengine.constants import *

from cardgames import truco

###############################################################################
# [optional] 1): Define the kind of Cards that your game has

class TrucoCardTests(unittest.TestCase):
  
  def testValues(self):
    self.assertEquals([], truco.TrucoCard.values)
    
  def testSuits(self):
    self.assertEquals([], truco.TrucoCard.suits)
    
###############################################################################
# [required] 2): Define the rules of command's execution

class TrucoRoundContextTests(unittest.TestCase):
  
  def setUp(self):
    self.context = truco.TrucoRoundContext()
    
  def testAttributes(self):
    # self.assertEquals(somevalue, self.context.someattr)
    pass
  
  def testSummary(self):
    self.assertEquals('TrucoRoundContext', self.context.summary())
    
###############################################################################
# [required] 3): Define player's commands

class TrucoCommandTests(unittest.TestCase):
  
  def setUp(self):
    self.context = truco.TrucoRoundContext()
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.player = self.players[0]
    self.params = None
    self.game = truco.TrucoCardGame(self.players)
    self.game.newRound()
    self.command = truco.TrucoCommand(self.player, self.params, self.context)
  
  def testIsValid(self):
    self.assertTrue(self.command.isValid())
    # self.context.someflag = False
    self.command.execute(self.game, self.currentRound)
    self.assertFalse(self.command.isValid())
  
  def testExecuteMustDoSomething(self):
    self.command.execute(self.game, self.currentRound)
    self.assertEquals(0, self.game.currentRound.seeTrucoCards(self.player).height())
  
###############################################################################
# [required] 4): Define strategies to a player

class TrucoStrategyTests(unittest.TestCase):

  def setUp(self):
    self.deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(truco.TrucoCard, 4, 13, 2, 2)
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = truco.TrucoCardGame(self.players)
    self.round = truco.TrucoRound(self.game, self.players, commands.CommandsManager(self.game))
    self.strategy = truco.TrucoStrategy()
    self.context = truco.TrucoRoundContext()

  def testPlay(self):
    self.strategy.play(self.game.commandsManager, self.context)
      
###############################################################################
# [optional] 5): Define a model of reports to store informations.

class TrucoRoundReportTests(unittest.TestCase):
  
  def setUp(self):
    self.report = truco.TrucoRoundReport()
  
  def testBasicAttributes(self):
    self.report.players
    self.report.initialNumberOfPlayers
    self.report.durationTime
    self.report.winners
    self.report.commands
    self.report.algorithmsErrors
  
class TrucoCardGameReportTests(unittest.TestCase):
  
  def setUp(self):
    self.report = truco.TrucoCardGameReport()
  
  def testBasicAttributes(self):
    self.report.players
    self.report.initialNumberOfPlayers
    self.report.durationTime
    self.report.winners
    self.report.roundsReports

###############################################################################
# [required] 6) Create the logic of a round of the game:

class TrucoRoundTests(unittest.TestCase):
  
  def setUp(self):
    self.deckPrototype = cards.DeckPrototypeBuilder.createCommonDeck(truco.TrucoCard, 4, 13, 2, 2)
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = truco.TrucoCardGame(self.players)
    self.round = truco.TrucoRound(self.game, self.players, commands.CommandsManager(self.game))
  
  def testPopulateContext(self):
    context = truco.TrucoRoundContext()
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

class TrucoConfigurationsTests(unittest.TestCase):

  def setUp(self):
    self.deckPrototype = truco.TrucoConfigurations().deckPrototype.clone()
    
  def testHeight(self):
    self.assertEquals(108, len(self.deckPrototype.cards))
    
  def testContainCards(self):
    self.assertTrue(self.deckPrototype.containsCard(truco.TrucoCard(0, 0)))
    self.assertFalse(self.deckPrototype.containsCard(truco.TrucoCard(15, 4)))
    
  def testScore(self):
    self.assertEquals(20, self.deckPrototype.popCard(hole.HoleCard(0, 0)).score)
    self.assertEquals(5, self.deckPrototype.popCard(hole.HoleCard(3, 1)).score)

  def testAttributes(self):
    pass
    
###############################################################################
# [required] 8) Create the logic of the game: Probably this is easy to create than TrucoRound class.

class TrucoCardGameTests(unittest.TestCase):
  
  def setUp(self):
    self.players = [players.Player('Player1'), players.Player('Player2')]
    self.game = truco.TrucoCardGame(self.players)
  
  def testValidCommands(self):
    self.assertEquals([], truco.TrucoCardGame.validCommands)
  
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
   